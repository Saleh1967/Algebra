"""شُغِّل ختمُ `0b8eae76…`: **ثلاثةٌ من أربعة — والفجوةُ في العريض لا الكتلة**.

`MY_OWN_CLAIM_FELL`: ف٢ كان **دعوايَ**: «الفجوةُ حيث الكتلةُ لا حيث كثرةُ
المفاصل»، واشترطتُ للعَرضين ٢ و٣ نصفَ العابرات فأكثر. **والمقيسُ ٠٫٢٥٥٩** —
أي أنّهما يحملان **رُبعَ** العبور وهما **نصفُ** الوقوعات تقريبًا
(٤٨٬٥٪). **فالفجوةُ في الرموز العريضة**، ويُنشَر ذلك بلا تجميل كما نصّ
الشرط.

`THE_RATE_CLIMBS_AND_THEN_LOCKS_AT_ONE`: وف٣ صمد: المعدّلُ **يطّرد** في
الثماني الأولى (أدنى فرقٍ **+٠٫٠٠٦٢**). وأحدُّ ما خرج **ليس في الشرط**:

| العَرض | معدّلُ العبور |
|---|---|
| ١ | **٠٫٠٠٠٠** |
| ٢ | ٠٫٠٤٠٩ |
| ٣ | ٠٫١٣٥٨ |
| ٥ | ٠٫٢٢٢٨ |
| ٧ | ٠٫٦١٨٨ |
| ٩ | ٠٫٨٥٠٩ |
| **١٠ فأكثر** | **١٫٠٠٠٠** |

**فمن العَرض عشرةٍ فصاعدًا يعبر كلُّ رمزٍ بلا استثناء** — ثلاثٌ وعشرون
مجموعةً متتاليةً معدّلُها واحدٌ صحيح. **وهو حدٌّ لا تدريج**، ويحمل
**٠٫١٨٤٠** من العبور.

`AND_THE_STRUCTURAL_ZERO_IS_EXACTLY_ZERO`: وف٤ صمد: العَرضُ ١ **صفرٌ
لازمٌ بالبناء** لا نادرٌ بالرصد — رمزٌ بوحدةٍ واحدةٍ لا جَوفَ له يُشقّ
بفراغ. **ويُنشَر لازمًا لا مرصودًا**، فالفرقُ بينهما أنّ الأوّلَ لا يُنقَض
بعيّنةٍ أكبر.

`AND_THE_PARTITION_IS_EXACT`: وف١ صمد: مجموعُ القسمة **١٧٬٩٨٩** يطابق
الجملةَ (١١٠٬٩٩٤ − ٩٣٬٠٠٥) **بلا بقيّةٍ واحدة**.

`AND_THE_TWO_NUMBERS_STAY_TWO`: والنصيبُ غيرُ المعدّل: العَرضُ ٢ **أكبرُ
المجموعات وقوعًا** (٢٨٬٥٦٣) و**أدناها معدّلًا** (٠٫٠٤٠٩)؛ والعَرضُ ٢٢
**معدّلُه واحدٌ صحيح** ونصيبُه **٠٫٠٠٧٠**. فخلطُهما كان سيُخرِج حكمين
متناقضين من صفٍّ واحد.
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from frozen_corpus import requires_corpus
from test_crossing_census_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "huffman_ascent_run.log"

pytestmark = requires_corpus

CROSSING = 17_989
CLEAN = 93_005
SEEN = 110_994
TWO_AND_THREE = 4_603
TEN_UP = 3_310
LOCKED_FROM = 10
LOCKED_GROUPS = 23


def _rows() -> list[tuple[int, int, int, float, float]]:
    text = LOG.read_text(encoding="utf-8")
    found = re.findall(
        r"^    عَرضُ (\d+): عابرٌ (\d+) من (\d+) \| نصيبٌ ([\d.]+) \| معدّلٌ ([\d.]+)$",
        text,
        re.MULTILINE,
    )
    return [(int(a), int(b), int(c), float(d), float(e)) for a, b, c, d, e in found]


def test_the_seal_was_deposited_before_the_census() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("0b8eae76")


def test_the_partition_closes_on_the_published_total() -> None:
    """ف١: ١٧٬٩٨٩ = ١١٠٬٩٩٤ − ٩٣٬٠٠٥ بلا بقيّة."""

    rows = _rows()
    assert sum(one for _, one, _, _, _ in rows) == CROSSING
    assert SEEN - CLEAN == CROSSING
    assert sum(one for _, _, one, _, _ in rows) == SEEN
    first = next(one for one in PREDICTIONS if one.identifier == "ف١")
    assert first.verdict(Fraction(0)) is Verdict.MET


def test_my_claim_that_the_gap_sits_in_the_mass_is_withdrawn() -> None:
    """ف٢: ٠٫٢٥٥٩ دون النصف — فالفجوةُ في العريض لا الكتلة."""

    rows = _rows()
    narrow = sum(one for width, one, _, _, _ in rows if width in {2, 3})
    assert narrow == TWO_AND_THREE
    share = Fraction(narrow, CROSSING)
    second = next(one for one in PREDICTIONS if one.identifier == "ف٢")
    assert second.verdict(share) is Verdict.FALSIFIED
    assert abs(float(share) - 0.2559) < 5e-5
    # وهما نصفُ الوقوعات تقريبًا وربعُ العبور
    mass = sum(one for width, _, one, _, _ in rows if width in {2, 3})
    assert Fraction(mass, SEEN) > Fraction(48, 100)


def test_the_rate_climbs_over_the_first_eight_widths() -> None:
    """ف٣: أدنى فرقٍ +٠٫٠٠٦٢ — فالاطّرادُ قائم."""

    rows = [one for one in _rows() if one[0] <= 8]
    steps = [b[4] - a[4] for a, b in zip(rows, rows[1:])]
    third = next(one for one in PREDICTIONS if one.identifier == "ف٣")
    assert third.verdict(Fraction(int(min(steps) * 10_000), 10_000)) is Verdict.MET
    assert abs(min(steps) - 0.0062) < 5e-5


def test_the_rate_locks_at_one_from_width_ten_upward() -> None:
    """ثلاثٌ وعشرون مجموعةً متتاليةً معدّلُها واحدٌ صحيح — حدٌّ لا تدريج."""

    rows = _rows()
    locked = [width for width, _, _, _, rate in rows if rate == 1.0]
    assert min(locked) == LOCKED_FROM
    assert len(locked) == LOCKED_GROUPS
    assert all(rate < 1.0 for width, _, _, _, rate in rows if width < LOCKED_FROM)
    wide = sum(one for width, one, _, _, _ in rows if width >= LOCKED_FROM)
    assert wide == TEN_UP
    assert abs(wide / CROSSING - 0.1840) < 5e-5


def test_the_structural_zero_is_published_as_necessary_not_observed() -> None:
    """ف٤: العَرضُ ١ صفرٌ لازمٌ بالبناء — لا يُنقَض بعيّنةٍ أكبر."""

    rows = _rows()
    single = next(one for one in rows if one[0] == 1)
    assert single[1] == 0 and single[4] == 0.0
    fourth = next(one for one in PREDICTIONS if one.identifier == "ف٤")
    assert fourth.verdict(Fraction(0)) is Verdict.MET
    assert "ممتنعٌ بالبناء" in fourth.falsifies


def test_the_share_and_the_rate_disagree_by_design() -> None:
    """العَرضُ ٢ أكبرُ وقوعًا وأدنى معدّلًا — وخلطُهما يُخرِج حكمين متناقضين."""

    rows = _rows()
    widest_mass = max(rows, key=lambda one: one[2])
    assert widest_mass[0] == 2
    lowest_rate = min((one for one in rows if one[0] > 1), key=lambda one: one[4])
    assert lowest_rate[0] == 2
    twenty_two = next(one for one in rows if one[0] == 22)
    assert twenty_two[4] == 1.0 and twenty_two[3] < 0.01


FELL_WITH_THEM: dict[str, str] = {
    "ف٢": "دعوايَ أنّ الفجوةَ تقع حيث الكتلةُ لا حيث",
}
"""ما عُلِّق على سقوط كلِّ شرطٍ، مقتبَسًا من نصّ الختم لا مُعادَ تفسيره.

