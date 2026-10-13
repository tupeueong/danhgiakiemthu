import csv
from datetime import datetime, timedelta
import io
import sqlite3

import app as app_module
from models import ReviewLog, SpeedReviewSession, Word, WordExample, WordProgress, db


def record(client, word_id, mode, correct, question_type="typing"):
    return client.post(
        "/api/study/result",
        json={
            "word_id": word_id,
            "mode": mode,
            "correct": correct,
            "question_type": question_type,
        },
    )


def parse_utc(value):
    return datetime.fromisoformat(value.removesuffix("Z"))


def test_add_form_contains_usage_fields_and_no_tips_panel(client):
    response = client.get("/")
    html = response.get_data(as_text=True)
    assert response.status_code == 200
    assert html.count('name="collocations"') == 2
    assert html.count('name="word_patterns"') == 2
    assert "Gợi ý nhỏ" not in html
    assert 'class="add-tips"' not in html


def complete_learning(client, word_id):
    result = None
    for _ in range(6):
        response = record(client, word_id, "learn", True)
        assert response.status_code == 200
        result = response.get_json()["word"]
    return result


def test_add_word_and_reject_exact_duplicate(client, add_word):
    word = add_word(
        collocation="highly compelling",
        word_pattern="compelling + noun",
    )
    assert word["progress"]["state"] == "new"
    assert word["phonetic"] == "/kəmˈpelɪŋ/"
    assert word["examples"] == ["She made a compelling argument."]
    assert word["example"] == word["examples"][0]
    assert word["collocation"] == "highly compelling"
    assert word["collocations"] == ["highly compelling"]
    assert word["word_pattern"] == "compelling + noun"
    assert word["word_patterns"] == ["compelling + noun"]

    duplicate = client.post(
        "/api/words",
        json={
            "english": "COMPELLING",
            "vietnamese": "THUYẾT PHỤC, HẤP DẪN",
            "part_of_speech": "ADJ.",
        },
    )
    assert duplicate.status_code == 409


def test_usage_lists_prefer_arrays_normalize_and_remove_duplicates(client, app, add_word):
    word = add_word(
        collocation="this legacy value is ignored",
        collocations=[
            "  strong   demand  ",
            "STRONG DEMAND",
            "ｓｔｒｏｎｇ demand",
            "meet demand",
            "",
        ],
        word_pattern="this legacy value is ignored",
        word_patterns=[
            "demand + for + noun",
            "  DEMAND + FOR + NOUN ",
            "demand that + clause",
        ],
    )

    assert word["collocations"] == ["strong demand", "meet demand"]
    assert word["collocation"] == "strong demand\nmeet demand"
    assert word["word_patterns"] == [
        "demand + for + noun",
        "demand that + clause",
    ]
    assert word["word_pattern"] == "demand + for + noun\ndemand that + clause"

    with app.app_context():
        stored = db.session.get(Word, word["id"])
        assert stored.collocation == "strong demand\nmeet demand"
        assert stored.word_pattern == "demand + for + noun\ndemand that + clause"


def test_usage_lists_accept_newline_legacy_strings(client, add_word):
    word = add_word(
        collocation="make a decision\n  reach   a decision \nMAKE A DECISION",
        word_pattern="decide to + verb\ndecide that + clause",
    )
    assert word["collocations"] == ["make a decision", "reach a decision"]
    assert word["word_patterns"] == ["decide to + verb", "decide that + clause"]


def test_usage_lists_reject_invalid_count_type_and_length(client):
    base = {"english": "allocate", "vietnamese": "phân bổ"}

    assert client.post(
        "/api/words",
        json={**base, "collocations": "not-an-array"},
    ).status_code == 400
    assert client.post(
        "/api/words",
        json={**base, "word_patterns": [123]},
    ).status_code == 400

    too_many = client.post(
        "/api/words",
        json={**base, "collocations": [f"item {index}" for index in range(101)]},
    )
    assert too_many.status_code == 400
    assert "100" in too_many.get_json()["error"]

    too_long = client.post(
        "/api/words",
        json={**base, "word_patterns": ["x" * 501]},
    )
    assert too_long.status_code == 400
    assert "500" in too_long.get_json()["error"]


