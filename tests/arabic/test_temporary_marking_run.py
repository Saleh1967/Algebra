"""شُغِّل ختمُ `89b59b10…`: **خمسةٌ من ثمانية — والعزلُ لم يكن عزلًا**.

`THE_MARK_WAS_LIFTED_AND_IT_MADE_THINGS_WORSE`: رفعُ الوسم لم يُصلِح شيئًا
بل **أفسد**: ١٬٤١٦٬٧٨٩ مقابلَ ١٬٤٠٠٬٣٩٢ — **أغلى ١٦٬٣٩٧** بتًّا، وبالتزاماتٍ
**أقلّ** (٢٬٢٨٤ مقابلَ ٢٬٦٦٢) وأبجديّةٍ **أصغر** (٢٬٣٨٢ مقابلَ ٢٬٦٨٥).
فدعوايَ أنّ **الوسمَ الأبديَّ** سببُ خسارة الترخيص **سقطت** (س٤ وس٥ وس٦).

`AND_THE_REFUSED_PAIR_WAS_INDEED_ONLY_REFUSED_BY_ITS_MOMENT`: وس٧ وس٨
صمدا: **٤١٤** زوجًا رُفِض ثمّ التُزِم بعد رفع وسمه، **والزوجُ المرصود** —
الذي رُفِض أوّلًا في `69a1c10c…` عند الاقتراح ١٨ — **التُزِم عند الالتزام
٢١**. فرفضُه كان **من الحال لا من الزوج**، وذلك مقيسٌ لا مُستنتَج.

`BUT_THE_ISOLATION_CARRIED_TWO_VARIABLES_NOT_ONE`: **وهذا حكمٌ لا يُنسَب
إلى الوسم وحدَه**. نصَّ الختمُ على «التغييرُ واحدٌ لا غير»، **وكان فيه
متغيّران**: رفعُ الوسم **وحدُّ عمق البحث** (٢٤ في كلّ حال)، بينما ذراعُ
`69a1c10c…` لم يكن محدودَ العمق. فالفرقُ **ملتبسٌ بمتغيّرين**، والعطلُ
مُسجَّلٌ ثالثَ عشرَ في `docs/سجل-الأعطال.md`، وتصحيحُه ختمُ `2cd80c0f…`.

`AND_THE_LIMIT_WAS_DECLARED_EVEN_WHERE_THE_CLAIM_WAS_TOO_WIDE`: ونصُّ
الختم على أنّ العمقَ محدودٌ وأنّ المبلوغَ حدٌّ أدنى **كان صحيحًا**. فيُقال
عن س٦ إنّ الكتليَّ **لم يُبلَغ عند عمق ٢٤**، لا إنّه **يمتنع**.
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from test_temporary_marking_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "temporary_marking_run.log"
FULL = REPOSITORY / "deposits" / "temporary_marking_full.log"
FLAWS = REPOSITORY / "docs" / "سجل-الأعطال.md"

COMMITS = 2_284
PROPOSALS = 8_254
REFUSALS = 5_970
REVIVED = 414
WATCHED_AT = 21
TOTAL = 1_416_789
RATIO = 0.6929
CLEAN = 0.8900
SYMBOLS = 2_382
BY_LASTING = 1_400_392
COMMITS_LASTING = 2_662
SYMBOLS_LASTING = 2_685
BY_BLOCK = 1_394_638


def _one(identifier: str) -> object:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("89b59b10")


def test_the_machine_held_and_the_licence_stayed_per_merge() -> None:
    """س١ وس٢ وس٣: انحرافٌ صفرٌ، ورجعةٌ صفرٌ، ولا التزامَ بلا نزول."""

    text = LOG.read_text(encoding="utf-8")
    (drift,) = re.findall(r"أقصى انحرافٍ بين الآلتين عند نقاط الفحص: ([\d.]+)", text)
    (back,) = re.findall(r"مواضعُ الخلاف بين بسطِ الرموز ومجرى L₀ = (\d+)", text)
    (rises,) = re.findall(r"التزاماتٌ بفرقٍ غيرِ سالب: (\d+)", text)
    assert _one("س١").verdict(_exact(float(drift))) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("س٢").verdict(Fraction(int(back))) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("س٣").verdict(Fraction(int(rises))) is Verdict.MET  # type: ignore[attr-defined]
    assert float(drift) == 0.0 and int(back) == 0 and int(rises) == 0


def test_lifting_the_mark_made_it_worse_not_better() -> None:
    """س٤ وس٥ وس٦ منقوضة — ودعوايَ عن الوسم الأبديّ تسقط."""

    assert _one("س٤").verdict(Fraction(COMMITS)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    assert _one("س٥").verdict(Fraction(TOTAL)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    assert _one("س٦").verdict(Fraction(TOTAL)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    assert TOTAL - BY_LASTING == 16_397
    assert COMMITS < COMMITS_LASTING and SYMBOLS < SYMBOLS_LASTING
    assert TOTAL > BY_BLOCK


def test_the_refused_pair_was_refused_by_its_moment_not_by_itself() -> None:
    """س٧ وس٨: ٤١٤ وسمًا رُفِع ثمّ التُزِم، والمرصودُ عند الالتزام ٢١."""

    text = LOG.read_text(encoding="utf-8")
    assert _one("س٧").verdict(Fraction(REVIVED)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("س٨").verdict(Fraction(WATCHED_AT)) is Verdict.MET  # type: ignore[attr-defined]
    assert f"الزوجُ المرصودُ التُزِم عند: {WATCHED_AT}" in text
    assert f"وسومٌ رُفِعت ثمّ التُزِمت {REVIVED}" in text
    lifted = FULL.read_text(encoding="utf-8")
    assert len(re.findall(r"وسمٌ يُرفَع عند الالتزام", lifted)) == REVIVED


def test_the_run_reports_its_own_numbers_unrounded() -> None:
    """الأرقامُ من السجلّ لا من الذاكرة."""

    text = LOG.read_text(encoding="utf-8")
    assert f"اقتراحاتٌ {PROPOSALS} | التزاماتٌ {COMMITS} | مرفوضاتٌ {REFUSALS}" in text
    assert f"الجملة {TOTAL} | النسبةُ إلى L₀ {RATIO:.4f}" in text
    assert f"= {CLEAN:.4f}" in text
    assert f"الجملة: رموزٌ {SYMBOLS} " in text


def test_this_isolation_is_declared_confounded() -> None:
    """متغيّران لا واحد — والعطلُ مُسجَّلٌ ومُصحَّحٌ بختمٍ آخر."""

    import test_temporary_marking_seal as sealed

    assert "تغييرٌ واحد" in ORACLE.extraction  # وهو ما لم يصدق
    assert "أعلى ٢٤ مقترَحًا فقط" in ORACLE.extraction  # والثاني ههنا
    assert sealed.__doc__ is not None
    written = FLAWS.read_text(encoding="utf-8")
    assert "ختمٌ يدّعي عزلًا وفيه متغيّران" in written
    assert "2cd80c0f" in written
    assert "صدقُ التفصيل لا يُصحّح دعوى الجملة" in written


def test_a_limited_search_is_reported_as_not_reached_not_impossible() -> None:
    """س٦ سقط عند عمق ٢٤ — ولا يُقال إنّ الكتليَّ يمتنع."""

    import test_temporary_marking_seal as sealed

    crux = _one("س٦")
    assert "لم تُبلَغ عند عمق ٢٤" in crux.falsifies  # type: ignore[attr-defined]
    assert sealed.__doc__ is not None
    assert "حدٌّ أدنى" in sealed.__doc__
    assert "فلا يُقال إنّها لا تُبلَغ" in sealed.__doc__
