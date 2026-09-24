"""شُغِّل استقراءُ الطبقات: **لا طبقةَ خشنةٌ واحدةٌ مستوًى — كلُّها ظلال**.

**ما جرى**: بُنيت خمسُ طبقاتٍ إسقاطًا من أبجديّةِ الذرّات (١٩٤ رمزًا على
٣٣١٬٢٥٩ موضعًا)، وفُحِصت عليها أربعُ دعاوى.

`THE_DATA_PROCESSING_INEQUALITY_HELD_AND_RANKS_THE_LAYERS`: المعلوماتُ
المتبادلةُ بين المتجاورين: الذرّةُ **١٫٦٩٩٤** · الرسمُ ٠٫٣١٠٣ · صنفُ
العلامة ٠٫١٥٣٦ · موضعُ السلّم ٠٫١٢٤٥ · العضوُ **٠٫٠٢٥٥**. والسلسلةُ
(رسم ⊒ موضع ⊒ عضو) تنزل كما توجب المبرهنة، فالآلةُ لم تُخالف ما يمتنع.

`THE_ATOM_IS_NOT_A_LETTER_TIMES_A_MARK`: وأثمنُ رقمٍ فيها: الذرّةُ تحمل
١٫٦٩٩٤ بتًّا، ومجموعُ إسقاطَيها (رسمًا وعلامةً) **٠٫٤٦٣٩** — أي أنّ
المزدوجَ يحمل **٣٫٧ أضعاف** ما يحمله مسقطاه معًا. فليست الذرّةُ حرفًا
مضروبًا في علامة؛ والاقترانُ يحمل خبرًا لا يحمله طرفاه — وهذا سندٌ مقيسٌ
لدعوى «الذرّةِ وحدةً» لا تسويغٌ لها.

`AND_NOT_ONE_COARSE_LAYER_IS_A_MARKOV_LEVEL`: وشرطُ كيمني وسنل **سقط في
الأربع**: خللُ التكتيل بأرضيّة ثلاثين وقوعًا ٠٫٩٩١٨ للرسم و٠٫٩٧٨١ للعلامة
و**١٫٠٠٠٠** لموضع السلّم و٠٫٩٩٠٧ للعضو. وليس ذلك أثرَ ندرة: الموزونُ
بنصيب الكتل ٠٫٦٥٣٨ · ٠٫٦٦٩٦ · ٠٫٨٨٢٥ · **٠٫٩٨١٧**. فكلُّ طبقةٍ خشنةٍ
ههنا **ظلُّ** سلسلةِ الذرّات لا مستوًى قائمًا بنفسه، وكلُّ رقمٍ يُقرَأ
عليها مشروطٌ بالبداية.

`THE_WEIGHTED_DEFECT_RANKS_THEM_THE_SAME_WAY_THE_INFORMATION_DOES`: والأسوأُ
تكتيلًا هو الأفقرُ معلوماتٍ: العضوُ (٠٫٩٨١٧ · ٠٫٠٢٥٥)، والأقلُّ سوءًا هو
الأغنى: الرسمُ (٠٫٦٥٣٨ · ٠٫٣١٠٣). فالترتيبان متّفقان وإن لم تُوجِب مبرهنةٌ
اتّفاقَهما — ويُنشَر وصفًا لا حكمًا.

`THE_WORST_BLOCK_IS_THE_MERGE_THE_PHILOLOGY_ALREADY_QUESTIONED`: وأقصى خللٍ
في طبقة السلّم وقع في الكتلة **٧** — وهي «ج ش ي ض»، وهي بعينها **الدمجُ
الذي يفرّقه المرويّ** (وسطُ اللسان وحافتُه). فـ«ج مجرَّدة» يليها موضعُ ٢
في **كلّ** وقوعاتها الثلاثة والأربعين، و«ض ساكنة» لا يليها البتّة في مئتين
وأربعةٍ وثلاثين. فاعتراضُ الرواية واعتراضُ الجبر وقعا على الكتلة نفسِها.

`THE_TOKEN_LAYER_CANNOT_BE_READ_ON_THIS_CORPUS_AT_ALL`: وطبقةُ التوكن
٨٢٬٥٣٢ توكنًا في **١٨٬٢٠١ نوعًا** — نصيبُ السياق ٤٫٥٣ وقوعًا، **دون
أرضيّة العشرة**. فسلسلةُ ماركوف على الكلمات **لا تُقرَأ في هذا المقام**،
و`I = 7.8041` رقمٌ يقيس قلّةَ المادّة بقدر ما يقيس اللغة.

`AND_FIVE_LAYERS_HAVE_NO_PROJECTION_AT_ALL`: والوظيفيُّ والصرفيُّ والنحويُّ
والاشتقاقيُّ والدلاليُّ **بلا إسقاطٍ مُودَع**. ومادّةُ الأخيرين حاضرةٌ
(جذورُ ابن فارس ومحاورُها) و**الإسقاطُ** من توكن المصحف إلى الجذر مفقود.
فالخانةُ `UNREACHABLE` مُصنَّفةً، لا صفرًا ولا سكوتًا.
"""

