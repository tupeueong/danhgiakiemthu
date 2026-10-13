from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

from srs import utc_now


db = SQLAlchemy()


@event.listens_for(Engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, _connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA busy_timeout=5000")
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()


class Word(db.Model):
    __tablename__ = "words"

    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(160), nullable=False, index=True)
    phonetic = db.Column(db.String(160), nullable=False, default="")
    vietnamese = db.Column(db.String(320), nullable=False, index=True)
    part_of_speech = db.Column(db.String(80), nullable=False, default="")
    collocation = db.Column(db.Text, nullable=False, default="")
    word_pattern = db.Column(db.Text, nullable=False, default="")
    example = db.Column(db.Text, nullable=False, default="")
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)
    updated_at = db.Column(db.DateTime, nullable=False, default=utc_now, onupdate=utc_now)

    progress = db.relationship(
        "WordProgress",
        back_populates="word",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    reviews = db.relationship(
        "ReviewLog",
        back_populates="word",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    examples = db.relationship(
        "WordExample",
        back_populates="word",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="WordExample.position, WordExample.id",
    )


class WordExample(db.Model):
    __tablename__ = "word_examples"
    __table_args__ = (
        db.UniqueConstraint(
            "word_id",
            "normalized_text",
            name="uq_word_examples_word_normalized_text",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(
        db.Integer,
        db.ForeignKey("words.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    text = db.Column(db.Text, nullable=False)
    normalized_text = db.Column(db.Text, nullable=False)
    position = db.Column(db.Integer, nullable=False, default=0)

    word = db.relationship("Word", back_populates="examples")


class WordProgress(db.Model):
    __tablename__ = "word_progress"

    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(
        db.Integer,
        db.ForeignKey("words.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    state = db.Column(db.String(20), nullable=False, default="new", index=True)
    learning_step = db.Column(db.Integer, nullable=False, default=0)
    srs_stage = db.Column(db.Integer, nullable=False, default=0)
    next_review_at = db.Column(db.DateTime, nullable=True, index=True)
    last_reviewed_at = db.Column(db.DateTime, nullable=True)
    learned_at = db.Column(db.DateTime, nullable=True)
    correct_count = db.Column(db.Integer, nullable=False, default=0)
    incorrect_count = db.Column(db.Integer, nullable=False, default=0)
    is_difficult = db.Column(db.Boolean, nullable=False, default=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)
    updated_at = db.Column(db.DateTime, nullable=False, default=utc_now, onupdate=utc_now)

    word = db.relationship("Word", back_populates="progress")


class ReviewLog(db.Model):
    __tablename__ = "review_logs"

    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(
        db.Integer,
        db.ForeignKey("words.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    mode = db.Column(db.String(20), nullable=False)
    question_type = db.Column(db.String(40), nullable=False, default="")
    correct = db.Column(db.Boolean, nullable=False)
    stage_before = db.Column(db.Integer, nullable=True)
    stage_after = db.Column(db.Integer, nullable=True)
    occurred_at = db.Column(db.DateTime, nullable=False, default=utc_now, index=True)

    word = db.relationship("Word", back_populates="reviews")


class SpeedReviewSession(db.Model):
    __tablename__ = "speed_review_sessions"

    id = db.Column(db.String(32), primary_key=True)
    started_at = db.Column(db.DateTime, nullable=False, default=utc_now, index=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    items = db.relationship(
        "SpeedReviewItem",
        back_populates="session",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="SpeedReviewItem.position",
    )


class SpeedReviewItem(db.Model):
    __tablename__ = "speed_review_items"
    __table_args__ = (
        db.UniqueConstraint("session_id", "word_id", name="uq_speed_review_session_word"),
    )

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(
        db.String(32),
        db.ForeignKey("speed_review_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    word_id = db.Column(
        db.Integer,
        db.ForeignKey("words.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    position = db.Column(db.Integer, nullable=False)
    attempt_id = db.Column(db.String(64), nullable=True, unique=True, index=True)
    answered_at = db.Column(db.DateTime, nullable=True)
    correct = db.Column(db.Boolean, nullable=True)
    timed_out = db.Column(db.Boolean, nullable=False, default=False)
    stage_before = db.Column(db.Integer, nullable=True)
    stage_after = db.Column(db.Integer, nullable=True)

    session = db.relationship("SpeedReviewSession", back_populates="items")
    word = db.relationship("Word")


class FormulaNote(db.Model):
    __tablename__ = "formula_notes"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)
    updated_at = db.Column(db.DateTime, nullable=False, default=utc_now, onupdate=utc_now)


class Setting(db.Model):
    __tablename__ = "settings"

    key = db.Column(db.String(80), primary_key=True)
    value = db.Column(db.Text, nullable=False, default="")
