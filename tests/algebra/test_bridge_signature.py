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
import re
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


def test_a_machine_signs_only_under_a_recorded_delegation() -> None:
    """توقيعٌ آليٌّ بلا تفويضٍ مُسجَّلٍ **يُردّ** — المادّة ٢٧ مفحوصةً."""

    tool = _tool("bridge_signature.py")
    signed = tool.FROZEN_SIGNATURE
    assert any(one in signed.signer for one in tool._MACHINES)
    for bad in (
        {"delegated_by": ""},
        {"delegated_by": "   "},
        {"delegated_by": "الآلة"},
        {"delegation_dated": ""},
    ):
        with pytest.raises(tool.BridgeSignatureError):
            replace(signed, **bad)
    with pytest.raises(tool.BridgeSignatureError):
        replace(signed, signer="   ")
    register = (REPOSITORY / "docs" / "دستور-القياس.md").read_text(encoding="utf-8")
    assert "**التوقيعُ فعلُ صاحب المستودع لا فعلُ الآلة**" in register


def test_a_delegated_machine_signature_must_disclose_the_double_role() -> None:
    """**التفويضُ لا يُزيل الدور**: توقيعٌ يُخفي أنّ الصائغَ هو المُوقِّع يُردّ."""

    tool = _tool("bridge_signature.py")
    signed = tool.FROZEN_SIGNATURE
    assert signed.drafter == signed.signer
    assert "تصديقُ المؤلِّف" in signed.adopts_as
    with pytest.raises(tool.BridgeSignatureError):
        replace(signed, drafter="صاحبُ المستودع")
    with pytest.raises(tool.BridgeSignatureError):
        replace(
            signed,
            adopts_as="تبنٍّ للقراءات فرضًا معلَنًا قابلًا للسقوط",
        )
    # ومُوقِّعٌ بشريٌّ لا يُسنِد الصياغةَ إلى نفسه — فالصائغُ الآلة
    with pytest.raises(tool.BridgeSignatureError):
        replace(signed, signer="فلانٌ", drafter="فلانٌ", delegated_by="")


def test_the_deposit_carries_the_disclosure_in_words() -> None:
    """الإفصاحُ مكتوبٌ في الإيداع لا في الشفرة وحدَها."""

    tool = _tool("bridge_signature.py")
    assert tool.verify_against_logs() == []
    flat = " ".join(SIGNED.read_text(encoding="utf-8").split())
    for row in (
        "**الصائغُ هو المُوقِّع**",
        "تصديقُ المؤلِّف على ما ألَّف",
        "ولا يُقرَأ شهادةً مستقلّة",
        "**وكيلٌ بتفويضٍ، لا أصيل**",
        "والتفويضُ يُجيز الفعلَ **ولا يُزيل الدور**",
        "**من فوَّض**: صاحبُ المستودع — Saleh1967",
        "وكالةً عن صاحب المستودع",
    ):
        assert row in flat, row


def test_a_licence_stands_only_on_a_deposited_table() -> None:
    """الترخيصُ لا يقوم إلّا على جدولٍ مُودَع — وترخيصٌ بلا جدولٍ يُردّ."""

    tool = _tool("bridge_signature.py")
    signed = tool.FROZEN_SIGNATURE
    assert len(signed.licenses) == signed.families == 4
    assert signed.tables == tool.TABLES
    assert (DEPOSITS / signed.tables).is_file()
    with pytest.raises(tool.BridgeSignatureError):
        replace(signed, tables="")
    with pytest.raises(tool.BridgeSignatureError):
        replace(signed, tables="   ")
    with pytest.raises(tool.BridgeSignatureError):
        replace(signed, licenses=(*signed.licenses, "عائلةٌ خامسة"))
    with pytest.raises(tool.BridgeSignatureError):
        replace(signed, licenses=("حالُ السابق", "حالُ السابق"))


def test_a_licence_for_a_family_that_does_not_exist_is_named() -> None:
    """ترخيصٌ لعائلةٍ ليست في الجسر **يُسمّى** في الشكاوى."""

    tool = _tool("bridge_signature.py")
    bent = replace(
        tool.FROZEN_SIGNATURE,
        licenses=("آخرُ السطر", "حالُ السابق", "حالُ ما قبله", "لا عائلة"),
    )
    complaints = tool.verify_against_logs(bent)
    assert any("عائلةٍ غيرِ موجودة" in one for one in complaints), complaints


def test_every_licensed_family_has_a_row_in_the_deposited_tables() -> None:
    """الجداولُ الثلاثةُ مُودَعةٌ، وكلُّ صفٍّ يحمل استثناءَه المُعلَن."""

    tool = _tool("bridge_signature.py")
    tables = _tool("write_bridge_tables.py")
    rows = (DEPOSITS / tool.FROZEN_SIGNATURE.tables).read_text(encoding="utf-8")
    for row in ("جدولُ الأبواب", "جدولُ الصرف", "حدُّ الآية"):
        assert row in rows, row
    assert "فرضٌ إسناديٌّ أوّليٌّ" in rows
    for point, (reading, unless) in {**tables.IRAB, **tables.SARF}.items():
        assert f"`U+{point}`" in rows, point
        assert reading in rows, point
        assert unless in rows, point
        assert len(unless) >= 30, point
    assert tables.BOUND[0] in rows and tables.BOUND[1] in rows
    # ولا حرفَ عربيٍّ في مفاتيح الجداول — سداسيّاتٌ لا حروف
    for point in {**tables.IRAB, **tables.SARF}:
        assert re.fullmatch(r"[0-9A-F]{4}", point), point


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
    assert "**فالمُرخَّصُ أربعٌ، والمقيسُ من لوازمها صفرٌ بعد.**" in " ".join(text.split())
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
