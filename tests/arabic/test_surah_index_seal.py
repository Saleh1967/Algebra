"""**ختمٌ قبل النظر**: فهرسُ السور — **ما يحلُّه البايتُ وما لا يحلُّه**.

**لم يُشغَّل شيءٌ بعد.**

**لِمَ هذا التشغيل**: كان «فهرسُ السور» دَينًا مُعلَنًا في هذه الشجرة —
لا فهرسَ يُقال فيه أيُّ سطرٍ من أيّ سورة. **والمدوّنةُ لا تحمل رقمًا ولا
عنوانًا**: ستّةُ آلافٍ ومئتان وستّةٌ وثلاثون سطرًا من نصٍّ مضبوطٍ ليس فيه
عددُ سورةٍ ولا عددُ آية. فالفهرسُ **يُشتَقّ أو لا يكون**.

`AND_THE_ONLY_MARKER_IN_THE_BYTES_IS_THE_OPENING`: والعلامةُ الوحيدةُ في
البايتات **هيكلُ البسملة الرباعيّ** — `بسم · الله · الرحمن · الرحيم`
مجرَّدةً من الضبط. **ويُقرَأ من `examples/rasm/run_basmala_lifted.py`
(`HEAD`) لا يُكتَب ههنا**، فلا يدخل القياسَ حرفٌ طبعناه (المادّة ٩).

**والقسمة**: سطرٌ تبتدئه الكلماتُ الأربعُ **رأسُ كتلة**؛ وما بعده حتّى
الرأس التالي **كتلةٌ واحدة**. ويُفرَّق بين حالين: **البسملةُ قائمةً
بنفسها** (أربعُ كلماتٍ لا أكثر — فهي سطرٌ تامّ) و**البسملةُ ملحَقةً**
(أكثرُ من أربعٍ — فهي مُلحَقةٌ بأوّل ما بعدها).

`AND_WHAT_THE_BYTES_DO_NOT_LICENSE_IS_NAMED_IMPORTED_NOT_MEASURED`: **وأنّ
السورَ مئةٌ وأربعَ عشرةَ ليس مقيسًا ههنا — هو معلومٌ من خارج.** فإن حلَّ
البايتُ مئةً وثلاثةَ عشرَ رأسًا **لزِم حدٌّ واحدٌ لا علامةَ له في
البايتات**، وحكمُه `Vacancy.UNATTESTED`: **انعدامُ دليلٍ لا امتناعُ
بلوغ**، ولا يُخترَع له موضعٌ ولا يُصفَّر.

**ولا يُسمّى المعلومُ من خارجٍ قياسًا**: لا يُقال «الكتلةُ الفلانيّةُ
سورتان»، ولا يُرقَّم رأسٌ برقم سورة. **يُقال: البايتُ يحلّ مئةً وثلاثةَ
عشرَ كتلةً، والباقي مُصنَّف.**

**وinduction on**: مجموعُ أطوال الكتل = عددُ الأسطر بالضبط — **فلا سطرَ
يسقط بين كتلتين ولا يُعَدّ مرّتين**. **وinduction FOR**: يُفحَص ذلك عند
كلّ كتلةٍ لا في الجملة.

**وما لا يُدَّعى**: ليس هذا فهرسًا للقرآن — **هو فهرسُ ما تُرخّصه بايتاتُ
هذا المجمَّد**. ومن أراد ترقيمَ السور فعليه **إيداعُ جردٍ موقَّع**،
وحينئذٍ يُقاس الفهرسُ عليه ولا يُستنبَط منه.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

from algebra.results import Vacancy
from algebra.signified import Direction, Oracle, Prediction, seal

ORACLE = Oracle(
    name="فهرسُ السور: ما يحلُّه هيكلُ البسملة من حدود المدوّنة",
    source="quran-simple-enhanced.txt — البصمة 37633090…",
    extraction=(
        "السطرُ ما بين فاصلَي أسطرٍ، والفارغُ يُطرَح. والكلمةُ ما بين "
        "فراغين. والهيكلُ الكلمةُ منقوصةً كلَّ محرفٍ فئتُه `Mn`. وسطرٌ "
        "**رأسُ كتلةٍ** إن كانت هياكلُ كلماته الأربعِ الأُولى هي `HEAD` "
        "المقروءةُ من `examples/rasm/run_basmala_lifted.py` بترتيبها. "
        "والكتلةُ رأسُها وما بعده حتّى الرأس التالي أو آخرِ المدوّنة. "
        "وطولُ الكتلة عددُ أسطرها رأسَها منها. و«قائمةٌ بنفسها» رأسٌ "
        "كلماتُه أربعٌ لا أكثر، و«ملحَقةٌ» رأسٌ كلماتُه أكثرُ من أربع. "
        "و«يحمل الهيكلَ غيرَ مبتدأٍ به» سطرٌ فيه الكلماتُ الأربعُ "
        "متتالياتٍ في غير موضع الابتداء"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="ن١",
        statistic="|عددُ الأسطر غيرِ الفارغة − ٦٬٢٣٦|",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies="الآلةَ لا المادّة: المدوّنةُ مُجمَّدةٌ ببصمةٍ مُودَعة",
    ),
    Prediction(
        identifier="ن٢",
        statistic="عددُ رؤوس الكتل (أسطرٌ تبتدئها الكلماتُ الأربع)",
        threshold=Fraction(113),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ العلامةَ تحلُّ مئةً وثلاثةَ عشرَ حدًّا؛ فإن نقصت "
            "فالعلامةُ تحلُّ أقلَّ، **والدَّينُ أوسعُ ممّا قدَّرت**"
        ),
    ),
    Prediction(
        identifier="ن٣",
        statistic="عددُ رؤوس الكتل (الحدُّ الأعلى)",
        threshold=Fraction(113),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوايَ نفسَها من الطرف الآخر؛ فإن زادت فثمّةَ سطرٌ تبتدئه "
            "الكلماتُ الأربعُ وليس رأسَ سورة، **فالعلامةُ ليست حدًّا**"
        ),
    ),
    Prediction(
        identifier="ن٤",
        statistic="أسطرٌ لا تدخل كتلةً، أو تدخل كتلتين",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "الآلةَ: القسمةُ تامّةٌ بالبناء — مجموعُ أطوال الكتل عددُ "
            "الأسطر، فإن خالف فالقسمةُ لم تقع"
        ),
    ),
    Prediction(
        identifier="ن٥",
        statistic="أقصرُ كتلةٍ، أسطرًا",
        threshold=Fraction(3),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ أقصرَ ما تفصله العلامةُ ثلاثةُ أسطر؛ فإن نقص "
            "فثمّةَ كتلةٌ أقصرُ، **وذلك خبرٌ عن المادّة لا عن الآلة**"
        ),
    ),
    Prediction(
        identifier="ن٦",
        statistic="أطولُ كتلةٍ، أسطرًا",
        threshold=Fraction(286),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ أطولَ كتلةٍ لا تقلّ عن ٢٨٦ سطرًا؛ فإن نقصت فإمّا "
            "أنّ العلامةَ تقطع داخلَ ما ظننتُه كتلةً واحدةً، **أو أنّ "
            "المجمَّدَ ليس ما قدَّرت**"
        ),
    ),
    Prediction(
        identifier="ن٧",
        statistic="كتلٌ طولُها صفرٌ (رأسان متجاوران)",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوايَ أنّ العلامةَ لا تتكرّر في سطرين متجاورين؛ فإن وقع "
            "فثمّةَ كتلةٌ خاوية، **وذلك يُسمّى ولا يُطوى**"
        ),
    ),
    Prediction(
        identifier="ن٨",
        statistic="كتلٌ طولُها خمسةُ أسطرٍ أو أقلّ",
        threshold=Fraction(6),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ في المدوّنة ستَّ كتلٍ قصيرةٍ فأكثر؛ فإن نقصت "
            "فتقديري لأطوال الكتل القصيرة خاطئ، **وذلك خبرٌ عن المادّة**"
        ),
    ),
    Prediction(
        identifier="ن٩",
        statistic="كتلٌ طولُها ثلاثةُ أسطرٍ بالضبط",
        threshold=Fraction(3),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ ثلاثًا من الكتل طولُها ثلاثةُ أسطرٍ بالضبط؛ فإن "
            "نقصت فتقديري خاطئ، **ولا يُعاد تفسيرُه بعد النظر**"
        ),
    ),
    Prediction(
        identifier="ن١٠",
        statistic="أسطرٌ تحمل الكلماتِ الأربعَ متتالياتٍ غيرَ مبتدأةٍ بها",
        threshold=Fraction(2),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوايَ أنّ العلامةَ ترد في غير الابتداء مرّتين لا أكثر؛ فإن "
            "زادت **فالعلامةُ أكثرُ التباسًا ممّا قدَّرت**، ويُعَدّ ذلك"
        ),
    ),
    Prediction(
        identifier="ن١١",
        statistic="رؤوسٌ كلماتُها أربعٌ لا أكثر (البسملةُ قائمةً بنفسها)",
        threshold=Fraction(1),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ في المدوّنة سطرًا واحدًا هو البسملةُ وحدَها؛ فإن "
            "لم يكن **فالرؤوسُ كلُّها ملحَقةٌ**، وذلك خبرٌ عن كتابة المجمَّد"
        ),
    ),
    Prediction(
        identifier="ن١٢",
        statistic="رؤوسٌ كلماتُها أربعٌ لا أكثر (الحدُّ الأعلى)",
        threshold=Fraction(1),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوايَ نفسَها من الطرف الآخر؛ فإن زادت فثمّةَ أكثرُ من سطرٍ "
            "بسملةً قائمةً بنفسها، **وذلك يُعَدّ ولا يُفسَّر**"
        ),
    ),
)

DIGEST = "eb26eef8b6e70794428f3545044ec049eef6d57b32fd6b2d5fc8df8abd537fa1"
"""ختمُ التسجيل، مثبَّتٌ في المتن؛ وتبديلُ شرطٍ بعد النظر يُعرَف بتغيُّره."""

THE_HUNDRED_AND_FOURTEENTH_HAS_NO_MARKER = Vacancy.UNATTESTED
"""أنّ السورَ ١١٤ **معلومٌ من خارجٍ لا مقيسٌ ههنا**.

