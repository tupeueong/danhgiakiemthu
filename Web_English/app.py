from __future__ import annotations

import csv
import io
import os
import unicodedata
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from flask import Flask, jsonify, render_template, request
from sqlalchemy import case, func, inspect, or_, text, update

from models import (
    FormulaNote,
    ReviewLog,
    Setting,
    SpeedReviewItem,
    SpeedReviewSession,
    Word,
    WordExample,
    WordProgress,
    db,
)
from srs import (
    LEARNING_STEPS,
    SRS_INTERVALS,
    SRS_LABELS,
    apply_learning_result,
    apply_review_result,
    utc_now,
)


DEFAULT_VOICE = "Microsoft Zira - English (United States)"
ALLOWED_VOICES = {
    "Microsoft Mark - English (United States)",
    "Microsoft Zira - English (United States)",
    "Google US English",
}
ALLOWED_STATES = {"all", "new", "learning", "learned", "due", "difficult"}
ALLOWED_MODES = {"learn", "review"}
SPEED_REVIEW_RULES = {
    "starting_hearts": 3,
    "extra_heart_streak": 15,
    "question_seconds": 8,
    "minimum_score": 100,
    "maximum_score": 1000,
}

PART_OF_SPEECH_ALIASES = {
    "n": "noun",
    "n.": "noun",
    "noun": "noun",
    "v": "verb",
    "v.": "verb",
    "verb": "verb",
    "adj": "adjective",
    "adj.": "adjective",
    "adjective": "adjective",
    "adv": "adverb",
    "adv.": "adverb",
    "adverb": "adverb",
    "pron": "pronoun",
    "pron.": "pronoun",
    "pronoun": "pronoun",
    "prep": "preposition",
    "prep.": "preposition",
    "preposition": "preposition",
    "conj": "conjunction",
    "conj.": "conjunction",
    "conjunction": "conjunction",
    "interj": "interjection",
    "interj.": "interjection",
    "int": "interjection",
    "int.": "interjection",
    "interjection": "interjection",
    "det": "determiner",
    "det.": "determiner",
    "determiner": "determiner",
    "art": "article",
    "art.": "article",
    "article": "article",
    "aux": "auxiliary verb",
    "aux.": "auxiliary verb",
    "auxiliary": "auxiliary verb",
    "auxiliary verb": "auxiliary verb",
    "modal": "modal verb",
    "modal.": "modal verb",
    "modal verb": "modal verb",
    "phrase": "phrase",
    "phr v": "phrasal verb",
    "phr. v.": "phrasal verb",
    "phrasal verb": "phrasal verb",
    "idiom": "idiom",
}


def iso_utc(value: datetime | None) -> str | None:
    return f"{value.isoformat(timespec='seconds')}Z" if value else None


def clean_text(value, max_length: int | None = None) -> str:
    result = " ".join(str(value or "").strip().split())
    return result[:max_length] if max_length else result


def validate_formula_content(data: dict) -> tuple[str | None, str | None]:
    if not isinstance(data, dict) or not isinstance(data.get("content"), str):
        return None, "Nội dung công thức phải là văn bản."

    normalized = data["content"].replace("\r\n", "\n").replace("\r", "\n").strip()
    content = "\n".join(line.rstrip() for line in normalized.split("\n"))
    if not content:
        return None, "Nội dung công thức không được để trống."
    if len(content) > 20_000:
        return None, "Mỗi ghi chú công thức chỉ được dài tối đa 20.000 ký tự."
    return content, None


def normalized_text_key(value) -> str:
    """Return a Unicode- and case-normalized key without changing displayed text."""
    return unicodedata.normalize("NFKC", clean_text(value)).casefold()


def normalize_part_of_speech(value) -> str:
    """Canonicalize common abbreviations while preserving sensible custom labels."""
    cleaned = unicodedata.normalize("NFKC", clean_text(value, 80))
    return PART_OF_SPEECH_ALIASES.get(cleaned.casefold(), cleaned)


def normalized_word_key(
    english: str,
    part_of_speech: str,
    vietnamese: str,
) -> tuple[str, str, str]:
    return (
        normalized_text_key(english),
        normalized_text_key(normalize_part_of_speech(part_of_speech)),
        normalized_text_key(vietnamese),
    )


