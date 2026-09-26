"""السقفُ مبرهَنٌ بالبناء، والتحليلُ محدودُ النطاق بنصّه.

**ما يحرسه**: أنّ **شطرَ الشدّة لا يكون آخرَ لفظه ألبتّة** — يُبرهَن
بالبناء ويُقابَل بالمقيس (صفرٌ من ٨١٧ ومن ٣٬٢٤٤). وأنّ **السقفَ** الذي
يفرضه ذلك على النسبة مقروءٌ من السجلّ لا مكتوبٌ. وأنّ تحليلَ تعليقِ ‎#45
**يُسمّي ما لم يُوقَّع عليه** — فلا يُقرَأ تصديقًا على ما لم يُحقَّق.

**وحدُّه**: يحرس **شكلَ التحليل ومقاديرَه**، ولا يحرس صوابَ ما في الفرع
الآخر — **فذاك يُقرَأ من تاريخه لا من ههنا**.
"""

from __future__ import annotations

import importlib.util
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[2]
DEPOSITS = REPOSITORY / "deposits"
WITNESS = DEPOSITS / "gemination_ceiling_witness.log"
ANALYSIS = DEPOSITS / "pr45_analysis.md"
WATCHED = ("0645", "062A")
THEIRS_TWIN = 817
THEIRS_SHARE = 0.2703


def _run() -> Any:
    path = REPOSITORY / "examples" / "rasm" / "run_gemination_ceiling.py"
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _block(point: str) -> dict[str, str]:
    text = WITNESS.read_text(encoding="utf-8")
    part = text.split(f"— الساكنُ U+{point}", 1)[1].split("\n\n", 1)[0]
    return {
        "whole": re.search(r"جملةً: (\d+)", part).group(1),  # type: ignore[union-attr]
        "final": re.search(r"آخرَ لفظه: (\d+)", part).group(1),  # type: ignore[union-attr]
        "twin": re.search(r"شطرُ شدّةٍ: (\d+)", part).group(1),  # type: ignore[union-attr]
        "twin_final": re.search(r"ومنها آخرَ لفظه: (\d+)", part).group(1),  # type: ignore[union-attr]
        "clean": re.search(r"مكتوبٌ في المدوّنة: (\d+)", part).group(1),  # type: ignore[union-attr]
        "ceiling": re.search(r"السقفُ الأعلى الممكن\*\*: ([0-9.]+)", part).group(1),  # type: ignore[union-attr]
    }


def test_a_geminate_half_is_never_word_final_by_construction() -> None:
    """الشطرُ الأوّلُ يتبعه الثاني في اللفظ — فلا يقع آخرًا، بناءً ومقيسًا."""

    run = _run()
    for word in ("حَتَّى", "ثُمَّ", "الَّذِينَ"):
        found = run.pieces_of(word)
        for place, (piece, twin) in enumerate(found):
            if twin:
                assert place < len(found) - 1, (word, piece)
                assert piece.endswith(run.SUKUN)
    for point in WATCHED:
        assert int(_block(point)["twin_final"]) == 0, point


def test_the_ceiling_is_derived_and_read_not_typed() -> None:
    """السقفُ = (الجملة − الأشطار) ÷ الجملة — يُعاد اشتقاقُه من السجلّ."""

    for point in WATCHED:
        rows = _block(point)
        whole = int(rows["whole"])
        clean = int(rows["clean"])
        assert clean == whole - int(rows["twin"])
        assert abs(clean / whole - float(rows["ceiling"])) < 5e-5
        assert int(rows["final"]) <= clean  # والبسطُ لا يفوق النظيف


def test_the_diagnosis_of_pr45_is_independently_confirmed() -> None:
    """الـ٨١٧ تطابق عدّي، والنسبةُ تطابق إلى أربع منازل."""

    rows = _block("062A")
    assert int(rows["twin"]) == THEIRS_TWIN
    share = int(rows["final"]) / int(rows["whole"])
    assert abs(share - THEIRS_SHARE) < 5e-4
    text = ANALYSIS.read_text(encoding="utf-8")
    assert "**٨١٧** | **٨١٧** — مطابقٌ تمامًا" in text


def test_the_same_confound_sits_in_the_condition_that_stood() -> None:
    """العطلُ نفسُه في «مْ» — ولم يُفحَص لأنّه صمد، ويُقال ذلك."""

    mim = _block("0645")
    assert int(mim["twin"]) == 3_244
    lifted = int(mim["final"]) / int(mim["clean"])
    assert lifted > 0.87
    text = ANALYSIS.read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert "**وتدقيقٌ يُسأل عند الخسارة وحدَها متحيّزٌ بالبناء**" in flat
    assert "٠٫٨٧٨٦" in text


