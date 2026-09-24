"""المُمتحِنُ منحازٌ بالتعريف: جدولُ الوزن الذي ينقل دقّتَه إلى المدوَّنة.

**موقعي**: لا أملك كتابَ الغريب ولا مخرَجَ النظام، فلا أُقوّم امتحانًا لم
يجرِ بعد. وأفعل شيئين: أُعيد حسابَ أرقام التقرير، وأبني **الوزنَ** الذي
قيل عنه «ولا تُنقَل إلى الكلّ بغير وزن» — فالوزنُ يُحسَب من الرقمين
المنشورين وحدَهما، ويُكتَب **قبل** أوّل قياس.

`THE_WEIGHT_IS_COMPUTABLE_FROM_TWO_PUBLISHED_NUMBERS`: نصيبُ اللِّمَم
النادرة ٣٩٫٩٪ في المُمتحِن و٨٫٩٪ في المدوَّنة. فوزنُ النطاق النادر
٨٫٩ ÷ ٣٩٫٩ = **٠٫٢٢٣**، ووزنُ الشائع ٩١٫١ ÷ ٦٠٫١ = **١٫٥١٦** — نسبةٌ
**٦٫٨٠×**. فالنادرُ يُخفَّض إلى نحوِ خُمسه، والشائعُ يُرفَع مرّةً ونصفًا.

`THE_HEADLINE_AND_THE_PROJECTION_DIFFER_BY_A_FIXED_FACTOR`: الفرقُ بين
الدقّة المُعلَنة على المُمتحِن والدقّة المُسقَطة على المدوَّنة يساوي
**٠٫٣١٠ × (أ_نادر − أ_شائع)** لا غير. فلو كان النادرُ أصعبَ بعشرين نقطة،
لكان المُعلَنُ **يُنقِص** المدوَّنةَ ٦٫٢ نقطة. والصيغةُ تُكتَب الآن فلا
يُختار اتّجاهُها بعد رؤية الرقم.

`ONE_THRESHOLD_THREE_NUMBERS_DEPENDING_ON_WHAT_IS_COUNTED`: «النادرُ ≤٥»
يعطي **٩٠٫٤٧٪** من أنواع السطح، و**٣٣٫٨١٪** من وقوعاته، و**٨٫٩٪** من
اللِّمَم. حدٌّ واحدٌ وثلاثةُ أرقام. وقد قارنتُ أوّلًا ٣٣٫٨١ بـ٣٩٫٩ فحسبتُ
وزنًا بوحدتين — **وذلك غلطٌ أُصلِح قبل نشره**، وهو عاشرُ موضعٍ من هذا الجنس.

`THE_SEPARATING_TEST_IS_AN_ABLATION_NOT_A_NUMBER`: الاحتمالان — «تمثيلُ
السياق خاطئ» و«المعنى مدخولٌ من خارج» — **لا يفترقان برقمِ دقّةٍ واحد**.
فدقّةٌ منخفضةٌ تُفسَّر بكليهما. والذي يفصلهما **منحنى**: تُشغَّل تمثيلاتٌ
للسياق متدرّجةٌ في الغنى، ويُنظَر أترتفع الدقّةُ معها أم تستوي. ارتفاعٌ
يرجّح الأوّل، واستواءٌ يرجّح الثاني. وكلُّ نقطةٍ في المنحنى تُقاس **داخل
النطاق** لا على الخليط، وإلّا خلط الانحيازُ الأثرَ بالعيّنة.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.reconciliation import Partition, rounds_to
from algebra.selection import Locus, partition_of_loci

# أرقامُ التقرير
VERSES_WITH_ENTRY, VERSES_TOTAL = 5_069, 6_236
ANCHORED_GLOSSES = 11_362
SINGLE_WORD = 6_689
ALIGNED, UNALIGNED = 6_574, 115
DISTINCT_TOKENS, DISTINCT_LEMMAS = 6_572, 2_739
MUSHAF_TOKENS = 77_428

# الانحيازُ كما قِيس، باللِّمّة في الطرفين
EXAMINER_RARE = Fraction("0.399")
CORPUS_RARE = Fraction("0.089")
EXAMINER_MEDIAN, CORPUS_MEDIAN = 9, 178

# وبوحدةِ السطح من ركيزتي — للمقارنة لا للوزن
SURFACE_RARE_TYPES = Fraction("0.9047")
SURFACE_RARE_TOKENS = Fraction("0.3381")


def test_the_report_recomputes_on_every_figure_it_publishes() -> None:
    """٦٬٥٧٤ + ١١٥ = ٦٬٦٨٩، والنسبةُ ٩٨٫٢٨٪ — وخمسةُ أرقامٍ أُخَر تُعاد."""

    assert (
        Partition(parts=(ALIGNED, UNALIGNED), declared_total=SINGLE_WORD).residue == 0
    )
    assert rounds_to(Fraction(ALIGNED, SINGLE_WORD) * 100, 2) == Fraction("98.28")
    assert rounds_to(Fraction(SINGLE_WORD, ANCHORED_GLOSSES) * 100, 1) == Fraction(
        "58.9"
    )
    assert rounds_to(Fraction(VERSES_WITH_ENTRY, VERSES_TOTAL) * 100, 1) == Fraction(
        "81.3"
    )
    assert rounds_to(Fraction(ALIGNED, MUSHAF_TOKENS) * 100, 2) == Fraction("8.49")
    assert DISTINCT_TOKENS < ALIGNED  # رمزان مكرَّران
    assert DISTINCT_LEMMAS < DISTINCT_TOKENS


def test_the_reweighting_factors_follow_from_two_published_numbers() -> None:
    """٠٫٢٢٣ للنادر و١٫٥١٦ للشائع — نسبةٌ ٦٫٨٠×، محسوبةٌ لا مقدَّرة."""

    rare_weight = CORPUS_RARE / EXAMINER_RARE
    common_weight = (1 - CORPUS_RARE) / (1 - EXAMINER_RARE)

    assert rounds_to(rare_weight, 3) == Fraction("0.223")
    assert rounds_to(common_weight, 3) == Fraction("1.516")
    assert rounds_to(common_weight / rare_weight, 2) == Fraction("6.80")
    assert rare_weight < 1 < common_weight


def test_the_projection_gap_is_a_fixed_multiple_of_the_band_difference() -> None:
    """الفرقُ = ٠٫٣١٠ × (أ_نادر − أ_شائع) — والصيغةُ تُكتَب قبل الرقم."""

    tilt = EXAMINER_RARE - CORPUS_RARE
    assert rounds_to(tilt, 3) == Fraction("0.310")

    for band_gap, expected in ((10, "3.10"), (20, "6.20"), (30, "9.30")):
        assert rounds_to(tilt * band_gap, 2) == Fraction(expected)

    # والاتّجاهُ يتبع إشارةَ الفرق، ولا يُختار بعد النظر
    harder = -20  # النادرُ أصعبُ بعشرين نقطة
    assert tilt * harder < 0  # فالمُعلَنُ يُنقِص المدوَّنة


def test_one_threshold_gives_three_numbers_by_unit() -> None:
    """«النادرُ ≤٥» = ٩٠٫٤٧٪ أنواعًا · ٣٣٫٨١٪ وقوعاتٍ · ٨٫٩٪ لِمَمًا.

    وقد قارنتُ أوّلًا ٣٣٫٨١ بـ٣٩٫٩ — وحدتان لا واحدة — فحسبتُ وزنًا كاذبًا
    (٠٫٨٤٧ بدل ٠٫٢٢٣). وأُصلِح قبل النشر، ويُسجَّل لأنّ السجلَّ جزءٌ من العمل.
    """

    readings = (SURFACE_RARE_TYPES, SURFACE_RARE_TOKENS, CORPUS_RARE)
    assert len(set(readings)) == 3
    assert max(readings) / min(readings) > 10

    wrong = SURFACE_RARE_TOKENS / EXAMINER_RARE
    right = CORPUS_RARE / EXAMINER_RARE
    assert rounds_to(wrong, 3) == Fraction("0.847")
    assert rounds_to(right, 3) == Fraction("0.223")
    assert wrong > right * 3  # والغلطُ كان يُخفي ثلاثةَ أرباع الانحياز


def test_the_median_ratio_agrees_with_the_share_in_direction() -> None:
    """وسيطُ المُمتحِن ٩ ووسيطُ المدوَّنة ١٧٨ — عشرون ضعفًا، والاتّجاه واحد."""

    assert CORPUS_MEDIAN > EXAMINER_MEDIAN * 19
    assert EXAMINER_RARE > CORPUS_RARE * 4
    # مقياسان مستقلّان للانحياز نفسِه، ويتّفقان في الاتّجاه لا في المقدار


def test_the_two_hypotheses_need_a_curve_not_a_single_accuracy() -> None:
    """«تمثيلٌ خاطئ» و«معنًى من خارج» لا يفترقان برقمٍ واحد، بل بميلٍ.

    فكلُّ رقمِ دقّةٍ منخفضٍ يُفسَّر بكليهما، والقسمةُ بلا فحصٍ فاصلٍ ليست
    قسمة. والفحصُ: تمثيلاتٌ متدرّجةٌ في الغنى، ويُنظَر أترتفع الدقّةُ معها.
    """

    loci = partition_of_loci(
        (
            Locus(
                name="تمثيلُ السياق خاطئ",
                settled=False,
                deciding_test=(
                    "تُشغَّل ثلاثةُ تمثيلاتٍ متدرّجةٍ في الغنى وتُقاس الدقّةُ "
                    "بكلٍّ داخلَ النطاق؛ فميلٌ موجبٌ معنويٌّ يرجّحه"
                ),
            ),
            Locus(
                name="المعنى مدخولٌ من خارج",
                settled=False,
                deciding_test=(
                    "الميلُ نفسُه: استواءٌ عبر التمثيلات الثلاثة مع بقاء الدقّة "
                    "دون سقفِ المعجم يرجّحه"
                ),
            ),
        )
    )
    assert len(loci) == 2
    assert all(not one.settled for one in loci)
    assert all(" أو " not in one.name for one in loci)
    assert len({one.deciding_test for one in loci}) == 2


def test_the_examiner_covers_less_than_a_tenth_of_the_corpus() -> None:
    """٦٬٥٧٤ من ٧٧٬٤٢٨ = ٨٫٤٩٪ — والتغطيةُ ليست قبولًا، كما قيل في ت١."""

    coverage = Fraction(ALIGNED, MUSHAF_TOKENS)
    assert coverage < Fraction(1, 10)
    assert rounds_to(coverage * 100, 2) == Fraction("8.49")

    # ولا يُقاس على ٩١٫٥١٪ الباقية شيءٌ من هذا الامتحان
    assert 1 - coverage > Fraction(9, 10)
