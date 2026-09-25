"""سلّمُ السياق مُجمَّدًا — والشكلُ قيدٌ في المُنشئ لا نثرٌ يتبدّل.

**ما يُفحَص ههنا**: أنّ بصمةَ السجلّ **تُشتَقّ من حقوله**، وأنّ كلَّ حقلٍ
**مقابَلٌ بالسجلّات المُودَعة**، وأنّ **شكلَ النتيجة مردودٌ ببنائه** — فمن
بدّل رقمًا ليُلطّف النتيجةَ رُدَّ سجلُّه.

`NO_GLYPH_OF_THE_CORPUS_IS_TYPED_IN_THE_RECORD`: **ولا محرفَ من المجمَّد
مكتوبٌ في السجلّ**: الأسئلةُ محفوظةٌ **بصنفها ونقطةِ ترميزها**، وصورتُها
تُقرَأ من السجلّ المُودَع عند التحقّق — وهو العطلُ الثاني، ممنوعًا بالبناء.
"""

from __future__ import annotations

import dataclasses
import importlib.util
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[2]
SEAL = REPOSITORY / "tools" / "context_ladder_seal.py"
LOG = REPOSITORY / "deposits" / "context_ladder_run.log"


def _seal() -> Any:
    spec = importlib.util.spec_from_file_location("context_ladder_seal", SEAL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_the_record_digest_is_rederived_from_its_fields() -> None:
    """البصمةُ تُشتَقّ من الحقول لا تُنقَل."""

    tool = _seal()
    assert tool.rederive_record_digest() == tool.RECORD_DIGEST
    assert tool.RECORD_DIGEST.startswith("041cdcf4")


def test_every_field_is_witnessed_in_the_deposited_logs() -> None:
    """كلُّ حقلٍ له شاهدٌ في السجلّات الثلاثة، وما خالف يُسمّى."""

    tool = _seal()
    assert tool.verify_against_logs() == []


def test_the_question_values_are_codepoints_not_typed_glyphs() -> None:
    """قيمُ الأسئلة **نقاطُ ترميز**، وصورتُها تُقرَأ من السجلّ المُودَع.

    **وحدُّ هذا الفحص مُعلَن**: يحرس **قيمَ الأسئلة** — وهي بيانُ المجمَّد —
    فلا تُكتَب شريحةٌ بيد. **ولا يحرس نثرَ السجلّ**: أسماءُ الأصناف عربيّةٌ
    بالضرورة، وفيها حروفٌ وعلاماتٌ مكتوبة. فالمحروسُ **ما نُقِل عن
    المجمَّد**، لا **ما كُتِب عنه**.
    """

    tool = _seal()
    record = tool.FROZEN_CONTEXT
    marks = [one for one in record.points if one.startswith("U+")]
    assert len(marks) == 9
    text = LOG.read_text(encoding="utf-8")
    for point in marks:
        glyph = chr(int(point[2:], 16))
        assert glyph not in record.points  # لم تُكتَب الشريحةُ قيمةً
        assert f"{glyph} {point}" in text  # وهي في السجلّ شريحةً ونقطة
    for one in record.points:
        if one and not one.startswith("U+"):
            assert len(one) == 1
            assert not unicodedata.name(one, "").startswith("ARABIC")
    assert re.search(r"points=\(", SEAL.read_text(encoding="utf-8"))


def test_the_shape_of_the_finding_is_enforced_by_the_constructor() -> None:
    """من بدّل رقمًا ليُلطّف النتيجةَ رُدَّ سجلُّه — تسعُ محاولاتِ تبديل."""

    tool = _seal()
    record = tool.FROZEN_CONTEXT
    worse = list(record.inside)
    worse[3] = "2.9999"  # ملحَقةٌ ترتفع
    lower = list(record.outside)
    lower[0] = "2.0000"  # محجوزةٌ تحت ملحَقتها
    dead = list(record.gains_out)
    dead[5] = "0.0000"  # درجةٌ لا تربح
    piled = list(record.gains_out)
    piled[3] = "0.9000"  # أكبرُ ربحٍ في غير الأولى
    wide = list(record.blocks)
    wide[1] = 99  # سؤالٌ يزيد الكتلَ على الضعف
    for name, value in (
        ("inside", tuple(worse)),
        ("outside", tuple(lower)),
        ("gains_out", tuple(dead)),
        ("gains_out", tuple(piled)),
        ("blocks", tuple(wide)),
        ("kinds", ("حالُ السابق",) + record.kinds[1:]),
        ("whole_out", "0.0100"),
        ("positional", "0.9000"),
        ("unreached", ()),
    ):
        try:
            dataclasses.replace(record, **{name: value})
        except tool.ContextLadderError:
            continue
        raise AssertionError(f"مرَّ حقلٌ مبدَّلٌ بلا ردّ: {name}")


def test_the_meeting_of_two_seals_is_guarded_not_narrated() -> None:
    """ربحُ الأولى يُقابَل بما قِيس في `26ae5b5b…` — والتباعدُ يردُّ السجلّ."""

    tool = _seal()
    record = tool.FROZEN_CONTEXT
    apart = abs(float(record.gains_out[0]) - float(record.positional))
    assert apart < 5e-4
    assert record.kinds[0] == tool.POSITIONAL
    assert float(record.gains_out[0]) == max(float(one) for one in record.gains_out)


def test_the_ladder_beats_the_neighbour_and_the_debt_is_carried() -> None:
    """مجموعُ الكسب يتجاوز الجارَ كلَّه، وما لم يُبلَغ محمولٌ بنصّه."""

    tool = _seal()
    record = tool.FROZEN_CONTEXT
    assert float(record.whole_out) / float(record.neighbour) > 3
    assert float(record.whole_in) > float(record.whole_out)
    assert len(record.unreached) == 3
    joined = " ".join(why for _, why in record.unreached)
    assert "الوقوفُ لم يقع" in joined
    assert "الجشعُ غيرُ مبرهَن" in joined
    assert "جوابٌ لا سؤال" in joined
    assert sum(two for _, two in record.tally) == len(record.kinds)
    assert tool.HEAD not in {one for one, _ in record.tally}
