"""شُغِّل ختمُ `c8602c00…`: **ستّةٌ من تسعة — والجوابُ لا، بل بالعكس**.

`THE_QUESTION_WAS_DOES_HUFFMAN_REPRODUCE_THE_GREEDY_ORDER`: والجوابُ
**لا**، ونصًّا: **الأكبرُ ربحًا هو الأوّلُ وقوعًا في ٢٧ حالًا من ١٬٥٣٠ —
٠٫٠١٧٦**. والقاعدتان تلتزمان الزوجَ نفسَه في ٢٨ حالًا — ٠٫٠١٨٣ — فتختلفان
في **١٬٥٠٢** حالًا من ١٬٥٣٠. فت٤ وت٥ **منقوضتان**.

`AND_THE_ORDER_IS_NOT_MERELY_DIFFERENT_BUT_INVERTED`: وليس الاختلافُ
عشوائيًّا: **وسيطُ رتبةِ ما يختاره «أكبرُ ربحًا» هو ٢٢ من ٢٤**، ويقع
**٠٫٤٥٠٠** من اختياراته في الرتبتين ٢٣ و٢٤. و«أوّلُ رابح» يختار الرتبةَ
الأولى في **٠٫٩٩٦٧**. ووسيطُ وقوعِ ما يختاره أكبرُ ربحٍ **٢٣٦** مقابلَ
**٤٠٥** — فالربحُ الأكبرُ في **الأندر**، والعددُ الخامُ ليس وكيلًا عن
الربح بل **يكاد يعاكسه**.

`AND_TAKING_THE_LARGEST_GAIN_EACH_STEP_IS_MUCH_WORSE`: وت٦ منقوضة:
**١٬٤٧٢٬٢٢٣** مقابلَ **١٬٤٠٨٬٥٨١** للضابط — **أغلى ٦٣٬٦٤٢** بتًّا، ويقف
عند **١٬٥٣٠** التزامًا لا ٢٬٣٠٨، ويُبقي **٠٫٥٧٩٠** من الوقوعات عند عَرضِ
واحد. **فالأمثلُ محلّيًّا أضرُّ من الكافي محلّيًّا** — وهو خبرٌ عن الجشع.

`BUT_THE_WINDOW_BINDS_THE_TWO_RULES_UNEQUALLY`: **وهذا حكمٌ عند عمق ٢٤
لا فوقه**. فالمقيسُ أنّ «أكبرَ ربحًا» **يتكدّس عند حافّة النافذة** (٠٫٤٥
في الرتبتين الأخيرتين)، أي أنّ مطلوبَه **خارجَها على الأرجح**؛ بينما
«أوّلُ رابح» يختار الرتبةَ الأولى دائمًا **فلا تمسُّه النافذةُ أصلًا**.
فالعمقُ مُعلَنٌ وواحدٌ للذراعين، **وليس ملزِمًا لهما بالسواء** — ويُقال
ذلك ولا يُترَك للقارئ.

`AND_THE_PROVEN_BOUNDS_HELD_ON_THE_MEASURED_FREQUENCIES`: وت٨ وت٩ صمدتا:
`L − H` في `[+٠٫٠٢٢٢، +٠٫٠٢٣٧]` على نقاط الفحص كلِّها — **فالمبنيُّ شفرةُ
هوفمان فعلًا** على ترددات الحال المقيسة على المُجمَّد، لا شيءٌ يشبهها.
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from test_measured_ranking_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "measured_ranking_run.log"
RANKS = REPOSITORY / "deposits" / "measured_ranking_rank.log"

STATES = 1_530
RANK_AGREE = 27
CHOICE_AGREE = 28
COMMITS = 1_530
TOTAL = 1_472_223
RATIO = 0.7200
CLEAN = 0.9449
SYMBOLS = 1_501
LOW_GAP = 0.0222
HIGH_GAP = 0.0237
BY_CONTROL = 1_408_581
CONTROL_COMMITS = 2_308
BY_BLOCK = 1_394_638


# **سقفُ كلّ شرطٍ محدود** — العطل ٢٦.
CEILINGS: dict[str, tuple[Fraction, str]] = {
    "ت٤": (
        Fraction(1),
        "نسبةٌ تامّة: كلُّ ما في المقام يقبل الدخولَ في البسط، فلا ممتنعَ فيه",
    ),
}


def _one(identifier: str) -> object:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("c8602c00")


def test_the_machine_held_and_the_licence_stayed_per_merge() -> None:
    """ت١ وت٢ وت٣: انحرافٌ صفرٌ، ورجعةٌ صفرٌ، ولا التزامَ بلا نزول."""

    text = LOG.read_text(encoding="utf-8")
    drifts = [float(one) for one in re.findall(r"انحرافٌ ([\d.]+)", text)]
    (back,) = re.findall(r"مواضعُ الخلاف بين بسطِ الرموز ومجرى L₀ = (\d+)", text)
    (rises,) = re.findall(r"التزاماتٌ بفرقٍ غيرِ سالب: (\d+)", text)
    assert drifts and max(drifts) == 0.0
    assert _one("ت١").verdict(_exact(max(drifts))) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ت٢").verdict(Fraction(int(back))) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ت٣").verdict(Fraction(int(rises))) is Verdict.MET  # type: ignore[attr-defined]


def test_huffman_does_not_reproduce_the_greedy_order() -> None:
    """ت٤ منقوضة: ٠٫٠١٧٦ — والعددُ الخامُ ليس وكيلًا عن الربح."""

    rate = Fraction(RANK_AGREE, STATES)
    assert _one("ت٤").verdict(rate) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    assert abs(float(rate) - 0.0176) < 5e-5
    text = LOG.read_text(encoding="utf-8")
    assert f"توافقُ الرتبة الأولى: {RANK_AGREE} من {STATES} = 0.0176" in text


def test_the_two_rules_disagree_in_almost_every_state() -> None:
    """ت٥ منقوضة: ١٬٥٠٢ من ١٬٥٣٠ — فهما مساران لا صياغتان لمسار."""

    apart = STATES - CHOICE_AGREE
    assert _one("ت٥").verdict(Fraction(apart)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    assert apart == 1_502
    assert abs(apart / STATES - 0.9817) < 5e-5


def test_the_order_is_inverted_not_merely_different() -> None:
    """المقيسُ من `measured_ranking_rank.log`: الوسيطُ ٢٢ من ٢٤."""

    text = RANKS.read_text(encoding="utf-8")
    (middle,) = re.findall(r"وسيطُ الرتبة: (\d+)", text)
    assert int(middle) == 22
    pairs = re.findall(r"رتبةُ\s+(\d+):\s+(\d+) حالًا \(([\d.]+)\)", text)
    edge = sum(float(share) for rank, _count, share in pairs[:24] if int(rank) >= 23)
    assert abs(edge - 0.4500) < 5e-4, edge
    (chosen,) = re.findall(r"يختاره «أكبرُ ربحًا»:  وسيطٌ (\d+)", text)
    (payer,) = re.findall(r"يختاره «أوّلُ رابح»:  وسيطٌ (\d+)", text)
    assert int(chosen) == 236 and int(payer) == 405
    assert int(chosen) < int(payer)  # فالربحُ الأكبرُ في الأندر


def test_the_largest_gain_each_step_costs_far_more_overall() -> None:
    """ت٦ منقوضة: +٦٣٬٦٤٢ بتًّا، ووقوفٌ أبكر، وكتلةٌ عند عَرضِ واحد."""

    assert _one("ت٦").verdict(Fraction(TOTAL)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    assert TOTAL - BY_CONTROL == 63_642
    assert COMMITS < CONTROL_COMMITS
    text = LOG.read_text(encoding="utf-8")
    assert f"النسبةُ إلى L₀ {RATIO:.4f}" in text
    assert "عَرضُ 1: رموزٌ 112 | وقوعاتٌ 101946 | نصيبٌ 0.5790" in text
    assert f"الجملة: رموزٌ {SYMBOLS} " in text


def test_the_window_binds_the_two_rules_unequally_and_that_is_said() -> None:
    """الضابطُ يختار الرتبةَ الأولى دائمًا، والمعالَجُ يتكدّس على الحافّة."""

    text = RANKS.read_text(encoding="utf-8")
    (first,) = re.findall(r"«أوّلُ رابح»:\n  رتبةُ  1:\s+(\d+) حالًا", text)
    assert int(first) == 299 and 299 / 300 > 0.99
    assert __doc__ is not None
    assert "يتكدّس عند حافّة النافذة" in __doc__
    assert "وليس ملزِمًا لهما بالسواء" in __doc__


def test_the_block_is_still_not_reached_and_shannon_held() -> None:
    """ت٧ وت٨ وت٩: لم يُبلَغ الكتليُّ، و`L−H` في `[٠، ١)`."""

    assert _one("ت٧").verdict(Fraction(TOTAL)) is Verdict.MET  # type: ignore[attr-defined]
    assert TOTAL > BY_BLOCK
    assert _one("ت٨").verdict(_exact(LOW_GAP)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ت٩").verdict(_exact(HIGH_GAP)) is Verdict.MET  # type: ignore[attr-defined]
    text = LOG.read_text(encoding="utf-8")
    assert f"أدنى L−H +{LOW_GAP:.4f} | أقصى L−H +{HIGH_GAP:.4f}" in text
    gaps = [float(one) for one in re.findall(r"L−H \+([\d.]+)", text)]
    assert gaps and 0.0 <= min(gaps) and max(gaps) < 1.0


def test_six_of_nine_and_the_three_that_fell_are_named() -> None:
    """الجردُ صريحٌ: ما صمد وما سقط، ولا يُعاد تفسيرُ شرطٍ بعد رقمه."""

    met = {"ت١", "ت٢", "ت٣", "ت٧", "ت٨", "ت٩"}
    fell = {"ت٤", "ت٥", "ت٦"}
    assert met | fell == {one.identifier for one in PREDICTIONS}  # type: ignore[attr-defined]
    assert len(met) == 6 and len(fell) == 3
    assert not met & fell


FELL_WITH_THEM: dict[str, str] = {
    "ت٤": "الدعوى المسؤولَ عنها: أنّ هوفمانَ بالتردّد",
    "ت٥": "الصورةَ القويّةَ من الدعوى: أن تكون",
    "ت٦": "أنّ أخذَ أكبرِ ربحٍ في كلّ حالٍ لا يكون",
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


THE_BOUND_BINDS_BOTH_ARMS = False
"""أيَعَضُّ الحدُّ المُعلَنُ (نافذةُ ٢٤) القاعدتين **بالسواء**؟ — والجوابُ: لا.

