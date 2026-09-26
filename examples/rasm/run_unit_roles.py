"""الـ١١٢ وأدوارُها — تشغيلُ ختم `a581ddb9…`: جامعٌ مانعٌ عند البايتات وعند الأدوار.

**عند البايتات**: كلُّ نقطةِ ترميزٍ في الملفّ تُسنَد إلى قناةٍ واحدةٍ بالضبط،
ثمّ تُعاد البايتاتُ من الوحدات وقنوات الباقي. فلا بتَّ بلا قناة.

**عند الأدوار**: سجلٌّ من خمسةَ عشرَ مستوًى على كلّ وحدةٍ من الـ١١٢. ولكلّ
خانةٍ قيمةٌ ومصدرٌ مسمًّى، أو `UNCLASSIFIED` وما تحتاجه مكتوب. **ولا يُكتَب في
السجلّ من المحفوظ ما منعته الشجرة**: الصفات (حاجز `SIFA_TABLE_BYTES`)،
وقيمُ الجُمَّل، والجذور.

**والمصادرُ ستّة، مغلقة**: بايتات · اصطلاح الشجرة · مُودَع · نصّ صاحب
المستودع · منقول من الكتاب · UNCLASSIFIED.
"""

from __future__ import annotations

import argparse
import importlib.util
import math
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

from alghanem.arabic.classical_makharij_table import CLASSICAL_MAKHARIJ

REPOSITORY = Path(__file__).resolve().parents[2]
RASM = REPOSITORY / "examples" / "rasm"
BOOK_PART_THREE = "978eb9cc57064e7526ac720fd23593d08bf2012344009f7e1b74cacea1429136"
"""بصمةُ نصّ «الشخصية الإسلامية» ج٣ الذي رفعه صاحبُ المستودع (نصًّا مستخرَجًا)."""

MARKUP = "<sel>"
BASE28 = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
CARRIERS = "أإآءؤئى"
FATHA, DAMMA, KASRA, SUKUN, SHADDA = "َ", "ُ", "ِ", "ْ", "ّ"
TANWIN = "ًٌٍ"
STATES = (FATHA, DAMMA, KASRA, SUKUN)
STATE_NAMES = {FATHA: "فتحة", DAMMA: "ضمة", KASRA: "كسرة", SUKUN: "سكون"}
FOLDED_INTO = {"ا": "ا أ إ آ ء ؤ ئ ى", "ه": "ه ة"}

BYTES = "بايتات"
TREE = "اصطلاح الشجرة"
DEPOSITED = "مُودَع"
OWNER = "نصّ صاحب المستودع"
BOOK = "منقول من الكتاب"
UNCLASSIFIED = "UNCLASSIFIED"
SOURCES = (BYTES, TREE, DEPOSITED, OWNER, BOOK, UNCLASSIFIED)

LEVELS = (
    "ترميزي",
    "أبجدي: الترتيب",
    "أبجدي: القيمة",
    "إملائي",
    "صوتي: المخرج",
    "صوتي: الحال وتحقّقها",
    "صوتي: الصفة",
    "وظيفي: الجدول المُودَع",
    "وظيفي: نصّ صاحب المستودع",
    "اشتقاقي",
    "صرفي",
    "نحوي",
    "إعرابي",
    "المدلول وحده",
    "الدال والمدلول معًا",
)

CHANNELS = (
    "هويّة",
    "حامل",
    "مربوطة",
    "حالة",
    "سكون مكتوب",
    "شدّة",
    "تنوين",
    "بنية",
)

