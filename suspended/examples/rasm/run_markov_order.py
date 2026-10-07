"""رتبةُ ماركوف ٠..٦ محجوزةً، وحاجزُ ستيرلنغ فوقها — تشغيلُ ختم `0fdd08b2…`.

**لا أرضيّة**: كلُّ موضعٍ في المقام، وغيرُ المشهود **يُشحَن بلابلاس ولا
يُستبعَد**. والقسمةُ زوجيٌّ وفرديٌّ **بالسطر** وبالتبادل، والحكمُ على
**الثمن المحجوز**.

**وستيرلنغُ حاجزٌ فوق الرتبة لا مقياسٌ فيها**: فضاءُ الرتبة `k^n`،
وتكتيلاتُه `Bell(k^n)`. فإن فاق عددُ التكتيلات عددَ المواضع **لم يبقَ في
المادّة ما يختار** — حدٌّ على المعرفة لا على الحساب.
"""

from __future__ import annotations

import argparse
import importlib.util
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
AUDIT = REPOSITORY / "examples" / "rasm" / "run_encoding_audit.py"
ORDERS = tuple(range(7))
START = "⊢"
MARKUP = "<sel>"
OPERATIONS = 50  # حدُّ الجدوى: ٢^٥٠ عمليّة


def _audit() -> object:
    spec = importlib.util.spec_from_file_location("run_encoding_audit", AUDIT)
    if spec is None or spec.loader is None:
        raise RuntimeError("لا قارئَ للمواصفة")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _stirling() -> object:
    sys.path.insert(0, str(REPOSITORY / "src"))
    from algebra import stirling

    return stirling


def lines_of_states(text: str) -> list[list[str]]:
    """حالاتُ مواضع الرسم سطرًا سطرًا — والسياقُ لا يعبر السطر."""

    audit = _audit()
    found: list[list[str]] = []
    for line in text.replace(MARKUP, " ").splitlines():
        if not line.strip():
            continue
        units = audit.rasm_units(line)  # type: ignore[attr-defined]
        found.append([state for _letter, state in units])
    return found


def table_of(lines: list[list[str]], order: int) -> dict[tuple[str, ...], Counter[str]]:
    """جدولُ (سياقٌ ← توزيعُ الحالة)؛ وأوّلُ السطر يُحشى ببدءٍ فلا يُستبعَد."""

    built: dict[tuple[str, ...], Counter[str]] = defaultdict(Counter)
    for row in lines:
        padded = [START] * order + row
        for index in range(len(row)):
            key = tuple(padded[index : index + order])
            built[key][row[index]] += 1
    return built


def charge(
    built: dict[tuple[str, ...], Counter[str]],
    lines: list[list[str]],
    order: int,
    alphabet: int,
) -> tuple[float, float, int]:
    """(الثمنُ للموضع، نصيبُ ما لم يُرَ سياقُه، عددُ المواضع) — بلابلاس."""

    total = 0.0
    places = 0
    unseen = 0
    for row in lines:
        padded = [START] * order + row
        for index in range(len(row)):
            key = tuple(padded[index : index + order])
            counts = built.get(key)
            places += 1
            if counts is None:
                unseen += 1
                total += math.log2(alphabet)
                continue
            mass = sum(counts.values())
            seen = counts.get(row[index], 0)
            total += -math.log2((seen + 1) / (mass + alphabet))
    if not places:
        return (float("nan"), 0.0, 0)
    return (total / places, unseen / places, places)


