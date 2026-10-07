"""البرهانُ الثالثُ مقيسًا: ثنائيّةٌ **مرصودةٌ بشكلها**، لا مبرهنةٌ بتعريفها.

**ما جرى**: البرهانُ الثالثُ صيغةٌ تنتظر رقمًا، والمدوّنةُ المشكولةُ عندي
(بصمةُ المصدر `46b4393fdb3a0920…`). فشُغِّل ولم يُؤجَّل.

`THE_ARGUMENT_OFFERED_WAS_VACUOUS_AND_THE_CONCLUSION_IS_TRUE_ANYWAY`: قيل:
«الإنتروبيا لا تتجزّأ — صفرٌ أو موجب، فالثنائيّةُ مبرهنةٌ من تعريفها». وذلك
**لا يُبرهِن شيئًا**: كلُّ مقدارٍ متّصلٍ صفرٌ أو موجب، وحجمُ أسرة الصيغ في
البرهان الثاني كذلك — وقد حُكِم عليه هناك بأنّه **سلّمٌ متّصل**. فالصيغةُ
نفسُها لا تفرّق بين البرهانين.

`WHAT_PROVES_IT_IS_THE_SHAPE_AND_THE_SHAPE_IS_BIMODAL`: والذي يفرّق
**شكلُ التوزيع**. وعلى الأنواع ذاتِ عشرة وقوعاتٍ فأكثر (١٬٠٠٨ نوعًا):
**٤٩٠ عند الصفر بالضبط**، ثمّ **وادٍ** فيه ٤٣ فقط دون ٠٫٣٠ بت، ثمّ تلٌّ
ثانٍ فيه ٤٧٥ وسيطُه ٠٫٩٠. **قمّتان وفجوةٌ بينهما.** فالبرهانُ الثالثُ قائم —
بدليلٍ غيرِ الذي قُدِّم له.

`FIFTY_NINE_PERCENT_OF_THE_VERDICT_WAS_ARITHMETIC_NOT_GRAMMAR`: والخطرُ
الذي لم يُسَمَّ: نوعٌ وقع **مرّةً واحدة** إنتروبيتُه صفرٌ **بالضرورة**.
وثمانيةُ آلافٍ وسبعُ مئةٍ واثنان وتسعون من ١٤٬٩٥٧ نوعًا (**٥٨٫٨٪**) وقعت
مرّةً. فالنسبةُ المجمَّعةُ **٨٨٫٦٪** أكثرُها حسابٌ لا نحو، ولا تُقرَأ وحدَها.

`AND_AFTER_THE_CONTROL_THE_SIGNAL_IS_ENORMOUS`: فيُصنَّف بعدد الوقوعات
ويُقابَل بصفريٍّ محسوب (`Σ pᵢⁿ`): عند وقوعين ٨٤٫٩٪ مقابل ٢٥٫٧٪، وعند
ثلاثةٍ إلى أربعةٍ ٧٤٫٥٪ مقابل ٦٫٧٪، **وعند خمسةٍ إلى تسعةٍ ٦٤٫٤٪ مقابل
٠٫٧٪ — نحوُ اثنين وتسعين ضعفًا**. فالثباتُ خبرٌ، والمجمَّعُ كان يُخفيه لا يُظهره.

`THE_MACHINE_RECOVERED_THE_GRAMMARIANS_CLASS_WITH_NO_GRAMMAR_IN_IT`: وأكثرُ
أربعةَ عشرَ نوعًا ثباتًا (خمسون وقوعًا فأكثر): فى · ما · لا · ولا · وما ·
إلى · قال · ثمّ · به · كان · ذلك · له · الذي · هو. **وكلُّها مبنيٌّ عند
النحاة** — والحروفُ والضمائرُ والإشاراتُ والموصولاتُ ومضاراعُ الماضي. ولم
يدخل الحسابَ وسمٌ نحويٌّ واحد: رسمٌ وحركةٌ أخيرةٌ لا غير. **فالصنفُ الموروثُ
استُرجِع من الصوت وحدَه.**
"""

