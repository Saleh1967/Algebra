"""الطبقةُ الرابعة: **شبهُ الجملة إضافةٌ حقيقيّة، والعدُّ والنواسخُ يسقطان**.

**لا مرفقَ ورد** (المسارُ في حاويةٍ أخرى)، فالفحصُ على ما نُقِل في المتن.
والمادّةُ مبنيّةٌ باليد.

`THE_DANGLING_PAIR_IS_A_REAL_ADDITION`: وأحسنُ ما في الطبقة: **شبهُ الجملة
زوجٌ لا يُغلق** — له حاملُه الداخليُّ وحالتُه، وهو ككلٍّ **حالةٌ تبحث عن
حاملٍ أعلى**. والاسمُ «شبه» يصير مقروءًا لا اصطلاحًا. وكونُه **دَينًا
تركيبيًّا** بلا متعلَّقٍ وصلٌ صحيحٌ بمفهوم الدَّين الحاكم.

`BUT_FOUR_PLUS_FIVE_IS_NOT_THE_INVENTORY`: و«٤ + ٥ = ٩» **جردٌ ناقص**.
الفرعيّةُ عندهم خمس، والمقرَّرُ يزيد عليها **ثلاثًا**: **حذفُ حرف العلّة**
(لم يدعُ · لم يرمِ · لم يخشَ)، و**الكسرةُ نيابةً عن الفتحة** (رأيتُ
المسلماتِ)، و**الفتحةُ نيابةً عن الكسرة** (مررتُ بأحمدَ). فالمجموعُ
**اثنتا عشرة** لا تسعًا.

`AND_THE_TWO_SUBSTITUTIONS_BREAK_THE_FOUR_EQUALS_FOUR_AGAIN`: والأخيرتان
أشدُّ أثرًا من العدّ: **حركةٌ أصليّةٌ تعمل عملًا فرعيًّا**. فالأربعةُ ليست
مقسومةً بالوظيفة حتّى، ولا تقابلَ بين «أصليٍّ» و«فرعيّ» — وهو **نقضٌ ثانٍ**
لشاهد «٤ = ٤» من داخل الطبقة الرابعة نفسِها.

`AND_THE_CLOSURE_SURVIVES_WHILE_THE_NUMBER_FALLS`: ويبقى `Q3` صحيحًا:
الفضاءُ **منتهٍ** فالإفادةُ محدودة. فالعطلُ في العدد لا في الإغلاق — لكنّ
`F4` يجعل العددَ حاملًا، فيسقط ما حُمِّل عليه.

`DELTA_WITHOUT_ITS_LAYER_IS_EITHER_FALSE_OR_EMPTY`: و«العاملُ يغيّر الموضعَ
لا النسبة (Δ=0 بنائيّ)» **بلا تسمية طبقته**. ففي طبقة العوالم: «ظننتُ
زيدًا قائمًا» **لا تستبعد عوالمَ قيام زيدٍ ألبتّة** بل عوالمَ الظنّ؛ و«كاد
زيدٌ يقوم» إثباتُها **نفيُ الفعل**؛ و«كان» تُبدِّل الزمنَ فتُبدِّل العوالم.
فـ`Δ ≠ 0` في الأربع. وفي طبقة **الموضع** يصير `Δ = 0` تحصيلَ حاصل، إذ
النسبةُ ليست فيها أصلًا. فالدعوى **كاذبةٌ في طبقةٍ وتافهةٌ في أخرى** —
وهو عطلُ الوحدات في صورته الثالثة.

`AND_F9_CONTRADICTS_Q4_FROM_THE_EARLIER_LAYER`: و«زمنُ العلاقة ⟵ الجملةُ
الاسميّة»: والاسميّةُ تدلّ على **الثبوت** — أي أنّها **لم تحمل زمنًا قطّ**،
لا أنّها أسقطته. و`Q4` يفرّق بالضبط بين «إسقاطٍ معلن» و«عدم حملٍ أصلًا»،
ويجعل الجامدَ من الثاني. فوضعُ الاسميّة بيتًا **لزمنٍ ثالث** يضعها في
الصنف الذي نفاه `Q4` عن نظيرتها. فإمّا يُسمّى الثبوتُ **لا-زمنًا** فتبقى
الأزمنةُ بيتين، وإمّا يُنقَض `Q4`.
"""