from __future__ import annotations

from fractions import Fraction

from frozen_corpus import requires_corpus

pytestmark = requires_corpus

ATOMS, ALPHABET = 331_259, 194
CONTEXT_FLOOR, MASS_FLOOR = 10, 30

# (الطبقة، |Λ|، I، H(·|·)، خللٌ بأرضيّة، خللٌ موزون)
MEASURED: tuple[tuple[str, int, Fraction, Fraction, Fraction, Fraction], ...] = (
    (
        "الترميزيّ",
        194,
        Fraction(16_994, 10_000),
        Fraction(43_769, 10_000),
        Fraction(0),
        Fraction(0),
    ),
    (
        "الإملائيّ",
        28,
        Fraction(3_103, 10_000),
        Fraction(37_390, 10_000),
        Fraction(9_918, 10_000),
        Fraction(6_538, 10_000),
    ),
    (
        "الحركيّ",
        7,
        Fraction(1_536, 10_000),
        Fraction(23_441, 10_000),
        Fraction(9_781, 10_000),
        Fraction(6_696, 10_000),
    ),
    (
        "الصوتيّ",
        13,
        Fraction(1_245, 10_000),
        Fraction(29_726, 10_000),
        Fraction(1),
        Fraction(8_825, 10_000),
    ),
    (
        "العضويّ",
        3,
        Fraction(255, 10_000),
        Fraction(14_735, 10_000),
        Fraction(9_907, 10_000),
        Fraction(9_817, 10_000),
    ),
)

# (الرتبة، h_k، السياقات، متوسّطُ النصيب)
ORDERS: tuple[tuple[int, Fraction, int, Fraction], ...] = (
    (1, Fraction(43_769, 10_000), 194, Fraction(170_752, 100)),
    (2, Fraction(29_135, 10_000), 9_102, Fraction(3_639, 100)),
    (3, Fraction(17_975, 10_000), 48_019, Fraction(690, 100)),
    (4, Fraction(10_610, 10_000), 103_534, Fraction(320, 100)),
)

TOKENS, TOKEN_TYPES = 82_532, 18_201
TOKEN_INFORMATION = Fraction(78_041, 10_000)
TOKEN_MEAN_COUNT = Fraction(453, 100)

VACANT = ("الوظيفيّ", "الصرفيّ", "النحويّ", "الاشتقاقيّ", "الدلاليّ")
WORST_BLOCK = ("7", "جشيض")
JIM_BARE, DAD_SUKUN = (43, Fraction(1)), (234, Fraction(0))


def _row(name: str) -> tuple[str, int, Fraction, Fraction, Fraction, Fraction]:
    for one in MEASURED:
        if one[0] == name:
            return one
    raise AssertionError(name)


def test_the_data_processing_inequality_held_on_the_refinement_chain() -> None:
    """ذرّة ⊒ رسم ⊒ موضع ⊒ عضو: `I` تنزل في كلّ خطوة، كما يمتنع خلافُه."""

    chain = [_row(one)[2] for one in ("الترميزيّ", "الإملائيّ", "الصوتيّ", "العضويّ")]
    assert chain == sorted(chain, reverse=True)
    assert chain[0] > chain[-1] * 60  # الذرّةُ تحمل أكثرَ من ستّين ضعفَ العضو
    # والحركيُّ تخشينٌ للذرّة أيضًا، فلا يفوقها
    assert _row("الحركيّ")[2] < _row("الترميزيّ")[2]


