"""**ختمٌ قبل النظر**: أداةُ التعدّي على محكٍّ من خارجها — Quranic Arabic Corpus.

**لم يُعَدّ شيءٌ على QAC بعد**: قُرئت من ملفّه أسطرُه الأولى وعددُ أسطره وعددُ كلمات
كلّ آية
(لمطابقة الآيات)، ولم يُقابَل به لفظٌ واحدٌ من ألفاظ الأداة.

**العِلّة**: وقّع صاحبُ المستودع جدولَ قرائن التعدّي
(`deposits/valency_cues_draft.tsv`) بنصّه
«حدث ووقع وادفع وقارن مع QAC». والأداةُ مودَعةٌ نصًّا قبل هذا الختم
(`deposits/valency_instrument.py.txt`، البصمة 4e0d868b…)؛ فالختمُ يسأل: هل ترى الأداةُ
من الرسم
ما يراه محلّلٌ صرفيٌّ مستقلّ، وهل يصمد أثرُ الوزن وعلامةُ ماركوف حين يُقاسان بتحليله
لا بها؟

**والمحكّ**: نسخةُ mustafa0x/quran-morphology (فرعٌ من QAC 0.4، الإيداع 8f38b39) —
رخصتُها GPL،
فلا تُودَع في المستودع (MIT)، ويُعطى مسارُها للتشغيل.

**وما أُجِّل**: ت١ في الجدول الموقَّع (سحبُ تصنيف الغني بعد الختم) يبقى لختمٍ بعده؛
وهذا الختمُ
يضع مكانه أثرَ الوزن بتحليل QAC.

**وتوقّعي بالتفكير**: يثبت ق١ وق٤ وت١ وت٣؛ ويسقط ق٢ (مضارعُ المجهول من المعتلّ يفوت
الأداة)؛
وق٣ وق٥ على الحدّ؛ وت٢ يثبت أو يسقط قليلًا.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, seal

ORACLE = Oracle(
    name="أداةُ التعدّي على محكّ QAC",
    source=(
        "quran-simple-enhanced.txt — البصمة 37633090…؛ "
        "وdeposits/valency_instrument.py.txt "
        "— البصمة 4e0d868b871a3a40…؛ وquran-morphology.txt "
        "من mustafa0x/quran-morphology "
        "عند 8f38b39"
    ),
    extraction=(
        "الأداةُ تُنفَّذ كما أُودعت، فتعطي TOKENS: (السطر، رقمُ اللفظ في سطره بعد طرح "
        "<sel>، اللفظ، التحليل) لكلّ لفظٍ عدّته فعلًا، والتحليلُ: الوزن، والبناءُ "
        "(فاعل/مفعول)، والزمن، والجذر، وعددُ الضمائر "
        "المفعولة؛ وres: صنفُ كلّ (جذر، وزن). "
        "والسطرُ i يقابل الآيةَ i بترتيب السور والآيات في QAC، ولا تُعَدّ إلّا آيةٌ "
        "تساوى عددُ ألفاظها في السطر وعددُ كلماتها في QAC، واللفظُ j يقابل الكلمةَ j. "
        "وكلمةُ QAC فعلٌ إن كان فيها مقطعٌ وسمُه V، "
        "ووزنُها VF، ومجهولةٌ إن كان فيه PASS، "
        "ولها ضميرٌ مفعولٌ إن تلا مقطعَ الفعل مقطعٌ فيه PRON وSUFF. "
        "ق١: من ألفاظ الأداة المجهولة في الآيات المتطابقة، "
        "حصّةُ ما هو في QAC فعلٌ مجهول. "
        "ق٢: من أفعال QAC المجهولة في الآيات المتطابقة، "
        "حصّةُ ما عدّته الأداةُ فعلًا مجهولًا. "
        "ق٣: من ألفاظ الأداة التي وزنُها I إلى X (لا I/IV) "
        "وهي في QAC فعل، حصّةُ ما وزنُه "
        "فيهما واحد. ق٤: من ألفاظ الأداة المبنيّة للفاعل "
        "وفيها ضميرٌ مفعولٌ فأكثر، حصّةُ ما "
        "هو في QAC فعلٌ بضميرٍ مفعول. ق٥: من ألفاظ الأداة "
        "كلّها في الآيات المتطابقة، حصّةُ "
        "ما هو في QAC فعل. "
        "ت١: جذورُ QAC التي لها في VF:1 ثلاثُ كلماتٍ فعليّةٍ فأكثر ليس فيها مجهولٌ ولا "
        "ضميرٌ مفعول، ولها في VF:4 كلمةٌ فأكثر (في المصحف "
        "كلّه لا المتطابق وحده)؛ حصّةُ ما "
        "في VF:4 منها مجهولٌ أو ضميرٌ مفعول. "
        "ت٢: لكلّ لفظٍ من الأداة مبنيٍّ للفاعل غيرِ أمرٍ "
        "ولا ضميرَ مفعولٍ فيه، صنفُه في res "
        "متعدٍّ (لواحد أو لاثنين) أو لازم (بأنواعه)، في آيةٍ "
        "متطابقة: أوّلُ كلمةٍ في الكلمات "
        "الثلاث بعده في QAC فيها مقطعٌ DET واسمٌ بحالةٍ من "
        "NOM ACC GEN، ويقف البحثُ عند كلمةٍ "
        "فيها مقطعٌ P (حرفُ جرّ) أو V؛ والمقيسُ حصّةُ ACC "
        "بعد المتعدّي ناقصًا حصّتَها بعد "
        "اللازم. "
        "ت٣: جذورُ QAC: سكن، شعر، طغي، عجب، عوذ، موت، "
        "فلح، بخل، شيأ، جري، توب، سجد، لبث "
        "(اللازمةُ في الغني) — عددُ كلماتها الفعليّة المجهولة في VF:1 نائبُها اسم (ليس "
        "بعدها مباشرةً كلمةٌ أوّلُ مقاطعها P)؛ والعدُّ على QAC لم يُرَ"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="ق١",
        statistic="دقّةُ المجهول: حصّةُ مجهولِ الأداة الذي هو مجهولٌ في QAC",
        threshold=Fraction(9, 10),
        direction=Direction.AT_LEAST,
        falsifies="أنّ قالبَ المجهول في الرسم يرى المجهولَ كما يراه المحلّل",
    ),
    Prediction(
        identifier="ق٢",
        statistic="استدعاءُ المجهول: حصّةُ مجهولِ QAC الذي عدّته الأداةُ مجهولًا",
        threshold=Fraction(4, 5),
        direction=Direction.AT_LEAST,
        falsifies="أنّ الأداةَ لا يفوتها من المجهول إلّا قليل",
    ),
    Prediction(
        identifier="ق٣",
        statistic="اتّفاقُ الوزن بين الأداة وQAC على الأفعال المشتركة",
        threshold=Fraction(17, 20),
        direction=Direction.AT_LEAST,
        falsifies="أنّ قوالبَ الأوزان العشرة تُصيب الوزنَ من الرسم",
    ),
    Prediction(
        identifier="ق٤",
        statistic="دقّةُ الضمير المفعول: حصّةُ ما عدّته الأداةُ بضميرٍ مفعولٍ وهو كذلك في QAC",
        threshold=Fraction(9, 10),
        direction=Direction.AT_LEAST,
        falsifies="أنّ القرينةَ ق١ (الضمير المفعول) قطعيّةٌ في الأداة",
    ),
    Prediction(
        identifier="ق٥",
        statistic="دقّةُ الفعل: حصّةُ ألفاظ الأداة التي هي أفعالٌ في QAC",
        threshold=Fraction(9, 10),
        direction=Direction.AT_LEAST,
        falsifies="أنّ الأداةَ تفرز الفعلَ من الاسم والحرف بالرسم وحده",
    ),
    Prediction(
        identifier="ت١",
        statistic="حصّةُ جذور VF:1 اللازمة في QAC التي لها في VF:4 مجهولٌ أو ضميرٌ مفعول",
        threshold=Fraction(4, 5),
        direction=Direction.AT_LEAST,
        falsifies="أنّ همزةَ أَفْعَلَ تعدّي اللازم، بتحليلٍ مستقلٍّ عن الأداة",
    ),
    Prediction(
        identifier="ت٢",
        statistic="حصّةُ ACC في أوّل معرَّفٍ بعد المتعدّي ناقصًا حصّتَها بعد اللازم (QAC)",
        threshold=Fraction(3, 20),
        direction=Direction.AT_LEAST,
        falsifies="أنّ تصنيفَ الأداة للتعدّي يتنبّأ بالمفعول المنصوب بعد الفعل",
    ),
    Prediction(
        identifier="ت٣",
        statistic="مجهولٌ نائبُه اسمٌ في VF:1 من الجذور الثلاثة عشر اللازمة في الغني",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies="أنّ اللازمَ لا يُبنى منه مجهولٌ نائبُه اسم",
    ),
)

DIGEST = "7f050383c3f695bf56afca44db098115c3cc6ea9ee05078854e529a8f2bf671e"
"""يُثبَّت بعد أوّل اشتقاق، ولا يُمَسّ بعدَه."""


def test_the_seal_is_recomputed_from_the_written_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_eight_conditions_five_on_the_instrument_three_on_the_language() -> None:
    """ق١–ق٥ على الأداة، وت١–ت٣ على اللغة."""

    names = [one.identifier for one in PREDICTIONS]
    assert names == ["ق١", "ق٢", "ق٣", "ق٤", "ق٥", "ت١", "ت٢", "ت٣"]


def test_the_table_is_signed_and_the_instrument_is_deposited() -> None:
    """الجدولُ موقَّع، والأداةُ مودَعةٌ ببصمتها — والعدُّ على QAC لم يُرَ."""

    import hashlib
    from pathlib import Path

    root = Path(__file__).resolve().parents[2] / "deposits"
    table = (root / "valency_cues_draft.tsv").read_text(encoding="utf-8")
    assert "# التوقيع: موقَّع" in table
    body = (root / "valency_instrument.py.txt").read_bytes()
    assert hashlib.sha256(body).hexdigest().startswith("4e0d868b871a3a40")
    assert "والعدُّ على QAC لم يُرَ" in ORACLE.extraction
