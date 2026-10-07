"""البندُ الثاني مُحضَّرًا: الجوابُ دالّةٌ في سطرٍ لم يُكتَب، والسطرُ ليس لي.

**ما يفعله هذا الملفّ**: لا يحسم شيئًا. يُقيم الجدولَ الذي يجعل الحسمَ
**سطرًا واحدًا**: ثلاثةُ معاييرِ قبولٍ مُعلَنة، ولكلٍّ جردُه اللازم، ولكلٍّ
ما يدخل به أو يخرج. فمتى كُتِب المعيارُ قُرئ الجوابُ من الجدول، ولا يُعاد
حسابٌ ولا يُفتَح بابُ اجتهاد.

`THE_ANSWER_IS_A_FUNCTION_OF_A_LINE_NOT_YET_WRITTEN`: «كم صنفَ مقطعٍ في
العربيّة؟» ليس سؤالًا واحدًا بل ثلاثةً، يفترقها **معيارُ القبول**. والجوابُ
أربعةٌ تحت واحدٍ وخمسةٌ تحت الآخرَين. فمن أجاب بعددٍ دون أن يُعلِن معيارَه لم
يُجِب، ومن أعلنه فالجوابُ يلزم عنه بلا بقيّة.

`THIS_DECISION_IS_NOT_MINE_TO_SIGN`: القرارُ مُعلَّقٌ في السجلّ، و«الجلسة»
و«claude» مرفوضتان سلطةً **في المُنشئ لا في تعليق**. فلو كتبتُ المعيارَ
لسقط البناءُ عند الإنشاء. وإعلانُ التمام يُرَدّ ما دام معلَّقًا.

`A_BRANCH_WITHOUT_A_PRICE_IS_NOT_A_BRANCH`: لكلّ معيارٍ ثمنٌ مكتوب — ما يلزم
قبولُه معه. فليس بين الثلاثة ما هو «أسلمُ» بلا كلفة، والاختيارُ مبادلةٌ
تُعلَن لا تفضيلٌ يُذاع.
"""

from __future__ import annotations

import pytest

from algebra.assignment import Assignment
from algebra.decisions import Branch, Decision, DecisionError, Register, Standing

CRITERIA = (
    "ق-أ مشهودٌ في المصحف",
    "ق-ب مولَّدٌ بالقواعد المُعلَنة",
    "ق-ج مقبولٌ عند النطق",
)
COLUMNS = (
    "نصُّ المعيار",
    "الجردُ اللازم",
    "ما يفترق به عن جاره",
    "ثمنُ اختياره",
)

CONSEQUENCE = Assignment(
    rows=CRITERIA,
    columns=COLUMNS,
    cells=(
        (
            "ق-أ مشهودٌ في المصحف",
            "نصُّ المعيار",
            "يُقبَل الصنفُ إن وقع مرّةً فأكثرَ في التقطيع المودَع",
        ),
        ("ق-أ مشهودٌ في المصحف", "الجردُ اللازم", "أربعة"),
        (
            "ق-أ مشهودٌ في المصحف",
            "ما يفترق به عن جاره",
            "يُخرِج الصنفَ الذي تولّده القواعدُ ولم يقع — والواقعُ ٢٢٥٬٩١٠ من ٢٢٥٬٩١١",
        ),
        (
            "ق-أ مشهودٌ في المصحف",
            "ثمنُ اختياره",
            "الجردُ يصير خبرًا عن **مدوَّنةٍ بعينها** لا عن العربيّة، ويتغيّر بتغيّرها",
        ),
        (
            "ق-ب مولَّدٌ بالقواعد المُعلَنة",
            "نصُّ المعيار",
            "يُقبَل الصنفُ إن لزم عن الذرّة والهبوط، وقع أم لم يقع",
        ),
        ("ق-ب مولَّدٌ بالقواعد المُعلَنة", "الجردُ اللازم", "خمسة"),
        (
            "ق-ب مولَّدٌ بالقواعد المُعلَنة",
            "ما يفترق به عن جاره",
            "يُدخِل الصنفَ المولَّدَ غيرَ المشهود؛ وهو موضعُ الفرق كلِّه",
        ),
        (
            "ق-ب مولَّدٌ بالقواعد المُعلَنة",
            "ثمنُ اختياره",
            "الجردُ يصير لازمَ **صيغةٍ** لا خبرًا عن وقوع، فيَسقط بسقوطها",
        ),
        (
            "ق-ج مقبولٌ عند النطق",
            "نصُّ المعيار",
            "يُقبَل الصنفُ إن نطقه أهلُ اللسان ولم يردّوه",
        ),
        ("ق-ج مقبولٌ عند النطق", "الجردُ اللازم", "خمسة"),
        (
            "ق-ج مقبولٌ عند النطق",
            "ما يفترق به عن جاره",
            "يوافق ق-ب في العدد ويخالفه في السند: حكمُ ناطقٍ لا لزومُ صيغة",
        ),
        (
            "ق-ج مقبولٌ عند النطق",
            "ثمنُ اختياره",
            "يقتضي **تجربةَ إدراكٍ** ليست عندنا، فهو معلَّقٌ على مدخلٍ مفقود",
        ),
    ),
)

