"""إيداعُ جدول جذور «مقاييس اللغة» مُبصَّمًا، وعدّان يُعاد اشتقاقهما منه.

**ما تفعله هذه الوحدة**: تُجمِّد بايتاتِ الملفّ الذي وصل إلى الشجرة —
`maqayis_by_root_csv_999.csv` — ببصمةٍ وطولٍ يُتحقَّق منهما من البايتات نفسها،
ثمّ تُعيد اشتقاقَ عددين كان النصُّ الوارد يُسمّيهما بلا سند: عددَ السجلّات
وعددَ الجذور الثلاثيّة المتمايزة. ولا أكثر.

`THE_BYTES_ARE_IN_THE_TREE_NOW`: كان `maqayis_by_root_csv_999.csv` مُسمًّى في
§٢-ب بلا بصمة، وكان `A_NAMED_SOURCE_IS_NOT_DEPOSITED_BYTES` يقرأ التسميةَ
تسميةً لا إيداعًا. وقد وصلت البايتاتُ بعدُ إلى الشجرة نفسِها، فتُبصَّم هنا
وتُطابَق؛ والمكسبُ أنّ العددين صارا **قابلين لإعادة الاشتقاق**، لا أنّ دعوى
النصّ صارت مُصدَّقة.

`THE_DIGEST_IS_READ_FROM_THE_FILE`: `FROZEN_ROOT_TABLE` يُعلن الطولَ والبصمة،
و`read_root_table_bytes` يقرأ البايتاتِ من الشجرة ويرفضها إن اختلف أحدُهما.
فبصمةٌ مكتوبةٌ بيدٍ بلا مطابقةٍ تُصادق على ما لم تُبصَّم عليه.

`A_COUNT_IS_RELATIVE_TO_ITS_COUNTING_RULE`: «سجلّ» و«جذر ثلاثيّ» ليسا
مُعطَيين في البايتات؛ هما ناتجُ قاعدةِ عدٍّ تُعلَن قبل الرقم. فكلُّ عددٍ هنا
يحمل قاعدتَه بنصّها (`RECORD_COUNTING_RULE`، `TRILATERAL_ROOT_COUNTING_RULE`،
`FILE_LINE_COUNTING_RULE`)، ورقمٌ بلا قاعدتِه ليس قابلًا لإعادة الاشتقاق ولو
طابقت بصمةُ ملفّه.

`THE_LINE_COUNT_WAS_ITSELF_RULE_FREE`: كان ٣٦٬٥٩٧ مذكورًا في نصّ القانون
أعلاه بلا قاعدةِ عدٍّ وبلا إعادةِ اشتقاق، بخلاف العددين المذكورين معه —
فالقانونُ كان يُخالَف في مثاله. وهو صحيحٌ تحت قاعدةٍ واحدةٍ بعينها (عدُّ
فواصل الأسطر)، ويصير ٣٦٬٥٩٨ تحت قاعدةٍ أخرى مشروعةٍ (`splitlines`) لأنّ
الملفَّ **لا ينتهي بفاصل سطر**؛ فالقاعدةُ تُعلَن هنا بنصّها، والعددُ يُعاد
اشتقاقُه، والفرقُ يُسمّى ولا يُطوى.

`A_COUNT_IN_A_FILE_IS_NOT_A_COUNT_IN_ARABIC`: ٤٬٠٨٧ عددُ جذورٍ ثلاثيّةٍ
متمايزةٍ **في هذا الملفّ**، وهو دالّةٌ في نسخة المعجم وفي قاعدة العدّ معًا؛
وليس عددَ الجذور الثلاثيّة في العربية، ولا عددَها عند ابن فارس، ولا حدًّا
على أيّهما.

`THE_CORPUS_FIGURES_STAY_WITHHELD`: أرقامُ المدوّنة (10,599 و11,467 و37,682
و18,333) لا تُرفَع بهذه الوحدة: هي دالّةٌ في مسار قياسٍ على
`quran-simple-enhanced.txt` لا في جدول الجذور وحده، ولا `MeasurementRunManifest`
لذلك المسار (`arabic/encoding/measurement.py`)، ولا توقّعٌ مكتوبٌ قبل القياس.
فالمرفوعُ ما تكفيه بايتاتُ هذا الملفّ وحدها، وما سواه باقٍ بحاله.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`؛ ولا تُرفَع بهذه الوحدة طبقةٌ محجوبة،
ولا يُصدَر بها تصنيفُ جذرٍ ولا وزنٍ ولا مقطع.
"""

