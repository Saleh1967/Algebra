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


FELL_WITH_THEM: dict[str, str] = {
    "س٤": "دعوايَ أنّ الوسمَ الأبديَّ كان يُنفِد",
    "س٥": "أنّ رفعَ الوسم يُحسِّن شيئًا أصلًا؛ فإن لم",
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


LICENCE = REPOSITORY / "deposits" / "greedy_licence_run.log"

THE_BOUND_BINDS_BOTH_ARMS = False
"""أيَعَضُّ الحدُّ المُعلَنُ (عمقُ ٢٤) الذراعين **بالسواء**؟ — والجوابُ: لا.

وهذا هو العطلُ الثالثَ عشر مقيسًا: ذراعُ هذا الختم **محدودُ العمق بأربعٍ
وعشرين**، وذراعُ المقابلة — تشغيلُ `69a1c10c…` — **لم يكن محدودَ العمق
أصلًا**، بل يقف بتوالي خمسِ مئةِ رفض. فالحدُّ ليس مختلفَ الأثر فحسب:
**هو قائمٌ في ذراعٍ ومرفوعٌ في الآخر**.

**والتصحيحُ مُودَعٌ**: `2cd80c0f…` أعاد المقابلةَ بذراعين في تشغيلٍ واحدٍ
وعمقٍ واحد. **وأرقامُ هذا الختم تبقى على حالها** ولا تُعاد قراءتُها؛ وإنّما
يُقال **ما كانت تحته**.
"""

THE_BOUND_EVIDENCE = (
    "الذراعُ ههنا يقف بـ«حالٌ لا يربح فيها أعلى 24 مقترَحٍ»، وذراعُ "
    "المقابلة يقف بـ«توالى 500 رفضًا» بلا عمقٍ محدود — فالحدُّ مرفوعٌ "
    "في أحدهما، ونصيبُ المرفوضات ٠٫٧٢٣٣ مقابلَ ٠٫٦٩٥٠ لا يُقابَل بينهما"
)


def test_the_declared_depth_stood_on_one_arm_only() -> None:
    """الحدُّ قائمٌ في ذراعٍ مرفوعٌ في الآخر — فلا عزلَ تامًّا ههنا."""

    mine = LOG.read_text(encoding="utf-8")
    other = LICENCE.read_text(encoding="utf-8")
    assert "الوقوف: حالٌ لا يربح فيها أعلى 24 مقترَحٍ" in mine
    assert "الوقوف: توالى 500 رفضًا" in other
    assert "عمق" not in other.splitlines()[9]  # سطرُ وقوفِ المقابلة بلا عمق
    here = re.findall(r"اقتراحاتٌ (\d+) \| التزاماتٌ \d+ \| مرفوضاتٌ (\d+)", mine)
    there = re.findall(r"اقتراحاتٌ (\d+) \| التزاماتٌ \d+ \| مرفوضاتٌ (\d+)", other)
    assert here == [("8254", "5970")] and there == [("8729", "6067")]
    shares = [int(two) / int(one) for one, two in here + there]
    assert abs(shares[0] - 0.7233) < 5e-5 and abs(shares[1] - 0.6950) < 5e-5
    bounded = ["أعلى 24 مقترَحٍ" in one for one in (mine, other)]
    assert bounded == [True, False]  # الحدُّ في ذراعٍ دون الآخر
    assert THE_BOUND_BINDS_BOTH_ARMS is (bounded[0] == bounded[1])


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ **مرّت** وتعليلُها المكتوبُ معها **لم يُؤيَّد بالقياس** — إن وُجِدت.

فشرطٌ يمرُّ بتعليلٍ خاطئ **ليس تأييدًا**: العددُ صحيحٌ والسببُ المنسوبُ إليه
غيرُ مقيس. وهذا الاسمُ **مطلوبٌ في كلّ تشغيل** وإن كان فارغًا، كي يُسأل
السؤالُ في كلّ مرّة ولا يُطوى بالسكوت — وهو العطلُ الثامن.
"""
