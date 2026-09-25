"""شُغِّل ختمُ `be03e5be…`: **تسعةٌ من عشرة — ولا نتيجةَ تنقلب**.

`EVERY_PUBLISHED_WORD_NUMBER_WAS_REMEASURED`: رُفِعت البسملاتُ الملحقةُ
من **١١٢** سطرًا، فصارت الألفاظُ **٧٧٬٧٩٧** — وهو الحسابُ بعينه
(٧٨٬٢٤٥ − ٤٤٨). والمدوّنةُ المشتقّةُ ببصمتها، **والمُجمَّدُ لم يُمَسّ**،
والسجلُّ المُقفَل `426f7fc8…` باقٍ.

`AND_NOT_ONE_CONCLUSION_TURNED`: ر٦ صمد: **أرخصُ درجةٍ `م١`** كما كانت.
ور١٠ صمد: الفصلُ ما زال **خاسرًا** (+٠٫٠٦٣٤، وكان +٠٫٠٨٩٤). **فحكمُ
`7bf3ccd8…` لم يكن رهنَ البسملات، وكذلك السلّمُ.**

`AND_EVERY_SHIFT_IS_IN_THE_THIRD_DECIMAL`: الثمنُ المحجوزُ عند الوحدة
**٥٫٦٠٧٢** (كان ٥٫٦٠٥٩)، وعند اللفظ **٤٫٢٠٦٩** (كان ٤٫٢١١٨)، وعند
السطر **٦٫٩٤٣٤** (كان ٦٫٩٣٦٩). **ولا فرقَ يتجاوز المنزلة الثالثة.**

`AND_THE_DIRECTION_WAS_DECLARED_BEFORE_THE_NUMBER`: ر٧ ور٨ صمدا كما
أُعلِن: رفعُ **أكثرِ ما تكرّر** يرفع الثمنَ (**+٠٫٠٠١٣**) ويرفع المرتدَّ
(**+٠٫٠٠١١**). **وذلك متوقَّعٌ ولا يُقرأ خبرًا عن البنية** — وهو مكتوبٌ
في الختم قبل النظر.

`BUT_ONE_FELL_AND_IT_IS_A_SMALL_REAL_FINDING`: ر٥ **منقوض**: نصيبُ كتلة
الغامض **٠٫٤٤٤٣** لا ٠٫٤٤٦١ — **نزل ٠٫٠٠١٨**. فبعضُ كلمات البسملة على
هياكلَ **غامضة**، خلافًا لما ظننت. وكتلتُها نزلت **٣٣٦** لا ٤٤٨.

`AND_THE_GREEDY_PATH_MOVED_MOST`: وأكبرُ ما تحرّك مسارُ الجشع: أبجديّةُ
`م١` **٢٬٩٥٢ ⟶ ٢٬٨٥٧** والتزاماتُه **٣٬٠٥٦ ⟶ ٢٬٩٣٣** — لأنّ تكرارَ
البسملات كان يغذّيه. **والانحرافُ صفرٌ** (ر٩).
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from test_basmala_lifted_seal import (
    DIGEST,
    LIFTED_LINES,
    LIFTED_WORDS,
    ORACLE,
    PREDICTIONS,
    TOKENS_AFTER,
    TOKENS_BEFORE,
)

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "basmala_lifted_run.log"
PAPER = REPOSITORY / "docs" / "الأرقام-مرفوعة-البسملات.md"
FROZEN = REPOSITORY / "tools" / "ladder_seal.py"

SHARE = 0.4443
SHARE_BEFORE = 0.4461
OUTSIDE = (5.6072, 3.6815, 4.2069, 6.9434)
BEFORE = (5.6059, 3.6549, 4.2118, 6.9369)
MISSING_TOKEN = 0.1983
CUT_COST = 4.2703


def _one(identifier: str) -> object:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def _grab(pattern: str) -> tuple[str, ...]:
    found = re.search(pattern, LOG.read_text(encoding="utf-8"), re.MULTILINE)
    assert found is not None, pattern
    return found.groups()


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("be03e5be")


def test_the_lift_is_exact_and_the_frozen_corpus_is_untouched() -> None:
    """ر١ ور٢ ور٣: ١١٢ سطرًا، و٦٬٢٣٦ باقيةً، و٧٧٬٧٩٧ لفظًا."""

    (lines, lifted) = _grab(r"^  أسطرٌ (\d+) \| أسطرٌ رُفِعت (\d+)$")
    assert _one("ر١").verdict(Fraction(abs(int(lifted) - LIFTED_LINES))) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ر٢").verdict(Fraction(abs(int(lines) - 6_236))) is Verdict.MET  # type: ignore[attr-defined]
    (tokens, before) = _grab(r"^  الألفاظُ: (\d+) \(قبلُ (\d+)\)$")
    assert _one("ر٣").verdict(Fraction(abs(int(tokens) - TOKENS_AFTER))) is Verdict.MET  # type: ignore[attr-defined]
    assert int(before) - int(tokens) == LIFTED_WORDS == TOKENS_BEFORE - TOKENS_AFTER
    (derived,) = _grab(r"^  بصمتُها ([0-9a-f]{64})$")
    assert derived != "37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a"
    import importlib.util
    import sys

    spec = importlib.util.spec_from_file_location("frozen_ladder_check", FROZEN)
    assert spec is not None and spec.loader is not None
    sealed = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = sealed
    spec.loader.exec_module(sealed)
    assert sealed.rederive_record_digest().startswith("426f7fc8")  # لم يُمَسّ


def test_the_skeletons_did_not_grow() -> None:
    """ر٤: ١٥٬٤٧١ ≤ ١٥٬٤٧٢ — وواحدٌ اختفى بكامله."""

    (shapes, before) = _grab(r"^  هياكلُ متمايزة: (\d+) \(قبلُ (\d+)\)$")
    assert _one("ر٤").verdict(Fraction(int(shapes))) is Verdict.MET  # type: ignore[attr-defined]
    assert int(before) - int(shapes) == 1


def test_the_ambiguous_mass_share_fell_and_that_falsifies_the_fifth() -> None:
    """ر٥ منقوض: ٠٫٤٤٤٣ لا ٠٫٤٤٦١ — فبعضُ كلمات البسملة على هياكلَ غامضة."""

    (mass, share, mass_before, _) = _grab(
        r"^  كتلتُها: (\d+) \(([\d.]+)\) \(قبلُ (\d+) و([\d.]+)\)$"
    )
    assert _one("ر٥").verdict(_exact(float(share))) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    assert abs(float(share) - SHARE) < 5e-5
    assert float(share) < SHARE_BEFORE
    assert int(mass_before) - int(mass) == 336
    assert 336 < LIFTED_WORDS  # فليست كلماتُ البسملة كلُّها على غامض


def test_the_cheapest_rung_did_not_move() -> None:
    """ر٦: أرخصُ درجةٍ `م١` كما كانت — فالسلّمُ ليس رهنَ البسملات."""

    assert _one("ر٦").verdict(Fraction(1)) is Verdict.MET  # type: ignore[attr-defined]
    text = LOG.read_text(encoding="utf-8")
    assert "أرخصُ درجةٍ محجوزًا: م١ الرمزُ المُرخَّص (قبلُ م١)" in text
    assert OUTSIDE.index(min(OUTSIDE)) == 1
    assert BEFORE.index(min(BEFORE)) == 1


def test_the_declared_direction_held_on_both_counts() -> None:
    """ر٧ ور٨: الثمنُ +٠٫٠٠١٣ والمرتدُّ +٠٫٠٠١١ — كما أُعلِن قبل الرقم."""

    apart = OUTSIDE[0] - BEFORE[0]
    assert _one("ر٧").verdict(_exact(apart)) is Verdict.MET  # type: ignore[attr-defined]
    assert abs(apart - 0.0013) < 5e-5
    assert _one("ر٨").verdict(_exact(MISSING_TOKEN)) is Verdict.MET  # type: ignore[attr-defined]
    assert abs((MISSING_TOKEN - 0.1972) - 0.0011) < 5e-5
    assert __doc__ is not None and "متوقَّعٌ ولا يُقرأ خبرًا" in __doc__


def test_the_machine_agreed_with_itself() -> None:
    """ر٩: انحرافُ الآلتين صفر."""

    (drift,) = _grab(r"^  انحرافُ الآلتين: ([\d.]+)$")
    assert _one("ر٩").verdict(_exact(float(drift))) is Verdict.MET  # type: ignore[attr-defined]
    assert float(drift) == 0.0


def test_the_separation_rule_verdict_did_not_flip() -> None:
    """ر١٠: الفصلُ ما زال خاسرًا — +٠٫٠٦٣٤ وكان +٠٫٠٨٩٤."""

    (cost, before, at_token) = _grab(
        r"^  للوحدة محجوزًا ([\d.]+) \(قبلُ ([\d.]+)\) \| ومستوى اللفظ ([\d.]+)$"
    )
    apart = float(cost) - float(at_token)
    assert _one("ر١٠").verdict(_exact(apart)) is Verdict.MET  # type: ignore[attr-defined]
    assert apart > 0 and abs(apart - 0.0634) < 5e-5
    assert abs(float(cost) - CUT_COST) < 5e-5
    assert apart < 0.0894  # ضاق الفرقُ ولم ينقلب


def test_every_shift_is_small() -> None:
    """لا فرقَ في الثمن المحجوز يتجاوز المنزلة الثالثة."""

    gaps = [abs(one - two) for one, two in zip(OUTSIDE, BEFORE)]
    assert max(gaps) < 0.03, gaps
    assert all(gap > 0 for gap in gaps)


def test_the_paper_is_generated_from_the_log() -> None:
    """الوثيقةُ تُولَّد من السجلّ — فمقارنتُها به مطابقةٌ تامّة."""

    import importlib.util

    tool = REPOSITORY / "tools" / "write_lifted_paper.py"
    spec = importlib.util.spec_from_file_location("write_lifted_paper", tool)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    written = PAPER.read_text(encoding="utf-8")
    assert module.render() == written
    assert "لم تنقلب نتيجةٌ واحدة" in written
    assert "لم يُمَسّ" in written


def test_nine_of_ten_and_the_one_that_fell_is_named() -> None:
    """الجردُ صريحٌ، ولا يُعاد تفسيرُ شرطٍ بعد رقمه."""

    met = {"ر١", "ر٢", "ر٣", "ر٤", "ر٦", "ر٧", "ر٨", "ر٩", "ر١٠"}
    fell = {"ر٥"}
    assert met | fell == {one.identifier for one in PREDICTIONS}  # type: ignore[attr-defined]
    assert len(met) == 9 and not met & fell


FELL_WITH_THEM: dict[str, str] = {
    "ر٥": "أنّ الغموضَ لا ينقص برفع البسملات:",
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
