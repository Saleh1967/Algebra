"""السطحُ والعمقُ صعودًا من الـ١١٢ — تشغيلُ ختمَي `945fd806…` و`34176d22…`.

**ما يُقاس**: كلُّ حرفٍ عارٍ في المدوّنة — لم تتلُه علامة — يُعطى أوّلَ صنفٍ
يطابقه من أنماطٍ **معرَّفةٍ بالبايتات وحدها**، وما لم يطابق شيئًا **باقٍ
يُسمّى بصوره**. ويُقاس معه ما يلي النونَ والميمَ العاريتين ولامَ «ال».

**والختمان يُشغَّلان كلاهما**: الأوّلُ بترتيبه كما خُتِم — وعطلُه معلَنٌ قبل
العدّ في الثاني — والثاني بترتيبه المصحَّح. ولا يُبدَّل أحدُهما بالآخر.

**وما فوق الوحدة مسرودٌ لا مقيس**: الدعاوى التي قيلت في المحادثة على خمسة
عشر سطرًا **فوق الوحدة** تُسرَد في `ABOVE_THE_UNIT` ببابها — المستوى الذي
تقع فيه من السلّم المُقفَل `426f7fc8…`، وما تحتاجه لتُقاس. **ولا تُرقّى
دعوى منها بهذا التشغيل.**

**ولا اسمٌ لغويٌّ يدخل الحساب**: القراءاتُ (مدّ، وصل، إدغام) مذكورةٌ غيرَ
موقَّعة، والأصنافُ أنماطٌ وأعداد.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from types import ModuleType

REPOSITORY = Path(__file__).resolve().parents[2]
PEELER = REPOSITORY / "examples" / "rasm" / "run_cv_peel.py"

MARKUP = "<sel>"
BASE28 = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
ALIF_FAMILY = "اءأإآؤئى"
LETTERS = frozenset(BASE28 + ALIF_FAMILY + "ة")
FATHA, DAMMA, KASRA, SUKUN, SHADDA = "َ", "ُ", "ِ", "ْ", "ّ"
FATHATAN, DAMMATAN, KASRATAN = "ً", "ٌ", "ٍ"
VOWELS = frozenset((FATHA, DAMMA, KASRA, FATHATAN, DAMMATAN, KASRATAN))
MARKS = frozenset((*VOWELS, SUKUN, SHADDA))
THROAT = frozenset("ءأإآؤئهعحغخ")
PREFIXES = frozenset("وفبكلأ")
WINDOW = range(6_222, 6_237)
"""الأسطرُ ٦٢٢٢–٦٢٣٦ بترقيمٍ يبدأ من واحد — النافذةُ المرئيّةُ قبل الختم."""

RESIDUE = "باقٍ"


@dataclass(frozen=True, slots=True)
class Scheme:
    """ترتيبُ الأصناف وتعريفُ التالي كما خُتِما — لا يُخلَط ختمٌ بختم."""

    seal: str
    order: tuple[str, ...]
    names: dict[str, str]
    follower_crosses_markup: bool
    refined_wasl: bool


FIRST = Scheme(
    seal="945fd806",
    order=("س١", "س٢", "س٣", "س٤", "س٥", "س٦"),
    names={
        "س١": "مدّ",
        "س٢": "وصل",
        "س٣": "شمسيّة",
        "س٤": "ن/م",
        "س٥": "فارقة",
        "س٦": "آ",
    },
    follower_crosses_markup=True,
    refined_wasl=False,
)

REFINED = Scheme(
    seal="34176d22",
    order=("ق١", "ق٢", "ق٣", "ق٤", "ق٥", "ق٦"),
    names={
        "ق١": "وصل",
        "ق٢": "شمسيّة",
        "ق٣": "مدّ",
        "ق٤": "ن/م",
        "ق٥": "فارقة",
        "ق٦": "آ",
    },
    follower_crosses_markup=False,
    refined_wasl=True,
)


@dataclass(frozen=True, slots=True)
class Letter:
    """حرفٌ بعلاماته وموضعه — لا أكثر."""

    glyph: str
    marks: str
    line: int
    segment: int
    token: int
    position: int
    last: bool

    @property
    def bare(self) -> bool:
        return not self.marks

    @property
    def voiced(self) -> bool:
        return any(one in VOWELS for one in self.marks)

    @property
    def vowel(self) -> str:
        for one in reversed(self.marks):
            if one in VOWELS:
                return one
        return ""


def letters_of(text: str) -> tuple[list[Letter], list[str]]:
    """الحروفُ بترتيب القراءة، وما لم يُعرَف من الأحرف يُعَدّ ولا يُطوى."""

    found: list[Letter] = []
    strange: list[str] = []
    token_id = 0
    for number, raw in enumerate(text.split("\n"), start=1):
        for segment_id, segment in enumerate(raw.split(MARKUP)):
            for token in segment.split():
                token_id += 1
                built: list[tuple[str, str]] = []
                for character in token:
                    if character in LETTERS:
                        built.append((character, ""))
                    elif character in MARKS and built:
                        glyph, marks = built[-1]
                        built[-1] = (glyph, marks + character)
                    else:
                        strange.append(character)
                for place, (glyph, marks) in enumerate(built):
                    found.append(
                        Letter(
                            glyph=glyph,
                            marks=marks,
                            line=number,
                            segment=segment_id,
                            token=token_id,
                            position=place,
                            last=place == len(built) - 1,
                        )
                    )
    return (found, strange)


def _same_token(letters: list[Letter], index: int, step: int) -> Letter | None:
    other = index + step
    if 0 <= other < len(letters) and letters[other].token == letters[index].token:
        return letters[other]
    return None


def follower(letters: list[Letter], index: int, scheme: Scheme) -> Letter | None:
    """أوّلُ حرفٍ بعده في السطر؛ ولا يعبر الوسمَ إلّا إن أذن الختم."""

    if index + 1 >= len(letters):
        return None
    one, two = letters[index], letters[index + 1]
    if two.line != one.line:
        return None
    if not scheme.follower_crosses_markup and two.segment != one.segment:
        return None
    return two


def _madd(letter: Letter, before: Letter | None) -> bool:
    vowel = before.vowel if before is not None else ""
    if letter.glyph in "اى":
        return vowel in (FATHA, FATHATAN)
    if letter.glyph == "و":
        return vowel in (DAMMA, DAMMATAN)
    if letter.glyph == "ي":
        return vowel in (KASRA, KASRATAN)
    return False


def _wasl(
    letters: list[Letter], index: int, before: Letter | None, scheme: Scheme
) -> bool:
    letter = letters[index]
    if letter.glyph != "ا":
        return False
    if letter.position == 0:
        return True
    if not scheme.refined_wasl:
        return letter.position == 1 and before is not None and before.voiced
    if letter.position > 2:
        return False
    for step in range(1, letter.position + 1):
        earlier = letters[index - step]
        if earlier.glyph not in PREFIXES or not earlier.voiced:
            return False
    after = _same_token(letters, index, 1)
    if after is None:
        return False
    return after.bare or SUKUN in after.marks or SHADDA in after.marks


def classify(letters: list[Letter], scheme: Scheme) -> list[str]:
    """صنفُ كلّ حرفٍ عارٍ، وسلسلةٌ فارغةٌ لما عليه علامة."""

    wasl_name = next(key for key, name in scheme.names.items() if name == "وصل")
    kinds: list[str] = []
    for index, letter in enumerate(letters):
        if not letter.bare:
            kinds.append("")
            continue
        before = _same_token(letters, index, -1)
        after = _same_token(letters, index, 1)
        chosen = RESIDUE
        for key in scheme.order:
            name = scheme.names[key]
            if name == "مدّ":
                hit = _madd(letter, before)
            elif name == "وصل":
                hit = _wasl(letters, index, before, scheme)
            elif name == "شمسيّة":
                hit = (
                    letter.glyph == "ل"
                    and before is not None
                    and kinds[index - 1] == wasl_name
                    and after is not None
                    and SHADDA in after.marks
                )
            elif name == "ن/م":
                hit = letter.glyph in "نم"
            elif name == "فارقة":
                hit = (
                    letter.glyph == "ا"
                    and letter.last
                    and before is not None
                    and before.glyph == "و"
                    and not before.voiced
                )
            else:
                hit = letter.glyph == "آ"
            if hit:
                chosen = key
                break
        kinds.append(chosen)
    return kinds


@dataclass(frozen=True, slots=True)
class Ratio:
    """بسطٌ ومقامٌ صحيحان — والنصيبُ كسرٌ لا عشريّ."""

    hits: int
    base: int

    @property
    def share(self) -> Fraction:
        return Fraction(self.hits, self.base) if self.base else Fraction(0)


@dataclass(frozen=True, slots=True)
class Reading:
    """ما يُحكَم به على شروط الختم، وما يُسرَد معه."""

    scheme: str
    lines: int
    unrebuilt: int
    bare: int
    classes: dict[str, int]
    residue: int
    closure_gap: int
    nun_throat: Ratio
    nun_without_follower: int
    mim_other: Ratio
    mim_without_follower: int
    lam_not_before_shadda: Ratio
    lam_marked_before_shadda: Ratio
    residue_letters: list[tuple[str, int]]
    residue_tokens: list[tuple[str, int]]
    mim_followers: list[tuple[str, int]]
    lam_misses: list[tuple[str, int]]


def _token_text(letters: list[Letter], token: int) -> str:
    return "".join(one.glyph + one.marks for one in letters if one.token == token)


def _peeler() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_cv_peel", PEELER)
    if spec is None or spec.loader is None:
        raise RuntimeError("لا قارئَ للتقشير")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def unrebuilt_lines(text: str) -> int:
    """أسطرٌ لا يعيدها التقشيرُ بايتةً بايتة (بعد طرح الوسم فراغًا)."""

    peeler = _peeler()
    missed = 0
    for raw in text.split("\n"):
        line = raw.replace(MARKUP, " ")
        units, extras = peeler.peel(line)
        if peeler.rebuild(units, extras) != line:
            missed += 1
    return missed


def read(text: str, scheme: Scheme, unrebuilt: int) -> Reading:
    letters, strange = letters_of(text)
    if strange:
        raise ValueError(f"أحرفٌ لا يعرفها التعريف: {Counter(strange)}")
    kinds = classify(letters, scheme)
    bare = sum(1 for one in letters if one.bare)
    classes = Counter(kind for kind in kinds if kind and kind != RESIDUE)
    residue = sum(1 for kind in kinds if kind == RESIDUE)
    gap = abs(sum(classes.values()) + residue - bare)

    nun_hits = nun_base = nun_none = 0
    mim_hits = mim_base = mim_none = 0
    mim_seen: Counter[str] = Counter()
    for index, letter in enumerate(letters):
        if not letter.bare or letter.glyph not in "نم":
            continue
        after = follower(letters, index, scheme)
        if letter.glyph == "ن":
            if after is None:
                nun_none += 1
                continue
            nun_base += 1
            nun_hits += after.glyph in THROAT
        else:
            if after is None:
                mim_none += 1
                continue
            mim_base += 1
            mim_seen[after.glyph] += 1
            mim_hits += after.glyph not in "بم"

    wasl_name = next(key for key, name in scheme.names.items() if name == "وصل")
    lam_bare = lam_bare_miss = lam_shadda = lam_shadda_marked = 0
    misses: Counter[str] = Counter()
    for index, letter in enumerate(letters):
        if letter.glyph != "ل" or index == 0:
            continue
        before = _same_token(letters, index, -1)
        if before is None or kinds[index - 1] != wasl_name:
            continue
        after = _same_token(letters, index, 1)
        doubled = after is not None and SHADDA in after.marks
        if letter.bare:
            lam_bare += 1
            if not doubled:
                lam_bare_miss += 1
                misses[_token_text(letters, letter.token)] += 1
        if doubled:
            lam_shadda += 1
            lam_shadda_marked += not letter.bare

    residue_letters = Counter(
        letters[index].glyph for index, kind in enumerate(kinds) if kind == RESIDUE
    )
    residue_tokens = Counter(
        _token_text(letters, letters[index].token)
        for index, kind in enumerate(kinds)
        if kind == RESIDUE
    )
    return Reading(
        scheme=scheme.seal,
        lines=text.count("\n") + (0 if text.endswith("\n") else 1),
        unrebuilt=unrebuilt,
        bare=bare,
        classes={key: classes[key] for key in scheme.order},
        residue=residue,
        closure_gap=gap,
        nun_throat=Ratio(nun_hits, nun_base),
        nun_without_follower=nun_none,
        mim_other=Ratio(mim_hits, mim_base),
        mim_without_follower=mim_none,
        lam_not_before_shadda=Ratio(lam_bare_miss, lam_bare),
        lam_marked_before_shadda=Ratio(lam_shadda_marked, lam_shadda),
        residue_letters=residue_letters.most_common(12),
        residue_tokens=residue_tokens.most_common(15),
        mim_followers=mim_seen.most_common(8),
        lam_misses=misses.most_common(10),
    )


def window_census(text: str, scheme: Scheme) -> tuple[int, int, dict[str, int]]:
    """(الحروف، العاري، الأصناف) في النافذة المرئيّة — شاهدٌ لا حكم."""

    lines = text.split("\n")
    chosen = "\n".join(lines[number - 1] for number in WINDOW)
    letters, _ = letters_of(chosen)
    kinds = classify(letters, scheme)
    census = Counter(kind for kind in kinds if kind)
    return (len(letters), sum(1 for one in letters if one.bare), dict(census))


ABOVE_THE_UNIT: tuple[tuple[str, str, str], ...] = (
    (
        "أنّ علامةَ آخر اللفظ إعرابٌ في ٣٥ من ٥٨ وبناءٌ في ٢٣ (النافذة)",
        "الكلمةُ المفردة — UNCLASSIFIED",
        "جردٌ مُودَعٌ موقَّعٌ للمبنيّات والمعربات؛ والعدُّ في المحادثة كان "
        "يدويًّا على قواعد نحوٍ لم تُودَع",
    ),
    (
        "أنّ «أَحَدٌ» في الإثبات وصفٌ وفي النفي «أيُّ أحد»",
        "التركيبُ الإسناديّ — UNCLASSIFIED",
        "إيداعٌ موقَّعٌ لأدوات النفي ونطاقها؛ والبايتاتُ تشهد بتطابق "
        "اللفظين فقط، لا باختلاف ما تحتهما",
    ),
    (
        "أنّ «كُفُواً» خبرٌ مقدَّم و«أَحَدٌ» اسمٌ مؤخَّر",
        "التركيبُ الإسناديّ — UNCLASSIFIED",
        "إسنادٌ موقَّعٌ بين لفظين؛ والبايتاتُ تشهد بتنوين الفتح هنا وتنوين "
        "الضمّ هناك، والدورُ قراءةٌ لا مقيس",
    ),
    (
        "أنّ «يَلِدْ» للمعلوم و«يُولَدْ» للمجهول",
        "الكلمةُ المفردة — UNCLASSIFIED",
        "جردٌ مُودَعٌ للأوزان؛ والبايتاتُ تشهد باختلاف الوحدات وحضور الواو "
        "في الثانية وحدَها",
    ),
    (
        "أنّ «مَا» في «مَا خَلَقَ» موصولةٌ عامّة",
        "التركيبُ الإسناديّ — UNCLASSIFIED",
        "تمييزٌ مُودَعٌ للموصولة من غيرها، ونصُّ الأصول المستشهَد به مُودَعًا",
    ),
    (
        "أنّ «مِنَ الْجِنَّةِ وَالنَّاسِ» بيانٌ للوسواس",
        "الجملة — UNCLASSIFIED",
        "وقفٌ مُودَعٌ وحدٌّ للجملة؛ والسطرُ ليس جملة",
    ),
    (
        "أنّ «الوَسْوَاس» بالفتح اسمٌ لا مصدر",
        "الكلمةُ المفردة — UNCLASSIFIED",
        "نقلٌ معجميٌّ موقَّعٌ عن اللغويّين؛ ولا يُشتَقّ من الشكل",
    ),
    (
        "أنّ جذرَ «النَّاس» مختلَفٌ فيه",
        "الكلمةُ المفردة — UNCLASSIFIED",
        "جدولُ جذورٍ مُودَع؛ والخلافُ نفسُه نقلٌ لا يحسمه جدولٌ واحد",
    ),
)
"""دعاوى المحادثة **فوق الوحدة**: الدعوى، ومستواها من السلّم، وما تحتاجه."""


def _show(reading: Reading, scheme: Scheme) -> None:
    print(f"\n== الختم {reading.scheme}… ==")
    print(f"الأسطر: {reading.lines} | لا تُعاد بايتةً بايتة: {reading.unrebuilt}")
    print(f"العُري: {reading.bare}")
    for key, count in reading.classes.items():
        print(f"  {key} ({scheme.names[key]}): {count} | {count / reading.bare:.4f}")
    print(f"  {RESIDUE}: {reading.residue} | {reading.residue / reading.bare:.4f}")
    print(f"  فجوةُ الانغلاق: {reading.closure_gap}")
    for name, ratio in (
        ("ن عاريةٌ قبل حرف حلق", reading.nun_throat),
        ("م عاريةٌ قبل غير ب/م", reading.mim_other),
        ("ل «ال» عاريةٌ قبل غير مشدّد", reading.lam_not_before_shadda),
        ("ل «ال» قبل مشدّد وعليها علامة", reading.lam_marked_before_shadda),
    ):
        print(f"{name}: {ratio.hits}/{ratio.base} = {float(ratio.share):.4f}")
    print(f"ن بلا تالٍ: {reading.nun_without_follower}")
    print(f"م بلا تالٍ: {reading.mim_without_follower}")
    print(f"توالي الميم العارية: {reading.mim_followers}")
    print(f"الباقي بالحرف: {reading.residue_letters}")
    print(f"الباقي بالألفاظ: {reading.residue_tokens}")
    print(f"لامٌ لم تُدغَم: {reading.lam_misses}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    text = given.text.read_text(encoding="utf-8").rstrip("\n")
    unrebuilt = unrebuilt_lines(text)
    for scheme in (FIRST, REFINED):
        _show(read(text, scheme, unrebuilt), scheme)
        total, bare, census = window_census(text, scheme)
        print(f"النافذة ٦٢٢٢–٦٢٣٦: حروف {total} | عارٍ {bare} | {census}")
    print("\n== فوق الوحدة — مسرودٌ لا مقيس ==")
    for claim, level, need in ABOVE_THE_UNIT:
        print(f"- {claim}\n  المستوى: {level}\n  يحتاج: {need}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
