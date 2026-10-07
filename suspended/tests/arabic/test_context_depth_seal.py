"""**ختمٌ قبل النظر**: سقفُ سلّم السياق **المادّيُّ** — لا سقفُ حدّي.

**لم يُشغَّل شيءٌ بعد.**

**لِمَ هذا التشغيل**: `deposits/context_ladder_run.log` يقف عند **الدرجة
الثانيةَ عشرة**، وليس في السجلّ سطرُ «الوقوف». **فالحلقةُ لم تتوقّف
بالمادّة، بل بسقفٍ كتبتُه أنا** (`MOST = 12`). **فالسقفُ المادّيُّ غيرُ
مبلوغ**، وذلك دَينٌ مُعلَن: كلُّ قولٍ عن «أقصى ما يفيده السياق» **مقيَّدٌ
بحدٍّ من عندي لا من المدوّنة**.

`AND_THE_LOOP_ALREADY_KNOWS_WHEN_TO_STOP`: والحلقةُ **تحمل شرطَ وقوفها
أصلًا**: `if best is None or best[0] <= 0` — تتوقّف إذ لا سؤالَ يربح
**محجوزًا**. فالسقفُ المادّيُّ **ليس شيئًا جديدًا يُخترَع**، هو ما تبلغه
الحلقةُ نفسُها إذا رُفِع السقفُ المكتوب.

`AND_THE_SEALED_SCRIPT_IS_NOT_EDITED`: **ولا يُحرَّر `run_context_ladder.py`
بحرف** — سجلٌّ مُودَعٌ مُبصَّمٌ يُقابَل بايتةً ببايتة يقرأ مخرَجَه (العطل
٢٩: **مُدخَلُ سجلٍّ مُقفَلٍ مُقفَلٌ مثلُه**). فيُكتَب **غلافٌ** يُحمِّل
الوحدةَ ويرفع `MOST` **في الذاكرة لا في الملفّ**، ويُشغِّل `main` نفسَها.
**فالشفرةُ المقيسةُ هي هي، والسقفُ وحدَه يتبدّل.**

`AND_THE_PREFIX_MUST_REPRODUCE_OR_THE_WRAPPER_IS_LYING`: **والاثنتا عشرةَ
الأولى يجب أن تُعاد حرفًا بحرف**: الجشعُ يختار عند كلّ درجةٍ أربحَ سؤالٍ
محجوزًا، **ولا يتعلّق اختيارُه بالسقف**. فإن خالفت درجةٌ من الأولى
**فالغلافُ يقيس شيئًا آخر**، ويسقط التشغيلُ لا المادّة.

**وinduction on**: `log₂ التباديل ≤ N·H` عند كلّ درجة، والربحُ المحجوزُ
موجبٌ في كلّ درجةٍ مبلوغةٍ **بحكم شرط الوقوف**. **وinduction FOR**: الحلقةُ
تشهد درجةً درجةً، ويُطبَع سطرُ الوقوف بموضعه.

**وما لا يُدَّعى**: بلوغُ السقف المادّيّ **لا يقول إنّ السياقَ استُنفِد** —
يقول إنّ **هذه العائلاتَ الخمسَ من الأسئلة** استُنفِدت على **هذه القسمة**
(زوجيٌّ وفرديٌّ بالسطر). وعائلةٌ سادسةٌ قد تربح، **وذلك دَينٌ يُسمّى ولا
يُسدّ بهذا التشغيل**.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, seal

ORACLE = Oracle(
    name="سقفُ سلّم السياق المادّيّ: أين تقف الحلقةُ إذا رُفِع سقفُ الآلة؟",
    source="quran-simple-enhanced.txt — البصمة 37633090…",
    extraction=(
        "تُحمَّل `examples/rasm/run_context_ladder.py` ويُرفَع `MOST` إلى "
        "عدد الأسئلة المتاحة، **ولا يُحرَّر الملفُّ**. والشفرةُ هي هي: "
        "الحالُ آخرُ محرفٍ إن كان `Mn` وإلّا «بلا علامة»؛ والسياقُ ما "
        "مضى وحدَه؛ والقسمةُ زوجيٌّ وفرديٌّ بالسطر بتنعيم لابلاس "
        "وبالتبادل؛ والحكمُ على المحجوز. والحلقةُ تقف إذ لا سؤالَ يربح "
        "محجوزًا (`best[0] <= 0`) أو إذ تنفد الأسئلة. و«الدرجاتُ "
        "المبلوغة» عددُ الأسئلة المختارة. و«أدنى إنتروبيا محجوزة» آخرُ "
        "قيمةٍ للمحجوزة. و«مجموعُ الكسب المحجوز» مجموعُ أرباح الدرجات"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="ذ١",
        statistic="|عددُ الأسطر − ٦٬٢٣٦|",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies="الآلةَ لا المادّة: المدوّنةُ مُجمَّدةٌ ببصمةٍ مُودَعة",
    ),
    Prediction(
        identifier="ذ٢",
        statistic="|عددُ الألفاظ − ٧٨٬٢٤٥|",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies="الآلةَ أيضًا: حدُّ اللفظ المُصحَّحُ من `494465d1…`",
    ),
    Prediction(
        identifier="ذ٣",
        statistic="|عددُ الأسئلة المتاحة − ٥٧|",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "الآلةَ: الأسئلةُ قيمُها مجموعةٌ من المجمَّد، فإن تبدّل عددُها "
            "فالغلافُ يقيس مسندًا آخر"
        ),
    ),
    Prediction(
        identifier="ذ٤",
        statistic="درجاتٌ من الاثنتي عشرةَ الأولى تخالف السجلَّ المُودَع",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "الآلةَ لا المادّة: اختيارُ الجشع لا يتعلّق بالسقف، فإن خالفت "
            "درجةٌ **فالغلافُ يقيس شيئًا آخر** ويسقط التشغيل"
        ),
    ),
    Prediction(
        identifier="ذ٥",
        statistic="الدرجاتُ المبلوغة",
        threshold=Fraction(13),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ سقفي عند ١٢ كان **سابقًا للمادّة**؛ فإن وقفت "
            "الحلقةُ عند ١٢ أو أقلَّ فسقفي كان **مطابقًا للسقف المادّيّ** "
            "بالمصادفة، ولا دَينَ كان"
        ),
    ),
    Prediction(
        identifier="ذ٦",
        statistic="الدرجاتُ المبلوغة (الحدُّ الأعلى)",
        threshold=Fraction(56),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوايَ أنّ الحلقةَ تقف **بالمادّة لا بنفاد الأسئلة**؛ فإن "
            "بلغت السبعةَ والخمسين فكلُّ سؤالٍ ربح، **والسقفُ المادّيُّ "
            "لم يُبلَغ بعدُ** — وذلك يُعلَن دَينًا لا يُطوى"
        ),
    ),
    Prediction(
        identifier="ذ٧",
        statistic="أدنى إنتروبيا محجوزةٍ تبلغها الحلقة، بتًّا",
        threshold=Fraction(22, 10),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ السياقَ لا ينزل بالمحجوزة إلى ما دون ٢٫٢٠ بتًّا؛ "
            "فإن نزلت **فالسياقُ أخبرُ ممّا قدَّرت**، وذلك خبرٌ عن المادّة"
        ),
    ),
    Prediction(
        identifier="ذ٨",
        statistic="مجموعُ الكسب المحجوز، بتًّا",
        threshold=Fraction(35, 100),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوايَ أنّ كلَّ ما يفيده السياقُ محجوزًا لا يبلغ ٠٫٣٥ بتًّا؛ "
            "فإن بلغه **فحدِّي عند ١٢ كان يكتم كسبًا معتبرًا**"
        ),
    ),
    Prediction(
        identifier="ذ٩",
        statistic="نصيبُ الدرجة الأولى من مجموع الكسب المحجوز",
        threshold=Fraction(15, 100),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ «آخرُ السطر» يبقى أكبرَ بتّةٍ ولو عُمِّق السلّم — "
            "لا يقلّ نصيبُها عن سُبعِ الكسب؛ فإن نقص **فالبتّةُ الأولى "
            "ليست غالبةً وإنّما بدت كذلك بسقفٍ قصير**"
        ),
    ),
    Prediction(
        identifier="ذ١٠",
        statistic="درجاتٌ مبلوغةٌ ربحُها المحجوزُ صفرٌ أو دونه",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "الآلةَ: شرطُ الوقوف يمنع ذلك بالبناء، فإن وقع فالحلقةُ لا "
            "تفعل ما يقول متنُها"
        ),
    ),
    Prediction(
        identifier="ذ١١",
        statistic="الربحُ المحجوزُ في الدرجة الأخيرة المبلوغة، بتًّا",
        threshold=Fraction(61, 10_000),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوايَ أنّ الأرباحَ تضمر كلّما عُمِّق السلّم، فلا يفوق آخرُها "
            "ربحَ الدرجة الثانيةَ عشرةَ؛ فإن فاقه **فالضمورُ ليس رتيبًا**، "
            "والجشعُ يجد متأخّرًا ما لم يجده متقدّمًا"
        ),
    ),
    Prediction(
        identifier="ذ١٢",
        statistic="درجاتٌ نزل فيها الربحُ الملحَقُ إلى صفرٍ أو دونه",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوايَ أنّ الملحَقَ ينزل بلا انقطاعٍ إلى آخر درجة؛ فإن توقّف "
            "**فالانقلابُ يبلغ الملحَقَ أيضًا**، وذلك خبرٌ عن المادّة"
        ),
    ),
)

DIGEST = "3fbbac9a65c5adc6c20d96d66b7811d4699dd903059fc2afdebb9a4dcb270cb7"
"""ختمُ التسجيل، مثبَّتٌ في المتن؛ وتبديلُ شرطٍ بعد النظر يُعرَف بتغيُّره."""

THE_FAMILIES_ARE_FIVE_AND_A_SIXTH_IS_NOT_MEASURED = (
    "بلوغُ السقف المادّيّ لهذه العائلات الخمس **لا يستنفد السياق**: "
    "عائلةٌ سادسةٌ (طولُ اللفظ، موقعُه من السطر، جارُه التالي…) قد تربح، "
    "ولم تُقَس ههنا — **دَينٌ يُسمّى ولا يُسدّ بهذا التشغيل**"
)
"""حدُّ التشغيل، مكتوبًا قبل النظر كي لا يُقرَأ استنفادًا."""


def test_the_seal_is_derived_from_the_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_nothing_has_been_run_yet() -> None:
    """يُعلَن في المتن أنّ الختمَ سبق النظر — والترتيبُ في التاريخ."""

    assert __doc__ is not None
    assert "**لم يُشغَّل شيءٌ بعد.**" in __doc__


def test_the_sealed_script_is_not_edited() -> None:
    """يُرفَع السقفُ في الذاكرة لا في الملفّ — العطل ٢٩ مقروءًا قبل الفعل."""

    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "**ولا يُحرَّر `run_context_ladder.py` بحرف**" in text
    assert "**مُدخَلُ سجلٍّ مُقفَلٍ مُقفَلٌ مثلُه**" in text
    assert "في الذاكرة لا في الملفّ" in text
    assert "ولا يُحرَّر الملفُّ" in " ".join(ORACLE.extraction.split())


def test_the_prefix_must_reproduce_or_the_wrapper_is_accused() -> None:
    """الاثنتا عشرةَ الأولى تُعاد حرفًا بحرف — وإلّا سقط التشغيل لا المادّة."""

    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "**والاثنتا عشرةَ الأولى يجب أن تُعاد حرفًا بحرف**" in text
    first = next(one for one in PREDICTIONS if one.identifier == "ذ٤")
    assert first.threshold == Fraction(0)
    assert "ويسقط التشغيل" in first.falsifies


def test_reaching_the_ceiling_is_not_exhausting_the_context() -> None:
    """بلوغُ السقف لا يقول إنّ السياقَ استُنفِد — والعائلةُ السادسةُ دَين."""

    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "**لا يقول إنّ السياقَ استُنفِد**" in text
    assert "وعائلةٌ سادسةٌ قد تربح" in text
    assert "دَينٌ يُسمّى" in THE_FAMILIES_ARE_FIVE_AND_A_SIXTH_IS_NOT_MEASURED


def test_five_refute_the_machine_and_seven_are_claims_of_mine() -> None:
    """خمسٌ تردُّ الآلةَ، وسبعٌ **دعاوٍ لي** تسقط بأرقامها."""

    machine = {"ذ١", "ذ٢", "ذ٣", "ذ٤", "ذ١٠"}
    mine = {one.identifier for one in PREDICTIONS} - machine
    assert len(mine) == 7
    for one in PREDICTIONS:
        if one.identifier in mine:
            assert "دعوايَ" in one.falsifies, one.identifier
        else:
            assert "الآلةَ" in one.falsifies, one.identifier