PENDING = Decision(
    identifier="ق-٥ معيارُ قبول صنفِ المقطع",
    question="أيُقبَل الصنفُ بوقوعه، أم بلزومه عن الصيغة، أم بقبول الناطق؟",
    blocks=(
        "الجردُ الرباعيُّ — أربعةٌ أم خمسة",
        "كلُّ قولٍ يبدأ بـ«جردُ المقاطع أربعة»",
    ),
    branches=(
        Branch(
            label="ق-أ مشهودٌ في المصحف",
            effect="الجردُ أربعة",
            price="الجردُ خبرٌ عن مدوَّنةٍ بعينها، يتغيّر بتغيّرها",
        ),
        Branch(
            label="ق-ب مولَّدٌ بالقواعد المُعلَنة",
            effect="الجردُ خمسة",
            price="الجردُ لازمُ صيغةٍ يسقط بسقوطها، لا خبرُ وقوع",
        ),
        Branch(
            label="ق-ج مقبولٌ عند النطق",
            effect="الجردُ خمسة",
            price="يقتضي تجربةَ إدراكٍ ليست عندنا",
        ),
    ),
)

REGISTER = Register(
    decisions=(PENDING,),
    refused_authorities=frozenset(
        {"الجلسة", "المساعد", "claude", "Claude", "assistant"}
    ),
)


def test_the_grid_of_consequences_is_total() -> None:
    """ثلاثةُ معاييرَ × أربعةُ أعمدةٍ = اثنتا عشرةَ خليّةً، ولا واحدةَ منسيّة."""

    assert CONSEQUENCE.covers_the_grid()
    assert CONSEQUENCE.filled == 12
    assert CONSEQUENCE.forbidden_count == 0


def test_the_answer_is_four_under_one_criterion_and_five_under_two() -> None:
    """الجوابُ دالّةٌ في المعيار: ٤ تحت ق-أ، و٥ تحت ق-ب وق-ج."""

    answers = {row: CONSEQUENCE.value_at(row, "الجردُ اللازم") for row in CRITERIA}
    assert answers["ق-أ مشهودٌ في المصحف"] == "أربعة"
    assert answers["ق-ب مولَّدٌ بالقواعد المُعلَنة"] == "خمسة"
    assert answers["ق-ج مقبولٌ عند النطق"] == "خمسة"
    assert len(set(answers.values())) == 2  # الجوابان اثنان لا ثلاثة


def test_two_criteria_agree_in_number_and_differ_in_ground() -> None:
    """ق-ب وق-ج يتّفقان في العدد ويفترقان في السند — والجدولُ يُظهِر ذلك.

    ولا يُميّزهما «الجردُ اللازم» وحدَه؛ يُميّزهما عمودُ الثمن. فمن قرأ
    العددَ وحدَه ظنّهما واحدًا، والفرقُ بينهما **مدخلٌ مفقودٌ** في أحدهما.
    """

    separating = CONSEQUENCE.separating_columns(
        "ق-ب مولَّدٌ بالقواعد المُعلَنة", "ق-ج مقبولٌ عند النطق"
    )
    assert "الجردُ اللازم" not in separating
    assert "ثمنُ اختياره" in separating
    assert CONSEQUENCE.indistinguishable_rows() == ()


def test_the_decision_is_pending_and_the_session_may_not_sign_it() -> None:
    """السلطةُ مرفوضةٌ في المُنشئ: لو وقّعتُ لسقط البناءُ عند الإنشاء."""

    assert PENDING.standing is Standing.PENDING
    for forged in ("الجلسة", "claude", "Claude", "المساعد"):
        with pytest.raises(DecisionError):
            Register(
                decisions=(
                    Decision(
                        identifier=PENDING.identifier,
                        question=PENDING.question,
                        blocks=PENDING.blocks,
                        branches=PENDING.branches,
                        standing=Standing.TAKEN,
                        chosen_branch="ق-أ مشهودٌ في المصحف",
                        authority=forged,
                        decided_on=__import__("datetime").date(2026, 9, 23),
                    ),
                ),
                refused_authorities=REGISTER.refused_authorities,
            )


def test_nothing_that_rests_on_it_may_be_reported_as_done() -> None:
    """ما يحجبه القرارُ يُرَدّ إعلانُ تمامه **باسم حاجبه** لا بصمت."""

    for blocked in PENDING.blocks:
        with pytest.raises(DecisionError) as raised:
            REGISTER.assert_not_reportable_as_done(blocked)
        assert PENDING.identifier in str(raised.value)

    # وما لا يحجبه يمرّ
    REGISTER.assert_not_reportable_as_done("محوّلُ ميلي: ٢١ حالةً و٤٤٦ مدخلًا")


def test_every_branch_carries_a_written_price() -> None:
    """لا فرعَ مجّانيّ: الاختيارُ مبادلةٌ تُعلَن لا تفضيلٌ يُذاع."""

    assert len(PENDING.branches) == 3
    for branch in PENDING.branches:
        assert len(branch.price) > 20
    prices = {branch.price for branch in PENDING.branches}
    assert len(prices) == 3  # ولا ثمنَ مكرَّرٌ يُخفي فرقًا


def test_the_register_digest_changes_if_a_branch_is_edited() -> None:
    """بصمةُ السجلّ تتغيّر بتبديل فرعٍ، فلا يُستبدَل ثمنٌ بعد النظر صمتًا."""

    before = REGISTER.digest()
    softened = Register(
        decisions=(
            Decision(
                identifier=PENDING.identifier,
                question=PENDING.question,
                blocks=PENDING.blocks,
                branches=(
                    PENDING.branches[0],
                    PENDING.branches[1],
                    Branch(
                        label="ق-ج مقبولٌ عند النطق",
                        effect="الجردُ خمسة",
                        price="لا ثمنَ يُذكَر — وهذا بعينه ما يُرَدّ",
                    ),
                ),
            ),
        ),
        refused_authorities=REGISTER.refused_authorities,
    )
    assert softened.digest() != before