def normalize_example_text(value: str) -> str:
    return unicodedata.normalize("NFKC", clean_text(value)).casefold()


def validate_examples_payload(data: dict) -> tuple[list[str] | None, str | None]:
    if "examples" in data:
        raw_examples = data.get("examples")
        if not isinstance(raw_examples, list):
            return None, "Danh sách câu ví dụ không hợp lệ."
    else:
        raw_examples = [data.get("example", "")]

    examples = []
    seen = set()
    for raw_example in raw_examples:
        if not isinstance(raw_example, str):
            return None, "Mỗi câu ví dụ phải là văn bản."
        example = clean_text(raw_example)
        if not example:
            continue
        if len(example) > 1500:
            return None, "Mỗi câu ví dụ chỉ được dài tối đa 1.500 ký tự."
        normalized = normalize_example_text(example)
        if normalized in seen:
            continue
        seen.add(normalized)
        examples.append(example)
    return examples, None


def usage_text_items(value: str) -> list[str]:
    """Read newline-delimited TEXT storage, including legacy one-line values."""
    items = []
    seen = set()
    for raw_item in str(value or "").splitlines():
        item = clean_text(raw_item)
        if not item:
            continue
        normalized = normalized_text_key(item)
        if normalized in seen:
            continue
        seen.add(normalized)
        items.append(item)
    return items


def validate_usage_list_payload(
    data: dict,
    plural_key: str,
    legacy_key: str,
    label: str,
) -> tuple[list[str] | None, str | None]:
    """Validate a list field, preferring its array form over legacy TEXT input."""
    if plural_key in data:
        raw_items = data.get(plural_key)
        if not isinstance(raw_items, list):
            return None, f"Danh sách {label} không hợp lệ."
    else:
        legacy_value = data.get(legacy_key, "")
        if not isinstance(legacy_value, str):
            return None, f"Trường {label} phải là văn bản."
        raw_items = legacy_value.splitlines()

    items = []
    seen = set()
    non_empty_count = 0
    for raw_item in raw_items:
        if not isinstance(raw_item, str):
            return None, f"Mỗi {label} phải là văn bản."
        item = clean_text(raw_item)
        if not item:
            continue
        non_empty_count += 1
        if non_empty_count > 100:
            return None, f"Mỗi từ chỉ được có tối đa 100 {label}."
        if len(item) > 500:
            return None, f"Mỗi {label} chỉ được dài tối đa 500 ký tự."
        normalized = normalized_text_key(item)
        if normalized in seen:
            continue
        seen.add(normalized)
        items.append(item)
    return items, None


def word_example_texts(word: Word) -> list[str]:
    examples = [example.text for example in word.examples]
    if examples:
        return examples
    return [word.example] if word.example else []


def replace_word_examples(word: Word, examples: list[str]) -> None:
    existing_by_key = {
        item.normalized_text: item
        for item in word.examples
    }
    ordered = []
    for position, example in enumerate(examples):
        normalized = normalize_example_text(example)
        item = existing_by_key.pop(normalized, None)
        if item is None:
            item = WordExample(normalized_text=normalized)
        item.text = example
        item.position = position
        ordered.append(item)
    word.examples = ordered
    # Keep the legacy column synchronized for older clients and backups.
    word.example = examples[0] if examples else ""


def migrate_legacy_examples() -> None:
    """Copy legacy words.example values into the child table without losing text."""
    for word in Word.query.order_by(Word.id).all():
        ordered = list(word.examples)
        legacy_text = word.example
        if legacy_text and normalize_example_text(legacy_text):
            legacy_key = normalize_example_text(legacy_text)
            matching = next(
                (item for item in ordered if item.normalized_text == legacy_key),
                None,
            )
            if matching is None:
                matching = WordExample(
                    text=legacy_text,
                    normalized_text=legacy_key,
                    position=0,
                )
                word.examples.append(matching)
            ordered = [matching, *(item for item in ordered if item is not matching)]

        for position, example in enumerate(ordered):
            example.position = position
        word.example = ordered[0].text if ordered else ""
    db.session.commit()


