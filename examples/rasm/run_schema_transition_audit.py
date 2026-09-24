"""تدقيقُ المخطّط بالسلوك: مجموعاتُ التراث تُعرَض على فضاء الانتقال المقيس.

**ما يفعله**: ينفّذ التسجيلَ المختوم
`9ed9eeead8cb2fa512cdde14fa9d4cca2538d4d48a8eb8035968f86604fa2673`:
يبني صفوفَ `P(اللاحق | السابق)` من تعدادٍ **لم يرَ التقسيم**، ثمّ يعرض
عليها مخارجَ الحروف المُودَعة ويقيس تماسكَها بصفريٍّ يبدّل وسومَ المجموعات
على الحروف — فالجدولُ ثابتٌ والهامشان محفوظان بالبناء.

`THE_SINGLETONS_ARE_EXCLUDED_AND_THE_EXCLUSION_IS_DECLARED`: ومخرجٌ فيه
حرفٌ واحدٌ **لا تشابهَ داخلَه يُقاس**، فيخرج من حساب «داخلَ المجموعة»
ويُعَدّ خارجًا لا يُطوى. وذلك شرطُ خ٤ بعينه.

`THE_NUN_JUNCTION_IS_NOT_MEASURED_WITHOUT_A_NAMED_READING`: وأحكامُ النون
معرَّفةٌ عند نونٍ **ساكنة**، والسكونُ صفةُ قراءةٍ لا رسم. فإن لم تُسمَّ
الروايةُ التي يُقرأ منها السكونُ **لم يُقَس الملتقى ألبتّة**، وسقط خ٥،
وصار خ٢ ساقطَ الأساس — لا مقيسًا ضعيفًا.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import math
import random
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
SEAL = "9ed9eeead8cb2fa512cdde14fa9d4cca2538d4d48a8eb8035968f86604fa2673"


def _census_module() -> object:
    path = REPOSITORY / "examples" / "rasm" / "run_letter_transitions.py"
    spec = importlib.util.spec_from_file_location("run_letter_transitions", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AuditError(ValueError):
    """رُدَّ تدقيقٌ لنقصٍ في إعلانٍ أو لمجموعاتٍ لا تُقاس."""


def cosine(first: dict[str, Fraction], second: dict[str, Fraction]) -> float:
    shared = set(first) & set(second)
    if not shared:
        return 0.0
    dot = sum(float(first[key] * second[key]) for key in shared)
    left = math.sqrt(sum(float(value * value) for value in first.values()))
    right = math.sqrt(sum(float(value * value) for value in second.values()))
    return dot / (left * right) if left and right else 0.0


def coherence(
    rows: dict[str, dict[str, Fraction]], grouping: dict[str, int]
) -> tuple[float, float, int, int]:
    """(داخلَ المجموعة، بينها، عددُ الأزواج الداخلة، عددُ الخارجة)."""

    letters = sorted(set(rows) & set(grouping))
    inside: list[float] = []
    outside: list[float] = []
    for index, first in enumerate(letters):
        for second in letters[index + 1 :]:
            value = cosine(rows[first], rows[second])
            if grouping[first] == grouping[second]:
                inside.append(value)
            else:
                outside.append(value)
    if not inside:
        raise AuditError("لا زوجَ داخلَ مجموعةٍ واحدة؛ فلا تماسكَ يُقاس.")
    return (
        sum(inside) / len(inside),
        sum(outside) / len(outside),
        len(inside),
        len(outside),
    )


def headroom(inside: float, outside: float) -> float:
    """نصيبُ ما فوق الصفريّ من المتاح؛ وصفريٌّ يبلغ الواحدَ لا مجالَ فوقه."""

    if outside >= 1:
        raise AuditError("صفريٌّ عند الواحد لا يترك متاحًا يُقسَم عليه.")
    return (inside - outside) / (1 - outside)


def permuted_null(
    rows: dict[str, dict[str, Fraction]],
    grouping: dict[str, int],
    replicates: int,
    seed: int,
) -> tuple[int, float]:
    """(كم صفريًّا بلغ المرصود، أعلى ما بلغه) — بتبديل الوسوم على الحروف.

    والجدولُ لا يُمَسّ ألبتّة، فالهامشان محفوظان بالبناء لا بالدعوى.
    """

    letters = sorted(set(rows) & set(grouping))
    labels = [grouping[one] for one in letters]
    observed = headroom(*coherence(rows, grouping)[:2])
    rng = random.Random(seed)
    reached = 0
    highest = float("-inf")
    for _ in range(replicates):
        shuffled = labels[:]
        rng.shuffle(shuffled)
        drawn = dict(zip(letters, shuffled, strict=True))
        value = headroom(*coherence(rows, drawn)[:2])
        highest = max(highest, value)
        if value >= observed:
            reached += 1
    return reached, highest


def named_readings() -> tuple[str, ...]:
    """الرواياتُ المُسمّاةُ في ختم العمود؛ ولا تُخمَّن من معرفةٍ خارج الشجرة."""

    return ()


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="تدقيقُ المخطّط بفضاء الانتقال")
    parser.add_argument("--text", type=Path, required=True)
    parser.add_argument("--digest", required=True)
    parser.add_argument("--closure", type=int, required=True)
    parser.add_argument("--policy", default="مطويّ")
    parser.add_argument("--replicates", type=int, default=2_000)
    parser.add_argument("--seed", type=int, default=20_260_924)
    return parser


def run(arguments: argparse.Namespace) -> list[str]:
    """شغِّل الشروطَ الخمسةَ واطبع حكمَ كلٍّ منها بختم النسبة."""

    census = _census_module()
    words = census.read_text_words(  # type: ignore[attr-defined]
        arguments.text, arguments.policy, arguments.digest, arguments.closure
    )
    pairs, first, _, places = census.census(words)  # type: ignore[attr-defined]
    rows = census.rows_of_probability(pairs, first)  # type: ignore[attr-defined]

    sys.path.insert(0, str(REPOSITORY / "src"))
    from alghanem.arabic.classical_makharij_table import (
        CLASSICAL_MAKHARIJ,
        CLASSICAL_ORDINAL,
    )

    present = {one: rank for one, rank in CLASSICAL_ORDINAL.items() if one in rows}
    sizes = Counter(present.values())
    usable = {one: rank for one, rank in present.items() if sizes[rank] >= 2}
    smallest = min(Counter(usable.values()).values())
    excluded = sorted(one for one in present if one not in usable)

    inside, outside, within_pairs, between_pairs = coherence(rows, usable)
    share = headroom(inside, outside)
    reached, highest = permuted_null(rows, usable, arguments.replicates, arguments.seed)
    p_value = Fraction(reached + 1, arguments.replicates + 1)
    readings = named_readings()

    seen = hashlib.sha256(arguments.text.read_bytes()).hexdigest()
    return [
        f"الختم: {SEAL[:12]}…",
        f"النسبة: {arguments.text.name} ({seen[:8]}…) · السياسة: {arguments.policy} "
        f"· الإغلاق: {arguments.closure} سطرًا · المواضع: {places}",
        f"المجموعاتُ المُودَعة: {len(CLASSICAL_MAKHARIJ)} مخرجًا · "
        f"الداخلةُ في القياس: {len(set(usable.values()))} · "
        f"الحروفُ الخارجةُ بالإفراد: {len(excluded)} ({''.join(excluded)})",
        f"خ١ نصيبُ المتاح: {share:.4f} "
        f"(داخلًا {inside:.4f} · بينًا {outside:.4f} · "
        f"أزواج {within_pairs}/{between_pairs}) — "
        + ("متحقّق" if share >= 0.05 else "ساقط"),
        "خ٢ استخراجُ تقسيم النون: ساقطُ الأساس — خ٥ لم يتحقّق",
        f"خ٣ الصفريّات: {arguments.replicates} · بلغها {reached} · "
        f"p = {float(p_value):.5f} · أرضيّة {Fraction(1, arguments.replicates + 1)} "
        f"· أعلى صفريّ {highest:.4f}",
        f"خ٤ أصغرُ مجموعةٍ داخلة: {smallest} — " + ("متحقّق" if smallest >= 2 else "ساقط"),
        f"خ٥ الرواياتُ المُسمّاة: {len(readings)} — " + ("متحقّق" if readings else "ساقط"),
        "ولا يُقاس ملتقى النون بلا روايةٍ مُسمّاة، ولا تُخمَّن من خارج الشجرة.",
    ]


def main() -> None:
    for line in run(build_argument_parser().parse_args()):
        print(line)


if __name__ == "__main__":
    main()
