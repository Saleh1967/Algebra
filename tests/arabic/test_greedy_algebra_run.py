"""شُغِّل ختمُ `cfdb2184…`: **سبعةٌ من ثمانية — والانقلابُ مُفسَّرٌ باشتقاق**.

`THE_INVERSION_IS_NOW_DERIVED_NOT_MERELY_OBSERVED`: ب٣ وب٤ صمدا معًا،
وهما متقابلان: `ρ(الوقوعِ الخام، الربح) = **+٠٫١٨٠٥**` بينما
`ρ(الربحِ المشتَقِّ بالتباديل، الربح) = **+٠٫٩٧٥٩**`. **فالعددُ الخامُ
يكاد لا يقول شيئًا عن الربح، والصيغةُ المشتقّةُ تقوله كلَّه.**

`AND_THE_FORMULA_IS_PERMUTATIONS_NOT_ANALOGY`: التكلفةُ **لوغاريتمُ عدد
التباديل المتمايزة**، والربحُ نسبةُ معاملين:
`G = log₂ N⁽ᵐ⁾ − log₂ nₐ⁽ᵐ⁾ − log₂ n_b⁽ᵐ⁾ + log₂ m!`. وتقريبُها الأوّلُ
`m·(PMI − log₂ e)` يتبع المقيسَ بـ`+٠٫٩٦٥٥` — **فالانقلابُ من الضرب في
`PMI` لا من شيءٍ آخر**، و`ρ(الوقوع، PMI) = +٠٫١٨٧٢` فحسب.

`AND_THE_LICENSING_THRESHOLD_IS_log2_e`: وب٦ صمد: عتبةُ `PMI > log₂ e`
(**١٫٤٤٢٧**) توافق إشارةَ الربح في **١٩٠ من ٢٠٠** — ٠٫٩٥٠٠. **فرخصةُ
الدمج حدٌّ على فائض الاقتران، لا على العدد.**

`AND_THE_IDENTITY_IS_EXACT`: وب١ صمد إلى آخر رقم: `|I − Σ p·PMI| = ٠`
تمامًا — فالمستخرَجُ بالدمج **هو بعينه** `I(Xₜ;Xₜ₊₁)`، لا ما يشبهه.

`BUT_THE_ASCENT_REACHES_PAST_ORDER_ONE`: وب٨ **منقوضٌ، وهو خبرٌ لا عطل**:
وفّر الصعودُ **٨٢٤٬٦١٨** بتًّا وسقفُ الرتبة الأولى **٤٦٧٬٣٥٥** —
النسبةُ **١٫٧٦٤٤**. فالدمجُ المتكرّرُ **لا يسعه اقترانُ الجارين**: الرموزُ
المدموجةُ تمتدّ، فيلتقط جوارُها رتبًا أبعد.

`AND_THE_INEQUALITY_HELD_UP_THE_LADDER`: وب٢ صمد: `log₂ التباديل ≤ N·H`
عند الحالات كلِّها، والفرقُ للرمز **يتّسع** بنموّ الأبجديّة
(`+٠٫٠٠١٩٦٩` عند L₀ إلى `+٠٫٠٥٩٤٨٢` بعد ٢٬٠٠٠) — وهو حدُّ ستيرلنغ،
`induction on` مُصانةً و`induction FOR` شاهدةً عليها.
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from test_greedy_algebra_seal import DIGEST, ORACLE, PREDICTIONS, SAVED

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "greedy_algebra_run.log"
HUFFMAN = REPOSITORY / "deposits" / "huffman_ascent_run.log"

BY_COUNT = 0.1805
BY_DERIVED = 0.9759
BY_LEADING = 0.9655
BY_PMI = 0.9221
COUNT_PMI = 0.1872
SIGN = Fraction(187, 200)
THRESHOLD = Fraction(190, 200)
MEDIAN_ERROR = 0.1997
CARRIED = 1.303600
PLACES = 358_511
CEILING = 467_355
RATIO = 1.7644
LOG2E = 1.4427


# **سقفُ كلّ شرطٍ محدود** — العطل ٢٦.
CEILINGS: dict[str, tuple[Fraction, str]] = {
    "ب٤": (
        Fraction(1),
        "معاملُ الارتباط لا يفوق الواحدَ مبرهنةً",
    ),
    "ب٦": (
        Fraction(1),
        "نسبةٌ تامّة: كلُّ ما في المقام يقبل الدخولَ في البسط، فلا ممتنعَ فيه",
    ),
}


def _one(identifier: str) -> object:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def _grab(pattern: str) -> str:
    found = re.search(pattern, LOG.read_text(encoding="utf-8"), re.MULTILINE)
    assert found is not None, pattern
    return found.group(1)


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("cfdb2184")


def test_the_mutual_information_identity_is_exact() -> None:
    """ب١: `Σ p·PMI` هي `I` إلى آخر رقم — لا ما يشبهها."""

    apart = float(_grab(r"\|I − Σ p·PMI\| = ([\d.]+)"))
    assert _one("ب١").verdict(_exact(apart)) is Verdict.MET  # type: ignore[attr-defined]
    assert apart == 0.0
    assert abs(float(_grab(r"I\(Xₜ;Xₜ₊₁\) = ([\d.]+)")) - CARRIED) < 5e-7
    assert abs(float(_grab(r"Σ p·PMI    = ([\d.]+)")) - CARRIED) < 5e-7


def test_the_counting_bound_held_at_every_state() -> None:
    """ب٢: `log₂ التباديل ≤ N·H` — والفرقُ يتّسع بنموّ الأبجديّة."""

    drifts = [
        float(one) for one in re.findall(r"للرمز \+([\d.]+)", LOG.read_text("utf-8"))
    ]
    assert drifts and min(drifts) > 0
    assert _one("ب٢").verdict(_exact(min(drifts))) is Verdict.MET  # type: ignore[attr-defined]
    assert drifts == sorted(drifts)  # فيتّسع ولا ينكمش — حدُّ ستيرلنغ
    laid = float(_grab(r"تباديل متعدّد المجموعة: ([\d.]+)"))
    by_entropy = float(_grab(r"N·H بالإنتروبيا:\s+([\d.]+)"))
    assert by_entropy > laid


def test_the_raw_count_barely_predicts_the_gain() -> None:
    """ب٣: `+٠٫١٨٠٥` — والعددُ الخامُ ليس وكيلًا عن الربح."""

    measured = float(_grab(r"ρ\(الوقوع، الربحِ المقيس\)\s+= \+([\d.]+)"))
    assert _one("ب٣").verdict(_exact(measured)) is Verdict.MET  # type: ignore[attr-defined]
    assert abs(measured - BY_COUNT) < 5e-5


def test_the_derived_formula_tracks_the_measured_gain() -> None:
    """ب٤: `+٠٫٩٧٥٩` — والتباديلُ ليست تشبيهًا بل تكلفةَ هذا البناء."""

    measured = float(_grab(r"ρ\(المشتَقّ، الربحِ المقيس\)\s+= \+([\d.]+)"))
    assert _one("ب٤").verdict(_exact(measured)) is Verdict.MET  # type: ignore[attr-defined]
    assert abs(measured - BY_DERIVED) < 5e-5
    leading = float(_grab(r"ρ\(التقريبِ، الربحِ المقيس\) = \+([\d.]+)"))
    assert abs(leading - BY_LEADING) < 5e-5
    assert leading > BY_COUNT  # فالتقريبُ وحدَه يسبق العددَ بفارقٍ بعيد


def test_the_coupling_beats_the_count_by_a_wide_margin() -> None:
    """ب٥: `+٠٫٩٢٢١` مقابلَ `+٠٫١٨٠٥` — والفرقُ `+٠٫٧٤١٦`."""

    coupling = float(_grab(r"ρ\(PMI، الربحِ المقيس\)\s+= \+([\d.]+)"))
    count = float(_grab(r"ρ\(الوقوع، الربحِ المقيس\)\s+= \+([\d.]+)"))
    assert _one("ب٥").verdict(_exact(coupling - count)) is Verdict.MET  # type: ignore[attr-defined]
    assert abs(coupling - BY_PMI) < 5e-5
    assert abs((coupling - count) - 0.7416) < 5e-5
    together = float(_grab(r"ρ\(الوقوع، PMI\)\s+= \+([\d.]+)"))
    assert abs(together - COUNT_PMI) < 5e-5
    assert together < 0.2  # فالعددُ والاقترانُ شبه مستقلَّين، وثَمَّ الانقلاب


def test_the_threshold_is_log_two_e() -> None:
    """ب٦: `PMI > log₂e` توافق إشارةَ الربح في ١٩٠ من ٢٠٠."""

    assert _one("ب٦").verdict(THRESHOLD) is Verdict.MET  # type: ignore[attr-defined]
    text = LOG.read_text(encoding="utf-8")
    assert f"عتبةُ PMI > log₂e ({LOG2E:.4f}): توافقٌ 190 من 200 = 0.9500" in text
    assert _one("ب٦").verdict(SIGN) is Verdict.MET  # type: ignore[attr-defined]


def test_the_derivation_estimates_and_not_only_orders() -> None:
    """ب٧: وسيطُ الخطأ النسبيّ `٠٫١٩٩٧` — فهي تُقدّر لا ترتّب فحسب."""

    median = float(_grab(r"وسيطٌ ([\d.]+) \| أدنى"))
    assert _one("ب٧").verdict(_exact(median)) is Verdict.MET  # type: ignore[attr-defined]
    assert abs(median - MEDIAN_ERROR) < 5e-5
    edge = float(_grab(r"المئينُ ٩٠ ([\d.]+)"))
    assert edge > median  # والذيلُ ثقيلٌ، ويُقال


def test_the_ascent_reaches_past_first_order_and_that_is_news() -> None:
    """ب٨ منقوضٌ: ١٫٧٦٤٤ — فالدمجُ لا يسعه اقترانُ الجارين."""

    assert _one("ب٨").verdict(_exact(RATIO)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    assert SAVED == 824_618
    assert abs(SAVED / CEILING - RATIO) < 5e-5
    assert abs(PLACES * CARRIED - CEILING) < 1.0
    assert "ما فوق الرتبة الأولى" in _one("ب٨").falsifies  # type: ignore[attr-defined]


def test_the_published_block_figures_come_from_the_deposit() -> None:
    """أرقامُ الصعود الكتليّ تُقرأ من سجلّه لا من الذاكرة."""

    text = HUFFMAN.read_text(encoding="utf-8")
    assert "ملحَقة 2044336" in text
    assert "معجم 163822" in text and "ملحَقة 1383540" in text
    assert (2_044_336 - 0) - (1_383_540 - 163_822) == SAVED


def test_seven_of_eight_and_the_one_that_fell_is_named() -> None:
    """الجردُ صريحٌ، ولا يُعاد تفسيرُ شرطٍ بعد رقمه."""

    met = {"ب١", "ب٢", "ب٣", "ب٤", "ب٥", "ب٦", "ب٧"}
    fell = {"ب٨"}
    assert met | fell == {one.identifier for one in PREDICTIONS}  # type: ignore[attr-defined]
    assert len(met) == 7 and not met & fell


def test_the_paper_is_regenerated_from_the_log_and_never_typed() -> None:
    """وثيقةُ جبر الربح تُبنى من السجلّ — فمقارنتُها به مطابقةٌ تامّة."""

    import importlib.util

    paper = REPOSITORY / "docs" / "جبر-الربح.md"
    tool = REPOSITORY / "tools" / "write_algebra_paper.py"
    spec = importlib.util.spec_from_file_location("write_algebra_paper", tool)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.render() == paper.read_text(encoding="utf-8")
    written = paper.read_text(encoding="utf-8")
    assert "**خبرٌ لا عطل**" in written
    assert "مقياسان لا مقياس" in written


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ **مرّت** وتعليلُها المكتوبُ معها **لم يُؤيَّد بالقياس** — إن وُجِدت.

فشرطٌ يمرُّ بتعليلٍ خاطئ **ليس تأييدًا**: العددُ صحيحٌ والسببُ المنسوبُ إليه
غيرُ مقيس. وهذا الاسمُ **مطلوبٌ في كلّ تشغيل** وإن كان فارغًا، كي يُسأل
السؤالُ في كلّ مرّة ولا يُطوى بالسكوت — وهو العطلُ الثامن.
"""