def test_duplicate_identity_includes_normalized_part_of_speech(client, add_word):
    noun = add_word(
        english="record",
        vietnamese="bản ghi",
        part_of_speech="n.",
    )
    verb = add_word(
        english="record",
        vietnamese="bản ghi",
        part_of_speech="v",
    )
    other_noun_meaning = add_word(
        english="record",
        vietnamese="kỷ lục",
        part_of_speech="noun",
    )

    assert noun["part_of_speech"] == "noun"
    assert verb["part_of_speech"] == "verb"
    assert other_noun_meaning["part_of_speech"] == "noun"

    exact_alias_duplicate = client.post(
        "/api/words",
        json={
            "english": "RECORD",
            "vietnamese": "BẢN GHI",
            "part_of_speech": "NOUN",
        },
    )
    assert exact_alias_duplicate.status_code == 409
    assert "loại từ" in exact_alias_duplicate.get_json()["error"]

    compatibility_unicode_duplicate = client.post(
        "/api/words",
        json={
            "english": "ｒｅｃｏｒｄ",
            "vietnamese": "bản ghi",
            "part_of_speech": "n.",
        },
    )
    assert compatibility_unicode_duplicate.status_code == 409

    update_into_existing_identity = client.put(
        f"/api/words/{verb['id']}",
        json={
            "english": "record",
            "vietnamese": "bản ghi",
            "part_of_speech": "n",
        },
    )
    assert update_into_existing_identity.status_code == 409


def test_common_part_of_speech_aliases_and_custom_label(client, add_word):
    cases = [
        ("N", "noun"),
        ("V.", "verb"),
        ("Adj.", "adjective"),
        ("ADV", "adverb"),
        ("prep.", "preposition"),
        ("Pron.", "pronoun"),
        ("Conj", "conjunction"),
        ("Interj.", "interjection"),
        ("Det.", "determiner"),
        ("Aux.", "auxiliary verb"),
        ("Modal.", "modal verb"),
        ("Phrase", "phrase"),
        ("Phr. V.", "phrasal verb"),
        ("Idiom", "idiom"),
        ("Art.", "article"),
    ]
    for index, (alias, expected) in enumerate(cases):
        word = add_word(
            english=f"alias-{index}",
            vietnamese=f"nghĩa {index}",
            part_of_speech=alias,
        )
        assert word["part_of_speech"] == expected

    custom = add_word(
        english="by and large",
        vietnamese="nhìn chung",
        part_of_speech="  idiomatic   expression  ",
    )
    assert custom["part_of_speech"] == "idiomatic expression"


