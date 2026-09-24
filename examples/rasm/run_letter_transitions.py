"""تعدادُ انتقالات الحروف: جدولٌ مرتَّبٌ بتساوٍ مُعلَن، وصفوفٌ تصلح لمقياس.

**ما يفعله هذا المُشغِّل**: يعُدّ الأزواجَ **المتعاقبة داخل الكلمة** — لا
المتراكبةَ على موضعٍ واحد — ويُخرِج ثلاثةَ أشياء: الجدولَ الخام، والهامشين
**الموضعيّين**، و**صفوفَ الاحتمال** `P(اللاحق | السابق)` التي يُقاس عليها
تماسكُ أيّ تقسيمٍ مُودَع (المخارج، أحكام النون).

`THE_CO_OCCURRENCE_CENSUS_IS_NOT_THE_ADJACENCY_CENSUS`: وأزواجُ العلامات
المتراكبة على موضعٍ واحد **تعايشٌ** لا تجاور، ودعاوى التنافر والأحكام كلُّها
عن التجاور. فالجدولان مقياسان لا مقياسٌ لجدولين، ولا يُنقَل رقمٌ من أحدهما
إلى الآخر.

`THE_MARGINS_COME_FROM_THE_POSITIONS_THAT_CAN_CARRY_THE_PAIR`: وآخرُ الكلمة
لا يبدأ زوجًا وأوّلُها لا يُنهيه؛ فالهامشان يُحسَبان من المواضع الحاملة
وحدَها. وإهمالُ ذلك ضخّم متوقَّعَ «هع» من ٢١٤ إلى ٣٨١ في أوّل تشغيلٍ سابق.

`A_TIE_IS_DECLARED_AND_NEVER_BROKEN`: وحين يتساوى زوجان في العدّ **يُعلَن
تساويهما** ولا يُفصَل بينهما بترتيب الأبجديّة ولا بأيّ حيلة. فالصدارةُ
لمجموعةٍ لا لواحد، وكسرُ التساوي صمتًا يصنع «أوّلَ» لا وجودَ له.

`A_PLAIN_TEXT_AND_AN_ALIGNMENT_ARE_TWO_DOORS_WITH_ONE_GATE`: وللمدخل بابان
لا واحد: محاذاةٌ بعمودٍ مُسمًّى (`--aligned`)، ونصٌّ سطرًا لكلّ آية
(`--text`). وبابُ النصّ لازمٌ لأنّ المدوّنةَ المُجمَّدةَ نصٌّ لا جدول؛ ولولاه
لاحتاج التشغيلُ **محوّلًا يُكتَب عند وصول البايتات**، وذلك نقضُ «بلا تعديلِ
سطر». والإغلاقُ في باب النصّ **عددُ الأسطر**، وفي باب المحاذاة عددُ الصفوف،
ويُسمَّى أيُّهما يُعَدّ.

`THE_INVENTORY_IS_A_DENOMINATOR_AND_IT_IS_DECLARED`: وعددُ الحروف الداخلةِ
يتبدّل بالسياسة، فيُطبَع مع كلّ جدول، ويُرَدّ التشغيلُ إن خالف ما أُعلِن
في `--expect-letters`.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import unicodedata
from collections import Counter
from fractions import Fraction
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


class TransitionError(ValueError):
    """رُدَّ تشغيلٌ بلا سياسةٍ أو بصمةٍ أو إغلاقٍ مُعلَن، أو بجردٍ مخالف."""


def drawn_letters(text: str, fold: dict[str, str], alphabet: str) -> str:
    """الرسمُ وحدَه بمقتضى السياسة؛ وعلاماتُ الضبط تُسقَط ولا تُعَدّ حرفًا."""

    out: list[str] = []
    for character in unicodedata.normalize("NFC", text):
        if ord(character) in MARKS:
            continue
        folded = fold.get(character, character)
        if folded and folded in alphabet:
            out.append(folded)
    return "".join(out)


def _checked(path: Path, policy: str, digest: str) -> tuple[dict[str, str], str]:
    """افحص السياسةَ والبصمةَ قبل قراءة حرفٍ واحد؛ وأرجِع أداةَ الرسم."""

    if policy not in POLICIES:
        raise TransitionError(
            f"سياسةٌ غيرُ مُعلَنةٍ «{policy}»؛ والمُعلَنُ: {'، '.join(POLICIES)}."
        )
    seen = hashlib.sha256(path.read_bytes()).hexdigest()
    if seen != digest:
        raise TransitionError(
            f"بصمةُ الملفّ {seen[:12]}… والمُعلَنةُ {digest[:12]}… — مدوّنتان لا مدوّنة."
        )
    return POLICIES[policy]


def _closed(counted: int, closure: int, unit: str) -> None:
    if counted != closure:
        raise TransitionError(
            f"{counted} {unit} في الملفّ و{closure} في الإغلاق المُعلَن؛ والفرقُ يُعلَن."
        )


def read_words(path: Path, policy: str, digest: str, closure: int) -> list[str]:
    """الكلماتُ من محاذاةٍ بعمود `surface`؛ والإغلاقُ عددُ الصفوف."""

    fold, alphabet = _checked(path, policy, digest)
    rows = 0
    words: list[str] = []
    with path.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            rows += 1
            word = drawn_letters(row["surface"], fold, alphabet)
            if word:
                words.append(word)
    _closed(rows, closure, "صفًّا")
    if not words:
        raise TransitionError("لا كلمةَ واحدةٌ قُرِئت؛ فالعمودُ أو المسارُ خطأ.")
    return words


def read_text_words(path: Path, policy: str, digest: str, closure: int) -> list[str]:
    """الكلماتُ من نصٍّ سطرًا لكلّ آية؛ والإغلاقُ **عددُ الأسطر** لا الصفوف.

    والسطرُ الفارغُ يُعَدّ سطرًا في الإغلاق ولا يُخرِج كلمة: فالإغلاقُ عن
    الملفّ كما هو، والعدُّ عن حروفه — ولا يُطوى أحدُهما في الآخر.
    """

    fold, alphabet = _checked(path, policy, digest)
    lines = path.read_text(encoding="utf-8").splitlines()
    words: list[str] = []
    for line in lines:
        for token in line.split():
            drawn = drawn_letters(token, fold, alphabet)
            if drawn:
                words.append(drawn)
    _closed(len(lines), closure, "سطرًا")
    if not words:
        raise TransitionError("لا كلمةَ واحدةٌ قُرِئت؛ فالمسارُ أو الترميزُ خطأ.")
    return words


def census(
    words: list[str],
) -> tuple[Counter[tuple[str, str]], Counter[str], Counter[str], int]:
    """(الانتقالاتُ، هامشُ السابق، هامشُ اللاحق، المواضعُ) — داخلَ الكلمة وحدَها."""

    pairs: Counter[tuple[str, str]] = Counter()
    first: Counter[str] = Counter()
    second: Counter[str] = Counter()
    places = 0
    for word in words:
        for index in range(len(word) - 1):
            before, after = word[index], word[index + 1]
            pairs[(before, after)] += 1
            first[before] += 1
            second[after] += 1
            places += 1
    return pairs, first, second, places


def rows_of_probability(
    pairs: Counter[tuple[str, str]], first: Counter[str]
) -> dict[str, dict[str, Fraction]]:
    """`P(اللاحق | السابق)` بكسورٍ صحيحة؛ وصفٌّ بلا وقوعٍ لا يُصطنَع له توزيع."""

    rows: dict[str, dict[str, Fraction]] = {}
    for (before, after), count in pairs.items():
        total = first[before]
        if total:
            rows.setdefault(before, {})[after] = Fraction(count, total)
    return rows


def tied_leaders(pairs: Counter[tuple[str, str]]) -> tuple[int, list[tuple[str, str]]]:
    """(أعلى عدّ، كلُّ من بلغه) — والصدارةُ لمجموعةٍ لا لواحد."""

    if not pairs:
        return 0, []
    highest = max(pairs.values())
    return highest, sorted(one for one, count in pairs.items() if count == highest)


def expectation(
    first: Counter[str], second: Counter[str], places: int, pair: tuple[str, str]
) -> Fraction:
    """المتوقَّعُ تحت الاستقلال بهامشين **موضعيّين**؛ ومواضعُ صفرٌ لا تُقسَم."""

    if places <= 0:
        raise TransitionError("لا موضعَ جوارٍ يُعَدّ؛ فالمتوقَّعُ بلا مقام.")
    before, after = pair
    return Fraction(first[before] * second[after], places)


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="تعدادُ انتقالات الحروف ببصمته")
    doors = parser.add_mutually_exclusive_group(required=True)
    doors.add_argument("--aligned", type=Path, help="محاذاةٌ بعمود `surface`")
    doors.add_argument("--text", type=Path, help="نصٌّ سطرًا لكلّ آية")
    parser.add_argument("--digest", required=True)
    parser.add_argument("--closure", type=int, required=True)
    parser.add_argument("--policy", choices=sorted(POLICIES), required=True)
    parser.add_argument("--expect-letters", type=int, default=None)
    parser.add_argument("--top", type=int, default=5)
    return parser


def run(arguments: argparse.Namespace) -> list[str]:
    """شغِّل التعدادَ واطبع الجردَ والصدارةَ المتساوية والهامشين."""

    door = arguments.aligned if arguments.aligned is not None else arguments.text
    reader = read_words if arguments.aligned is not None else read_text_words
    words = reader(door, arguments.policy, arguments.digest, arguments.closure)
    pairs, first, second, places = census(words)
    inventory = sorted(set(first) | set(second))
    if arguments.expect_letters is not None and len(inventory) != (
        arguments.expect_letters
    ):
        raise TransitionError(
            f"الجردُ {len(inventory)} حرفًا والمُعلَنُ {arguments.expect_letters}؛ "
            "والمقامُ يُعلَن قبل الجدول لا بعده."
        )
    highest, leaders = tied_leaders(pairs)
    rows = rows_of_probability(pairs, first)

    lines = [
        f"النسبة: {door.name} ({arguments.digest[:8]}…) · "
        f"السياسة: {arguments.policy} · "
        f"الإغلاق: {arguments.closure} "
        + ("صفًّا" if arguments.aligned is not None else "سطرًا"),
        f"الجرد: {len(inventory)} حرفًا · الخانات: {len(inventory) ** 2}",
        f"المواضع: {places} · الأزواجُ المرصودة: {len(pairs)} · "
        f"الخالية: {len(inventory) ** 2 - len(pairs)}",
        f"الصدارة: {highest} — وبلغها {len(leaders)}: "
        + "، ".join(f"{one}{two}" for one, two in leaders[:8]),
        f"صفوفُ الاحتمال المبنيّة: {len(rows)} من {len(inventory)}",
    ]
    for pair, count in pairs.most_common(arguments.top):
        expected = expectation(first, second, places, pair)
        lines.append(
            f"  {pair[0]}{pair[1]}: مرصود {count} · متوقَّع "
            f"{float(expected):.2f} · النسبة {float(count / expected):.2f}"
        )
    lines.append("والتساوي يُعلَن ولا يُكسَر، والهامشان موضعيّان لا عامّان.")
    return lines


def main() -> None:
    for line in run(build_argument_parser().parse_args()):
        print(line)


if __name__ == "__main__":
    main()
