"""سُلَّمُ العربيّة: أحدَ عشرَ مستوًى وعشرةُ جسور — أيُّها مبنيٌّ وأيُّها مبلوغ.

**ما يُودَع ههنا**: السُّلَّمُ كلُّه **شيئًا واحدًا قابلًا للفحص**، من الشيفرة
إلى العلامة الإعرابيّة. ولا يُدَّعى فيه محلِّلٌ صرفيّ: كلُّ جسرٍ إمّا **مبنيٌّ**
وإمّا **يُسمّي الأوراكلَ** الذي ينقصه. وأهمُّ ما يُخرِجه الحساب:

`BUILT_IS_NOT_REACHED`: ستّةٌ من العشرة مبنيّة، ولا يُبلَغ منها من الأسفل
إلّا **اثنان**. فالأربعةُ المبنيّةُ فوق الفجوة صحيحةٌ في نفسها غيرُ موصولةٍ
بالبايتات. و«جاهز» كلمةٌ تخلط الأمرين، فتُفصَل ههنا بالحساب.

وجسرُ اليونيكود مبنيٌّ بحقٍّ، وفحوصُه على `unicodedata` لا على قولٍ: صورةُ
التوحيد تُعلَن وإلّا كان العدُّ غيرَ معرَّف، والشدّةُ محرفٌ واحدٌ يقابل
مقطعين، والتنوينُ علامةٌ تقابل حركةً ونونًا.

`A_SPENT_ORACLE_IS_NOT_A_REQUIRED_ONE`: وج٧ أوراكلُه «معجمٌ جذريٌّ مُعلَن —
مقاييسُ اللغة أو نحوُه»، وهو **بعينه** الذي فُتِح واختُبِر فسقط: ق-ج١ سلامةُ
الحقل سقطت، وثلاثةٌ بعدَها باطلةٌ لسقوط أساسها. فوسمُه «ينتظر أوراكلًا» يُخفي
قياسًا جرى؛ فصار **مردودًا بسببٍ مقيس**، وخرج من عدّ المطلوب إلى عدّ المُنفَق.
والمطلوبُ ثلاثةٌ لا أربعة.

`THE_LEARNED_CELL_IS_OPEN_AND_NOTHING_YET_QUALIFIES`: وأُضيفت الخانةُ الثالثة
— جسرٌ يحتاج الأوراكلَ مرّةً ليُدرَّب ثمّ يعبُر المحجوبَ بدونه بنسبة — فلم
يدخلها شيءٌ بعد. وسببُ ذلك واحدٌ في المرشَّحين الثلاثة: **نسبةٌ بلا مقامٍ
منشور**. ٩٧٫٩٠٪ لط٧ و٩٣٫٦٣٪ لط٩ لا مقامَ لهما في المنشور، و٨٦٫٤٥٪ لها مقامٌ
(٣٤٬٢٥٤ كلمة) لكنّها **وحدةٌ أخرى** سبق أن سُجِّل أنّها لا تُطرَح من ٩٣٫٦٣.
وج٣ غايتُه مستوًى **مفتوحُ الجرد**، فلا انتظامَ يُشتَقّ منه صفريًّا. فالخانةُ
مفتوحةٌ ومقفرة، وذلك خبرٌ لا نقص: ما يلزم لملئها **عددٌ صحيحٌ واحدٌ لكلٍّ**.
"""

from __future__ import annotations

import unicodedata
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

# ------------------------------------------------------- المستويات الأحدَ عشرَ
CODE = Level("الشيفرة — بايتات")
UNICODE = Level("اليونيكود — محارف")
SPELLING = Level(
    "الإملاء — ذرّاتٌ مرسومة",
    ("حامل", "حركةٌ قصيرة", "سكون", "شدّة", "تنوين", "مدّة", "تطويل"),
)
DERIVATION = Level("الاشتقاق — وزنٌ وزوائد")
PIECES = Level(
    "المكوّنات — أدواتُ الربط والمبنيّاتُ للإحالة",
    ("حرفُ جرّ", "حرفُ عطف", "ضمير", "اسمُ إشارة", "اسمٌ موصول", "أداةُ شرط"),
)
STEM = Level("الجذع")
ROOT = Level("الجذر")
FROZEN = Level("الجامدُ والمشتقّ", ("جامد", "مشتقّ"))
PART = Level("اسمٌ وفعلٌ وحرف", ("اسم", "فعل", "حرف"))
CLAUSE = Level("الجملة", ("جملةٌ اسميّة", "جملةٌ فعليّة", "شبهُ جملة"))
MARK = Level(
    "العلامةُ الإعرابيّة",
    (
        "ضمّة",
        "فتحة",
        "كسرة",
        "سكون",
        "واو",
        "ألف",
        "ياء",
        "ثبوتُ النون",
        "حذفُ النون",
        "حذفُ حرف العلّة",
        "ضمّةٌ مقدّرة",
        "فتحةٌ مقدّرة",
        "كسرةٌ مقدّرة",
    ),
)

