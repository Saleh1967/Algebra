"""الجرُّ بلا هامش على المستويات الثلاثة — تشغيلُ ختم `a57f54c1…`.

كلُّ لفظٍ يحكمه جارٌّ (داخلَ اللفظ، أو بين لفظين، أو على بُعد لفظ) يُسأل: آخرُه
كسرة؟ أو بابٌ من الجدول الموقَّع `deposits/jarr_exceptions_draft.tsv`؟ وما سوى
ذلك يُسجَّل موضعًا بعينه (السطر، ورقمُ اللفظ، والمستوى، واللفظ).
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from collections import Counter
from pathlib import Path
from types import ModuleType

RASM = Path(__file__).resolve().parent
TABLE = RASM.parents[1] / "deposits" / "jarr_exceptions_draft.tsv"
FATHA, DAMMA, KASRA = "َ", "ُ", "ِ"
VOWELS = (FATHA, DAMMA, KASRA)
BUILT = ("مبنيّ: إشارة", "مبنيّ: موصول", "مبنيّ: ضمير منفصل", "مبنيّ: استفهام وشرط وغيرُهما")
CLASSES = (
    "كسرة",
    "مبنيّ",
    "ضمير متّصل",
    "إعرابٌ بالحرف",
    "إعرابٌ مقدَّر",
    "ممنوعٌ من الصرف: وزن",
    "ممنوعٌ من الصرف: علَم",
    "استئنافٌ بعلامة وقف",
)


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


def units(token: str) -> list[tuple[tuple[str, str], dict[str, str]]]:
    peeled, extras = PEELER.peel(token)
    return [
        (unit, extra)
        for unit, extra in zip(peeled, extras, strict=True)
        if unit[0] != PEELER.STRUCTURE and extra.get("تنوين") != "ذيل"
    ]


def skeleton(token: str) -> str:
    return "".join(u[0] for u, extra in units(token) if extra.get("شدّة") != "نعم")


def final(token: str) -> str | None:
    kept = units(token)
    if not kept:
        return None
    state = kept[-1][0][1]
    return state if state in VOWELS else None


def table() -> dict[str, set[str]]:
    """أبوابُ الجدول الموقَّع بصورها المطبَّعة."""

    text = TABLE.read_text(encoding="utf-8")
    if "# التوقيع: موقَّع" not in text:
        raise RuntimeError("الجدولُ غيرُ موقَّع")
    found: dict[str, set[str]] = {}
    for line in text.split("\n"):
        if not line or line.startswith("#"):
            continue
        name, forms, _ = line.split("\t")
        found[name] = {
            skeleton(one.strip().split(" ")[-1])
            for one in forms.split(",")
            if one.strip()
        }
    return found


TABLE_FORMS = table()
BUILT_FORMS = set().union(*(TABLE_FORMS[one] for one in BUILT))
PRONOUNS = sorted(TABLE_FORMS["ضمير متّصل في الآخر"], key=len, reverse=True)
NAMES = TABLE_FORMS["ممنوعٌ من الصرف: علَم"]


def _pronoun(governed: str) -> bool:
    if governed.startswith("ال"):
        return False
    return any(governed.endswith(one) and len(governed) > len(one) for one in PRONOUNS)


def _diptote_shape(governed: str) -> bool:
    n = len(governed)
    return (
        (n == 5 and governed[2] == "ا")
        or (n == 6 and governed[2] == "ا" and governed[4] == "ي")
        or (n == 4 and governed[0] == "ا")
        or (n >= 4 and (governed.endswith("اا") or governed.endswith("ان")))
    )


def explain(governed: str, vowel: str | None) -> str | None:
    """البابُ الذي يفسّر، بالترتيب المختوم — أو لا شيء."""

    if vowel == KASRA:
        return "كسرة"
    if governed in BUILT_FORMS:
        return "مبنيّ"
    if _pronoun(governed):
        return "ضمير متّصل"
    if governed.endswith("ين") and vowel in (FATHA, KASRA):
        return "إعرابٌ بالحرف"
    if vowel is None and governed[-1:] in ("ا", "ي"):
        return "إعرابٌ مقدَّر"
    plain = not governed.startswith("ال") and not _pronoun(governed)
    if vowel == FATHA and plain and _diptote_shape(governed):
        return "ممنوعٌ من الصرف: وزن"
    if vowel == FATHA and governed in NAMES:
        return "ممنوعٌ من الصرف: علَم"
    return None


def _inside(token: str) -> str | None:
    """محكومُ المستوى الأوّل، أو لا شيء."""

    kept = [u for u, _ in units(token)]
    letters = "".join(u[0] for u in kept)
    whole = skeleton(token)
    if len(kept) >= 5 and letters.startswith("بال") and kept[0][1] == KASRA:
        return whole[1:]
    if len(kept) >= 4 and letters.startswith("لل") and kept[0][1] == KASRA:
        return "ا" + whole[1:]
    return None


def _starts_with_al(token: str) -> str | None:
    kept = [u for u, _ in units(token)]
    whole = skeleton(token)
    if whole.startswith("ال"):
        return whole
    if whole.startswith("وال") and kept and kept[0][1] == FATHA:
        return whole[1:]
    return None


def census(text: str) -> tuple[Counter[str], list[tuple[int, int, str, str, str]], int]:
    """(عدُّ الأبواب، المواضعُ غيرُ المفسَّرة، والمستثنى بالوقف)."""

    fired: Counter[str] = Counter()
    unexplained: list[tuple[int, int, str, str, str]] = []
    paused = 0
    for number, line in enumerate(text.split("\n"), start=1):
        segments = [part.split() for part in line.split("<sel>")]
        flat: list[tuple[str, int]] = []
        for index, segment in enumerate(segments):
            flat.extend((token, index) for token in segment)
        for place, (token, seg) in enumerate(flat):
            governed = _inside(token)
            if governed is not None:
                _judge(
                    governed,
                    final(token),
                    fired,
                    unexplained,
                    (number, place, "١", token),
                )
            if place == 0:
                continue
            before, before_seg = flat[place - 1]
            if GOVERNED.kind(*PEELER.peel(before), PEELER.STRUCTURE) == "جر":
                if before_seg != seg:
                    paused += 1
                else:
                    _judge(
                        skeleton(token),
                        final(token),
                        fired,
                        unexplained,
                        (number, place, "٢", token),
                    )
            if place >= 2:
                third = _starts_with_al(token)
                head, head_seg = flat[place - 2]
                if (
                    third is not None
                    and final(before) == KASRA
                    and GOVERNED.kind(*PEELER.peel(head), PEELER.STRUCTURE) == "جر"
                ):
                    if not head_seg == before_seg == seg:
                        paused += 1
                    else:
                        _judge(
                            third,
                            final(token),
                            fired,
                            unexplained,
                            (number, place, "٣", token),
                        )
    if paused:
        fired["استئنافٌ بعلامة وقف"] += paused
    return (fired, unexplained, paused)


def _judge(
    governed: str,
    vowel: str | None,
    fired: Counter[str],
    unexplained: list[tuple[int, int, str, str, str]],
    where: tuple[int, int, str, str],
) -> None:
    reason = explain(governed, vowel)
    if reason is None:
        names = {FATHA: "فتحة", DAMMA: "ضمة", None: "لا حركة"}
        unexplained.append((*where, names[vowel]))
    else:
        fired[reason] += 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()
    fired, unexplained, paused = census(
        given.text.read_text(encoding="utf-8").rstrip("\n")
    )
    print("الأبواب:", {one: fired[one] for one in CLASSES})
    dead = [one for one in CLASSES if fired[one] == 0]
    print(f"ص١: غيرُ المفسَّر {len(unexplained)} | ص٢: أبوابٌ لم تعمل {len(dead)} {dead}")
    print("بالمستوى:", Counter(one[2] for one in unexplained))
    print("بالحركة:", Counter(one[4] for one in unexplained))
    print("أكثرُ الألفاظ:", Counter(one[3] for one in unexplained).most_common(25))
    return 0


if __name__ == "__main__":
    sys.exit(main())
