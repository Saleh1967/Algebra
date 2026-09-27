"""العاملُ الملتصق والعاملُ المنفصل — تشغيلُ ختم `58e14ba9…`.

الملتصقُ العامل: «بِال» (باءٌ مكسورة، ألف، لام) أو «لِل» (لامٌ مكسورة، لام)،
وبعدها وحدتان فأكثر. والضابط: «وَال» أو «فَال» (واوٌ أو فاءٌ مفتوحة، ألف،
لام). والحركةُ الأخيرة حالُ آخر وحدةٍ بعد طرح البنيويّ وذيل التنوين.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from collections import Counter
from pathlib import Path
from types import ModuleType

RASM = Path(__file__).resolve().parent
MARKUP = "<sel>"
FATHA, DAMMA, KASRA = "َ", "ُ", "ِ"
VOWELS = (FATHA, DAMMA, KASRA)


def _peeler() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "run_cv_peel", RASM / "run_cv_peel.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("لا قارئَ للتقشير")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def prefix(units: list[tuple[str, str]]) -> str | None:
    """«عامل» أو «ضابط» أو لا شيء — بالوحدات الأولى، مع وحدتين بعدها فأكثر."""

    letters = "".join(letter for letter, _ in units)
    first = units[0][1] if units else ""
    if letters.startswith("بال") and first == KASRA and len(units) >= 5:
        return "عامل"
    if letters.startswith("لل") and first == KASRA and len(units) >= 4:
        return "عامل"
    if letters[:3] in ("وال", "فال") and first == FATHA and len(units) >= 5:
        return "ضابط"
    return None


def census(text: str) -> dict[str, Counter[str]]:
    peeler = _peeler()
    found: dict[str, Counter[str]] = {"عامل": Counter(), "ضابط": Counter()}
    for line in text.split("\n"):
        for token in line.replace(MARKUP, " ").split():
            units, extras = peeler.peel(token)
            kept = [
                unit
                for unit, extra in zip(units, extras, strict=True)
                if unit[0] != peeler.STRUCTURE and extra.get("تنوين") != "ذيل"
            ]
            kind = prefix(kept)
            if kind is None:
                continue
            last = kept[-1][1]
            found[kind][last if last in VOWELS else "لا حركة"] += 1
    return found


def share(counts: Counter[str]) -> tuple[int, int]:
    return (counts[KASRA], sum(counts[one] for one in VOWELS))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()
    found = census(given.text.read_text(encoding="utf-8").rstrip("\n"))
    names = {FATHA: "فتحة", DAMMA: "ضمة", KASRA: "كسرة"}
    for kind, counts in found.items():
        parts = " | ".join(f"{names[one]} {counts[one]}" for one in VOWELS)
        print(f"{kind}: {parts} | لا حركة {counts['لا حركة']}")
    kasra, shown = share(found["عامل"])
    other, total = share(found["ضابط"])
    print(f"ف١: {kasra}/{shown} = {kasra / shown:.4f}")
    print(f"ف٢: |{kasra / shown:.4f} − 0.8109| = {abs(kasra / shown - 0.8109):.4f}")
    gap = kasra / shown - other / total
    print(f"ف٣: {kasra / shown:.4f} − {other / total:.4f} = {gap:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
