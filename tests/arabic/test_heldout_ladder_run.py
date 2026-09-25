"""شُغِّل ختمُ `455167a5…`: **م٣ سقط — وأسحبُ نتيجتي المنشورة في `ca8fd2c`**.

`WHAT_I_PUBLISHED_WAS_PART_ARTEFACT`: نشرتُ أنّ الضبطَ ينزل إلى **٠٫٧٦٥٢**
بتًّا بحرفين، وأنّ «أكثرَ الشكل مُستنتَجٌ لا مُخبِر». والقياسُ المحجوزُ يقول
غيرَ ذلك: عند الرتبة الثانية **١٫٦٢٣٣** — أي **أكثرُ من ضِعف** ما نشرتُ.
والفرقُ **انتحالُ تقديرٍ داخلَ العيّنة**: التوزيعُ كان يُقدَّر من المواضع
نفسِها التي يُقاس عليها. **وهو بعينه العطلُ الذي سمّيتُه في هضبة المدى
البعيد، ثمّ وقعتُ فيه.**

`THE_LADDER_TURNS_AROUND_WHERE_THE_DATA_RUNS_OUT`: والسلّمُ المحجوزُ **لا
يتّصل نزولًا**:

| الرتبة | سلّم | مُبلَّغة | **محجوزة** | نصيبُ المرتدّ |
|---|---|---|---|---|
| ٠ | رسم/فكّ | ١٫٩٥٢٥ | **١٫٩٥٥١** | ٠٫٠٠٠٠ |
| ١ | رسم | ١٫٤٩٦٤ | **١٫٥٦١٩** | ٠٫٠٠٠٤ |
| ١ | فكّ | ١٫١٠٦٦ | **١٫٣١٧٧** | ٠٫٠٠٤٩ |
| ٢ | رسم | ١٫٠٩٩٠ | **١٫٥٩٣٣** | ٠٫٠١٧٩ |
| ٢ | فكّ | ٠٫٧٦٥٢ | **١٫٦٢٣٣** | ٠٫٠٨٢٣ |

فأدنى قيمةٍ صادقةٍ **١٫٣١٧٧ عند الرتبة الأولى**، والرتبةُ الثانيةُ **ترتفع**
— فليست مستوًى أعمقَ بل **موضعَ نفادِ المادّة**.

`SO_CONDITION_THREE_OF_THE_EARLIER_SEAL_STANDS_AFTER_ALL`: وس٣ من ختم
`9034199d…` — «أدنى h ≥ بتٍّ واحد» — **يعود إلى الصمود**: أدنى محجوزةٍ
١٫٣١٧٧ > ١. فحكمي عليه بالسقوط كان **حكمًا على مقدِّرٍ لا على لغة**.

`AND_THE_RECOVERED_SHARE_IS_A_THIRD_NOT_THREE_FIFTHS`: والمصحَّح: حرفٌ واحدٌ
قبلَه يستردّ **٢٠٫١٪**، وقارئٌ متتابعٌ حلّ ما قبلَه يستردّ **٣٢٫٦٪** — لا
٢٣٪ و٦١٪. **وثُلُثا الضبط لا يُستردّان** عند أيّ رتبةٍ تحتملها المادّة.

`THE_MACHINE_CONDITIONS_ALL_HELD`: وم١ (الرتبةُ صفرٌ تتطابق: الفرقُ
٠٫٠٠٢٦ من حدٍّ ٠٫٠١) وم٢ (المحجوزةُ لا تنزل تحت المُبلَّغة: أدنى فرقٍ
٠٫٠٠٢٦) وم٥ (التناقصُ على السند المشترك: ١٫٧٧٠٣ · ١٫١٢٧٧ · ٠٫٨٠٨٣) صمدت.
فالآلةُ سليمةٌ — **والخللُ كان في تفسيري لا في حسابي**.

`AND_THE_FOURTH_DECIMAL_WAS_NEVER_MINE_TO_PUBLISH`: وم٤ صمد (٠٫٠٠٥١ من حدٍّ
٠٫٠٥)، **ويُقرأ قيدًا لا إجازة**: خطأٌ معياريٌّ ٠٫٠٠٥ يعني أنّ **الخانة
الثالثةَ آخرُ ما يُقرأ**. فتُنشَر الأرقامُ من الآن **بخطئها**: ١٫٣١٧٧ ±
٠٫٠٠٥١.

`AND_THE_EARLIER_RECORD_IS_NOT_AMENDED`: و`test_vowel_ladder_run` يبقى كما
كُتِب — **السجلُّ لا يُعدَّل بعد الحدث**؛ وهذا الملفُّ يَنسخه ولا يمحوه.
والمُصحَّحُ في `docs/ما-بُرهن-وما-قِيس.md` وحدَه، لأنّه جردٌ حيٌّ لا سجلُّ
تشغيل.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

from frozen_corpus import CORPUS, requires_corpus
from test_heldout_ladder_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_heldout_ladder.py"

pytestmark = requires_corpus

HELD_OUT = {
    (0, False): 1.9551,
    (0, True): 1.9551,
    (1, False): 1.5619,
    (1, True): 1.3177,
    (2, False): 1.5933,
    (2, True): 1.6233,
}
IN_SAMPLE = {
    (0, False): 1.9525,
    (0, True): 1.9525,
    (1, False): 1.4964,
    (1, True): 1.1066,
    (2, False): 1.0990,
    (2, True): 0.7652,
}
SHARED = (1.7703, 1.1277, 0.8083)
SHARED_POSITIONS = 131_418
ERRORS = {False: 0.0038, True: 0.0051}
WITHDRAWN = "أكثرُ الشكل مُستنتَجٌ لا مُخبِر"


def _exact(measured: float) -> Fraction:
    """كسرٌ مضبوطٌ بلا بترٍ نحو الصفر — والبترُ يُقرِّب الحدَّ خلسة."""

    return Fraction(measured).limit_denominator(10**6)


def _reader() -> object:
    spec = importlib.util.spec_from_file_location("run_heldout_ladder", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _lines() -> list[list[tuple[str, str]]]:
    reader = _reader()
    ladder = reader._ladder()  # type: ignore[attr-defined]
    return ladder.lines_of_units(CORPUS.read_text(encoding="utf-8"))  # type: ignore[attr-defined,no-any-return]


def test_the_seal_is_the_one_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("455167a5")


def test_the_run_reproduces_the_recorded_held_out_ladder() -> None:
    """السلّمُ المحجوزُ يُعادُ اشتقاقُه من الشيفرة لا يُنقَل."""

    reader = _reader()
    lines = _lines()
    for (order, states), expected in HELD_OUT.items():
        measured, _ = reader.held_out(lines, order, states)  # type: ignore[attr-defined]
        assert abs(measured - expected) < 5e-4, (order, states)


def test_condition_three_is_falsified_and_my_published_claim_is_withdrawn() -> None:
    """أدنى محجوزةٍ ١٫٣١٧٧ > ١ — فسقوطُ س٣ كان انتحالًا، والقولُ يُسحَب."""

    third = next(one for one in PREDICTIONS if one.identifier == "م٣")
    lowest = min(HELD_OUT.values())
    assert abs(lowest - 1.3177) < 5e-4
    assert third.verdict(_exact(lowest)) is Verdict.FALSIFIED
    assert "ca8fd2c" in third.falsifies
    superseded = REPOSITORY / "tests" / "arabic" / "test_vowel_ladder_run.py"
    assert WITHDRAWN in superseded.read_text(encoding="utf-8")  # يبقى ولا يُمحى


def test_the_held_out_ladder_turns_around_at_the_second_rung() -> None:
    """الرتبةُ الثانيةُ ترتفع — فهي موضعُ نفادِ المادّة لا مستوًى أعمق."""

    assert HELD_OUT[(2, True)] > HELD_OUT[(1, True)]
    assert HELD_OUT[(2, False)] > HELD_OUT[(1, False)]
    # وفي المُبلَّغة تنزل — والفرقُ بينهما هو الانتحالُ بعينه
    assert IN_SAMPLE[(2, True)] < IN_SAMPLE[(1, True)]
    inflation = HELD_OUT[(2, True)] - IN_SAMPLE[(2, True)]
    assert inflation > 0.85  # أكثرُ من ضِعف


def test_the_machine_conditions_held() -> None:
    """م١ وم٢ وم٥ — فالحسابُ سليمٌ والخللُ كان في التفسير."""

    first = next(one for one in PREDICTIONS if one.identifier == "م١")
    gap = abs(HELD_OUT[(0, False)] - IN_SAMPLE[(0, False)])
    assert first.verdict(_exact(gap)) is Verdict.MET
    second = next(one for one in PREDICTIONS if one.identifier == "م٢")
    worst = min(HELD_OUT[key] - IN_SAMPLE[key] for key in HELD_OUT)
    assert second.verdict(_exact(worst)) is Verdict.MET
    fifth = next(one for one in PREDICTIONS if one.identifier == "م٥")
    steps = [a - b for a, b in zip(SHARED, SHARED[1:])]
    assert fifth.verdict(_exact(min(steps))) is Verdict.MET


def test_the_standard_error_caps_the_published_decimals() -> None:
    """٠٫٠٠٥١ — فالخانةُ الثالثةُ آخرُ ما يُقرأ، وتُنشَر الأرقامُ بخطئها."""

    fourth = next(one for one in PREDICTIONS if one.identifier == "م٤")
    worst = max(ERRORS.values())
    assert abs(worst - 0.0051) < 5e-5
    assert fourth.verdict(_exact(worst)) is Verdict.MET
    assert worst > 1e-4  # فالخانةُ الرابعةُ دون الخطأ


def test_the_recovered_share_is_a_third_not_three_fifths() -> None:
    """٢٠٫١٪ بحرفٍ و٣٢٫٦٪ للقارئ المتتابع — لا ٢٣٪ و٦١٪."""

    base = HELD_OUT[(0, False)]
    by_letter = (base - HELD_OUT[(1, False)]) / base
    by_decoder = (base - HELD_OUT[(1, True)]) / base
    assert abs(by_letter - 0.2011) < 2e-3
    assert abs(by_decoder - 0.3260) < 2e-3
    assert by_decoder < 0.5  # فثُلُثا الضبط لا يُستردّان


def test_the_common_support_ladder_still_descends() -> None:
    """على سندٍ واحدٍ يوجب الشرطُ التناقصَ — وهو واقع."""

    reader = _reader()
    ladder = reader._ladder()  # type: ignore[attr-defined]
    shared = reader.common_support(_lines())  # type: ignore[attr-defined]
    assert len(shared) == SHARED_POSITIONS
    for order, expected in enumerate(SHARED):
        step = ladder.ladder_step(  # type: ignore[attr-defined]
            ladder.contexts(shared, order, with_states=False)  # type: ignore[attr-defined]
        )
        assert abs(step[0] - expected) < 5e-4
        assert abs(step[2] - 1.0) < 1e-9  # ونصيبُ المقروء تامٌّ بالبناء


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ **مرّت** وتعليلُها المكتوبُ معها **لم يُؤيَّد بالقياس** — إن وُجِدت.

فشرطٌ يمرُّ بتعليلٍ خاطئ **ليس تأييدًا**: العددُ صحيحٌ والسببُ المنسوبُ إليه
غيرُ مقيس. وهذا الاسمُ **مطلوبٌ في كلّ تشغيل** وإن كان فارغًا، كي يُسأل
السؤالُ في كلّ مرّة ولا يُطوى بالسكوت — وهو العطلُ الثامن.
"""
