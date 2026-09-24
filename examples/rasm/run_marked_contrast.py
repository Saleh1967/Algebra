"""تشغيلُ `6a584a5a…`: تباينُ الوسم داخلَ مواضع النون، وكفّتا الرسم والضبط.

**قراراتٌ لم يحسمها الختمُ فتُعلَن ههنا** (ولا تُطوى في الشيفرة):

* **التنعيمُ نصفُ وقوعٍ لكلّ خانة** (جِفريز)، إذ اللوغاريتمُ يمتنع عند
  الصفر. وحرفٌ لا يقع بعد نونٍ ألبتّة — موسومةً ولا غيرَ موسومة — **يخرج**
  من القياس ولا يُصطنَع له نصيب.
* **عددُ المجموعات المستخرَجة ثلاثٌ**، مطابقًا لعدد مجموعات المُودَع
  المُقابَل به. وتسميتُه ههنا لأنّ الختمَ لم يُسمِّه، فلا يُختار بعد النظر.
* **كفّةُ الضبط**: رمزُها (حرفٌ + صنفُ علامته)، وصفُّ الحرف توزيعُه على
  الرمز التالي. فالرسمُ المجرَّدُ حروفٌ وحدَها، والضبطُ حروفٌ بعلاماتها.
"""

from __future__ import annotations

import argparse
import math
import random
import sys
import unicodedata
from collections import Counter
from fractions import Fraction
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
SEAL = "6a584a5a1254329445f8a8c5dcc5b52303155fe9c13cafb9dd844a3abf36c1d3"
CORPUS_RECORD = "30c7e393eff12641e27802dbfc38c51e7171ed873bfd2f78dc889de2fad7a359"

BASE = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
FOLD = {
    "أ": "ا",
    "إ": "ا",
    "آ": "ا",
    "ٱ": "ا",
    "ة": "ه",
    "ى": "ي",
    "ؤ": "و",
    "ئ": "ي",
    "ء": "",
}
SUKUN = "ْ"
SHADDA = "ّ"
MARK_RANGE = (0x064B, 0x0655)
OTHER_MARKS = (0x0640, 0x0670, 0x06DF)
SMOOTHING = Fraction(1, 2)
GROUPS = 3


class ContrastError(ValueError):
    """رُدَّ تشغيلٌ لنقصٍ في إعلانٍ أو لمادّةٍ لا تكفي."""


def _is_mark(one: str) -> bool:
    return MARK_RANGE[0] <= ord(one) <= MARK_RANGE[1] or ord(one) in OTHER_MARKS


def _mark_class(marks: str) -> str:
    if SHADDA in marks and SUKUN in marks:
        return "شدّة+سكون"
    for mark, name in (
        (SHADDA, "شدّة"),
        (SUKUN, "سكون"),
        ("ً", "تنوين"),
        ("ٌ", "تنوين"),
        ("ٍ", "تنوين"),
        ("َ", "فتحة"),
        ("ُ", "ضمّة"),
        ("ِ", "كسرة"),
    ):
        if mark in marks:
            return name
    return "مجرَّد"


def read_stream(text: str) -> list[tuple[str, str]]:
    """(الحرفُ المطويّ، صنفُ علامته) عبر النصّ كلِّه."""

    stream = unicodedata.normalize("NFC", text)
    out: list[tuple[str, str]] = []
    index = 0
    while index < len(stream):
        folded = FOLD.get(stream[index], stream[index])
        if folded in BASE:
            step = index + 1
            marks = ""
            while step < len(stream) and _is_mark(stream[step]):
                marks += stream[step]
                step += 1
            out.append((folded, _mark_class(marks)))
            index = step
        else:
            index += 1
    return out


def nun_sites(stream: list[tuple[str, str]]) -> list[tuple[str, bool]]:
    """(الحرفُ التالي، أموسومةٌ بالسكون؟) لكلّ نونٍ يليها حرف."""

    return [
        (stream[index + 1][0], stream[index][1] == "سكون")
        for index in range(len(stream) - 1)
        if stream[index][0] == "ن"
    ]


