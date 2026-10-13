"""بوّابةُ المدلول وحده (ADR ٩): مرآةُ `formal/Madlul.lean` — لا نصَّ هنا.

المرجعُ ألفاظٌ (أعدادُ شهاداتٍ من بوّابة الغانم) أو عقدةُ معنًى من مودَعٍ مختوم؛ والمودَعُ يقول لكلّ مرجعٍ
شاهدَه. الأقسامُ الخمسة (ج3 س409): معنى، مفردٌ مستعمل، مفردٌ مهمل، مركّبٌ مستعمل، مركّبٌ مهمل. وما لا
شاهدَ له رفضٌ باسمه: لا يُحكم بإهمال لفظٍ من غياب شاهد استعماله (المادّة ١٦).
"""

from __future__ import annotations

from collections.abc import Callable, Hashable, Sequence
from dataclasses import dataclass
from typing import Final

__all__ = ["NAW", "QISM", "RAFD", "Madlul", "Mawda", "Rafd", "enter", "exit_ref", "qism"]

QISM: Final[tuple[str, ...]] = (
    "maana", "mufradMustamal", "mufradMuhmal", "murakkabMustamal", "murakkabMuhmal")
NAW: Final[tuple[str, ...]] = ("jins", "mushtaq", "alam", "damir")
ISTI: Final[tuple[str, ...]] = ("mustamal", "muhmal")
RAFD: Final[tuple[str, ...]] = ("EMPTY_LAFZ_REF", "MAANA_WITHOUT_WITNESS", "ISTI_WITHOUT_WITNESS")

Ref = tuple[str, Hashable]
"""("N", عقدة) أو ("L", ألفاظ)."""


@dataclass(frozen=True)
class Madlul:
    kind: str  # "maana" | "mufrad" | "murakkab"
    ref: Hashable  # العقدة، أو اللفظ، أو الألفاظ
    sub: str  # نوعُ المعنى أو الاستعمال
    witness: Hashable


@dataclass(frozen=True)
class Rafd:
    name: str


@dataclass(frozen=True)
class Mawda:
    naw: Callable[[Hashable], tuple[str, Hashable] | None]
    isti: Callable[[tuple[Hashable, ...]], tuple[str, Hashable] | None]


def enter(d: Mawda, ref: Ref) -> Madlul | Rafd:
    tag, x = ref
    if tag == "N":
        got = d.naw(x)
        return Rafd("MAANA_WITHOUT_WITNESS") if got is None else Madlul("maana", x, *got)
    ls = tuple(x) if isinstance(x, Sequence) else (x,)
    if not ls:
        return Rafd("EMPTY_LAFZ_REF")
    got = d.isti(ls)
    if got is None:
        return Rafd("ISTI_WITHOUT_WITNESS")
    if len(ls) == 1:
        return Madlul("mufrad", ls[0], *got)
    return Madlul("murakkab", ls, *got)


def exit_ref(m: Madlul) -> Ref:
    if m.kind == "maana":
        return ("N", m.ref)
    if m.kind == "mufrad":
        return ("L", (m.ref,))
    ref = m.ref
    assert isinstance(ref, tuple)
    return ("L", ref)


def qism(m: Madlul) -> str:
    if m.kind == "maana":
        return "maana"
    return m.kind + ("Mustamal" if m.sub == "mustamal" else "Muhmal")
