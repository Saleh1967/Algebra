"""شُغِّل: **الملحَقُ ينزل بلا حدّ، والمحجوزُ يقف عند الرتبة الرابعة**.

**الحصاد**: تسعٌ من اثنتي عشرةَ صمدت، و**ثلاثٌ سقطت** — ض٣ وض٨ وض١٠.

## النمطُ المستنبَط، وهو الحاصلُ الأوّل

| الرتبة | ملحَقة | محجوز | ربحٌ محجوز | فجوةُ الانتحال |
|---|---|---|---|---|
| ٠ | ٢٫٦٢٨٣ | ٢٫٦٢٨٣ | — | ٠٫٠٠٠٠ |
| ١ | ٢٫٤٣٩٥ | ٢٫٤٤٠٧ | **+٠٫١٨٧٦** | ٠٫٠٠١٣ |
| ٢ | ٢٫٣٠١٤ | ٢٫٣١١٦ | +٠٫١٢٩١ | ٠٫٠١٠٢ |
| ٣ | ٢٫١٨٣٨ | ٢٫٢٣٧٦ | +٠٫٠٧٤١ | ٠٫٠٥٣٨ |
| **٤** | ٢٫٠٤٢٠ | **٢٫٢٣٢٧** | +٠٫٠٠٤٩ | ٠٫١٩٠٦ |
| ٥ | ١٫٨٤٧٧ | ٢٫٣٥٢٠ | **−٠٫١١٩٤** | ٠٫٥٠٤٣ |
| ٦ | ١٫٥٧٩٢ | ٢٫٥٩٥٦ | −٠٫٢٤٣٥ | ١٫٠١٦٣ |

`THE_IN_SAMPLE_SAYS_NOTHING_BECAUSE_IT_CANNOT_RISE`: الملحَقةُ تنزل من
**٢٫٦٢٨٣ إلى ١٫٥٧٩٢** ولا ترتفع في رتبةٍ واحدة — **وذلك مبرهَنٌ لا مقيس**
(`H(X|Y,Z) ≤ H(X|Y)`). فقولُ «الرتبةُ الأعلى أخبر» **ملحَقًا فارغٌ
بالبناء**: لا يمكن أن يكذب، فلا يُخبِر.

`AND_THE_HELD_OUT_HAS_A_FLOOR_AT_ORDER_FOUR`: والمحجوزُ يقف: **أدناه
٢٫٢٣٢٧ عند الرابعة**، ويرتفع عند **الخامسة** (ض٥ وض٦ صمدتا معًا، والحدُّ
الأعلى كان خمسًا فوقع عليها بالضبط). **فالسقفُ المادّيُّ للرتبة أربعٌ**،
وما فوقها **انتحالٌ لا مادّة**.

`AND_THE_LAW_IS_IN_THE_GAP_NOT_IN_THE_ENTROPY`: **وفجوةُ الانتحال
(محجوز − ملحَقة) تنمو رتيبًا**، ونسبتُها إلى سابقتها **تضمر إلى ٢**:
٦٤٫٠٦ · ٨٫٠٨ · ٥٫٢٥ · ٣٫٥٤ · ٢٫٦٥ · **٢٫٠٢**. **فالانتحالُ يتضاعف رتبةً
بعد رتبة** في الرتب العُليا، ونسبةُ تضاعفه تهدأ. **وهذا هو القانونُ الذي
يُستنبَط**: ليس «كم يفيد السياقُ» بل **كم يكذب** — والكذبُ مضاعفٌ
والفائدةُ ضامرة.

`AND_THE_GAIN_DECAYS_THEN_COLLAPSES`: ونسبُ الأرباح المتتالية **٠٫٦٨٨ ·
٠٫٥٧٤ · ٠٫٠٦٦**. فالضمورُ **ليس هندسيًّا**: يمشي نحو الثلثين ثمّ **ينهار
عند الرابعة** إلى سبعةٍ بالمئة. **فالرتبةُ الرابعةُ ليست ذروةً بل حدُّ
نفاد**: تشتري ٠٫٠٠٤٩ بتًّا — أي لا شيءَ عمليًّا — ثمّ ينقلب.

## وحاجزُ ستيرلنغ يسبق كلَّ ذلك — وهذا أشدُّ ما خرج

أبجديّةُ الحالات **١٥**، فسياقُ الرتبة `n` فضاؤه `15^n`:

| الرتبة | الفضاء | تكتيلاتٌ > مواضع | يُحسَب أمثلُه دون ٢^٥٠ |
|---|---|---|---|
| ٠ | ١ | لا | نعم |
| **١** | ١٥ | **نعم** (⌊log₂ Bell(15)⌋ = ٣٠) | نعم |
| ٢ | ٢٢٥ | نعم | **لا** |
| ٦ | ١١٬٣٩٠٬٦٢٥ | نعم | لا |

`AND_MEASUREMENT_OUTRUNS_SELECTION`: **فالحاجزُ يقع عند الرتبة الأولى**
— أسبقَ ممّا ختمتُ (ض١١ حدُّها اثنتان فصمدت بهامش). ومن الرتبة **الثانية**
لا يُحسَب أمثلُ تكتيلٍ في `O(k·3^m)`.

**فالنتيجةُ الحاسمة**: الرتبُ التي **تشتري** (٢ و٣ و٤) هي نفسُها الرتبُ
التي **يمتنع فيها اختيارُ تكتيلٍ من المادّة**. **فيُقاس أنّ الرابعةَ خيرٌ،
ولا يُمكِن أن يُبحَث كيف تُكتَّل.** وذلك موضعُ الحاجة إلى **فرضٍ سابقٍ**
— لا زينةً بل **ضرورةَ حسابٍ**: ما لا تُرجِّحه المادّةُ يجب أن يأتي من
خارجها أو لا يأتي.

## وما سقط — وفيه سقوطٌ من نوعٍ جديد

**ض٨ سقطت**: قدَّرتُ ربحَ الرتبة الأولى بثلاثة أعشارٍ فأكثر، **فكان
٠٫١٨٧٦**. فأكبرُ ما يفيده السياقُ أقلُّ ممّا ظننت.

**ض١٠ سقطت**: قدَّرتُ غيرَ المشهود عند السادسة بثلاثة أعشارٍ فأكثر،
**فكان ٠٫٠٧٩٧**. **فالمدوّنةُ أكثفُ ممّا قدَّرت** على هذه القناة —
والانقلابُ ليس من رقّةِ المشهود بل من **تفتّتِ الجدول**: ٣٨٬٨٤١ سياقًا
على ٣٣٢٬٨٣٧ موضعًا، أي **٨٫٦ موضعًا لكلّ سياق**.

`AND_A_SEALED_FALSIFICATION_CLAUSE_CAN_ITSELF_BE_WRONG`: **وض٣ سقطت
سقوطًا من نوعٍ لم يُسجَّل**. ختمتُ أنّ أبجديّةَ الحالات **لا تزيد على
اثنتَي عشرةَ**، وكتبتُ في نصّ سقوطها: «فالتقشيرُ يخلط شيئًا آخر».
**فكانت الأبجديّةُ ١٥ — والتقشيرُ صحيح**: الشدّةُ تتركّب مع كلّ علامةٍ
(`ًّ ٌّ ٍّ َّ ُّ ِّ`) فتزيد ستًّا على التسع. **فالخطأُ في حدِّي لا في
الآلة، ونصُّ السقوط نفسُه كان خاطئًا.**

**ولا يُعاد تفسيرُه** (المادّة ٢): يُسجَّل أنّ الشرطَ سقط، **ويُسجَّل معه
أنّ تعليلَ سقوطه المختومَ كان خطأً** — وذلك **العطل ٣٠**. وسبقُ الرقم
٨ خانةً في `context_ladder` **قناةٌ أخرى**: تلك حالُ **خاتمة اللفظ**،
وهذه حالُ **كلّ موضع رسم**. **ولا يُقابَل الرقمان.**

**وما لا يُدَّعى**: الأرضيّةُ مرفوعةٌ ههنا، **فلا يُقابَل ٢٫٢٣٢٧ بـ٠٫٧٥٣٧**
من سلّم الضبط المُؤرَّض (ذاك ملحَقٌ على ٠٫٤١٨٤ من المواضع، وهذا محجوزٌ على
الكلّ). والقناةُ **حالُ موضع الرسم** — ورتبةُ الانقلاب رتبةُ **هذه
القناة في هذا المجمَّد بهذه القسمة**، لا حدًّا للعربيّة.
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from frozen_corpus import requires_corpus
from test_markov_order_seal import (
    DIGEST,
    ONE_CHANNEL_IS_NOT_A_LANGUAGE,
    ORACLE,
    PREDICTIONS,
    STIRLING_BOUNDS_KNOWLEDGE_NOT_COMPUTATION,
    THE_FLOOR_IS_REMOVED_AND_THAT_IS_THE_POINT,
)

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "markov_order_run.log"

pytestmark = requires_corpus

LINES = 6_236
PLACES = 332_837
ALPHABET = 15
INSIDE = (2.6283, 2.4395, 2.3014, 2.1838, 2.0420, 1.8477, 1.5792)
HELD = (2.6283, 2.4407, 2.3116, 2.2376, 2.2327, 2.3520, 2.5956)
CONTEXTS = (1, 16, 143, 949, 4389, 15002, 38841)
GAINS = (0.1876, 0.1291, 0.0741, 0.0049, -0.1194, -0.2435)
GAPS = (0.0000, 0.0013, 0.0102, 0.0538, 0.1906, 0.5043, 1.0163)
WIDEN_LAST = 2.02
RATIOS = (0.688, 0.574, 0.066)
TURNED = 5
FLOOR_AT = 4
LOWEST = 2.2327
UNSEEN_AT_SIX = 0.0797
TOTAL_GAIN = 0.3956
BELL_FIFTEEN_BITS = 30
FIRST_OVER = 1
LARGEST_FEASIBLE = 1
PER_CONTEXT = 8.6

FELL = ("ض٣", "ض٨", "ض١٠")
REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ مرّت وتعليلُها لم يُؤيَّد بالقياس — **ولا واحدَ ههنا**.

وكلُّ عددٍ يُروى في هذا الشرح له صفٌّ في السجلّ: الفجواتُ ونسبُها وأرباحُ
الرتب كلُّها مطبوعةٌ في جدول «النمط».
"""