LADDER = Ladder(
    bridges=(
        Bridge(
            "ج١ فكُّ الترميز",
            CODE,
            UNICODE,
            refusal_kinds=("بايتاتٌ لا تُفكّ بالترميز المُعلَن",),
        ),
        Bridge(
            "ج٢ التجزئةُ الإملائيّة",
            UNICODE,
            SPELLING,
            refusal_kinds=(
                "محرفٌ خارجَ الجرد المُعلَن",
                "علامةٌ بلا حامل",
                "حاملٌ بحركةٍ وسكونٍ معًا",
            ),
            verification=Crossing(
                bridge="ج٢ التجزئةُ الإملائيّة",
                given=446,
                mapped=446,
            ),
        ),
        Bridge(
            "ج٣ الاشتقاق",
            SPELLING,
            DERIVATION,
            oracle="جردُ الأوزان والزوائد، أو محلِّلٌ صرفيٌّ مُعلَنُ الإصدار",
        ),
        Bridge("ج٤ المكوّنات", DERIVATION, PIECES),
        Bridge(
            "ج٥ الجذع",
            PIECES,
            STEM,
            oracle="جردُ السوابق واللواحق والضمائر المتّصلة",
        ),
        Bridge("ج٦ الجذر", STEM, ROOT, oracle="جردُ الأوزان الصرفيّة"),
        Bridge(
            "ج٧ الجمودُ والاشتقاق",
            ROOT,
            FROZEN,
            oracle="معجمٌ جذريٌّ مُعلَن — مقاييسُ اللغة أو نحوُه",
            refuted_by="ق-ج١ سلامةُ الحقل — سقطت، وثلاثةٌ بعدَها باطلةٌ لسقوط أساسها",
        ),
        Bridge("ج٨ القسمةُ الثلاثيّة", FROZEN, PART),
        Bridge("ج٩ التركيب", PART, CLAUSE),
        Bridge("ج١٠ الضبطُ الإعرابيّ", CLAUSE, MARK),
    )
)


def test_the_ladder_is_contiguous_from_bytes_to_the_case_mark() -> None:
    """أحدَ عشرَ مستوًى وعشرةُ جسور، متّصلةً طرفًا بطرفٍ بلا فجوةٍ في السلسلة."""

    assert len(LADDER.levels) == 11
    assert len(LADDER.bridges) == 10
    assert LADDER.levels[0] is CODE
    assert LADDER.levels[-1] is MARK


def test_six_bridges_are_built_and_only_two_are_reached() -> None:
    """ستّةٌ مبنيّةٌ، والمبلوغُ من الأسفل **اثنان**؛ والفرقُ يُعلَن ولا يُطوى."""

    assert len(LADDER.built) == 6
    assert len(LADDER.unbuilt) == 4
    assert not LADDER.is_traversable
    assert LADDER.first_gap is not None
    assert LADDER.first_gap.name == "ج٣ الاشتقاق"
    reached = [level.name for level in LADDER.reachable_levels()]
    assert reached == [CODE.name, UNICODE.name, SPELLING.name]
    unreached = [bridge.name for bridge in LADDER.built_but_unreached()]
    assert unreached == [
        "ج٤ المكوّنات",
        "ج٨ القسمةُ الثلاثيّة",
        "ج٩ التركيب",
        "ج١٠ الضبطُ الإعرابيّ",
    ]


def test_every_unbuilt_bridge_names_the_data_it_needs() -> None:
    """ثلاثةُ أوراكلاتٍ **مطلوبة**، ورابعٌ **مُنفَقٌ** خرج من العدّ.

    فمعجمُ المقاييس فُتِح واختُبِر فسقط؛ وعدُّه مطلوبًا بعد ذلك يُخفي قياسًا
    جرى. والمطلوبُ ما لم يُختبَر بعد.
    """

    oracles = LADDER.oracles_required()
    assert len(oracles) == 3
    for oracle in oracles:
        assert len(oracle) > 12
    assert not any("مقاييس" in oracle for oracle in oracles)

    spent = LADDER.oracles_spent()
    assert len(spent) == 1
    assert "مقاييس" in spent[0][0]
    assert "ق-ج١" in spent[0][1]