from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Final

from .pipeline_stations import repository_root_path

__all__ = [
    "A_COUNT_IN_A_FILE_IS_NOT_A_COUNT_IN_ARABIC_NOTE",
    "A_COUNT_IS_RELATIVE_TO_ITS_COUNTING_RULE_NOTE",
    "DECLARED_COLUMNS",
    "FILE_LINE_COUNTING_RULE",
    "FROZEN_ROOT_TABLE",
    "RECORD_COUNTING_RULE",
    "REDERIVED_DISTINCT_TRILATERAL_ROOTS",
    "REDERIVED_FILE_LINE_COUNT",
    "REDERIVED_RECORD_COUNT",
    "REDERIVED_SPECIFICATION_FIGURES",
    "ROOT_TABLE_RELATIVE_PATH",
    "THE_BYTES_ARE_IN_THE_TREE_NOW_NOTE",
    "THE_CORPUS_FIGURES_STAY_WITHHELD_NOTE",
    "THE_LINE_COUNT_WAS_ITSELF_RULE_FREE_NOTE",
    "TRILATERAL_ROOT_COUNTING_RULE",
    "TRILATERAL_ROOT_TYPE",
    "MaqayisRootTableError",
    "RederivedSpecificationFigure",
    "RootTableReference",
    "file_ends_with_a_line_separator",
    "read_root_table_bytes",
    "rederive_distinct_trilateral_roots",
    "rederive_file_line_count",
    "rederive_record_count",
    "root_table_digest",
    "root_table_path",
    "root_table_rows",
]


ROOT_TABLE_RELATIVE_PATH: Final[str] = "maqayis_by_root_csv_999.csv"


class MaqayisRootTableError(ValueError):
    """رفضٌ صريح: الملفُّ غائبٌ، أو بايتاتُه لا تطابق المُجمَّد، أو عمودٌ ناقص."""


@dataclass(frozen=True, slots=True)
class RootTableReference:
    """مرجعُ بايتات جدول الجذور: اسمٌ وطولٌ وبصمةٌ وترميزٌ وسياسةُ تطبيق."""

    source_name: str
    byte_length: int
    sha256_hex: str
    encoding: str
    normalization_policy: str

    def __post_init__(self) -> None:
        if not self.source_name.strip():
            raise MaqayisRootTableError("مرجعُ البايتات بلا اسمِ مصدر")
        if self.byte_length <= 0:
            raise MaqayisRootTableError("طولُ البايتات لا يكون غيرَ موجب")
        if len(self.sha256_hex) != 64 or any(
            character not in "0123456789abcdef" for character in self.sha256_hex
        ):
            raise MaqayisRootTableError("البصمةُ ليست SHA-256 ستّ عشريّةً كاملة")
        if not self.encoding.strip() or not self.normalization_policy.strip():
            raise MaqayisRootTableError("الترميزُ وسياسةُ التطبيع مُصرَّحان")

    def as_canonical_content(self) -> dict[str, object]:
        return {
            "source_name": self.source_name,
            "byte_length": self.byte_length,
            "sha256_hex": self.sha256_hex,
            "encoding": self.encoding,
            "normalization_policy": self.normalization_policy,
        }