def test_add_update_search_and_export_multiple_examples(client, app, add_word):
    word = add_word(
        english="allocate",
        vietnamese="phân bổ",
        collocations=["allocate resources efficiently", "allocate enough time"],
        word_patterns=["allocate something to somebody", "allocate something for a purpose"],
        examples=[
            "We allocate funds carefully.",
            "  We   allocate funds carefully.  ",
            "THE TEAM ALLOCATES TIME WISELY.",
            "the team allocates time wisely.",
            "",
        ],
    )
    assert word["examples"] == [
        "We allocate funds carefully.",
        "THE TEAM ALLOCATES TIME WISELY.",
    ]
    assert word["example"] == "We allocate funds carefully."

    search = client.get("/api/words?q=allocates%20time").get_json()
    assert search["total"] == 1
    assert search["items"][0]["id"] == word["id"]
    assert client.get("/api/words?q=resources%20efficiently").get_json()["total"] == 1
    assert client.get("/api/words?q=purpose").get_json()["total"] == 1

    update = client.put(
        f"/api/words/{word['id']}",
        json={
            "english": "allocate",
            "phonetic": "/ˈæləkeɪt/",
            "vietnamese": "phân bổ",
            "part_of_speech": "verb",
            "collocations": ["allocate scarce resources", "allocate || reserve resources"],
            "word_patterns": [
                "allocate something among people",
                "allocate something for a task",
            ],
            "examples": ["Allocate one hour.", "Allocate two hours."],
        },
    )
    assert update.status_code == 200
    updated = update.get_json()["word"]
    assert updated["examples"] == ["Allocate one hour.", "Allocate two hours."]
    assert updated["example"] == "Allocate one hour."
    assert updated["collocations"] == [
        "allocate scarce resources",
        "allocate || reserve resources",
    ]
    assert updated["word_patterns"] == [
        "allocate something among people",
        "allocate something for a task",
    ]

    with app.app_context():
        stored = db.session.get(Word, word["id"])
        assert stored.example == "Allocate one hour."
        assert stored.collocation == "allocate scarce resources\nallocate || reserve resources"
        assert stored.word_pattern == (
            "allocate something among people\nallocate something for a task"
        )
        assert [example.text for example in stored.examples] == updated["examples"]

    unchanged_examples = client.put(
        f"/api/words/{word['id']}",
        json={
            "english": "allocate",
            "phonetic": "/ˈæləkeɪt/",
            "vietnamese": "phân bổ",
            "part_of_speech": "verb",
            "collocations": updated["collocations"],
            "word_patterns": updated["word_patterns"],
            "examples": updated["examples"],
        },
    )
    assert unchanged_examples.status_code == 200
    assert unchanged_examples.get_json()["word"]["examples"] == updated["examples"]

    response = client.get("/api/export.csv")
    rows = list(csv.reader(io.StringIO(response.get_data(as_text=True))))
    assert rows[0][4] == "Examples (separated by ||)"
    assert rows[1][4] == "Allocate one hour. || Allocate two hours."
    assert rows[0][5:7] == [
        "Collocations (one per line)",
        "Word patterns (one per line)",
    ]
    assert rows[1][5:7] == [
        "allocate scarce resources\nallocate || reserve resources",
        "allocate something among people\nallocate something for a task",
    ]


def test_delete_word_cascades_to_all_examples(client, app, add_word):
    word = add_word(examples=["First example.", "Second example."])
    with app.app_context():
        assert WordExample.query.filter_by(word_id=word["id"]).count() == 2

    assert client.delete(f"/api/words/{word['id']}").status_code == 200
    with app.app_context():
        assert WordExample.query.filter_by(word_id=word["id"]).count() == 0


def test_examples_payload_rejects_non_list_or_non_text(client):
    base = {"english": "allocate", "vietnamese": "phân bổ"}
    assert client.post("/api/words", json={**base, "examples": "not-a-list"}).status_code == 400
    assert client.post("/api/words", json={**base, "examples": [123]}).status_code == 400
    too_long = client.post("/api/words", json={**base, "examples": ["x" * 1501]})
    assert too_long.status_code == 400
    assert "1.500" in too_long.get_json()["error"]


def test_bulk_import_skips_duplicate_rows(client, add_word):
    add_word()
    response = client.post(
        "/api/words/bulk",
        json={
            "items": [
                {
                    "english": "allocate",
                    "phonetic": "/ˈæləkeɪt/",
                    "vietnamese": "phân bổ",
                    "part_of_speech": "verb",
                    "collocations": ["allocate the budget", "allocate enough time"],
                    "word_patterns": [
                        "allocate something to something",
                        "allocate something among people",
                    ],
                    "examples": [
                        "Allocate the budget.",
                        "Allocate   the budget.",
                        "Allocate enough time.",
                    ],
                },
                {
                    "english": "allocate",
                    "vietnamese": "phân bổ",
                    "part_of_speech": "V.",
                },
                {
                    "english": "compelling",
                    "vietnamese": "thuyết phục, hấp dẫn",
                    "part_of_speech": "adj.",
                },
                {"english": "", "vietnamese": "thiếu từ"},
            ]
        },
    )
    assert response.status_code == 201
    payload = response.get_json()
    assert payload["added"] == 1
    assert len(payload["skipped"]) == 3
    imported = client.get("/api/words?q=allocate").get_json()["items"][0]
    assert imported["examples"] == ["Allocate the budget.", "Allocate enough time."]
    assert imported["collocations"] == ["allocate the budget", "allocate enough time"]
    assert imported["word_patterns"] == [
        "allocate something to something",
        "allocate something among people",
    ]


