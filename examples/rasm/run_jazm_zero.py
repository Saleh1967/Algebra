"""الجزمُ بلا هامش طردًا وعكسًا — تشغيلُ ختم `0dd2643d…`.

كلُّ تعريفٍ هنا نصُّ الاستخراج في الختم. وحيث احتمل النصُّ وجهين أُخذ بلفظه: «إِمَّا» بلا
سابقة، و«السكون» حالُ الوحدة «ْ» في التقشير كتبت أم لم تُكتب (فالألفُ العاريةُ الأخيرة
سكون)، و«ألفٌ عاريةٌ خامًا» أوّلَ اللفظ تشمل «ال».
"""

from __future__ import annotations

import argparse
import importlib.util
import random
import re
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from types import ModuleType

RASM = Path(__file__).resolve().parent
TABLE = RASM.parents[1] / "deposits" / "rafa_jazm_exceptions_draft.tsv"
FATHA, DAMMA, KASRA, SUKUN = "َ", "ُ", "ِ", "ْ"
SHORT = (FATHA, DAMMA, KASRA)
MARKS = re.compile("[ً-ْ]")
MUDARAA = "نيت"
CAUSES = {
    "لم",
    "لما",
    "لا",
    "إن",
    "إما",
    "من",
    "ما",
    "مهما",
    "متى",
    "أين",
    "أينما",
    "حيثما",
    "أيان",
    "أنى",
    "أي",
    "إذما",
    "كيفما",
    "هل",
}
REASONING_NOT_SUPPORTED: tuple[str, ...] = ()


