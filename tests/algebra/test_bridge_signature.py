"""التوقيعُ مربوطٌ بما وُقِّع عليه، **والآلةُ لا تُوقِّع ألبتّة**.

**ما يحرسه**: أنّ بصمةَ القراءات الأربع تُعاد **الآن** وتُقابَل بالموقَّع
عليه — فتبديلُ حرفٍ في قراءةٍ **يكسر التوقيع**. وأنّ التوقيعَ **لا
يُرخِّص شيئًا**: كلُّ عائلةٍ يُذكَر ما يُلزَمها ولم يُودَع. وأنّ
المُوقِّعَ **إنسانٌ لا آلة** — وذلك المادّة ٢٧، **مفحوصةً لا مقولةً**.

**وحدُّه مُصرَّحٌ به**: يحرس **شكلَ التوقيع** لا **صوابَ القراءة**.
فقراءةٌ خاطئةٌ موقَّعةٌ بشكلٍ صحيحٍ تمرُّ عليه — **وإنّما يُنقَض ما وُقِّع
عليه بقياسٍ لا بفحصِ شكل**. وهذا هو نفعُ التوقيع: **يُدخِل القراءةَ في
دائرة النقض**.
"""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

REPOSITORY = Path(__file__).resolve().parents[2]
DEPOSITS = REPOSITORY / "deposits"
SIGNED = DEPOSITS / "bridge_signature.md"


def _tool(name: str) -> Any:
    path = REPOSITORY / "tools" / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None, name
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_the_signature_binds_to_the_readings_and_they_are_unchanged() -> None:
    """بصمةُ القراءات تُعاد الآن فتطابق الموقَّعَ عليه — أو يسقط الفحص."""

    tool = _tool("bridge_signature.py")
    assert tool.verify_against_logs() == []
    assert tool.rederive_readings_digest() == tool.FROZEN_SIGNATURE.readings
    assert tool.rederive_record_digest() == tool.RECORD_DIGEST
    assert len(tool.RECORD_DIGEST) == 64


def test_changing_one_letter_of_a_reading_breaks_the_signature() -> None:
    """تبديلُ حرفٍ في قراءةٍ **يكسر التوقيع** — وذلك مقصودُ الربط."""

    tool = _tool("bridge_signature.py")
    bridge = _tool("write_bit_bridge.py")
    signed = tool.FROZEN_SIGNATURE.readings
    assert tool.rederive_readings_digest(bridge.FAMILIES) == signed
    for name in bridge.FAMILIES:
        reading, kind, needed = bridge.FAMILIES[name]
        for bent in (
            {**bridge.FAMILIES, name: (reading + "ـ", kind, needed)},
            {**bridge.FAMILIES, name: (reading, kind + "ـ", needed)},
            {**bridge.FAMILIES, name: (reading, kind, needed + "ـ")},
        ):
            assert tool.rederive_readings_digest(bent) != signed, name
    # وحذفُ عائلةٍ يكسره كذلك — فالتوقيعُ على الأربع لا على واحدة
    fewer = {
        one: two
        for one, two in bridge.FAMILIES.items()
        if one != next(iter(bridge.FAMILIES))
    }
    assert tool.rederive_readings_digest(fewer) != signed


def test_the_machine_can_never_be_the_signer() -> None:
    """المادّة ٢٧ **مفحوصةً**: مُوقِّعٌ فيه اسمُ آلةٍ يُردّ."""

    tool = _tool("bridge_signature.py")
    for name in ("الآلة", "Claude", "المولّد", "آلةُ القياس"):
        with pytest.raises(tool.BridgeSignatureError):
            replace(tool.FROZEN_SIGNATURE, signer=name)
    with pytest.raises(tool.BridgeSignatureError):
        replace(tool.FROZEN_SIGNATURE, signer="   ")
    register = (REPOSITORY / "docs" / "دستور-القياس.md").read_text(encoding="utf-8")
    assert "**التوقيعُ فعلُ صاحب المستودع لا فعلُ الآلة**" in register


def test_a_signature_that_claims_a_licence_is_refused() -> None:
    """توقيعٌ يدّعي ترخيصًا يُردّ — ولا جدولَ مُودَعٌ يُرخِّص شيئًا."""

    tool = _tool("bridge_signature.py")
    with pytest.raises(tool.BridgeSignatureError):
        replace(tool.FROZEN_SIGNATURE, licenses=("حالُ السابق",))
    assert tool.FROZEN_SIGNATURE.licenses == ()
    assert len(tool.FROZEN_SIGNATURE.withheld) == tool.FROZEN_SIGNATURE.families


def test_a_signature_must_say_it_adopts_a_hypothesis_not_a_fact() -> None:
    """التوقيعُ تبنٍّ **فرضًا** — وصيغةٌ لا تقول ذلك تُردّ."""

    tool = _tool("bridge_signature.py")
    assert "فرض" in tool.FROZEN_SIGNATURE.adopts_as
    with pytest.raises(tool.BridgeSignatureError):
        replace(tool.FROZEN_SIGNATURE, adopts_as="إقرارٌ بأنّ القراءاتَ صحيحة")
    with pytest.raises(tool.BridgeSignatureError):
        replace(tool.FROZEN_SIGNATURE, withheld=())
    with pytest.raises(tool.BridgeSignatureError):
        replace(tool.FROZEN_SIGNATURE, families=0)


def test_the_deposit_names_every_family_and_what_is_withheld() -> None:
    """الإيداعُ يذكر كلَّ عائلةٍ وما لا يُرخَّص لها — ولا يُطوى واحد."""

    tool = _tool("bridge_signature.py")
    bridge = _tool("write_bit_bridge.py")
    text = SIGNED.read_text(encoding="utf-8")
    for name, (reading, kind, _) in bridge.FAMILIES.items():
        assert f"«{name}»" in text, name
        assert reading in text, name
        assert kind in text, name
    assert "**فالموقَّعُ عليه أربعةُ فروض، والمُرخَّصُ صفرٌ.**" in text
    assert "المادّة ٢٧" in text
    assert tool.FROZEN_SIGNATURE.readings in text


def test_the_signature_changes_no_measured_number() -> None:
    """التوقيعُ لا يُغيّر رقمًا — والسقفُ المقيسُ قائمٌ كما هو."""

    text = SIGNED.read_text(encoding="utf-8")
    morph = (DEPOSITS / "morph_residue_run.log").read_text(encoding="utf-8")
    assert "+١٫٢١٥٢٥٢" in text
    assert "1.215252" in morph
    assert "٠٫٠٣٩٧" in text
    assert "0.0397" in morph
    assert "**فالتوقيعُ تبنٍّ لفرضٍ داخلَ هذا السقف، لا نقضٌ له.**" in " ".join(text.split())
