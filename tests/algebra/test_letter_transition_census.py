"""تعدادُ الانتقالات مفحوصًا على رسمٍ مصنوع: التساوي يُعلَن، والهامشان موضعيّان.

**ولا مدوّنةَ ههنا**: الكلماتُ تُكتَب في هذا الملفّ وتُحسَب بصمتُها من
بايتاتها. فالمفحوصُ آلةُ التعداد لا رقمٌ عن العربيّة.

`THE_LESSON_OF_THE_INFLATED_EXPECTATION_IS_A_TEST_NOW`: وهامشٌ محسوبٌ على
الحروف كلِّها يضخّم المتوقَّع — وقد فعل مرّةً (٣٨١ بدل ٢١٤). فيُفحَص ههنا
بحالةٍ مصنوعةٍ يظهر فيها الفرق: حرفٌ يكثر في آخر الكلمة لا يبدأ زوجًا،
فنصيبُه في هامش السابق **صفرٌ** وإن كثر في النصّ.
"""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from fractions import Fraction
from pathlib import Path
from types import ModuleType

import pytest

REPOSITORY = Path(__file__).resolve().parents[2]
RUNNER_PATH = REPOSITORY / "examples" / "rasm" / "run_letter_transitions.py"


def _runner() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_letter_transitions", RUNNER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


transitions = _runner()

WORDS = ("بات", "باب", "تاب", "ناب")


def _write(folder: Path, words: tuple[str, ...] = WORDS) -> tuple[Path, str, int]:
    lines = ["loc\tsurface"]
    for index, word in enumerate(words, start=1):
        lines.append(f"1:1:{index}\t{word}")
    path = folder / "aligned.tsv"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path, hashlib.sha256(path.read_bytes()).hexdigest(), len(words)


def test_the_pairs_are_consecutive_and_never_cross_a_word(tmp_path: Path) -> None:
    """الزوجُ متعاقبٌ داخلَ الكلمة، ولا يُصنَع من آخر كلمةٍ وأوّلِ التي تليها."""

    pairs, first, second, places = transitions.census(["بات", "ناب"])
    assert places == 4  # زوجان في كلّ كلمةٍ من ثلاثة أحرف
    assert pairs[("ب", "ا")] == 1 and pairs[("ا", "ت")] == 1
    assert pairs[("ن", "ا")] == 1 and pairs[("ا", "ب")] == 1
    assert ("ت", "ن") not in pairs  # ولو عبر الحدَّ لصُنِع هذا الزوج
    assert sum(pairs.values()) == places
    assert sum(first.values()) == sum(second.values()) == places


def test_a_final_letter_carries_no_weight_in_the_first_margin() -> None:
    """حرفٌ لا يقع إلّا آخرًا نصيبُه في هامش السابق صفرٌ وإن كثر في النصّ."""

    _, first, second, _ = transitions.census(["ابت", "ابت", "ابت"])
    assert second["ت"] == 3
    assert first["ت"] == 0  # فلا يبدأ زوجًا ألبتّة
    assert first["ا"] == 3 and second["ا"] == 0


def test_the_expectation_uses_positional_margins_not_totals() -> None:
    """المتوقَّعُ من الهامشين الموضعيّين؛ وزوجٌ صدرُه حرفٌ نهائيٌّ متوقَّعُه صفر."""

    words = ["ابت", "ابت", "ابت"]
    _, first, second, places = transitions.census(words)
    assert transitions.expectation(first, second, places, ("ت", "ا")) == 0
    assert transitions.expectation(first, second, places, ("ا", "ب")) == Fraction(
        3 * 3, places
    )

    with pytest.raises(transitions.TransitionError):
        transitions.expectation(first, second, 0, ("ا", "ب"))


def test_a_tie_at_the_top_is_declared_and_not_broken() -> None:
    """أربعةُ أزواجٍ بعدٍّ واحد: الصدارةُ لمجموعةٍ، ولا يُنتقى منها أوّل."""

    pairs, _, _, _ = transitions.census(["اب", "تث", "جح", "دذ"])
    highest, leaders = tied_leaders = transitions.tied_leaders(pairs)
    assert highest == 1
    assert len(leaders) == 4
    assert leaders == sorted(leaders)  # مسرودةٌ كلُّها، ولا واحدَ يُقدَّم حكمًا
    assert tied_leaders[0] == highest


def test_the_probability_rows_sum_to_one_where_they_exist() -> None:
    """كلُّ صفٍّ مبنيٍّ يجمع إلى الواحد بكسورٍ صحيحة، ولا يُصطنَع صفٌّ لغائب."""

    pairs, first, _, _ = transitions.census(list(WORDS))
    rows = transitions.rows_of_probability(pairs, first)
    for row in rows.values():
        assert sum(row.values()) == 1
    assert set(rows) <= set(first)
    assert "ت" not in rows or first["ت"] > 0


def test_the_run_refuses_a_wrong_digest_or_closure_or_policy(tmp_path: Path) -> None:
    """بصمةٌ أو إغلاقٌ أو سياسةٌ مخالفةٌ تردُّ التشغيل، ولا تُقرَّب."""

    path, digest, rows = _write(tmp_path)
    with pytest.raises(transitions.TransitionError):
        transitions.read_words(path, "مطويّ", "0" * 64, rows)
    with pytest.raises(transitions.TransitionError):
        transitions.read_words(path, "مطويّ", digest, rows + 1)
    with pytest.raises(transitions.TransitionError):
        transitions.read_words(path, "سياسةٌ لا وجودَ لها", digest, rows)


def test_a_declared_inventory_that_differs_stops_the_run(tmp_path: Path) -> None:
    """الجردُ مقامٌ يُعلَن قبل الجدول؛ ومخالفتُه توقِف التشغيل لا تُطوى."""

    path, digest, rows = _write(tmp_path)
    parser = transitions.build_argument_parser()
    arguments = parser.parse_args(
        [
            "--aligned",
            str(path),
            "--digest",
            digest,
            "--closure",
            str(rows),
            "--policy",
            "مطويّ",
            "--expect-letters",
            "99",
        ]
    )
    with pytest.raises(transitions.TransitionError) as raised:
        transitions.run(arguments)
    assert "المقامُ يُعلَن قبل الجدول" in str(raised.value)


def test_a_full_run_prints_the_inventory_and_the_tie(tmp_path: Path) -> None:
    """الجردُ والخاناتُ والمواضعُ والصدارةُ المتساويةُ مطبوعةٌ مع النسبة."""

    path, digest, rows = _write(tmp_path)
    arguments = transitions.build_argument_parser().parse_args(
        [
            "--aligned",
            str(path),
            "--digest",
            digest,
            "--closure",
            str(rows),
            "--policy",
            "مطويّ",
        ]
    )
    lines = transitions.run(arguments)
    joined = "\n".join(lines)
    assert "النسبة:" in joined and "مطويّ" in joined
    assert "الجرد:" in joined and "الصدارة:" in joined
    assert "والتساوي يُعلَن ولا يُكسَر" in joined