def test_bulk_duplicate_key_uses_english_pos_and_meaning(client):
    response = client.post(
        "/api/words/bulk",
        json={
            "items": [
                {"english": "record", "vietnamese": "bản ghi", "part_of_speech": "n"},
                {"english": "RECORD", "vietnamese": "BẢN GHI", "part_of_speech": "noun"},
                {"english": "record", "vietnamese": "bản ghi", "part_of_speech": "v."},
                {"english": "record", "vietnamese": "kỷ lục", "part_of_speech": "noun"},
            ]
        },
    )
    assert response.status_code == 201
    payload = response.get_json()
    assert payload["added"] == 3
    assert [item["row"] for item in payload["skipped"]] == [2]

    library = client.get("/api/words?q=record&per_page=100").get_json()
    assert library["total"] == 3
    assert sorted(item["part_of_speech"] for item in library["items"]) == [
        "noun",
        "noun",
        "verb",
    ]


def test_six_correct_answers_complete_learning_and_schedule_four_hours(
    client, add_word, monkeypatch
):
    now = datetime(2026, 8, 11, 3, 0, 0)
    monkeypatch.setattr(app_module, "utc_now", lambda: now)
    word = add_word()

    for step in range(6):
        response = record(client, word["id"], "learn", True)
        assert response.status_code == 200
        progress = response.get_json()["word"]["progress"]
        assert progress["learning_step"] == step + 1

    assert progress["state"] == "learned"
    assert progress["srs_stage"] == 0
    assert parse_utc(progress["next_review_at"]) == now + timedelta(hours=4)


def test_wrong_learning_answer_requires_an_extra_success(client, add_word, monkeypatch):
    monkeypatch.setattr(app_module, "utc_now", lambda: datetime(2026, 8, 11, 3, 0, 0))
    word = add_word()
    first = record(client, word["id"], "learn", True).get_json()["word"]
    wrong = record(client, word["id"], "learn", False).get_json()["word"]
    assert first["progress"]["learning_step"] == 1
    assert wrong["progress"]["learning_step"] == 1
    assert wrong["progress"]["is_difficult"] is True


def test_same_english_different_pos_have_independent_progress(
    client, app, add_word, monkeypatch
):
    now = datetime(2026, 8, 11, 3, 0, 0)
    monkeypatch.setattr(app_module, "utc_now", lambda: now)
    noun = add_word(
        english="record",
        phonetic="/ˈrek.ɔːd/",
        vietnamese="bản ghi",
        part_of_speech="noun",
    )
    verb = add_word(
        english="record",
        phonetic="/rɪˈkɔːd/",
        vietnamese="ghi lại",
        part_of_speech="verb",
    )

    learned_noun = complete_learning(client, noun["id"])
    learning_verb = record(client, verb["id"], "learn", True).get_json()["word"]

    assert learned_noun["progress"]["state"] == "learned"
    assert learned_noun["progress"]["learning_step"] == 6
    assert learned_noun["progress"]["correct_count"] == 6
    assert learning_verb["progress"]["state"] == "learning"
    assert learning_verb["progress"]["learning_step"] == 1
    assert learning_verb["progress"]["correct_count"] == 1
    assert learning_verb["progress"]["next_review_at"] is None

    with app.app_context():
        noun_progress = WordProgress.query.filter_by(word_id=noun["id"]).one()
        verb_progress = WordProgress.query.filter_by(word_id=verb["id"]).one()
        assert noun_progress.id != verb_progress.id
        assert ReviewLog.query.filter_by(word_id=noun["id"]).count() == 6
        assert ReviewLog.query.filter_by(word_id=verb["id"]).count() == 1