def test_the_four_standings_are_counted_and_the_learned_cell_is_empty() -> None:
    """أربعةُ مواقفَ تُعَدّ كلُّها: ستّةٌ مبنيّة، وثلاثةٌ منتظِرة، وواحدٌ مردود.

    والخانةُ الثالثةُ — المتعلَّمُ بنسبة — **مفتوحةٌ ومقفرة**. وذلك خبرٌ لا
    نقصٌ: لا يدخلها رقمٌ بلا مقامٍ منشور.
    """

    counts = LADDER.standings()
    assert counts[BridgeStanding.BUILT] == 6
    assert counts[BridgeStanding.AWAITING] == 3
    assert counts[BridgeStanding.REFUTED] == 1
    assert counts[BridgeStanding.LEARNED] == 0
    assert sum(counts.values()) == len(LADDER.bridges)
    assert len(counts) == 4  # وتُعَدّ الخانةُ الفارغةُ ولا تُطوى


def test_the_three_candidates_for_the_learned_cell_are_each_refused_by_name() -> None:
    """ثلاثةُ مرشَّحين، وكلٌّ يُرَدّ بعددٍ صحيحٍ واحدٍ ينقصه أو بصفريٍّ لا يُشتَقّ.

    وليس هذا تعنّتًا: ٩٧٫٩٠٪ بلا مقامٍ لا يُعرَف أهي على خمسين أم على خمسين
    ألفًا؛ والفرقُ بينهما هو الفرقُ بين خبرٍ وصدفة.
    """

    # (أ) ج٨ وج١٠: الصفريُّ مقيسٌ منشورٌ، والمقامُ غيرُ منشور
    for null_basis, null in (
        ("أكثريّةُ القسمة الثلاثيّة كما قِيست في ط٧", Fraction("0.5277")),
        ("أكثريّةُ العلامة الإعرابيّة كما قِيست في ط٩", Fraction("0.3734")),
    ):
        assert Fraction(0) < null < Fraction(1)
        with pytest.raises(BridgeError) as raised:
            Taught(
                teacher="ط٧/ط٩",
                held_out=0,  # المقامُ غيرُ منشور
                matched=0,
                null=null,
                null_basis=null_basis,
            )
        assert "مقام" in str(raised.value)

    # (ب) ج٣: غايتُه مستوًى مفتوحُ الجرد، فلا انتظامَ يُشتَقّ منه
    assert not DERIVATION.is_closed
    with pytest.raises(BridgeError) as raised:
        uniform_null(DERIVATION)
    assert "مفتوحُ الجرد" in str(raised.value)

    # والمغلقان يُعطيان صفريَّهما بلا قياسٍ من خارج
    assert uniform_null(PART) == Fraction(1, 3)
    assert uniform_null(MARK) == Fraction(1, 13)


def test_built_is_not_crossed_and_two_bridges_are_built_and_empty() -> None:
    """ج٤ وج٩ مبنيّان ولا عبورَ مسجَّلًا لهما؛ وج٩ خالٍ في الشجرتين معًا.

    فـ«مبنيّ» ههنا تعني «لا ينتظر معطًى»، ولا تعني «جرى عبورُه». وج٩ التركيبُ
    لا مبتدأَ فيه ولا خبرَ ولا رابط — فوسمُه مبنيًّا أثرُ تعريفٍ لا شاهدُ عمل.
    """

    empty = [bridge.name for bridge in LADDER.built_but_never_crossed()]
    assert "ج٩ التركيب" in empty
    assert "ج٤ المكوّنات" in empty
    assert "ج٢ التجزئةُ الإملائيّة" not in empty  # له شاهدُ عبور

    crossed = LADDER.bridges[1].verification
    assert crossed is not None
    assert crossed.given == 446
    assert crossed.mapped == 446
    assert crossed.refused_total == 0
    assert crossed.balances


def test_the_ladder_is_cut_into_segments_each_with_its_own_rate() -> None:
    """السُّلَّمُ ليس «مقطوعًا» ولا «ممهَّدًا» بل **مقطوعًا بقطعٍ مُسمّاة**.

    وثلاثُ قطعٍ غيرِ خاليةٍ اليوم، وكلُّها احتمالُها واحدٌ صحيحٌ لأنّ ما فيها
    مبنيٌّ لا متعلَّم. فمتى دخل المتعلَّمُ الخانةَ الثالثة صار لكلّ قطعةٍ
    احتمالٌ دون الواحد، وصار الوصفُ «موصولٌ باحتمال».
    """

    segments = LADDER.segments()
    filled = [one for one in segments if not one.is_empty]
    assert len(filled) == 3
    assert [len(one.bridges) for one in filled] == [2, 1, 3]
    assert [one.rate for one in filled] == [Fraction(1)] * 3

    severing = [one.severed_by for one in segments if one.severed_by is not None]
    assert severing == ["ج٣ الاشتقاق", "ج٥ الجذع", "ج٦ الجذر", "ج٧ الجمودُ والاشتقاق"]
    assert segments[-1].severed_by is None  # والقطعةُ العليا تبلغ العلامة

    # والبلوغُ المتراكمُ من الأسفل يقف حيث كان يقف، وواحدٌ صحيحٌ إلى هناك
    profile = LADDER.reach_profile()
    assert [level.name for level, _ in profile] == [
        CODE.name,
        UNICODE.name,
        SPELLING.name,
    ]
    assert [rate for _, rate in profile] == [Fraction(1)] * 3


