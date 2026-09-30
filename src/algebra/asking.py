"""لغةُ السؤال — **مفرداتٌ مُغلَقة**، وجوابٌ أثرُه معه، ومُتحقِّقٌ مستقلّ.

**ثلاثُ طبقاتٍ لا تُخلَط**، وهذه الوحدةُ في الأوليَين منها:

| الطبقة | ما تفعل | حكمُها |
|---|---|---|
| س١ | تُجيب عن سؤالٍ بإعادة اشتقاقه من بايتات المُدخَل | `DERIVED` |
| س٢ | تُرفق بالجواب أثرًا يُعاد التحقّقُ منه خطوةً خطوة | `PROVED_ON_FINITE_INPUT` |
| س٣ | تُحسِّن اختيارَ القاعدة من أمثلة | `NOT_A_PROOF` |

`A_LEARNER_NEVER_PRODUCES_A_PROOF`: **س٣ لا يُنتِج س٢ أبدًا**، ولا شيءَ منها
في هذه الوحدة. ونموذجٌ يتعلّم من ألفِ مثالٍ يبقى **مُسنَدَ حَدْسٍ** حتّى
يمرَّ جوابُه في `audit`؛ ونسبةُ قبولٍ عاليةٌ **قياسٌ على المُقترِح لا صحّةٌ
لقاعدة**.

`A_CLOSED_VOCABULARY_IS_WHAT_MAKES_A_REFUSAL_EXPLICIT`: أسماءُ الأسئلة
**مُغلَقةٌ ومعدودة**. فما خرج عنها يُردّ `UNSUPPORTED_QUESTION`، **ولا
يُخمَّن**؛ وما دخلها ولم يُبنَ له مُجيبٌ بعدُ يُردّ `NOT_ANSWERABLE_YET`
**مُصنَّفًا لا مسكوتًا عنه**. والفرقُ بين الردّين خبرٌ: الأوّلُ يقول «لا
أعرف هذا السؤال»، والثاني يقول «أعرفه ولم أُجب عنه بعدُ».

`AN_ANSWER_WITHOUT_A_TRACE_IS_A_NUMBER_NOT_A_PROOF`: كلُّ جوابٍ يحمل قيمتَه
وأثرَه وثمنَه بالبتّات وبصمةَ بايتات مُدخَله. و`audit` **يعيد فحصَ الأثر من
غير طريق `answer`**: يبسط البايتةَ بصيغةٍ مكتوبةٍ لا بالقسمة على اثنين، فلو
أخطأت إحدى الطريقتين لم توافقها الأخرى صدفةً.

`THIS_MODULE_CLAIMS_NOTHING_ABOUT_ANY_LANGUAGE`: أسماءُ الأسئلة رموزٌ
لاتينيّةٌ مُغلَقة، ولا تُقرَأ عربيّةً ولا تُدَّعى فهمًا لها.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import Final

from algebra.bits import BYTE_WIDTH, Step, read_bytes

__all__ = [
    "AN_ANSWER_WITHOUT_A_TRACE_IS_A_NUMBER_NOT_A_PROOF_NOTE",
    "ANSWERED_TODAY",
    "A_CLOSED_VOCABULARY_IS_WHAT_MAKES_A_REFUSAL_EXPLICIT_NOTE",
    "A_LEARNER_NEVER_PRODUCES_A_PROOF_NOTE",
    "Answer",
    "Ask",
    "AskError",
    "Question",
    "Status",
    "THIS_MODULE_CLAIMS_NOTHING_ABOUT_ANY_LANGUAGE",
    "answer",
    "audit",
    "vocabulary",
]

THIS_MODULE_CLAIMS_NOTHING_ABOUT_ANY_LANGUAGE: Final[str] = (
    "أسماءُ الأسئلة رموزٌ مُغلَقة؛ ولا تُقرَأ لغةً ولا تُدَّعى فهمًا لها"
)


class AskError(ValueError):
    """رُفض سؤالٌ أو جوابٌ لا يصحّ بناؤه؛ ولا يُحمَل على أقرب مقبول."""


class Question(Enum):
    """مفرداتُ السؤال، **مُغلَقةً ستًّا**: ولا سؤالَ اسمُه «وما رأيُك»."""

    VALUE = "قيمةُ العدد المقروء من البايتات"
    COST_BITS = "كم بتّةً يكلّف العددُ المقروء من البايتات"
    DIVIDES = "هل يقسم العددُ الأوّلُ الثانيَ بلا باقٍ"
    FOLD = "طيُّ مجرى الحالات إلى عددٍ واحد"
    UNFOLD = "فكُّ العدد الواحد فيرجع المجرى بعينه"
    COUNT = "عدُّ الجائزات بالحارس `T(n) = f·T(n−1) + f·b·T(n−2)`"


ANSWERED_TODAY: Final[frozenset[Question]] = frozenset({Question.COST_BITS})
"""ما بُنِي له مُجيبٌ **اليوم** — واحدٌ من ستّة، وأخواتُه مُصنَّفاتٌ لا مطويّات.

