"""تشغيلُ الختمين: الإظهارُ المطلق تحقّق تامًّا، وقراءةُ التكرار **سقطت بوّابتُها**.

**ترتيبُ العمل مثبتٌ في تاريخ git**: أُودِع الختمان في دفعةٍ لا رقمَ فيها،
وهذه الدفعةُ تشغيلُهما. فالتسجيلُ سبق القياسَ بشهادةٍ خارجةٍ عن دعوايَ.

`THE_GATE_I_WROTE_AGAINST_MYSELF_FIRED`: وأهمُّ ما خرج **سقوطُ ص٢**. كنتُ
كتبتُ: وسمٌ عشوائيٌّ بالعدد نفسِه على مواضع النون نفسِها يجب ألّا يبلغ
مؤشّرُه ٠٫١٠، وإلّا فالمؤشّرُ يقيس **كثرةَ الوسم لا موافقتَه**. فبلغ
**٠٫٢١٢٥**. وحكمُ ص١ — وقد جاوز حدَّه (٠٫٤٩٤٤ فوق ٠٫٤٠) — **غيرُ مقروءٍ
بنصّ ما سجّلتُه**، ولا أُعيد تفسيرَ الشرط بعد أن رأيتُ الرقم.

`WHAT_MAY_STILL_BE_SAID_IS_SAID_APART`: ويبقى وصفٌ يُنشَر **خارجَ الختم**:
المرصودُ ٠٫٤٩٤٤ وأعلى ألفي صفريٍّ عشوائيٍّ ٠٫٢١٢٥، فلم يبلغه واحدٌ منها.
وذلك خبرٌ عن كون المرصود **فوق الكثرة وحدَها**، وليس هو الشرطَ الذي كُتِب.

`THE_SHARP_PREDICTION_CAME_OUT_AT_ITS_CEILING`: وط١ تنبّأ بأنّ **تسعين
بالمئة فأكثر** من مواضع الواو والياء بعد النون الساكنة داخلَ الكلمة. فخرجت
**مئةٌ في المئة**: مئةٌ وخمسةٌ وعشرون موضعًا، **ولا واحدَ يعبر حدَّ الكلمة**.

`AND_THE_FOUR_WORDS_NAMED_BEFORE_THE_COUNT_COVER_IT_ENTIRELY`: وسُمِّيت
أربعةُ ألفاظٍ قبل العدّ — دنيا، بنيان، قنوان، صنوان — فغطّت **المواضعَ
كلَّها** بلا بقيّة: ١١٥ في «الدنيا»، و٧ في «بنيان» وصوره، و٢ في «صنوان»،
وواحدٌ في «قنوان». ولم يقع موضعٌ واحدٌ خارجها.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

from frozen_corpus import requires_corpus

from algebra.signified import Verdict

REPOSITORY = Path(__file__).resolve().parents[2]

pytestmark = requires_corpus

NUN_SEAL = "85f59f23c39d3ded9d459a332c7df7587f13891d7e54d4fdad40f63dfb51a160"
IZHAR_SEAL = "57ac0f3852debdaff5164c78add3e623f982025b2ee6239d046f41e723ecc499"

HELD_OUT_RAND = Fraction(4_944, 10_000)
HIGHEST_RANDOM_MARKING = Fraction(2_125, 10_000)
TOP_FIVE = "هخعحغ"
JUNCTIONS_BY_HALF = (1_098, 618)

RESIDUE_INSIDE, RESIDUE_ACROSS = 125, 0
CARRIERS: tuple[tuple[str, int], ...] = (
    ("الدنيا", 115),
    ("بنيانه", 2),
    ("بنيانهم", 2),
    ("بنيانا", 2),
    ("صنوان", 2),
    ("بنيان", 1),
    ("قنوان", 1),
)


def _prediction(identifier: str):
    import importlib.util
    import sys

    path = REPOSITORY / "tests" / "algebra"
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
    module_name = (
        "test_nun_replication_preregistration"
        if identifier.startswith("ص")
        else "test_izhar_mutlaq_preregistration"
    )
    spec = importlib.util.spec_from_file_location(
        module_name, path / f"{module_name}.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    for one in module.PREDICTIONS:
        if one.identifier.startswith(identifier):
            return one
    raise AssertionError(identifier)


def test_the_readability_gate_fell_and_it_was_written_against_myself() -> None:
    """ص٢ بلغ ٠٫٢١٢٥ والحدُّ ٠٫١٠ «لا يجاوز» — فسقط، وأسقط قراءةَ ص١."""

    second = _prediction("ص٢")
    assert second.verdict(HIGHEST_RANDOM_MARKING) is Verdict.FALSIFIED
    assert second.verdict(Fraction(9, 100)) is Verdict.MET
    assert "كثرةَ الوسم لا موافقتَه" in second.falsifies


def test_the_first_condition_passed_its_own_bar_and_is_still_not_readable() -> None:
    """٠٫٤٩٤٤ فوق ٠٫٤٠ — ومع ذلك لا يُقرَأ، لأنّ بوّابتَه سقطت بنصّها."""

    first = _prediction("ص١")
    assert first.verdict(HELD_OUT_RAND) is Verdict.MET
    assert HELD_OUT_RAND > first.threshold

    # ولا يُعاد تفسيرُ ص٢ بعد رؤية رقمه: الحكمُ يبقى «غيرُ مقروء»
    gate = _prediction("ص٢")
    assert gate.verdict(HIGHEST_RANDOM_MARKING) is not Verdict.MET


def test_the_observed_still_exceeds_every_random_marking_drawn() -> None:
    """وصفٌ خارجَ الختم: لم يبلغ المرصودَ واحدٌ من ألفي صفريّ."""

    assert HELD_OUT_RAND > HIGHEST_RANDOM_MARKING
    assert HELD_OUT_RAND / HIGHEST_RANDOM_MARKING > Fraction(2)
    # وهو خبرٌ عن تجاوز الكثرة، لا الشرطُ الذي كُتِب — والفرقُ يُكتَب لا يُطوى


def test_the_other_three_conditions_were_met() -> None:
    """ص٣ خمسةٌ من الإظهار في أعلى خمسة، وص٤ أقلُّ نصفٍ ٦١٨، وص٥ مصدرٌ واحد."""

    assert len(TOP_FIVE) == 5
    assert _prediction("ص٣").verdict(Fraction(5)) is Verdict.MET
    assert _prediction("ص٤").verdict(Fraction(min(JUNCTIONS_BY_HALF))) is Verdict.MET
    assert _prediction("ص٥").verdict(Fraction(1)) is Verdict.MET

    assert sum(JUNCTIONS_BY_HALF) == 1_716
    assert min(JUNCTIONS_BY_HALF) == 618


def test_the_absolute_izhar_prediction_came_out_at_its_ceiling() -> None:
    """مئةٌ وخمسةٌ وعشرون موضعًا، كلُّها داخلَ الكلمة، ولا واحدَ يعبر."""

    first = _prediction("ط١")
    total = RESIDUE_INSIDE + RESIDUE_ACROSS
    assert total == 125
    assert RESIDUE_ACROSS == 0

    share = Fraction(RESIDUE_INSIDE, total)
    assert share == 1
    assert first.verdict(share) is Verdict.MET
    assert first.threshold == Fraction(90, 100)


def test_the_four_named_words_cover_every_site_without_residue() -> None:
    """الأربعةُ المُسمّاةُ قبل العدّ تغطّي المواضعَ كلَّها — ولا خامسَ ظهر."""

    assert sum(count for _, count in CARRIERS) == RESIDUE_INSIDE
    roots = {"دنيا", "بنيان", "قنوان", "صنوان"}
    for shape, _ in CARRIERS:
        assert any(root in shape or shape in f"ال{root}" for root in roots), shape

    assert dict(CARRIERS)["الدنيا"] == 115
    assert len(CARRIERS) == 7  # سبعُ صورٍ لأربعة أصول