def contrast(sites: list[tuple[str, bool]]) -> dict[str, float]:
    """لوغاريتمُ نسبة حظِّ الحرف من الموسومة إلى حظِّه من غيرها، منعَّمًا."""

    marked = Counter(one for one, flag in sites if flag)
    plain = Counter(one for one, flag in sites if not flag)
    letters = sorted(set(marked) | set(plain))
    if not letters:
        raise ContrastError("لا موضعَ نونٍ يُعَدّ؛ فلا تباينَ يُقاس.")
    marked_total = sum(marked.values()) + float(SMOOTHING) * len(letters)
    plain_total = sum(plain.values()) + float(SMOOTHING) * len(letters)
    if marked_total <= 0 or plain_total <= 0:
        raise ContrastError("كفّةٌ خاليةٌ من المواضع؛ فالنسبةُ بلا مقام.")
    return {
        letter: math.log2(
            ((marked[letter] + float(SMOOTHING)) / marked_total)
            / ((plain[letter] + float(SMOOTHING)) / plain_total)
        )
        for letter in letters
    }


def split_into(values: dict[str, float], groups: int = GROUPS) -> dict[str, int]:
    """تقسيمٌ على بُعدٍ واحدٍ بمراكزَ حتميّةِ البدء؛ وعددُ المجموعات مُعلَن."""

    letters = sorted(values)
    points = [values[one] for one in letters]
    ordered = sorted(points)
    centres = [
        ordered[min(len(ordered) - 1, (len(ordered) * index) // groups)]
        for index in range(groups)
    ]
    labels = [0] * len(points)
    for _ in range(50):
        labels = [
            min(range(groups), key=lambda k: abs(point - centres[k]))
            for point in points
        ]
        moved = False
        for k in range(groups):
            members = [p for p, g in zip(points, labels, strict=True) if g == k]
            if members:
                centre = sum(members) / len(members)
                if centre != centres[k]:
                    centres[k] = centre
                    moved = True
        if not moved:
            break
    return dict(zip(letters, labels, strict=True))


def assign_to(values: dict[str, float], centres: list[float]) -> dict[str, int]:
    return {
        one: min(range(len(centres)), key=lambda k: abs(values[one] - centres[k]))
        for one in values
    }


def centres_of(values: dict[str, float], labels: dict[str, int]) -> list[float]:
    centres: list[float] = []
    for group in range(GROUPS):
        members = [values[one] for one in values if labels[one] == group]
        centres.append(sum(members) / len(members) if members else 0.0)
    return centres


def adjusted_rand(first: dict[str, int], second: dict[str, int]) -> float:
    keys = sorted(set(first) & set(second))
    if len(keys) < 2:
        raise ContrastError("تقسيمان على أقلَّ من عنصرين لا يُقارَنان.")
    table = Counter((first[one], second[one]) for one in keys)
    rows = Counter(first[one] for one in keys)
    columns = Counter(second[one] for one in keys)

    def choose(value: int) -> float:
        return value * (value - 1) / 2

    index = sum(choose(one) for one in table.values())
    row_sum = sum(choose(one) for one in rows.values())
    column_sum = sum(choose(one) for one in columns.values())
    total = choose(len(keys))
    expected = row_sum * column_sum / total
    highest = (row_sum + column_sum) / 2
    if highest == expected:
        raise ContrastError("تقسيمان لا يترك أحدُهما مجالًا للمؤشّر.")
    return (index - expected) / (highest - expected)


def cosine(first: dict[str, int], second: dict[str, int]) -> float:
    shared = set(first) & set(second)
    if not shared:
        return 0.0
    dot = sum(first[one] * second[one] for one in shared)
    left = math.sqrt(sum(one * one for one in first.values()))
    right = math.sqrt(sum(one * one for one in second.values()))
    return dot / (left * right) if left and right else 0.0


def coherence(rows: dict[str, dict[str, int]], grouping: dict[str, int]) -> float:
    letters = sorted(set(rows) & set(grouping))
    inside: list[float] = []
    outside: list[float] = []
    for index, first in enumerate(letters):
        for second in letters[index + 1 :]:
            value = cosine(rows[first], rows[second])
            (inside if grouping[first] == grouping[second] else outside).append(value)
    if not inside or not outside:
        raise ContrastError("كفّةٌ بلا زوجٍ داخلٍ أو خارج؛ فلا تماسكَ يُقاس.")
    within = sum(inside) / len(inside)
    between = sum(outside) / len(outside)
    return (within - between) / (1 - between)


def rows_over(
    stream: list[tuple[str, str]], *, with_marks: bool
) -> tuple[dict[str, dict[str, int]], int]:
    """صفوفُ الحرف: على الرسم المجرَّد، أو على الرمز (حرفٌ + صنفُ علامته)."""

    rows: dict[str, Counter[str]] = {}
    places = 0
    for index in range(len(stream) - 1):
        current = stream[index][0]
        nxt = (
            f"{stream[index + 1][0]}|{stream[index + 1][1]}"
            if with_marks
            else stream[index + 1][0]
        )
        rows.setdefault(current, Counter())[nxt] += 1
        places += 1
    return {one: dict(counter) for one, counter in rows.items()}, places


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="تشغيلُ تباين الوسم والكفّتين")
    parser.add_argument("--text", type=Path, required=True)
    parser.add_argument("--replicates", type=int, default=2_000)
    parser.add_argument("--seed", type=int, default=20_260_924)
    return parser


def run(arguments: argparse.Namespace) -> list[str]:
    sys.path.insert(0, str(REPOSITORY / "src"))
    from alghanem.arabic.classical_makharij_table import CLASSICAL_ORDINAL
    from alghanem.arabic.phonetic_economy_tool import (
        IDGHAM_NUN_LETTERS,
        IZHAR_NUN_LETTERS,
    )

    text = arguments.text.read_text(encoding="utf-8")
    lines = text.splitlines()
    middle = len(lines) // 2
    whole = read_stream(text)
    first_half = read_stream("\n".join(lines[:middle]))
    second_half = read_stream("\n".join(lines[middle:]))

    deposited = {
        one: (0 if one in IZHAR_NUN_LETTERS else 1 if one in IDGHAM_NUN_LETTERS else 2)
        for one in BASE
    }

    sites_all = nun_sites(whole)
    sites_first, sites_second = nun_sites(first_half), nun_sites(second_half)
    marked_all = sum(1 for _, flag in sites_all if flag)

    learned = split_into(contrast(sites_first))
    centres = centres_of(contrast(sites_first), learned)
    held_out = assign_to(contrast(sites_second), centres)
    second_condition = adjusted_rand(held_out, deposited)

    rng = random.Random(arguments.seed)
    flags = [flag for _, flag in sites_all]
    followers = [one for one, _ in sites_all]
    highest = float("-inf")
    for _ in range(arguments.replicates):
        shuffled = flags[:]
        rng.shuffle(shuffled)
        drawn = list(zip(followers, shuffled, strict=True))
        value = adjusted_rand(split_into(contrast(drawn)), deposited)
        highest = max(highest, value)

    bare_rows, bare_places = rows_over(whole, with_marks=False)
    marked_rows, marked_places = rows_over(whole, with_marks=True)
    present = {one: rank for one, rank in CLASSICAL_ORDINAL.items() if one in bare_rows}
    sizes = Counter(present.values())
    usable = {one: rank for one, rank in present.items() if sizes[rank] >= 2}
    bare_pan = coherence(bare_rows, usable)
    marked_pan = coherence(marked_rows, usable)

    return [
        f"الختم: {SEAL[:12]}… · السجلُّ البايتيّ: {CORPUS_RECORD[:12]}…",
        f"مواضعُ النون: {len(sites_all)} · الموسومة: {marked_all} · "
        f"غيرُ الموسومة: {len(sites_all) - marked_all}",
        f"التنعيم: {SMOOTHING} لكلّ خانة · المجموعاتُ المستخرَجة: {GROUPS}",
        f"ك١ أعلى صفريٍّ (تبديلُ الوسمين، {arguments.replicates}): "
        f"{highest:.4f} — " + ("متحقّق" if highest <= 0.10 else "ساقط"),
        f"ك٢ التكرارُ على النصف المحجوب: {second_condition:.4f} — "
        + ("متحقّق" if second_condition >= 0.35 else "ساقط"),
        f"ك٣ مجموعاتُ المُقابَل به: {len(set(deposited.values()))} — "
        + ("متحقّق" if len(set(deposited.values())) <= GROUPS else "ساقط"),
        f"ك٤ كفّةُ الرسم المجرَّد: {bare_pan:.4f} · "
        f"كفّةُ الضبط: {marked_pan:.4f} — متحقّق (نُشِرتا معًا)",
        f"ك٥ أقلُّ كفّةٍ بالمواضع: {min(bare_places, marked_places)} — "
        + ("متحقّق" if min(bare_places, marked_places) >= 200 else "ساقط"),
        f"ومقامُ النصفين: الأوّل {len(sites_first)} · الثاني {len(sites_second)}",
    ]


def main() -> None:
    for line in run(build_argument_parser().parse_args()):
        print(line)


if __name__ == "__main__":
    main()
