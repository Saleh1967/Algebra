"""شُغِّل ختمُ `69a1c10c…`: **أربعةٌ من سبعة — والثلاثةُ الساقطةُ دعاوايَ**.

`THE_LICENCE_IS_NOW_PER_MERGE_AND_THAT_MUCH_HELD`: ر١ ور٢ ور٣ صمدت.
انحرافُ الآلتين **٠٫٠٠٠٠٠٠٠٠٠** على نقاط الفحص، والرجعةُ **٠** موضعًا،
و**لا التزامَ واحدٌ** من ٢٬٦٦٢ نزلت عنده التكلفةُ. فالقولُ «لا يبقى بتٌّ
إلّا ليسهم بإفادة» **مُحقَّقٌ الآن بمعناه الحرفيّ**، لا كتلةً.

`AND_MY_THREE_SUBSTANTIVE_CLAIMS_ALL_FELL`: ور٤ ور٦ ور٧ **منقوضة**:
الالتزاماتُ **٢٬٦٦٢** لا ٤٬٥٠١، والنسبةُ **٠٫٦٨٤٩** لا دون ٠٫٦٨٢،
والفراغُ **٠٫٨٩١٩** لا دون ٠٫٨٣٧٩. **فالترخيصُ بتّةً بتّة أغلى** من
الكتليّ بـ**٥٬٧٥٤** بتًّا (٠٫٤١٪).

`AND_THE_SEVENTH_FELL_BACKWARDS`: ور٧ سقط **في الجهة المعاكسة لدعوايَ**:
قلتُ الرخصةُ تشتري الضغطَ **بعبورٍ أكثر**، والمقيسُ أنّها تحفظ الفراغَ
**أكثر** — ٠٫٨٩١٩ مقابلَ ٠٫٨٣٧٩. والمرفوضُ **نادرٌ عريض** (وسيطُ
استبداله ٧)، وهو نفسُه العابر.

`AND_THE_BIT_WAS_TRACED_NOT_GUESSED`: وأوّلُ رفضٍ (بعد ١٧ التزامًا،
بوقوعٍ ١٬٣٩٧) أُعيد بالآلة المنشورة على الآيات فأعطى **+٣٤٢٫٠٥٠٩** نفسَه.
وتعليلي الأوّل — «دمجُ طرفين كثيرَي الوقوع يُسطِّح التوزيع» — **مخالفٌ
للمقيس**: الطرفان **لم يتغيّر ثمنُهما** (٥ و٤ قبلُ وبعدُ)، والاستبدالاتُ
**وفّرت ١٬٣٩٧** بتًّا حقًّا. والذي أسقطها أنّ الرمزَ الجديد **حمَّل سائرَ
الرموز ١٬٧٢٤** بتًّا — فضاءُ الشفرة محدود، وكلُّ داخلٍ يقتطع منه.

`AND_WHAT_IS_NOT_ISOLATED_IS_SAID_TO_BE_NOT_ISOLATED`: والكتليُّ يلتزم
هذا الزوجَ بعينه وينتهي أرخص — **ولم يُعزَل أثرُ هذه الدمجة وحدَها**،
فنسبةُ الفرق إليها **استنتاجٌ لا قياس**، ومكتوبٌ في الوثيقة أنّه كذلك.
"""

from __future__ import annotations

import re
import sys
from fractions import Fraction
from pathlib import Path

from test_greedy_licence_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "greedy_licence_run.log"
REFUSAL = REPOSITORY / "deposits" / "greedy_licence_refusal.log"
PAPER = REPOSITORY / "docs" / "الترخيص-بتّةً-بتّة.md"

COMMITS = 2_662
PROPOSALS = 8_729
REFUSALS = 6_067
BEFORE_FIRST = 17
TOTAL = 1_400_392
RATIO = 0.6849
CLEAN = 0.8919
SYMBOLS = 2_685
BY_BLOCK = 1_394_638
BLOCK_RATIO = 0.6821
BLOCK_CLEAN = 0.8379
BLOCK_SYMBOLS = 4_538


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def _one(identifier: str) -> object:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("69a1c10c")


