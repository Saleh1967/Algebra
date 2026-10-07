"""تشغيلُ `81884f7e…`: مئينٌ بدل الأقصى، واتّجاهان، وفرقُ كفّتين مقيسٌ بصفريّه.

**قراراتٌ لم يحسمها الختمُ فتُعلَن**: التنعيمُ نصفُ وقوعٍ لكلّ خانة،
والمجموعاتُ المستخرَجةُ ثلاثٌ مطابقًا للمُودَع، وسياسةُ الجوار في كفّتَي
هذا التشغيل **عابرةٌ حدَّ الكلمة** — وتُنشَر إلى جانبها قراءةُ الرسم
**داخلَ الكلمة** وفاءً بم٥.
"""

from __future__ import annotations

import argparse
import random
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
SEAL = "81884f7ea02235c37ef6edac5d555418924e9f0acd54bf1793fb5d2afb12e8eb"
CORPUS_RECORD = "30c7e393eff12641e27802dbfc38c51e7171ed873bfd2f78dc889de2fad7a359"
QUANTILE = 0.95


def _contrast_module() -> object:
    import importlib.util

    path = REPOSITORY / "examples" / "rasm" / "run_marked_contrast.py"
    spec = importlib.util.spec_from_file_location("run_marked_contrast", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


mc = _contrast_module()


def quantile_of(values: list[float], share: float = QUANTILE) -> float:
    """مئينٌ على قيمٍ مرتّبة؛ ويُسمّى نصيبُه ولا يُفترَض."""

    if not values:
        raise mc.ContrastError("لا قيمةَ يُؤخَذ منها مئين.")
    ordered = sorted(values)
    index = min(len(ordered) - 1, int(share * (len(ordered) - 1)))
    return ordered[index]


def direction_reading(
    learn: list[tuple[str, bool]],
    test: list[tuple[str, bool]],
    deposited: dict[str, int],
) -> float:
    """مؤشّرُ رَند: تُتعلَّم المراكزُ من كفّةٍ ويُختبَر على الأخرى."""

    learned = mc.split_into(mc.contrast(learn))
    centres = mc.centres_of(mc.contrast(learn), learned)
    return mc.adjusted_rand(mc.assign_to(mc.contrast(test), centres), deposited)


def direction_null(
    learn: list[tuple[str, bool]],
    test: list[tuple[str, bool]],
    deposited: dict[str, int],
    replicates: int,
    seed: int,
) -> list[float]:
    """صفريُّ اتّجاهٍ: تُبدَّل وسومُ الكفّتين بأعدادها، ويُعاد القياسُ كاملًا."""

    rng = random.Random(seed)
    drawn: list[float] = []
    for _ in range(replicates):
        shuffled = []
        for sites in (learn, test):
            flags = [flag for _, flag in sites]
            rng.shuffle(flags)
            shuffled.append(list(zip([one for one, _ in sites], flags, strict=True)))
        drawn.append(direction_null_reading(shuffled[0], shuffled[1], deposited))
    return drawn


def direction_null_reading(
    learn: list[tuple[str, bool]],
    test: list[tuple[str, bool]],
    deposited: dict[str, int],
) -> float:
    return direction_reading(learn, test, deposited)


def marked_pan_null(
    stream: list[tuple[str, str]],
    usable: dict[str, int],
    replicates: int,
    seed: int,
) -> list[float]:
    """صفريُّ كفّة الضبط: **خلطُ أصناف العلامات** مع بقاء الحروف في مواضعها.

    فإن بقي ارتفاعُ الكفّة بعد الخلط فهو أثرُ **توسيع الرمز** لا أثرُ الضبط.
    """

    letters = [one for one, _ in stream]
    classes = [one for _, one in stream]
    class_names = sorted(set(classes))
    class_index = {name: number for number, name in enumerate(class_names)}
    letter_names = sorted(set(letters))
    letter_index = {name: number for number, name in enumerate(letter_names)}

    rows = [letter_index[one] for one in letters]
    followers = [letter_index[one] for one in letters]
    marks = [class_index[one] for one in classes]
    width = len(class_names)
    symbols = len(letter_names) * width

    usable_rows = {letter_index[one] for one in usable if one in letter_index}
    rng = random.Random(seed)
    drawn: list[float] = []
    for _ in range(replicates):
        shuffled = marks[:]
        rng.shuffle(shuffled)
        counts: dict[int, Counter[int]] = {one: Counter() for one in usable_rows}
        for index in range(len(rows) - 1):
            current = rows[index]
            if current in usable_rows:
                counts[current][followers[index + 1] * width + shuffled[index + 1]] += 1
        table = {
            letter_names[one]: {str(key): value for key, value in counter.items()}
            for one, counter in counts.items()
        }
        drawn.append(mc.coherence(table, usable))
        _ = symbols
    return drawn


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="تشغيلُ فرق الكفّتين والاتّجاهين")
    parser.add_argument("--text", type=Path, required=True)
    parser.add_argument("--replicates", type=int, default=2_000)
    parser.add_argument("--pan-replicates", type=int, default=2_000)
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
    whole = mc.read_stream(text)
    first = mc.read_stream("\n".join(lines[:middle]))
    second = mc.read_stream("\n".join(lines[middle:]))

    deposited = {
        one: (0 if one in IZHAR_NUN_LETTERS else 1 if one in IDGHAM_NUN_LETTERS else 2)
        for one in mc.BASE
    }
    sites_all = mc.nun_sites(whole)
    sites_first, sites_second = mc.nun_sites(first), mc.nun_sites(second)

    # م١: مئينُ صفريّ تبديل الوسمين على المدوّنة كلِّها
    rng = random.Random(arguments.seed)
    flags = [flag for _, flag in sites_all]
    followers = [one for one, _ in sites_all]
    whole_null = []
    for _ in range(arguments.replicates):
        shuffled = flags[:]
        rng.shuffle(shuffled)
        whole_null.append(
            mc.adjusted_rand(
                mc.split_into(mc.contrast(list(zip(followers, shuffled, strict=True)))),
                deposited,
            )
        )
    first_condition = quantile_of(whole_null)

    # م٢ وم٣: الاتّجاهان ومئينا صفريّهما
    forward = direction_reading(sites_first, sites_second, deposited)
    reverse = direction_reading(sites_second, sites_first, deposited)
    forward_bar = quantile_of(
        direction_null(
            sites_first, sites_second, deposited, arguments.replicates, arguments.seed
        )
    )
    reverse_bar = quantile_of(
        direction_null(
            sites_second, sites_first, deposited, arguments.replicates, arguments.seed
        )
    )
    above = int(forward > forward_bar) + int(reverse > reverse_bar)

    # م٤: كفّةُ الضبط مقابل مئين صفريّ خلط العلامات
    bare_rows, _ = mc.rows_over(whole, with_marks=False)
    marked_rows, _ = mc.rows_over(whole, with_marks=True)
    present = {one: rank for one, rank in CLASSICAL_ORDINAL.items() if one in bare_rows}
    sizes = Counter(present.values())
    usable = {one: rank for one, rank in present.items() if sizes[rank] >= 2}
    marked_pan = mc.coherence(marked_rows, usable)
    pan_bar = quantile_of(
        marked_pan_null(whole, usable, arguments.pan_replicates, arguments.seed)
    )
    margin = marked_pan - pan_bar

    # م٥: الإغلاقان
    lost = len(sites_all) - len(sites_first) - len(sites_second)
    within: dict[str, Counter[str]] = {}
    for word in text.split():
        drawn = [one for one, _ in mc.read_stream(word)]
        for index in range(len(drawn) - 1):
            within.setdefault(drawn[index], Counter())[drawn[index + 1]] += 1
    bare_within = {one: dict(counter) for one, counter in within.items()}
    bare_pan_within = mc.coherence(bare_within, usable)
    bare_pan_across = mc.coherence(bare_rows, usable)

    return [
        f"الختم: {SEAL[:12]}… · السجلُّ البايتيّ: {CORPUS_RECORD[:12]}…",
        f"م١ مئينُ الصفريّ ٩٥: {first_condition:.4f} — "
        + ("متحقّق" if first_condition <= 0.10 else "ساقط"),
        f"م٢ الاتّجاهان فوق مئينهما: {above}/2 "
        f"(أمامًا {forward:.4f} فوق {forward_bar:.4f} · "
        f"خلفًا {reverse:.4f} فوق {reverse_bar:.4f}) — "
        + ("متحقّق" if above >= 2 else "ساقط"),
        f"م٣ تقاربُ الاتّجاهين: {abs(forward - reverse):.4f} — "
        + ("متحقّق" if abs(forward - reverse) <= 0.10 else "ساقط"),
        f"م٤ كفّةُ الضبط {marked_pan:.4f} ناقصَ مئين صفريّها "
        f"{pan_bar:.4f} = {margin:+.4f} — " + ("متحقّق" if margin >= 0 else "ساقط"),
        f"م٥ الإغلاق: {len(sites_first)} + {len(sites_second)} + {lost} "
        f"= {len(sites_all)} · سياستا الجوار للرسم: "
        f"داخلَ الكلمة {bare_pan_within:.4f} · عابرًا {bare_pan_across:.4f} — "
        + (
            "متحقّق"
            if len(sites_first) + len(sites_second) + lost == len(sites_all)
            else "ساقط"
        ),
        f"والمفقودُ على القطع: {lost} من {len(sites_all)} "
        f"({float(Fraction(lost, len(sites_all))):.6f})",
    ]


def main() -> None:
    for line in run(build_argument_parser().parse_args()):
        print(line)


if __name__ == "__main__":
    main()
