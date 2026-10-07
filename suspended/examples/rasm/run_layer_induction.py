"""استقراءُ الطبقات: تُبنى الطبقاتُ إسقاطًا، ثمّ يُستقرَأ عليها أربعُ مبرهنات.

**البناءُ استقراءً (induction for)**: أبجديّةُ الأساس ذرّاتٌ (حرفٌ + صنفُ
علامته)، وكلُّ طبقةٍ إسقاطٌ منها. ويمتدّ الإسقاطُ إلى التيار بالاستقراء على
الطول، وتُبنى سلسلةُ الرتبة `k` بالاستقراء على `k`.

**الاستقراءُ عليها (induction on)**: أربعُ دعاوى تُفحَص لا تُفترَض —
حفظُ التدفّق (هُويّةٌ بالاستقراء على الطول)، وتناقصُ المعلومات بالتخشين
(مبرهنةُ معالجة المعطيات)، وتناقصُ `h_k` بالرتبة مع مقامها، وشرطُ
التكتيل الشديد (كيمني وسنل) الذي يفصل **المستوى** عن **الظلّ**.

**قراراتٌ تُعلَن ولا تُطوى**: الجوارُ **عابرٌ لحدّ الكلمة** في تيار الذرّات
(كما في `6a584a5a…`)، و**داخلَ السطر** في تيار التوكن. وأرضيّةُ قراءة
الرتبة **عشرةُ وقوعاتٍ لكلّ سياق**. وطبقةُ التوكن **مقامٌ آخر**، فلا
يُقارَن رقمُها برقم الذرّات طرحًا.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
LADDER_DEPOSIT = REPOSITORY / "deposits" / "ladder_map.tsv"
CONTEXT_FLOOR = 10
MASS_FLOOR = 30
VACANT: tuple[tuple[str, str], ...] = (
    ("الوظيفيّ", "قائمةُ الأدوات المُودَعةُ تفصل الأداةَ عن الاسم والفعل"),
    ("الصرفيّ", "وسمٌ صرفيٌّ لكلّ توكن (بنيةً وزوائدَ)، ولا مُودَعَ منه"),
    ("النحويّ", "وسمُ المقولة لكلّ توكن، ولا مُودَعَ منه"),
    (
        "الاشتقاقيّ",
        "جدولُ الجذور مُودَعٌ، و**الإسقاطُ** من توكن المصحف إلى جذره ليس كذلك",
    ),
    (
        "الدلاليّ",
        "محاورُ ابن فارس مُودَعةٌ بالجذر، والإسقاطُ إلى التوكن مفقودٌ كسابقه",
    ),
)
"""خمسُ طبقاتٍ موادُّها حاضرةٌ أو غائبة، وإسقاطُها مفقودٌ في الحالين.

