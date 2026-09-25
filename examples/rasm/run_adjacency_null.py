"""أصفارُ الجوار: كم خانةً تخلو، وكم يُتوقَّع خلوُّها بالصدفة وحدَها.

**السؤالُ الذي يحسمه رقمٌ واحد**: خانةٌ خاليةٌ في جدول الجوار — أهي منعٌ في
اللغة أم صدفةٌ من الندرة؟ ولا تُجاب بعتبةٍ لكلّ خانةٍ على حدة، بل **بعددٍ
واحد**: مجموعُ `exp(−E)` على الخانات كلِّها، أي كم خانةً يُتوقَّع خلوُّها
تحت الاستقلال. فإن قارب المرصودَ فلا خبرَ فيه، وإن قارب الصفرَ فكلُّه خبر.

`AN_EXPECTATION_OF_A_HALF_IS_NOT_A_RESCUE`: وعتبةُ «متوقَّعٌ فوق نصف» لا
تكفي: احتمالُ خلوّ خانةٍ متوقَّعُها نصفٌ **٦٠٫٧٪** — فخلوُّها هو الأرجح.
والعتبةُ التي تجعل الخلوَّ نادرًا (٥٪) هي ثلاثة.

`THE_MARGINS_MUST_COME_FROM_THE_POSITIONS_THAT_CAN_CARRY_THE_PAIR`: وحرفٌ
يقع في آخر الكلمة **لا يبدأ زوجًا**، وحرفٌ في أوّلها لا يُنهي زوجًا. فمن
حسب الهامشَ من الحروف كلِّها ضخّم متوقَّعَ كلّ خانةٍ صدرُها حرفٌ غالبُه
نهائيّ. وذلك وقع ههنا أوّلَ مرّة: متوقَّعُ «هع» كان ٣٨١ فصار **٢١٤** بعد
تصحيح الهامشين — أي أنّ الخطأَ كان يضخّمه الضِّعفَ تقريبًا.

`A_JOINING_SPACE_IS_NOT_A_LETTER_OF_THE_LANGUAGE`: وأوّلُ تشغيلٍ ضمّ الفراغَ
إلى المفردة، فخرجت أقوى خانةٍ خاليةٍ «فراغٌ يتلوه فراغ» بمتوقَّعٍ ١٤٬٩٨٦ —
وهي **أثرُ وصلٍ في الآلة** لا خبرٌ عن العربيّة، إذ لا يتجاور فراغان أصلًا.
فصار العدُّ داخلَ الكلمة وحدَها، والمفردةُ حروفٌ لا غير.

`THE_FOLDING_POLICY_IS_DECLARED_BECAUSE_IT_MOVES_THE_ANSWER`: وردُّ الهمزات
إلى حواملها وطيُّ التاء المربوطة والألف المقصورة **يغيّر الجواب**: ١٤٤ خانةً
خاليةً بمتوقَّعٍ ٠٫٦١ إن طُوِيت، و٣٧٤ بمتوقَّعٍ ٣٩٫١٧ إن فُصِلت. والفائضُ
قائمٌ في الحالين، والعددُ ليس واحدًا. فالسياسةُ تُعلَن بـ`--policy` ويُرَدّ
التشغيلُ بدونها.
"""

from __future__ import annotations

import argparse
import csv
import math
import unicodedata
from collections import Counter
from pathlib import Path

BASE = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
MARKS = frozenset(range(0x064B, 0x0653)) | {
    0x0640,
    0x0670,
    0x06DF,
    0x0653,
    0x0654,
    0x0655,
}

POLICIES: dict[str, tuple[dict[str, str], str]] = {
    "مطويّ": (
        {
            "أ": "ا",
            "إ": "ا",
            "آ": "ا",
            "ٱ": "ا",
            "ة": "ه",
            "ى": "ي",
            "ؤ": "و",
            "ئ": "ي",
            "ء": "",
        },
        BASE,
    ),
    "مفصول": ({"ٱ": "ا"}, BASE + "أإآةىؤئء"),
}
"""سياستا التسوية المُعلَنتان؛ وهما تعطيان جوابين، فتُسمّى الواحدةُ منهما."""

BANDS: tuple[tuple[float, float, str], ...] = (
    (0.0, 0.5, "مُنقَذٌ بالندرة"),
    (0.5, 3.0, "غيرُ حاسم"),
    (3.0, 5.0, "خبرٌ ضعيف"),
    (5.0, 20.0, "خبرٌ قويّ"),
    (20.0, float("inf"), "خبرٌ قاطع"),
)


class AdjacencyError(ValueError):
    """رُفض تشغيلٌ بلا سياسةٍ مُعلَنة، أو بمدوّنةٍ لا تُقرَأ."""