def test_the_machine_checked_itself_against_the_published_one() -> None:
    """ر١ ور٢: انحرافُ الآلتين صفرٌ، والرجعةُ صفرُ موضعٍ."""

    text = LOG.read_text(encoding="utf-8")
    (drift,) = re.findall(r"أقصى انحرافٍ بين الآلتين عند نقاط الفحص: ([\d.]+)", text)
    (back,) = re.findall(r"مواضعُ الخلاف بين بسطِ الرموز ومجرى L₀ = (\d+)", text)
    assert _one("ر١").verdict(_exact(float(drift))) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ر٢").verdict(Fraction(int(back))) is Verdict.MET  # type: ignore[attr-defined]
    assert float(drift) == 0.0 and int(back) == 0


def test_no_single_merge_was_committed_without_paying() -> None:
    """ر٣ — وهو معنى «بتّةً بتّة»: صفرٌ من ٢٬٦٦٢."""

    text = LOG.read_text(encoding="utf-8")
    (rises,) = re.findall(r"التزاماتٌ بفرقٍ غيرِ سالب: (\d+)", text)
    assert _one("ر٣").verdict(Fraction(int(rises))) is Verdict.MET  # type: ignore[attr-defined]
    assert int(rises) == 0
    assert f"التزاماتٌ {COMMITS} " in text


def test_the_refusal_came_early_and_that_one_held() -> None:
    """ر٥: أوّلُ رفضٍ بعد ١٧ التزامًا — فالرفضُ متخلّلٌ لا ذيلٌ خالص."""

    text = LOG.read_text(encoding="utf-8")
    assert f"أوّلُ رفضٍ بعد {BEFORE_FIRST} التزامًا" in text
    assert _one("ر٥").verdict(Fraction(BEFORE_FIRST)) is Verdict.MET  # type: ignore[attr-defined]
    assert f"مرفوضاتٌ {REFUSALS}" in text and f"اقتراحاتٌ {PROPOSALS}" in text