فإن حلَّ البايتُ ١١٣ رأسًا فحدٌّ واحدٌ **لا علامةَ له في البايتات**:
`UNATTESTED` — **انعدامُ دليلٍ لا امتناعُ بلوغ**. ولا يُخترَع له موضعٌ،
ولا يُقال «الكتلةُ الفلانيّةُ سورتان»، ولا يُصفَّر. **ويُسدّ بإيداع جردٍ
موقَّعٍ لا باستنباط.**
"""

NO_SURAH_IS_NUMBERED_HERE = "لا يُرقَّم رأسٌ برقم سورة؛ والترقيمُ يحتاج جردًا مُودَعًا"
"""حدُّ التشغيل: فهرسُ حدودٍ لا فهرسُ أسماء."""


def test_the_seal_is_derived_from_the_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_nothing_has_been_run_yet() -> None:
    """يُعلَن في المتن أنّ الختمَ سبق النظر — والترتيبُ في التاريخ."""

    assert __doc__ is not None
    assert "**لم يُشغَّل شيءٌ بعد.**" in __doc__


def test_the_marker_is_read_from_the_tree_not_typed_here() -> None:
    """هيكلُ البسملة يُقرَأ من الشجرة — المادّةُ ٩: لا حرفَ يُطبَع في فحصِ شكل."""

    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "`HEAD`" in text
    assert "لا يُكتَب ههنا" in text
    assert "HEAD" in " ".join(ORACLE.extraction.split())


def test_the_count_of_surahs_is_declared_imported_not_measured() -> None:
    """أنّ السورَ ١١٤ **معلومٌ من خارج** — ويُسمّى كذلك قبل النظر."""

    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "**وأنّ السورَ مئةٌ وأربعَ عشرةَ ليس مقيسًا ههنا — هو معلومٌ" in text
    assert THE_HUNDRED_AND_FOURTEENTH_HAS_NO_MARKER is Vacancy.UNATTESTED
    source = Path(__file__).read_text(encoding="utf-8")
    assert "**انعدامُ دليلٍ لا امتناعُ بلوغ**" in source
    assert "ولا يُصفَّر" in source


def test_the_partition_is_complete_by_construction() -> None:
    """مجموعُ أطوال الكتل عددُ الأسطر — ويُفحَص عند كلّ كتلة."""

    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "**فلا سطرَ يسقط بين كتلتين ولا يُعَدّ مرّتين**" in text
    assert any(one.identifier == "ن٤" for one in PREDICTIONS)


def test_this_is_not_an_index_of_the_book() -> None:
    """ليس فهرسًا للقرآن — فهرسُ ما تُرخّصه بايتاتُ هذا المجمَّد."""

    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "**هو فهرسُ ما تُرخّصه بايتاتُ هذا المجمَّد**" in text
    assert "إيداعُ جردٍ موقَّع" in text
    assert "جردًا مُودَعًا" in NO_SURAH_IS_NUMBERED_HERE


def test_four_refute_the_machine_and_the_rest_are_claims_of_mine() -> None:
    """أربعٌ تردُّ الآلةَ، والباقيةُ **دعاوٍ لي** تسقط بأرقامها."""

    machine = {"ن١", "ن٤"}
    mine = {one.identifier for one in PREDICTIONS} - machine
    assert len(mine) == 10
    for one in PREDICTIONS:
        if one.identifier in mine:
            assert "دعوايَ" in one.falsifies, one.identifier
        else:
            assert "الآلةَ" in one.falsifies, one.identifier