def strip_to_rasm(text: str, fold: dict[str, str], alphabet: str) -> str:
    """الرسمُ وحدَه بمقتضى السياسة المُعلَنة؛ وعلاماتُ الضبط تُسقَط."""

    out: list[str] = []
    for character in unicodedata.normalize("NFC", text):
        if ord(character) in MARKS:
            continue
        folded = fold.get(character, character)
        if folded and folded in alphabet:
            out.append(folded)
    return "".join(out)


def read_words(path: Path, policy: str) -> list[str]:
    """الكلماتُ مرسومةً؛ والعمودُ `surface` وحدَه يُقرَأ."""

    if policy not in POLICIES:
        raise AdjacencyError(
            f"سياسةُ تسويةٍ غيرُ مُعلَنةٍ «{policy}»؛ والمُعلَنُ: "
            f"{'، '.join(POLICIES)}. وهما يعطيان جوابين لا جوابًا."
        )
    fold, alphabet = POLICIES[policy]
    words: list[str] = []
    with path.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            drawn = strip_to_rasm(row["surface"], fold, alphabet)
            if drawn:
                words.append(drawn)
    if not words:
        raise AdjacencyError("لا كلمةَ واحدةٌ قُرِئت؛ فالعمودُ أو المسارُ خطأ.")
    return words


def table(words: list[str], policy: str) -> tuple[Counter, Counter, Counter, int]:
    """(جوارٌ مرصود، هامشٌ أوّل، هامشٌ ثانٍ، مواضعُ الجوار) — داخلَ الكلمة.

    والهامشان من المواضع التي **تحمل الزوج**: فآخرُ الكلمة لا يبدأ زوجًا،
    وأوّلُها لا يُنهيه. وإهمالُ ذلك يضخّم المتوقَّع.
    """

    del policy
    pairs = Counter((a, b) for word in words for a, b in zip(word, word[1:]))
    first = Counter(a for word in words for a in word[:-1])
    second = Counter(b for word in words for b in word[1:])
    positions = sum(pairs.values())
    if positions != sum(first.values()) or positions != sum(second.values()):
        raise AdjacencyError("الهامشان لا يوازنان المواضعَ؛ وذلك عيبٌ في العدّ.")
    return pairs, first, second, positions


def report(path: Path, policy: str) -> int:
    """المرصودُ والمتوقَّعُ معًا؛ ولا يُطبَع أحدُهما وحدَه."""

    words = read_words(path, policy)
    _, alphabet = POLICIES[policy]
    pairs, first, second, positions = table(words, policy)

    empty: list[tuple[str, float]] = []
    expected_empty = 0.0
    for left in alphabet:
        for right in alphabet:
            chance = positions * (first[left] / positions) * (second[right] / positions)
            expected_empty += math.exp(-chance)
            if pairs[(left, right)] == 0:
                empty.append((f"{left}{right}", chance))

    cells = len(alphabet) ** 2
    print(f"السياسةُ: {policy}  ·  الجردُ: {len(alphabet)} حرفًا  ·  الخانات: {cells}")
    print(f"كلماتٌ: {len(words):,}  ·  مواضعُ الجوار: {positions:,}\n")
    print(f"خاناتٌ خاليةٌ **مرصودة** : {len(empty)}")
    print(f"ويُتوقَّع خلوُّها **صدفةً**: {expected_empty:.2f}")
    print(f"الفائضُ فوق الصدفة       : {len(empty) - expected_empty:+.2f}\n")

    for low, high, name in BANDS:
        band = [one for one in empty if low <= one[1] < high]
        print(f"  {name:16} ({low:g} ≤ E < {high:g})  {len(band):4}")

    print("\nأقوى ستٍّ من الخالي:")
    for name, chance in sorted(empty, key=lambda one: -one[1])[:6]:
        print(f"   «{name}»  متوقَّعٌ {chance:9.1f}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="أصفارُ الجوار ومتوقَّعُها")
    parser.add_argument("--aligned", type=Path, required=True)
    parser.add_argument(
        "--policy",
        default="",
        help=f"سياسةُ التسوية المُعلَنة: {'، '.join(POLICIES)}",
    )
    args = parser.parse_args(argv)

    if not args.policy:
        parser.error(
            "سياسةُ التسوية تُعلَن بـ`--policy`؛ فطيُّ الهمزات يغيّر الجواب "
            "من ١٤٤ خانةً إلى ٣٧٤، والمتوقَّعَ من ٠٫٦١ إلى ٣٩٫١٧."
        )
    return report(args.aligned, args.policy)


if __name__ == "__main__":
    raise SystemExit(main())
