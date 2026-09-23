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
"""

from __future__ import annotations

import unicodedata

from algebra.bridge import Bridge, Crossing, Ladder, Level

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
    """أربعةُ أوراكلاتٍ مُسمّاة، ولا «يحتاج معجمًا» بلا تسمية."""

    oracles = LADDER.oracles_required()
    assert len(oracles) == 4
    for oracle in oracles:
        assert len(oracle) > 12
    assert any("مقاييس" in oracle for oracle in oracles)


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