CEILINGS: dict[str, tuple[Fraction, str]] = {
    "ض٧": (
        Fraction(183_445, 10_000),
        "ثمنُ لابلاس للموضع أقصاه `log2(n+k)` عند `c = 0`؛ وn ≤ ٣٣٢٬٨٣٧ "
        "وk = ١٥ — فالسقفُ ١٨٫٣٤٤٥. **حدٌّ سليمٌ بعيدٌ، ويُقال**",
    ),
    "ض٨": (
        Fraction(183_445, 10_000),
        "والربحُ فرقُ ثمنين، فلا يفوق أعلى ثمنٍ ممكنٍ للموضع — "
        "**والسقفُ هو هو، بعيدًا كذلك**",
    ),
    "ض١٠": (
        Fraction(1),
        "نصيبٌ تامٌّ من مواضع المحجوز: قد لا يُرَ سياقُ واحدٍ منها — "
        "فلا ممتنعَ في المقام، والسقفُ الواحد",
    ),
}
"""**سقفُ كلّ شرطٍ محدود** — العطل ٢٦."""

FORBIDDEN = ("مبنيّ", "معرب", "فاعل", "مبتدأ", "حرف جرّ", "إعراب")
DECLARATION = "— ما لا يُدَّعى"


def _text() -> str:
    return LOG.read_text(encoding="utf-8")


