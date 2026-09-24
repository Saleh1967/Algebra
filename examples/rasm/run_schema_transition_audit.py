"""تدقيقُ المخطّط بالسلوك: مجموعاتُ التراث تُعرَض على فضاء الانتقال المقيس.

**ما يفعله**: ينفّذ التسجيلَ المختوم
`9ed9eeead8cb2fa512cdde14fa9d4cca2538d4d48a8eb8035968f86604fa2673`:
يبني صفوفَ `P(اللاحق | السابق)` من تعدادٍ **لم يرَ التقسيم**، ثمّ يعرض
عليها مخارجَ الحروف المُودَعة ويقيس تماسكَها بصفريٍّ يبدّل وسومَ المجموعات
على الحروف — فالجدولُ ثابتٌ والهامشان محفوظان بالبناء.

`THE_SINGLETONS_ARE_EXCLUDED_AND_THE_EXCLUSION_IS_DECLARED`: ومخرجٌ فيه
حرفٌ واحدٌ **لا تشابهَ داخلَه يُقاس**، فيخرج من حساب «داخلَ المجموعة»
ويُعَدّ خارجًا لا يُطوى. وذلك شرطُ خ٤ بعينه.

`THE_NUN_JUNCTION_IS_NOT_MEASURED_WITHOUT_A_NAMED_SOURCE`: وأحكامُ النون
معرَّفةٌ عند نونٍ **ساكنة**، والسكونُ صفةُ قراءةٍ لا رسم. فإن لم يُسمَّ
مصدرُ الضبط **لم يُقَس الملتقى ألبتّة**، وسقط خ٥، وصار خ٢ ساقطَ الأساس.

`A_NAMED_SOURCE_IS_NOT_A_NAMED_READING_AND_THE_OUTPUT_SAYS_SO`: والمُسمّى
ههنا **مصدرُ البايتات** (`tanzil`) بتوقيع صاحب المستودع، لا **الروايةُ**.
وهما حقلان لا حقل: المصدرُ يقول من أين جاء الضبط، والروايةُ تقول ضبطَ مَن
هو. فالنتيجةُ منسوبةٌ إلى **سكونٍ كما وسَمه هذا المصدر**، لا إلى «العربيّة»
ولا إلى روايةٍ بعينها — وذلك يكفي لغرض خ٥ (منعِ النسبة إلى العربيّة)، ولا
يكفي لنسبةٍ إلى راوٍ. ويُطبَع الفرقُ مع الرقم لا في حاشيته.

`THE_SEAL_NAMED_A_PARTITION_THE_TREE_DOES_NOT_HOLD`: وخ٢ يُقابِل المستخرَجَ
بالتقسيم الخماسيّ ٦/٤/٢/١/١٥. **وذلك التقسيمُ غيرُ مُودَعٍ في هذه الشجرة**:
المُودَعُ مجموعتان فقط — إظهارٌ (ءهعحغخ) وإدغامٌ (يرملون) — فيلزم منهما
ثلاثيٌّ ٦/٦/١٦ لا خماسيّ. ولا أكتب الخماسيَّ بيدي: كتابتُه إيداعٌ، والإيداعُ
توقيعٌ. فيبقى خ٢ **باطلَ الأساس بعلّةٍ ثانية**، ويُنشَر المؤشّرُ على
الثلاثيّ المُودَع **خارجَ الختم** مُسمًّى بما هو، لا تحت اسم خ٢.

`THE_EXTRACTION_IS_A_RATE_NOT_A_COUNT`: واستخراجُ التقسيم من **نصيب** كلّ
حرفٍ: كم مرّةً وقع بعد نونٍ موسومةٍ بالسكون، مقسومًا على وقوعه لاحقًا في
النصّ كلِّه. فالحرفُ الشائعُ لا يعلو بشيوعه، والنادرُ لا يهبط بندرته.
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


NAMED_SOURCES: tuple[str, ...] = ("tanzil",)
"""مصدرُ الضبط، مُسمًّى بتوقيع صاحب المستودع لا باستنباطٍ من خارج الشجرة."""

NAMED_READINGS: tuple[str, ...] = ()
"""الرواياتُ المُسمّاة؛ ولا واحدةَ بعدُ — والمصدرُ غيرُ الرواية."""


SUKUN = "\u0652"
MARKS_RANGE = (0x064B, 0x0655)
OTHER_MARKS = (0x0640, 0x0670, 0x06DF)


def letters_with_sukun(
    text: str, fold: dict[str, str], alphabet: str
) -> list[tuple[str, bool]]:
    """تسلسلُ (الحرفِ، أعليه سكون؟) عبر النصّ كلِّه، لا داخلَ الكلمة وحدَها.

    فأحكامُ النون تعبر الكلمةَ إلى ما بعدها بنصّ التراث، فيُعَدّ التاليَ
    حرفًا في مجرى النصّ لا في مجرى الكلمة — وذلك مُعلَنٌ لا مفترض.
    """

    import unicodedata

    stream = unicodedata.normalize("NFC", text)
    out: list[tuple[str, bool]] = []
    index = 0
    while index < len(stream):
        folded = fold.get(stream[index], stream[index])
        if folded in alphabet:
            step = index + 1
            marks = ""
            while step < len(stream) and (
                MARKS_RANGE[0] <= ord(stream[step]) <= MARKS_RANGE[1]
                or ord(stream[step]) in OTHER_MARKS
            ):
                marks += stream[step]
                step += 1
            out.append((folded, SUKUN in marks))
            index = step
        else:
            index += 1
    return out


def post_nun_rates(stream: list[tuple[str, bool]], alphabet: str) -> dict[str, float]:
    """نصيبُ كلّ حرفٍ من الوقوع بعد نونٍ موسومةٍ بالسكون، منسوبًا إلى وقوعه لاحقًا."""

    after: Counter[str] = Counter()
    follower: Counter[str] = Counter()
    for index in range(len(stream) - 1):
        current, marked = stream[index]
        nxt = stream[index + 1][0]
        follower[nxt] += 1
        if current == "ن" and marked:
            after[nxt] += 1
    return {
        letter: (after[letter] / follower[letter]) if follower[letter] else 0.0
        for letter in alphabet
    }


def five_way_split(rates: dict[str, float], seed: int) -> dict[str, int]:
    """تقسيمٌ خماسيٌّ على بُعدٍ واحدٍ بمراكزَ تبدأ من الخمسينات، محسومٌ بالبذرة."""

    letters = sorted(rates)
    values = [rates[one] for one in letters]
    ordered = sorted(values)
    centres = [
        ordered[min(len(ordered) - 1, (len(ordered) * k) // 5)] for k in range(5)
    ]
    for _ in range(50):
        groups = [
            min(range(5), key=lambda k: abs(value - centres[k])) for value in values
        ]
        moved = False
        for k in range(5):
            members = [value for value, group in zip(values, groups) if group == k]
            if members:
                centre = sum(members) / len(members)
                if centre != centres[k]:
                    centres[k] = centre
                    moved = True
        if not moved:
            break
    _ = seed  # البذرةُ مُعلَنةٌ وإن كان البدءُ حتميًّا، فلا عشوائيّةَ تُخفى
    return dict(zip(letters, groups, strict=True))


def adjusted_rand(first: dict[str, int], second: dict[str, int]) -> float:
    """مؤشّرُ رَند المعدَّل بين تقسيمين على المجموعة نفسِها."""

    keys = sorted(set(first) & set(second))
    if len(keys) < 2:
        raise AuditError("تقسيمان على أقلَّ من عنصرين لا يُقارَنان.")
    table: Counter[tuple[int, int]] = Counter((first[one], second[one]) for one in keys)
    rows: Counter[int] = Counter(first[one] for one in keys)
    columns: Counter[int] = Counter(second[one] for one in keys)

    def choose(value: int) -> float:
        return value * (value - 1) / 2

    index = sum(choose(count) for count in table.values())
    row_sum = sum(choose(count) for count in rows.values())
    column_sum = sum(choose(count) for count in columns.values())
    total = choose(len(keys))
    expected = row_sum * column_sum / total
    highest = (row_sum + column_sum) / 2
    if highest == expected:
        raise AuditError("تقسيمان لا يترك أحدُهما مجالًا للمؤشّر.")
    return (index - expected) / (highest - expected)


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

    from alghanem.arabic.phonetic_economy_tool import (
        IDGHAM_NUN_LETTERS,
        IZHAR_NUN_LETTERS,
    )

    fold, alphabet = census.POLICIES[arguments.policy]  # type: ignore[attr-defined]
    stream = letters_with_sukun(
        arguments.text.read_text(encoding="utf-8"), fold, alphabet
    )
    rates = post_nun_rates(stream, alphabet)
    extracted = five_way_split(rates, arguments.seed)

    def deposited(letter: str) -> int:
        if letter in IZHAR_NUN_LETTERS:
            return 0
        if letter in IDGHAM_NUN_LETTERS:
            return 1
        return 2

    three_way = {one: deposited(one) for one in alphabet}
    rand = adjusted_rand(extracted, three_way)
    junction = sum(
        1
        for index in range(len(stream) - 1)
        if stream[index][0] == "ن" and stream[index][1]
    )
    deposited_sizes = Counter(three_way.values())

    inside, outside, within_pairs, between_pairs = coherence(rows, usable)
    share = headroom(inside, outside)
    reached, highest = permuted_null(rows, usable, arguments.replicates, arguments.seed)
    p_value = Fraction(reached + 1, arguments.replicates + 1)
    readings = NAMED_READINGS

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
        "خ٢ استخراجُ تقسيم النون: **باطلُ الأساس** — التقسيمُ الخماسيُّ "
        "٦/٤/٢/١/١٥ غيرُ مُودَعٍ في الشجرة، ولا يُكتَب بيدٍ ههنا",
        f"خ٣ الصفريّات: {arguments.replicates} · بلغها {reached} · "
        f"p = {float(p_value):.5f} · أرضيّة {Fraction(1, arguments.replicates + 1)} "
        f"· أعلى صفريّ {highest:.4f}",
        f"خ٤ أصغرُ مجموعةٍ داخلة: {smallest} — " + ("متحقّق" if smallest >= 2 else "ساقط"),
        f"خ٥ المصادرُ المُسمّاة: {len(NAMED_SOURCES)} "
        f"({'، '.join(NAMED_SOURCES)}) · الرواياتُ المُسمّاة: {len(readings)} — "
        + ("متحقّق بالمصدر" if NAMED_SOURCES else "ساقط"),
        "— قراءةٌ مُعلَنةٌ خارجَ الختم (ليست خ٢) —",
        f"ملتقى النون الموسومةِ بالسكون: {junction} موضعًا",
        f"التقسيمُ المُودَعُ ثلاثيٌّ: {dict(sorted(deposited_sizes.items()))} "
        "(إظهارٌ · إدغامٌ · الباقي)",
        f"مؤشّرُ رَند المعدَّل بين المستخرَج والمُودَع الثلاثيّ: {rand:.4f}",
        "والنتيجةُ منسوبةٌ إلى سكونٍ كما وسَمه المصدرُ المُسمّى، "
        "لا إلى روايةٍ بعينها ولا إلى «العربيّة».",
    ]


def main() -> None:
    for line in run(build_argument_parser().parse_args()):
        print(line)


if __name__ == "__main__":
    main()