FROZEN_ROOT_TABLE: Final[RootTableReference] = RootTableReference(
    source_name=ROOT_TABLE_RELATIVE_PATH,
    byte_length=5_539_405,
    sha256_hex="2c6000bd47797e183294b89da77df4ddfd27921ea595c6071ba52299c382ccb0",
    encoding="utf-8-without-bom",
    normalization_policy=(
        "لا تطبيع البتّة: البايتاتُ تُقرأ كما وردت، ويُفَكّ ترميزُها مرّةً "
        "واحدةً بـ UTF-8، ولا تُطوى حركةٌ ولا همزةٌ ولا صورةُ ألفٍ في أخرى"
    ),
)
"""البايتاتُ موجودةٌ في الشجرة بمسارها، والمُجمَّدُ هنا بصمتُها وطولُها."""


DECLARED_COLUMNS: Final[tuple[str, ...]] = (
    "root_full",
    "root_type",
    "entry_num",
    "root_display",
    "semantic_axes",
    "axes_count",
    "poetry_evidence",
    "body_text",
    "chapter_header",
)
"""ترويسةُ الملفّ كما وردت؛ تُطابَق عند القراءة فلا يُعَدّ عمودٌ باسمٍ متوهَّم."""

TRILATERAL_ROOT_TYPE: Final[str] = "ثلاثي"
"""قيمةُ `root_type` التي يُعَدّ بها الجذرُ ثلاثيًّا، كما هي في الملفّ."""

RECORD_COUNTING_RULE: Final[str] = (
    "السجلُّ صفٌّ واحدٌ في `csv` بعد صفّ الترويسة، مقروءًا بقارئٍ يحترم "
    "الاقتباسَ وفواصلَ الأسطر داخل الحقول؛ فعددُ الأسطر في الملفّ ليس عددَ "
    "السجلّات، إذ تحمل حقولُ الشواهد والنصّ أسطرًا داخلها"
)

TRILATERAL_ROOT_COUNTING_RULE: Final[str] = (
    "الجذرُ الثلاثيُّ صفٌّ قيمةُ `root_type` فيه «ثلاثي» بالضبط، والعدُّ على "
    "قيمِ `root_full` **المتمايزة** لا على الصفوف: الملفُّ يحمل جذرين "
    "بصفّين لكلٍّ منهما، فعدُّ الصفوف يزيد اثنين. والمعتلُّ والمضاعفُ "
    "والرباعيُّ المكرَّرُ خارج هذا العدّ بنصّ القاعدة لا بإهمال"
)

FILE_LINE_COUNTING_RULE: Final[str] = (
    "سطرُ الملفّ محسوبٌ بعدد فواصل الأسطر (`\\n`) في البايتات، وهي قاعدةُ "
    "`wc -l` نفسُها. وهذه القاعدةُ ليست الوحيدةَ المشروعة: الملفُّ **لا "
    "ينتهي بفاصل سطر**، فقاعدةُ «عدُّ المقاطع التي يُنتجها `splitlines`» "
    "تُعطي واحدًا أكثر، لأنّ البايتات بعد الفاصل الأخير مقطعٌ لا فاصلَ له. "
    "فالعددان صحيحان كلٌّ تحت قاعدته، والمُجمَّدُ هنا الأولى بنصّها"
)


def root_table_path(root: Path | None = None) -> Path:
    """مسارُ الملفّ، مُشتقًّا من جذر المستودع لا مكتوبًا مطلقًا."""

    return (root or repository_root_path()) / ROOT_TABLE_RELATIVE_PATH


def read_root_table_bytes(root: Path | None = None) -> bytes:
    """بايتاتُ الملفّ كما هي على القرص، مرفوضةً إن خالفت الطولَ أو البصمة."""

    path = root_table_path(root)
    if not path.is_file():
        raise MaqayisRootTableError(
            f"جدولُ الجذور غيرُ موجودٍ في الشجرة: {ROOT_TABLE_RELATIVE_PATH}"
        )
    data = path.read_bytes()
    if len(data) != FROZEN_ROOT_TABLE.byte_length:
        raise MaqayisRootTableError(
            f"طولُ البايتات {len(data)} لا يطابق المُجمَّد "
            f"{FROZEN_ROOT_TABLE.byte_length}"
        )
    digest = hashlib.sha256(data).hexdigest()
    if digest != FROZEN_ROOT_TABLE.sha256_hex:
        raise MaqayisRootTableError(
            f"بصمةُ البايتات {digest} لا تطابق المُجمَّد " f"{FROZEN_ROOT_TABLE.sha256_hex}"
        )
    return data