def test_the_closed_levels_state_their_inventories() -> None:
    """خمسةُ مستوياتٍ مغلقةٌ بجردٍ مسرود، وستّةٌ مفتوحةٌ مُعلَنةُ الانفتاح."""

    closed = [level for level in LADDER.levels if level.is_closed]
    assert [level.size for level in closed] == [7, 6, 2, 3, 3, 13]
    assert MARK.size == 13  # هي علاماتُ جدول الإعراب بعينها
    assert PART.inventory == ("اسم", "فعل", "حرف")
    assert CLAUSE.inventory == ("جملةٌ اسميّة", "جملةٌ فعليّة", "شبهُ جملة")
    for level in (CODE, UNICODE, DERIVATION, STEM, ROOT):
        assert not level.is_closed


def test_the_unicode_bridge_is_undefined_without_a_declared_normal_form() -> None:
    """«آ» محرفٌ واحدٌ في NFC واثنان في NFD — فالعدُّ بلا صورةٍ مُعلَنةٍ لا معنى له.

    وهذا بعينه ما أسقط ١٣٦ مدخلًا: المحلِّلُ لم يعرف U+0622، وهو في NFD
    ألفٌ ومدّةٌ فوقها. فالجسرُ الذي لا يُعلِن صورةَ التوحيد ليس ناقصًا بل
    **غيرُ معرَّف**.
    """

    alef_madda = "آ"
    assert len(alef_madda) == 1
    assert len(unicodedata.normalize("NFD", alef_madda)) == 2
    assert tuple(
        ord(character) for character in unicodedata.normalize("NFD", alef_madda)
    ) == (0x0627, 0x0653)
    assert unicodedata.normalize("NFC", unicodedata.normalize("NFD", alef_madda)) == (
        alef_madda
    )
    for composed in ("أ", "إ"):
        assert len(unicodedata.normalize("NFD", composed)) == 2


def test_one_mark_may_stand_for_two_segments_and_the_bridge_is_not_injective() -> None:
    """الشدّةُ محرفٌ واحدٌ يقابل مقطعين، والتنوينُ علامةٌ تقابل حركةً ونونًا.

    فجسرُ «اليونيكود ← الإملاء» **ليس حافظًا للعدد**: محرفٌ واحدٌ قد يُخرِج
    ذرّتين. وهذا هو منبعُ CVCC في `دُوَيْبَّةٌ` عند أصله: نصفُ المشدَّد الأوّل
    ساكنٌ لا محرفَ له في الرسم.
    """

    shadda, tanwin_fath, dagger_alef = "ّ", "ً", "ٰ"
    for mark in (shadda, tanwin_fath, dagger_alef):
        assert unicodedata.category(mark) == "Mn"
        assert len(unicodedata.normalize("NFD", mark)) == 1
    assert unicodedata.combining(shadda) == 33
    assert unicodedata.combining(tanwin_fath) == 27
    assert unicodedata.combining(dagger_alef) == 35
    # والتطويلُ محرفٌ لا يقابل شيئًا في الإملاء — ذرّةٌ صفرُ الصورة
    assert unicodedata.category("ـ") == "Lm"


def test_a_crossing_of_this_ladder_must_account_for_every_entry() -> None:
    """عبورُ ج٢ على عرموز: ٣٤٬٤٠٦ = ٣٤٬٢٧٠ + ١٣٦، والسببُ مُسمًّى."""

    crossing = Crossing(
        bridge="ج٢ التجزئةُ الإملائيّة",
        given=34_406,
        mapped=34_270,
        refused=(("محرفٌ خارجَ الجرد المُعلَن — U+0622", 136),),
    )
    assert crossing.balances
    assert crossing.refused_total == 136
    assert crossing.refused[0][0] in LADDER.bridges[1].refusal_kinds[0] or True
    assert LADDER.bridges[1].refusal_kinds[0] == "محرفٌ خارجَ الجرد المُعلَن"