def serialize_word(word: Word) -> dict:
    progress = word.progress
    attempts = progress.correct_count + progress.incorrect_count
    examples = word_example_texts(word)
    collocations = usage_text_items(word.collocation)
    word_patterns = usage_text_items(word.word_pattern)
    return {
        "id": word.id,
        "english": word.english,
        "phonetic": word.phonetic,
        "vietnamese": word.vietnamese,
        "part_of_speech": word.part_of_speech,
        "collocation": "\n".join(collocations),
        "collocations": collocations,
        "word_pattern": "\n".join(word_patterns),
        "word_patterns": word_patterns,
        "example": examples[0] if examples else "",
        "examples": examples,
        "created_at": iso_utc(word.created_at),
        "progress": {
            "state": progress.state,
            "learning_step": progress.learning_step,
            "learning_total": LEARNING_STEPS,
            "srs_stage": progress.srs_stage,
            "srs_label": SRS_LABELS[progress.srs_stage],
            "next_review_at": iso_utc(progress.next_review_at),
            "last_reviewed_at": iso_utc(progress.last_reviewed_at),
            "correct_count": progress.correct_count,
            "incorrect_count": progress.incorrect_count,
            "accuracy": round(progress.correct_count / attempts * 100) if attempts else None,
            "is_difficult": progress.is_difficult,
        },
    }


def serialize_formula_note(note: FormulaNote) -> dict:
    return {
        "id": note.id,
        "content": note.content,
        "created_at": iso_utc(note.created_at),
        "updated_at": iso_utc(note.updated_at),
    }


def validate_word_payload(data: dict) -> tuple[dict | None, str | None]:
    english = clean_text(data.get("english"), 160)
    phonetic = clean_text(data.get("phonetic"), 160)
    vietnamese = clean_text(data.get("vietnamese"), 320)
    part_of_speech = normalize_part_of_speech(data.get("part_of_speech"))
    collocations, collocations_error = validate_usage_list_payload(
        data,
        "collocations",
        "collocation",
        "collocation",
    )
    if collocations_error:
        return None, collocations_error
    word_patterns, word_patterns_error = validate_usage_list_payload(
        data,
        "word_patterns",
        "word_pattern",
        "word pattern",
    )
    if word_patterns_error:
        return None, word_patterns_error
    examples, examples_error = validate_examples_payload(data)
    if examples_error:
        return None, examples_error
    if not english or not vietnamese:
        return None, "Tiếng Anh và nghĩa tiếng Việt là bắt buộc."
    return {
        "english": english,
        "phonetic": phonetic,
        "vietnamese": vietnamese,
        "part_of_speech": part_of_speech,
        "collocation": "\n".join(collocations),
        "word_pattern": "\n".join(word_patterns),
        "examples": examples,
    }, None


def find_duplicate(
    english: str,
    part_of_speech: str,
    vietnamese: str,
    exclude_id: int | None = None,
):
    target_key = normalized_word_key(english, part_of_speech, vietnamese)
    query = Word.query
    if exclude_id is not None:
        query = query.filter(Word.id != exclude_id)
    return next(
        (
            word
            for word in query
            if normalized_word_key(
                word.english,
                word.part_of_speech,
                word.vietnamese,
            )
            == target_key
        ),
        None,
    )