def test_review_ladder_and_wrong_answer_reset(client, add_word, monkeypatch):
    base = datetime(2026, 8, 11, 3, 0, 0)
    current = {"value": base}
    monkeypatch.setattr(app_module, "utc_now", lambda: current["value"])
    word = add_word()
    for _ in range(6):
        learned = record(client, word["id"], "learn", True).get_json()["word"]

    expected_intervals = [
        timedelta(hours=12),
        timedelta(days=1),
        timedelta(days=6),
        timedelta(days=12),
        timedelta(days=48),
        timedelta(days=96),
        timedelta(days=180),
    ]
    for expected_stage, interval in enumerate(expected_intervals, start=1):
        current["value"] = parse_utc(learned["progress"]["next_review_at"])
        response = record(client, word["id"], "review", True)
        assert response.status_code == 200
        learned = response.get_json()["word"]
        assert learned["progress"]["srs_stage"] == expected_stage
        assert parse_utc(learned["progress"]["next_review_at"]) == current["value"] + interval

    current["value"] = parse_utc(learned["progress"]["next_review_at"])
    reset_response = record(client, word["id"], "review", False)
    reset = reset_response.get_json()
    assert reset["schedule_reset"] is True
    assert reset["word"]["progress"]["srs_stage"] == 0
    assert reset["word"]["progress"]["is_difficult"] is True
    assert parse_utc(reset["word"]["progress"]["next_review_at"]) == current["value"] + timedelta(hours=4)


def test_speed_review_requires_three_learned_words(client, add_word, monkeypatch):
    current = {"value": datetime(2026, 8, 11, 3, 0, 0)}
    monkeypatch.setattr(app_module, "utc_now", lambda: current["value"])
    first = add_word(english="alpha", vietnamese="đầu tiên")
    second = add_word(english="beta", vietnamese="thứ hai")
    complete_learning(client, first["id"])
    complete_learning(client, second["id"])
    current["value"] += timedelta(hours=4)

    response = client.post("/api/study/speed/start", json={})
    assert response.status_code == 409
    assert response.get_json()["required_learned"] == 3


def test_speed_review_snapshots_only_learned_words_that_are_due(
    client, app, add_word, monkeypatch
):
    base = datetime(2026, 8, 11, 3, 0, 0)
    current = {"value": base}
    monkeypatch.setattr(app_module, "utc_now", lambda: current["value"])
    due_one = add_word(english="alpha", vietnamese="đầu tiên")
    future = add_word(english="beta", vietnamese="thứ hai")
    due_two = add_word(english="gamma", vietnamese="thứ ba")
    new_word = add_word(english="delta", vietnamese="thứ tư")
    learning_word = add_word(english="epsilon", vietnamese="thứ năm")
    for word in (due_one, future, due_two):
        complete_learning(client, word["id"])
    record(client, learning_word["id"], "learn", True)
    current["value"] = base + timedelta(hours=4)

    with app.app_context():
        future_progress = WordProgress.query.filter_by(word_id=future["id"]).one()
        future_progress.next_review_at = current["value"] + timedelta(hours=2)
        db.session.commit()

    response = client.post("/api/study/speed/start", json={})
    assert response.status_code == 201
    payload = response.get_json()
    assert payload["mode"] == "speed"
    assert payload["rules"]["starting_hearts"] == 3
    assert {item["id"] for item in payload["items"]} == {due_one["id"], due_two["id"]}
    assert new_word["id"] not in {item["id"] for item in payload["items"]}
    assert learning_word["id"] not in {item["id"] for item in payload["items"]}


