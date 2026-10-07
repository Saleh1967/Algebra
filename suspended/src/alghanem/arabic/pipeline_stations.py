"""محطّاتُ الأنبوب الإحدى عشرة، مُشتقّةً من الشجرة لا مكتوبةً (§9 من G0.N).

كلّ محطّةٍ تُسمّي وحدتَها بمسارها في الشجرة، ووجودُ الوحدة يُقرأ من الشجرة
نفسها؛ وغيابُها يُنتج `محطة_غير_مُرمَّزة` لا تخطّيًا صامتًا.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from pathlib import Path
from typing import Final

__all__ = [
    "ARABIC_PACKAGE_RELATIVE_PATH",
    "STATIONS_LEDGER_IS_NOT_A_GATE_NOTE",
    "STATION_ZERO_NOTE",
    "TERMINAL_STATION_NOTE",
    "PipelineStationsError",
    "StationCoding",
    "StationDeclaration",
    "StationEpistemicState",
    "StationReading",
    "read_stations",
    "repository_root_path",
]


class PipelineStationsError(ValueError):
    """رفضٌ صريحٌ في دفتر محطّات الأنبوب."""


class StationEpistemicState(Enum):
    """الحالُ المعرفية للمحطّة؛ مفردةٌ مغلقةٌ خماسية."""

    معلومة = "معلومة"
    فرض = "فرض"
    آحاد = "آحاد"
    آحاد_مُجمَّد = "آحاد_مُجمَّد"
    ظنّي = "ظنّي"


class StationCoding(Enum):
    """حالُ ترميز المحطّة، مُشتقّةً من الشجرة."""

    مُرمَّزة = "مُرمَّزة"
    محطة_غير_مُرمَّزة = "محطة_غير_مُرمَّزة"


ARABIC_PACKAGE_RELATIVE_PATH: Final[str] = "src/alghanem/arabic"

STATION_ZERO_NOTE: Final[str] = (
    "المحطّة صفر (الصوت المنطوق) خارج الأنبوب: بياناتُ هذا المستودع نصٌّ "
    "مُرمَّز لا صوتٌ مُسجَّل، فإدراجُها في الجدول بوصفها محطّةً يُرفَض باسمه "
    "لا يُطوى، على منوال `UnicodeIsNotRecordedSound`."
)

TERMINAL_STATION_NOTE: Final[str] = (
    "المحطّة ∞ (الدلالةُ التامّة) بلا وحدةٍ بالضرورة لا بالتقصير: ليست موضعًا "
    "في الشجرة يُنتظَر ترميزُه، بل حدٌّ لا يبلغه أنبوب."
)

STATIONS_LEDGER_IS_NOT_A_GATE_NOTE: Final[str] = (
    "دفترُ المحطّات قراءةٌ للشجرة لا سلطةٌ عليها: لا يُصدر ولادةً ولا تجميدًا، "
    "ولا تقرؤه وحدةٌ في `kernel/`."
)

_DECLARED_STATIONS: Final[tuple[tuple[int, str, str, StationEpistemicState], ...]] = (
    (
        1,
        "الرصدُ السطحيّ الخام",
        "encoding/observation.py",
        StationEpistemicState.معلومة,
    ),
    (
        2,
        "تسويةُ السطح وجدولُ البقايا",
        "encoding/normalization.py",
        StationEpistemicState.معلومة,
    ),
    (
        3,
        "تجميدُ بروتوكول القياس",
        "encoding/measurement.py",
        StationEpistemicState.آحاد_مُجمَّد,
    ),
    (
        4,
        "جنسُ المنشأ",
        "encoding/provenance_genus.py",
        StationEpistemicState.معلومة,
    ),
    (
        5,
        "مرشَّحاتُ الذرّات السطحية",
        "encoding/candidates.py",
        StationEpistemicState.فرض,
    ),
    (
        6,
        "المفردةُ المستورَدة وبصمةُ مصدرها",
        "imported_feature_vocabulary.py",
        StationEpistemicState.آحاد,
    ),
    (
        7,
        "التسجيلُ القبْليّ للمسبار",
        "probe_preregistration.py",
        StationEpistemicState.فرض,
    ),
    (
        8,
        "تقريرُ المسبار التوزيعيّ",
        "distributional_probe_report.py",
        StationEpistemicState.ظنّي,
    ),
    (
        9,
        "رتبةُ الجاهزية",
        "readiness_rank.py",
        StationEpistemicState.ظنّي,
    ),
    (
        10,
        "الشهاداتُ الصورية المُجمَّدة",
        "word_class_formal.py",
        StationEpistemicState.آحاد_مُجمَّد,
    ),
    (
        11,
        "سجلُّ دعوى التقارب",
        "convergence_claim_register.py",
        StationEpistemicState.ظنّي,
    ),
)


def repository_root_path() -> Path:
    """جذرُ المستودع، مُشتقًّا من موضع هذه الوحدة لا مكتوبًا."""

    return Path(__file__).resolve().parents[3]


@dataclass(frozen=True, slots=True)
class StationDeclaration:
    """إعلانُ محطّةٍ واحدة: رتبتُها، واسمُها، ووحدتُها، وحالُها المعرفية."""

    ordinal: int
    title: str
    module_relative_path: str
    epistemic_state: StationEpistemicState

    def __post_init__(self) -> None:
        if not isinstance(self.ordinal, bool) and isinstance(self.ordinal, int):
            if self.ordinal == 0:
                raise PipelineStationsError(STATION_ZERO_NOTE)
            if not 1 <= self.ordinal <= 11:
                raise PipelineStationsError(
                    "رتبةُ المحطّة بين الأولى والحادية عشرة؛ وما بعدها المحطّةُ "
                    "∞ التي لا تُدرَج."
                )
        else:
            raise PipelineStationsError("رتبةُ المحطّة عددٌ صحيح.")
        for name in ("title", "module_relative_path"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise PipelineStationsError(f"{name} نصٌّ غير فارغ.")
        if self.module_relative_path.endswith("__init__.py"):
            raise PipelineStationsError("وحدةُ المحطّة وحدةٌ مُسمّاة، لا ملفَّ تجميعِ حزمة.")
        if not isinstance(self.epistemic_state, StationEpistemicState):
            raise PipelineStationsError("الحالُ المعرفية من مفردتها المغلقة.")

    @property
    def module_path(self) -> str:
        """مسارُ الوحدة في الشجرة، منسوبًا إلى جذر المستودع."""

        return f"{ARABIC_PACKAGE_RELATIVE_PATH}/{self.module_relative_path}"


@dataclass(frozen=True, slots=True)
class StationReading:
    """قراءةُ محطّةٍ واحدة: إعلانُها، وحالُ ترميزها المُشتقّ من الشجرة."""

    declaration: StationDeclaration
    coding: StationCoding

    def __post_init__(self) -> None:
        if not isinstance(self.declaration, StationDeclaration):
            raise PipelineStationsError("إعلانُ المحطّة إعلانٌ مُصاغ.")
        if not isinstance(self.coding, StationCoding):
            raise PipelineStationsError("حالُ الترميز من مفردتها المغلقة.")

    @property
    def is_coded(self) -> bool:
        return self.coding is StationCoding.مُرمَّزة


def read_stations(root: Path | None = None) -> tuple[StationReading, ...]:
    """اقرأ المحطّات الإحدى عشرة، مُشتقًّا وجودَ كلّ وحدةٍ من الشجرة."""

    base = repository_root_path() if root is None else root
    if not isinstance(base, Path):
        raise PipelineStationsError("جذرُ المستودع مسار.")
    package = base / ARABIC_PACKAGE_RELATIVE_PATH
    if not package.is_dir():
        raise PipelineStationsError(
            f"طبقةُ العربية غير موجودة عند {package}: شجرةٌ غائبةٌ تُقرأ «لا "
            "وحدات» وهو ادّعاءٌ لم تُقرأ الشجرة لأجله."
        )
    readings: list[StationReading] = []
    for ordinal, title, relative, state in _DECLARED_STATIONS:
        declaration = StationDeclaration(
            ordinal=ordinal,
            title=title,
            module_relative_path=relative,
            epistemic_state=state,
        )
        coding = (
            StationCoding.مُرمَّزة
            if (package / relative).is_file()
            else StationCoding.محطة_غير_مُرمَّزة
        )
        readings.append(StationReading(declaration=declaration, coding=coding))
    return tuple(readings)


def _assert_no_fields_matching(markers: tuple[str, ...]) -> None:
    for declaring_type in (StationDeclaration, StationReading):
        for field in fields(declaring_type):
            for marker in markers:
                if marker in field.name:
                    raise RuntimeError(
                        f"{declaring_type.__name__} يحمل حقلاً محظورًا: {field.name}"
                    )


if len(StationEpistemicState) != 5:
    raise RuntimeError("الحالُ المعرفية خماسيةٌ مغلقة.")
if len(StationCoding) != 2:
    raise RuntimeError("حالُ الترميز ثنائيةٌ مغلقة.")
if len(_DECLARED_STATIONS) != 11:
    raise RuntimeError("محطّاتُ الأنبوب إحدى عشرةَ محطّة.")
if tuple(row[0] for row in _DECLARED_STATIONS) != tuple(range(1, 12)):
    raise RuntimeError("رتبُ المحطّات متعاقبةٌ من الأولى إلى الحادية عشرة.")
_assert_no_fields_matching(("count", "number", "total", "verdict", "birth"))