فنصُّ `falsifies` **دعوًى ثانيةٌ معرَّضةٌ للسقوط** لا شرحًا محايدًا: إن سقط
الشرطُ سقط معه ما عُلِّق عليه، ويُعلَن ذلك **عند موضع السقوط** لا في شرحٍ
لاحق. وهو العطلُ الثاني عشر، ممنوعًا آليًّا.
"""


def test_what_fell_with_each_fallen_condition_is_quoted_where_it_fell() -> None:
    """كلُّ منقوضٍ يحمل نصَّ ما سقط معه، مطابقًا لنصّ الختم بايتةً."""

    for identifier, meaning in FELL_WITH_THEM.items():
        found = next(one for one in PREDICTIONS if one.identifier == identifier)
        assert meaning in found.falsifies, identifier
        assert len(meaning) >= 10


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ **مرّت** وتعليلُها المكتوبُ معها **لم يُؤيَّد بالقياس** — إن وُجِدت.

فشرطٌ يمرُّ بتعليلٍ خاطئ **ليس تأييدًا**: العددُ صحيحٌ والسببُ المنسوبُ إليه
غيرُ مقيس. وهذا الاسمُ **مطلوبٌ في كلّ تشغيل** وإن كان فارغًا، كي يُسأل
السؤالُ في كلّ مرّة ولا يُطوى بالسكوت — وهو العطلُ الثامن.
"""
