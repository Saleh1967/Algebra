"""الصعودُ الجبريُّ المُرخَّص — تشغيلُ ختم `0021350c…`.

**ثلاثةُ بنودٍ مجتمعة**: الدالّيةُ الكلّيّة، والابتلاعُ (Δ = ٠ بلا قناةٍ
جانبيّةٍ ولا راية)، والاقتصادُ بتكلفةٍ **ذات شطرين** — معجمٌ يُهجّى بحروف
الطبقة الأدنى، وبيانٌ إنتروبيا **محجوزةً** في عدد الوحدات.

**وقاعدةُ المقطع المختومة** (بإصلاح `b8aa21e`): ألفُ الوصل تُحذَف في مبتدأ
كلمةٍ ليست مبتدأَ الآية، ومبتدأُ الآية يُفتَح، والتقطيعُ على الآية.

**وتُشغَّل معها صورةٌ ثانيةٌ خارج الختم** تُسمّى **الضامّة**: لا تحذف ألفَ
الوصل بل **تضمّها إلى المقطع صامتةً** — فيُقاس ثمنُ البندين حين يتعارضان،
ولا يُحكَم لواحدٍ منهما بغير عدّ.
"""

from __future__ import annotations

import argparse
import importlib.util
import math
import sys
from collections import Counter
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
PEEL = REPOSITORY / "examples" / "rasm" / "run_cv_peel.py"
FATHA, DAMMA, KASRA, SUKUN = "َ", "ُ", "ِ", "ْ"
SHORT = (FATHA, DAMMA, KASRA)
BASE_ALPHABET = 112
Unit = tuple[str, str]
Chunk = tuple[Unit, ...]


def _peel() -> object:
    spec = importlib.util.spec_from_file_location("run_cv_peel", PEEL)
    if spec is None or spec.loader is None:
        raise RuntimeError("لا قارئَ للتقشير")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def verses(text: str) -> list[list[list[Unit]]]:
    """كلُّ آيةٍ قائمةَ كلماتٍ، وكلُّ كلمةٍ قائمةَ وحدات."""

    peeler = _peel()
    built: list[list[list[Unit]]] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        units, _ = peeler.peel(line)  # type: ignore[attr-defined]
        words: list[list[Unit]] = []
        current: list[Unit] = []
        for base, value in units:
            if base == peeler.STRUCTURE:  # type: ignore[attr-defined]
                if current:
                    words.append(current)
                    current = []
            else:
                current.append((base, value))
        if current:
            words.append(current)
        if words:
            built.append(words)
    return built


def flatten(verse: list[list[Unit]], *, drop_wasl: bool) -> tuple[list[Unit], int]:
    """تيّارُ الآية، وعددُ ألفات الوصل المحذوفة إن أُمِرَ بالحذف."""

    stream: list[Unit] = []
    dropped = 0
    for place, word in enumerate(verse):
        start = 0
        if word and word[0] == ("ا", SUKUN):
            if place == 0:
                stream.append(("ا", FATHA))  # مبتدأُ الآية يُفتَح
                start = 1
            elif drop_wasl:
                dropped += 1
                start = 1
        stream.extend(word[start:])
    return (stream, dropped)


def syllabify(stream: list[Unit]) -> tuple[list[Chunk], int]:
    """(المقاطع، وحداتٌ لم تدخل) — القصيرةُ تفتح، والساكناتُ تلحق."""

    built: list[Chunk] = []
    loose = 0
    current: list[Unit] = []
    for unit in stream:
        if unit[1] in SHORT:
            if current:
                built.append(tuple(current))
            current = [unit]
        elif current:
            current.append(unit)
        else:
            loose += 1
    if current:
        built.append(tuple(current))
    return (built, loose)