from __future__ import annotations

import math

ORIGINAL_MARKERS = ("الضمّة", "الفتحة", "الكسرة", "السكون")
THEIR_BRANCH = ("الألف", "الواو", "الياء", "ثبوتُ النون", "حذفُ النون")
MISSING_BRANCH = (
    "حذفُ حرف العلّة",
    "الكسرةُ نيابةً عن الفتحة",
    "الفتحةُ نيابةً عن الكسرة",
)
WORLDS = frozenset(range(8))


def _delta(before: frozenset[int], after: frozenset[int]) -> float:
    return math.log2(len(before) / len(after))


def test_the_marker_inventory_is_twelve_not_nine() -> None:
    """أربعٌ أصليّةٌ وثمانٍ فرعيّة — والإغلاقُ يصمد والعددُ يسقط."""

    assert len(ORIGINAL_MARKERS) == 4
    assert len(THEIR_BRANCH) == 5
    assert len(MISSING_BRANCH) == 3
    whole = len(ORIGINAL_MARKERS) + len(THEIR_BRANCH) + len(MISSING_BRANCH)
    assert whole == 12 != 9
    assert whole < math.inf  # والإغلاقُ باقٍ: فضاءٌ منتهٍ


def test_two_of_the_missing_markers_are_original_marks_doing_branch_duty() -> None:
    """الكسرةُ عن الفتحة والفتحةُ عن الكسرة — فالأربعةُ غيرُ مقسومةٍ بالوظيفة."""

    substitutions = [one for one in MISSING_BRANCH if "نيابةً" in one]
    assert len(substitutions) == 2
    for one in substitutions:
        assert any(mark in one for mark in ORIGINAL_MARKERS)


def test_every_operator_moves_the_worlds_so_delta_is_not_zero_there() -> None:
    """ظنّ وكاد وكان: الباقي يتبدّل — فـ`Δ ≠ 0` في طبقة العوالم."""

    standing = frozenset({0, 2, 4, 6})
    readings = {
        "إنّ": standing,
        "كان": frozenset({0, 1}),
        "ظنّ": frozenset({1, 3, 5, 7}),
        "كاد": frozenset({2, 3}),
    }
    for name, after in readings.items():
        assert _delta(WORLDS, after) > 0, name
    # وظنَّ لا تشترك مع «زيدٌ قائم» في عالمٍ واحد — فليست النسبةَ نفسَها
    assert not (readings["ظنّ"] & standing)
    # وكاد تنفي الفعل، فتخرج عن عوالم القيام إلّا واحدًا
    assert len(readings["كاد"] & standing) < len(readings["كاد"])


def test_delta_is_zero_only_where_the_relation_is_not_measured() -> None:
    """في طبقة الموضع لا نسبةَ تُقاس — فصفرُها تحصيلُ حاصل."""

    positions_before = {"المبتدأ": "رفع", "الخبر": "رفع"}
    positions_after = {"اسمُ كان": "رفع", "خبرُ كان": "نصب"}
    assert positions_before != positions_after  # الموضعُ تبدّل
    relation_measured_here = False
    assert not relation_measured_here  # ولا نسبةَ في هذه الطبقة تُقاس


def test_the_nominal_sentence_belongs_to_the_class_q4_carved_out() -> None:
    """الثبوتُ **عدمُ حملٍ** لا إسقاطًا — فبيتُ الزمن الثالث ينقض Q4."""

    carries_time = {"الفعليّة": True, "الاسميّة": False, "المقام": True}
    declared_drop = {"المصدر": True}  # Δزمن > 0 مصرَّحٌ به
    never_carried = {"الجامد": True, "الاسميّة": True}
    assert not carries_time["الاسميّة"]
    assert "الاسميّة" in never_carried and "الاسميّة" not in declared_drop
    # فإمّا بيتان للزمن، وإمّا يُنقَض الفرقُ الذي أقامه Q4
    houses = [one for one, has in carries_time.items() if has]
    assert len(houses) == 2
