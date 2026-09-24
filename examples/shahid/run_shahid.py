"""«الشاهد» مُشغَّلًا: فرقُ إحلالٍ من الرسم وحدَه، بخمسة شروطٍ مختومةٍ قبله.

**ما يفعله هذا المُشغِّل**: يقرأ محاذاةً عمودُها `loc` و`surface`، ويبني
**شاهدَ الإحلال** — عقدتان جارتان إن وقعتا في إطارٍ محليٍّ واحدٍ بعينه
(السابقُ واللاحقُ أنفسُهما لفظًا) — ثمّ يقيس الشروطَ الخمسةَ المُسجَّلةَ في
`df8fe34a88bbf641e554f2ca923ac17f8c4c355691a109261bbe3a9b8c06ba07`.

`THE_BYTES_ARE_CHECKED_AGAINST_A_DECLARED_DIGEST_NOT_TRUSTED`: ويُرَدّ
التشغيلُ إن خالفت بصمةُ الملفّ ما أُعلِن في `--digest`، أو خالف عددُ صفوفه
`--closure`. فالسطحُ المشتقُّ في مكانٍ آخرَ **مدوّنةٌ أخرى**، ولا يُعرَف ذلك
إلّا ببصمةٍ تُقارَن. والانضمامُ على مفتاحٍ من مدوّنتين انضمامُ هواء.

`THE_SURFACE_KIND_IS_A_DECISION_NOT_A_DEFAULT`: و«أرسمٌ خامٌ أم مخرَجُ
تطبيعٍ؟» قرارٌ يبدّل كلَّ رقمٍ بعده، فلا افتراضيَّ له: يُعلَن بـ
`--surface-kind` أو يُرَدّ التشغيل.

`THE_CLASS_ASSIGNMENT_IS_AN_INPUT_NOT_A_GUESS`: وأصنافُ السابق واللاحق
الخمسةُ مُسمّاةٌ في الختم، وأمّا **إسنادُ لفظٍ إلى صنفه** فمُدخَلٌ يُعلَن
بـ`--classes`. ولا يُخمَّن ههنا: تخمينُه يجعل الرقمَ خبرًا عن مخمِّنه.
وشرطُ ش٣ هو فحصُ هذا المُدخَل نفسِه: إن ابتلع «سواه» أكثرَ من النصف فالتوقيعُ
بتّةٌ واحدةٌ اسمُها «ليس من الأربعة».

`NO_Z_IS_PRINTED_UNDIVIDED`: ولا يُطبَع `z` إلّا مقسومًا على جذر «الحوافِّ
للعقدة»، ويُطبَع الخامُ بجانبه ليُرى مقدارُ ما طُرِح. فالحافّةُ ليست مشاهدةً
مستقلّة، والعقدةُ الواحدةُ تدخل حوافَّ كثيرة.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
import random
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

SEAL = "df8fe34a88bbf641e554f2ca923ac17f8c4c355691a109261bbe3a9b8c06ba07"

CLASSES: tuple[str, ...] = ("جار", "فعل", "معرفة", "ضمير", "سواه")
CATCH_ALL = "سواه"

SURFACE_KINDS: tuple[str, ...] = ("رسم-خام", "مخرج-phon")

EDGE = "\u0000"
"""حدُّ الآية: إطارٌ لا يعبرها، فلا يُصنَع جوارٌ من طرفين متباعدين."""


class ShahidError(ValueError):
    """رُدَّ تشغيلٌ لنقصٍ في إعلانٍ أو لمخالفة إغلاق."""


def read_alignment(path: Path, closure: int, digest: str) -> list[tuple[str, str]]:
    """اقرأ (loc، surface) بعد فحص البصمة والإغلاق؛ ويُرَدّ أيُّهما خالف."""

    seen = hashlib.sha256(path.read_bytes()).hexdigest()
    if seen != digest:
        raise ShahidError(
            f"بصمةُ الملفّ {seen[:12]}… والمُعلَنةُ {digest[:12]}… — "
            "مدوّنتان لا مدوّنة، ولا يُبنى على المخالفة."
        )
    with path.open(encoding="utf-8", newline="") as handle:
        rows = [
            (row["loc"].strip(), row["surface"].strip())
            for row in csv.DictReader(handle, delimiter="\t")
        ]
    if len(rows) != closure:
        raise ShahidError(
            f"{len(rows)} صفًّا في الملفّ و{closure} في الإغلاق المُعلَن؛ "
            "والفرقُ يُعلَن ولا يُطوى."
        )
    if any(not loc or not surface for loc, surface in rows):
        raise ShahidError("صفٌّ بلا موضعٍ أو بلا سطحٍ لا يدخل العدّ.")
    return rows


def read_classes(path: Path) -> dict[str, str]:
    """اقرأ إسنادَ الألفاظ إلى الأصناف؛ وصنفٌ خارج الخمسة يُرَدّ."""

    with path.open(encoding="utf-8", newline="") as handle:
        table = {
            row["surface"].strip(): row["class"].strip()
            for row in csv.DictReader(handle, delimiter="\t")
        }
    unknown = {one for one in table.values() if one not in CLASSES}
    if unknown:
        raise ShahidError(f"أصنافٌ خارج الخمسة المختومة: {'، '.join(sorted(unknown))}.")
    return table


def _verse_of(loc: str) -> str:
    return ":".join(loc.split(":")[:2])


def frames(rows: list[tuple[str, str]]) -> list[tuple[str, str, str]]:
    """(السابقُ، المركزُ، اللاحقُ) داخلَ الآية الواحدة؛ ولا إطارَ يعبر آيتين."""

    built: list[tuple[str, str, str]] = []
    for index, (loc, surface) in enumerate(rows):
        verse = _verse_of(loc)
        before = (
            rows[index - 1][1]
            if index and _verse_of(rows[index - 1][0]) == verse
            else EDGE
        )
        after = (
            rows[index + 1][1]
            if index + 1 < len(rows) and _verse_of(rows[index + 1][0]) == verse
            else EDGE
        )
        built.append((before, surface, after))
    return built


def neighbours(built: list[tuple[str, str, str]]) -> set[frozenset[str]]:
    """شاهدُ الإحلال: مركزان في إطارٍ محليٍّ واحدٍ بعينه."""

    centres: dict[tuple[str, str], set[str]] = defaultdict(set)
    for before, centre, after in built:
        if before == EDGE or after == EDGE:
            continue
        centres[(before, after)].add(centre)
    edges: set[frozenset[str]] = set()
    for group in centres.values():
        ordered = sorted(group)
        for first in range(len(ordered)):
            for second in range(first + 1, len(ordered)):
                edges.add(frozenset((ordered[first], ordered[second])))
    return edges


def signatures(
    built: list[tuple[str, str, str]], classes: dict[str, str]
) -> dict[str, Counter[tuple[str, str]]]:
    """توقيعُ كلّ لفظٍ على **الجدول المشترَك**: ٢٥ خانةً لا عشرةُ هوامش."""

    table: dict[str, Counter[tuple[str, str]]] = defaultdict(Counter)
    for before, centre, after in built:
        cell = (
            classes.get(before, CATCH_ALL),
            classes.get(after, CATCH_ALL),
        )
        table[centre][cell] += 1
    return table


def _cosine(first: Counter[tuple[str, str]], second: Counter[tuple[str, str]]) -> float:
    shared = set(first) & set(second)
    if not shared:
        return 0.0
    dot = sum(first[cell] * second[cell] for cell in shared)
    left = math.sqrt(sum(value * value for value in first.values()))
    right = math.sqrt(sum(value * value for value in second.values()))
    return dot / (left * right) if left and right else 0.0


def transfer(
    edges: set[frozenset[str]],
    held_out: dict[str, Counter[tuple[str, str]]],
    seed: int,
    draws: int,
) -> tuple[float, float, int]:
    """(تشابهُ الجيران، تشابهُ أزواجٍ عشوائيّة، عددُ الأزواج المقيسة)."""

    pairs = [
        tuple(sorted(edge)) for edge in edges if all(one in held_out for one in edge)
    ]
    if not pairs:
        raise ShahidError("لا زوجَ جيرةٍ نجا إلى النصف المحجوب؛ فلا انتقالَ يُقاس.")
    observed = sum(_cosine(held_out[one], held_out[two]) for one, two in pairs)
    observed /= len(pairs)

    names = sorted(held_out)
    rng = random.Random(seed)
    null = 0.0
    for _ in range(draws):
        one, two = rng.sample(names, 2)
        null += _cosine(held_out[one], held_out[two])
    return observed, null / draws, len(pairs)


def catch_all_share(
    built: list[tuple[str, str, str]], classes: dict[str, str]
) -> Fraction:
    """نصيبُ «سواه» من مواضع السابق واللاحق مجتمعةً."""

    total = 0
    caught = 0
    for before, _, after in built:
        for side in (before, after):
            if side == EDGE:
                continue
            total += 1
            if classes.get(side, CATCH_ALL) == CATCH_ALL:
                caught += 1
    if not total:
        raise ShahidError("لا موضعَ سياقٍ يُعَدّ؛ فالنصيبُ بلا مقام.")
    return Fraction(caught, total)


def _predict(
    built: list[tuple[str, str, str]],
    learned: dict[str, Counter[tuple[str, str]]],
    classes: dict[str, str],
    *,
    joint: bool,
) -> Fraction:
    """نصيبُ الإصابة في التنبّؤ بصنف اللاحق: بالجدول المشترَك أو بالهامش."""

    hits = 0
    tried = 0
    for before, centre, after in built:
        if after == EDGE or centre not in learned:
            continue
        cells = learned[centre]
        if joint:
            before_class = classes.get(before, CATCH_ALL)
            cells = Counter(
                {
                    cell: count
                    for cell, count in cells.items()
                    if cell[0] == before_class
                }
            )
            if not cells:
                cells = learned[centre]
        tally: Counter[str] = Counter()
        for (_, next_class), count in cells.items():
            tally[next_class] += count
        if not tally:
            continue
        tried += 1
        if tally.most_common(1)[0][0] == classes.get(after, CATCH_ALL):
            hits += 1
    if not tried:
        raise ShahidError("لا موضعَ يُتنبَّأ به في النصف المحجوب.")
    return Fraction(hits, tried)


def _smallest_group(edges: set[frozenset[str]]) -> int:
    """أصغرُ فرقةٍ (مركّبةٍ متّصلة) تدخل القراءة."""

    parent: dict[str, str] = {}

    def find(node: str) -> str:
        parent.setdefault(node, node)
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    for edge in edges:
        one, two = sorted(edge)
        parent[find(one)] = find(two)
    groups: Counter[str] = Counter(find(node) for node in list(parent))
    return min(groups.values()) if groups else 0


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="تشغيلُ «الشاهد» على محاذاةٍ مختومة")
    parser.add_argument("--aligned", type=Path, required=True)
    parser.add_argument("--closure", type=int, required=True)
    parser.add_argument("--digest", required=True)
    parser.add_argument("--classes", type=Path, required=True)
    parser.add_argument("--surface-kind", choices=SURFACE_KINDS, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--draws", type=int, default=2_000)
    return parser


def run(arguments: argparse.Namespace) -> list[str]:
    """شغِّل الشروطَ الخمسةَ واطبع كلَّ رقمٍ بختمه."""

    if len(arguments.digest) != 64 or set(arguments.digest) - set("0123456789abcdef"):
        raise ShahidError("البصمةُ أربعٌ وستّون خانةً ستّةَ عشريّة.")
    rows = read_alignment(arguments.aligned, arguments.closure, arguments.digest)
    classes = read_classes(arguments.classes)

    middle = len(rows) // 2
    first, second = rows[:middle], rows[middle:]
    built_first, built_second = frames(first), frames(second)
    edges = neighbours(built_first)
    held_out = signatures(built_second, classes)
    learned = signatures(built_first, classes)

    nodes = len({centre for _, centre, _ in built_first})
    per_node = Fraction(len(edges), nodes) if nodes else Fraction(0)
    observed, null, measured = transfer(
        edges, held_out, arguments.seed, arguments.draws
    )
    headroom = (observed - null) / (1 - null) if null < 1 else 0.0
    share = catch_all_share(built_first, classes)
    joint = _predict(built_second, learned, classes, joint=True)
    marginal = _predict(built_second, learned, classes, joint=False)

    stamp = (
        f"المدوّنة: {arguments.aligned.name} ({arguments.digest[:8]}…) · "
        f"السطح: {arguments.surface_kind} · الإغلاق: {arguments.closure}"
    )
    lines = [
        f"الختم: {SEAL[:12]}…",
        f"النسبة: {stamp}",
        f"العقد: {nodes} · الحوافّ: {len(edges)} · للعقدة: {float(per_node):.4f}",
        f"ش١ نصيبُ المتاح: {headroom:.4f} "
        f"(مرصود {observed:.4f} · صفريّ {null:.4f} · أزواج {measured})",
        f"ش٢ الحوافُّ للعقدة مُعلَنة: {float(per_node):.4f}",
        f"ش٣ نصيبُ «{CATCH_ALL}»: {float(share):.4f}",
        f"ش٤ أصغرُ فرقة: {_smallest_group(edges)}",
        f"ش٥ المشترَك − الهامش: {float(joint - marginal):.4f} "
        f"(مشترَك {float(joint):.4f} · هامش {float(marginal):.4f})",
    ]
    if per_node > 0:
        lines.append(
            "ولا يُطبَع z إلّا مقسومًا على "
            f"{math.sqrt(float(per_node)):.4f} — جذرِ الحوافِّ للعقدة."
        )
    return lines


def main() -> None:
    arguments = build_argument_parser().parse_args()
    for line in run(arguments):
        print(line)


if __name__ == "__main__":
    main()