def test_the_analysis_names_what_it_does_not_sign() -> None:
    """ما لم يُحقَّق يُسمّى — فلا يُقرَأ التوقيعُ تصديقًا عليه."""

    text = ANALYSIS.read_text(encoding="utf-8")
    assert "## ما **لم** يُوقَّع عليه" in text
    for row in ("الـ١٬٦٨٠", "الـ٨٢٤", "الاقتباساتُ الخمسةَ عشرَ"):
        assert row in text, row
    flat = " ".join(text.split())
    assert "**وهذا توقيعُ وكالةٍ لا توقيعُ أصيل**" in flat
    assert "**واليدُ يدُ الآلة**" in flat
    assert "**والصائغُ هو الوكيلُ نفسُه**" in flat
    assert "ولا يُقرَأ شهادةً مستقلّة" in flat


def test_the_analysis_upholds_the_fall_and_the_constitution() -> None:
    """السقوطُ يبقى سقوطًا — والمادّةُ ٢ تُذكَر باسمها."""

    text = ANALYSIS.read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert "**سقوطُ ك٤ يبقى سقوطًا كما خُتِم، ولا يُقلَب إلّا بختمٍ جديد.**" in flat
    assert "لا يُعاد تفسيرُ شرطٍ بعد النظر" in flat
    assert "**شرطٌ حدُّه فوق سقفِه شرطٌ لا يُختبَر**" in flat
    register = (REPOSITORY / "docs" / "دستور-القياس.md").read_text(encoding="utf-8")
    assert "لا يُعاد تفسيرُ شرطٍ بعد النظر" in register


def test_the_old_failure_is_named_as_flaw_twenty_five() -> None:
    """«الفشلُ القديم» ليس أجنبيًّا — هو العطل ٢٥ وعلاجُه في الشجرة."""

    text = ANALYSIS.read_text(encoding="utf-8")
    assert "هو العطل ٢٥" in text
    assert "test_deposits_are_tracked.py" in text
    register = (REPOSITORY / "docs" / "سجل-الأعطال.md").read_text(encoding="utf-8")
    assert "## ٢٥) ثلاثةٌ وثلاثون شاهدًا خارجَ المستودع" in register


def test_no_name_from_outside_the_bytes_entered_the_witness() -> None:
    """السجلُّ نقاطُ ترميزٍ ووحداتٌ — لا اسمَ بابٍ ولا يونيكود."""

    text = WITNESS.read_text(encoding="utf-8")
    for word in ("ARABIC", "سكون", "تنوين", "إعراب", "مرفوع", "مجرور"):
        assert word not in text.split("— ما لا يدخل هذا السجلّ")[0], word
    assert unicodedata.name("ّ").startswith("ARABIC")  # الشدّةُ اسمُها خارجٌ


def _proxy() -> Any:
    path = REPOSITORY / "tools" / "pr45_signature.py"
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_the_proxy_signature_carries_the_principals_name_and_the_agents_hand() -> None:
    """الاسمُ اسمُ الأصيل، واليدُ يدُ الوكيل — والإفصاحُ لازمٌ في البناء."""

    tool = _proxy()
    record = tool.FROZEN_PROXY
    assert tool.verify_against_logs() == []
    assert record.signer.endswith("Saleh1967")
    assert record.executed_by != record.signer
    assert record.drafter == record.executed_by
    assert record.signer in record.authority
    assert tool.rederive_record_digest() == tool.RECORD_DIGEST


def test_a_proxy_that_hides_its_agency_is_refused() -> None:
    """توقيعٌ يُخفي وكالتَه **يُردّ** — ولا يُترَك للنثر."""

    from dataclasses import replace

    import pytest

    tool = _proxy()
    record = tool.FROZEN_PROXY
    for bad in (
        {"authority": ""},
        {"authority": "تفويضٌ من فلان"},  # لا يُسمّي صاحبَ الاسم
        {"authority_dated": ""},
        {"drafter": "صاحبُ المستودع"},
        {"signer": "آلةُ القياس"},  # الآلةُ لا تكون اسمًا
        {"signer": "  "},
        {"signed_scope": ()},
        {"withheld_scope": ()},
    ):
        with pytest.raises(tool.ProxySignatureError):
            replace(record, **bad)
    # وأصيلٌ يحمل سندَ وكالةٍ تلبيسٌ يُردّ
    with pytest.raises(tool.ProxySignatureError):
        replace(record, executed_by=record.signer, drafter=record.signer)


def test_the_signed_scope_is_only_what_was_verified_here() -> None:
    """الموقَّعُ عليه ما حُقِّق على المدوّنة — وكلُّ بندٍ له شاهدٌ في السجلّ."""

    tool = _proxy()
    record = tool.FROZEN_PROXY
    assert len(record.signed_scope) == 5
    assert len(record.withheld_scope) == 5
    text = ANALYSIS.read_text(encoding="utf-8")
    for row in ("٨١٧", "٠٫٢٧٠٢", "٠٫٤٥٥٠", "٠٫٦٥٦٤", "٠٫٨٧٨٦"):
        assert row in text, row
    witness = WITNESS.read_text(encoding="utf-8")
    for row in ("817", "0.2702", "0.4550", "0.6564", "0.8786"):
        assert row in witness, row
