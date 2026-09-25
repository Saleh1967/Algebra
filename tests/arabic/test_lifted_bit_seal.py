"""**ختمٌ قبل النظر**: أثرُ **بتّةٍ واحدة** معزولًا — وهو ما بقي غيرَ معزول.

**لم يُشغَّل شيءٌ على المدوّنة بعد.** والآلةُ جُرّبت على شريحةٍ من ثمانين
سطرًا، وجاء فيها **الفرقُ +٤٧٦ بتًّا** والنسبةُ **٠٫٠١٦٦** والالتزاماتُ
**−١٦**؛ **ويُعلَن ذلك ههنا** فما رأيتُه قبل الختم لا يُخفى. **ولا يُستخرَج
من شريحةٍ بهذا الصغر شيءٌ عن أرقام المدوّنة** — ولا سيّما النسبةُ، فأثرُ
بتّةٍ واحدةٍ في ٥٬٥٤٥ وحدةً غيرُ أثرِها في ٣٦٤٬٧٤٧.

**ما يُعزَل**: كُتِب في `docs/الترخيص-بتّةً-بتّة.md` أنّ نسبةَ الفرق إلى
**دمجةٍ بعينها** استنتاجٌ لا قياس، وأنّها تُوسَم كذلك **حتّى تُعزَل**.

**والبتّةُ تُختار بالآلة لا باليد**: هي المُلتزَمةُ في **أوّل حالٍ يختلف
فيه** «أكبرُ ربحًا» عن «أوّلِ رابح» — أي **أوّلُ بتّةٍ صعدت بسبب الانقلاب
نفسِه**. فليست بتّةً تُنتقى بعد النظر، ولا يملك مُشغِّلُها اختيارَها.

**وذراعان لا يفترقان إلّا فيها**: الأوّلُ كما في `c8602c00…` بلا تبديل،
والثاني كهو إلّا أنّ تلك البتّةَ **ممنوعةٌ من الاقتراح طولَ التشغيل**.
فالفرقُ بينهما **أثرُها**، لا أثرُ قاعدةٍ ولا عمقٍ ولا وسم.

**وشرطُ إعادة الإنتاج أوّلُ الشروط**: إن لم يُعِد الذراعُ الأوّلُ رقمَ
`c8602c00…` بتًّا بتًّا فالمقابلةُ مردودةٌ كلُّها.

**ولا اسمَ لغويٌّ يدخل**: بتّاتٌ ووقوعاتٌ وتكلفةٌ فقط.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, seal

BY_RANKING = 1_472_223
RANKING_COMMITS = 1_530

ORACLE = Oracle(
    name="أثرُ بتّةٍ واحدةٍ معزولًا فوق ١١٢",
    source="quran-simple-enhanced.txt — البصمة 37633090…",
    extraction=(
        "آلةُ `c8602c00…` بعينها في ذراعين: الأوّلُ بلا تبديل، والثاني "
        "وقد مُنِعت من الاقتراح **بتّةٌ واحدة** هي المُلتزَمةُ في أوّل "
        "حالٍ يختلف فيه «أكبرُ ربحًا» عن «أوّلِ رابح»؛ وتُطبَع البتّةُ "
        "بوقوعاتها وطرفيها ببايتاتهما و`PMI` والربحِ المشتَقِّ بالتباديل "
        "والربحِ المقيس ورتبتِها الخام"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="ن١",
        statistic="|جملةُ الذراع الأوّل − جملةِ تشغيل `c8602c00…`| (بتًّا)",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "إعادةَ الإنتاج: الذراعُ الأوّلُ هو `c8602c00…` بقاعدته وعمقه، "
            "فاختلافُ بتٍّ واحدٍ عطلُ آلةٍ يردّ المقابلةَ كلَّها"
        ),
    ),
    Prediction(
        identifier="ن٢",
        statistic="أكبرُ عددِ مواضعِ الخلاف بين بسطِ الرموز ومجرى L₀ في الذراعين",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies="الرجعةَ: أيُّ خلافٍ في أيّ ذراعٍ ضياعٌ لا ضغط",
    ),
    Prediction(
        identifier="ن٣",
        statistic="مجموعُ الالتزامات التي لم تنزل عندها التكلفةُ في الذراعين",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies="أنّ الرخصةَ بقيت للدمجة الواحدة في الذراعين جميعًا",
    ),
    Prediction(
        identifier="ن٤",
        statistic="PMI للبتّة المرفوعة − log₂ e (بتًّا للوقوع)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies=(
            "العتبةَ المشتقّةَ في `cfdb2184…`: بتّةٌ التُزِمت لأنّها أربحُ "
            "ما في النافذة، فإن كانت `PMI` دون `log₂ e` فالعتبةُ لا تصف "
            "الملتزَمَ الفعليَّ بل أكثريّتَه فحسب"
        ),
    ),
    Prediction(
        identifier="ن٥",
        statistic="|جملةُ الذراع الثاني − جملةِ الأوّل| (بتًّا)",
        threshold=Fraction(1),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ لبتّةٍ واحدةٍ أثرًا أصلًا: فإن تطابق الذراعان فالجشعُ "
            "**يلتفّ** على منعها ويبلغ ما كان يبلغه، ويكون كلُّ حديثٍ عن "
            "أثرِ دمجةٍ بعينها لاغيًا — وذلك خبرٌ يُنشَر"
        ),
    ),
    Prediction(
        identifier="ن٦",
        statistic="جملةُ الذراع الثاني − جملةِ الأوّل (بتًّا)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ رفعَ بتّةٍ التزمها الجشعُ لا ينفع؛ فإن نزلت الجملةُ برفعها "
            "فالبتّةُ **كانت ضارّةً وقد التُزِمت**، ويكون الجشعُ يلتزم ما "
            "يضرّه — وهو أقوى ممّا ادّعيت على الجشع"
        ),
    ),
    Prediction(
        identifier="ن٧",
        statistic="|فرقُ الذراعين| ÷ جملةِ الذراع الأوّل",
        threshold=Fraction(1, 100),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوى أنّ أثرَ البتّة الواحدة صغيرٌ في الجملة؛ فإن جاوز المئينَ "
            "فبتّةٌ واحدةٌ تحمل من الفرق ما لا يُهمَل، ويُعاد النظرُ في "
            "نسبة الفروق إلى القواعد دون الأفراد"
        ),
    ),
)

DIGEST = "0c070831149aa9aaf608f6631a698c813f86d3e0194c7c951f61650cbfdbd15a"
"""يُثبَّت بعد أوّل اشتقاق، ولا يُمَسّ بعدَه."""


def test_the_seal_is_recomputed_from_the_written_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_the_bit_is_chosen_by_the_machine_not_by_the_operator() -> None:
    """أوّلُ حالٍ يختلف فيه الحكمان — ولا يملك مُشغِّلٌ اختيارَها."""

    assert "أوّل حالٍ يختلف فيه" in ORACLE.extraction
    assert __doc__ is not None
    assert "لا يملك مُشغِّلُها اختيارَها" in __doc__
    assert len(PREDICTIONS) == 7


def test_the_two_arms_differ_in_one_bit_and_nothing_else() -> None:
    """القاعدةُ والعمقُ والوسمُ من `c8602c00…` — والبتّةُ وحدَها تُرفَع."""

    assert "آلةُ `c8602c00…` بعينها في ذراعين" in ORACLE.extraction
    assert "**بتّةٌ واحدة**" in ORACLE.extraction
    same = next(one for one in PREDICTIONS if one.identifier == "ن١")
    assert same.threshold == Fraction(0)
    assert "إعادةَ الإنتاج" in same.falsifies


def test_three_conditions_read_one_difference_three_ways() -> None:
    """ن٥ وجودُه، ون٦ إشارتُه، ون٧ قدرُه — ولا يُغني أحدُها عن الآخر."""

    there = next(one for one in PREDICTIONS if one.identifier == "ن٥")
    sign = next(one for one in PREDICTIONS if one.identifier == "ن٦")
    size = next(one for one in PREDICTIONS if one.identifier == "ن٧")
    assert there.direction is Direction.AT_LEAST and there.threshold == Fraction(1)
    assert sign.direction is Direction.AT_LEAST and sign.threshold == Fraction(0)
    assert size.direction is Direction.AT_MOST and size.threshold == Fraction(1, 100)


def test_the_slice_i_saw_before_sealing_is_declared() -> None:
    """ما رأيتُه قبل الختم مكتوبٌ فيه — ولا يُخفى بعد النظر."""

    assert __doc__ is not None
    for one in ("+٤٧٦", "٠٫٠١٦٦", "−١٦", "ثمانين"):
        assert one in __doc__, one