وهو العطلُ السابعَ عشر بعينه، مقيسًا ههنا لا مُعلَّلًا: «أكبرُ ربحًا» يختار
من **حافّة** النافذة فمطلوبُه على الأرجح **خارجَها**، و«أوّلُ رابح» يختار
الرتبةَ الأولى فلا تمسُّه النافذةُ أصلًا. فالحدُّ **واحدٌ في قيمته، مختلفٌ
في أثره** — وحكمُ ت٦ **عند عمق ٢٤** لا فوقه.
"""

THE_BOUND_EVIDENCE = (
    "وسيطُ رتبةِ ما يختاره «أكبرُ ربحًا» ٢٢ من ٢٤، و٠٫٤٥٠٠ من اختياراته "
    "في الرتبتين ٢٣ و٢٤؛ بينما «أوّلُ رابح» يأخذ الرتبةَ الأولى في "
    "٠٫٩٩٦٧ من الحالات — فنافذةُ ٢٤ تَعَضُّ الأوّلَ ولا تمسُّ الثاني"
)


def test_the_declared_window_is_measured_on_each_rule_not_declared_once() -> None:
    """عَضّةُ النافذة تُقاس **لكلّ قاعدةٍ على حدة** — لا تُعلَن مرّةً للاثنتين."""

    text = RANKS.read_text(encoding="utf-8")
    pairs = re.findall(r"رتبةُ\s+(\d+):\s+(\d+) حالًا \(([\d.]+)\)", text)
    edge = sum(float(share) for rank, _count, share in pairs[:24] if int(rank) >= 23)
    assert abs(edge - 0.4500) < 5e-5
    (middle,) = re.findall(r"وسيطُ الرتبة: (\d+)", text)
    assert int(middle) == 22
    first = float(
        re.findall(r"«أوّلُ رابح»:\n  رتبةُ\s+1:\s+\d+ حالًا \(([\d.]+)\)", text)[0]
    )
    assert abs(first - 0.9967) < 5e-5
    assert THE_BOUND_BINDS_BOTH_ARMS is (abs(first - edge) < 0.01)


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ **مرّت** وتعليلُها المكتوبُ معها **لم يُؤيَّد بالقياس** — إن وُجِدت.

فشرطٌ يمرُّ بتعليلٍ خاطئ **ليس تأييدًا**: العددُ صحيحٌ والسببُ المنسوبُ إليه
غيرُ مقيس. وهذا الاسمُ **مطلوبٌ في كلّ تشغيل** وإن كان فارغًا، كي يُسأل
السؤالُ في كلّ مرّة ولا يُطوى بالسكوت — وهو العطلُ الثامن.
"""
