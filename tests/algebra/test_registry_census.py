"""إحصاءُ ما سُجِّل وما آل إليه: خمسةٌ وعشرون شرطًا، وتسعةٌ لم تُحكَم.

**ما يُحصى ههنا**: الشروطُ المُسجَّلةُ **المودَعةُ في هذا المستودع** لا غير.
وهي أقلُّ ممّا سُجِّل في المشروع كلِّه، لأنّ منه ما لم يصل هذه الشجرة. فالعددُ
أدناه **حدٌّ أدنى محقَّق**، لا حصرًا للمشروع.

`THE_UNJUDGEABLE_ARE_THE_FINDING_NOT_THE_FALSIFIED`: ثلاثةَ عشرَ شرطًا سقطت،
وذلك متوقَّعٌ من تسجيلٍ صادق. والخبرُ في **التسعة التي لم تُحكَم**: ٣٦٪ من
المجموع. ولو حُسِبت النسبةُ على ما أمكن الحكمُ فيه وحدَه لكان الساقطُ
**١٣ من ١٦ = ٨١٪** — وهو رقمٌ آخرُ غيرُ «أربعين بالمئة»، ويُقرأ معه لا بدله.

`EVERY_VOID_HAS_THE_SAME_CAUSE`: التسعةُ المُبطَلةُ ليست تسعَ عللٍ متفرّقة.
كلُّها **مجالٌ لم يُعدَّد**: سياسةٌ لمخرجٍ خامسٍ لم تُعلَن، وعمودُ صنفٍ غيرُ
موجود، ووسمٌ مستقلٌّ مفقود، وقاعدةٌ قِيست في حزمةٍ لا وحدَها، وشرطٌ سقط أساسُه
قبله. فالعيبُ المتكرّرُ في الشيفرة هو **نفسُه** أكبرُ سببٍ لتعذُّر الحكم —
وهذا لا يظهر من عدّ السواقط وحدَه.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.assignment import Assignment
from algebra.reconciliation import Partition, rounds_to

FELL = "ساقط"
HELD = "محقَّق"
VOID = "لم يُحكَم"

# (التسجيل، الشرط، المآل، سببُ تعذُّر الحكم إن وُجد)
REGISTER: tuple[tuple[str, str, str, str], ...] = (
    ("ق مقاييسُ اللغة", "ق-ج١ سلامةُ الحقل", FELL, ""),
    ("ق مقاييسُ اللغة", "ق-ج٢ التلوّث", VOID, "سقط أساسُه قبله"),
    ("ق مقاييسُ اللغة", "ق-ج٣ نوعُ الجذر", VOID, "سقط أساسُه قبله"),
    ("ق مقاييسُ اللغة", "ق-ج٤ الفاء", VOID, "سقط أساسُه قبله"),
    ("السلّمُ المنفَّذ", "ط١ الاسترجاع", FELL, ""),
    ("السلّمُ المنفَّذ", "ط٣ الدقّة", FELL, ""),
    ("السلّمُ المنفَّذ", "ط٥ الجذر", HELD, ""),
    ("الإعرابُ بالحرف — الأوّل", "أ ق١ وحدَها", VOID, "قِيست في حزمةٍ لا وحدَها"),
    ("الإعرابُ بالحرف — الأوّل", "ب البقيّةُ معًا", VOID, "قِيست في حزمةٍ لا وحدَها"),
    ("الإعرابُ بالحرف — الأوّل", "ج المجموعُ النهائيّ", FELL, ""),
    ("الإعرابُ بالحرف — الأوّل", "ج' بندُ الإعلان", HELD, ""),
    ("الرقعةُ — الثاني", "أ' ق٠ وحدَها", FELL, ""),
    ("الرقعةُ — الثاني", "ب' لواحقُ الحرف", FELL, ""),
    ("الرقعةُ — الثاني", "ك١ الممنوعُ من الصرف", FELL, ""),
    ("الرقعةُ — الثاني", "ك٢ ق٤ لا تُنقِص", FELL, ""),
    ("الرقعةُ — الثاني", "ك٣ الكلّيّة", FELL, ""),
    ("الرقعةُ — الثاني", "ك٤ الدقّةُ حيث تُسنَد", FELL, ""),
    ("الرقعةُ — الثاني", "ك٥ التغطية", FELL, ""),
    ("الامتناعُ — الثالث", "أ نصيبُ «لا إعراب»", HELD, ""),
    ("الامتناعُ — الثالث", "ب بلا امتناع", VOID, "سياسةُ المخرج الخامس لم تُعلَن"),
    ("الامتناعُ — الثالث", "ج بإضافة ق٥", FELL, ""),
    ("الامتناعُ — الثالث", "د استردادُ الممنوع", VOID, "عمودُ الصنف غيرُ موجود"),
    ("الامتناعُ — الثالث", "هـ انخفاضُ الثلاثيّ", VOID, "وقع في منطقةٍ لم تُسمَّ"),
    ("الامتناعُ — لي", "و ق٥ المختومة", FELL, ""),
    ("الامتناعُ — لي", "ز ثمنُ ط٧", VOID, "الوسمُ المستقلُّ مفقود"),
)


def _count(outcome: str) -> int:
    return sum(1 for _, _, standing, _ in REGISTER if standing == outcome)


def test_the_register_is_twenty_five_conditions_and_sums_without_residue() -> None:
    """خمسةٌ وعشرون شرطًا: ١٣ ساقطًا و٣ محقَّقةً و٩ لم تُحكَم — بلا بقيّة."""

    assert len(REGISTER) == 25
    parts = (_count(FELL), _count(HELD), _count(VOID))
    assert parts == (13, 3, 9)
    assert Partition(parts=parts, declared_total=25).residue == 0

    names = [f"{book} · {item}" for book, item, _, _ in REGISTER]
    assert len(set(names)) == 25  # ولا شرطَ يُعَدّ مرّتين


def test_the_falsification_share_differs_by_the_denominator_chosen() -> None:
    """١٣ من ٢٥ = ٥٢٪، ومن ١٦ محكومةً = ٨١٪ — والمقامُ يُعلَن مع النسبة."""

    on_all = Fraction(_count(FELL), len(REGISTER))
    judged = len(REGISTER) - _count(VOID)
    on_judged = Fraction(_count(FELL), judged)

    assert judged == 16
    assert rounds_to(on_all, 4) == Fraction("0.52")
    assert rounds_to(on_judged, 4) == Fraction("0.8125")
    assert on_judged > on_all  # والرقمان صادقان، والفرقُ في السؤال لا في العدّ


def test_the_unjudged_are_more_than_a_third_of_what_was_sealed() -> None:
    """تسعةٌ من خمسةٍ وعشرين = ٣٦٪ لم تُحكَم — وهذا أثقلُ من عدّ السواقط."""

    share = Fraction(_count(VOID), len(REGISTER))
    assert rounds_to(share, 4) == Fraction("0.36")
    assert _count(VOID) == _count(HELD) * 3  # تسعةٌ لم تُحكَم مقابلَ ثلاثةٍ محقَّقة


def test_every_unjudged_condition_names_one_missing_enumeration() -> None:
    """لكلّ مُبطَلٍ سببٌ مكتوب، والأسبابُ ستّةٌ من جنسٍ واحد: مجالٌ لم يُعدَّد."""

    reasons = [reason for _, _, standing, reason in REGISTER if standing == VOID]
    assert len(reasons) == 9
    assert all(reason.strip() for reason in reasons)

    distinct = sorted(set(reasons))
    assert len(distinct) == 6  # ستّةُ وجوهٍ لعلّةٍ واحدة
    assert reasons.count("سقط أساسُه قبله") == 3
    assert reasons.count("قِيست في حزمةٍ لا وحدَها") == 2

    # ولا سببَ منها نقصٌ في الحساب: كلُّها نقصٌ في المُدخَل أو في الصياغة
    for reason in distinct:
        assert "حساب" not in reason


def test_the_books_are_a_total_grid_over_outcome() -> None:
    """ستّةُ تسجيلاتٍ × ثلاثةِ مآلاتٍ: جدولٌ تامٌّ، وخانةٌ خاليةٌ تُعلَن ممتنعة."""

    books = tuple(dict.fromkeys(book for book, _, _, _ in REGISTER))
    assert len(books) == 6
    outcomes = (FELL, HELD, VOID)

    tally: dict[tuple[str, str], int] = {}
    for book, _, standing, _ in REGISTER:
        tally[(book, standing)] = tally.get((book, standing), 0) + 1

    grid = Assignment(
        rows=books,
        columns=outcomes,
        cells=tuple(
            (book, outcome, str(tally.get((book, outcome), 0)))
            for book in books
            for outcome in outcomes
        ),
    )
    assert grid.covers_the_grid()
    assert grid.filled == 18

    # التسجيلُ الثاني كلُّه ساقط، ولا محقَّقَ فيه ولا مُبطَل
    assert grid.value_at("الرقعةُ — الثاني", FELL) == "7"
    assert grid.value_at("الرقعةُ — الثاني", HELD) == "0"
    assert grid.value_at("الرقعةُ — الثاني", VOID) == "0"

    # ولا تسجيلَين يتّفق توقيعُهما: لكلّ دفترٍ صورةٌ تخصّه
    assert grid.indistinguishable_rows() == ()
    assert grid.separating_columns("ق مقاييسُ اللغة", "الإعرابُ بالحرف — الأوّل") == (
        HELD,
        VOID,
    )
