"""Kiểm thử Đường đi cơ sở (Basis Path Testing) theo Đồ thị dòng điều khiển (CFG)
Hàm mục tiêu: srs.py -> apply_review_result()
Độ phức tạp Cyclomatic V(G) = 4 (tương ứng 4 đường đi độc lập).
"""

from datetime import UTC, datetime
import pytest
from models import Word, WordProgress, db
from srs import apply_review_result


def test_basis_path_1_not_learned_exception(app, add_word):
    """Đường đi 1 (Path 1): state != 'learned' -> Ném ngoại lệ ValueError."""
    word_dict = add_word(english="synergy", vietnamese="sự cộng hưởng")
    with app.app_context():
        word = db.session.get(Word, word_dict["id"])
        word.progress.state = "learning"
        db.session.commit()

        with pytest.raises(ValueError):
            apply_review_result(word.progress, correct=True, now=datetime.now(UTC).replace(tzinfo=None))


def test_basis_path_2_correct_advance_stage(app, add_word):
    """Đường đi 2 (Path 2): state == 'learned' AND correct == True AND stage < 7 -> Tăng 1 bậc."""
    word_dict = add_word(english="catalyst", vietnamese="chất xúc tác")
    with app.app_context():
        word = db.session.get(Word, word_dict["id"])
        word.progress.state = "learned"
        word.progress.srs_stage = 2
        db.session.commit()

        before, after = apply_review_result(
            word.progress, correct=True, now=datetime.now(UTC).replace(tzinfo=None)
        )
        assert before == 2
        assert after == 3
        assert word.progress.correct_count == 1


def test_basis_path_3_correct_max_stage_boundary(app, add_word):
    """Đường đi 3 (Path 3): state == 'learned' AND correct == True AND stage == 7 -> Chặn trên ở bậc 7."""
    word_dict = add_word(english="paradigm", vietnamese="mô hình, mẫu hình")
    with app.app_context():
        word = db.session.get(Word, word_dict["id"])
        word.progress.state = "learned"
        word.progress.srs_stage = 7  # Bậc tối đa (6 tháng)
        db.session.commit()

        before, after = apply_review_result(
            word.progress, correct=True, now=datetime.now(UTC).replace(tzinfo=None)
        )
        assert before == 7
        assert after == 7  # Không vượt quá 7


def test_basis_path_4_incorrect_reset_to_zero(app, add_word):
    """Đường đi 4 (Path 4): state == 'learned' AND correct == False -> Reset về 0 và bật cờ khó."""
    word_dict = add_word(english="epiphany", vietnamese="sự giác ngộ")
    with app.app_context():
        word = db.session.get(Word, word_dict["id"])
        word.progress.state = "learned"
        word.progress.srs_stage = 5
        word.progress.is_difficult = False
        db.session.commit()

        before, after = apply_review_result(
            word.progress, correct=False, now=datetime.now(UTC).replace(tzinfo=None)
        )
        assert before == 5
        assert after == 0
        assert word.progress.is_difficult is True
        assert word.progress.incorrect_count == 1