def held_out(sequences: list[list[object]]) -> tuple[float, float]:
    """(الإنتروبيا المحجوزة، الملحَقة) بتًّا للرمز، بقسمة الآيات."""

    even: Counter[object] = Counter()
    odd: Counter[object] = Counter()
    for index, one in enumerate(sequences):
        (even if index % 2 == 0 else odd).update(one)
    whole = even + odd

    def cross(support: Counter[object], measure: Counter[object]) -> float:
        alphabet = max(len(support), 1)
        mass = sum(support.values())
        total = sum(measure.values())
        if not total:
            return 0.0
        return (
            -math.fsum(
                number * math.log2((support.get(symbol, 0) + 1) / (mass + alphabet))
                for symbol, number in measure.items()
            )
            / total
        )

    outside = (cross(even, odd) + cross(odd, even)) / 2
    mass = sum(whole.values())
    inside = -math.fsum(
        (number / mass) * math.log2(number / mass) for number in whole.values()
    )
    return (outside, inside)


def dictionary_bits(alphabet: set[tuple[object, ...]], below: int) -> float:
    """معجمٌ يُهجّى بحروف الطبقة الأدنى، ومعه طولُ كلّ مدخل."""

    if not alphabet:
        return 0.0
    longest = max(len(one) for one in alphabet)
    per_length = math.log2(longest + 1)
    return math.fsum(len(one) * math.log2(below) + per_length for one in alphabet)


def cost(
    sequences: list[list[tuple[object, ...]]], below: int
) -> tuple[float, float, float, int, int]:
    """(الجملة، المعجم، البيان، عددُ الوحدات، حجمُ الأبجديّة)."""

    flat = [one for row in sequences for one in row]
    alphabet = set(flat)
    outside, _ = held_out(sequences)  # type: ignore[arg-type]
    book = dictionary_bits(alphabet, below) if below else 0.0
    body = outside * len(flat)
    return (book + body, book, body, len(flat), len(alphabet))


def feet(built: list[Chunk]) -> list[tuple[Chunk, ...]]:
    """تفعيلةٌ = مقطعان متجاوران — تجميعٌ لا يحتاج حدَّ الكلمة."""

    return [tuple(built[one : one + 2]) for one in range(0, len(built), 2)]


def build(text: str, *, drop_wasl: bool) -> tuple[float, ...]:
    corpus = verses(text)
    streams: list[list[Unit]] = []
    dropped = 0
    for verse in corpus:
        stream, lost = flatten(verse, drop_wasl=drop_wasl)
        dropped += lost
        streams.append(stream)
    units = sum(len(one) for one in streams)

    syllables: list[list[Chunk]] = []
    loose = 0
    for stream in streams:
        made, missed = syllabify(stream)
        loose += missed
        syllables.append(made)
    paces = [feet(one) for one in syllables]
    lines = [[tuple(one)] for one in paces]

    body_zero = held_out(streams)[0] * units  # type: ignore[arg-type]
    first = cost(syllables, BASE_ALPHABET)  # type: ignore[arg-type]
    second = cost(paces, first[4])  # type: ignore[arg-type]
    third = cost(lines, second[4])  # type: ignore[arg-type]

    print(f"  وحداتُ L₀: {units} | محذوفٌ وصلًا: {dropped} | لم يدخل: {loose}")
    print(f"  L₀ الوحدة: عدد {units} | أبجديّة {BASE_ALPHABET} | الجملة {body_zero:.0f}")
    for name, step in (
        ("L₁ المقطع", first),
        ("L₂ التفعيلة", second),
        ("L₃ الآية", third),
    ):
        print(
            f"  {name}: عدد {step[3]} | أبجديّة {step[4]} | معجم {step[1]:.0f} "
            f"| بيان {step[2]:.0f} | الجملة {step[0]:.0f}"
        )
    print(
        f"  النسب: L₁/L₀ {first[0] / body_zero:.4f} | "
        f"L₂/L₁ {second[0] / first[0]:.4f} | L₃/L₂ {third[0] / second[0]:.4f}"
    )
    recovered = sum(len(one) for row in syllables for one in row)
    print(f"  الابتلاع: مستعادٌ {recovered} | فاقدٌ {dropped + loose}")
    return (body_zero, first[0], second[0], third[0], float(dropped), float(loose))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()
    text = given.text.read_text(encoding="utf-8")
    print("— الصورةُ المختومة (ألفُ الوصل تُحذَف)")
    build(text, drop_wasl=True)
    print("\n— الصورةُ الضامّة (خارجَ الختم: تُضَمّ صامتةً)")
    build(text, drop_wasl=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