from __future__ import annotations

from fractions import Fraction

from algebra.evaluation import ClusteredSample
from algebra.reconciliation import Partition, rounds_to

SOURCE_DIGEST = "46b4393fdb3a09208ecb96fbbac990a150e4374f82d7940c655430cd1b1611ae"

TYPES, TOKENS = 14_957, 77_398
HAPAX = 8_792
POOLED_FROZEN = Fraction("0.886")

# (وقوعات، أنواع، ثابتٌ مرصود٪، ثابتٌ صفريّ٪)
BANDS: tuple[tuple[str, int, float, float], ...] = (
    ("١", 8_792, 100.0, 100.0),
    ("٢", 2_380, 84.9, 25.7),
    ("٣–٤", 1_630, 74.5, 6.7),
    ("٥–٩", 1_147, 64.4, 0.7),
    ("١٠–٤٩", 806, 50.4, 0.0),
    ("٥٠+", 202, 41.6, 0.0),
)

RICH_TYPES = 1_008
SHAPE = {"صفرٌ تامّ": 490, "وادٍ": 43, "تلٌّ ثانٍ": 475}
SMALLEST_POSITIVE = 0.0137
MEDIAN_POSITIVE = 0.9044

TOP_FROZEN = (
    "فى",
    "ما",
    "لا",
    "ولا",
    "وما",
    "إلى",
    "قال",
    "ثم",
    "به",
    "كان",
    "ذلك",
    "له",
    "ٱلذى",
    "هو",
)


def test_more_than_half_the_types_are_frozen_by_arithmetic() -> None:
    """٨٬٧٩٢ من ١٤٬٩٥٧ وقعت مرّةً — وإنتروبيتُها صفرٌ بالضرورة لا بالنحو."""

    assert Fraction(HAPAX, TYPES) > Fraction(1, 2)
    assert rounds_to(Fraction(HAPAX, TYPES) * 100, 1) == Fraction("58.8")

    # والمجمَّعُ ٨٨٫٦٪ — وأكثرُه هذا، فلا يُقرَأ وحدَه
    assert POOLED_FROZEN > Fraction(HAPAX, TYPES)
    assert BANDS[0][2] == 100.0 == BANDS[0][3]  # فالصفريُّ يساوي المرصودَ تمامًا

    assert (
        Partition(parts=tuple(one[1] for one in BANDS), declared_total=TYPES).residue
        == 0
    )


def test_after_stratification_the_lift_is_large_and_grows() -> None:
    """٣× ثمّ ١١× ثمّ ٩٣× — والرفعُ يشتدّ كلّما كثرت الفرصُ للتغيّر."""

    lifts = [observed / chance for _, _, observed, chance in BANDS if chance > 0]
    assert [round(one) for one in lifts] == [1, 3, 11, 92]
    assert lifts == sorted(lifts)  # فالرفعُ متزايدٌ لا متذبذب

    # وعند خمسةٍ إلى تسعةٍ: ٦٤٫٤٪ مقابل ٠٫٧٪ ⇒ ٩٢×. وطبع المُشغِّلُ ٩٣×
    # لأنّه قسم على صفريٍّ غيرِ مقرَّب؛ والفرقُ واحدٌ من التقريب لا من العدّ.
    band = next(one for one in BANDS if one[0] == "٥–٩")
    assert band[2] > band[3] * 90
    assert round(band[2] / band[3]) == 92