وهي أوّلُ خطوةٍ لا آخرَها: نوعُ سؤالٍ واحدٌ بمُتحقِّقٍ مستقلٍّ وتشغيلٍ مختوم،
**فإن مرَّ ذلك في البوّابة أُضيف الثاني**. والخمسةُ الباقيةُ مكتوبةٌ في
المفردات كي **يُرى غيابُ مُجيبها**، ولا يُظَنَّ أنّها لم تخطر.
"""


class Status(Enum):
    """أحكامُ الجواب، مُغلَقةً ثلاثًا: ولا حكمَ اسمُه «تقريبٌ معقول»."""

    ANSWERED = "أُجيب عنه، ومعه أثرُه وثمنُه"
    NOT_ANSWERABLE_YET = "اسمٌ في المفردات لم يُبنَ له مُجيبٌ بعدُ"
    UNSUPPORTED_QUESTION = "اسمٌ خارجَ المفردات — ولا يُخمَّن له جواب"


def vocabulary() -> frozenset[str]:
    """أسماءُ المفردات كما تُكتَب في السؤال — تُشتَقّ ولا تُنسَخ."""

    return frozenset(one.name for one in Question)


@dataclass(frozen=True, slots=True)
class Ask:
    """سؤالٌ: اسمُه كما كُتِب — لا كما فُهِم — وبايتاتُ موضوعه."""

    kind: str
    subject: bytes

    def __post_init__(self) -> None:
        if not self.kind.strip():
            raise AskError("سؤالٌ بلا اسمٍ لا يُردّ ولا يُجاب.")
        if not self.subject:
            raise AskError("سؤالٌ بلا بايتاتٍ لا موضوعَ له.")

    @property
    def digest(self) -> str:
        """بصمةُ بايتات الموضوع — فالجوابُ مقيَّدٌ بما سُئِل عنه بعينه."""

        return hashlib.sha256(self.subject).hexdigest()

    @property
    def named(self) -> Question | None:
        """المفردةُ إن كان الاسمُ منها، وإلّا فلا شيء — ولا تُقرَّب."""

        for one in Question:
            if one.name == self.kind:
                return one
        return None


@dataclass(frozen=True, slots=True)
class Answer:
    """جوابٌ: حالُه، وقيمتُه، وأثرُه، وثمنُه بالبتّات — أو ردٌّ مُصنَّف."""

    ask: Ask
    status: Status
    value: str
    steps: tuple[Step, ...]
    cost_bits: int

    def __post_init__(self) -> None:
        if self.cost_bits < 0:
            raise AskError("ثمنٌ سالبٌ ليس ثمنًا.")
        if self.status is Status.ANSWERED:
            if not self.steps:
                raise AskError("جوابٌ بلا أثرٍ رقمٌ لا يُعاد التحقّقُ منه.")
            if not self.value.strip():
                raise AskError("جوابٌ بلا قيمةٍ لم يُخبر بشيء.")
            if self.cost_bits != sum(one.bits for one in self.steps):
                raise AskError("ثمنٌ لا يساوي مجموعَ خطواته دعوًى ثانية.")
            return
        if self.steps or self.value or self.cost_bits:
            raise AskError("ردٌّ يحمل أثرًا أو قيمةً أو ثمنًا ليس ردًّا.")


def _refusal(ask: Ask, status: Status) -> Answer:
    return Answer(ask=ask, status=status, value="", steps=(), cost_bits=0)


def answer(ask: Ask) -> Answer:
    """أجِب إن كان السؤالُ مبنيًّا له، **وصنِّف الردَّ وإلّا**.

    ولا يُخمَّن ولا يُقرَّب: اسمٌ خارجَ المفردات يُردّ `UNSUPPORTED_QUESTION`،
    واسمٌ فيها بلا مُجيبٍ يُردّ `NOT_ANSWERABLE_YET`.
    """

    named = ask.named
    if named is None:
        return _refusal(ask, Status.UNSUPPORTED_QUESTION)
    if named not in ANSWERED_TODAY:
        return _refusal(ask, Status.NOT_ANSWERABLE_YET)
    read = read_bytes(ask.subject)
    found = read.values[0]
    counting = Step(
        operation="عَدٌّ",
        inputs=(found.written,),
        output=str(found.width),
        bits=found.width,
    )
    steps = (*read.steps, counting)
    return Answer(
        ask=ask,
        status=Status.ANSWERED,
        value=str(found.width),
        steps=steps,
        cost_bits=sum(one.bits for one in steps),
    )


def _spread(one: int) -> str:
    """بسطُ البايتة ثماني بتّاتٍ **بصيغةٍ مكتوبة** — طريقٌ غيرُ طريق `answer`."""

    return format(one, f"0{BYTE_WIDTH}b")


def audit(found: Answer) -> tuple[str, ...]:
    """أعِد فحصَ الجواب **من أثره وحدَه**؛ وما خالف **يُسمّى** ولا يُعَدّ صفرًا.

    ولا تُستدعى `answer` ههنا ولا `read_bytes`: البايتةُ تُبسَط بصيغةٍ
    مكتوبة، وحذفُ الصدر يُعاد بقصٍّ من اليسار، والعدُّ بطولِ ما بقي. فاتّفاقُ
    الطريقين شاهدٌ، واختلافُهما **عطلٌ يُسمّى**.
    """

    said: list[str] = []
    if found.status is not Status.ANSWERED:
        if found.steps or found.value or found.cost_bits:
            said.append("ردٌّ مُصنَّفٌ يحمل أثرًا أو قيمةً أو ثمنًا")
        return tuple(said)
    if found.ask.named not in ANSWERED_TODAY:
        said.append(f"أُجيب عن سؤالٍ لا مُجيبَ له: {found.ask.kind}")
        return tuple(said)
    if len(found.steps) != len(found.ask.subject) + 2:
        said.append(
            f"خطواتٌ {len(found.steps)} وبايتاتٌ {len(found.ask.subject)} — والفرقُ اثنان"
        )
        return tuple(said)
    spread = ""
    for place, (one, step) in enumerate(
        zip(found.ask.subject, found.steps[: len(found.ask.subject)], strict=True)
    ):
        if step.operation != "بايتة":
            said.append(f"خطوةٌ {place} اسمُها {step.operation} لا «بايتة»")
            continue
        if step.inputs != (str(place), str(one)):
            said.append(f"خطوةٌ {place} لا تُسمّي بايتتَها: {step.inputs}")
            continue
        if step.output != _spread(one):
            said.append(f"خطوةٌ {place}: بُسِطت {step.output} والمكتوبُ {_spread(one)}")
            continue
        if step.bits != BYTE_WIDTH:
            said.append(f"خطوةٌ {place}: ثمنُها {step.bits} وعرضُ البايتة {BYTE_WIDTH}")
            continue
        spread += step.output
    trimming = found.steps[-2]
    if trimming.operation != "حذفُ الصدر":
        said.append(f"ما قبلَ الأخيرة اسمُها {trimming.operation} لا «حذفُ الصدر»")
    elif trimming.inputs != (spread,):
        said.append("حذفُ الصدر لا يقرأ ما بسطته البايتات")
    else:
        kept = spread.lstrip("0")
        if trimming.output != (kept if kept else "-"):
            said.append(f"حذفُ الصدر ردَّ {trimming.output} والمقصوصُ {kept or '-'}")
        if trimming.bits != len(spread):
            said.append(f"حذفُ الصدر ثمنُه {trimming.bits} والمبسوطُ {len(spread)}")
    counting = found.steps[-1]
    kept = spread.lstrip("0")
    if counting.operation != "عَدٌّ":
        said.append(f"الأخيرةُ اسمُها {counting.operation} لا «عَدٌّ»")
    else:
        if counting.output != str(len(kept)):
            said.append(f"العدُّ ردَّ {counting.output} والباقي {len(kept)}")
        if counting.bits != len(kept):
            said.append(f"العدُّ ثمنُه {counting.bits} والباقي {len(kept)}")
    if found.value != found.steps[-1].output:
        said.append("القيمةُ المُعلَنةُ ليست مخرَجَ آخرِ خطوة")
    if found.cost_bits != sum(one.bits for one in found.steps):
        said.append("الثمنُ المُعلَنُ ليس مجموعَ الخطوات")
    if found.ask.digest != hashlib.sha256(found.ask.subject).hexdigest():
        said.append("البصمةُ لا تطابق بايتاتِ الموضوع")
    return tuple(said)


A_LEARNER_NEVER_PRODUCES_A_PROOF_NOTE: Final[str] = (
    "ALearnerNeverProducesAProof: طبقةُ التعلّم تقترح ولا تكتب قيمةً في جواب؛ "
    "ونسبةُ قبولها قياسٌ على المُقترِح لا صحّةٌ لقاعدة — "
    "HighAcceptanceRateIsNotCorrectness"
)

A_CLOSED_VOCABULARY_IS_WHAT_MAKES_A_REFUSAL_EXPLICIT_NOTE: Final[str] = (
    "AClosedVocabularyIsWhatMakesARefusalExplicit: ما خرج عن المفردات يُردّ "
    "UNSUPPORTED_QUESTION ولا يُخمَّن، وما دخلها بلا مُجيبٍ يُردّ "
    "NOT_ANSWERABLE_YET مُصنَّفًا؛ وبين الردّين خبرٌ لا لفظ"
)

AN_ANSWER_WITHOUT_A_TRACE_IS_A_NUMBER_NOT_A_PROOF_NOTE: Final[str] = (
    "AnAnswerWithoutATraceIsANumberNotAProof: كلُّ جوابٍ يحمل أثرَه وثمنَه "
    "وبصمةَ مُدخَله، ويُعاد فحصُ الأثر بطريقٍ غيرِ طريق حسابه"
)
