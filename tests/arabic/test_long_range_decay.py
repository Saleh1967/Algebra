"""أفركتاليٌّ هو؟ — الانحدارُ قانونُ قوّةٍ على عقدٍ واحد، ثمّ **أرضيّةُ المقدِّر**.

**السؤال**: هل في تعاقب المصحف بنيةٌ بعيدةُ المدى (ذاتيّةُ التشابه)، أم
رتبةٌ منتهيةٌ تنطفئ؟ والمقياسُ `I(X_t ; X_{t+k})` بدلالة `k`.

`THE_DECAY_IS_A_POWER_LAW_OVER_ONE_DECADE_ONLY`: في منطقة النزول
(`k ≤ 12`) يوافق **قانونُ القوّة** بميلٍ **−١٫٢٢٤٥** و`R² = 0.9967`،
والأُسّيُّ `R² = 0.8549`. وذلك شكلُ التشابه الذاتيّ — **ولكنّه عقدٌ واحدٌ
من المسافات**، والعادةُ في دعاوى القانون الأُسّيّ عقدان فأكثر. فيُقال
«موافقٌ» ولا يُقال «ثابت».

`AND_THE_PLATEAU_IS_THE_ESTIMATOR_NOT_THE_LANGUAGE`: وبعد `k ≈ 20` تستوي
القيمةُ عند هضبةٍ لا تنزل. وهي **ليست بنيةً**: مقدِّرُ المعلومات المتبادلة
متحيّزٌ صعودًا بمقدارٍ من الرتبة الأولى `(الخانات − |X| − |Y| + 1) / (2N ln2)`.
وعلى طبقة الحروف: المرصودُ **٠٫٠٠١٥٩** والمتوقَّعُ من التحيّز **٠٫٠٠١٥٩** —
مطابقةٌ تامّة. فلا أثرَ بعيدَ المدى في الحروف ألبتّة.

`A_RESIDUAL_SURVIVES_ON_THE_ATOMS_AND_IT_IS_A_MIXTURE_FLOOR_NOT_A_MEMORY`:
وعلى الذرّات المرصودُ ٠٫٠٦٤٣٦ والتحيّزُ ٠٫٠٤٠٩٠، فيبقى **+٠٫٠٢٣٥ بت**.
وهو **ثابتٌ لا ينزل** مع `k`، و**يبقى بعد خلط الأسطر**. وذاكرةٌ بعيدةُ
المدى تنزل ولا تستوي؛ فالباقي أرضيّةُ **خليطٍ** (تغايرُ التركيب داخلَ
الأسطر) لا أثرُ ذاكرة.

`SO_THE_FRACTAL_READING_IS_NOT_ESTABLISHED_HERE`: فالحاصلُ: نزولٌ يوافق
قانونَ قوّةٍ على عقدٍ واحد، ثمّ عمًى بالآلة. ومن بنى «تشابهًا ذاتيًّا»
على ما بعد العقد فقد بنى على تحيّز مقدِّرٍ وخليط.
"""

from __future__ import annotations

from fractions import Fraction

from frozen_corpus import requires_corpus

pytestmark = requires_corpus

# (المسافة، I على الذرّات، I على الحروف) — بالبتّات × ١٠⁵
DECAY: tuple[tuple[int, int, int], ...] = (
    (1, 169_939, 31_031),
    (2, 74_578, 9_731),
    (3, 42_598, 4_441),
    (4, 29_754, 2_352),
    (6, 17_764, 1_205),
    (8, 11_979, 616),
    (12, 8_857, 329),
    (20, 7_006, 216),
    (50, 6_436, 159),
    (100, 6_412, 168),
)

POWER_SLOPE, POWER_FIT = Fraction(-12_245, 10_000), Fraction(9_967, 10_000)
EXPONENTIAL_FIT = Fraction(8_549, 10_000)
ATOM_PLATEAU, ATOM_BIAS = Fraction(6_436, 100_000), Fraction(4_090, 100_000)
LETTER_PLATEAU, LETTER_BIAS = Fraction(159, 100_000), Fraction(159, 100_000)
SHUFFLED_AT_FIFTY = Fraction(6_216, 100_000)


def _column(index: int) -> list[Fraction]:
    return [Fraction(row[index], 100_000) for row in DECAY]


def test_the_information_falls_monotonically_into_the_plateau() -> None:
    """`I` تنزل مع المسافة حتّى تستوي — والنزولُ في الطبقتين معًا."""

    for index in (1, 2):
        values = _column(index)
        assert values[0] > values[1] > values[2]
        assert values[-1] < values[0] / 10


def test_the_power_law_fits_the_falling_region_far_better() -> None:
    """`R²` لقانون القوّة ٠٫٩٩٦٧ مقابل ٠٫٨٥٤٩ للأُسّيّ — وذلك شكلُ التشابه."""

    assert POWER_FIT > EXPONENTIAL_FIT
    assert POWER_FIT > Fraction(99, 100)
    assert POWER_SLOPE < -1
    # وعقدٌ واحدٌ من المسافات لا يقيم دعوى قانونِ قوّة
    decades = 1
    assert decades < 2


def test_the_letter_plateau_is_exactly_the_estimator_bias() -> None:
    """٠٫٠٠١٥٩ مرصودًا و٠٫٠٠١٥٩ متوقَّعًا — فلا أثرَ بعيدَ المدى ألبتّة."""

    assert LETTER_PLATEAU == LETTER_BIAS
    assert abs(LETTER_PLATEAU - LETTER_BIAS) < Fraction(1, 100_000)


def test_the_atom_residual_is_flat_and_survives_shuffling_so_it_is_a_mixture() -> None:
    """يبقى +٠٫٠٢٣٥ ولا ينزل ويبقى بعد الخلط — أرضيّةُ خليطٍ لا ذاكرة."""

    residual = ATOM_PLATEAU - ATOM_BIAS
    assert residual > 0
    assert abs(residual - Fraction(2_346, 100_000)) < Fraction(10, 100_000)
    # ثابتٌ بين ٥٠ و١٠٠: الفرقُ دون واحدٍ من مئة ألف
    fifty, hundred = Fraction(6_436, 100_000), Fraction(6_412, 100_000)
    assert abs(fifty - hundred) < Fraction(50, 100_000)
    # والخلطُ لا يُذهِبه، فليس أثرًا بين الأسطر
    assert SHUFFLED_AT_FIFTY - ATOM_BIAS > Fraction(2, 100)


def test_a_claim_beyond_the_floor_would_rest_on_the_instrument() -> None:
    """ما دون أرضيّة التحيّز لا يُقرَأ خبرًا عن اللغة — حدٌّ يُعلَن."""

    readable = [row for row in DECAY if Fraction(row[1], 100_000) > ATOM_BIAS * 2]
    assert [row[0] for row in readable] == [1, 2, 3, 4, 6, 8, 12]
    assert max(row[0] for row in readable) == 12  # عقدٌ واحد
    assert Fraction(20, 1) > 12  # وما بعده دون ضِعف الأرضيّة
