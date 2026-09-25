"""شُغِّل ختمُ `7bf3ccd8…`: **ستّةٌ من سبعة — البنيةُ حقيقيّة، والحسابُ سالب**.

`THE_RULE_DOES_CAPTURE_REAL_STRUCTURE`: ص٤ وص٥ صمدا بفارقٍ بعيد.
الأنواعُ **١٧٬٩٠٩ ⟶ ١٢٬٦٦٨** (ناقصًا **٥٬٢٤١**)، ونصيبُ المرتدّ
**٠٫١٩٧٢ ⟶ ٠٫٠٧٤٤** (ناقصًا **٠٫١٢٢٨**). **فالفصلُ يجمع أصولًا ويقلّل
ما لم يُرَ** — وهذا أثرُ بنيةٍ لا أثرُ تقطيعٍ عشوائيّ.

`BUT_THE_ACCOUNT_COMES_OUT_NEGATIVE`: وص٦ **منقوض** — وهو الشرطُ الذي
أنا مسؤولٌ عنه: الثمنُ المحجوزُ للوحدة **٤٫٣٠١٢** مقابلَ **٤٫٢١١٨**
للفظ، **بزيادة +٠٫٠٨٩٤**.

`AND_THE_REASON_IS_ARITHMETIC_NOT_STRUCTURE`: والسببُ مقسومٌ بلا بقيّة:
الثمنُ **للرمز** ينزل **١٩٫٦٣٣٩ ⟶ ١١٫٣٨٢١** (٠٫٥٧٩٧×)، **وعددُ الرموز**
يرتفع **٧٨٬٢٤٥ ⟶ ١٣٧٬٨٣٤** (١٫٧٦١٦×). وحاصلُهما **١٫٠٢١٢** — فالجملةُ
ترتفع **+٣٢٬٥٨٦** بتًّا (+٢٫١٢٪). **فالقاعدةُ تشتري شفرةً أرخصَ بثمنِ
رموزٍ أكثر، والصفقةُ خاسرةٌ بقليل.**

`SO_THE_RUNG_DOES_NOT_OPEN`: وص٧ صمد: المفصولُ **+٠٫٦٤٦٣** فوق الرمز
المُرخَّص، **فأرخصُ درجةٍ تبقى `م١`** ولا يُعاد فتحُ السلّم المُجمَّد.

`AND_THE_LEVEL_IS_NOT_PROMOTED`: **والمواصفةُ غيرُ موقَّعة**، فحالُ
الكلمة المفردة في `426f7fc8…` يبقى `UNCLASSIFIED` — **وهذا لا يتوقّف على
الرقم أصلًا**: لو نزل الثمنُ لبقي كذلك، فالترقيةُ على **القاعدة** لا على
**قياسها**.

`AND_ACCURACY_WAS_NEVER_MEASURED_AND_IS_NOT_CLAIMED`: **ولا جردَ صحيحًا
قُوبِلت به**، فلا يُقال إنّها تفصل صوابًا ولا خطأً — يُقال **ما فعلت**
و**ما كلّف**.
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from test_separation_rule_seal import (
    BY_SYMBOL,
    BY_TOKEN,
    DIGEST,
    ORACLE,
    PREDICTIONS,
    TOKEN_KINDS,
    TOKEN_MISSING,
)

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "separation_rule_run.log"
RULE = REPOSITORY / "deposits" / "separation_rule.md"
LADDER = REPOSITORY / "tools" / "ladder_seal.py"

TOKENS = 78_245
WORDS = 137_834
KINDS = 12_668
MISSING = 0.0744
OUTSIDE = 4.3012
INSIDE = 3.3209
PER_WORD = 11.3821
PER_TOKEN = 19.6339
CUT = 0.5946


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
    assert DIGEST.startswith("7bf3ccd8")


def test_the_split_is_reversible_and_bounded() -> None:
    """ص١ وص٢: الرجعةُ صفرٌ، و`L − H` تحت الواحد."""

    back = int(_grab(r"ألفاظٌ لا تُستعاد = (\d+)"))
    assert _one("ص١").verdict(Fraction(back)) is Verdict.MET and back == 0  # type: ignore[attr-defined]
    gap = float(_grab(r"L−H \+([\d.]+)"))
    assert _one("ص٢").verdict(_exact(gap)) is Verdict.MET  # type: ignore[attr-defined]
    assert "أطوالٌ مخالفة = 0" in LOG.read_text(encoding="utf-8")


def test_the_rule_touches_most_of_the_corpus() -> None:
    """ص٣: ٠٫٥٩٤٦ من الألفاظ فُصِلت — فالقاعدةُ تفعل شيئًا."""

    share = float(_grab(r"ألفاظٌ فُصِلت: \d+ \(([\d.]+)\)"))
    assert _one("ص٣").verdict(_exact(share)) is Verdict.MET  # type: ignore[attr-defined]
    assert abs(share - CUT) < 5e-5
    assert f"الكلماتُ الناتجة: {WORDS} | أنواعٌ {KINDS}" in LOG.read_text("utf-8")


def test_the_rule_gathers_stems_and_cuts_the_unseen() -> None:
    """ص٤ وص٥: الأنواعُ −٥٬٢٤١، والمرتدُّ −٠٫١٢٢٨ — وهذا أثرُ بنية."""

    assert _one("ص٤").verdict(Fraction(KINDS)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ص٥").verdict(_exact(MISSING)) is Verdict.MET  # type: ignore[attr-defined]
    assert TOKEN_KINDS - KINDS == 5_241
    assert abs((MISSING - TOKEN_MISSING) - -0.1228) < 5e-5


def test_the_account_comes_out_negative_and_that_falsifies_the_sixth() -> None:
    """ص٦ منقوض: ٤٫٣٠١٢ مقابلَ ٤٫٢١١٨ — بزيادة +٠٫٠٨٩٤."""

    assert _one("ص٦").verdict(_exact(OUTSIDE)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    assert abs((OUTSIDE - BY_TOKEN) - 0.0894) < 5e-5
    assert "الدعوى المسؤولَ عنها" in _one("ص٦").falsifies  # type: ignore[attr-defined]
    assert f"للوحدة محجوزًا {OUTSIDE:.4f}" in LOG.read_text(encoding="utf-8")


def test_the_loss_decomposes_into_price_and_count() -> None:
    """الشفرةُ أرخصُ ٠٫٥٧٩٧× والرموزُ أكثرُ ١٫٧٦١٦× — وحاصلُهما ١٫٠٢١٢."""

    cheaper = PER_WORD / PER_TOKEN
    more = WORDS / TOKENS
    assert abs(cheaper - 0.5797) < 5e-5
    assert abs(more - 1.7616) < 5e-5
    assert abs(cheaper * more - 1.0212) < 5e-4
    assert round(WORDS * PER_WORD - TOKENS * PER_TOKEN) == 32_586


def test_the_cheapest_rung_is_still_the_licensed_symbol() -> None:
    """ص٧: +٠٫٦٤٦٣ فوق `م١` — فلا يُعاد فتحُ السلّم المُجمَّد."""

    apart = OUTSIDE - BY_SYMBOL
    assert _one("ص٧").verdict(_exact(apart)) is Verdict.MET  # type: ignore[attr-defined]
    assert abs(apart - 0.6463) < 5e-5
    assert "426f7fc8" in _one("ص٧").falsifies  # type: ignore[attr-defined]


def test_the_rule_stays_unsigned_and_promotes_nothing() -> None:
    """المواصفةُ بلا توقيع، وحالُ الكلمة المفردة كما هو في السجلّ المُجمَّد."""

    rule = RULE.read_text(encoding="utf-8")
    assert "**التوقيع**: — (غيرُ موقَّعة)" in rule
    assert "`DRAFT`" in rule
    assert "غيرُ موقَّعة: True" in LOG.read_text(encoding="utf-8")
    assert "UNCLASSIFIED" in LOG.read_text(encoding="utf-8")
    ladder = LADDER.read_text(encoding="utf-8")
    assert '"الكلمةُ المفردة",' in ladder  # لم تُرفَع من المحمولات


def test_accuracy_is_not_claimed_anywhere() -> None:
    """لا شاهدَ قُوبِلت به — فلا يُقال صوابٌ ولا خطأ، بل ما فعلت وما كلّف."""

    assert __doc__ is not None
    assert "ولا جردَ صحيحًا" in __doc__
    assert "يُقال **ما فعلت**" in __doc__
    rule = RULE.read_text(encoding="utf-8")
    assert "فلا تُقاس دقّتُها" in rule
    assert "لا معجمَ فيها" in rule and "لا سياقَ فيها" in rule


def test_six_of_seven_and_the_one_that_fell_is_mine() -> None:
    """الجردُ صريحٌ، ولا يُعاد تفسيرُ شرطٍ بعد رقمه."""

    met = {"ص١", "ص٢", "ص٣", "ص٤", "ص٥", "ص٧"}
    fell = {"ص٦"}
    assert met | fell == {one.identifier for one in PREDICTIONS}  # type: ignore[attr-defined]
    assert len(met) == 6 and not met & fell