def _one(identifier: str) -> object:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _grab(pattern: str) -> str:
    found = re.search(pattern, _text(), re.M)
    assert found is not None, pattern
    return found.group(1)


def _rows() -> list[tuple[int, int, float, float, float, float, float]]:
    body = _text().split("ربحٌ محجوز")[1].split("— النمطُ")[0]
    found = re.findall(
        r"^   (\d)   \| *(\d+) \| ([\d.]+) \| ([\d.]+) \| *([\d.]+) "
        r"\| *([\d.]+) \| ([+-][\d.]+)$",
        body,
        re.M,
    )
    assert len(found) == 7, found
    return [
        (int(a), int(b), float(c), float(d), float(e), float(f), float(g))
        for a, b, c, d, e, f, g in found
    ]


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def test_the_seal_is_unchanged() -> None:
    """الختمُ كما دُفِع — ولا يُعاد تفسيرُ شرطٍ بعد رؤية رقمه."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_the_corpus_and_places_hold() -> None:
    """ض١ وض٢: المدوّنةُ هي هي، ومواضعُ الرسم ٣٣٢٬٨٣٧."""

    assert int(_grab(r"^— الأسطر: (\d+) \|")) == LINES
    places = int(_grab(r"مواضعُ الرسم: (\d+)$"))
    assert places == PLACES
    assert _one("ض١").verdict(Fraction(0)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ض٢").verdict(Fraction(places)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_alphabet_condition_fell_and_its_clause_was_wrong() -> None:
    """ض٣ سقطت: الأبجديّةُ ١٥ لا ≤١٢ — **ونصُّ سقوطها المختومُ كان خاطئًا**.

    كتبتُ فيه «فالتقشيرُ يخلط شيئًا آخر»، **والتقشيرُ صحيح**: الشدّةُ
    تتركّب مع كلّ علامةٍ فتزيد ستًّا. **فالخطأُ في حدِّي** — ويُسجَّل
    السقوطُ ويُسجَّل خطأُ تعليله، **ولا يُعاد تفسيرُه** (المادّة ٢).
    """

    alphabet = int(_grab(r"^— أبجديّةُ الحالات: (\d+) \|"))
    assert alphabet == ALPHABET
    assert _one("ض٣").verdict(Fraction(alphabet)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    assert "فالتقشيرُ يخلط شيئًا آخر" in _one("ض٣").falsifies  # type: ignore[attr-defined]
    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "**فكانت الأبجديّةُ ١٥ — والتقشيرُ صحيح**" in text
    assert "**فالخطأُ في حدِّي لا في الآلة، ونصُّ السقوط نفسُه كان خاطئًا.**" in text
    assert "**العطل ٣٠**" in text


def test_the_in_sample_falls_monotonically_as_proved() -> None:
    """ض٤: لا رتبةَ ارتفعت فيها الملحَقةُ — وذلك مبرهَنٌ لا مقيس."""

    rose = int(_grab(r"رتباتٌ ارتفعت فيها الملحَقةُ: (\d+)"))
    assert rose == 0
    assert _one("ض٤").verdict(Fraction(rose)) is Verdict.MET  # type: ignore[attr-defined]
    inside = tuple(one[2] for one in _rows())
    assert inside == INSIDE
    assert list(inside) == sorted(inside, reverse=True)
    assert __doc__ is not None
    assert "**ملحَقًا فارغٌ بالبناء**" in " ".join(__doc__.split())


def test_the_held_out_turns_at_order_five_and_floors_at_four() -> None:
    """ض٥ وض٦ وض٧: الانقلابُ عند الخامسة، وأدنى محجوزٍ ٢٫٢٣٢٧ عند الرابعة."""

    turned = int(_grab(r"أوّلُ رتبةٍ ارتفع فيها المحجوز: (\d+)"))
    assert turned == TURNED
    assert _one("ض٥").verdict(Fraction(turned)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ض٦").verdict(Fraction(turned)) is Verdict.MET  # type: ignore[attr-defined]
    lowest = float(_grab(r"أدنى محجوزٍ: ([\d.]+) عند الرتبة"))
    where = int(_grab(r"أدنى محجوزٍ: [\d.]+ عند الرتبة (\d+)"))
    assert (lowest, where) == (LOWEST, FLOOR_AT)
    assert _one("ض٧").verdict(_exact(lowest)) is Verdict.MET  # type: ignore[attr-defined]
    assert tuple(one[4] for one in _rows()) == HELD


def test_the_first_order_gain_fell_below_my_threshold() -> None:
    """ض٨ سقطت: ربحُ الأولى ٠٫١٨٧٦ والحدُّ ٠٫٣٠ — فالسياقُ أقلُّ نفعًا."""

    gain = float(_grab(r"ربحُ الرتبة الأولى محجوزًا: \+([\d.]+)"))
    assert gain == GAINS[0]
    assert _one("ض٨").verdict(_exact(gain)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    assert "أقلُّ ممّا ظننت" in _one("ض٨").falsifies  # type: ignore[attr-defined]


def test_the_third_order_gain_is_thin_as_sealed() -> None:
    """ض٩: ربحُ الثالثة ٠٫٠٧٤١ دون العُشر — والضمورُ مقيسٌ لا موصوف."""

    gain = float(_grab(r"ربحُ الرتبة الثالثة محجوزًا: \+([\d.]+)"))
    assert gain == GAINS[2]
    assert _one("ض٩").verdict(_exact(gain)) is Verdict.MET  # type: ignore[attr-defined]
    assert tuple(one[6] for one in _rows()[1:]) == GAINS


def test_the_sparsity_condition_fell_and_the_cause_is_named() -> None:
    """ض١٠ سقطت: غيرُ المشهود ٠٫٠٧٩٧ لا ≥٠٫٣٠ — **والانقلابُ من التفتّت**."""

    unseen = float(_grab(r"غيرُ المشهود عند السادسة: ([\d.]+)"))
    assert unseen == UNSEEN_AT_SIX
    assert _one("ض١٠").verdict(_exact(unseen)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    assert "أكثفُ ممّا" in _one("ض١٠").falsifies  # type: ignore[attr-defined]
    contexts = tuple(one[1] for one in _rows())
    assert contexts == CONTEXTS
    assert abs(PLACES / contexts[6] - PER_CONTEXT) < 0.05
    assert __doc__ is not None
    assert "**تفتّتِ الجدول**" in " ".join(__doc__.split())


def test_the_overfitting_gap_doubles_and_its_ratio_decays_to_two() -> None:
    """النمطُ: الفجوةُ تنمو رتيبًا، ونسبتُها تضمر إلى ٢٫٠٢ — مقيسًا لا موصوفًا."""

    body = _text().split("— النمطُ")[1].split("— حاجزُ")[0]
    gaps = tuple(float(one) for one in re.findall(r"\| *([\d.]+) \| ", body))
    assert gaps == GAPS
    assert list(gaps) == sorted(gaps)
    widen = [
        float(one) for one in re.findall(r"\| *([\d.]+) \| *[+-]?[\d.]+$", body, re.M)
    ]
    assert widen and abs(widen[-1] - WIDEN_LAST) < 0.005
    assert list(widen) == sorted(widen, reverse=True)
    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "**فالانتحالُ يتضاعف رتبةً بعد رتبة**" in text
    assert "**كم يكذب**" in text


def test_the_gain_decays_then_collapses_at_four() -> None:
    """ونسبُ الأرباح ٠٫٦٨٨ · ٠٫٥٧٤ · ٠٫٠٦٦ — **فالرابعةُ حدُّ نفادٍ لا ذروة**."""

    body = _text().split("— النمطُ")[1].split("— حاجزُ")[0]
    ratios = [float(one) for one in re.findall(r"\| *([\d.]+)$", body, re.M)]
    assert tuple(ratios[:3]) == RATIOS
    assert ratios[2] < ratios[1] / 5
    assert __doc__ is not None
    assert "**ينهار عند الرابعة**" in " ".join(__doc__.split())


def test_stirling_bars_the_search_before_the_gain_is_spent() -> None:
    """ض١١ وض١٢: الحاجزُ عند الأولى، والأمثلُ لا يُحسَب فوقها."""

    over = int(_grab(r"أصغرُ رتبةٍ تفوق تكتيلاتُها المواضعَ: (\d+)"))
    feasible = int(_grab(r"أكبرُ رتبةٍ فضاءُ تكتيلها دون 2\^50: (\d+)"))
    assert (over, feasible) == (FIRST_OVER, LARGEST_FEASIBLE)
    assert _one("ض١١").verdict(Fraction(over)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ض١٢").verdict(Fraction(feasible)) is Verdict.MET  # type: ignore[attr-defined]
    bits = int(_grab(r"^   1   \| +15 \| +(\d+) \|"))
    assert bits == BELL_FIFTEEN_BITS
    assert "حدٌّ على ما تستطيع المادّةُ" in STIRLING_BOUNDS_KNOWLEDGE_NOT_COMPUTATION


def test_measurement_outruns_selection_and_that_is_the_pattern() -> None:
    """الرتبُ التي تشتري هي التي يمتنع فيها اختيارُ تكتيلٍ — وهذا المستنبَط."""

    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "**فيُقاس أنّ الرابعةَ خيرٌ، ولا يُمكِن أن يُبحَث كيف تُكتَّل.**" in text
    assert "**ضرورةَ حسابٍ**" in text
    assert "ما لا تُرجِّحه المادّةُ يجب أن يأتي من خارجها أو لا يأتي" in text
    rows = _rows()
    assert rows[2][6] > 0 and rows[3][6] > 0 and rows[4][6] > 0
    assert FIRST_OVER < 2


def test_the_two_supports_are_not_compared() -> None:
    """ولا يُقابَل ٢٫٢٣٢٧ بـ٠٫٧٥٣٧ — العطل ٢٤، معلَنًا قبل النظر وبعده."""

    assert "٠٫٤١٨٤" in THE_FLOOR_IS_REMOVED_AND_THAT_IS_THE_POINT
    text = _text()
    assert DECLARATION in text
    _, _, owned = text.partition(DECLARATION)
    assert "الأرضيّةُ مرفوعةٌ ههنا" in owned
    assert "محجوزٌ على الكلّ" in owned
    for word in FORBIDDEN:
        assert word not in text.partition(DECLARATION)[0], word


def test_one_channel_is_not_a_language() -> None:
    """ورتبةُ الانقلاب رتبةُ هذه القناة — لا حدًّا للعربيّة."""

    _, _, owned = _text().partition(DECLARATION)
    assert "لا حدًّا للعربيّة" in owned
    assert "لا تُقرَأ حدًّا للعربيّة" in ONE_CHANNEL_IS_NOT_A_LANGUAGE


def test_nine_held_and_three_fell_and_the_ceilings_are_declared() -> None:
    """تسعٌ صمدت وثلاثٌ سقطت، ولكلّ محدودٍ سقفٌ مُصرَّحٌ به."""

    assert len(PREDICTIONS) == 12
    assert FELL == ("ض٣", "ض٨", "ض١٠")
    assert REASONING_NOT_SUPPORTED == ()
    assert set(CEILINGS) == {"ض٧", "ض٨", "ض١٠"}
    for identifier, (ceiling, why) in CEILINGS.items():
        assert _one(identifier).threshold <= ceiling  # type: ignore[attr-defined]
        assert len(why) >= 25
    assert float(_grab(r"ومجموعُ الربح المحجوز إلى أدناه: \+([\d.]+)")) == TOTAL_GAIN
