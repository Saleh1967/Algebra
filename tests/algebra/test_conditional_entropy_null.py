"""صفريُّ الاشتراك: النتيجةُ صائبةٌ والعلّةُ المذكورةُ ليست العلّة.

**ما يُقاس ههنا**: الآلةُ والحساب. لا مدوّنةَ تُقرَأ، وأرقامُ الأمثلة صغيرةٌ
مصنوعةٌ ليُرى الفرقُ بالعين.

`THE_DIAGNOSIS_HOLDS_AND_ITS_STATED_REASON_DOES_NOT`: قيل إنّ الصفريَّ أعطى
`H(معنى|لفظ)` **مطابقًا للمرصود** لأنّه «يحفظ هامشَي الجدول». والحكمُ صائب —
ذلك هُويّةٌ لا صفريّ — **والعلّةُ المذكورةُ باطلة**: جدولان ٢×٢ هامشا صفوفهما
(٤، ٤) وهامشا أعمدتهما (٤، ٤) يعطيان ٠٫٨١١٣ و١٫٠٠٠٠ بت — فرقُ **٠٫١٨٨٧**.
فحفظُ الهامشين **لا يثبّت** الإنتروبيا الشرطيّة.

`WHAT_ACTUALLY_FIXES_IT_IS_THE_ROW_PROFILE`: والذي يثبّتها حفظُ **ملمحِ كلّ
صفّ** — أي تبديلُ أسماء المعاني وحدَها دون تغيير كم وقعت كلُّ لفظةٍ بكلّ معنًى.
وذلك مطابقٌ إلى آخر رقمٍ **بالبناء**، لأنّ `H(M|W=w)` تُحسَب من ملمح الصفّ ولا
ترى الأسماء.

**ولماذا يهمّ الفرق؟** لأنّ التشخيصَ يوجّه الإصلاح. فمن ظنّ العلّةَ حفظَ
الهامشين انتقل إلى إعادةِ ربطٍ تحفظ الهامشين **وهي صفريٌّ صحيح** — فيظنّ أنّه
عالج وهو قد بنى المقياسَ الذي كان يطلبه. والعكسُ بالعكس.

`A_COVERAGE_PERCENTAGE_DECLARES_ITS_DENOMINATOR`: و٥٩٬٤٤٣ على ٧٧٬٤٢٨ =
**٧٦٫٨٪** لا ٨٠٫٢٪. ولـ٨٠٫٢٪ مقامٌ آخرُ قدرُه ٧٤٬١١٨ لم يُسَمَّ. فأحدُهما
يُصحَّح، وهو الموضعُ السادسَ عشرَ من هذا الجنس.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import (
    BOTH_MARGINS_DO_NOT_FIX_A_CONDITIONAL_ENTROPY_NOTE,
    CONDITIONING_SIDES,
    SIGNIFIED_NAMED_RESIDUALS,
    conditional_entropy,
)

MUSHAF = 77_428
MEASURED_TOKENS = 59_443

SHARING = 2.3514  # H(معنى | لفظ)
SYNONYMY = 0.9591  # H(لفظ | معنى)
SYNONYMY_NULL = 0.0549


def _pairs(table: tuple[tuple[int, ...], ...]) -> list[tuple[str, str]]:
    """جدولُ تكراراتٍ إلى أزواج؛ الصفُّ صورةٌ والعمودُ مدلول."""

    out: list[tuple[str, str]] = []
    for row, counts in enumerate(table):
        for column, count in enumerate(counts):
            out.extend([(f"ص{row}", f"م{column}")] * count)
    return out


def test_two_tables_share_both_margins_and_differ_in_conditional_entropy() -> None:
    """(٤،٤) صفوفًا و(٤،٤) أعمدةً، و٠٫٨١١٣ مقابل ١٫٠٠٠٠ — فالعلّةُ ليست الهامشين."""

    tight = ((3, 1), (1, 3))
    flat = ((2, 2), (2, 2))

    for table in (tight, flat):
        assert [sum(row) for row in table] == [4, 4]
        assert [sum(column) for column in zip(*table, strict=True)] == [4, 4]

    one = conditional_entropy(_pairs(tight), given="صورة")
    other = conditional_entropy(_pairs(flat), given="صورة")
    assert round(one, 4) == 0.8113
    assert round(other, 4) == 1.0
    assert round(other - one, 4) == 0.1887
    assert one != other


def test_preserving_each_row_profile_is_the_identity_to_the_last_digit() -> None:
    """تبديلُ أسماء المعاني وحدَها لا يحرّك الرقم — وهو الحفظُ الفعليّ."""

    table = ((3, 1), (1, 3))
    relabelled = ((1, 3), (3, 1))  # العمودان متبادلان، والملمحُ محفوظ

    assert conditional_entropy(_pairs(table), given="صورة") == conditional_entropy(
        _pairs(relabelled), given="صورة"
    )

    # وليس ذلك صدفةَ تماثل: جدولٌ غيرُ متماثلٍ يُعطي الحكمَ نفسَه
    skewed = ((5, 1), (2, 2))
    swapped = ((1, 5), (2, 2))
    assert conditional_entropy(_pairs(skewed), given="صورة") == conditional_entropy(
        _pairs(swapped), given="صورة"
    )


def test_the_two_directions_are_two_numbers_and_the_side_is_named() -> None:
    """الاشتراكُ والترادفُ اتّجاها معلومةٍ واحدة، ورقمان لا رقم."""

    assert CONDITIONING_SIDES == ("صورة", "مدلول")

    table = ((5, 1), (2, 2))
    forward = conditional_entropy(_pairs(table), given="صورة")
    backward = conditional_entropy(_pairs(table), given="مدلول")
    assert round(forward, 4) != round(backward, 4)

    # وعلى الأرقام المنشورة: الاشتراكُ ٢٫٤٥ أضعافِ الترادف
    assert round(SHARING / SYNONYMY, 4) == 2.4517
    assert SHARING > SYNONYMY


def test_the_second_direction_stands_because_its_null_is_far_below_it() -> None:
    """٠٫٩٥٩١ مقابل ٠٫٠٥٤٩ = ١٧٫٤٧ ضعفًا؛ فالرقمُ الثاني يُنقَل والأوّلُ يُوقَف."""

    lift = SYNONYMY / SYNONYMY_NULL
    assert round(lift, 2) == 17.47
    assert lift > 17

    # وأمّا الأوّلُ فصفريُّه يساوي مرصودَه، فالرفعُ واحدٌ صحيحٌ ولا يُقرَأ
    assert SHARING / SHARING == 1.0


def test_a_coverage_percentage_declares_its_denominator() -> None:
    """٥٩٬٤٤٣ / ٧٧٬٤٢٨ = ٧٦٫٨٪؛ ولـ٨٠٫٢٪ مقامٌ آخرُ قدرُه ٧٤٬١١٨ لم يُسَمَّ."""

    measured = Fraction(MEASURED_TOKENS, MUSHAF)
    assert round(float(measured) * 100, 1) == 76.8
    assert round(float(measured) * 100, 1) != 80.2

    implied = round(MEASURED_TOKENS / 0.802)
    assert implied == 74_118
    assert implied < MUSHAF
    assert MUSHAF - implied == 3_310


def test_the_named_residue_states_the_correction_not_the_symptom() -> None:
    """البقيّةُ تقول ما يثبّت الرقمَ لا ما لا يثبّته وحدَه."""

    assert BOTH_MARGINS_DO_NOT_FIX_A_CONDITIONAL_ENTROPY_NOTE in (
        SIGNIFIED_NAMED_RESIDUALS
    )
    assert "ملمحِ كلّ صفٍّ" in BOTH_MARGINS_DO_NOT_FIX_A_CONDITIONAL_ENTROPY_NOTE
    assert "هُويّةٌ لا صفريّ" in BOTH_MARGINS_DO_NOT_FIX_A_CONDITIONAL_ENTROPY_NOTE
    assert len(set(SIGNIFIED_NAMED_RESIDUALS)) == len(SIGNIFIED_NAMED_RESIDUALS)