def in_sample(built: dict[tuple[str, ...], Counter[str]]) -> tuple[float, float]:
    """(الإنتروبيا الملحَقةُ مصحَّحةً بميلر–مادو، مقدارُ التصحيح)."""

    everything = sum(sum(one.values()) for one in built.values())
    plugin = 0.0
    bias = 0.0
    for counts in built.values():
        mass = sum(counts.values())
        weight = mass / everything
        plugin += weight * -math.fsum(
            (one / mass) * math.log2(one / mass) for one in counts.values()
        )
        bias += weight * (len(counts) - 1) / (2 * mass * math.log(2))
    return (plugin + bias, bias)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    lines = lines_of_states(given.text.read_text(encoding="utf-8"))
    places = sum(len(one) for one in lines)
    states = sorted({one for row in lines for one in row})
    alphabet = len(states)
    print(f"— الأسطر: {len(lines)} | مواضعُ الرسم: {places}")
    print(f"— أبجديّةُ الحالات: {alphabet} | وحالُ البدء زائدةٌ في السياق فقط")
    print(f"  والحالاتُ: {' · '.join(states)}")
    print("— لا أرضيّةَ ولا استبعاد: كلُّ موضعٍ في المقام، وغيرُ المشهود بلابلاس")
    print()

    even = [row for index, row in enumerate(lines) if index % 2 == 0]
    odd = [row for index, row in enumerate(lines) if index % 2 == 1]

    print("الرتبة | سياقاتٌ | ملحَقة | تصحيح | محجوزٌ للموضع | غيرُ مشهودٍ | ربحٌ محجوز")
    rows: list[tuple[int, int, float, float, float, float, float]] = []
    previous: float | None = None
    for order in ORDERS:
        whole = table_of(lines, order)
        inside, bias = in_sample(whole)
        first = charge(table_of(even, order), odd, order, alphabet)
        second = charge(table_of(odd, order), even, order, alphabet)
        held = (first[0] + second[0]) / 2
        unseen = (first[1] + second[1]) / 2
        gain = 0.0 if previous is None else previous - held
        previous = held
        rows.append((order, len(whole), inside, bias, held, unseen, gain))
        print(
            f"   {order}   | {len(whole):7d} | {inside:6.4f} | {bias:6.4f} "
            f"| {held:13.4f} | {unseen:10.4f} | {gain:+.4f}"
        )
    print()

    print("— الحكمُ على الرتبة")
    inside_rose = sum(1 for one, two in zip(rows, rows[1:]) if two[2] > one[2] + 1e-12)
    print(f"  رتباتٌ ارتفعت فيها الملحَقةُ: {inside_rose}")
    turned = [one[0] for one in rows[1:] if one[6] < 0]
    if turned:
        print(f"  أوّلُ رتبةٍ ارتفع فيها المحجوز: {turned[0]}")
    else:
        print("  لم يرتفع المحجوزُ في أيّ رتبةٍ إلى السادسة")
    best = min(one[4] for one in rows)
    where = next(one[0] for one in rows if one[4] == best)
    print(f"  أدنى محجوزٍ: {best:.4f} عند الرتبة {where}")
    print(f"  ربحُ الرتبة الأولى محجوزًا: {rows[1][6]:+.4f}")
    print(f"  ربحُ الرتبة الثالثة محجوزًا: {rows[3][6]:+.4f}")
    print(f"  غيرُ المشهود عند السادسة: {rows[6][5]:.4f}")
    print(f"  ومجموعُ الربح المحجوز إلى أدناه: {rows[0][4] - best:+.4f}")
    print()

    # **والنمطُ يُطبَع عددًا لا يُوصَف**: الفجوةُ بين الملحَق والمحجوز هي
    # **الانتحالُ بعينه**، ونسبُ الأرباح المتتاليةِ تقول كيف يضمر الربح.
    print("— النمطُ: فجوةُ الانتحال، ونسبُ الضمور")
    print("الرتبة | فجوةٌ (محجوز − ملحَقة) | نسبةُ الفجوة إلى سابقتها | نسبةُ الربح")
    for index, one in enumerate(rows):
        gap = one[4] - one[2]
        before = rows[index - 1][4] - rows[index - 1][2] if index else 0.0
        widen = gap / before if index and before > 1e-9 else float("nan")
        ratio = (
            one[6] / rows[index - 1][6]
            if index > 1 and abs(rows[index - 1][6]) > 1e-9
            else float("nan")
        )
        print(f"   {one[0]}   | {gap:20.4f} | {widen:23.2f} | {ratio:11.3f}")
    print()

    print("— حاجزُ ستيرلنغ فوق الرتبة: فضاءٌ وتكتيلات")
    stirling = _stirling()
    print(
        "الرتبة | فضاءُ السياق k^n | ⌊log₂ Bell(k^n)⌋ "
        "| تكتيلاتٌ > مواضع | O(k·3^m) دون 2^50"
    )
    first_over: int | None = None
    largest_feasible: int | None = None
    for order in ORDERS:
        space = alphabet**order
        if space <= 64:
            bell = sum(
                stirling.subsets(space, k)  # type: ignore[attr-defined]
                for k in range(1, space + 1)
            )
            bits = bell.bit_length() - 1
            over = bell > places
            shown = str(bits)
        else:
            # Bell(k^n) فوق هذا الحجم لا يُعَدّ ههنا — ويُقال حدُّه لا يُخمَّن
            bell = None
            bits = None
            over = True
            shown = "فوق العدّ"
        feasible = space * math.log2(3) < OPERATIONS
        if over and first_over is None:
            first_over = order
        if feasible:
            largest_feasible = order
        print(
            f"   {order}   | {space:16d} | {shown:>16} "
            f"| {'نعم' if over else 'لا':>16} | {'نعم' if feasible else 'لا':>16}"
        )
    print()
    print(f"  أصغرُ رتبةٍ تفوق تكتيلاتُها المواضعَ: {first_over}")
    print(f"  أكبرُ رتبةٍ فضاءُ تكتيلها دون 2^{OPERATIONS}: {largest_feasible}")
    print()

    print("— ما لا يُدَّعى")
    print("  الأرضيّةُ مرفوعةٌ ههنا، فلا يُقابَل رقمُ هذا السجلّ برقم سلّم")
    print("  الضبط المُؤرَّض: ذاك ملحَقٌ على نصيبٍ من المواضع، وهذا محجوزٌ على الكلّ.")
    print("  وحاجزُ ستيرلنغ حدٌّ على ما تُرجِّحه المادّةُ لا على ما تحسبه الآلة:")
    print("  فعددُ التكتيلات إذا فاق المواضعَ لم يبقَ في المادّة ما يختار.")
    print("  والقناةُ حالُ موضع الرسم — لا اللفظ ولا الجملة؛ ورتبةُ الانقلاب")
    print("  رتبةُ هذه القناة في هذا المجمَّد بهذه القسمة، لا حدًّا للعربيّة.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