def test_speed_review_skip_keeps_srs_and_completes_session(
    client, app, add_word, monkeypatch
):
    base = datetime(2026, 8, 11, 3, 0, 0)
    current = {"value": base}
    monkeypatch.setattr(app_module, "utc_now", lambda: current["value"])
    words = [
        add_word(english="record", vietnamese="bản ghi", part_of_speech="noun"),
        add_word(english="record", vietnamese="ghi lại", part_of_speech="verb"),
        add_word(english="entry", vietnamese="bản ghi", part_of_speech="noun"),
    ]
    for word in words:
        complete_learning(client, word["id"])
    current["value"] = base + timedelta(hours=4)
    session = client.post("/api/study/speed/start", json={}).get_json()
    before = {
        item["id"]: item["progress"].copy()
        for item in session["items"]
    }

    for index, item in enumerate(session["items"]):
        response = client.post(
            "/api/study/speed/skip",
            json={
                "session_id": session["session_id"],
                "word_id": item["id"],
                "attempt_id": f"skip-{index}",
            },
        )
        assert response.status_code == 200

    duplicate = client.post(
        "/api/study/speed/skip",
        json={
            "session_id": session["session_id"],
            "word_id": session["items"][0]["id"],
            "attempt_id": "skip-0",
        },
    )
    assert duplicate.status_code == 200
    assert duplicate.get_json()["duplicate"] is True
    assert client.get("/api/stats").get_json()["due"] == 3

    with app.app_context():
        stored_session = db.session.get(SpeedReviewSession, session["session_id"])
        assert stored_session.completed_at == current["value"]
        assert ReviewLog.query.filter_by(mode="speed").count() == 0
        for word in words:
            progress = WordProgress.query.filter_by(word_id=word["id"]).one()
            expected = before[word["id"]]
            assert progress.srs_stage == expected["srs_stage"]
            assert progress.correct_count == expected["correct_count"]
            assert progress.incorrect_count == expected["incorrect_count"]
            assert progress.next_review_at == parse_utc(expected["next_review_at"])


def test_speed_review_correct_result_is_idempotent_and_advances_srs(
    client, app, add_word, monkeypatch
):
    base = datetime(2026, 8, 11, 3, 0, 0)
    current = {"value": base}
    monkeypatch.setattr(app_module, "utc_now", lambda: current["value"])
    words = [
        add_word(english="alpha", vietnamese="đầu tiên"),
        add_word(english="beta", vietnamese="thứ hai"),
        add_word(english="gamma", vietnamese="thứ ba"),
    ]
    for word in words:
        complete_learning(client, word["id"])
    current["value"] = base + timedelta(hours=4)
    session = client.post("/api/study/speed/start", json={}).get_json()
    word_id = session["items"][0]["id"]
    payload = {
        "session_id": session["session_id"],
        "word_id": word_id,
        "attempt_id": "attempt-correct-1",
        "correct": True,
        "timed_out": False,
        "question_type": "speed-meaning-choice",
    }

    response = client.post("/api/study/speed/result", json=payload)
    assert response.status_code == 200
    progress = response.get_json()["word"]["progress"]
    assert progress["srs_stage"] == 1
    assert parse_utc(progress["next_review_at"]) == current["value"] + timedelta(hours=12)

    duplicate = client.post("/api/study/speed/result", json=payload)
    assert duplicate.status_code == 200
    assert duplicate.get_json()["duplicate"] is True
    different_attempt = client.post(
        "/api/study/speed/result",
        json={**payload, "attempt_id": "attempt-correct-2"},
    )
    assert different_attempt.status_code == 409
    with app.app_context():
        assert ReviewLog.query.filter_by(word_id=word_id, mode="speed").count() == 1


def test_speed_review_wrong_and_timeout_reset_to_four_hours(
    client, app, add_word, monkeypatch
):
    base = datetime(2026, 8, 11, 3, 0, 0)
    current = {"value": base}
    monkeypatch.setattr(app_module, "utc_now", lambda: current["value"])
    words = [
        add_word(english="alpha", vietnamese="đầu tiên"),
        add_word(english="beta", vietnamese="thứ hai"),
        add_word(english="gamma", vietnamese="thứ ba"),
    ]
    for word in words:
        complete_learning(client, word["id"])
    current["value"] = base + timedelta(hours=4)
    session = client.post("/api/study/speed/start", json={}).get_json()

    for index, timed_out in enumerate((False, True)):
        word_id = session["items"][index]["id"]
        response = client.post(
            "/api/study/speed/result",
            json={
                "session_id": session["session_id"],
                "word_id": word_id,
                "attempt_id": f"attempt-wrong-{index}",
                "correct": timed_out,
                "timed_out": timed_out,
                "question_type": "speed-word-choice",
            },
        )
        assert response.status_code == 200
        payload = response.get_json()
        assert payload["schedule_reset"] is True
        assert payload["word"]["progress"]["srs_stage"] == 0
        assert payload["word"]["progress"]["is_difficult"] is True
        assert parse_utc(payload["word"]["progress"]["next_review_at"]) == current["value"] + timedelta(hours=4)

    with app.app_context():
        timeout_log = ReviewLog.query.filter_by(
            word_id=session["items"][1]["id"],
            mode="speed",
        ).one()
        assert timeout_log.correct is False
        assert timeout_log.question_type == "speed-timeout"


