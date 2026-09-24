"""الخانةُ الثالثةُ والرابعةُ في `Bridge`: أربعةُ مواقفَ بدل ثنائيّةٍ كاذبة.

**ما يُقاس ههنا**: لا عربيّةَ ولا سُلَّم. تُفحَص **الآلة**؛ وأرقامُ الأمثلة
**مُصطنَعةٌ** ولا تُنقَل إلى شيء. وسُلَّمُ العربيّة في `test_arabic_ladder`.

`A_BINARY_STANDING_HAS_NO_CELL_FOR_A_TAUGHT_CROSSING`: كان `is_built` ثنائيًّا
— مبنيٌّ إن لم يكن له أوراكل — ولا خانةَ للحال الواقعة: **جسرٌ يحتاج الأوراكلَ
مرّةً ليُدرَّب، ثمّ يعبُر المحجوبَ بدونه بنسبةٍ مُعلَنة**. فليس مبنيًّا ولا
غيرَ مبنيّ. وإقحامُه في إحدى الخانتين يكذب في الاتّجاهين: يُعلَن ممهَّدًا وقد
احتاج معطًى، أو مقطوعًا وهو يعبُر فعلًا.

`A_REFUSAL_IS_A_RESULT_NOT_A_WAIT`: وأوراكلٌ **اختُبِر فسقط** ليس منتظِرًا.
والفرقُ عمليٌّ لا لفظيّ: المنتظِرُ يُطلَب، والساقطُ **انقضى طلبُه**، ومن عدَّه
مطلوبًا وعد بما لا يأتي.

`A_RATE_WITHOUT_A_NAMED_NULL_IS_NOT_A_RESULT`: والنسبةُ لا تدخل الخانةَ
الثالثةَ إلّا بثلاثةٍ معًا: مُعلِّمٌ يُسمّى، ومقامٌ صحيحٌ موجب، وصفريٌّ يُسمّى
أساسُه. فأيُّها سقط رُدَّ الإيداعُ عند الإنشاء لا عند القراءة.

`BUILT_IS_NOT_CROSSED`: و«مبنيّ» تعني «لا ينتظر معطًى»، لا «جرى عبورُه».
فجسرٌ بلا أوراكلَ ولا عبورٍ مسجَّلٍ مبنيٌّ **وفارغٌ** معًا، ويُفرَد عدُّه.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from algebra.bridge import (
    Bridge,
    BridgeError,
    BridgeStanding,
    Crossing,
    Ladder,
    Level,
    Taught,
    uniform_null,
)

# مستوياتٌ مُصطنَعةٌ لفحص الآلة وحدَها
A = Level("أ")
B = Level("ب")
C = Level("ج", ("س", "ص", "ع", "ق"))
D = Level("د")

TEACHING = Taught(
    teacher="جدولٌ مُصطنَعٌ دخل التدريبَ ولم يدخل المحجوب",
    held_out=200,
    matched=150,
    null=Fraction(1, 4),
    null_basis="انتظامٌ على جردٍ مغلقٍ من أربعة",
)


def test_the_four_standings_are_derived_not_written() -> None:
    """أربعةٌ، كلٌّ مُشتَقٌّ من مكوّناته: لا حقلَ اسمُه «الموقف» يُكتَب باليد."""

    built = Bridge("مبنيّ", A, B)
    awaiting = Bridge("منتظِر", A, B, oracle="معطًى مُسمًّى لم يُختبَر بعد")
    learned = Bridge("متعلَّم", B, C, oracle="معطًى مُسمًّى دُرِّب عليه", taught=TEACHING)
    refuted = Bridge("مردود", A, B, oracle="معطًى مُسمًّى اختُبِر", refuted_by="فحصٌ أسقطه")

    assert built.standing is BridgeStanding.BUILT
    assert awaiting.standing is BridgeStanding.AWAITING
    assert learned.standing is BridgeStanding.LEARNED
    assert refuted.standing is BridgeStanding.REFUTED
    assert len(BridgeStanding) == 4


def test_a_learned_bridge_is_neither_built_nor_unreachable() -> None:
    """المتعلَّمُ ليس مبنيًّا (احتاج معطًى) وليس مقطوعًا (يعبُر باحتمالٍ موجب)."""

    learned = Bridge("متعلَّم", B, C, oracle="معطًى دُرِّب عليه", taught=TEACHING)

    assert not learned.is_built  # لأنّه احتاج الأوراكلَ مرّةً
    assert learned.is_crossable  # ومع ذلك يعبُر
    assert learned.crossing_rate == Fraction(3, 4)
    assert TEACHING.rate == Fraction(3, 4)
    assert TEACHING.lift == 3  # ثلاثةُ أضعافِ صفريِّه


def test_a_rate_is_refused_without_a_teacher_a_denominator_and_a_named_null() -> None:
    """ثلاثةٌ معًا أو لا إيداع؛ وكلُّ نقصٍ يُرَدّ عند الإنشاء باسمه."""

    def taught(**changes: object) -> Taught:
        fields: dict[str, object] = {
            "teacher": "مُعلِّم",
            "held_out": 200,
            "matched": 150,
            "null": Fraction(1, 4),
            "null_basis": "أساسٌ مُسمًّى",
        }
        fields.update(changes)
        return Taught(**fields)  # type: ignore[arg-type]

    assert taught().rate == Fraction(3, 4)

    with pytest.raises(BridgeError, match="مُعلِّمَه"):
        taught(teacher="   ")
    with pytest.raises(BridgeError, match="مقام"):
        taught(held_out=0)
    with pytest.raises(BridgeError, match="أكثرُ ممّا حُجِب"):
        taught(matched=201)
    with pytest.raises(BridgeError, match="خارجَ الوحدة"):
        taught(null=Fraction(0))
    with pytest.raises(BridgeError, match="خارجَ الوحدة"):
        taught(null=Fraction(1))
    with pytest.raises(BridgeError, match="أساسُه"):
        taught(null_basis=" ")


def test_a_learned_bridge_still_names_the_oracle_it_used_once() -> None:
    """التدريبُ استعمالٌ يُسمّى؛ و«لم يدخل المحجوب» لا يمحو أنّه دخل مرّة."""

    with pytest.raises(BridgeError, match="متعلَّمٌ بلا أوراكل"):
        Bridge("متعلَّم", B, C, taught=TEACHING)

    with pytest.raises(BridgeError, match="متعلَّمٌ ومردودٌ معًا"):
        Bridge("كلاهما", B, C, oracle="معطًى", taught=TEACHING, refuted_by="فحص")

    with pytest.raises(BridgeError, match="مردودٌ بلا أوراكل"):
        Bridge("مردودٌ بلا أوراكل", A, B, refuted_by="فحص")


def test_a_verification_belongs_to_its_own_bridge_only() -> None:
    """شاهدُ عبورٍ باسمِ جسرٍ آخرَ يُرَدّ؛ فلا يُحتسَب عملُ غيرِه له."""

    own = Crossing(bridge="مبنيّ", given=10, mapped=10)
    assert Bridge("مبنيّ", A, B, verification=own).verification is own

    with pytest.raises(BridgeError, match="لا يُحتسَب لغيره"):
        Bridge("آخر", A, B, verification=own)


def test_built_but_never_crossed_is_counted_apart() -> None:
    """المبنيُّ الفارغُ يُعَدّ وحدَه؛ فتعريفٌ لا يصنع عبورًا."""

    ladder = Ladder(
        bridges=(
            Bridge("م١", A, B, verification=Crossing(bridge="م١", given=9, mapped=9)),
            Bridge("م٢", B, C),
        )
    )
    empty = [bridge.name for bridge in ladder.built_but_never_crossed()]
    assert empty == ["م٢"]
    assert len(ladder.built) == 2  # كلاهما مبنيّ…
    assert len(empty) == 1  # …وأحدُهما فارغ


def test_the_reach_profile_multiplies_and_stops_at_the_first_severed_bridge() -> None:
    """الاحتمالُ يتراكم بالضرب، ويقف السيرُ عند أوّل جسرٍ لا يُعبَر."""

    ladder = Ladder(
        bridges=(
            Bridge("م١", A, B),
            Bridge("م٢", B, C, oracle="دُرِّب عليه", taught=TEACHING),
            Bridge("م٣", C, D, oracle="لم يُختبَر"),
        )
    )
    profile = ladder.reach_profile()
    assert [level.name for level, _ in profile] == ["أ", "ب", "ج"]
    assert [rate for _, rate in profile] == [Fraction(1), Fraction(1), Fraction(3, 4)]

    # و«د» لا تُبلَغ ألبتّة، فلا تُطبَع باحتمالٍ صفريٍّ يُقرَأ بلوغًا ضعيفًا
    assert D.name not in [level.name for level, _ in profile]

    # والبلوغُ الثنائيُّ القديمُ باقٍ على معناه: بلا أيّ معطًى من خارج
    assert [level.name for level in ladder.reachable_levels()] == ["أ", "ب"]


def test_the_segments_carry_their_own_rates_and_name_what_cut_them() -> None:
    """قطعٌ متّصلةٌ، لكلٍّ احتمالُها ومن قطعها؛ وقاطعان متجاوران يصنعان قطعةً خالية."""

    ladder = Ladder(
        bridges=(
            Bridge("م١", A, B),
            Bridge("م٢", B, C, oracle="أ", refuted_by="فحصٌ أسقطه"),
            Bridge("م٣", C, D, oracle="ب"),
            Bridge("م٤", D, A, oracle="ج", taught=TEACHING),
        )
    )
    segments = ladder.segments()
    assert [one.severed_by for one in segments] == ["م٢", "م٣", None]
    assert [len(one.bridges) for one in segments] == [1, 0, 1]
    assert segments[1].is_empty
    assert segments[1].rate == Fraction(1)  # قطعةٌ خاليةٌ احتمالُها واحدٌ لا صفر
    assert segments[0].rate == Fraction(1)
    assert segments[2].rate == Fraction(3, 4)

    # والمطلوبُ ما لم يُختبَر وحدَه: «أ» سقط و«ج» دُرِّب عليه، فبقي «ب»
    assert ladder.oracles_required() == ("ب",)
    assert ladder.oracles_spent() == (("أ", "فحصٌ أسقطه"),)


def test_a_uniform_null_needs_a_closed_inventory() -> None:
    """الانتظامُ يُشتَقّ من جردٍ مغلقٍ وحدَه؛ ومستوًى مفتوحٌ يُرَدّ باسمه."""

    assert uniform_null(C) == Fraction(1, 4)
    assert C.size == 4

    for open_level in (A, B, D):
        with pytest.raises(BridgeError, match="مفتوحُ الجرد"):
            uniform_null(open_level)
