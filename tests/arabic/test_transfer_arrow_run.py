"""شُغِّل ختمُ `4289fc6c…`: **أحدَ عشرَ من اثني عشر — والساقطُ عطلٌ فيّ**.

`THE_LETTER_LEADS_THE_STATE_AND_NOT_THE_OTHER_WAY`: ظ٥ صمد.
`T(ر ⟶ ح)` محجوزًا **+٠٫٠٩٥٧٣٦** بتًّا، و`T(ح ⟶ ر)` **+٠٫٠٢٠٢٢٢**.
وبالتسوية بإنتروبيا الهدف: **٠٫٠٣٦٦٧٢** مقابلَ **٠٫٠٠٥٥٠٧** — **ستّةُ
أضعافٍ وثلاثةُ أرباع**. **فمجرى الحرف يُنبئ عن مجرى الحال أكثرَ بكثيرٍ
ممّا يُنبئ الحالُ عن الحرف**، والزيادةُ **بعد طرح ماضي الهدف نفسِه**.

`AND_THERE_IS_AN_ARROW_AND_THE_TWO_CHANNELS_POINT_OPPOSITE_WAYS`: ظ٧
وظ٨ صمدا. `T(ر ⟶ ح)` أمامًا **+٠٫٠٩٥٧٣٦** ومقلوبًا **+٠٫٠٣٨١٩٠** —
فرقٌ **+٠٫٠٥٧٥٤٦** **يُفضِّل الأمام**. و`T(ح ⟶ ر)` أمامًا **+٠٫٠٢٠٢٢٢**
ومقلوبًا **+٠٫٠٥٣٢٩٤** — **يُفضِّل الخلف**. **فالقناتان سهماهما
متعاكسان**، وهذا أقوى ممّا سألتُ عنه.

`AND_THE_SELF_CHANNEL_IS_TIME_SYMMETRIC_AS_IT_MUST_BE`: و`ح ⟵ ح`
محجوزًا **أمامًا ومقلوبًا سواءً بسواء** — `٠٫٠٦٤٢٧٧` في الحالين. **وهذا
ليس نتيجةً بل فحصُ آلة**: معلوماتُ زوجٍ متجاورٍ **متناظرة**، فلو اختلفتا
لكان في الحساب عطل.

`AND_ALL_FOUR_STAND_FAR_ABOVE_A_SHUFFLED_NULL`: ظ٦ صمد. الصفريُّ
المُبدَّلُ **سالبٌ في المقاييس الأربعة كلِّها** (وذاك أثرُ التنعيم على
شقٍّ محجوز)، وأدنى فضلٍ للمقيس عليه **+٠٫٠٦٠٠٢٢** بتًّا. **فلا واحدٌ منها
في حدود الانحياز.**

`AND_TWO_SEALS_MEET_AGAIN`: ظ١١ صمد. `I(حₜ ؛ حₜ₋₁)` محجوزةً ههنا
**٠٫٠٦٤٢٧٧**، والمقيسُ في `494465d1…` **٠٫٠٦٥٣** — بفارقٍ
**٠٫٠٠١٠٢٣** بآلةٍ أخرى وقسمةٍ أخرى وتنعيمٍ آخر.

`AND_THE_ONE_THAT_FELL_IS_A_FLAW_IN_MY_OWN_GAUGE`: ظ١٠ **سقط**: أدنى
(ملحَق − محجوز) **−٠٫٠٢٠٢٠٣**، والمحجوزُ **يعلو الملحَق** في قناة
`ح ⟵ ح`. **والعلّةُ في آلتي لا في المادّة**: تقديري الملحَقُ لتلك القناة
طرح `H(الحال)` المحسوبةَ على **الألفاظ كلِّها** من إنتروبيا شرطيّةٍ
محسوبةٍ على **المواضع التي لها سابق** — و**المسندان مختلفان**
(٧٨٬٢٤٥ مقابلَ ٧٢٬٠٠٩). **فما طُرِح ليس معلوماتٍ متبادلةً على الحقيقة.**

`AND_THE_SAME_FLAW_SHOWS_ITSELF_A_SECOND_TIME`: وأثرُه ظاهرٌ في موضعٍ
ثانٍ: الملحَقُ لتلك القناة **أمامًا ٠٫٠٤٤٠٧٥ ومقلوبًا ٠٫١١٠١٥٣** —
**والمحجوزُ متساوٍ**. فذلك الفرقُ **أثرُ المسند المختلف لا سهمُ زمن**،
**ولا يُقرأ سهمًا**. وسُجِّل عطلًا رابعًا وعشرين.

`AND_THE_JUDGEMENT_WAS_NOT_MOVED_TO_SAVE_IT`: **ولم يُعَد تفسيرُ ظ١٠ بعد
النظر**، ولم يُعَد التشغيلُ بمقياسٍ آخرَ ثمّ يُنشَر مختومًا. **السقوطُ
سقوطٌ**، والعطلُ **يُسمّى بأرقامه**.

`AND_WHAT_IS_STILL_NOT_CLAIMED`: **والنقلُ ليس السببيّة.** لا تدخّلَ في
نصٍّ مجمَّد، **فلا تُشتَقّ سببيّةٌ من ارتباطٍ مهما بلغ** — وهذا مكتوبٌ في
الختم **قبل النظر**، لا عذرًا بعده.
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from frozen_corpus import requires_corpus
from test_transfer_arrow_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "transfer_arrow_run.log"
NEIGHBOUR = REPOSITORY / "deposits" / "arabic_token_run.log"

pytestmark = requires_corpus

LINES = 6_236
TOKENS = 78_245
STATE_BOXES = 8
LETTER_BOXES = 36
STATE_H = 2.6106
LETTER_H = 3.6723
SELF_STATE = 0.064277
TO_STATE = 0.095736
TO_LETTER = 0.020222
BACK_TO_STATE = 0.038190
BACK_TO_LETTER = 0.053294
LEAD = 0.031166
ARROW = 0.057546
ABOVE_NULL = 0.060022
SLACK = -29.785261
THEFT = -0.020203
DECLARATION = "— ما لا يُدَّعى"
FORBIDDEN = (
    "ARABIC",
    "فتحة",
    "ضمّة",
    "كسرة",
    "سكون",
    "تنوين",
    "شدّة",
    "فاعل",
    "مفعول",
    "مبتدأ",
    "إعراب",
    "مرفوع",
    "منصوب",
)


def _one(identifier: str) -> object:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def _grab(pattern: str, where: Path = LOG) -> str:
    (found,) = re.findall(pattern, where.read_text(encoding="utf-8"))
    return str(found)


def _gauges() -> dict[str, tuple[float, float, float, float]]:
    """المقياس ⟶ (ملحَقٌ أمامًا، محجوزٌ أمامًا، ملحَقٌ مقلوبًا، محجوزٌ مقلوبًا)."""

    found = re.findall(
        r"^   (\S+)\s+([+-][\d.]+)\s+([+-][\d.]+)\s+([+-][\d.]+)\s+([+-][\d.]+)$",
        LOG.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    return {one: (float(a), float(b), float(c), float(d)) for one, a, b, c, d in found}


def _nulls() -> dict[str, tuple[float, float, float, float]]:
    """المقياس ⟶ (وسطُ الصفريّ، أدناه، أقصاه، المقيس)."""

    found = re.findall(
        r"^   (\S+)\s+وسطٌ ([+-][\d.]+) \| مجالٌ \[([+-][\d.]+) , ([+-][\d.]+)\]"
        r" \| المقيسُ ([+-][\d.]+)$",
        LOG.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    return {one: (float(a), float(b), float(c), float(d)) for one, a, b, c, d in found}


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("4289fc6c")


def test_the_machine_conditions_hold_under_the_corrected_token_bound() -> None:
    """ظ١ وظ٢: الأسطرُ ٦٬٢٣٦ والألفاظُ ٧٨٬٢٤٥ — ولا يُعاد العطل ٢٣."""

    assert int(_grab(r"— الأسطر: (\d+)")) == LINES
    both = re.findall(
        r"— الألفاظ: (\d+) \| وعبرَ العدّادات (\d+)", LOG.read_text("utf-8")
    )
    assert both == [(str(TOKENS), str(TOKENS))]
    assert _one("ظ١").verdict(Fraction(0)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ظ٢").verdict(Fraction(0)) is Verdict.MET  # type: ignore[attr-defined]
    for label, boxes, height in (
        ("الحال", STATE_BOXES, STATE_H),
        ("الحرف", LETTER_BOXES, LETTER_H),
    ):
        count, value = re.findall(
            rf"— خاناتُ {label}: (\d+) \| H = ([\d.]+)", LOG.read_text("utf-8")
        )[0]
        assert int(count) == boxes and abs(float(value) - height) < 5e-5


def test_the_two_proven_bounds_hold() -> None:
    """ظ٣ وظ٤: المعلوماتُ غيرُ سالبة، والتباديلُ دون N·H بعد ألف."""

    lowest = float(_grab(r"أدنى مقياسٍ ملحَق: (\S+)"))
    slack = float(_grab(r"أقصى \(log₂ التباديل − N·H\) بعد ألف = (\S+)"))
    assert _one("ظ٣").verdict(_exact(lowest)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ظ٤").verdict(_exact(slack)) is Verdict.MET  # type: ignore[attr-defined]
    assert lowest > 0 and abs(slack - SLACK) < 5e-7
    gauges = _gauges()
    assert len(gauges) == 4
    assert all(one >= 0 for row in gauges.values() for one in row)


def test_the_letter_leads_the_state_by_almost_seven_to_one() -> None:
    """ظ٥ صمد: ٠٫٠٣٦٦٧٢ مقابلَ ٠٫٠٠٥٥٠٧ بعد التسوية — والزيادةُ بعد الطرح."""

    to_state = float(_grab(r"نصيبُ «ر⟶ح» من H\(ح\): ([\d.]+)"))
    to_letter = float(_grab(r"نصيبُ «ح⟶ر» من H\(ر\): ([\d.]+)"))
    lead = float(_grab(r"الفرقُ \(القيادة\): (\S+)"))
    assert abs(lead - LEAD) < 5e-7
    assert abs((to_state - to_letter) - lead) < 2e-6  # جمعُ تقريبين
    assert _one("ظ٥").verdict(_exact(lead)) is Verdict.MET  # type: ignore[attr-defined]
    assert to_state / to_letter > 6.5
    gauges = _gauges()
    assert abs(gauges["ر⟶ح"][1] - TO_STATE) < 5e-7
    assert abs(gauges["ح⟶ر"][1] - TO_LETTER) < 5e-7
    assert _one("ظ٩").verdict(_exact(gauges["ر⟶ح"][1])) is Verdict.MET  # type: ignore[attr-defined]
    assert gauges["ر⟶ح"][1] > 9 * _one("ظ٩").threshold  # type: ignore[attr-defined]


def test_the_arrow_exists_and_the_two_channels_point_opposite_ways() -> None:
    """ظ٧ وظ٨: سهمٌ مقدارُه ٠٫٠٥٧٥٤٦ — وقناةٌ تُفضِّل الأمام وأخرى الخلف."""

    arrow = float(_grab(r"أقصى \|أمامًا − مقلوبًا\| محجوزًا: ([\d.]+)"))
    ahead = float(_grab(r"«ر⟶ح» أمامًا − مقلوبًا: (\S+)"))
    assert abs(arrow - ARROW) < 5e-7 and abs(ahead - ARROW) < 5e-7
    assert _one("ظ٧").verdict(_exact(arrow)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ظ٨").verdict(_exact(ahead)) is Verdict.MET  # type: ignore[attr-defined]
    gauges = _gauges()
    assert abs(gauges["ر⟶ح"][3] - BACK_TO_STATE) < 5e-7
    assert abs(gauges["ح⟶ر"][3] - BACK_TO_LETTER) < 5e-7
    assert gauges["ح⟶ر"][3] > gauges["ح⟶ر"][1]  # وهذه تُفضِّل الخلف


def test_the_self_channel_is_time_symmetric_as_the_machine_requires() -> None:
    """`ح ⟵ ح` محجوزًا أمامًا ومقلوبًا سواءً — فحصُ آلةٍ لا نتيجة."""

    gauges = _gauges()
    assert gauges["ح⟵ح"][1] == gauges["ح⟵ح"][3]
    assert abs(gauges["ح⟵ح"][1] - SELF_STATE) < 5e-7
    assert abs(gauges["ر⟵ر"][1] - gauges["ر⟵ر"][3]) < 1e-4  # وكذلك قناةُ الحرف


def test_all_four_stand_far_above_a_shuffled_null() -> None:
    """ظ٦: الصفريُّ سالبٌ في الأربع، وأدنى فضلٍ +٠٫٠٦٠٠٢٢."""

    nulls = _nulls()
    assert len(nulls) == 4
    above = float(_grab(r"أدنى \(المقيس − أعلى الصفريّ\): (\S+)"))
    assert abs(above - ABOVE_NULL) < 5e-7
    assert _one("ظ٦").verdict(_exact(above)) is Verdict.MET  # type: ignore[attr-defined]
    for middle, low, high, measured in nulls.values():
        assert low <= middle <= high
        assert high < 0 < measured  # الصفريُّ سالبٌ والمقيسُ موجب
    gauges = _gauges()
    for name, row in nulls.items():
        assert abs(row[3] - gauges[name][1]) < 5e-7  # والمقيسُ هو المحجوزُ أمامًا


def test_two_seals_meet_on_the_neighbour_information() -> None:
    """ظ١١: ٠٫٠٦٤٢٧٧ ههنا و٠٫٠٦٥٣ في `494465d1…` — بفارقٍ ٠٫٠٠١٠٢٣."""

    mine = _gauges()["ح⟵ح"][1]
    theirs = float(_grab(r"\n  I = ([\d.]+)", NEIGHBOUR))
    apart = abs(mine - theirs)
    assert _one("ظ١١").verdict(_exact(apart)) is Verdict.MET  # type: ignore[attr-defined]
    assert abs(apart - 0.001023) < 5e-6
    assert LOG.read_text(encoding="utf-8").count("494465d1") == 1  # الحدُّ لا الرقم


def test_the_tenth_fell_because_my_own_in_sample_gauge_is_wrong() -> None:
    """ظ١٠ سقط: المحجوزُ يعلو الملحَق — والعلّةُ في آلتي لا في المادّة."""

    theft = float(_grab(r"أدنى \(ملحَق − محجوز\): (\S+)"))
    assert abs(theft - THEFT) < 5e-7
    assert _one("ظ١٠").verdict(_exact(theft)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    gauges = _gauges()
    inside, outside = gauges["ح⟵ح"][0], gauges["ح⟵ح"][1]
    assert outside > inside
    assert abs((inside - outside) - theft) < 2e-6  # جمعُ تقريبين
    assert TOKENS - LINES == 72_009  # والمسندان مختلفان: ٧٨٬٢٤٥ مقابلَ ٧٢٬٠٠٩
    assert gauges["ح⟵ح"][2] > gauges["ح⟵ح"][0]  # وأثرُه ثانيةً في المقلوب
    assert gauges["ح⟵ح"][1] == gauges["ح⟵ح"][3]  # بينما المحجوزُ متساوٍ
    astray = abs(gauges["ح⟵ح"][2] - gauges["ح⟵ح"][0])
    assert abs(astray - 0.066078) < 2e-6  # وقدرُ أثر المسند المختلف
    assert astray > max(
        abs(one[1] - one[3]) for one in gauges.values()
    )  # ويفوق كلَّ سهمٍ محجوزٍ مقيس
    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "والعلّةُ في آلتي لا في المادّة" in text
    assert "ولا يُقرأ سهمًا" in text


def test_no_name_from_outside_the_corpus_entered_the_log() -> None:
    """ظ١٢: لا اسمَ بابٍ ولا علامةٍ ولا يونيكود فوق سطر الإعلان."""

    text = LOG.read_text(encoding="utf-8")
    assert DECLARATION in text
    measured = text.split(DECLARATION)[0]
    leaked = [one for one in FORBIDDEN if one in measured]
    assert not leaked, leaked
    assert _one("ظ١٢").verdict(Fraction(len(leaked))) is Verdict.MET  # type: ignore[attr-defined]
    latin = set(re.findall(r"[A-Za-z]", measured))
    assert latin <= set("HNdlog")
    assert re.search(r"U\+[0-9A-F]{4}", text)  # والشريحةُ بنقطةِ ترميزها


def test_the_transfer_is_not_called_a_cause() -> None:
    """النقلُ ليس السببيّة — والقولُ مكتوبٌ في الختم قبل النظر."""

    text = LOG.read_text(encoding="utf-8")
    assert "النقلُ ليس السببيّة" in text
    assert "فلا تُشتَقّ" in text and "من ارتباطٍ مهما بلغ" in text
    import test_transfer_arrow_seal as sealed

    words = " ".join((sealed.__doc__ or "").split())
    assert "**وهو ليس السببيّة**" in words
    assert "مكتوبٌ قبل النظر" in words
    assert "لا تُشتَقّ من البايتات" in words


def test_eleven_of_twelve_stood_and_the_one_that_fell_is_named() -> None:
    """الحصادُ يُعَدّ ولا يُدَّعى: أحدَ عشرَ صمدت وواحدٌ سقط."""

    fell = {"ظ١٠"}
    stood = {one.identifier for one in PREDICTIONS} - fell
    assert len(stood) == 11 and len(fell) == 1
    assert __doc__ is not None
    assert "أحدَ عشرَ من اثني عشر" in __doc__


FELL_WITH_THEM: dict[str, str] = {
    "ظ١٠": "اتّجاهَ الانتحال: التقديرُ داخلَ العيّنة لا ينزل",
}
"""ما عُلِّق على سقوط الشرط، مقتبَسًا من نصّ الختم لا مُعادَ تفسيره."""


def test_what_fell_with_each_fallen_condition_is_quoted_where_it_fell() -> None:
    """كلُّ منقوضٍ يحمل نصَّ ما سقط معه، مطابقًا لنصّ الختم بايتةً."""

    for identifier, meaning in FELL_WITH_THEM.items():
        found = next(one for one in PREDICTIONS if one.identifier == identifier)
        assert meaning in found.falsifies, identifier
        assert len(meaning) >= 10


REASONING_NOT_SUPPORTED: tuple[str, ...] = ("ظ٧",)
"""ظ٧ **مرَّ ونصُّه لا يحدّد بأيّ تقديرٍ يُحكَم**.

إحصاؤه «أقصى |مقياسٍ أمامًا − مقياسِه مقلوبًا|» **بلا كلمة «محجوزًا»**،
بينما ظ٨ يقولها صراحةً. **وقد حُكِم بالمحجوز** لأنّ الاستخراجَ ينصّ على
أنّ «المحجوزَ هو الحكم». **ولو حُكِم بالملحَق لمرَّ أيضًا** (أقصى فرقٍ
ملحَقٍ ٠٫٠٦٦٠٧٨ في قناة `ح ⟵ ح`) — **لكنّه كان سيمرُّ بعطلٍ لا بخبر**،
إذ ذلك الفرقُ **أثرُ المسند المختلف** لا سهمُ زمن. **فالمرورُ صحيحٌ
والصياغةُ ناقصة**، ويُقال ذلك ولا يُطوى.
"""
