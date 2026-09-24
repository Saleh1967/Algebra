"""استطلاعا النثر مقروءَين: ت٢ تنجو بالمعاودة، وت٣ تسقط على مخطّط النثر نفسِه.

**ما ههنا**: أرقامٌ منقولةٌ عن تشغيلٍ جرى على نثرٍ حديثٍ لمؤلّفٍ واحد، لم
تُعَد في هذه الشجرة. ولا يُقاس عليها شيءٌ عن العربيّة؛ يُقاس **ما يلزم عنها**.

`THE_PAIRED_ESTIMATE_ANSWERS_THE_CLUSTER_OBJECTION_PROPERLY`: كان اعتراضي
«القسمةُ على جذر الحوافِّ للعقدة»، وهو **حدٌّ محافظٌ** لا تقدير. والمعاودةُ
المجمَّعةُ على الكلمات جوابُه الصحيح: فرقٌ مقترنٌ ٠٫١٣٤٢ بمجالٍ [٠٫١٢٢،
٠٫١٤٧]، ولا يقترب طرفُه الأدنى من الصفر. فت٢ **قائمةٌ بعد التصحيحين معًا**،
ولا يُذيبها التعالُق.

`THE_SAME_SURVEY_SINKS_THE_THIRD_FINDING_ON_ITS_OWN_GRAPH`: ومتوسّطُ الحوافِّ
للعقدة في مخطّط النثر **٣٫٨**. وقسمةُ ت٣ عليه: `3.7 ÷ √3.8 = 1.898` — **دون
١٫٩٦**. فليست ت٣ «هشّةً إن كثُفت مدوّنةٌ يومًا»: هي ساقطةٌ بقاعدة ش٢ على
المخطّط الذي خرجت منه. وت٢ بالقسمة نفسِها `19.6 ÷ √3.8 = 10.05` فتنجو خامًا
قبل المعاودة.

`A_MEDIAN_DEGREE_OF_ZERO_IS_THE_DENOMINATOR_NOBODY_NAMED`: ووسيطُ الدرجة
**صفر**. ومعناه أنّ نصفَ المفردات فأكثرَ **لا شاهدَ إحلالٍ لها ألبتّة**،
فلا تدخل ش١ ولا تخرج منها. فكلُّ رقمٍ في هذا الباب خبرٌ عمّن له جارٌ
مرصود، لا عن المعجم. وهذا مقامٌ ثالثٌ لم يُسمِّه أحدُنا، وقد صار يُطبَع مع
كلّ تشغيل.

`THE_CATCH_ALL_SHARE_IS_ALREADY_A_SEALED_CONDITION_NOT_A_DESCRIPTION`:
وتصويبٌ في التقسيم: «نصيبُ سواه» ليس مقامًا وصفيًّا — هو **ش٣** في الختم
بحدٍّ ٥٠٪ واتّجاه «لا يجاوز». فالوصفيُّ منهما عددُ العقد وحدَه، ومعه نصيبُ
ذوي الشاهد. والفرقُ ليس لفظيًّا: ما كان شرطًا يُسقِط، وما كان وصفًا يُقرَأ.
"""

from __future__ import annotations

import math
from fractions import Fraction

from algebra.reconciliation import rounds_to
from algebra.results import Vacancy

# منقولةٌ عن النثر: (المرصودُ المقترن، أدنى المجال، أعلاه، z)
PAIRED = (Fraction("0.1342"), Fraction("0.122"), Fraction("0.147"), 21.1)

# مخطّطُ الإطارات على النثر: وسيطٌ، و`p90`، ومتوسّطٌ، وأقصى
DEGREE_MEDIAN, DEGREE_P90, DEGREE_MEAN, DEGREE_MAX = 0, 8, 3.8, 341

RAW_Z = {"ت٢": 19.6, "ت٣": 3.7}
CONVENTIONAL = 1.96