def test_speed_review_rejects_word_that_was_reviewed_in_another_mode(
    client, add_word, monkeypatch
):
    base = datetime(2026, 8, 11, 3, 0, 0)
    current = {"value": base}
    monkeypatch.setattr(app_module, "utc_now", lambda: current["value"])
    words = [
        add_word(english="alpha", vietnamese="đầu tiên"),
        add_word(english="beta", vietnamese="thứ hai"),
        add_word(english="gamma", vietnamese="thứ ba"),
    ]
    for word in words:
        complete_learning(client, word["id"])
    current["value"] = base + timedelta(hours=4)
    session = client.post("/api/study/speed/start", json={}).get_json()
    word_id = session["items"][0]["id"]
    assert record(client, word_id, "review", True).status_code == 200

    response = client.post(
        "/api/study/speed/result",
        json={
            "session_id": session["session_id"],
            "word_id": word_id,
            "attempt_id": "attempt-after-classic-review",
            "correct": True,
            "timed_out": False,
            "question_type": "speed-meaning-choice",
        },
    )
    assert response.status_code == 409
    assert "không còn đến hạn" in response.get_json()["error"]


def test_library_search_and_delete_cascade(client, add_word):
    word = add_word(english="allocate", vietnamese="phân bổ")
    results = client.get("/api/words?q=phan")
    # Accent-sensitive SQLite search should not invent accent folding.
    assert results.status_code == 200

    results = client.get("/api/words?q=allocate").get_json()
    assert results["total"] == 1
    assert client.delete(f"/api/words/{word['id']}").status_code == 200
    assert client.get("/api/words").get_json()["total"] == 0


def test_settings_only_accept_three_supported_voice_names(client):
    accepted = client.put(
        "/api/settings",
        json={"voice_name": "Google US English"},
    )
    assert accepted.status_code == 200
    assert client.get("/api/settings").get_json()["voice_name"] == "Google US English"

    rejected = client.put("/api/settings", json={"voice_name": "Unknown voice"})
    assert rejected.status_code == 400


def test_formula_notes_persist_and_are_ordered_by_latest_update(client, add_formula):
    first = add_formula("a² + b² = c²")
    second = add_formula("F = ma")

    listing = client.get("/api/formulas")
    assert listing.status_code == 200
    payload = listing.get_json()
    assert payload["total"] == 2
    assert [item["id"] for item in payload["items"]] == [second["id"], first["id"]]
    assert all(item["created_at"].endswith("Z") for item in payload["items"])
    assert all(item["updated_at"].endswith("Z") for item in payload["items"])

    updated = client.put(
        f"/api/formulas/{first['id']}",
        json={"content": "a² + b² = c²\nDùng cho tam giác vuông."},
    )
    assert updated.status_code == 200
    updated_formula = updated.get_json()["formula"]
    assert updated_formula["created_at"] == first["created_at"]
    assert updated_formula["content"] == "a² + b² = c²\nDùng cho tam giác vuông."

    reordered = client.get("/api/formulas").get_json()["items"]
    assert [item["id"] for item in reordered] == [first["id"], second["id"]]