def _load(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, RASM / f"{name}.py")
    if spec is None or spec.loader is None:
        raise RuntimeError(f"لا قارئَ لـ{name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


PEELER = _load("run_cv_peel")
GOVERNED = _load("run_governed_vowel")

Unit = tuple[tuple[str, str], dict[str, str]]


def units(token: str) -> list[Unit]:
    peeled, extras = PEELER.peel(token)
    return [
        (unit, extra)
        for unit, extra in zip(peeled, extras, strict=True)
        if unit[0] != PEELER.STRUCTURE and extra.get("تنوين") != "ذيل"
    ]


def raw(token: str) -> str:
    return MARKS.sub("", token)


def skeleton(kept: list[Unit]) -> str:
    return "".join(u[0] for u, extra in kept if extra.get("شدّة") != "نعم")


def key(kept: list[Unit]) -> tuple:
    """الجذع: الهيكلُ مع حال كلّ وحدةٍ إلّا الأخيرة، بعد طرح وَ/فَ."""

    if len(kept) > 1 and kept[0][0][0] in "وف" and kept[0][0][1] == FATHA:
        kept = kept[1:]
    if not kept:
        return ()
    return tuple(u for u, _ in kept[:-1]) + (kept[-1][0][0],)


def _hamza_above(unit: Unit) -> bool:
    return unit[0][0] == "ا" and unit[1].get("حامل") == "أ"


def _mudaraa(unit: Unit) -> bool:
    return (unit[0][0] in MUDARAA or _hamza_above(unit)) and unit[0][1] in (
        FATHA,
        DAMMA,
    )


def table() -> tuple[set[str], list[str]]:
    text = TABLE.read_text(encoding="utf-8")
    if "# التوقيع: موقَّع" not in text:
        raise RuntimeError("الجدولُ غيرُ موقَّع")
    built: set[str] = set()
    pronouns: list[str] = []
    for line in text.split("\n"):
        if not line or line.startswith("#"):
            continue
        name, forms, _ = line.split("\t")
        shapes = [one.strip() for one in forms.split(",") if one.strip()]
        if name.startswith("مبنيّ:") and "نون" not in name:
            built |= {skeleton(units(one)) for one in shapes}
        if name == "ضمير متّصل في الآخر":
            pronouns = sorted(shapes, key=len, reverse=True)
    return built, pronouns


BUILT, PRONOUNS = table()


class Corpus:
    """الأسماءُ (بعلاماتها) والهياكلُ، من المصحف كلّه."""

    def __init__(self, text: str) -> None:
        self.nouns: set[tuple] = set()
        self.skeletons: set[str] = set()
        for line in text.split("\n"):
            tokens = line.replace(GOVERNED.MARKUP, " ").split()
            previous = None
            for token in tokens:
                kept = units(token)
                self.skeletons.add(skeleton(kept))
                peeled, extras = PEELER.peel(token)
                if any(extra.get("تنوين") for extra in extras):
                    self.nouns.add(key(kept))
                if previous is not None and (
                    GOVERNED.kind(*PEELER.peel(previous), PEELER.STRUCTURE) == "جر"
                ):
                    self.nouns.add(key(kept))
                after = _after_al(token, kept)
                if after is not None:
                    self.nouns.add(key(after))
                previous = token

    def is_mudari(self, token: str) -> list[Unit] | None:
        """الوحداتُ بعد السابقة إن كان مضارعًا، أو لا شيء."""

        kept = units(token)
        for strip in (0, 1):
            if strip and not (
                len(kept) > strip
                and kept[strip - 1][0][0] in "وفسل"
                and kept[strip - 1][0][1] == FATHA
            ):
                break
            rest = kept[strip:]
            if len(rest) >= 3 and _mudaraa(rest[0]):
                if key(kept) in self.nouns or key(rest) in self.nouns:
                    return None
                if skeleton(rest) in BUILT or skeleton(kept) in BUILT:
                    return None
                return rest
        return None


def _after_al(token: str, kept: list[Unit]) -> list[Unit] | None:
    r = raw(token)
    for cut in (0, 1):
        if r[cut : cut + 2] == "ال" and (cut == 0 or r[0] in "وفبلك"):
            rest = kept[cut + 2 :]
            if rest and rest[0][1].get("شدّة") == "نعم":
                rest = rest[1:]
            return rest or None
    if r.startswith("لل"):
        rest = kept[2:]
        return rest or None
    return None


def _classes(kept: list[Unit], nxt: str | None, skeletons: set[str]) -> str | None:
    if not kept:
        return None
    (letter, state), extra = kept[-1]
    if state == SUKUN:
        return "سكون"
    bare = [u[0] for u, e in kept[-2:] if u[1] == SUKUN and e.get("سكون") == "عارٍ"]
    if len(kept) >= 3 and (
        (bare == ["و", "ا"])
        or (letter == "ا" and state == SUKUN)
        or (letter == "ي" and state == SUKUN and kept[-2][0][1] == KASRA)
    ):
        return "حذف النون"
    if state in SHORT and any(skeleton(kept) + one in skeletons for one in "ياو"):
        return "حذف حرف العلّة"
    if state in SHORT and nxt is not None and raw(nxt).startswith("ا"):
        return "التقاء الساكنين"
    if len(kept) >= 2 and kept[-2][1].get("شدّة") == "نعم" and kept[-2][0][0] == letter:
        return "مضعَّف"
    if len(kept) >= 2 and kept[-2][0][0] == letter and state == SUKUN:
        return "مضعَّف"
    if skeleton(kept)[1:] == "ك":
        return "يك"
    if letter == "ن" and (
        (len(kept) >= 2 and kept[-2][1].get("شدّة") == "نعم" and kept[-2][0][0] == "ن")
        or (state == SUKUN and len(kept) >= 2 and kept[-2][0][1] == FATHA)
    ):
        return "نون التوكيد"
    return None


def explain(kept: list[Unit], nxt: str | None, skeletons: set[str]) -> str | None:
    found = _classes(kept, nxt, skeletons)
    if found is not None:
        return found
    letters = skeleton(kept)
    for one in PRONOUNS:
        if letters.endswith(one) and len(kept) > len(one):
            stem = _classes(kept[: len(kept) - len(one)], None, skeletons)
            if stem is not None:
                return stem
    return None


def _strip_raw(r: str, allowed: str, most: int) -> list[str]:
    out = [r]
    for _ in range(most):
        if r and r[0] in allowed:
            r = r[1:]
            out.append(r)
    return out


def governors(
    flat: list[tuple[str, int]], corpus: Corpus
) -> dict[int, tuple[str, list[Unit]]]:
    """الموضعُ المحكوم ⟵ (الجازم، وحداتُ المحكوم)."""

    found: dict[int, tuple[str, list[Unit]]] = {}
    for place, (token, seg) in enumerate(flat):
        r = raw(token)
        kept = units(token)
        nxt = flat[place + 1] if place + 1 < len(flat) else None
        same_next = nxt is not None and nxt[1] == seg
        states = [u[1] for u, _ in kept]
        if "لم" in _strip_raw(r, "أوف", 2) and states[-2:] == [FATHA, SUKUN]:
            if same_next and nxt is not None:
                found[place + 1] = ("لم", units(nxt[0]))
            continue
        if r == "لما" and any(e.get("شدّة") == "نعم" for _, e in kept):
            if same_next and nxt is not None and corpus.is_mudari(nxt[0]) is not None:
                found[place + 1] = ("لمّا", units(nxt[0]))
            continue
        if (
            len(kept) >= 3
            and kept[0][0][0] in "وف"
            and kept[0][0][1] == FATHA
            and kept[1][0] == ("ل", SUKUN)
            and _mudaraa(kept[2])
        ):
            found[place] = ("لام الأمر", kept[2:])
            continue
        before = flat[place - 1] if place else None
        if (
            len(kept) >= 2
            and kept[0][0] == ("ل", SUKUN)
            and _mudaraa(kept[1])
            and before is not None
            and before[1] == seg
            and raw(before[0]) == "ثم"
        ):
            found[place] = ("لام الأمر", kept[1:])
            continue
        if (
            len(kept) >= 2
            and kept[0][0] == ("ل", KASRA)
            and _mudaraa(kept[1])
            and (place == 0 or flat[place - 1][1] != seg)
        ):
            found[place] = ("لام الأمر", kept[1:])
            continue
        shadda = any(e.get("شدّة") == "نعم" for _, e in kept)
        if "إن" in _strip_raw(r, "وف", 1) and states[-1:] == [SUKUN] and not shadda:
            if same_next and nxt is not None and corpus.is_mudari(nxt[0]) is not None:
                later = [t for t, s in flat[place + 1 :] if s == seg]
                blocked = any(
                    raw(t) in ("إلا", "لما")
                    or (units(t) and units(t)[0][0] == ("ل", FATHA))
                    for t in later
                )
                if not blocked:
                    found[place + 1] = ("إن", units(nxt[0]))
            continue
        if r == "إما" and same_next and nxt is not None:
            if corpus.is_mudari(nxt[0]) is not None:
                found[place + 1] = ("إمّا", units(nxt[0]))
    return found


def _own_sukun(kept: list[Unit]) -> bool:
    if not kept or kept[-1][0][1] != SUKUN:
        return False
    letters = skeleton(kept)
    for one in PRONOUNS:
        if letters.endswith(one) and len(kept) > len(one):
            if kept[len(kept) - len(one) - 1][0][1] in SHORT:
                return False
    return not (kept[-1][0][0] == "ت" and len(kept) >= 2 and kept[-2][0][1] == FATHA)


def census(text: str) -> dict[str, object]:
    corpus = Corpus(text)
    forward: list[tuple[int, int, str, str]] = []
    fired: Counter[str] = Counter()
    reverse: list[tuple[int, int, str]] = []
    pool: list[tuple[int, int, str, str | None]] = []
    governed_total = 0
    for number, line in enumerate(text.split("\n"), start=1):
        flat: list[tuple[str, int]] = []
        for index, part in enumerate(line.split(GOVERNED.MARKUP)):
            flat.extend((token, index) for token in part.split())
        ruled = governors(flat, corpus)
        for place, (tool, kept) in ruled.items():
            governed_total += 1
            token, seg = flat[place]
            nxt = flat[place + 1] if place + 1 < len(flat) else None
            after = nxt[0] if nxt is not None and nxt[1] == seg else None
            reason = explain(kept, after, corpus.skeletons)
            if reason is None:
                forward.append((number, place, tool, token))
            else:
                fired[reason] += 1
        for place, (token, seg) in enumerate(flat):
            if place in ruled:
                continue
            rest = corpus.is_mudari(token)
            if rest is None:
                continue
            nxt = flat[place + 1] if place + 1 < len(flat) else None
            pool.append(
                (number, place, token, nxt[0] if nxt and nxt[1] == seg else None)
            )
            if not _own_sukun(units(token)):
                continue
            if not _has_cause(flat, place, seg, corpus):
                reverse.append((number, place, token))
    draw = random.Random(0).sample(pool, governed_total)
    missed = sum(
        1
        for _, _, token, after in draw
        if explain(units(token), after, corpus.skeletons) is None
    )
    return {
        "forward": forward,
        "fired": fired,
        "reverse": reverse,
        "governed": governed_total,
        "control": Fraction(missed, governed_total),
        "pool": len(pool),
    }


def _has_cause(
    flat: list[tuple[str, int]], place: int, seg: int, corpus: Corpus
) -> bool:
    for token, s in flat[:place]:
        if s != seg:
            continue
        r = raw(token)
        if any(one in CAUSES for one in _strip_raw(r, "وفأ", 2)):
            return True
        if r.startswith("ا"):
            return True
        if corpus.is_mudari(token) is not None and _own_sukun(units(token)):
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()
    found = census(given.text.read_text(encoding="utf-8").rstrip("\n"))
    forward = found["forward"]
    reverse = found["reverse"]
    assert isinstance(forward, list) and isinstance(reverse, list)
    print("المحكوم:", found["governed"], "| الأبواب:", dict(found["fired"]))  # type: ignore[arg-type]
    print("ج١ غيرُ المفسَّر:", len(forward), Counter(one[2] for one in forward))
    print("  أكثرُها:", Counter(one[3] for one in forward).most_common(30))
    print("ج٢ ساكنٌ بلا سبب:", len(reverse))
    print("  أكثرُها:", Counter(one[2] for one in reverse).most_common(30))
    control = found["control"]
    assert isinstance(control, Fraction)
    print(f"ج٣ الضابط: {control} = {float(control):.4f} (من {found['pool']} مضارعًا)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