def test_the_paired_interval_excludes_zero_and_contains_its_estimate() -> None:
    """٠٫١٣٤٢ داخلَ [٠٫١٢٢، ٠٫١٤٧]، وأدنى المجال بعيدٌ عن الصفر."""

    mean, low, high = PAIRED[0], PAIRED[1], PAIRED[2]
    assert low < mean < high
    assert low > 0
    assert rounds_to((high - low) * 1_000, 0) == 25  # اتّساعُ المجال ٠٫٠٢٥


def test_the_mean_degree_sinks_the_third_finding_under_the_sealed_rule() -> None:
    """٣٫٧ ÷ √٣٫٨ = ١٫٨٩٨ — دون ١٫٩٦، فت٣ ساقطةٌ على مخطّطها هي."""

    divided = {name: z / math.sqrt(DEGREE_MEAN) for name, z in RAW_Z.items()}
    assert round(divided["ت٣"], 3) == 1.898
    assert divided["ت٣"] < CONVENTIONAL

    assert round(divided["ت٢"], 2) == 10.05
    assert divided["ت٢"] > CONVENTIONAL

    # وحدُّ التعادل الذي حُسِب قبل الاستطلاع كان ٣٫٥٦، والمتوسّطُ جاء فوقه
    assert (RAW_Z["ت٣"] / CONVENTIONAL) ** 2 < DEGREE_MEAN


def test_a_zero_median_means_half_the_vocabulary_never_enters_the_reading() -> None:
    """وسيطُ الدرجة صفرٌ: نصفُ المفردات بلا شاهدِ إحلال، فهي خارج المقام."""

    assert DEGREE_MEDIAN == 0
    assert DEGREE_MEAN > DEGREE_P90 / 4  # ذيلٌ ثقيلٌ لا توزيعٌ متماثل
    assert DEGREE_MAX > DEGREE_P90 * 40

    # ومنزلةُ هؤلاء ليست «لا جوار لهم» بل «لم يُبلَغوا بما في اليد»
    assert Vacancy.UNREACHABLE.value == "لا تُبلَغ بما في اليد"
    assert Vacancy.UNREACHABLE is not Vacancy.UNATTESTED


def test_the_catch_all_share_is_a_condition_not_a_description() -> None:
    """«سواه» ش٣ بحدٍّ ٥٠٪، والوصفيُّ عددُ العقد ونصيبُ ذوي الشاهد."""

    sealed = {"ش٣ نصيبُ «سواه»"}
    described = {"عددُ العقد", "نصيبُ العقد التي لها شاهدُ إحلال"}
    assert not (sealed & described)

    # وما كان شرطًا يُسقِط، وما كان وصفًا يُقرَأ — والخلطُ بينهما بابٌ بعديّ
    assert len(sealed) == 1 and len(described) == 2


def test_the_road_after_the_five_is_ordered_with_its_material_named() -> None:
    """ثلاثةُ أبوابٍ بالترتيب، ولكلٍّ منزلةُ مادّته — ولا بابَ بلا مادّةٍ مُسمّاة."""

    road = (
        ("النظمُ المعنويُّ بالفرق", "يتبع تشغيلَ الشاهد نفسِه"),
        ("أوسمةُ اللسان معلَّقةً", "روايةٌ عن مدوّنة استعمال، بالعزل المفحوص"),
        ("إعرابُ H(الحركة الأخيرة | اللفظ، الدور)", "محاذاةٌ مشكولةٌ لم تُودَع ههنا"),
    )
    assert len(road) == 3
    assert len({name for name, _ in road}) == 3

    # والثالثُ وحدَه مشروطٌ بمادّةٍ غيرِ موجودةٍ في هذه الشجرة، وذلك يُقال لا يُطوى
    needs_material = [name for name, note in road if "لم تُودَع" in note]
    assert needs_material == ["إعرابُ H(الحركة الأخيرة | اللفظ، الدور)"]
