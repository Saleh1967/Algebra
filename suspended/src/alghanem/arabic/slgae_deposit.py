"""إيداعُ وثيقة SLGAE نصًّا مُبصَّمًا، وقياسُ ما تفعله صفاتُها المولودة بالخانات.

**ما تفعله هذه الوحدة**: تُثبِّت بايتاتِ وثيقةٍ وصلت من خارج الشجرة بتاريخ
22 Sept 2026 منسوبةً إلى `@saleh`، وتُسجّل قسمتَها المولودة وصفاتِها، ثمّ
**تُشغّل** تلك الصفاتِ على خانات المخرج المُجمَّدة فتقول بالعدد كم حرفًا
تحسم وكم يبقى. لا أكثر، وعلى منوال `gflk_specification_deposit`.

`THE_DEPOSIT_IS_NOT_AN_ADOPTION`: إيداعُ نصٍّ ليس تصديقًا لرقمٍ فيه ولا
لتصنيف. وأرقامُ الوثيقة الأخرى — الإعلالُ والقوالبُ والحوافُ والأوزان —
مُودَعةٌ بنصّها **غيرَ مُعادةِ الاشتقاق هنا**، ومساراتُ قياسها ليست هذا
الملفّ.

`THE_BORN_TABLE_IS_NOT_AN_IMPORTED_TABLE`: حاجزُ جدول الصفة في
`gflk_feature_table_import_barrier` قام على جدولٍ **مستورَدٍ** بلا مصدرٍ ولا
بصمة. وما في هذه الوثيقة مختلفٌ في جنسه: قسمةٌ وصفاتٌ **مولودةٌ من تجنُّب
الحروف في الجذور** بمدوّنةٍ مسمّاة. فلا هذه الوحدةُ ترفع ذلك الحاجزَ ولا
تلتفّ عليه: هي تُودِع مصدرًا مسمًّى مُبصَّمًا وتقيس أثرَه، ورفعُ الحاجز أو
إبقاؤه قرارٌ في وحدته لا هنا.

`THE_INVENTORY_CONFLICT_IS_STRUCTURAL_NOT_INCIDENTAL`: الوثيقةُ تعدّ الصوامتَ
**ستّةً وعشرين** وتُخرِج الواوَ والياء؛ والجدولُ المُجمَّد يُرقّم **ثمانيةً
وعشرين** وفيهنّ الواوُ والياء. فالفرقُ حرفان بأعيانهما، وهو يُشتَقّ هنا
بالطرح لا يُكتَب. وأثرُه مقيسٌ لا موصوف: خانةٌ فيها حرفٌ خارجَ المفردة
المولودة **لا تُحسَم ولا تبقى متعادلةً**، بل تخرج ثالثةً `UNDECIDED`.

`AN_ABSENT_ROW_IS_NOT_A_DISTINGUISHING_FEATURE`: ولا يُعَدُّ غيابُ الصفّ عن
حرفٍ صفةً تفصله عن أقرانه. فحرفٌ بلا صفاتٍ يُفرَد بذلك انفرادًا سببُه غيابُ
البيان لا اختلافُ الصفة، وهو أشدُّ من التعادل خطرًا لأنّه يُخرِج حسمًا من
فراغ.

`THE_THIRD_DIVISION_IS_REGISTERED_NOT_MERGED`: صارت في الشجرة ثلاثةُ أعدادٍ
لقسمةٍ واحدة: **خمسُ** كتلٍ مولودةٍ هنا، و**ستّةَ عشرَ** مخرجًا مُجمَّدًا،
و**ثلاثَ عشرةَ** فئةً في المواصفة. ولا تُدمَج، على ما قرّره
`THE_CONFLICT_IS_RESOLVED_BEFORE_THE_IMPORT_NOT_AFTER`.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا بالمعنى الكرنليّ، ولا
حكمَ ولادة، ولا تجميدَ `E0`، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Final

from alghanem.canonical_content import canonical_digest

from .classical_makharij_table import CLASSICAL_MAKHARIJ, CLASSICAL_ORDINAL
from .gflk_feature_table_import_barrier import frozen_makhraj_count
from .makhraj_bit_decoder import MAKHRAJ_LETTERS, MAKHRAJ_NAMES
from .makhraj_bit_decoder import census as makhraj_census

__all__ = [
    "AN_ABSENT_ROW_IS_NOT_A_FEATURE_NOTE",
    "BORN_BLOCKS",
    "BORN_BLOCK_COUNT",
    "BORN_SIFA_SPLITS",
    "SLGAE_ATTRIBUTION",
    "SLGAE_NAMED_RESIDUALS",
    "SLGAE_RELATIVE_PATH",
    "SPECIFICATION_CATEGORY_COUNT",
    "THE_BORN_TABLE_IS_NOT_AN_IMPORTED_TABLE_NOTE",
    "THE_DEPOSIT_IS_NOT_AN_ADOPTION_NOTE",
    "THE_INVENTORY_CONFLICT_IS_STRUCTURAL_NOTE",
    "THE_THIRD_DIVISION_IS_REGISTERED_NOT_MERGED_NOTE",
    "UNREDERIVED_SECTIONS",
    "BornSifaSplit",
    "ClassOutcome",
    "ClassReading",
    "DivisionConflict",
    "InventoryConflict",
    "SlgaeDepositError",
    "SlgaeSeparationReading",
    "born_inventory",
    "derive_class_readings",
    "derive_division_conflict",
    "derive_inventory_conflict",
    "features_of",
    "separation_reading",
    "slgae_digest",
    "slgae_path",
    "read_slgae_bytes",
]

SLGAE_RELATIVE_PATH: Final[str] = "docs/reference/slgae_slot_licensing_algebra.md"

SLGAE_ATTRIBUTION: Final[str] = (
    "SLGAE — جبر ترخيص الخانات، 22 Sept 2026، منسوبةً إلى @saleh؛ وصلت إلى "
    "هذه الشجرة من خارجها، وليست دعوى هذه الشجرة"
)

SPECIFICATION_CATEGORY_COUNT: Final[int] = 13
"""عددُ فئات المخرج في مواصفة GFLK، مذكورًا هنا للمقابلة لا للدمج."""


class SlgaeDepositError(ValueError):
    """رُفض مدخلٌ خارج شرطه؛ ولا يُحمَل على أقرب حالةٍ مقبولة."""


@dataclass(frozen=True, slots=True)
class BornSifaSplit:
    """صفةٌ مولودةٌ داخل كتلةٍ واحدة: شقّان، أو لا شيءَ إن لم تولد."""

    block: str
    side_a: str
    side_b: str

    def __post_init__(self) -> None:
        if not self.block.strip():
            raise SlgaeDepositError("قسمةٌ بلا اسم كتلةٍ لا تُنسَب إلى موضعها.")
        if set(self.side_a) & set(self.side_b):
            raise SlgaeDepositError(
                f"حرفٌ في شقَّي الصفة معًا في كتلة {self.block}؛ "
                "وشقّان متداخلان لا يفصلان."
            )
        if not self.side_a or not self.side_b:
            raise SlgaeDepositError(
                f"شقٌّ فارغٌ في كتلة {self.block}؛ وصفةٌ بشقٍّ واحدٍ لا تفصل، "
                "وغيابُ الصفة يُسجَّل بتركها خارج هذه المجموعة."
            )


BORN_BLOCKS: Final[tuple[tuple[str, str], ...]] = (
    ("حلقية", "عحهخغء"),
    ("كقج", "كقج"),
    ("أسنانية", "ظثصضطسزتذشد"),
    ("شفوية", "فبم"),
    ("نلر", "نلر"),
)
"""الكتلُ الخمسُ المولودة، بحروفها كما وردت في الوثيقة نصًّا."""

BORN_BLOCK_COUNT: Final[int] = len(BORN_BLOCKS)

BORN_SIFA_SPLITS: Final[tuple[BornSifaSplit, ...]] = (
    BornSifaSplit(block="حلقية", side_a="عغء", side_b="حهخ"),
    BornSifaSplit(block="أسنانية", side_a="تدط", side_b="ظثصضسزذش"),
    BornSifaSplit(block="شفوية", side_a="م", side_b="فب"),
    BornSifaSplit(block="نلر", side_a="ن", side_b="لر"),
)
"""الصفاتُ المولودة. وكتلةُ «كقج» ليست هنا: الوثيقةُ تقول لم تولد فيها صفة."""

UNREDERIVED_SECTIONS: Final[tuple[str, ...]] = (
    "٢ — المقياس والعتبة (أوزان شابلي، θ = 15.65)",
    "٣ — قوانين الترخيص الخمسة",
    "٤ — الإعلال مشغّلًا على الخانة (9,239 خانة)",
    "٥ب — قانون الحواف (EDGE-LAW-AR-1)",
    "٥ج — الفراكتالية (FRACTAL-JOINT-AR-1)",
    "٥د — ولادة CV-112 في أربع قنوات",
    "٥هـ — ولادة القوالب بالتتابع وإعادة التدوير",
    "٥و — الجذر والوزن (ROOT-WAZN-BIRTH-AR-1)",
    "٥ز — المبني للمجهول والمصدر",
    "٥ح — شبكة الخانات",
    "٥ط — المقولات النحوية عوامل حواف",
)
"""أبوابُ الوثيقة المُودَعةُ نصًّا وغيرُ المُعادةِ الاشتقاق في هذه الوحدة."""


def slgae_path(root: Path | None = None) -> Path:
    """مسارُ الوثيقة المُودَعة، مبنيًّا من جذر الشجرة لا مكتوبًا مطلقًا."""

    base = root if root is not None else Path(__file__).resolve().parents[3]
    return base / SLGAE_RELATIVE_PATH


def read_slgae_bytes(root: Path | None = None) -> bytes:
    """اقرأ بايتاتِ الوثيقة كما هي؛ ولا تطبيعَ هنا قصدًا.

    والسببُ هو المكتوبُ في `classical_table_bytes`: تطبيعُنا إيّاها يجعل
    البصمةَ بصمةَ نصٍّ آخرَ ثمّ يُسمّى الاختلافُ تطابقًا.
    """

    path = slgae_path(root)
    if not path.is_file():
        raise SlgaeDepositError(
            f"وثيقةٌ مُودَعةٌ غيرُ موجودةٍ في موضعها: {SLGAE_RELATIVE_PATH}؛ "
            "وبصمةٌ بلا بايتاتٍ بصمةٌ لا تُفحَص."
        )
    return path.read_bytes()


def slgae_digest(root: Path | None = None) -> str:
    """بصمةُ الوثيقة، مُشتَقّةً من بايتاتها الآن لا من رقمٍ مكتوبٍ في حقل."""

    return canonical_digest(read_slgae_bytes(root))


def born_inventory() -> frozenset[str]:
    """مفردةُ الصوامت المولودة، مجموعةً من الكتل لا مكتوبةً عددًا."""

    letters: set[str] = set()
    for block, chars in BORN_BLOCKS:
        for letter in chars:
            if letter in letters:
                raise SlgaeDepositError(
                    f"حرفٌ في كتلتَين: {letter} عند {block}؛ "
                    "وكتلتان لحرفٍ واحدٍ تخلطان قسمتَين."
                )
            letters.add(letter)
    return frozenset(letters)


def features_of(letter: str) -> tuple[str, ...] | None:
    """صفاتُ حرفٍ في القسمة المولودة: كتلتُه ثمّ شقُّ صفته إن وُلدت.

    وتُرجِع `None` لحرفٍ خارجَ المفردة المولودة، ولا تُرجِع مجموعةً فارغةً:
    الفارغةُ تُساوي الفارغةَ فتفصل بلا بيان، و`None` تُوقِف الحسم.
    """

    for block, chars in BORN_BLOCKS:
        if letter not in chars:
            continue
        features = [f"كتلة:{block}"]
        for split in BORN_SIFA_SPLITS:
            if split.block != block:
                continue
            side = "أ" if letter in split.side_a else "ب"
            features.append(f"صفة:{block}:{side}")
        return tuple(features)
    return None


@dataclass(frozen=True, slots=True)
class InventoryConflict:
    """فرقُ المفردتين، مُشتَقًّا بالطرح لا مكتوبًا."""

    born_letters: int
    frozen_letters: int
    only_in_frozen: tuple[str, ...]
    only_in_born: tuple[str, ...]


def derive_inventory_conflict() -> InventoryConflict:
    """قابِلْ مفردةَ الوثيقة بمفردة الجدول المُجمَّد حرفًا بحرف."""

    born = born_inventory()
    frozen = frozenset(CLASSICAL_ORDINAL)
    return InventoryConflict(
        born_letters=len(born),
        frozen_letters=len(frozen),
        only_in_frozen=tuple(sorted(frozen - born)),
        only_in_born=tuple(sorted(born - frozen)),
    )


@dataclass(frozen=True, slots=True)
class DivisionConflict:
    """ثلاثةُ أعدادٍ لقسمةٍ واحدة، مُسجَّلةً معًا ولا تُدمَج."""

    born_blocks: int
    frozen_makharij: int
    specification_categories: int

    def __post_init__(self) -> None:
        if len({self.born_blocks, self.frozen_makharij}) == 1:
            raise SlgaeDepositError(
                "لا يُسجَّل تعارضٌ حيث لا تعارض؛ وصفٌّ بلا فرقٍ يُقرأ خلافًا لم يقع."
            )


def derive_division_conflict() -> DivisionConflict:
    """اقرأ الأعدادَ الثلاثةَ من مواضعها، ولا تكتب واحدًا منها هنا."""

    return DivisionConflict(
        born_blocks=BORN_BLOCK_COUNT,
        frozen_makharij=frozen_makhraj_count(),
        specification_categories=SPECIFICATION_CATEGORY_COUNT,
    )


class ClassOutcome(Enum):
    """ما فعلته الصفاتُ المولودة بخانةٍ مُجمَّدةٍ فيها أكثرُ من حرف."""

    RESOLVED = "محسومة: كلُّ حرفٍ انفرد بمجموعة صفاته"
    TIED = "متعادلة: حرفان فأكثر اتّفقت مجموعتاهما"
    UNDECIDED = "موقوفة: فيها حرفٌ خارج المفردة المولودة"


@dataclass(frozen=True, slots=True)
class ClassReading:
    """قراءةُ خانةٍ واحدة: حروفُها، وما انفرد، وما تعادل، وما وقف."""

    makhraj_rank: int
    makhraj_name: str
    letters: tuple[str, ...]
    outcome: ClassOutcome
    separated_letters: tuple[str, ...]
    tied_groups: tuple[tuple[str, ...], ...]
    letters_outside_born: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.outcome is ClassOutcome.UNDECIDED and not self.letters_outside_born:
            raise SlgaeDepositError(
                "خانةٌ موقوفةٌ بلا حرفٍ خارج المفردة؛ والوقفُ بلا سببه حسمٌ مؤجَّل."
            )
        if self.outcome is not ClassOutcome.UNDECIDED and self.letters_outside_born:
            raise SlgaeDepositError(
                "خانةٌ فيها حرفٌ خارج المفردة وقد حُسِمت؛ وحسمُها يُفرِد حرفًا "
                "بغياب بيانه لا باختلاف صفته."
            )


def derive_class_readings() -> tuple[ClassReading, ...]:
    """شغِّل الصفاتِ المولودةَ على الخانات التي فيها أكثرُ من حرف."""

    readings: list[ClassReading] = []
    for rank in sorted(MAKHRAJ_LETTERS):
        letters = MAKHRAJ_LETTERS[rank]
        if len(letters) == 1:
            continue
        outside = tuple(letter for letter in letters if features_of(letter) is None)
        if outside:
            readings.append(
                ClassReading(
                    makhraj_rank=rank,
                    makhraj_name=MAKHRAJ_NAMES[rank],
                    letters=letters,
                    outcome=ClassOutcome.UNDECIDED,
                    separated_letters=(),
                    tied_groups=(),
                    letters_outside_born=outside,
                )
            )
            continue
        cells: dict[tuple[str, ...], list[str]] = {}
        for letter in letters:
            features = features_of(letter)
            if features is None:  # pragma: no cover - حارس
                raise SlgaeDepositError("حرفٌ بلا صفاتٍ بعد فحص الخروج.")
            cells.setdefault(features, []).append(letter)
        separated = tuple(cell[0] for cell in cells.values() if len(cell) == 1)
        tied = tuple(tuple(cell) for cell in cells.values() if len(cell) > 1)
        readings.append(
            ClassReading(
                makhraj_rank=rank,
                makhraj_name=MAKHRAJ_NAMES[rank],
                letters=letters,
                outcome=ClassOutcome.TIED if tied else ClassOutcome.RESOLVED,
                separated_letters=separated,
                tied_groups=tied,
                letters_outside_born=(),
            )
        )
    return tuple(readings)


@dataclass(frozen=True, slots=True)
class SlgaeSeparationReading:
    """حصادُ التشغيل على الخانات كلِّها، والحروفُ الثلاثُ موزّعةٌ بلا بقيّة."""

    letters_unresolved_before: int
    resolved_letters: int
    tied_letters: int
    undecided_letters: int
    resolved_classes: int
    tied_classes: int
    undecided_classes: int
    document_digest: str

    def __post_init__(self) -> None:
        total = self.resolved_letters + self.tied_letters + self.undecided_letters
        if total != self.letters_unresolved_before:
            raise SlgaeDepositError(
                f"مجموعُ المحسوم والمتعادل والموقوف {total} والمعلَّقُ قبلُ "
                f"{self.letters_unresolved_before}؛ وحرفٌ يُعَدُّ مرّتين أو لا "
                "يُعَدُّ يُفسِد الحصاد."
            )


def separation_reading(root: Path | None = None) -> SlgaeSeparationReading:
    """أخرِج الحصادَ بالعدد: كم حُسِم، وكم تعادل، وكم وقف، وببصمة الوثيقة."""

    readings = derive_class_readings()
    resolved = tuple(r for r in readings if r.outcome is ClassOutcome.RESOLVED)
    tied = tuple(r for r in readings if r.outcome is ClassOutcome.TIED)
    undecided = tuple(r for r in readings if r.outcome is ClassOutcome.UNDECIDED)
    return SlgaeSeparationReading(
        letters_unresolved_before=makhraj_census().letters_in_underdetermined_patterns,
        resolved_letters=sum(len(r.letters) for r in resolved)
        + sum(len(r.separated_letters) for r in tied),
        tied_letters=sum(len(group) for r in tied for group in r.tied_groups),
        undecided_letters=sum(len(r.letters) for r in undecided),
        resolved_classes=len(resolved),
        tied_classes=len(tied),
        undecided_classes=len(undecided),
        document_digest=slgae_digest(root),
    )


THE_DEPOSIT_IS_NOT_AN_ADOPTION_NOTE: Final[str] = (
    "TheDepositIsNotAnAdoption: إيداعُ نصٍّ ليس تصديقًا لرقمٍ فيه ولا لتصنيف؛ "
    "وأبوابُ الوثيقة الأخرى مُودَعةٌ نصًّا غيرَ مُعادةِ الاشتقاق هنا"
)

THE_BORN_TABLE_IS_NOT_AN_IMPORTED_TABLE_NOTE: Final[str] = (
    "TheBornTableIsNotAnImportedTable: حاجزُ جدول الصفة قام على جدولٍ مستورَدٍ "
    "بلا مصدرٍ ولا بصمة، وما هنا قسمةٌ مولودةٌ من الجذور بمدوّنةٍ مسمّاة؛ فلا "
    "تُرفَع بها الحاجزُ ولا يُلتَفّ عليه، والقرارُ في وحدته"
)

THE_INVENTORY_CONFLICT_IS_STRUCTURAL_NOTE: Final[str] = (
    "TheInventoryConflictIsStructuralNotIncidental: الوثيقةُ تعدّ الصوامتَ "
    "ستًّا وعشرين والجدولُ يُرقّم ثمانيًا وعشرين؛ والفرقُ يُشتَقّ بالطرح، "
    "وأثرُه خانةٌ تخرج موقوفةً لا محسومةً ولا متعادلة"
)

AN_ABSENT_ROW_IS_NOT_A_FEATURE_NOTE: Final[str] = (
    "AnAbsentRowIsNotADistinguishingFeature: غيابُ الصفّ عن حرفٍ لا يُعَدُّ "
    "صفةً تفصله؛ وإفرادُه بغياب بيانه يُخرِج حسمًا من فراغ، وهو أشدُّ من "
    "التعادل خطرًا"
)

THE_THIRD_DIVISION_IS_REGISTERED_NOT_MERGED_NOTE: Final[str] = (
    "TheThirdDivisionIsRegisteredNotMerged: صارت ثلاثةُ أعدادٍ لقسمةٍ واحدة — "
    "خمسُ كتلٍ مولودة، وستّةَ عشرَ مخرجًا مُجمَّدًا، وثلاثَ عشرةَ فئةً في "
    "المواصفة — ولا تُدمَج"
)

SLGAE_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    THE_DEPOSIT_IS_NOT_AN_ADOPTION_NOTE,
    THE_BORN_TABLE_IS_NOT_AN_IMPORTED_TABLE_NOTE,
    THE_INVENTORY_CONFLICT_IS_STRUCTURAL_NOTE,
    AN_ABSENT_ROW_IS_NOT_A_FEATURE_NOTE,
    THE_THIRD_DIVISION_IS_REGISTERED_NOT_MERGED_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


if len(born_inventory()) != sum(
    len(chars) for _block, chars in BORN_BLOCKS
):  # pragma: no cover - حارس
    raise RuntimeError(
        "حرفٌ مكرّرٌ بين الكتل المولودة؛ وقسمتان لحرفٍ واحدٍ تُفسِدان كلَّ " "قسمةٍ مبنيّةٍ عليهما."
    )
if not set(born_inventory()) <= set(CLASSICAL_ORDINAL):  # pragma: no cover - حارس
    raise RuntimeError(
        "في المفردة المولودة حرفٌ لا رتبةَ له في الجدول المُجمَّد؛ "
        "والمقابلةُ حينئذٍ تقابلُ ما ليس في الطرفين."
    )
if len(CLASSICAL_MAKHARIJ) != frozen_makhraj_count():  # pragma: no cover - حارس
    raise RuntimeError("عددُ المخارج يخالف ما تقرؤه وحدةُ الحاجز منه.")
