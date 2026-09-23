"""النسختان جنبًا إلى جنب: الواردةُ كما وصلت، والمنقّحةُ — ليُفحَص الفرقُ لا يُوصَف.

**لماذا ههنا لا في `algebra`**: هذه شيفرةُ عربيّةٍ بمحارفَ وقواعدَ لسانٍ
بعينه، و`algebra` لا تحمل ذلك. وهي ليست اختبارًا في نفسها بل **مادّةُ**
اختبارٍ: `test_harf_rules_executed` يُشغّلها ويُثبِت ثلاثةَ أشياءَ لا تُقبَل
بالنظر — أنّ خللًا كان، وأنّه زال، وأنّ ما لم يُقصَد لم يتبدّل.

`received_irab_of` منقولةٌ عن النسخة الواردة بسلوكها لا بحرفها: أُعيد ترتيبُ
ما يلزمه المُنسِّق، ولم يُغيَّر شرطٌ ولا ترتيبُ قاعدةٍ ولا قيمةُ ثابت. وفحصُ
ذلك أنّ مخارجَها في الاختبار هي المخارجُ المنشورةُ في تقرير صاحبها.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping, Sequence
from typing import Any

HARAKA: dict[str, str] = {
    "ُ": "raf'",
    "ٌ": "raf'",
    "َ": "nasb",
    "ً": "nasb",
    "ِ": "jarr",
    "ٍ": "jarr",
}
SUKUN = "ْ"
TANWEEN = {"ً", "ٌ", "ٍ"}
SMALL = re.compile("[ۖ-ۭـ ⁠]")
BASE = {chr(code) for code in range(0x0621, 0x064B)} | {"ٱ", "ى", "ة"}
CARRIER = {"ا", "ى"}
PRON_SUF = {"ه", "هم", "هما", "هن", "ها", "ك", "كم", "كما", "كن", "نا", "ي", "ني"}
LETTER_SUF: dict[str, set[str]] = {
    "ون": {"raf'"},
    "ين": {"nasb", "jarr"},
    "ان": {"raf'"},
}
DEFINITE = {"ال", "ٱل"}

RAF, NASB, JARR = "raf'", "nasb", "jarr"
NO_CASE = "لا إعراب"
"""حكمٌ: لا علامةَ لهذا الرمز."""
DEFER = "لم يُحسَم"
"""امتناعٌ عن علم: لا أدري — وهو غيرُ الذي قبله، والفرقُ يغيّر الحساب."""

OUTCOMES = (RAF, NASB, JARR, NO_CASE, DEFER)
ALL_RULES = ("ق٠", "ق١", "ق٢", "ق٣", "ق٤", "ق٥", "ق٥و", "ق٦")
SEALED_RULES = tuple(rule for rule in ALL_RULES if rule != "ق٥و")
"""ما خُتِم: بلا «ق٥و» — توسيعُ الامتناع إلى الفعل، وهو لاحقٌ على الختم."""

Record = Mapping[str, Any]


def clean(text: str) -> str:
    return SMALL.sub("", text or "")


def _base_positions(text: str) -> list[int]:
    return [index for index, char in enumerate(text) if char in BASE]


def _marks_after(text: str, positions: list[int], slot: int) -> str:
    end = positions[slot + 1] if slot + 1 < len(positions) else len(text)
    return text[positions[slot] + 1 : end]


def drop_last_letters(text: str, count: int) -> str:
    """يُسقط آخرَ `count` حرفِ أساسٍ مع علاماتها."""

    positions = _base_positions(text)
    if count <= 0 or len(positions) <= count:
        return text
    return text[: positions[len(positions) - count]]


def final_mark(text: str) -> str | None:
    """محرفُ الضبط الأخير كما هو — لا الحالةَ المشتقّةَ منه.

    وفصلُهما شرطُ ق٦: «فتحةٌ بلا تنوين» فرقٌ بين «َ» و«ً»، والحالةُ تخلطهما
    إذ ترُدّهما جميعًا إلى `nasb`.
    """

    if not text:
        return None
    positions = _base_positions(text)
    if not positions:
        return None
    slot = len(positions) - 1
    tail = _marks_after(text, positions, slot)
    carried = text[positions[slot]] in CARRIER
    if carried and not any(ch in HARAKA or ch == SUKUN for ch in tail) and slot > 0:
        slot -= 1
    for char in _marks_after(text, positions, slot):
        if char in HARAKA:
            return char
        if char == SUKUN:
            return None
    return None


def haraka_case(text: str) -> str | None:
    """حالةُ الحرف الحامل — سلوكٌ مطابقٌ للنسخة الواردة."""

    mark = final_mark(text)
    return HARAKA[mark] if mark else None


# ==================================================== النسخةُ الواردةُ كما وصلت


def received_is_no_case(rec: Record) -> bool:
    """ق٥ كما نُفِّذت: `pos in ("harf", "fi'l")` — والفعلُ ليس في المختوم."""

    if rec.get("pos") in ("harf", "fi'l"):
        return True
    components = rec.get("components") or []
    return any(one.get("kind") == "deictic" for one in components)


def received_irab_of(
    rec: Record, prev_is_jarr_harf: bool = False
) -> tuple[str | None, str]:
    """النسخةُ الواردة. تُعيد `None` للتأجيل و`NO_CASE` للامتناع — وهما اثنان."""

    if received_is_no_case(rec):
        return NO_CASE, "L9-R5-imtina"
    surface = clean(str(rec.get("surface", "")))
    suffixes = list(rec.get("suffixes") or [])
    if suffixes:
        last = suffixes[-1]
        if last in LETTER_SUF:
            cases = LETTER_SUF[last]
            if len(cases) == 1:
                return next(iter(cases)), "L9-R0c-harf"
            return (JARR if prev_is_jarr_harf else NASB), "L9-R0c-harf+فضّ"
        if last in PRON_SUF:
            core = drop_last_letters(surface, sum(1 for ch in last if ch in BASE))
            settled = haraka_case(core)
            return (settled, "L9-R0c-pron") if settled else (None, "defer")
    diptote = (
        prev_is_jarr_harf
        and not surface.startswith(("ال", "ٱل"))
        and haraka_case(surface) == NASB
        and not (set(surface) & TANWEEN)
    )
    if diptote:
        return JARR, "L9-R6-diptote"
    settled = haraka_case(surface)
    return (settled, "L9-R0-tashkil") if settled else (None, "defer")


# ======================================================== النسخةُ المنقّحة


def revised_is_no_case(
    rec: Record,
    rules: Iterable[str] = ALL_RULES,
    oracle_pos: str | None = None,
) -> tuple[bool, str]:
    """ق٥ المختومةُ وق٥و التوسيعُ برايتين، فيُقاس كلٌّ منهما وحدَه."""

    enabled = set(rules)
    pos = oracle_pos if oracle_pos is not None else rec.get("pos")
    if "ق٥" in enabled and pos == "harf":
        return True, "ق٥ حرف"
    if "ق٥و" in enabled and pos == "fi'l":
        return True, "ق٥و فعل — توسيعٌ بعد الختم"
    if "ق٥" in enabled:
        for component in rec.get("components") or []:
            if component.get("kind") == "deictic":
                return True, "ق٥ مبنيُّ إحالة"
    return False, ""


def revised_irab_of(
    rec: Record,
    prev_is_jarr_harf: bool = False,
    *,
    rules: Iterable[str] = ALL_RULES,
    oracle_pos: str | None = None,
) -> tuple[str, str]:
    """تُعيد مخرجًا من الخمسة دائمًا، ولا تُعيد `None` أبدًا."""

    enabled = set(rules)
    refused, why = revised_is_no_case(rec, rules=rules, oracle_pos=oracle_pos)
    if refused:
        return NO_CASE, f"L9-R0e-imtina · {why}"

    surface = clean(str(rec.get("surface", "")))
    suffixes = list(rec.get("suffixes") or [])
    prefixes: Sequence[str] = list(rec.get("prefixes") or [])

    if suffixes:
        last = suffixes[-1]
        if "ق١" in enabled and last in LETTER_SUF:
            cases = LETTER_SUF[last]
            if len(cases) == 1:
                return next(iter(cases)), "L9-R0e-harf"
            if "ق٢" not in enabled:
                return DEFER, "defer(ق٢ معطَّلة)"
            return (JARR if prev_is_jarr_harf else NASB), "L9-R0e-harf+فضّ"
        if "ق٤" in enabled and last == "ات":
            mark = final_mark(surface)
            if mark in ("ُ", "ٌ"):
                return RAF, "L9-R0e-aat"
            if mark in ("ِ", "ٍ"):
                if "ق٢" not in enabled:
                    return DEFER, "defer(ق٢ معطَّلة)"
                return (JARR if prev_is_jarr_harf else NASB), "L9-R0e-aat+فضّ"
            return DEFER, "defer"
        if "ق٠" in enabled and last in PRON_SUF:
            core = drop_last_letters(surface, sum(1 for ch in last if ch in BASE))
            settled = haraka_case(core)
            return (settled, "L9-R0e-pron") if settled else (DEFER, "defer")

    if "ق٦" in enabled and prev_is_jarr_harf:
        definite = any(one in DEFINITE for one in prefixes)
        if final_mark(surface) == "َ" and not definite:
            return JARR, "L9-R0e-diptote"

    if "ق٣" in enabled:
        settled = haraka_case(surface)
        if settled:
            return settled, "L9-R0e-tashkil"
    return DEFER, "defer"


def four_way(outcome: str, *, defer_counts_as: str) -> str:
    """التحويلُ إلى المقياس الرباعيّ — **بلا قيمةٍ افتراضيّة**.

    التسجيلُ يُعلن أربعةَ أصناف، والنظامُ يُخرِج خمسة. فمصيرُ `DEFER` قرارٌ
    يُعلَن قبل التشغيل: حسابُه «لا إعراب» يرفع الحكمَ بلا استحقاق، وحسابُه
    خطأً يخفضه. ولا ثالثَ، ولا سكوت.
    """

    if defer_counts_as not in (NO_CASE, "خطأ"):
        raise ValueError(
            "مصيرُ «لم يُحسَم» يُعلَن قبل التشغيل: «لا إعراب» أو «خطأ»؛ "
            "ولا قيمةَ افتراضيّةَ هنا لأنّ الافتراضَ يغيّر الحكمَ صمتًا."
        )
    if outcome == DEFER:
        return NO_CASE if defer_counts_as == NO_CASE else "خطأٌ مُعلَن"
    return outcome


def record(
    surface: str,
    *,
    pos: str | None = None,
    suffixes: Sequence[str] = (),
    prefixes: Sequence[str] = (),
    deictic: bool = False,
) -> dict[str, Any]:
    """سجلُّ رمزٍ كما تُخرِجه الطبقاتُ — لا تخمينَ في الاختبار كما لا تخمينَ فيها."""

    return {
        "surface": surface,
        "pos": pos,
        "suffixes": list(suffixes),
        "prefixes": list(prefixes),
        "components": [{"kind": "deictic"}] if deictic else [],
    }
