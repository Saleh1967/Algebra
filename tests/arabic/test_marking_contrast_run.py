"""شُغِّل ختمُ `2cd80c0f…`: **سبعةٌ من سبعة — والالتباسُ ينقسم قسمةً تامّة**.

`THE_ISOLATION_IS_CLEAN_THIS_TIME`: ذراعان في تشغيلٍ واحدٍ بعمقٍ واحدٍ
(٢٤) ووقوفٍ واحد، لا يفترقان إلّا في بقاء وسم المرفوض أو رفعِه.

`AND_MY_CORRECTED_CLAIM_HELD`: ع٤ صمد: **الأبديُّ أرخصُ** عند عمقٍ واحد —
١٬٤٠٨٬٥٨١ مقابلَ ١٬٤١٦٬٧٨٩. **فالوسمُ الأبديُّ لم يكن سببَ الخسارة**، ورفعُه
يضرّ لا ينفع. ودعوايَ الأولى — أنّه يقطع الطريقَ إلى ما فوق المرفوض —
**ساقطةٌ بعزلٍ نظيف**، لا بمقابلةٍ ملتبسة.

`AND_THE_CONFOUND_SPLITS_WITH_NO_REMAINDER`: والفرقُ الذي نُشِر ملتبسًا
(**١٦٬٣٩٧** بتًّا) ينقسم: **٨٬١٨٩** لحدّ العمق (بلا حدٍّ ⟶ ٢٤)
و**٨٬٢٠٨** لرفع الوسم عند عمقٍ ٢٤ — ومجموعُهما **١٦٬٣٩٧** بلا بقيّة.
**والمتغيّران متقاربان**، فلم يكن أحدُهما يخفي الآخرَ بل كانا نصفين.

`AND_THE_DEPTH_LIMIT_DOES_BITE`: وع٦ صمد: ذراعُ الأبديِّ عند عمق ٢٤ يقف
عند **٢٬٣٠٨** التزامًا، بينما بلا حدِّ عمقٍ بلغ **٢٬٦٦٢**. فحدُّ العمق
**قيدٌ حقيقيٌّ**، وكان الالتباسُ الذي أُصلِح **قائمًا فعلًا** لا متوهَّمًا.

`AND_THE_RUN_REPRODUCES_THE_SEALED_ONE_BIT_FOR_BIT`: وع٧ صمد: الذراعُ
المؤقّتُ أعاد رقمَ `89b59b10…` — **١٬٤١٦٬٧٨٩** — وأعاد معه نقاطَ الفحص
الأربعَ والتزاماتِه ومرفوضاتِه ووسومَه المرفوعة، **رقمًا رقمًا**.

`AND_NEITHER_ARM_REACHES_THE_BLOCK`: وع٥ صمد: أدنى الذراعين **١٬٤٠٨٬٥٨١**،
والكتليُّ **١٬٣٩٤٬٦٣٨**. **ويُقال إنّه لم يُبلَغ عند عمق ٢٤، لا إنّه يمتنع.**
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from test_marking_contrast_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "marking_contrast_run.log"
SEALED = REPOSITORY / "deposits" / "temporary_marking_run.log"
PAPER = REPOSITORY / "docs" / "الترخيص-بتّةً-بتّة.md"

LASTING = 1_408_581
LIFTED = 1_416_789
LASTING_COMMITS = 2_308
LIFTED_COMMITS = 2_284
UNBOUNDED = 1_400_392
UNBOUNDED_COMMITS = 2_662
BY_BLOCK = 1_394_638
DEPTH_COST = 8_189
MARK_COST = 8_208


def _one(identifier: str) -> object:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("2cd80c0f")


def test_both_arms_passed_the_machine_checks() -> None:
    """ع١ وع٢ وع٣ على الذراعين معًا لا على أحدهما."""

    text = LOG.read_text(encoding="utf-8")
    (drift,) = re.findall(r"أقصى انحرافٍ في الذراعين ([\d.]+)", text)
    (first, second) = re.findall(r"رجعةُ الذراعين (\d+) و(\d+)", text)[0]
    (one, two) = re.findall(r"بلا نزولٍ في الذراعين (\d+) و(\d+)", text)[0]
    assert _one("ع١").verdict(_exact(float(drift))) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ع٢").verdict(Fraction(max(int(first), int(second)))) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ع٣").verdict(Fraction(int(one) + int(two))) is Verdict.MET  # type: ignore[attr-defined]
    assert float(drift) == 0.0


def test_the_lasting_mark_is_the_cheaper_one_at_equal_depth() -> None:
    """ع٤: المؤقّتُ − الأبديّ = +٨٬٢٠٨ — فدعوايَ الأولى ساقطةٌ بعزلٍ نظيف."""

    assert _one("ع٤").verdict(Fraction(LIFTED - LASTING)) is Verdict.MET  # type: ignore[attr-defined]
    assert LIFTED - LASTING == MARK_COST
    assert LIFTED_COMMITS < LASTING_COMMITS
    text = LOG.read_text(encoding="utf-8")
    assert f"جملةُ الأبديّ {LASTING} | جملةُ المؤقّت {LIFTED}" in text


def test_the_confound_splits_with_no_remainder() -> None:
    """١٦٬٣٩٧ = ٨٬١٨٩ (عمق) + ٨٬٢٠٨ (وسم) — قسمةٌ تامّة."""

    assert LASTING - UNBOUNDED == DEPTH_COST
    assert LIFTED - LASTING == MARK_COST
    assert DEPTH_COST + MARK_COST == LIFTED - UNBOUNDED == 16_397
    assert abs(DEPTH_COST - MARK_COST) < 25  # والمتغيّران متقاربان


def test_neither_arm_reaches_the_block_and_that_is_a_floor_not_a_wall() -> None:
    """ع٥: أدنى الذراعين ١٬٤٠٨٬٥٨١ — ولم يُبلَغ الكتليُّ عند هذا العمق."""

    assert _one("ع٥").verdict(Fraction(min(LASTING, LIFTED))) is Verdict.MET  # type: ignore[attr-defined]
    assert min(LASTING, LIFTED) > BY_BLOCK
    assert "لم تُبلَغ" in _one("ع٥").falsifies or "تُعاد قراءةُ" in _one("ع٥").falsifies  # type: ignore[attr-defined]


def test_the_depth_limit_really_bites() -> None:
    """ع٦: ٢٬٣٠٨ عند عمق ٢٤ مقابلَ ٢٬٦٦٢ بلا حدّ — فالالتباسُ كان قائمًا."""

    assert _one("ع٦").verdict(Fraction(LASTING_COMMITS)) is Verdict.MET  # type: ignore[attr-defined]
    assert LASTING_COMMITS < UNBOUNDED_COMMITS
    assert UNBOUNDED_COMMITS - LASTING_COMMITS == 354


def test_the_lifted_arm_reproduces_the_sealed_run_bit_for_bit() -> None:
    """ع٧: الرقمُ نفسُه، ونقاطُ الفحص نفسُها، من سجلّين مختلفين."""

    assert _one("ع٧").verdict(Fraction(0)) is Verdict.MET  # type: ignore[attr-defined]
    here = LOG.read_text(encoding="utf-8")
    there = SEALED.read_text(encoding="utf-8")
    assert f"الجملة {LIFTED} " in here and f"الجملة {LIFTED} " in there
    mine = re.findall(r"بعد (\d+): الجملة (\d+) \| أبجديّة (\d+)", here)
    lifted_side = mine[len(mine) // 2 :]
    for at, total, alphabet in lifted_side:
        assert f"بعد {at}: الجملة {total} | معجم" in there, at
        assert f"| أبجديّة {alphabet} |" in there, at
    assert len(lifted_side) == 4
    for field in (f"التزاماتٌ {LIFTED_COMMITS}", "مرفوضاتٌ 5970", "التُزِمت 414"):
        assert field in here and field in there, field


def test_the_paper_now_carries_the_isolation_instead_of_the_guess() -> None:
    """ما كان «غيرَ معزولٍ بعد» صار معزولًا وساقطًا — في الوثيقة نفسِها."""

    written = PAPER.read_text(encoding="utf-8")
    assert "**غيرُ معزولٍ بعد**" not in written
    assert "**عُزِل وسقط** بختم `2cd80c0f…`" in written
    assert "**تامّةٌ بلا بقيّة**" in written