والطبقةُ إسقاطٌ لا تسمية؛ فغيابُه غيابُ الطبقة، ويُصنَّف `UNREACHABLE`:
لا تُبلَغ بما في اليد — لا مستحيلةً ولا مردودةً ولا غيرَ مشهودة.
"""

ORGANS: tuple[tuple[str, range], ...] = (
    ("حلق", range(2, 5)),
    ("لسان", range(5, 13)),
    ("شفتان", range(13, 15)),
)


class InductionError(ValueError):
    """رُدَّ تشغيلٌ لنقصِ مُودَعٍ أو بابٍ أو لرمزٍ خارجَ إسقاط."""


def _algebra() -> object:
    sys.path.insert(0, str(REPOSITORY / "src"))
    import algebra.markov_layers as module

    return module


def read_ladder() -> dict[str, int]:
    """خريطةُ ٢٨ ← الموضعِ من المُودَع؛ والهمزةُ المفردةُ تُطوى في الألف."""

    if not LADDER_DEPOSIT.is_file():
        raise InductionError(
            f"خريطةُ السلّم غيرُ مُودَعةٍ في {LADDER_DEPOSIT}؛ "
            "ولا تُكتَب ههنا، فنسبةُ متنٍ إلى قائله توقيع."
        )
    out: dict[str, int] = {}
    for line in LADDER_DEPOSIT.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith(("#", "letter")):
            continue
        parts = line.split("\t")
        letter = "ا" if parts[0].strip() == "ء" else parts[0].strip()
        out[letter] = int(parts[1])
    return out


def organ_of(place: int) -> str:
    for name, span in ORGANS:
        if place in span:
            return name
    raise InductionError(f"موضعٌ {place} خارجَ الأعضاء الثلاثة المُعلَنة.")


def build_layers(atoms: list[str], ladder: dict[str, int]) -> list[object]:
    """الطبقاتُ الأربعُ المُودَعُ إسقاطُها، من الأدقّ إلى الأخشن."""

    markov = _algebra()
    layer = markov.Layer  # type: ignore[attr-defined]
    present = sorted(set(atoms))
    letters = {one: one.split("|")[0] for one in present}
    marks = {one: one.split("|")[1] for one in present}
    places = {one: str(ladder[letters[one]]) for one in present}
    organs = {one: organ_of(ladder[letters[one]]) for one in present}
    return [
        markov.identity_layer(present, "الترميزيّ (ذرّة)"),  # type: ignore[attr-defined]
        layer(name="الإملائيّ (رسم)", projection=letters),
        layer(name="الحركيّ (صنفُ العلامة)", projection=marks),
        layer(name="الصوتيّ (موضعُ السلّم)", projection=places),
        layer(name="الصوتيّ الأخشن (عضو)", projection=organs),
    ]


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="استقراءُ طبقات ماركوف")
    parser.add_argument("--text", type=Path, required=True)
    parser.add_argument("--orders", type=int, default=4)
    return parser


def _reader() -> object:
    path = REPOSITORY / "examples" / "rasm" / "run_marked_contrast.py"
    spec = importlib.util.spec_from_file_location("run_marked_contrast", path)
    if spec is None or spec.loader is None:  # pragma: no cover - بابٌ لا يُبلَغ
        raise InductionError("قارئُ التيار غيرُ موجودٍ في موضعه المُعلَن.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run(arguments: argparse.Namespace) -> list[str]:
    markov = _algebra()
    reader = _reader()
    text = arguments.text.read_text(encoding="utf-8")
    stream = reader.read_stream(text)  # type: ignore[attr-defined]
    atoms = [f"{one}|{kind}" for one, kind in stream]
    ladder = read_ladder()
    layers = build_layers(atoms, ladder)

    base = markov.bigram_census(atoms)  # type: ignore[attr-defined]
    lines = [
        f"الأساس: {len(atoms):,} ذرّةً · أبجديّتُه {len(set(atoms))} · "
        f"جوارٌ عابرٌ لحدّ الكلمة",
        f"خريطةُ السلّم: {LADDER_DEPOSIT.name} ({len(ladder)} حرفًا)",
        "",
        f"أرضيّةُ الصادر في التكتيل: {MASS_FLOOR} وقوعًا · "
        f"أرضيّةُ قراءة الرتبة: {CONTEXT_FLOOR}",
        "",
        "الطبقة                  |Λ|      I      H(·|·)   خللٌ خام  خللٌ بأرضيّة"
        "  موزونٌ  مستبعَدة",
    ]
    informations: list[float] = []
    for one in layers:
        census = markov.project_census(base, one)  # type: ignore[attr-defined]
        information = markov.mutual_information(census)  # type: ignore[attr-defined]
        conditional = markov.conditional_entropy(census)  # type: ignore[attr-defined]
        raw = markov.lumpability(base, one)  # type: ignore[attr-defined]
        held = markov.lumpability(base, one, MASS_FLOOR)  # type: ignore[attr-defined]
        informations.append(information)
        lines.append(
            f"{one.name:<24}{len(one.alphabet):>4}  {information:7.4f}  "
            f"{conditional:7.4f}   {float(raw.defect):.4f}    {float(held.defect):.4f}"
            f"      {float(held.weighted):.4f}  {held.excluded_states:>4}"
            + ("  مستوًى" if held.is_strong else "  ظلّ")
        )

    lines.append("")
    ordered = [
        (layers[index].name, informations[index]) for index in range(1, len(layers))
    ]
    falls = all(
        informations[index] >= informations[index + 1] - 1e-12
        for index in (1, 3)  # رسم ⊒ موضع ⊒ عضو
    )
    lines.append(
        "مبرهنةُ المعالجة على السلسلة (رسم ⊒ موضع ⊒ عضو): "
        + ("تصدق" if falls else "**تُخرَق**")
        + " — "
        + " ≥ ".join(
            f"{value:.4f}" for _, value in ordered if _ != "الحركيّ (صنفُ العلامة)"
        )
    )

    defect = markov.flow_defect(atoms)  # type: ignore[attr-defined]
    broken = {one: value for one, value in defect.items() if value != 0}
    lines.append(f"حفظُ التدفّق على الأساس: {'صفرٌ في كلّ رمز' if not broken else broken}")

    lines.append("")
    lines.append("سلّمُ الرتبة على الذرّات (h_k · سياقاتُه · متوسّطُ نصيبها):")
    for order in range(1, arguments.orders + 1):
        reading = markov.context_reading(atoms, order)  # type: ignore[attr-defined]
        lines.append(
            f"  k={order}  h={reading.entropy:7.4f}  سياقاتٌ {reading.contexts:>7,}  "
            f"نصيبٌ {float(reading.mean_count):8.2f}  "
            + ("مقروء" if reading.is_readable else "**دون الأرضيّة**")
        )

    lines.append("")
    lines.append("طبقاتٌ لا إسقاطَ لها مُودَعٌ — خانةٌ خاليةٌ مُصنَّفةٌ لا مطويّة:")
    for name, missing in VACANT:
        lines.append(f"  {name:<12} UNREACHABLE — {missing}")

    words = [one for line in text.splitlines() for one in line.split()]
    token_census = markov.bigram_census(words)  # type: ignore[attr-defined]
    lines.append("")
    lines.append(
        f"طبقةُ التوكن (مقامٌ آخر، لا يُطرَح من الأعلى): {len(words):,} توكنًا · "
        f"أنواعٌ {len(set(words)):,} · "
        f"I = {markov.mutual_information(token_census):.4f}"  # type: ignore[attr-defined]
    )
    for order in (1, 2):
        reading = markov.context_reading(words, order)  # type: ignore[attr-defined]
        lines.append(
            f"  k={order}  h={reading.entropy:7.4f}  سياقاتٌ {reading.contexts:>7,}  "
            f"نصيبٌ {float(reading.mean_count):8.2f}  "
            + ("مقروء" if reading.is_readable else "**دون الأرضيّة**")
        )
    return lines


def main() -> None:
    for line in run(build_argument_parser().parse_args()):
        print(line)


if __name__ == "__main__":
    main()
