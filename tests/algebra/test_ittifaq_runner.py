"""مُشغِّلُ الاتّفاق مفحوصًا: يَرُدّ خمسةً، ويَرُدّ كلمةَ «سقف» بلا حَكَم.

**ما يُقاس ههنا**: الآلةُ وحدَها. وأرقامُ العيّنة مُصطنَعةٌ ولا تُنقَل.

`THE_CLAIM_IS_TRUE_WITH_A_QUALIFICATION`: «معدّلُ اتّفاقهما سقفُ أيّ نظام»
صائبةٌ **بتقييد**: الاتّفاقُ يقيس **ثباتَ الوسم** لا حدَّ الدقّة. فنظامٌ
يُقاس على ممتحِنٍ واحدٍ قد **يتجاوزه** بتعلُّم خصوصيّةِ ذلك الممتحِن. فما
يَحُدُّه الاتّفاقُ هو ما يُحسَب **دون تعيين أيِّهما الحَكَم**. فرُدَّت كلمةُ
«سقف» ما لم يُسَمَّ الحَكَم، وذلك التقييدُ هو الإضافة.

`A_COMPLETE_MAPPING_OR_NO_MEASUREMENT`: وجدولُ المقابلة يُعلَن **تامًّا**:
كلُّ وسمٍ في الطرفين إمّا مقابَلٌ وإمّا مُعلَنٌ «لا مقابلَ له». ووسمٌ يمرّ
بلا حكمٍ يُرَدّ باسمه، لأنّ إسقاطَه الصامتَ **يرفع الاتّفاق** بلا قياس.

`RAW_AGREEMENT_WITHOUT_CHANCE_IS_NOT_A_READING`: وعلى العيّنة: الخامُ
**٦٢٫٥٠٪** وكابّا **+٠٫٤١٤٦**. فالفرقُ واحدٌ وعشرون نقطةً تقريبًا من الصدفة
وحدَها، ومن طبع الخامَ وحدَه طبع نصفَ خبر.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

import pytest

REPOSITORY = Path(__file__).resolve().parents[2]
RUNNER_PATH = REPOSITORY / "examples" / "isnad" / "run_ittifaq.py"


def _load() -> object:
    spec = importlib.util.spec_from_file_location("run_ittifaq", RUNNER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


RUNNER = _load()


def test_a_label_that_passes_without_a_ruling_is_refused_by_name() -> None:
    """وسمٌ لم يُحكَم عليه يُرَدّ؛ وإسقاطُه الصامتُ يرفع الاتّفاقَ بلا قياس."""

    with pytest.raises(RUNNER.IttifaqError) as raised:  # type: ignore[attr-defined]
        RUNNER.Correspondence(  # type: ignore[attr-defined]
            left="كتاب",
            right="شجرة",
            pairs=(("فاعل", "subj"),),
            left_labels=("فاعل", "حال"),
            right_labels=("subj",),
        )
    assert "حال" in str(raised.value)

    # ويُقبَل متى أُعلِن «لا مقابلَ له»
    table = RUNNER.Correspondence(  # type: ignore[attr-defined]
        left="كتاب",
        right="شجرة",
        pairs=(("فاعل", "subj"), ("حال", RUNNER.NO_COUNTERPART)),  # type: ignore[attr-defined]
        left_labels=("فاعل", "حال"),
        right_labels=("subj",),
    )
    assert len(table.mapped) == 1
    assert table.declared_without_counterpart == ("حال",)


def test_the_two_coverages_do_not_bound_the_intersection_above_zero() -> None:
    """حدُّ التقاطع الأدنى صفرٌ حين تقلّ التغطيتان مجموعتين عن المدوّنة."""

    book = RUNNER.Examiner(  # type: ignore[attr-defined]
        name="جدول", unit="وسمٌ على رمز", covered=38_805, corpus=77_428
    )
    tree = RUNNER.Examiner(  # type: ignore[attr-defined]
        name="QAC", unit="حافّةٌ بين رمزين", covered=32_617, corpus=77_428
    )
    assert RUNNER.intersection_bounds(book, tree) == (0, 32_617)  # type: ignore[attr-defined]

    # ومتى زادت التغطيتان على المدوّنة لزم تقاطعٌ موجب
    wide = RUNNER.Examiner(  # type: ignore[attr-defined]
        name="واسع", unit="وسمٌ على رمز", covered=60_000, corpus=77_428
    )
    lower, upper = RUNNER.intersection_bounds(wide, book)  # type: ignore[attr-defined]
    assert lower == 60_000 + 38_805 - 77_428 == 21_377
    assert upper == 38_805


def test_an_undeclared_unit_is_refused() -> None:
    """الوحدةُ تُعلَن من مُعلَنتين؛ ووسمُ رمزٍ غيرُ حافّةٍ بين رمزين."""

    assert set(RUNNER.UNITS) == {"وسمٌ على رمز", "حافّةٌ بين رمزين"}  # type: ignore[attr-defined]
    with pytest.raises(RUNNER.IttifaqError, match="وحدةٌ غيرُ مُعلَنة"):  # type: ignore[attr-defined]
        RUNNER.Examiner(  # type: ignore[attr-defined]
            name="ثالث", unit="تبعيّة", covered=10, corpus=100
        )


def test_the_raw_rate_alone_is_refused_and_chance_must_be_named() -> None:
    """الخامُ وحدَه يُرَدّ؛ ونموذجُ الصدفة يُسمّى من مُعلَن."""

    with pytest.raises(RUNNER.IttifaqError, match="--chance"):  # type: ignore[attr-defined]
        RUNNER.report(RUNNER.SMOKE_ROWS, RUNNER.SMOKE_TABLE)  # type: ignore[attr-defined]

    with pytest.raises(RUNNER.IttifaqError, match="غيرُ مُعلَن"):  # type: ignore[attr-defined]
        RUNNER.report(  # type: ignore[attr-defined]
            RUNNER.SMOKE_ROWS,  # type: ignore[attr-defined]
            RUNNER.SMOKE_TABLE,  # type: ignore[attr-defined]
            chance_model="انتظامٌ لم يُعلَن",
            gold="كتاب",
        )


def test_the_word_ceiling_is_refused_without_a_named_gold() -> None:
    """«سقف» تحتاج حَكَمًا مُسمًّى: الاتّفاقُ يقيس الثباتَ لا حدَّ الدقّة."""

    with pytest.raises(RUNNER.IttifaqError) as raised:  # type: ignore[attr-defined]
        RUNNER.assert_gold_is_named("هذا سقفٌ لأيّ نظام", "")  # type: ignore[attr-defined]
    assert "ثباتَ" in str(raised.value)

    # وبلا الكلمة لا يُطلَب حَكَم؛ فالتقييدُ على الدعوى لا على كلّ قياس
    RUNNER.assert_gold_is_named("الاتّفاقُ كذا", "")  # type: ignore[attr-defined]
    RUNNER.assert_gold_is_named("هذا سقفٌ", "الجدولُ في إعراب القرآن")  # type: ignore[attr-defined]


def test_chance_correction_moves_the_reading_by_twenty_one_points() -> None:
    """الخامُ ٦٢٫٥٠٪ وكابّا +٠٫٤١٤٦ — والفرقُ من الصدفة وحدَها."""

    raw = RUNNER.raw_agreement(RUNNER.SMOKE_ROWS, RUNNER.SMOKE_TABLE)  # type: ignore[attr-defined]
    kappa = RUNNER.cohen_kappa(RUNNER.SMOKE_ROWS, RUNNER.SMOKE_TABLE)  # type: ignore[attr-defined]

    assert raw == Fraction(5, 8)
    assert round(float(raw) * 100, 2) == 62.50
    assert round(float(kappa), 4) == 0.4146
    assert kappa < raw
    assert round(float(raw - kappa) * 100, 1) == 21.0


def test_a_row_outside_the_declared_table_is_not_counted_silently() -> None:
    """صفٌّ خارجَ الجدول لا يُحتسَب؛ وخلوُّ المقام يُرَدّ لا يُقرَأ صفرًا."""

    table = RUNNER.SMOKE_TABLE  # type: ignore[attr-defined]
    outside = (("حال", "poss"), ("حال", "poss"))
    with pytest.raises(RUNNER.IttifaqError, match="لا صفَّ واحدٌ"):  # type: ignore[attr-defined]
        RUNNER.raw_agreement(outside, table)  # type: ignore[attr-defined]

    with pytest.raises(RUNNER.IttifaqError, match="صفٌّ واحدٌ لا تُحسَب"):  # type: ignore[attr-defined]
        RUNNER.cohen_kappa((("فاعل", "subj"),), table)  # type: ignore[attr-defined]


def test_the_smoke_run_declares_itself_synthetic(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """التشغيلُ يتمّ ويُصدِّر مخرَجَه بأنّ العيّنةَ مُصطنَعة."""

    assert RUNNER.main(["--smoke"]) == 0  # type: ignore[attr-defined]
    printed = capsys.readouterr().out
    assert "مُصطنَعة" in printed
    assert "62.50" in printed
    assert "+0.4146" in printed
    assert "الحَكَمُ المُسمّى" in printed