def test_formula_content_normalization_and_validation(client, add_formula):
    note = add_formula(
        "\r\n  x = (-b ± √(b² - 4ac)) / 2a  \r\n\r\n"
        "Giữ dòng trống có ý nghĩa.   \r\n   \r\n"
    )
    assert note["content"] == (
        "x = (-b ± √(b² - 4ac)) / 2a\n\n"
        "Giữ dòng trống có ý nghĩa."
    )

    invalid_payloads = [
        {},
        {"content": None},
        {"content": 123},
        {"content": " \r\n\t "},
        {"content": "x" * 20_001},
    ]
    for payload in invalid_payloads:
        response = client.post("/api/formulas", json=payload)
        assert response.status_code == 400
        assert response.get_json()["error"]

    maximum = client.post("/api/formulas", json={"content": "x" * 20_000})
    assert maximum.status_code == 201
    assert len(maximum.get_json()["formula"]["content"]) == 20_000

    unchanged = client.put(
        f"/api/formulas/{note['id']}",
        json={"content": "x" * 20_001},
    )
    assert unchanged.status_code == 400
    stored = {
        item["id"]: item for item in client.get("/api/formulas").get_json()["items"]
    }
    assert stored[note["id"]]["content"] == note["content"]


def test_formula_delete_does_not_change_vocabulary(client, add_formula, add_word):
    word = add_word(english="integral", vietnamese="tích phân")
    note = add_formula("∫ x dx = x² / 2 + C")

    deleted = client.delete(f"/api/formulas/{note['id']}")
    assert deleted.status_code == 200
    assert client.get("/api/formulas").get_json() == {"items": [], "total": 0}

    library = client.get("/api/words?q=integral").get_json()
    assert library["total"] == 1
    assert library["items"][0]["id"] == word["id"]
    assert library["items"][0]["vietnamese"] == "tích phân"


def test_formula_page_contract_and_missing_note_errors(client, add_formula):
    page = client.get("/")
    assert page.status_code == 200
    html = page.get_data(as_text=True)
    assert html.count('class="nav-item') == 5
    assert 'data-route="formulas"' in html
    assert 'id="formulasView"' in html
    assert 'id="formulaContent"' in html
    assert 'maxlength="20000"' in html

    stats_before = client.get("/api/stats").get_json()
    note = add_formula("S + be + adjective")
    assert client.get("/api/stats").get_json() == stats_before

    assert client.put(
        "/api/formulas/999999",
        json={"content": "missing"},
    ).status_code == 404
    assert client.delete("/api/formulas/999999").status_code == 404
    assert client.get("/api/formulas").get_json()["items"][0]["id"] == note["id"]


def test_existing_database_is_migrated_with_optional_word_columns():
    sqlite_uri = "file:lexiloop-legacy-test?mode=memory&cache=shared"
    connection = sqlite3.connect(sqlite_uri, uri=True)
    connection.execute(
        """
        CREATE TABLE words (
            id INTEGER PRIMARY KEY,
            english VARCHAR(160) NOT NULL,
            vietnamese VARCHAR(320) NOT NULL,
            part_of_speech VARCHAR(80) NOT NULL DEFAULT '',
            example TEXT NOT NULL DEFAULT '',
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL
        )
        """
    )
    connection.execute(
        """
        INSERT INTO words (
            id, english, vietnamese, part_of_speech, example, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            1,
            "legacy",
            "cũ",
            "adjective",
            "  The original legacy example stays intact.  ",
            "2026-08-11 03:00:00",
            "2026-08-11 03:00:00",
        ),
    )
    connection.commit()
    app_module.create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "SQLALCHEMY_ENGINE_OPTIONS": {
                "creator": lambda: sqlite3.connect(sqlite_uri, uri=True)
            },
        }
    )

    columns = {row[1] for row in connection.execute("PRAGMA table_info(words)")}
    migrated = connection.execute(
        "SELECT word_id, text, position FROM word_examples"
    ).fetchall()
    legacy_value = connection.execute(
        "SELECT example FROM words WHERE id = 1"
    ).fetchone()[0]
    new_text_fields = connection.execute(
        "SELECT collocation, word_pattern FROM words WHERE id = 1"
    ).fetchone()
    connection.close()
    assert "phonetic" in columns
    assert "collocation" in columns
    assert "word_pattern" in columns
    assert new_text_fields == ("", "")
    assert migrated == [(1, "  The original legacy example stays intact.  ", 0)]
    assert legacy_value == "  The original legacy example stays intact.  "