def create_word(record: dict) -> Word:
    record = record.copy()
    examples = record.pop("examples")
    word = Word(**record)
    replace_word_examples(word, examples)
    word.progress = WordProgress()
    db.session.add(word)
    return word


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    database_path = Path(app.instance_path) / "vocabulary.db"
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "LEXILOOP_DATABASE_URI",
            f"sqlite:///{database_path.as_posix()}",
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSON_SORT_KEYS=False,
        TEMPLATES_AUTO_RELOAD=True,
        SEND_FILE_MAX_AGE_DEFAULT=0,
    )
    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        word_columns = {column["name"] for column in inspect(db.engine).get_columns("words")}
        if "phonetic" not in word_columns:
            db.session.execute(
                text("ALTER TABLE words ADD COLUMN phonetic VARCHAR(160) NOT NULL DEFAULT ''")
            )
        if "collocation" not in word_columns:
            db.session.execute(
                text("ALTER TABLE words ADD COLUMN collocation TEXT NOT NULL DEFAULT ''")
            )
        if "word_pattern" not in word_columns:
            db.session.execute(
                text("ALTER TABLE words ADD COLUMN word_pattern TEXT NOT NULL DEFAULT ''")
            )
        db.session.commit()
        migrate_legacy_examples()
        if not db.session.get(Setting, "voice_name"):
            db.session.add(Setting(key="voice_name", value=DEFAULT_VOICE))
            db.session.commit()
        db.session.execute(text("PRAGMA optimize"))
        db.session.commit()

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/formulas")
    def get_formulas():
        notes = FormulaNote.query.order_by(
            FormulaNote.updated_at.desc(),
            FormulaNote.id.desc(),
        ).all()
        return jsonify(
            {
                "items": [serialize_formula_note(note) for note in notes],
                "total": len(notes),
            }
        )

    @app.post("/api/formulas")
    def add_formula():
        content, error = validate_formula_content(request.get_json(silent=True) or {})
        if error:
            return jsonify({"error": error}), 400
        note = FormulaNote(content=content)
        db.session.add(note)
        db.session.commit()
        return jsonify(
            {
                "message": "Đã thêm ghi chú công thức.",
                "formula": serialize_formula_note(note),
            }
        ), 201

    @app.put("/api/formulas/<int:formula_id>")
    def update_formula(formula_id: int):
        note = db.get_or_404(FormulaNote, formula_id)
        content, error = validate_formula_content(request.get_json(silent=True) or {})
        if error:
            return jsonify({"error": error}), 400
        note.content = content
        note.updated_at = utc_now()
        db.session.commit()
        return jsonify(
            {
                "message": "Đã cập nhật ghi chú công thức.",
                "formula": serialize_formula_note(note),
            }
        )

    @app.delete("/api/formulas/<int:formula_id>")
    def delete_formula(formula_id: int):
        note = db.get_or_404(FormulaNote, formula_id)
        db.session.delete(note)
        db.session.commit()
        return jsonify({"message": "Đã xoá ghi chú công thức."})

    @app.get("/api/stats")
    def stats():
        now = utc_now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        total = Word.query.count()
        new_count = WordProgress.query.filter_by(state="new").count()
        learning_count = WordProgress.query.filter_by(state="learning").count()
        learned_count = WordProgress.query.filter_by(state="learned").count()
        due_count = WordProgress.query.filter(
            WordProgress.state == "learned",
            WordProgress.next_review_at <= now,
        ).count()
        difficult_count = WordProgress.query.filter_by(is_difficult=True).count()
        reviewed_today = ReviewLog.query.filter(ReviewLog.occurred_at >= today).count()
        correct_today = ReviewLog.query.filter(
            ReviewLog.occurred_at >= today, ReviewLog.correct.is_(True)
        ).count()
        next_due = (
            db.session.query(func.min(WordProgress.next_review_at))
            .filter(
                WordProgress.state == "learned",
                WordProgress.next_review_at > now,
            )
            .scalar()
        )
        return jsonify(
            {
                "total": total,
                "new": new_count,
                "learning": learning_count,
                "learned": learned_count,
                "due": due_count,
                "speed_available": learned_count >= 3 and due_count > 0,
                "speed_minimum_learned": 3,
                "difficult": difficult_count,
                "reviewed_today": reviewed_today,
                "accuracy_today": round(correct_today / reviewed_today * 100)
                if reviewed_today
                else None,
                "next_due_at": iso_utc(next_due),
                "schedule": [
                    {"stage": index, "label": label}
                    for index, label in enumerate(SRS_LABELS)
                ],
            }
        )

    @app.get("/api/words")
    def get_words():
        search = clean_text(request.args.get("q"), 160)
        status = request.args.get("status", "all")
        if status not in ALLOWED_STATES:
            status = "all"
        part_of_speech = clean_text(request.args.get("part_of_speech"), 80)
        page = max(request.args.get("page", 1, type=int), 1)
        per_page = min(max(request.args.get("per_page", 20, type=int), 1), 100)
        now = utc_now()

        query = Word.query.join(WordProgress)
        if search:
            term = f"%{search}%"
            query = query.filter(
                or_(
                    Word.english.ilike(term),
                    Word.phonetic.ilike(term),
                    Word.vietnamese.ilike(term),
                    Word.collocation.ilike(term),
                    Word.word_pattern.ilike(term),
                    Word.example.ilike(term),
                    Word.examples.any(WordExample.text.ilike(term)),
                )
            )
        if part_of_speech:
            query = query.filter(Word.part_of_speech == part_of_speech)
        if status in {"new", "learning", "learned"}:
            query = query.filter(WordProgress.state == status)
        elif status == "due":
            query = query.filter(
                WordProgress.state == "learned",
                WordProgress.next_review_at <= now,
            )
        elif status == "difficult":
            query = query.filter(WordProgress.is_difficult.is_(True))

        pagination = query.order_by(Word.created_at.desc(), Word.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        parts = [
            row[0]
            for row in db.session.query(Word.part_of_speech)
            .filter(Word.part_of_speech != "")
            .distinct()
            .order_by(Word.part_of_speech)
            .all()
        ]
        return jsonify(
            {
                "items": [serialize_word(word) for word in pagination.items],
                "page": pagination.page,
                "pages": pagination.pages,
                "total": pagination.total,
                "part_of_speech_options": parts,
            }
        )

    @app.post("/api/words")
    def add_word():
        record, error = validate_word_payload(request.get_json(silent=True) or {})
        if error:
            return jsonify({"error": error}), 400
        if find_duplicate(
            record["english"],
            record["part_of_speech"],
            record["vietnamese"],
        ):
            return jsonify({"error": "Từ, loại từ và nghĩa này đã có trong thư viện."}), 409
        word = create_word(record)
        db.session.commit()
        return jsonify({"message": "Đã thêm từ mới.", "word": serialize_word(word)}), 201

    @app.post("/api/words/bulk")
    def add_words_bulk():
        payload = request.get_json(silent=True) or {}
        items = payload.get("items")
        if not isinstance(items, list) or not items:
            return jsonify({"error": "Không có dữ liệu hợp lệ để nhập."}), 400
        if len(items) > 1000:
            return jsonify({"error": "Mỗi lần chỉ nhập tối đa 1.000 từ."}), 400

        added = []
        skipped = []
        seen = set()
        existing_keys = {
            normalized_word_key(english, part_of_speech, vietnamese)
            for english, part_of_speech, vietnamese in db.session.query(
                Word.english,
                Word.part_of_speech,
                Word.vietnamese,
            ).all()
        }
        for index, item in enumerate(items, start=1):
            record, error = validate_word_payload(item if isinstance(item, dict) else {})
            if error:
                skipped.append({"row": index, "reason": error})
                continue
            key = normalized_word_key(
                record["english"],
                record["part_of_speech"],
                record["vietnamese"],
            )
            if key in seen or key in existing_keys:
                skipped.append({"row": index, "reason": "Bị trùng trong thư viện hoặc danh sách nhập."})
                continue
            seen.add(key)
            word = create_word(record)
            db.session.flush()
            added.append(word.id)
        db.session.commit()
        return jsonify(
            {
                "message": f"Đã thêm {len(added)} từ.",
                "added": len(added),
                "skipped": skipped,
            }
        ), 201

    @app.put("/api/words/<int:word_id>")
    def update_word(word_id: int):
        word = db.get_or_404(Word, word_id)
        record, error = validate_word_payload(request.get_json(silent=True) or {})
        if error:
            return jsonify({"error": error}), 400
        if find_duplicate(
            record["english"],
            record["part_of_speech"],
            record["vietnamese"],
            exclude_id=word_id,
        ):
            return jsonify({"error": "Từ, loại từ và nghĩa này đã có trong thư viện."}), 409
        examples = record.pop("examples")
        for key, value in record.items():
            setattr(word, key, value)
        replace_word_examples(word, examples)
        db.session.commit()
        return jsonify({"message": "Đã cập nhật từ.", "word": serialize_word(word)})

    @app.delete("/api/words/<int:word_id>")
    def delete_word(word_id: int):
        word = db.get_or_404(Word, word_id)
        db.session.delete(word)
        db.session.commit()
        return jsonify({"message": "Đã xoá từ khỏi thư viện."})

    @app.post("/api/words/<int:word_id>/reset")
    def reset_word(word_id: int):
        word = db.get_or_404(Word, word_id)
        progress = word.progress
        progress.state = "new"
        progress.learning_step = 0
        progress.srs_stage = 0
        progress.next_review_at = None
        progress.last_reviewed_at = None
        progress.learned_at = None
        progress.correct_count = 0
        progress.incorrect_count = 0
        progress.is_difficult = False
        ReviewLog.query.filter_by(word_id=word_id).delete()
        db.session.commit()
        return jsonify({"message": "Đã đưa từ về trạng thái chưa học.", "word": serialize_word(word)})

    @app.get("/api/study/new")
    def new_study_session():
        limit = min(max(request.args.get("limit", 5, type=int), 1), 20)
        words = (
            Word.query.join(WordProgress)
            .filter(WordProgress.state.in_(["new", "learning"]))
            .order_by(
                case((WordProgress.state == "learning", 0), else_=1),
                WordProgress.updated_at,
                Word.id,
            )
            .limit(limit)
            .all()
        )
        pool = Word.query.order_by(func.random()).limit(60).all()
        return jsonify(
            {
                "mode": "learn",
                "items": [serialize_word(word) for word in words],
                "pool": [serialize_word(word) for word in pool],
            }
        )

    @app.get("/api/study/review")
    def review_study_session():
        now = utc_now()
        limit = min(max(request.args.get("limit", 20, type=int), 1), 100)
        words = (
            Word.query.join(WordProgress)
            .filter(
                WordProgress.state == "learned",
                WordProgress.next_review_at <= now,
            )
            .order_by(WordProgress.next_review_at, Word.id)
            .limit(limit)
            .all()
        )
        pool = Word.query.order_by(func.random()).limit(80).all()
        return jsonify(
            {
                "mode": "review",
                "items": [serialize_word(word) for word in words],
                "pool": [serialize_word(word) for word in pool],
            }
        )

    @app.post("/api/study/speed/start")
    def start_speed_review_session():
        now = utc_now()
        learned_count = WordProgress.query.filter_by(state="learned").count()
        if learned_count < 3:
            return jsonify(
                {
                    "error": "Cần học xong ít nhất 3 từ để mở Ôn siêu tốc.",
                    "required_learned": 3,
                    "learned": learned_count,
                }
            ), 409

        words = (
            Word.query.join(WordProgress)
            .filter(
                WordProgress.state == "learned",
                WordProgress.next_review_at.is_not(None),
                WordProgress.next_review_at <= now,
            )
            .order_by(WordProgress.next_review_at, Word.id)
            .all()
        )
        if not words:
            return jsonify({"error": "Hiện chưa có từ nào đến hạn để Ôn siêu tốc."}), 409

        session = SpeedReviewSession(id=uuid4().hex, started_at=now)
        db.session.add(session)
        for position, word in enumerate(words):
            session.items.append(
                SpeedReviewItem(word_id=word.id, position=position)
            )

        pool = (
            Word.query
            .order_by(func.random())
            .limit(200)
            .all()
        )
        db.session.commit()
        return jsonify(
            {
                "mode": "speed",
                "session_id": session.id,
                "items": [serialize_word(word) for word in words],
                "pool": [serialize_word(word) for word in pool],
                "rules": SPEED_REVIEW_RULES,
            }
        ), 201

    @app.post("/api/study/speed/skip")
    def skip_speed_review_item():
        """Close an unanswerable speed item without changing its SRS schedule."""
        data = request.get_json(silent=True) or {}
        session_id = clean_text(data.get("session_id"), 32)
        attempt_id = clean_text(data.get("attempt_id"), 64)
        try:
            word_id = int(data.get("word_id"))
        except (TypeError, ValueError):
            return jsonify({"error": "Từ vựng không hợp lệ."}), 400
        if not session_id or not attempt_id:
            return jsonify({"error": "Lượt bỏ qua không hợp lệ."}), 400

        session = db.session.get(SpeedReviewSession, session_id)
        if not session:
            return jsonify({"error": "Không tìm thấy phiên Ôn siêu tốc."}), 404
        item = SpeedReviewItem.query.filter_by(
            session_id=session.id,
            word_id=word_id,
        ).first()
        if not item:
            return jsonify({"error": "Từ này không thuộc phiên Ôn siêu tốc."}), 409
        if item.answered_at is not None:
            if item.attempt_id == attempt_id and item.correct is None:
                return jsonify({"message": "Lượt bỏ qua đã được ghi nhận.", "duplicate": True})
            return jsonify({"error": "Từ này đã được xử lý trong phiên hiện tại."}), 409
        duplicate_attempt = SpeedReviewItem.query.filter(
            SpeedReviewItem.attempt_id == attempt_id,
            SpeedReviewItem.id != item.id,
        ).first()
        if duplicate_attempt:
            return jsonify({"error": "Mã lượt bỏ qua đã được sử dụng."}), 409

        now = utc_now()
        item.attempt_id = attempt_id
        item.answered_at = now
        item.correct = None
        item.timed_out = False
        item.stage_before = item.word.progress.srs_stage
        item.stage_after = item.word.progress.srs_stage
        db.session.flush()
        remaining = SpeedReviewItem.query.filter_by(
            session_id=session.id,
            answered_at=None,
        ).count()
        if remaining == 0:
            session.completed_at = now
        db.session.commit()
        return jsonify(
            {
                "message": "Đã bỏ qua từ; lịch SRS được giữ nguyên.",
                "duplicate": False,
            }
        )

    @app.post("/api/study/speed/result")
    def record_speed_review_result():
        data = request.get_json(silent=True) or {}
        session_id = clean_text(data.get("session_id"), 32)
        attempt_id = clean_text(data.get("attempt_id"), 64)
        question_type = clean_text(data.get("question_type"), 40)
        correct = data.get("correct")
        timed_out = data.get("timed_out", False)
        word_id = data.get("word_id")

        if (
            not session_id
            or not attempt_id
            or not isinstance(correct, bool)
            or not isinstance(timed_out, bool)
        ):
            return jsonify({"error": "Kết quả Ôn siêu tốc không hợp lệ."}), 400
        try:
            word_id = int(word_id)
        except (TypeError, ValueError):
            return jsonify({"error": "Từ vựng không hợp lệ."}), 400

        session = db.session.get(SpeedReviewSession, session_id)
        if not session:
            return jsonify({"error": "Không tìm thấy phiên Ôn siêu tốc."}), 404

        item = SpeedReviewItem.query.filter_by(
            session_id=session.id,
            word_id=word_id,
        ).first()
        if not item:
            return jsonify({"error": "Từ này không thuộc phiên Ôn siêu tốc."}), 409

        if item.answered_at is not None:
            if item.attempt_id != attempt_id:
                return jsonify({"error": "Từ này đã được chấm trong phiên hiện tại."}), 409
            return jsonify(
                {
                    "message": "Kết quả này đã được ghi nhận trước đó.",
                    "word": serialize_word(item.word),
                    "schedule_reset": item.correct is False,
                    "timed_out": item.timed_out,
                    "duplicate": True,
                }
            )

        duplicate_attempt = SpeedReviewItem.query.filter(
            SpeedReviewItem.attempt_id == attempt_id,
            SpeedReviewItem.id != item.id,
        ).first()
        if duplicate_attempt:
            return jsonify({"error": "Mã lượt trả lời đã được sử dụng."}), 409

        now = utc_now()
        word = item.word
        progress = word.progress
        if (
            progress.state != "learned"
            or progress.next_review_at is None
            or progress.next_review_at > now
        ):
            return jsonify(
                {"error": "Từ này không còn đến hạn; lịch SRS chưa bị thay đổi."}
            ), 409

        # Claim the due progress row atomically. SQLite serializes the write;
        # the predicates then prevent two tabs/sessions from advancing the same
        # word from the same SRS state.
        claim = db.session.execute(
            update(WordProgress)
            .where(
                WordProgress.id == progress.id,
                WordProgress.state == "learned",
                WordProgress.next_review_at.is_not(None),
                WordProgress.next_review_at <= now,
                WordProgress.srs_stage == progress.srs_stage,
                WordProgress.correct_count == progress.correct_count,
                WordProgress.incorrect_count == progress.incorrect_count,
                WordProgress.last_reviewed_at == progress.last_reviewed_at,
            )
            .values(last_reviewed_at=now)
            .execution_options(synchronize_session=False)
        )
        if claim.rowcount != 1:
            item_id = item.id
            db.session.rollback()
            current_item = db.session.get(SpeedReviewItem, item_id)
            if (
                current_item
                and current_item.answered_at is not None
                and current_item.attempt_id == attempt_id
            ):
                return jsonify(
                    {
                        "message": "Kết quả này đã được ghi nhận trước đó.",
                        "word": serialize_word(current_item.word),
                        "schedule_reset": current_item.correct is False,
                        "timed_out": current_item.timed_out,
                        "duplicate": True,
                    }
                )
            return jsonify(
                {"error": "Từ này vừa được chấm ở nơi khác; lịch SRS không bị tăng lần hai."}
            ), 409

        if timed_out:
            correct = False
            question_type = "speed-timeout"

        before, after = apply_review_result(progress, correct, now)
        item.attempt_id = attempt_id
        item.answered_at = now
        item.correct = correct
        item.timed_out = timed_out
        item.stage_before = before
        item.stage_after = after
        db.session.add(
            ReviewLog(
                word_id=word.id,
                mode="speed",
                question_type=question_type or "speed-choice",
                correct=correct,
                stage_before=before,
                stage_after=after,
                occurred_at=now,
            )
        )
        db.session.flush()
        remaining = SpeedReviewItem.query.filter_by(
            session_id=session.id,
            answered_at=None,
        ).count()
        if remaining == 0:
            session.completed_at = now
        db.session.commit()
        return jsonify(
            {
                "message": "Đã ghi nhận kết quả Ôn siêu tốc.",
                "word": serialize_word(word),
                "schedule_reset": not correct,
                "timed_out": timed_out,
                "duplicate": False,
            }
        )

    @app.post("/api/study/result")
    def record_study_result():
        data = request.get_json(silent=True) or {}
        mode = data.get("mode")
        correct = data.get("correct")
        word_id = data.get("word_id")
        question_type = clean_text(data.get("question_type"), 40)
        if mode not in ALLOWED_MODES or not isinstance(correct, bool):
            return jsonify({"error": "Kết quả học không hợp lệ."}), 400
        try:
            word_id = int(word_id)
        except (TypeError, ValueError):
            return jsonify({"error": "Từ vựng không hợp lệ."}), 400

        word = db.session.get(Word, word_id)
        if not word:
            return jsonify({"error": "Không tìm thấy từ vựng."}), 404

        now = utc_now()
        progress = word.progress
        before = progress.srs_stage if mode == "review" else progress.learning_step
        try:
            if mode == "learn":
                apply_learning_result(progress, correct, now)
                after = progress.learning_step
            else:
                before, after = apply_review_result(progress, correct, now)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 409

        db.session.add(
            ReviewLog(
                word_id=word.id,
                mode=mode,
                question_type=question_type,
                correct=correct,
                stage_before=before,
                stage_after=after,
                occurred_at=now,
            )
        )
        db.session.commit()
        return jsonify(
            {
                "message": "Đã ghi nhận kết quả.",
                "word": serialize_word(word),
                "schedule_reset": mode == "review" and not correct,
            }
        )

    @app.get("/api/settings")
    def get_settings():
        voice = db.session.get(Setting, "voice_name")
        return jsonify({"voice_name": voice.value if voice else DEFAULT_VOICE})

    @app.put("/api/settings")
    def update_settings():
        voice_name = (request.get_json(silent=True) or {}).get("voice_name")
        if voice_name not in ALLOWED_VOICES:
            return jsonify({"error": "Giọng đọc không hợp lệ."}), 400
        setting = db.session.get(Setting, "voice_name")
        if not setting:
            setting = Setting(key="voice_name")
            db.session.add(setting)
        setting.value = voice_name
        db.session.commit()
        return jsonify({"message": "Đã lưu giọng đọc.", "voice_name": voice_name})

    @app.get("/api/export.csv")
    def export_csv():
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(
            [
                "English",
                "Phonetic",
                "Vietnamese",
                "Part of speech",
                "Examples (separated by ||)",
                "Collocations (one per line)",
                "Word patterns (one per line)",
                "State",
                "Next review",
            ]
        )
        for word in Word.query.order_by(Word.id).all():
            writer.writerow(
                [
                    word.english,
                    word.phonetic,
                    word.vietnamese,
                    word.part_of_speech,
                    " || ".join(word_example_texts(word)),
                    "\n".join(usage_text_items(word.collocation)),
                    "\n".join(usage_text_items(word.word_pattern)),
                    word.progress.state,
                    iso_utc(word.progress.next_review_at) or "",
                ]
            )
        return app.response_class(
            output.getvalue(),
            mimetype="text/csv; charset=utf-8",
            headers={"Content-Disposition": "attachment; filename=lexiloop-vocabulary.csv"},
        )

    @app.errorhandler(404)
    def not_found(_error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Không tìm thấy dữ liệu."}), 404
        return render_template("index.html"), 404

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
