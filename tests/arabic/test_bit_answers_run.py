"""شُغِّل ختمُ `ec24c73f…`: **سبعةٌ من سبعة، والمجالُ عُدَّ كلُّه**.

`THE_DOMAIN_WAS_COUNTED_NOT_SAMPLED`: بُنِي **٢٬٠٤٨** سؤالًا — ثمانيةُ
أسماءٍ × ٢٥٦ بايتة — **ولم يُترَك منها واحد**. فالأرقامُ ههنا تعدادٌ تامٌّ
على مجالٍ متناهٍ، لا استقراءٌ من عيّنة. **وحدُّها معها**: بايتةٌ واحدةٌ
موضوعًا، ولا يُقال منها شيءٌ عن بايتتين.

`AND_THE_REFUSALS_ARE_THE_LARGER_HALF`: **٢٥٦** أُجيب عنها، و**١٬٢٨٠**
رُدَّت `NOT_ANSWERABLE_YET` — اسمٌ في المفردات بلا مُجيبٍ بعدُ — و**٥١٢**
رُدَّت `UNSUPPORTED_QUESTION`. **فثمانيةُ أعشار ما سُئِل لم يُجَب عنه،
وكلُّ ردٍّ منه مُصنَّفٌ باسمه**. وهذا ما تشتريه المفرداتُ المغلقة: أنّ
«لم أُجِب» حكمٌ يُقرَأ، لا صمتٌ يُفسَّر.

`AND_THE_CHECKER_IS_NOT_THE_COMPUTER`: عُرِض كلُّ جوابٍ على `audit` الذي
يبسط البايتةَ بصيغةٍ مكتوبةٍ ويقصُّ الصدرَ من اليسار — **طريقٌ غيرُ طريق
الحساب** — فجاءت الشكاوى **صفرًا**. ولو اتّفق الطريقان على خطأٍ لمرَّ؛
والمانعُ أنّهما لا يشتركان في خطوةٍ واحدة.

`AND_THE_ANSWER_COSTS_MORE_THAN_IT_TELLS`: ب٥ صمد: **لا جوابَ واحدٌ** ثمنُه
دون قيمته أو مساويًا لها. وأكبرُ ثمنٍ **٢٤** وأصغرُه **١٦**، ومجموعُ
الأثمان **٥٬٨٨٩** بتًّا — بإزاء قيمٍ لا تجاوز الثمانية. **فالحسابُ يستهلك
أكثرَ ممّا يُخبر**، وذلك معدودٌ في الخطوات لا مُقدَّرٌ بصيغة.

`AND_THE_COUNT_MATCHES_THE_IDENTITY_EXACTLY`: توزيعُ الأجوبة طابق
`٢^(ك−١)` في كلّ خانةٍ — **صفرُ خانةٍ مخالفة**. وذلك متطابقةٌ **معدودةٌ**
على المجال كلِّه، لا مقيسةٌ على عيّنة.

**وما لا يُقال**: لا تعلّمَ في هذا التشغيل ولا اقتراح. وواحدةٌ من ستّ
مفرداتٍ بُنِي لها مُجيب، **والخمسُ مؤجَّلاتٌ مُصنَّفاتٌ لا مطويّات**.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

from test_bit_answers_seal import DIGEST, ORACLE, PREDICTIONS, WHOLE

from algebra.asking import ANSWERED_TODAY, Question, Status, audit
from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "bit_answers.log"
EXAMPLE = REPOSITORY / "examples" / "kernel" / "run_bit_answers.py"

ASKED = 2_048
GIVEN = 256
DEFERRED = 1_280
UNSUPPORTED = 512
COMPLAINTS = 0
DEAREST = 24
CHEAPEST = 16
PAID = 5_889
DRIFT = 0
POSTPONED = 5


def _one(identifier: str) -> object:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _text() -> str:
    return LOG.read_text(encoding="utf-8")


def _measured() -> dict[str, int]:
    """تُعاد الأرقامُ **حسابًا في الجلسة** لا قراءةً من السجلّ وحدَه.

    وهذا ما يفرّق هذا التشغيلَ عن تشغيلات المدوّنة: مادّتُه **مولَّدةٌ
    بالكامل**، فلا يحتاج بايتاتٍ من خارج الشجرة، **ويُعاد عند كلّ أحد**.
    """

    import sys

    sys.path.insert(0, str(REPOSITORY / "examples" / "kernel"))
    from run_bit_answers import OUTSIDE, answered, asked

    asks = asked()
    found = answered(asks)
    given = [one for one in found if one.status is Status.ANSWERED]
    widths: dict[int, int] = {}
    for one in given:
        widths[int(one.value)] = widths.get(int(one.value), 0) + 1
    expected = {0: 1} | {one: 2 ** (one - 1) for one in range(1, 9)}
    return {
        "asked": len(asks),
        "given": len(given),
        "deferred": sum(1 for one in found if one.status is Status.NOT_ANSWERABLE_YET),
        "unsupported": sum(
            1 for one in found if one.status is Status.UNSUPPORTED_QUESTION
        ),
        "complaints": sum(len(audit(one)) for one in found),
        "astray": sum(
            1
            for one in found
            if (one.ask.kind in OUTSIDE) != (one.status is Status.UNSUPPORTED_QUESTION)
        ),
        "cheap": sum(1 for one in given if one.cost_bits <= int(one.value)),
        "dearest": max(one.cost_bits for one in given),
        "cheapest": min(one.cost_bits for one in given),
        "paid": sum(one.cost_bits for one in given),
        "drift": sum(1 for one, many in expected.items() if widths.get(one, 0) != many),
        "postponed": len(Question) - len(ANSWERED_TODAY),
    }


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("ec24c73f")


def test_the_closed_grammar_was_enumerated_whole() -> None:
    """ب١: ٢٬٠٤٨ سؤالًا — ثمانيةُ أسماءٍ × ٢٥٦ موضوعًا، بلا اختيار."""

    found = _measured()
    assert _one("ب١").verdict(Fraction(abs(found["asked"] - WHOLE))) is Verdict.MET  # type: ignore[attr-defined]
    assert found["asked"] == ASKED == WHOLE
    assert f"الأسئلةُ المولَّدة {ASKED}" in _text()
    assert found["given"] == GIVEN
    assert found["deferred"] == DEFERRED
    assert found["unsupported"] == UNSUPPORTED
    assert GIVEN + DEFERRED + UNSUPPORTED == ASKED
    assert f"ANSWERED {GIVEN}" in _text()
    assert f"NOT_ANSWERABLE_YET {DEFERRED}" in _text()
    assert f"UNSUPPORTED_QUESTION {UNSUPPORTED}" in _text()


def test_an_independent_checker_reread_every_trace_and_complained_of_nothing() -> None:
    """ب٢: صفرُ شكوى — والمُتحقِّقُ لا يستدعي حاسبَه ولا يشاركه خطوة."""

    found = _measured()
    assert _one("ب٢").verdict(Fraction(found["complaints"])) is Verdict.MET  # type: ignore[attr-defined]
    assert found["complaints"] == COMPLAINTS
    assert f"شكاوى المُتحقِّق المستقلّ {COMPLAINTS}" in _text()


def test_every_refusal_landed_in_its_own_door() -> None:
    """ب٣: صفرُ ردٍّ في غير بابه — وخارجُ المفردات يُعرَف بردّه."""

    found = _measured()
    assert _one("ب٣").verdict(Fraction(found["astray"])) is Verdict.MET  # type: ignore[attr-defined]
    assert found["astray"] == 0
    assert "ردٌّ في غير بابه 0" in _text()


def test_the_complete_count_matches_the_identity_in_every_cell() -> None:
    """ب٤: `٢^(ك−١)` معدودةً على المجال كلِّه — صفرُ خانةٍ مخالفة."""

    found = _measured()
    assert _one("ب٤").verdict(Fraction(found["drift"])) is Verdict.MET  # type: ignore[attr-defined]
    assert found["drift"] == DRIFT
    assert "خانةٌ خالفت ٢^(ك−١) 0" in _text()
    assert "قيمةٌ 8 | مواضيعُ 128 | المنتظَرُ 128" in _text()


def test_no_answer_was_cheaper_than_what_it_told() -> None:
    """ب٥: صفرُ جوابٍ ثمنُه دون قيمته — والثمنُ معدودٌ في الخطوات."""

    found = _measured()
    assert _one("ب٥").verdict(Fraction(found["cheap"])) is Verdict.MET  # type: ignore[attr-defined]
    assert found["cheap"] == 0
    assert "أجوبةٌ ثمنُها لا يجاوز قيمتَها 0" in _text()


def test_the_dearest_answer_stays_under_the_structural_ceiling() -> None:
    """ب٦: أكبرُ ثمنٍ ٢٤ — وهو سقفُ البناء نفسُه (٨ + ٨ + ٨)."""

    found = _measured()
    assert _one("ب٦").verdict(Fraction(found["dearest"])) is Verdict.MET  # type: ignore[attr-defined]
    assert found["dearest"] == DEAREST == 8 + 8 + 8
    assert found["cheapest"] == CHEAPEST
    assert found["paid"] == PAID
    assert f"أكبرُ ثمنٍ {DEAREST} | أصغرُ ثمنٍ {CHEAPEST} | مجموعُ الأثمان {PAID}" in _text()


def test_the_postponed_vocabulary_is_counted_and_bounded() -> None:
    """ب٧: خمسُ مفرداتٍ مؤجَّلةٌ من ستّ — معدودةً ومكتوبةً لا مطويّة."""

    found = _measured()
    assert _one("ب٧").verdict(Fraction(found["postponed"])) is Verdict.MET  # type: ignore[attr-defined]
    assert found["postponed"] == POSTPONED
    assert len(Question) - len(ANSWERED_TODAY) == POSTPONED
    assert "المفرداتُ 6 | المُجابُ عنه اليومَ 1" in _text()


def test_seven_of_seven_and_none_fell() -> None:
    """الجردُ صريحٌ، ولا يُعاد تفسيرُ شرطٍ بعد رقمه."""

    met = {"ب١", "ب٢", "ب٣", "ب٤", "ب٥", "ب٦", "ب٧"}
    assert met == {one.identifier for one in PREDICTIONS}
    assert len(met) == 7


def test_the_deposited_log_is_what_this_session_recomputes() -> None:
    """السجلُّ المُودَعُ ليس شاهدًا على غائب: يُعاد توليدُه ههنا ويُقابَل سطرًا سطرًا.

    ومادّةُ هذا التشغيل **مولَّدةٌ بالكامل**، فلا عذرَ له في أن يُقرَأ ولا
    يُعاد — بخلاف تشغيلات المدوّنة التي تحتاج بايتاتٍ من خارج الشجرة.
    """

    import subprocess
    import sys

    finished = subprocess.run(  # noqa: S603
        [sys.executable, str(EXAMPLE)],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=REPOSITORY,
    )
    assert finished.returncode == 0, finished.stderr[-600:]
    assert finished.stdout == _text()


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ **مرّت** وتعليلُها المكتوبُ معها **لم يُؤيَّد بالقياس** — إن وُجِدت.

وههنا **خالية**: كلُّ شرطٍ مرّ، وتعليلُه المكتوبُ في الختم مقيسٌ في متن
التشغيل نفسِه — العددُ والتوزيعُ والثمنُ والشكوى كلُّها تُعاد في الجلسة.
والاسمُ **مطلوبٌ في كلّ تشغيل** وإن كان فارغًا، كي يُسأل السؤالُ في كلّ
مرّةٍ ولا يُطوى بالسكوت — وهو العطلُ الثامن.
"""
