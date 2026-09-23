"""القياسُ تحت الختم: شرطٌ واحدٌ سقط، فسقطت الثلاثةُ الباقيةُ معه.

**ترتيبُ الالتزامين هو الحجّة**: التسجيلُ `780d948a…` دُفِع في التزامٍ سابقٍ
لا رقمَ فيه، وهذا الالتزامُ يحمل الأرقامَ ويُحكَم بها لا عليها. ولم يُبدَّل
حدٌّ ولا اتّجاه — والبصمةُ المفحوصةُ في `test_maqayis_preregistration` تشهد.

والحصيلة:

| الشرط | الحدّ | المقيس | الحكم |
|---|---|---|---|
| ق-ج١ سلامةُ الحقل | ≤ ٠٫٠٥ | **٠٫٣٦٨٤** | `FALSIFIED` |
| ق-ج٢ التلوّث | ≤ ٠٫٢٠ | ٠٫٠٩٣٣ | `VOID` |
| ق-ج٣ نوعُ الجذر | ≥ ٠٫٠١ بت | ٠٫٠٠٤٤ | `VOID` |
| ق-ج٤ الفاء | ≥ ٠٫٠١ بت | ٠٫٠٤٦٠ | `VOID` |

`A_VOID_IS_NOT_A_QUIET_PASS`: الثلاثةُ الباقيةُ **لم تُحكَم**، لا أنّها نجحت
ولا أنّها سقطت. ومقاديرُها مُعلَنةٌ لأنّها تدلّ على الطريق، لا لأنّها تحمل
حكمًا. ومن قرأ ٠٫٠٤٦ حكمًا فقد نقض الختم.

`AN_IDENTIFIER_IS_NOT_A_CATEGORY`: ٩٤٫٧٪ من المحاور وردت **مرّةً واحدة**،
فالمدلولُ ههنا اسمٌ لا صنف. وقياسُ الاقتران بمتغيّرٍ يكاد يكون مُعرِّفًا
قياسٌ لشبهِ الهويّة، ولا يُقرأ حكمًا على اللغة مهما بلغ انحرافُه.
"""

from __future__ import annotations

from fractions import Fraction

from test_maqayis_preregistration import PREDICTIONS, REPLICATES, SEED

from algebra.signified import Verdict

# ما قرأه العدُّ من maqayis_by_root_csv_999.csv (٤٬٥٧٦ صفًّا)
ROWS = 4_576
UNREADABLE_COUNT_FIELD = 864
STRICT_MISMATCH = 1_686
RESTRICTED_MISMATCH = 822
RESTRICTED_ROWS = 3_712

PAIRS = 3_217
DISTINCT_AXES = 2_936
SINGLETON_AXES = 2_781
CONTAMINATED = 300

ENTROPY_OF_AXIS = Fraction("11.4193")
ROOT_TYPE_EXCESS = Fraction("0.004442")
ROOT_TYPE_Z = Fraction("0.94")
FIRST_RADICAL_EXCESS = Fraction("0.046006")
FIRST_RADICAL_Z = Fraction("15.66")


def test_the_field_integrity_condition_is_falsified() -> None:
    """ق-ج١ يسقط بفارقٍ سبعةِ أضعاف: ٣٦٫٨٪ مقابل حدٍّ ٥٪.

    وبالقراءة المقيَّدة (على الصفوف التي يُقرَأ عددُها) ٢٢٫١٪ — وهي أيضًا فوق
    الحدّ بأربعة أضعاف. فالحكمُ واحدٌ على القراءتين، ولم يُحتَج إلى ترجيح.
    """

    strict = Fraction(STRICT_MISMATCH, ROWS)
    restricted = Fraction(RESTRICTED_MISMATCH, RESTRICTED_ROWS)
    assert round(float(strict), 4) == 0.3684
    assert round(float(restricted), 4) == 0.2214
    assert ROWS - RESTRICTED_ROWS == UNREADABLE_COUNT_FIELD
    integrity = PREDICTIONS[0]
    assert integrity.verdict(strict) is Verdict.FALSIFIED
    assert integrity.verdict(restricted) is Verdict.FALSIFIED
    assert strict > 7 * integrity.threshold


