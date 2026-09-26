"""الجسرُ مُشتَقٌّ، وكلُّ عددٍ فيه له شاهدٌ، **ولا سطرَ يدّعي برهانًا لغويًّا**.

**ما يحرسه**: أنّ `docs/جسر-البتّات.md` يُعاد توليدُه مطابقًا، وأنّ كلَّ
رقمٍ فيه مقروءٌ من سجلٍّ مُودَع، وأنّ **لكلّ بتّةٍ جنسَ جسرٍ من مفرداتٍ
مُغلَقة** — فلا يُترَك مدلولٌ بلا تصنيف. **وأنّ لا عائلةَ مُرخَّصة**:
كلُّ جسرٍ معلَّقٌ على إيداعٍ لم يُودَع، ويُقال ذلك بنصّه.

**والحدُّ الذي يحرسه أخصُّ من ذلك**: أنّ الجدولَ **لا يُطبَع فارغًا**.
وقد وقع ذلك أوّلَ كتابة المولّد — طُبِع جدولُ الخانات بلا صفٍّ واحد،
**فقُرِئ «لا خانات» وهو كذبٌ يقرأُه القارئُ لا الآلة**.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from typing import Any

import pytest

REPOSITORY = Path(__file__).resolve().parents[2]
DOCS = REPOSITORY / "docs"
DEPOSITS = REPOSITORY / "deposits"
BRIDGE = DOCS / "جسر-البتّات.md"
WESTERN = str.maketrans("٠١٢٣٤٥٦٧٨٩٫", "0123456789.")


def _tool() -> Any:
    path = REPOSITORY / "tools" / "write_bit_bridge.py"
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _signature() -> Any:
    path = REPOSITORY / "tools" / "bridge_signature.py"
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_the_bridge_is_regenerated_and_never_typed() -> None:
    """المكتوبُ مطابقٌ لما تولّده الأداة — حرفًا بحرف."""

    assert _tool().render() == BRIDGE.read_text(encoding="utf-8")


def test_no_table_is_printed_empty() -> None:
    """كلُّ جدولٍ في الوثيقة له صفٌّ بعد سطر المحاذاة — ولا جدولَ فارغ."""

    rows = BRIDGE.read_text(encoding="utf-8").splitlines()
    heads = [one for one, two in enumerate(rows) if re.fullmatch(r"\|[-:| ]+\|", two)]
    assert len(heads) == 5, heads
    for one in heads:
        assert rows[one + 1].startswith("|"), rows[one : one + 2]


def test_the_target_boxes_are_eight_and_carry_their_slices() -> None:
    """خاناتُ الهدف ثمانٍ، كلُّها شريحةٌ ونقطةُ ترميزٍ لا اسمُ يونيكود."""

    tool = _tool()
    ladder = (DEPOSITS / "context_ladder_run.log").read_text(encoding="utf-8")
    found = tool.boxes(ladder)
    assert len(found) == tool.BOXES == 8
    assert sum(int(two) for _, two, _ in found) == 78_245
    written = BRIDGE.read_text(encoding="utf-8")
    for slice_, count, share in found:
        assert f"| `{slice_}` |" in written, slice_
        assert tool.eastern(count) in written and tool.eastern(share) in written
    assert "ARABIC" not in written


def test_every_bit_is_classified_from_a_closed_vocabulary() -> None:
    """لكلّ بتّةٍ جنسُ جسرٍ مُعلَنٌ — ولا بتّةَ بلا تصنيف."""

    tool = _tool()
    ladder = (DEPOSITS / "context_ladder_run.log").read_text(encoding="utf-8")
    rows = tool.steps(ladder)
    assert len(rows) == 12, len(rows)
    kinds = {tool.FAMILIES[tool.family_of(one[1])][1] for one in rows}
    assert kinds == {
        "يحتاج حدًّا مُودَعًا",
        "يحتاج جدولَ أبوابٍ مُودَعًا",
        "يحتاج جدولَ صرفٍ مُودَعًا",
    }, kinds
    written = BRIDGE.read_text(encoding="utf-8")
    for step, question, gain, blocks in rows:
        row = f"| د{tool.eastern(step)} | «{question}» | **+{tool.eastern(gain)}**"
        assert row in written, row


def test_every_number_in_the_bridge_has_a_witness_or_a_derivation() -> None:
    """كلُّ عددٍ إمّا شاهدٌ في سجلٍّ مُودَع، **وإمّا مُشتَقٌّ يُعاد اشتقاقُه**.

    **ولا قائمةَ استثناءات**: مجاميعُ العائلات ليست في سجلٍّ، فتُجمَع
    ههنا من بتّاتها المشهودة وتُقابَل. فما لم يُشهَد له ولم يُشتَقّ يسقط.
    """

    tool = _tool()
    written = BRIDGE.read_text(encoding="utf-8")
    body = written.split("## ما لا يُدَّعى", 1)[0]
    logs = "".join(
        (DEPOSITS / one).read_text(encoding="utf-8")
        for one in (
            "context_ladder_run.log",
            "arabic_token_run.log",
            "pausal_split_run.log",
            "pausal_split_witness.log",
            "morph_residue_run.log",
        )
    )
    ladder = (DEPOSITS / "context_ladder_run.log").read_text(encoding="utf-8")
    rows = tool.steps(ladder)
    derived = set()
    for name in tool.FAMILIES:
        mine = [one for one in rows if tool.family_of(one[1]) == name]
        assert mine, name
        derived.add(f"{sum(float(one[2]) for one in mine):.6f}")
    # ونِسبُ البقاء مُشتَقّةٌ أيضًا — تُعاد قسمةً ولا تُستثنى
    for whole_gain, inner_gain in tool.lifted().values():
        stayed = float(inner_gain) / float(whole_gain) if float(whole_gain) else 0.0
        derived.add(f"{stayed:.2f}")
    # ونِسَبُ السقف مُشتَقّةٌ كذلك — وتُعاد **بعينها** لا بجدول ضربٍ
    morph = (DEPOSITS / "morph_residue_run.log").read_text(encoding="utf-8")

    def _read(pattern: str, where: str = morph) -> float:
        found = re.search(pattern, where)
        assert found is not None, pattern
        return float(found.group(1))

    field = _read(r"— خاناتُ الحال: 8 \| H = ([0-9.]+)")
    held = _read(r"مجموعُ الكسب المحجوز: \+([0-9.]+)", logs)
    shape = _read(r"— I\(الحال؛ه\) محجوزةً: \+([0-9.]+)")
    ceiling = _read(r"— وسقفُ ما يزيده الجارُ بعد الصورة ملحَقًا: \+([0-9.]+)")
    for one in (
        _read(r"— I\(الحال؛ج\) محجوزةً: \+([0-9.]+)"),
        _read(r"— I\(الحال؛ر\) محجوزةً: \+([0-9.]+)"),
        shape,
        ceiling,
    ):
        derived.add(f"{one / field:.4f}")
    derived.add(f"{shape / held:.2f}")
    counting = {str(one) for one in range(0, len(rows) + 1)} | {str(tool.BOXES)}
    figures = {one.translate(WESTERN) for one in re.findall(r"[٠-٩][٠-٩٫]*", body)}
    astray = sorted(
        figures - derived - counting - {one for one in figures if one in logs}
    )
    assert astray == [], astray
    for one in derived:
        assert tool.eastern(one) in body, one


def test_the_strongest_bit_is_the_positional_one() -> None:
    """أكبرُ بتّةٍ بتّةُ موضعٍ — والوثيقةُ تقول ذلك، والسجلُّ يشهد."""

    tool = _tool()
    ladder = (DEPOSITS / "context_ladder_run.log").read_text(encoding="utf-8")
    rows = tool.steps(ladder)
    best = max(rows, key=lambda one: float(one[2]))
    assert best[0] == "1", best
    assert tool.family_of(best[1]) == "آخرُ السطر"
    assert float(best[2]) > 2 * max(float(one[2]) for one in rows[1:])
    written = BRIDGE.read_text(encoding="utf-8")
    assert "**وهي بتّةُ موضعٍ لا بتّةُ نحو**" in written


def test_no_line_claims_a_proven_linguistic_meaning() -> None:
    """لا سطرَ يقول «بُرهن» عن مدلولٍ لغويّ — والنفيُ مكتوبٌ بنصّه."""

    written = BRIDGE.read_text(encoding="utf-8")
    assert "**لا بتّةَ ههنا بُرهنت إفادتُها اللغويّة.**" in written
    assert "**ولا جسرَ ههنا مُرخَّص**" in written
    assert "**ولا تُوقِّع الآلةُ ما صاغته**" in written
    assert "**والمُرخَّصُ صفرٌ**" in written
    for one in written.splitlines():
        if "بُرهن" in one and "لغوي" in one:
            assert one.lstrip().startswith("- **لا بتّةَ"), one


def test_the_signature_is_carried_in_the_bridge_and_bound_to_it() -> None:
    """الجسرُ يحمل المُوقِّعَ وبصمةَ ما وُقِّع عليه — ولا يُقرَأ ترخيصًا."""

    tool = _tool()
    hand = _signature()
    written = BRIDGE.read_text(encoding="utf-8")
    assert hand.FROZEN_SIGNATURE.readings[:16] in written
    assert hand.FROZEN_SIGNATURE.signer in written
    assert hand.rederive_readings_digest(tool.FAMILIES) == (
        hand.FROZEN_SIGNATURE.readings
    )
    assert hand.verify_against_logs() == []
    assert hand.FROZEN_SIGNATURE.licenses == ()
    assert "موقَّعٌ فرضًا، غيرُ مُرخَّصٍ برهانًا" in written
    for name in tool.FAMILIES:
        assert f"### «{name}»" in written, name


def test_the_families_are_exhaustive_over_the_questions() -> None:
    """كلُّ سؤالٍ في السجلّ يقع في عائلةٍ — وسؤالٌ بلا عائلةٍ يردُّ التوليد."""

    tool = _tool()
    with pytest.raises(SystemExit):
        tool.family_of("سؤالٌ لم يُعلَن")
