"""Spaced-repetition rules used by the application.

The public Community Courses schedule is deliberately represented as a fixed
ladder.  Stage 0 means that the next review is due in four hours; answering a
review correctly advances one stage, while an incorrect answer resets to 0.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta


LEARNING_STEPS = 6

SRS_INTERVALS: tuple[timedelta, ...] = (
    timedelta(hours=4),
    timedelta(hours=12),
    timedelta(days=1),
    timedelta(days=6),
    timedelta(days=12),
    timedelta(days=48),
    timedelta(days=96),
    timedelta(days=180),
)

SRS_LABELS: tuple[str, ...] = (
    "4 giờ",
    "12 giờ",
    "24 giờ",
    "6 ngày",
    "12 ngày",
    "48 ngày",
    "96 ngày",
    "6 tháng",
)


def utc_now() -> datetime:
    """Return a naive UTC datetime, which SQLite stores consistently."""

    return datetime.now(UTC).replace(tzinfo=None)


def complete_initial_learning(progress, now: datetime) -> None:
    progress.state = "learned"
    progress.learning_step = LEARNING_STEPS
    progress.srs_stage = 0
    progress.learned_at = now
    progress.last_reviewed_at = now
    progress.next_review_at = now + SRS_INTERVALS[0]


def apply_learning_result(progress, correct: bool, now: datetime) -> None:
    """Update the six-step acquisition phase.

    Wrong answers do not erase the successful exposures already earned; the
    same step is asked again later in the session. This makes mistakes require
    more than six total tests, matching the public Community Courses behaviour.
    """

    if progress.state == "learned":
        raise ValueError("Từ này đã hoàn tất giai đoạn học mới.")

    progress.state = "learning"
    progress.last_reviewed_at = now

    if correct:
        progress.correct_count += 1
        progress.learning_step = min(progress.learning_step + 1, LEARNING_STEPS)
        if progress.learning_step >= LEARNING_STEPS:
            complete_initial_learning(progress, now)
    else:
        progress.incorrect_count += 1
        progress.is_difficult = True


def apply_review_result(progress, correct: bool, now: datetime) -> tuple[int, int]:
    """Apply one scheduled review and return ``(stage_before, stage_after)``."""

    if progress.state != "learned":
        raise ValueError("Từ này chưa hoàn tất giai đoạn học mới.")

    before = progress.srs_stage
    progress.last_reviewed_at = now

    if correct:
        progress.correct_count += 1
        progress.srs_stage = min(before + 1, len(SRS_INTERVALS) - 1)
    else:
        progress.incorrect_count += 1
        progress.is_difficult = True
        progress.srs_stage = 0

    progress.next_review_at = now + SRS_INTERVALS[progress.srs_stage]
    return before, progress.srs_stage