def root_table_digest(root: Path | None = None) -> str:
    """بصمةُ الملفّ مُشتقّةً من بايتاته، لا منسوخةً من حقلٍ في وحدةٍ أخرى."""

    return hashlib.sha256(read_root_table_bytes(root)).hexdigest()


def root_table_rows(root: Path | None = None) -> tuple[dict[str, str], ...]:
    """صفوفُ الملفّ بعد التحقّق من بايتاته ومن ترويسته، بلا تطبيعِ محتوى."""

    data = read_root_table_bytes(root)
    if data.startswith(b"\xef\xbb\xbf"):
        raise MaqayisRootTableError(
            "البايتاتُ تبدأ بعلامة ترتيبٍ، والمُجمَّدُ «utf-8 بلا علامة ترتيب»"
        )
    reader = csv.DictReader(StringIO(data.decode("utf-8"), newline=""))
    if tuple(reader.fieldnames or ()) != DECLARED_COLUMNS:
        raise MaqayisRootTableError(
            "ترويسةُ الملفّ لا تطابق الأعمدةَ المُعلَنة، فلا يُعَدّ عمودٌ " "باسمٍ متوهَّم"
        )
    return tuple(dict(row) for row in reader)


def rederive_record_count(root: Path | None = None) -> int:
    """عددُ السجلّات تحت `RECORD_COUNTING_RULE`، مُشتقًّا من البايتات المُبصَّمة."""

    return len(root_table_rows(root))


def rederive_file_line_count(root: Path | None = None) -> int:
    """عددُ أسطر الملفّ تحت `FILE_LINE_COUNTING_RULE`، من البايتات المُبصَّمة."""

    return read_root_table_bytes(root).count(b"\n")


def file_ends_with_a_line_separator(root: Path | None = None) -> bool:
    """هل تنتهي البايتاتُ بفاصل سطر؟ عليه يدور فرقُ القاعدتين، فلا يُخمَّن."""

    return read_root_table_bytes(root).endswith(b"\n")


def rederive_distinct_trilateral_roots(root: Path | None = None) -> int:
    """عددُ الجذور الثلاثيّة المتمايزة تحت `TRILATERAL_ROOT_COUNTING_RULE`."""

    return len(
        {
            row["root_full"]
            for row in root_table_rows(root)
            if row["root_type"] == TRILATERAL_ROOT_TYPE
        }
    )


REDERIVED_RECORD_COUNT: Final[int] = 4_576
"""٤٬٥٧٦: الرقمُ الذي سمّته §٢-ب، مُعادًا اشتقاقُه هنا ومفحوصًا في الاختبارات."""

REDERIVED_DISTINCT_TRILATERAL_ROOTS: Final[int] = 4_087
"""٤٬٠٨٧: الرقمُ الذي سمّاه مُعرِّفُ التجميد الوارد في §٢-أ، مُعادًا اشتقاقُه هنا.

وصفوفُ «ثلاثي» ٤٬٠٨٩ لا ٤٬٠٨٧؛ والفرقُ جذران مكرَّران بصفّين، فالمطابقةُ تقع
على **المتمايز** لا على الصفوف، وهو ما تقوله `TRILATERAL_ROOT_COUNTING_RULE`.
"""

REDERIVED_FILE_LINE_COUNT: Final[int] = 36_597
"""٣٦٬٥٩٧: الرقمُ الذي ذُكر في نصّ القانون بلا قاعدةٍ، مُعادًا اشتقاقُه بقاعدته.

وهو عددُ فواصل الأسطر تحت `FILE_LINE_COUNTING_RULE`. والملفُّ لا ينتهي بفاصل
سطر، فقاعدةُ `splitlines` تُعطي ٣٦٬٥٩٨؛ والعددان ليسا تناقضًا بل قاعدتان،
و`file_ends_with_a_line_separator` هي الواقعةُ التي يدور عليها الفرق.
"""


