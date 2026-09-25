"""**ختمٌ قبل النظر**: سلّمُ ماركوف بالمستويات — وأين تقف البايتات.

**لم يُشغَّل شيءٌ على المدوّنة بعد.** والآلةُ جُرّبت على شريحةٍ من ثمانين
سطرًا، وجاء فيها الملحَقُ للوحدة **٥٫٥٧ ⟶ ٤٫٨٠ ⟶ ١٫٩١ ⟶ ٠٫٠٩** نازلًا،
والمحجوزُ **٥٫٦٥ ⟶ ٤٫٩٢ ⟶ ٦٫١٧ ⟶ ٦٫٩١** — **فينقلب عند اللفظ**؛
و`I` **١٫٨٨ ⟶ ٢٫٧٩ ⟶ ٨٫٠٥ ⟶ ٦٫٣٠**. **ويُعلَن ذلك ههنا** فما رأيتُه قبل
الختم لا يُخفى. **ولا يُستخرَج من شريحةٍ بهذا الصغر شيءٌ عن أرقام
المدوّنة** — ولا سيّما موضعُ الانقلاب، فهو رهنُ التكرار، والمُجمَّدُ
أكثرُ تكرارًا من الشريحة بكثير.

**العطلُ الذي يُصلَح**: في `2a849c9a…` سمّيتُ الفاصلَ البنيويَّ **كلمةً**،
وهو **لفظٌ** — ما بين فاصلين. واللفظُ قد يحمل أكثرَ من كلمة، فتسميتُه
كلمةً **خلطُ مستويين**؛ والعدُّ صحيحٌ والاسمُ خطأ، ويُسجَّل كذلك.

**والسلّمُ مستوياتٌ مُشتَقّةٌ من البايتات وحدَها**: `م٠` الوحدةُ (١١٢)،
`م١` الرمزُ المُرخَّصُ بقيدِ الفاصل، `م٢` اللفظُ المفرد، `م٣` السطر —
**وهو ليس الجملة**.

**وما فوق ذلك لا تُرخّصه البايتات**: الكلمةُ المفردة، والتركيبُ
الإسناديّ، والتركيبُ المزجيّ، والجملة. **تُصنَّف ولا تُخترَع**، ولكلٍّ
سببٌ مكتوب.

**والمحجوزُ يُشحَن شحنًا يُفَكّ**: رمزٌ لم يُرَ يُشحَن **هروبًا ثمّ
هجاءً بالـ١١٢**، فلا يُفلِت بـ«أطول+١» — وإلّا كان مستوًى مرتدُّه واحدٌ
يبدو أرخصَ ممّا مرتدُّه صفر، **وهو عطلُ قياسٍ لا نتيجة**.

**و`induction on`**: متراجحتان مبرهَنتان عند كلّ مستوًى —
`log₂ التباديل ≤ N·H` و`H ≤ L < H+1`. **و`induction FOR`**: الحلقةُ
تشهد عليهما مستوًى مستوًى وتُري أين ينقلب المحجوزُ على الملحَق.

**ولا اسمٌ لصنفٍ يدخل**: وحداتٌ وألفاظٌ وأسطرٌ وبتّات.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, seal

VACANT = 4

ORACLE = Oracle(
    name="سلّمُ ماركوف من الوحدة إلى السطر — وحدُّ ما تُرخّصه البايتات",
    source="quran-simple-enhanced.txt — البصمة 37633090…",
    extraction=(
        "أربعةُ مستوياتٍ مُشتَقّةٍ من البايتات: الوحدةُ، والرمزُ المُرخَّصُ "
        "بقيدِ الفاصل، واللفظُ المفرد، والسطر. ولكلٍّ `H` وطولُ شفرةِ "
        "هوفمان ملحَقًا ومحجوزًا (بشطرَي المواضع، والمرتدُّ يُشحَن هروبًا "
        "ثمّ هجاءً بالـ١١٢) و`I(Xₜ;Xₜ₊₁)` على المجرى المسطَّح "
        "و`log₂` التباديل؛ وتُقسَم الأثمانُ على عدد وحدات L₀ فتُقارَن. "
        "وأربعةُ مستوياتٍ أعلى تُصنَّف UNCLASSIFIED بأسبابها"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="ي١",
        statistic="أدنى (L − H) على المستويات كلِّها (بتًّا للرمز)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies="مبرهنةَ شانون: شفرةٌ تُفَكّ لا تنزل تحت الإنتروبيا",
    ),
    Prediction(
        identifier="ي٢",
        statistic="أقصى (L − H) على المستويات كلِّها (بتًّا للرمز)",
        threshold=Fraction(999, 1000),
        direction=Direction.AT_MOST,
        falsifies="حدَّ هوفمان الأعلى `L < H + 1` في مستوًى من المستويات",
    ),
    Prediction(
        identifier="ي٣",
        statistic="أدنى (N·H − log₂ التباديل) على المستويات كلِّها (بتًّا)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies="متراجحةً مبرهَنة: عددُ التباديل لا يجاوز `2^(N·H)`",
    ),
    Prediction(
        identifier="ي٤",
        statistic="أقصى ارتفاعٍ في الثمن الملحَق للوحدة صعودًا في السلّم",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "أنّ التكتيلَ لا يرفع الثمنَ داخلَ العيّنة: فإن ارتفع في "
            "درجةٍ فالمستوى الأعلى **أغلى حتّى ملحَقًا**، وذلك خبرٌ عن "
            "المادّة لا عن الانتحال"
        ),
    ),
    Prediction(
        identifier="ي٥",
        statistic="أقصى ارتفاعٍ في الثمن المحجوز للوحدة صعودًا في السلّم",
        threshold=Fraction(1, 1000),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ السلّمَ ينقلب محجوزًا في درجةٍ ما؛ فإن نزل "
            "المحجوزُ في الدرجات كلِّها فالتصعيدُ **يربح إلى السطر**، "
            "ولا حدَّ يمنعه من المادّة — ويُنشَر ذلك"
        ),
    ),
    Prediction(
        identifier="ي٦",
        statistic="المحجوزُ للوحدة عند السطر − المحجوزُ عند الوحدة (بتًّا)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ القمّةَ أغلى من القاع محجوزًا؛ فإن كانت أرخصَ فالسطرُ "
            "مستوًى **يربح**، ويُعاد النظرُ في السلّم كلِّه"
        ),
    ),
    Prediction(
        identifier="ي٧",
        statistic="المحجوزُ للوحدة عند اللفظ − المحجوزُ عند الوحدة (بتًّا)",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "أنّ اللفظَ يبقى رابحًا محجوزًا على المُجمَّد؛ فإن جاء أغلى "
            "فالانقلابُ يقع **عند اللفظ** لا عند السطر، وحدُّ التصعيد "
            "أدنى ممّا يظنّ"
        ),
    ),
    Prediction(
        identifier="ي٨",
        statistic="I عند السطر − I عند الوحدة (بتًّا للموضع)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ `I` ترتفع صعودًا: وارتفاعُها ههنا **انتحالٌ لا بنية** — "
            "إذ كلُّ سطرٍ فريدٌ فيعيّن تاليَه في العيّنة. فإن نزلت فثمّ "
            "تكرارٌ بين الأسطر يستحقّ القياس"
        ),
    ),
    Prediction(
        identifier="ي٩",
        statistic="|عددُ المستويات المُصنَّفة UNCLASSIFIED − ٤|",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "الانضباطَ: الكلمةُ المفردة والإسناديُّ والمزجيُّ والجملة "
            "**لا تُرخّصها البايتات**، فتُصنَّف أربعةً بأسبابها؛ وزيادةٌ "
            "أو نقصٌ يعني أنّي اخترعتُ مستوًى أو طويتُه"
        ),
    ),
)

DIGEST = "248f10df081269afebdcb97ad1f4bea6879c6d52d9ce09e64bacb43bf4121ae2"
"""يُثبَّت بعد أوّل اشتقاق، ولا يُمَسّ بعدَه."""


def test_the_seal_is_recomputed_from_the_written_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_three_conditions_are_proven_bounds_not_claims_of_mine() -> None:
    """ي١ وي٢ وي٣ — شانون وهوفمان وستيرلنغ؛ وسقوطُها عطلُ حساب."""

    named = {
        "ي١": "مبرهنةَ شانون",
        "ي٢": "حدَّ هوفمان الأعلى",
        "ي٣": "متراجحةً مبرهَنة",
    }
    for identifier, mark in named.items():
        one = next(item for item in PREDICTIONS if item.identifier == identifier)
        assert mark in one.falsifies, identifier
    assert len(PREDICTIONS) == 9


def test_the_turn_is_read_at_two_places_not_one() -> None:
    """ي٥ أنّه ينقلب، وي٧ أين — وي٦ أنّ القمّةَ أغلى من القاع."""

    turn = next(one for one in PREDICTIONS if one.identifier == "ي٥")
    where = next(one for one in PREDICTIONS if one.identifier == "ي٧")
    top = next(one for one in PREDICTIONS if one.identifier == "ي٦")
    assert turn.direction is Direction.AT_LEAST
    assert where.direction is Direction.AT_MOST
    assert top.direction is Direction.AT_LEAST
    assert "عند اللفظ" in where.falsifies


def test_the_levels_above_the_bytes_are_classified_not_invented() -> None:
    """أربعةٌ تُصنَّف UNCLASSIFIED — ولا يُسمّى السطرُ جملةً."""

    counted = next(one for one in PREDICTIONS if one.identifier == "ي٩")
    assert counted.threshold == Fraction(0)
    assert "اخترعتُ مستوًى أو طويتُه" in counted.falsifies
    assert __doc__ is not None
    assert "وهو ليس الجملة" in __doc__
    assert VACANT == 4


def test_the_conflation_of_token_and_word_is_owned() -> None:
    """اللفظُ ليس الكلمة — والخلطُ مُسجَّلٌ في نصّ الختم."""

    assert __doc__ is not None
    assert "سمّيتُ الفاصلَ البنيويَّ **كلمةً**" in __doc__
    assert "وهو **لفظٌ**" in __doc__
    assert "خلطُ مستويين" in __doc__
    assert "والعدُّ صحيحٌ والاسمُ خطأ" in __doc__


def test_the_escape_must_be_decodable_and_says_why() -> None:
    """المرتدُّ يُهجّى بالـ١١٢ — وإلّا بدا المستوى الفارغُ أرخصَ."""

    assert "هروبًا ثمّ هجاءً بالـ١١٢" in ORACLE.extraction
    assert __doc__ is not None
    assert "عطلُ قياسٍ لا نتيجة" in __doc__


def test_the_slice_i_saw_before_sealing_is_declared() -> None:
    """ما رأيتُه قبل الختم مكتوبٌ فيه — ولا يُخفى بعد النظر."""

    assert __doc__ is not None
    for one in ("٥٫٦٥", "٦٫٩١", "١٫٨٨", "ثمانين"):
        assert one in __doc__, one
