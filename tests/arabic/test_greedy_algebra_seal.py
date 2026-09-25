"""**ختمٌ قبل النظر**: لماذا ينقلب الربح؟ — بالتوافيق والتباديل، وماركوف.

**لم يُشغَّل شيءٌ على المدوّنة بعد.** والآلةُ جُرّبت على شريحةٍ من ثمانين
سطرًا، وجاء فيها `ρ(الوقوع، الربح) = +٠٫٤٥٥` و`ρ(المشتَقّ، الربح) = +٠٫٩٨٥`
و`|I − Σ p·PMI| = ٠` وتوافقُ العتبة `٠٫٩٠`؛ **ويُعلَن ذلك ههنا** فما رأيتُه
قبل الختم لا يُخفى. **ولا يُستخرَج من شريحةٍ بهذا الصغر شيءٌ عن أرقام
المدوّنة** — ولا سيّما `I`، فهي مقدارُ مادّةٍ لا مقدارُ آلة.

**الاشتقاق المعروض للسقوط**: تكلفةُ البيان لنموذجٍ بلا سياقٍ هي **لوغاريتم
عدد التباديل المتمايزة** لمتعدّد المجموعة، `log₂ N!/∏nₛ!`. فربحُ دمج
`(a,b) ⟶ f` بـ`m` استبدالًا نسبةُ معاملين، وهي **بالتباديل النازلة**:

    G = log₂ N⁽ᵐ⁾ − log₂ nₐ⁽ᵐ⁾ − log₂ n_b⁽ᵐ⁾ + log₂ m!

وبالتقريب الأوّل `G ≈ m·(PMI − log₂ e)` حيث `PMI = log₂(m·N / nₐ·n_b)`.

**فالدعوى**: الربحُ ليس `m`، بل `m` مضروبًا في **فائض الاقتران على
الاستقلال** ناقصًا `log₂ e ≈ ١٫٤٤٢٧`. ومن ثَمَّ **ينقلب الترتيب**: زوجٌ
طرفاه كثيرا الوقوع يلتقيان بالمصادفة فـ`PMI` صغيرة ولو عظُم `m`.

**وماركوف**: `Σ p(a,b)·PMI(a,b) = I(Xₜ₊₁) − H(Xₜ₊₁|Xₜ) = I(Xₜ;Xₜ₊₁)`
هويّةً. فالمستخرَجُ بالدمج هو **بعينه** اقترانُ الجارين.

**والاستقراءان**: `induction on` — المتراجحةُ `log₂ التباديل ≤ N·H` تُصان
عند كلّ حال؛ و`induction FOR` — الحلقةُ تشهد عليها عددًا عددًا، وتُقابَل
العدّاداتُ بالآيات عند كلّ نقطةٍ فلا تنفرد آلةٌ برقم.

**ولا اسمَ لغويٌّ يدخل**: بتّاتٌ ووقوعاتٌ وتكلفةٌ فقط.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, seal

SAVED = 824_618

ORACLE = Oracle(
    name="جبرُ الربح الجشع فوق ١١٢ — بالتباديل واقترانِ الجارين",
    source="quran-simple-enhanced.txt — البصمة 37633090…",
    extraction=(
        "على L₀ من المُجمَّد: تُحسَب لأكثرِ مئتَي زوجٍ وقوعًا `m` و`PMI` "
        "والربحُ المشتَقُّ بالتباديل النازلة، ويُقابَل بالربح **المقيس** "
        "من تغيّر طول شفرة هوفمان داخلَ العيّنة؛ وتُحسَب "
        "`I(Xₜ;Xₜ₊₁)` و`Σ p·PMI` على مواضع الجوار، ويُقابَل ما وفّره "
        "الصعودُ الكتليُّ (٨٢٤٬٦١٨ بتًّا) بسقفِ الرتبة الأولى"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="ب١",
        statistic="|I(Xₜ;Xₜ₊₁) − Σ p·PMI| على مواضع الجوار (بتًّا للموضع)",
        threshold=Fraction(1, 10**9),
        direction=Direction.AT_MOST,
        falsifies=(
            "الهويّةَ لا المادّة: `Σ p·PMI` هي `I` بالتعريف، فاختلافُهما "
            "عطلُ آلةٍ — أو خلطُ الهامش الأيسر بالأيمن — يردّ الباب كلَّه"
        ),
    ),
    Prediction(
        identifier="ب٢",
        statistic="أدنى (N·H − log₂ التباديل) على نقاط الفحص (بتًّا)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies=(
            "متراجحةً مبرهَنة: عددُ التباديل المتمايزة لا يجاوز `2^(N·H)`، "
            "فنزولُ الفرق تحت الصفر عطلُ حسابٍ لا اكتشاف"
        ),
    ),
    Prediction(
        identifier="ب٣",
        statistic="ρ(الوقوعِ الخام، الربحِ المقيس) على المئتَي زوج",
        threshold=Fraction(1, 2),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوى أنّ العددَ الخامَ ليس وكيلًا عن الربح — وهي تفسيرُ "
            "الانقلاب. فإن ارتفع الارتباطُ فوق النصف فالعددُ وكيلٌ صالح، "
            "ويبقى انقلابُ `c8602c00…` بلا تفسير"
        ),
    ),
    Prediction(
        identifier="ب٤",
        statistic="ρ(الربحِ المشتَقِّ بالتباديل، الربحِ المقيس) على المئتَي زوج",
        threshold=Fraction(9, 10),
        direction=Direction.AT_LEAST,
        falsifies=(
            "الاشتقاقَ نفسَه: إن لم يتبع المشتَقُّ المقيسَ فالصيغةُ "
            "بالتباديل ليست تكلفةَ هذا البناء، ويسقط الباب ولا يُرقَّع"
        ),
    ),
    Prediction(
        identifier="ب٥",
        statistic="ρ(PMI، الربحِ المقيس) − ρ(الوقوعِ الخام، الربحِ المقيس)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ فائضَ الاقتران أقربُ إلى الربح من العدد الخام؛ فإن كان "
            "العددُ أقربَ فالتفسيرُ معكوسٌ ويُنشَر معكوسًا"
        ),
    ),
    Prediction(
        identifier="ب٦",
        statistic="نسبةُ الأزواج التي توافق فيها عتبةُ PMI > log₂e إشارةَ الربح",
        threshold=Fraction(8, 10),
        direction=Direction.AT_LEAST,
        falsifies=(
            "العتبةَ المشتقّة: `log₂ e` ليست حدًّا مضبوطًا للترخيص، فالحكمُ "
            "يحتاج المعجمَ والحدودَ الأعلى رتبةً، ويُقال إنّها تقريبٌ لا حدّ"
        ),
    ),
    Prediction(
        identifier="ب٧",
        statistic="وسيطُ |المشتَقّ − المقيس| ÷ |المقيس| على ما ربحُه ≥ ١ بتًّا",
        threshold=Fraction(1, 4),
        direction=Direction.AT_MOST,
        falsifies=(
            "دقّةَ الاشتقاق مقدارًا لا ترتيبًا فحسب؛ فإن جاوز الخطأُ الربعَ "
            "فالصيغةُ ترتّب ولا تُقدّر، ويُقال ذلك ولا يُدَّعى أكثرُ منه"
        ),
    ),
    Prediction(
        identifier="ب٨",
        statistic="ما وفّره الصعودُ الكتليُّ ÷ سقفِ الرتبة الأولى",
        threshold=Fraction(1),
        direction=Direction.AT_MOST,
        falsifies=(
            "أنّ الدمجَ المتكرّرَ يسعه اقترانُ الجارين وحدَه. فإن جاوزت "
            "النسبةُ الواحدَ فالصعودُ **يبلغ ما فوق الرتبة الأولى** — لأنّ "
            "الرموزَ المدموجةَ تمتدّ فيلتقط جوارُها رتبًا أبعد — وذلك خبرٌ "
            "لا عطل، ويُنشَر باسمه"
        ),
    ),
)

DIGEST = "cfdb2184f5b4c81bbe2364f28d8e8cc411d5fff667b3b9b52cd9141ea97e9f75"
"""يُثبَّت بعد أوّل اشتقاق، ولا يُمَسّ بعدَه."""


def test_the_seal_is_recomputed_from_the_written_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_two_conditions_are_identities_not_claims_of_mine() -> None:
    """ب١ هويّةٌ وب٢ متراجحةٌ مبرهَنة — وسقوطُهما عطلُ حساب."""

    same = next(one for one in PREDICTIONS if one.identifier == "ب١")
    below = next(one for one in PREDICTIONS if one.identifier == "ب٢")
    assert same.threshold <= Fraction(1, 10**9)
    assert below.threshold == Fraction(0)
    assert "عطلُ آلةٍ" in same.falsifies and "عطلُ حسابٍ" in below.falsifies


def test_the_explanation_is_staked_on_two_opposite_correlations() -> None:
    """ب٣ يطلب ضعفَ العدد، وب٤ يطلب قوّةَ المشتَقّ — ولا يصمدان معًا صدفةً."""

    weak = next(one for one in PREDICTIONS if one.identifier == "ب٣")
    strong = next(one for one in PREDICTIONS if one.identifier == "ب٤")
    assert weak.direction is Direction.AT_MOST
    assert strong.direction is Direction.AT_LEAST
    assert weak.threshold < strong.threshold
    assert len(PREDICTIONS) == 8


def test_the_markov_ceiling_reads_either_way_and_says_so() -> None:
    """ب٨ خبرٌ في الحالين — ومكتوبٌ ما يعنيه تجاوزُه."""

    roof = next(one for one in PREDICTIONS if one.identifier == "ب٨")
    assert roof.threshold == Fraction(1)
    assert "ما فوق الرتبة الأولى" in roof.falsifies
    assert "خبرٌ" in roof.falsifies and "لا عطل" in roof.falsifies
    assert str(SAVED) == "824618"


def test_the_slice_i_saw_before_sealing_is_declared() -> None:
    """ما رأيتُه قبل الختم مكتوبٌ فيه — ولا يُخفى بعد النظر."""

    assert __doc__ is not None
    for one in ("+٠٫٤٥٥", "+٠٫٩٨٥", "٠٫٩٠", "ثمانين"):
        assert one in __doc__, one