def test_the_three_remaining_conditions_are_void_not_judged() -> None:
    """ما يقوم على الحقل الساقط يُحكَم VOID — ولا يُقرَأ نجاحًا ولا سقوطًا."""

    measured = (
        Fraction(CONTAMINATED, PAIRS),
        ROOT_TYPE_EXCESS,
        FIRST_RADICAL_EXCESS,
    )
    for prediction, value in zip(PREDICTIONS[1:], measured, strict=True):
        assert prediction.verdict(value, void=True) is Verdict.VOID
    # ولولا السقوطُ لكانت أحكامُها هذه — وتُذكَر لبيان الطريق لا للاحتجاج
    assert PREDICTIONS[1].verdict(measured[0]) is Verdict.MET
    assert PREDICTIONS[2].verdict(measured[1]) is Verdict.FALSIFIED
    assert PREDICTIONS[3].verdict(measured[2]) is Verdict.MET


def test_the_oracle_is_not_heavily_circular() -> None:
    """التلوّثُ ٩٫٣٪: ابنُ فارسٍ لا يشرح الجذرَ بمشتقٍّ منه في الأغلب.

    وهذا أنفعُ ما في القياس وإن كان VOID: لو جاء التلوّثُ عاليًا لكان كلُّ
    ارتباطٍ بين صورةٍ ومدلولٍ مضمونًا بالإنشاء. فالأوراكلُ صالحٌ في هذا الوجه،
    والعطبُ في **استخراجه** لا في **مصدره**.
    """

    share = Fraction(CONTAMINATED, PAIRS)
    assert round(float(share), 4) == 0.0933
    assert share < PREDICTIONS[1].threshold
    assert share < Fraction(1, 10)


def test_the_signified_here_is_an_identifier_not_a_category() -> None:
    """٩٤٫٧٪ من المحاور فردةٌ، فالمدلولُ اسمٌ لا صنف — وهذا حدُّ القياس كلِّه."""

    singleton_share = Fraction(SINGLETON_AXES, DISTINCT_AXES)
    assert round(float(singleton_share), 3) == 0.947
    assert DISTINCT_AXES > PAIRS * 9 // 10
    assert float(ENTROPY_OF_AXIS) > 11


def test_the_first_radical_carries_a_measurable_but_tiny_share() -> None:
    """الفاءُ تحمل ٠٫٠٤٦ بت: انحرافُها ١٥٫٧ وحصّتُها **٠٫٤٪** من H(المحور).

    والرقمان يقولان شيئين لا شيئًا واحدًا: الاقترانُ **ليس صدفة** (z كبير)،
    وهو **ضئيلٌ جدًّا** (أربعةٌ من الألف من إنتروبيا المدلول). ونوعُ الجذر
    دونه بعشرة أضعاف وبانحرافٍ لا يبلغ الواحد — فالبنيةُ الصرفيّةُ الخشنة
    لا تقول عن المدلول شيئًا يُذكَر.
    """

    assert FIRST_RADICAL_Z > 15
    assert ROOT_TYPE_Z < 1
    assert FIRST_RADICAL_EXCESS > 10 * ROOT_TYPE_EXCESS
    share = FIRST_RADICAL_EXCESS / ENTROPY_OF_AXIS
    assert round(float(share) * 100, 3) == 0.403
    assert share < Fraction(1, 200)


def test_the_measurement_is_bound_to_its_declared_seed_and_replicates() -> None:
    """البذرةُ والتكرارُ معطَيان مُعلَنان، فالرقمُ يُعاد حرفًا أو لا يُصدَّق."""

    assert (REPLICATES, SEED) == (2_000, 20_260_923)


def test_the_row_count_disagrees_with_an_earlier_deposit() -> None:
    """٤٬٥٧٦ صفًّا ههنا و٤٬٥٦٢ في تدقيق مصفوفة الحركة — فرقُ ١٤.

    و«الثلاثيّ» ٤٬٠٨٩ ههنا و٤٬٠٨٧ مُجمَّدًا هناك — فرقُ ٢. والرقمان من الملفّ
    نفسِه في الشجرة نفسِها، فأحدُ العَدَّين على تصفيةٍ غيرِ مُعلَنة. ويُسجَّل
    التخالفُ ولا يُرجَّح أحدُهما ههنا.
    """

    assert ROWS - 4_562 == 14
    assert 4_089 - 4_087 == 2