def test_the_three_substantive_claims_were_falsified() -> None:
    """ر٤ ور٦ ور٧ — ولا يُعاد تفسيرُ شرطٍ بعد رؤية رقمه."""

    assert _one("ر٤").verdict(Fraction(COMMITS)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    assert _one("ر٦").verdict(_exact(RATIO)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    assert _one("ر٧").verdict(_exact(CLEAN)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    text = LOG.read_text(encoding="utf-8")
    assert f"النسبةُ إلى L₀ {RATIO:.4f}" in text
    assert f"= {CLEAN:.4f}" in text


def test_the_seventh_fell_in_the_direction_opposite_to_the_claim() -> None:
    """ظننتُها تشتري الضغطَ بعبورٍ أكثر — والمقيسُ حفظٌ أكثر.

    **وما كتبتُه في الختم عن معنى سقوطها لم يتحقّق أيضًا**: قلتُ إن
    ارتفع النصيبُ فالترخيصُ «يشتري الضغطَ والفراغَ معًا». والمقيسُ أنّه
    **حفظ الفراغَ وخسر الضغط**. فالشرطُ سقط، **والمعنى الذي علّقتُه على
    سقوطه سقط معه** — ويُسجَّل، ولا يُعاد تفسيرُ نصٍّ مختوم.
    """

    seventh = _one("ر٧")
    assert CLEAN > BLOCK_CLEAN
    assert "الضغطُ يُشترى بعبورٍ أكثر" in seventh.falsifies  # type: ignore[attr-defined]
    assert abs((CLEAN - BLOCK_CLEAN) - 0.0540) < 5e-5
    assert "يشتري الضغطَ والفراغَ معًا" in seventh.falsifies  # type: ignore[attr-defined]
    assert RATIO > BLOCK_RATIO  # فالضغطُ لم يُشترَ، بل خُسِر


def test_licensing_costs_compression_and_buys_a_smaller_alphabet() -> None:
    """أغلى ٥٬٧٥٤ بتًّا، وأصغر ١٬٨٥٣ رمزًا — رقمان لا رقمٌ واحد."""

    assert TOTAL - BY_BLOCK == 5_754
    assert BLOCK_SYMBOLS - SYMBOLS == 1_853
    assert abs((TOTAL - BY_BLOCK) / BY_BLOCK - 0.0041) < 5e-5
    assert RATIO > BLOCK_RATIO
    text = LOG.read_text(encoding="utf-8")
    assert f"الجملة: رموزٌ {SYMBOLS} | وقوعاتٌ 133230" in text


def test_the_first_refusal_reproduces_on_the_verses_not_the_counters() -> None:
    """+٣٤٢٫٠٥٠٩ من الآلتين معًا — والرقمُ واحدٌ لا رقمان."""

    text = REFUSAL.read_text(encoding="utf-8")
    (counters,) = re.findall(r"الفرقُ من العدّادات \+([\d.]+)", text)
    (mirror,) = re.findall(r"الفرقُ من الآيات   \+([\d.]+)", text)
    assert counters == mirror == "342.0509"
    assert "وهي الزوجُ الذي رفضه الترخيص: True" in text


def test_the_bit_was_traced_and_my_first_explanation_was_wrong() -> None:
    """الاستبدالاتُ وفّرت، وسائرُ الرموز دفع — والطرفان لم يتغيّرا."""

    text = REFUSAL.read_text(encoding="utf-8")
    (saved,) = re.findall(r"فالفرقُ على الاستبدالات وحدَها -(\d+)", text)
    (charged,) = re.findall(r"سائرُ الرموز: \d+ ⟶ \d+ \(\+(\d+)\)", text)
    (kept,) = re.findall(r"الطرفان فيما لم يُستبدَل: \d+ ⟶ \d+ \(\+(\d+)\)", text)
    assert int(saved) == 1_397 and int(charged) == 1_724 and int(kept) == 0
    assert int(charged) - int(saved) == 327  # وهو البيانُ داخلَ العيّنة
    (before, after) = re.findall(r"جملةُ البتّات داخلَ العيّنة: (\d+) ⟶ (\d+)", text)[0]
    assert int(after) - int(before) == 327


def test_the_paper_is_regenerated_from_the_log_and_never_typed() -> None:
    """الوثيقةُ تُبنى من السجلّ — فمقارنتُها به مطابقةٌ تامّة."""

    sys.path.insert(0, str(REPOSITORY / "tools"))
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "write_licence_paper", REPOSITORY / "tools" / "write_licence_paper.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.render() == PAPER.read_text(encoding="utf-8")


def test_the_paper_quotes_shapes_verbatim_and_has_no_gloss_column() -> None:
    """صورُ الوثيقة تُقارَن بصور السجلّ مطابقةً، ولا عمودَ تفسير."""

    text = LOG.read_text(encoding="utf-8")
    shapes = {
        one
        for one, _, _ in re.findall(
            r"^    (\S+)  \((\d+)\) وحداتُه (\d+)$", text, re.MULTILINE
        )
    }
    written = PAPER.read_text(encoding="utf-8")
    quoted = re.findall(
        r"^\| \*\*([^*|٠-٩]+)\*\* \| ([٠-٩٬]+) \| ([٠-٩]+) \|$", written, re.MULTILINE
    )
    assert {one for one, _, _ in quoted} == shapes
    assert len(quoted) == 14
    assert "| ما هي |" not in written


def test_what_was_not_isolated_is_declared_not_isolated() -> None:
    """أثرُ **الدمجة الواحدة** لم يُعزَل — ومكتوبٌ أنّه لم يُعزَل.

    وهو غيرُ ما عُزِل بختم `2cd80c0f…`: ذاك **سياسةُ الوسم**، وقد عُزِلت
    وسقطت دعوايَ فيها. **وأمّا أنّ هذه الدمجةَ بعينها درجةٌ لما فوقها
    فلا يزال استنتاجًا**، ولا يُخلَط البابان.
    """

    written = PAPER.read_text(encoding="utf-8")
    assert "**وما لم يُقَس**" in written
    assert "**استنتاجٌ لا قياس**" in written
    assert "حتّى يُعزَل بختمٍ خاصّ" in written
    assert "**عُزِل وسقط** بختم `2cd80c0f…`" in written  # وهو بابٌ آخر