@dataclass(frozen=True, slots=True)
class RederivedSpecificationFigure:
    """رقمٌ سمّاه النصُّ الوارد وصار يُعاد اشتقاقُه هنا: قيمتُه وقاعدتُه وحدُّه.

    `A_MATCHING_COUNT_IS_NOT_A_VINDICATED_CLAIM`: مطابقةُ الرقم تُثبت أنّ
    العادَّ عدَّ هذا الملفَّ بهذه القاعدة، ولا تُثبت الدعوى المبنيّةَ عليه؛
    فحقلُ `what_it_still_does_not_establish` لازمٌ لا زينة.
    """

    figure: str
    locus: str
    claim_text: str
    rederived_count: int
    counting_rule: str
    what_it_still_does_not_establish: str

    def __post_init__(self) -> None:
        for field_name in (
            "figure",
            "locus",
            "claim_text",
            "counting_rule",
            "what_it_still_does_not_establish",
        ):
            if not str(getattr(self, field_name)).strip():
                raise MaqayisRootTableError(
                    "رقمٌ مُعادُ الاشتقاق بلا قاعدةِ عدٍّ أو بلا حدٍّ مكتوبٍ "
                    "لما لا يُثبته يُقرأ بعد جلساتٍ تصديقًا للدعوى، وليس إيّاه"
                )
        if self.rederived_count <= 0:
            raise MaqayisRootTableError("عددٌ مُعادُ الاشتقاق لا يكون غيرَ موجب")


REDERIVED_SPECIFICATION_FIGURES: Final[tuple[RederivedSpecificationFigure, ...]] = (
    RederivedSpecificationFigure(
        figure="4,576",
        locus="§٢-ب — رسالةُ التسمية",
        claim_text="«maqayis_by_root_csv_999.csv (معجم مقاييس اللغة، 4,576 سجلًّا)»",
        rederived_count=REDERIVED_RECORD_COUNT,
        counting_rule=RECORD_COUNTING_RULE,
        what_it_still_does_not_establish=(
            "أنّ هذه النسخةَ هي التي قاس عليها المُرسِل: البصمةُ تُثبت ما في "
            "هذه الشجرة، والنصُّ الواردُ لم يذكر بصمةً يُطابَق عليها. ولا "
            "يُعرَف من النصّ ما «السجلّ» عنده، فالمطابقةُ في القيمة لا في "
            "المفهوم"
        ),
    ),
    RederivedSpecificationFigure(
        figure="4,087",
        locus="§٢-أ — مُعرِّفُ التجميد الواردُ لتصحيح المجرد والمزيد",
        claim_text=(
            "«معجم مقاييس اللغة، 4,087 جذرًا ثلاثيًّا مُبصَّمًا، ملف "
            "maqayis_by_root_csv_999.csv»"
        ),
        rederived_count=REDERIVED_DISTINCT_TRILATERAL_ROOTS,
        counting_rule=TRILATERAL_ROOT_COUNTING_RULE,
        what_it_still_does_not_establish=(
            "التجميدَ الذي سُمّي به: مُعرِّفُه مُسجَّلٌ بحروفه في "
            "`SUBMITTED_FREEZE_IDENTIFIERS` ولا يُعاد نسخُه هنا، ولم تُصدِره "
            "هذه الشجرة؛ ومطابقةُ عددِ جذوره لا تُصدِّر تجميدًا. ولا "
            "يُثبت العددُ أنّ الأربعةَ آلافٍ وسبعةً وثمانين جذورُ العربية "
            "الثلاثيّة، ولا يُقرأ منه تصنيفُ جذرٍ بعينه مجرّدًا أو مزيدًا"
        ),
    ),
    RederivedSpecificationFigure(
        figure="36,597",
        locus="§٢-ب ونصُّ `A_COUNT_IS_RELATIVE_TO_ITS_COUNTING_RULE` نفسِه",
        claim_text="«صفٌّ في csv لا سطرٌ في ملفّ (أسطرُه ٣٦٬٥٩٧)»",
        rederived_count=REDERIVED_FILE_LINE_COUNT,
        counting_rule=FILE_LINE_COUNTING_RULE,
        what_it_still_does_not_establish=(
            "أنّ ٣٦٬٥٩٧ «عددُ أسطر الملفّ» مطلقًا: هو عددُها تحت قاعدةٍ "
            "واحدةٍ من قاعدتين مشروعتين، ويصير ٣٦٬٥٩٨ تحت الأخرى لأنّ "
            "الملفَّ لا ينتهي بفاصل سطر. وكان الرقمُ مذكورًا هنا بلا قاعدةٍ "
            "ولا إعادةِ اشتقاق، فكان نصُّ القانون يُخالَف في مثاله؛ "
            "والمرفوعُ بهذا الإدخال تلك المخالفةُ وحدها، لا شيءٌ عن الملفّ"
        ),
    ),
)