OWNER_BY_LETTER: dict[str, dict[str, str]] = {
    "ت": {
        FATHA: "التاء ضمير بالفتح للمخاطب",
        KASRA: "والتاء بالكسر للمخاطب المؤنث",
    },
    "ه": {state: "والهاء ضمير والتاء المربوطة" for state in STATES},
    "ي": {
        state: "والياء للنسبة … ومع الواو والياء والالف للجمع والمثنى"
        for state in STATES
    },
    "ك": {state: "والكاف. للملك لك كتابك" for state in STATES},
    "م": {
        SUKUN: "والميم مع سكون للجمع في نهاية اللواحق لكم لهم",
        FATHA: "والميم مع الفتح … سوابق بالمفعول والفاعل المزيد",
        DAMMA: "والميم مع الضم سوابق بالمفعول والفاعل المزيد",
    },
    "ا": {state: "والهمزة الوصل والاستفهام … والالف للجمع والمثنى" for state in STATES},
    "ل": {KASRA: "واللام مع كسرة للتعليل", FATHA: "لام مع فتح للأمر"},
    "س": {
        KASRA: "السين مع الكسر للمستقبل",
        SUKUN: "ومع السكون للطلب في الفعل المزيد",
    },
    "ن": {
        state: "والنون للتوكيد ونون النسوة ومع الواو والياء والالف للجمع"
        for state in STATES
    },
    "و": {state: "ومع الواو والياء والالف للجمع والمثنى" for state in STATES},
}
"""عباراتُ صاحب المستودع بحروفها مقسومةً على الحروف — والقسمةُ عملُ الآلة."""

MUHMAL = (
    "لفظٌ مفردٌ مهمل: لا مدلولَ له بالوضع؛ واسمُه (الضاد، الراء…) لفظٌ "
    "مدلولُه هذا المهمل — «فحروف ضرب وهي: ضه، وره، وبه، لم توضع لمعنى»"
)