def test_the_distribution_is_bimodal_not_a_continuum() -> None:
    """٤٩٠ عند الصفر · وادٍ فيه ٤٣ · تلٌّ ثانٍ فيه ٤٧٥ — قمّتان وفجوة."""

    assert sum(SHAPE.values()) == RICH_TYPES
    assert (
        Partition(parts=tuple(SHAPE.values()), declared_total=RICH_TYPES).residue == 0
    )

    valley = SHAPE["وادٍ"]
    assert valley * 10 < SHAPE["صفرٌ تامّ"]
    assert valley * 10 < SHAPE["تلٌّ ثانٍ"]
    assert abs(SHAPE["صفرٌ تامّ"] - SHAPE["تلٌّ ثانٍ"]) < SHAPE["تلٌّ ثانٍ"] // 4

    # وأصغرُ قيمةٍ موجبةٍ ٠٫٠١٣٧ ووسيطُ الموجب ٠٫٩٠ — فالفجوةُ لا التصاق
    assert SMALLEST_POSITIVE < 0.02
    assert MEDIAN_POSITIVE > SMALLEST_POSITIVE * 60


def test_the_offered_argument_does_not_separate_it_from_the_second_proof() -> None:
    """«صفرٌ أو موجب» تصدق على حجم الأسرة أيضًا — وقد حُكِم عليه بالاتّصال.

    فالصيغةُ لا تفرّق بين برهانٍ ثالثٍ قائمٍ وثانٍ موقوف؛ الذي يفرّق الشكلُ.
    والبرهانُ الثاني **قاس شكلَه فأحسن**، والثالثُ اكتفى بالتعريف — وجاء
    الشكلُ في صفّه، وذلك حظٌّ لا حجّة.
    """

    family_sizes_singleton = Fraction("0.391")  # ٣٩٫١٪ وحيدةُ الصيغة
    assert Fraction(0) < family_sizes_singleton < 1  # صفرٌ أو موجبٌ كذلك

    # والفرقُ: هناك ذيلٌ متّصل (١٧٫٨ ثمّ ١٠٫٥ ثمّ ٦٫٣)، وههنا وادٍ
    continuous_tail = (17.8, 10.5, 6.3)
    assert continuous_tail == tuple(sorted(continuous_tail, reverse=True))
    assert min(continuous_tail) > SHAPE["وادٍ"] / RICH_TYPES * 100  # ٤٫٣٪

    # فالسلّمُ ينزل بانتظامٍ، والقمّتان يفصلهما انخفاضٌ ثمّ ارتفاع
    assert SHAPE["وادٍ"] < SHAPE["تلٌّ ثانٍ"]


def test_the_recovered_class_is_the_one_the_grammarians_named() -> None:
    """أربعةَ عشرَ نوعًا أشدَّ ثباتًا، وكلُّها مبنيٌّ — بلا وسمٍ نحويٍّ واحد."""

    assert len(TOP_FROZEN) == 14
    assert len(set(TOP_FROZEN)) == 14

    particles = {"فى", "ما", "لا", "ولا", "وما", "إلى", "ثم"}
    pronouns_and_deixis = {"به", "ذلك", "له", "ٱلذى", "هو"}
    past_verbs = {"قال", "كان"}
    assert particles | pronouns_and_deixis | past_verbs == set(TOP_FROZEN)
    assert len(particles) + len(pronouns_and_deixis) + len(past_verbs) == 14

    # والماضي مبنيٌّ على الفتح، فدخولُه ليس شذوذًا بل تصديق
    assert past_verbs <= set(TOP_FROZEN)


def test_the_frequent_types_are_few_so_the_top_band_is_clustered() -> None:
    """٢٠٢ نوعًا تحمل شريحةَ الخمسين؛ والمشاهداتُ أنواعٌ لا وقوعات."""

    band = next(one for one in BANDS if one[0] == "٥٠+")
    sample = ClusteredSample(observations=TOKENS, clusters=band[1])
    assert sample.effective == 202
    assert round(sample.inflation, 1) == 19.6

    frozen_in_band = round(band[1] * band[2] / 100)
    assert frozen_in_band == 84
    assert 0 < frozen_in_band < band[1]
    assert SOURCE_DIGEST[:8] == "46b4393f"