THE_BYTES_ARE_IN_THE_TREE_NOW_NOTE: Final[str] = (
    "TheBytesAreInTheTreeNow: وصل `maqayis_by_root_csv_999.csv` إلى الشجرة "
    "بمساره، فبصمتُه وطولُه مُجمَّدان هنا ويُطابَقان على البايتات نفسِها عند "
    "كلّ قراءة؛ والمرفوعُ بذلك تعذُّرُ إعادة اشتقاق عددين، لا التصديقُ على "
    "دعوى النصّ الوارد"
)

A_COUNT_IS_RELATIVE_TO_ITS_COUNTING_RULE_NOTE: Final[str] = (
    "ACountIsRelativeToItsCountingRule: «سجلّ» و«جذر ثلاثيّ» و«سطر» ناتجُ "
    "قاعدةٍ تُعلَن قبل الرقم لا مُعطًى في البايتات؛ فأسطرُ الملفّ ٣٦٬٥٩٧ تحت "
    "`FILE_LINE_COUNTING_RULE`، وسجلّاتُه ٤٬٥٧٦، وصفوفُ «ثلاثي» ٤٬٠٨٩ "
    "ومتمايزُها ٤٬٠٨٧ — كلٌّ بقاعدته المكتوبة ومُعادَ الاشتقاق"
)

THE_LINE_COUNT_WAS_ITSELF_RULE_FREE_NOTE: Final[str] = (
    "TheLineCountWasItselfRuleFree: ذُكر ٣٦٬٥٩٧ في نصّ القانون أعلاه بلا "
    "قاعدةِ عدٍّ وبلا إعادةِ اشتقاق، بخلاف العددين المذكورين معه؛ فكان "
    "القانونُ يُخالَف في مثاله. وقد صار له قاعدةٌ ودالّةٌ تُعيد اشتقاقَه، "
    "وصار فرقُ القاعدتين (٣٦٬٥٩٧ مقابل ٣٦٬٥٩٨) مُسمًّى بعلّته: غيابُ فاصل "
    "السطر الأخير، مفحوصًا بـ `file_ends_with_a_line_separator` لا مُخمَّنًا"
)

A_COUNT_IN_A_FILE_IS_NOT_A_COUNT_IN_ARABIC_NOTE: Final[str] = (
    "ACountInAFileIsNotACountInArabic: العددان دالّةٌ في هذه النسخة من "
    "المعجم وفي قاعدة العدّ معًا؛ وليسا عددَ الجذور في العربية ولا حدًّا "
    "عليه، ولا يُقرأ منهما تصنيفُ جذرٍ واحدٍ بعينه"
)

THE_CORPUS_FIGURES_STAY_WITHHELD_NOTE: Final[str] = (
    "TheCorpusFiguresStayWithheld: 10,599 و11,467 و37,682 و18,333 باقيةٌ غيرَ "
    "قابلةٍ لإعادة الاشتقاق: مسارُ قياسها على المدوّنة لا على هذا الملفّ، ولا "
    "`MeasurementRunManifest` يُجمّد صورةَ التطبيع وإصدارَ قاعدة Unicode، ولا "
    "توقّعٌ مكتوبٌ قبل القياس"
)