def _load(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, RASM / f"{name}.py")
    if spec is None or spec.loader is None:
        raise RuntimeError(f"لا قارئَ لـ{name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@dataclass(frozen=True, slots=True)
class Cell:
    """خانةٌ في السجلّ: قيمتُها ومصدرُها، وما تحتاجه إن لم تُصنَّف."""

    value: str
    source: str
    need: str = ""

    @property
    def silent(self) -> bool:
        if self.source not in SOURCES:
            return True
        if self.source == UNCLASSIFIED:
            return not self.need.strip()
        return not self.value.strip()


def partition(text: str) -> tuple[Counter[str], int]:
    """كلُّ نقطةِ ترميزٍ إلى قناةٍ واحدة: (العدّ بالقناة، غيرُ المُسنَد)."""

    counts: Counter[str] = Counter()
    unassigned = 0
    index = 0
    while index < len(text):
        if text.startswith(MARKUP, index):
            counts["بنية"] += len(MARKUP)
            index += len(MARKUP)
            continue
        one = text[index]
        if one in BASE28:
            counts["هويّة"] += 1
        elif one in CARRIERS:
            counts["حامل"] += 1
        elif one == "ة":
            counts["مربوطة"] += 1
        elif one in (FATHA, DAMMA, KASRA):
            counts["حالة"] += 1
        elif one == SUKUN:
            counts["سكون مكتوب"] += 1
        elif one == SHADDA:
            counts["شدّة"] += 1
        elif one in TANWIN:
            counts["تنوين"] += 1
        elif one in " \n":
            counts["بنية"] += 1
        else:
            unassigned += 1
        index += 1
    return (counts, unassigned)


@dataclass(frozen=True, slots=True)
class Profile:
    """ما تقوله البايتاتُ عن وحدةٍ واحدة على المدوّنة."""

    total: int
    first: int
    middle: int
    last: int
    from_shadda: int
    tanwin: int
    written: int
    bare: int


def profiles(text: str) -> dict[tuple[str, str], Profile]:
    """كلُّ وحدةٍ من الـ١١٢: عددُها ومواضعُها ومن أين جاءت حالتُها."""

    peeler = _load("run_cv_peel")
    tally: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for line in text.split("\n"):
        for token in line.replace(MARKUP, " ").split():
            units, extras = peeler.peel(token)
            size = len(units)
            for place, (unit, extra) in enumerate(zip(units, extras, strict=True)):
                if unit[0] == peeler.STRUCTURE:
                    continue
                row = tally[unit]
                row["total"] += 1
                row[
                    "first" if place == 0 else "last" if place == size - 1 else "middle"
                ] += 1
                if extra.get("شدّة") == "نعم":
                    row["from_shadda"] += 1
                if "تنوين" in extra:
                    row["tanwin"] += 1
                if extra.get("سكون") == "مكتوب":
                    row["written"] += 1
                if extra.get("سكون") == "عارٍ":
                    row["bare"] += 1
    return {
        unit: Profile(
            total=row["total"],
            first=row["first"],
            middle=row["middle"],
            last=row["last"],
            from_shadda=row["from_shadda"],
            tanwin=row["tanwin"],
            written=row["written"],
            bare=row["bare"],
        )
        for unit, row in tally.items()
    }


def bare_realizations(text: str) -> dict[str, Counter[str]]:
    """أصنافُ العُري بالحرف، بترتيب الختم المصحَّح `34176d22…`."""

    depth = _load("run_surface_depth")
    letters, _ = depth.letters_of(text)
    kinds = depth.classify(letters, depth.REFINED)
    found: dict[str, Counter[str]] = defaultdict(Counter)
    for letter, kind in zip(letters, kinds, strict=True):
        if not kind:
            continue
        base = "ا" if letter.glyph in "اأإآءؤئى" else letter.glyph
        base = "ه" if base == "ة" else base
        name = depth.REFINED.names.get(kind, kind)
        found[base][name] += 1
    return found


def displaced_by_tanwin(text: str) -> Counter[str]:
    """حرفٌ عارٍ يليه «اً» في لفظه: حالتُه في التيّار سكون، وحركتُه على الألف."""

    depth = _load("run_surface_depth")
    letters, _ = depth.letters_of(text)
    found: Counter[str] = Counter()
    for index, letter in enumerate(letters):
        if not letter.bare:
            continue
        after = depth._same_token(letters, index, 1)
        if after is not None and after.glyph == "ا" and "ً" in after.marks:
            base = "ا" if letter.glyph in "اأإآءؤئى" else letter.glyph
            found["ه" if base == "ة" else base] += 1
    return found


def first_unit_census(text: str) -> tuple[int, list[str]]:
    """ج٤: كم لفظًا يبدأ بوحدةٍ ساكنةٍ غيرِ الألف وليست شطرَ شدّة — وأيُّها."""

    peeler = _load("run_cv_peel")
    tokens = 0
    offending: list[str] = []
    for line in text.split("\n"):
        for token in line.replace(MARKUP, " ").split():
            units, extras = peeler.peel(token)
            if not units:
                continue
            tokens += 1
            letter, state = units[0]
            if state != SUKUN or letter == "ا":
                continue
            if extras[0].get("شدّة") == "نعم":
                continue
            offending.append(token)
    return (tokens, offending)


def single_letter_tokens(text: str) -> tuple[list[str], list[str]]:
    """ج٥: ألفاظٌ من حرفٍ واحد — (ما عليه علامة، وما هو عارٍ)."""

    depth = _load("run_surface_depth")
    marked: list[str] = []
    bare: list[str] = []
    for line in text.split("\n"):
        for token in line.replace(MARKUP, " ").split():
            count = sum(1 for one in token if one in depth.LETTERS)
            if count != 1:
                continue
            (marked if any(one in depth.MARKS for one in token) else bare).append(token)
    return (marked, bare)


def _makhraj(letter: str) -> Cell:
    for rank, name, letters in CLASSICAL_MAKHARIJ:
        if letter in letters:
            note = ""
            if letter in "وي":
                note = "؛ ومدًّا: الجوف، خارجَ الترقيم في الجدول"
            return Cell(f"الرتبة {rank}: {name}{note}", DEPOSITED)
    if letter == "ا":
        return Cell(
            "الوحدةُ تجمع صوتين: الهمزةُ (ء) الرتبة ١: أقصى الحلق، والألفُ في "
            "الجوف خارجَ الترقيم — وقناةُ الحامل وحدَها تفرّق بينهما",
            DEPOSITED,
        )
    return Cell("", UNCLASSIFIED, "حرفٌ لا يرد في الجدول المُودَع")


def registry(
    text: str,
) -> tuple[dict[tuple[str, str], dict[str, Cell]], dict[tuple[str, str], Profile]]:
    """السجلّ: ١١٢ وحدةً × خمسةَ عشرَ مستوًى، ومعه ملفُّ كلّ وحدة."""

    roles = _load("run_letter_roles").table()
    found = profiles(text)
    realized = bare_realizations(text)
    displaced = displaced_by_tanwin(text)
    rows: dict[tuple[str, str], dict[str, Cell]] = {}
    bits = math.log2(len(BASE28) * len(STATES))
    for i, letter in enumerate(BASE28):
        for j, state in enumerate(STATES):
            unit = (letter, state)
            profile = found.get(unit, Profile(0, 0, 0, 0, 0, 0, 0, 0))
            name = STATE_NAMES[state]
            cells: dict[str, Cell] = {}
            cells["ترميزي"] = Cell(
                f"الوحدة {i * 4 + j + 1} من ١١٢ = الحرف {i + 1} × الحال {j + 1}؛ "
                f"{bits:.4f} بتًّا سقفًا؛ يُطوى إليها: "
                f"{FOLDED_INTO.get(letter, letter)}",
                TREE,
            )
            cells["أبجدي: الترتيب"] = Cell(
                f"الموضع {i + 1} في ترتيب BASE28 للشجرة", TREE
            )
            cells["أبجدي: القيمة"] = Cell(
                "",
                UNCLASSIFIED,
                "قيمُ حساب الجُمَّل تحتاج جدولًا مُودَعًا بمصدرٍ مسمّى؛ ولا تُكتَب " "من المحفوظ",
            )
            cells["إملائي"] = Cell(
                f"وقوعٌ {profile.total}؛ من شدّة {profile.from_shadda}؛ "
                f"من تنوين {profile.tanwin}; سكونٌ مكتوب {profile.written}؛ "
                f"عارٍ {profile.bare}",
                BYTES,
            )
            cells["صوتي: المخرج"] = _makhraj(letter)
            if state == SUKUN:
                parts = realized.get(letter, Counter())
                moved = displaced.get(letter, 0)
                cells["صوتي: الحال وتحقّقها"] = Cell(
                    "سكونٌ في التيّار؛ والعاري منه: "
                    + (
                        "، ".join(f"{k} {v}" for k, v in parts.most_common())
                        or "لا شيء"
                    )
                    + f"؛ وحركتُه على ألفٍ بعده {moved}",
                    BYTES,
                )
            else:
                cells["صوتي: الحال وتحقّقها"] = Cell(
                    f"{name} مكتوبة؛ ومنها من تنوين {profile.tanwin}", BYTES
                )
            cells["صوتي: الصفة"] = Cell(
                "",
                UNCLASSIFIED,
                "حاجزُ SIFA_TABLE_BYTES قائم: جدولُ صفاتٍ بطبعته وجزئه وصفحته",
            )
            if letter in "استهمونيل":
                spread = {
                    place: sorted(roles.get((letter, place, name), frozenset()))
                    for place in ("أوّل", "وسط", "آخر")
                }
                text_roles = " | ".join(
                    f"{place}: {'،'.join(value) or '—'}"
                    for place, value in spread.items()
                )
                cells["وظيفي: الجدول المُودَع"] = Cell(
                    f"{text_roles} (letter_roles_draft.tsv، غيرُ موقَّع)", DEPOSITED
                )
                union = set().union(*spread.values())
                cells["الدال والمدلول معًا"] = Cell(
                    (
                        "وحدةٌ واحدةٌ لأدوارٍ عدّة: " + "،".join(sorted(union))
                        if len(union) > 1
                        else "دورٌ واحد: " + "،".join(sorted(union))
                        if union
                        else "لا دورَ في الجدول"
                    ),
                    DEPOSITED,
                )
            else:
                cells["وظيفي: الجدول المُودَع"] = Cell(
                    "",
                    UNCLASSIFIED,
                    "الحرفُ خارجَ جدول الأدوار المُودَع (سألتمونيها)؛ والنبهاني "
                    "يعدّ الباء والفاء والكاف في حروف المعاني — ويحتاج جدولًا",
                )
                cells["الدال والمدلول معًا"] = Cell(
                    "", UNCLASSIFIED, "لا جدولَ أدوارٍ مُودَعٌ لهذا الحرف"
                )
            phrase = OWNER_BY_LETTER.get(letter, {}).get(state)
            cells["وظيفي: نصّ صاحب المستودع"] = Cell(
                phrase
                or (
                    "لم يذكر النصُّ هذا الحرفَ"
                    if letter not in OWNER_BY_LETTER
                    else "لم يذكر النصُّ هذه الحال لهذا الحرف"
                ),
                OWNER,
            )
            cells["اشتقاقي"] = Cell(
                "",
                UNCLASSIFIED,
                "جدولُ الجذور غيرُ مستقبَلٍ في هذه الشجرة (tools/intake_corpus.py)",
            )
            cells["صرفي"] = Cell("", UNCLASSIFIED, "جردُ أوزانٍ مُودَعٌ موقَّع")
            cells["نحوي"] = Cell(
                "",
                UNCLASSIFIED,
                "إسنادٌ موقَّعٌ بين لفظين — «التركيب الإسناديّ» في السلّم 426f7fc8…",
            )
            cells["إعرابي"] = Cell(
                "",
                UNCLASSIFIED,
                {
                    FATHA: "قسمةُ النحاة مُودَعة؛ والمرشَّح آخرَ اللفظ: نصبٌ أو بناء",
                    DAMMA: "قسمةُ النحاة مُودَعة؛ والمرشَّح آخرَ اللفظ: رفعٌ أو بناء",
                    KASRA: "قسمةُ النحاة مُودَعة؛ والمرشَّح آخرَ اللفظ: جرٌّ أو بناء",
                    SUKUN: "قسمةُ النحاة مُودَعة؛ والمرشَّح آخرَ اللفظ: جزمٌ أو بناءٌ "
                    "أو وقف",
                }[state],
            )
            cells["المدلول وحده"] = Cell(MUHMAL, BOOK)
            rows[unit] = cells
    return (rows, found)


def silent_cells(rows: dict[tuple[str, str], dict[str, Cell]]) -> int:
    """ج٣: خاناتٌ بلا قيمةٍ ولا سببٍ مكتوب، أو مستوًى غائب."""

    silent = 0
    for cells in rows.values():
        silent += sum(1 for level in LEVELS if level not in cells)
        silent += sum(1 for cell in cells.values() if cell.silent)
    return silent


def coverage(rows: dict[tuple[str, str], dict[str, Cell]]) -> dict[str, Counter[str]]:
    """لكلّ مستوًى: كم وحدةً من الـ١١٢ مصدرُها كذا."""

    found: dict[str, Counter[str]] = {level: Counter() for level in LEVELS}
    for cells in rows.values():
        for level, cell in cells.items():
            found[level][cell.source] += 1
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    raw = given.text.read_text(encoding="utf-8")
    counts, unassigned = partition(raw)
    print(f"نقاطُ الترميز: {len(raw)} | المُسنَد: {sum(counts.values())}")
    print(f"غيرُ المُسنَد: {unassigned}")
    for channel in CHANNELS:
        print(f"  {channel}: {counts[channel]}")

    text = raw.rstrip("\n")
    depth = _load("run_surface_depth")
    print(f"أسطرٌ لا تُعاد: {depth.unrebuilt_lines(text)}")

    rows, found = registry(text)
    print(f"الوحداتُ في السجلّ: {len(rows)} | المرصودة: {len(found)}")
    print(f"الخاناتُ: {len(rows) * len(LEVELS)} | الصامتة: {silent_cells(rows)}")
    for level, sources in coverage(rows).items():
        print(f"  {level}: {dict(sources)}")

    tokens, offending = first_unit_census(text)
    print(f"\nج٤: {len(offending)} من {tokens} | {Counter(offending).most_common(20)}")
    marked, bare = single_letter_tokens(text)
    print(f"ج٥: عليه علامة {len(marked)} | عارٍ {len(bare)} {Counter(bare)}")
    print(f"حركةٌ على ألفٍ بعدها: {sum(displaced_by_tanwin(text).values())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