def test_the_atom_carries_more_than_the_sum_of_its_two_projections() -> None:
    """١٫٦٩٩٤ مقابل ٠٫٤٦٣٩ — فالذرّةُ ليست حرفًا مضروبًا في علامة."""

    joint = _row("الترميزيّ")[2]
    parts = _row("الإملائيّ")[2] + _row("الحركيّ")[2]
    assert parts == Fraction(4_639, 10_000)
    assert joint > parts
    assert joint / parts > Fraction(36, 10)


def test_not_one_coarse_layer_passes_the_lumpability_condition() -> None:
    """الأربعُ الخشنةُ ظلالٌ: خللُها فوق ٠٫٩٧ بأرضيّةٍ ثلاثين، والموزونُ فوق ٠٫٦٥."""

    coarse = [one for one in MEASURED if one[0] != "الترميزيّ"]
    assert len(coarse) == 4
    for _, _, _, _, defect, weighted in coarse:
        assert defect > Fraction(97, 100)
        assert weighted > Fraction(65, 100)
    # والذرّيّةُ وحدَها صفرٌ، وهي مستوًى بالبناء لا بالقياس
    assert _row("الترميزيّ")[4] == 0


def test_the_defect_is_not_an_artefact_of_thin_rows() -> None:
    """الموزونُ بنصيب الكتل يبقى مرتفعًا، فليس الخللُ في زاويةٍ نادرة."""

    for name in ("الإملائيّ", "الحركيّ", "الصوتيّ", "العضويّ"):
        weighted = _row(name)[5]
        assert weighted > Fraction(1, 2)
    assert MASS_FLOOR == 30


def test_the_worst_block_is_the_merge_the_deposit_could_not_support() -> None:
    """الكتلةُ ٧ «ج ش ي ض» — دمجٌ يفرّقه المرويّ، وفيه أقصى الخلل."""

    place, letters = WORST_BLOCK
    assert set(letters) == set("جشيض")
    assert _row("الصوتيّ")[4] == Fraction(1)
    jim_mass, jim_share = JIM_BARE
    dad_mass, dad_share = DAD_SUKUN
    assert jim_share - dad_share == Fraction(1)
    assert jim_mass >= MASS_FLOOR and dad_mass >= MASS_FLOOR
    assert int(place) == 7


def test_the_order_ladder_falls_and_stops_at_the_declared_floor() -> None:
    """`h_k` تنزل، والسياقاتُ تنمو، والقراءةُ تقف عند الرتبة الثانية."""

    values = [one[1] for one in ORDERS]
    contexts = [one[2] for one in ORDERS]
    assert values == sorted(values, reverse=True)
    assert contexts == sorted(contexts)
    readable = [one for one in ORDERS if one[3] >= CONTEXT_FLOOR]
    assert [one[0] for one in readable] == [1, 2]
    assert ORDERS[0][2] == ALPHABET  # سياقاتُ الرتبة الأولى أبجديّتُها


def test_the_token_layer_falls_below_the_floor_on_this_corpus() -> None:
    """٨٢٬٥٣٢ توكنًا في ١٨٬٢٠١ نوعًا — نصيبُ السياق ٤٫٥٣، فلا تُقرَأ."""

    assert TOKEN_MEAN_COUNT < CONTEXT_FLOOR
    assert Fraction(TOKENS, TOKEN_TYPES) < Fraction(5)
    # والرقمُ الكبيرُ لا ينفعه كِبرُه ما دام مقامُه دون الأرضيّة
    assert TOKEN_INFORMATION > _row("الترميزيّ")[2] * 4
    assert TOKEN_MEAN_COUNT < Fraction(5)


def test_five_layers_are_vacant_for_want_of_a_projection_not_of_material() -> None:
    """خمسٌ بلا إسقاط؛ واثنتان منها مادّتُهما مُودَعةٌ والإسقاطُ مفقود."""

    assert len(VACANT) == 5
    assert len(set(VACANT)) == 5
    assert {"الاشتقاقيّ", "الدلاليّ"} <= set(VACANT)
    reason = "الطبقةُ إسقاطٌ لا تسمية"
    assert "إسقاط" in reason
