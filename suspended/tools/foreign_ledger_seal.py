"""تجميدُ نتائجِ أنبوبٍ **غيرِ هذه الشجرة**، وإعادةُ اشتقاقِ ما يُشتَقّ منها.

**ما هذا السجلّ**: أُودِعت في `deposits/foreign_*.txt` أربعةُ ملفّاتٍ من
تشغيلٍ أُجري **خارج** هذا المستودع، بمقامٍ غيرِ مقامه. **ولستُ أنا مَن
أجراها ولا مَن يوقّع تأويلَها.**

`THE_ONLY_THING_A_FOREIGN_RUN_LETS_ME_DO_IS_RECOMPUTE_ITS_OWN_ARITHMETIC`:
ولا أملك مدوّنتَه ولا وسومَه، **فلا أعيد قياسَه**. وأملك **أعدادَه
المطبوعة**، فأُعيد منها ما يُشتَقّ: الإنتروبيا من النِّسَب، ومتوسّطَ
هافمان من أطوال الرموز، ومجموعَ كرافت، وأعماقَ الشجرات، والمجاميع.

`WHAT_THE_FILES_DO_NOT_PUBLISH_IS_BOUNDED_NOT_BELIEVED`: وجردُ المتّجه
يُنشَر **ثمانيةً من أربعَ عشرةَ خانة**، فلا تُعاد `H(المتّجه)` حسابًا
تامًّا. **فتُحَدُّ بحدّين** يُشتقّان من المنشور وحدَه، ويُقال أَداخلَها
المنشورُ أم خارج. **ولا تُصدَّق ولا تُكذَّب.**

`THE_STAND_IS_NOT_THE_SAME_STAND`: والمقامُ **٧٧٬٤٢٩** كلمةً و**٦٬٢٠٨**
آيةً، ومقامُ هذه الشجرة **٧٨٬٢٤٥** و**٦٬٢٣٦**. **فلا يُنقَل رقمٌ من أحدهما
إلى الآخر**، والفرقُ **يُسمّى ولا يُخمَّن**.

`AND_WHAT_THE_RUN_SPENT_WITHOUT_PRINTING_IS_NAMED_AS_A_DEBT`: وثَمَّ
مواضعُ **صُرِفت في التزاحم ولم يُطبَع عددُها**، وأعدادُ وسومٍ لا تجمع إلى
المنشور. **تُسمّى دَينًا بأرقامها** ولا تُطوى ولا تُفسَّر.

**ولا اسمَ بابٍ يدخل هذا السجلّ**: بنودٌ وأساليبُ بأسمائها كما طُبِعت،
وأعدادٌ وبتّات.
"""

from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Final

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[1]
DEPOSITS: Final[Path] = REPOSITORY / "deposits"
BUNUD_OUT: Final[str] = "foreign_bunud_out.txt"
ASALIB_OUT: Final[str] = "foreign_asalib_out.txt"
ASALIB_PRED: Final[str] = "foreign_asalib_pred.txt"

_FIELD_SEPARATOR: Final[str] = "\x1f"
_RECORD_SEPARATOR: Final[str] = "\x1e"
_TOLERANCE: Final[float] = 5e-4
"""حدُّ المطابقة: الأعدادُ منشورةٌ بأربع منازل، فالفرقُ دونها تقريبٌ لا خلاف."""


class ForeignLedgerError(ValueError):
    """رُدَّ سجلٌّ خالف حسابَه، أو ادّعى إعادةَ ما لا يُعاد."""


def bit_entropy(share: float) -> float:
    """`H` لبتٍّ ثنائيٍّ نصيبُه `share` — تُشتَقّ ولا تُنقَل."""

    if not 0.0 < share < 1.0:
        raise ForeignLedgerError(f"نصيبُ بتٍّ خارجَ (٠، ١): {share}")
    return -(share * math.log2(share) + (1.0 - share) * math.log2(1.0 - share))


def entropy(shares: tuple[float, ...]) -> float:
    return -math.fsum(one * math.log2(one) for one in shares if one > 0)


def kraft(lengths: tuple[int, ...]) -> float:
    return math.fsum(2.0**-one for one in lengths)


def prefix_free(codes: tuple[str, ...]) -> bool:
    return not any(one != two and two.startswith(one) for one in codes for two in codes)


@dataclass(frozen=True, slots=True)
class ForeignLedger:
    """نتائجُ الأنبوب الخارجيّ مُقفَلةً — وكلُّ حقلٍ منها مطبوعٌ في ملفّاته."""

    stand_words: int
    stand_verses: int
    bunud_names: tuple[str, ...]
    bunud_counts: tuple[int, ...]
    bunud_entropies: tuple[str, ...]
    bunud_gains: tuple[str, ...]
    vector_shown: tuple[int, ...]
    vector_cells: int
    vector_entropy: str
    vector_gain: str
    bunud_code_lengths: tuple[int, ...]
    bunud_codes: tuple[str, ...]
    bunud_huffman: str
    asalib_names: tuple[str, ...]
    asalib_counts: tuple[int, ...]
    asalib_entropy: str
    asalib_huffman: str
    asalib_by_frequency: str
    asalib_by_book: str
    asalib_book_ranks: tuple[int, ...]
    asalib_code_lengths: tuple[int, ...]
    debts: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if len(self.bunud_names) != 8:
            raise ForeignLedgerError("بنودُ الأنبوب ثمانيةٌ كما طُبِعت.")
        for name in ("bunud_counts", "bunud_entropies", "bunud_gains"):
            if len(getattr(self, name)) != 8:
                raise ForeignLedgerError(f"{name}: ثمانيةُ حقولٍ لا غير.")
        for index, count in enumerate(self.bunud_counts):
            mine = bit_entropy(count / self.stand_words)
            theirs = float(self.bunud_entropies[index])
            if abs(mine - theirs) > _TOLERANCE:
                raise ForeignLedgerError(
                    f"{self.bunud_names[index]}: H المطبوعةُ {theirs} "
                    f"والمُشتَقّةُ من العدّ {mine:.4f}"
                )
        if sum(self.vector_shown) >= self.stand_words:
            raise ForeignLedgerError("المنشورُ من خانات المتّجه يفوق المقام.")
        if len(self.vector_shown) >= self.vector_cells:
            raise ForeignLedgerError(
                "الخاناتُ المنشورةُ ليست دون المشغولة، فلا حاجةَ إلى حدّين."
            )
        low, high = self.vector_bounds()
        measured = float(self.vector_entropy)
        if not low <= measured <= high:
            raise ForeignLedgerError(
                f"H(المتّجه) المطبوعةُ {measured} خارجَ الحدّين " f"[{low:.4f}، {high:.4f}]"
            )
        if len(self.bunud_codes) != len(self.bunud_code_lengths):
            raise ForeignLedgerError("لكلّ رمزٍ طولُه، ولا رمزَ بلا طول.")
        for index, code in enumerate(self.bunud_codes):
            if len(code) != self.bunud_code_lengths[index]:
                raise ForeignLedgerError(f"طولُ الرمز يخالف رمزَه: {code}")
        if not prefix_free(self.bunud_codes):
            raise ForeignLedgerError("رموزُ البنود ليست سليمةَ البادئة.")
        if kraft(self.bunud_code_lengths) > 1.0:
            raise ForeignLedgerError("مجموعُ كرافت للمنشور يفوق الواحد.")
        if not float(self.vector_entropy) <= float(self.bunud_huffman):
            raise ForeignLedgerError("هافمانُ البنود دون إنتروبيتها — حدُّ شانون.")
        if not float(self.bunud_huffman) < float(self.vector_entropy) + 1.0:
            raise ForeignLedgerError("هافمانُ البنود يبلغ H + 1 — حدُّ شانون.")

        if len(self.asalib_names) != len(self.asalib_counts):
            raise ForeignLedgerError("لكلّ أسلوبٍ عددُه.")
        shares = self.asalib_shares()
        mine = entropy(shares)
        if abs(mine - float(self.asalib_entropy)) > _TOLERANCE:
            raise ForeignLedgerError(
                f"H(الأسلوب) المطبوعةُ {self.asalib_entropy} "
                f"والمُشتَقّةُ من الأعداد {mine:.4f}"
            )
        if abs(kraft(self.asalib_code_lengths) - 1.0) > 1e-12:
            raise ForeignLedgerError("مجموعُ كرافت لشجرة هافمان ليس واحدًا تامًّا.")
        walked = math.fsum(
            one * two for one, two in zip(shares, self.asalib_code_lengths)
        )
        if abs(walked - float(self.asalib_huffman)) > _TOLERANCE:
            raise ForeignLedgerError(
                f"عمقُ هافمان المطبوعُ {self.asalib_huffman} والمُشتَقُّ {walked:.4f}"
            )
        linear = math.fsum(one * (index + 1) for index, one in enumerate(shares))
        if abs(linear - float(self.asalib_by_frequency)) > _TOLERANCE:
            raise ForeignLedgerError(
                f"عمقُ الترتيب التكراريِّ المطبوعُ {self.asalib_by_frequency} "
                f"والمُشتَقُّ {linear:.4f}"
            )
        booked = math.fsum(
            one * two for one, two in zip(shares, self.asalib_book_ranks)
        )
        if abs(booked - float(self.asalib_by_book)) > _TOLERANCE:
            raise ForeignLedgerError(
                f"عمقُ ترتيب الكتاب المطبوعُ {self.asalib_by_book} "
                f"والمُشتَقُّ {booked:.4f}"
            )
        if not float(self.asalib_entropy) <= float(self.asalib_huffman):
            raise ForeignLedgerError("هافمانُ الأساليب دون إنتروبيتها.")
        if not float(self.asalib_huffman) < float(self.asalib_entropy) + 1.0:
            raise ForeignLedgerError("هافمانُ الأساليب يبلغ H + 1.")
        if not self.debts:
            raise ForeignLedgerError("سجلٌّ بلا دَينٍ مُسمًّى دعوى براءةٍ لا تُقفَل.")
        for name, why in self.debts:
            if not name.strip() or len(why) <= 25:
                raise ForeignLedgerError(f"دَينٌ بلا بيانٍ مكتوب: {name}")

    def asalib_shares(self) -> tuple[float, ...]:
        whole = sum(self.asalib_counts)
        return tuple(one / whole for one in self.asalib_counts)

    def vector_bounds(self) -> tuple[float, float]:
        """حدّا `H(المتّجه)` من المنشور وحدَه — وما بينهما لا يُصدَّق ولا يُكذَّب.

        **الأعلى**: ما بقي من الكتلة موزّعٌ **بالسواء** على الخانات غيرِ
        المنشورة. **والأدنى**: مجموعٌ ما استطاع، على أنّ خانةً غيرَ منشورةٍ
        **لا تفوق أصغرَ منشورة** — وإلّا لكانت منشورة.
        """

        whole = self.stand_words
        shown = tuple(one / whole for one in self.vector_shown)
        known = -math.fsum(one * math.log2(one) for one in shown)
        left = whole - sum(self.vector_shown)
        hidden = self.vector_cells - len(self.vector_shown)
        even = left / hidden / whole
        high = known - hidden * even * math.log2(even)
        ceiling = min(self.vector_shown)
        piled: list[int] = []
        rest = left
        while rest > 0 and len(piled) < hidden:
            room = hidden - len(piled) - 1
            take = min(ceiling, rest - room)
            piled.append(take)
            rest -= take
        low = known - math.fsum(
            (one / whole) * math.log2(one / whole) for one in piled if one > 0
        )
        return low, high


FROZEN_FOREIGN: Final[ForeignLedger] = ForeignLedger(
    stand_words=77_429,
    stand_verses=6_208,
    bunud_names=(
        "أمر",
        "نهي",
        "عموم",
        "استثناء",
        "شرط",
        "صفة",
        "غاية",
        "إطلاق",
    ),
    bunud_counts=(1_956, 332, 8_790, 848, 1_029, 1_957, 884, 8_669),
    bunud_entropies=(
        "0.1700",
        "0.0399",
        "0.5105",
        "0.0870",
        "0.1019",
        "0.1701",
        "0.0900",
        "0.5058",
    ),
    bunud_gains=(
        "0.0357",
        "0.0386",
        "0.0272",
        "0.0344",
        "0.0331",
        "0.0292",
        "0.0334",
        "0.0360",
    ),
    vector_shown=(54_901, 8_109, 7_311, 1_956, 1_251, 1_028, 884, 844),
    vector_cells=14,
    vector_entropy="1.5873",
    vector_gain="0.1063",
    bunud_code_lengths=(1, 2, 3, 5, 5, 8),
    bunud_codes=("1", "00", "011", "01010", "01000", "01011101"),
    bunud_huffman="1.7379",
    asalib_names=("استفهام", "استثناء", "نداء", "قسم", "تحذير", "مدح"),
    asalib_counts=(894, 848, 366, 41, 24, 19),
    asalib_entropy="1.7270",
    asalib_huffman="1.8554",
    asalib_by_frequency="1.8641",
    asalib_by_book="6.2172",
    asalib_book_ranks=(7, 6, 5, 8, 2, 4),
    asalib_code_lengths=(1, 2, 3, 4, 5, 5),
    debts=(
        (
            "مواضعُ التزاحم غيرُ المطبوعة",
            "التسجيلُ يعلن أنّ وسمَ الاستفهام ٩٠٢ والتشغيلُ ينشر ٨٩٤؛ "
            "فثمانيةُ مواضعَ صُرِفت في التزاحم ولم يُطبَع عددُها",
        ),
        (
            "أعدادُ وسوم الاستثناء لا تجمع إلى المنشور",
            "التسجيلُ يعلن RES ٥٥٧ وEXP ١٠٢ وغير ١٤٧ وسوى ١٤ وخلا ٢٥ "
            "ومجموعُها ٨٤٥، والتشغيلُ ينشر ٨٤٨ — وثلاثةٌ بلا بيان",
        ),
        (
            "ستُّ خاناتٍ من أربعَ عشرةَ غيرُ منشورة",
            "جردُ المتّجه ينشر ثمانيَ خاناتٍ تحمل ٧٦٬٢٨٤، وتبقى ١٬١٤٥ "
            "كلمةً في ستٍّ لا تُعرَف أنصبتُها، فلا تُعاد H إلّا بحدّين",
        ),
        (
            "بندُ العموم مُشغَّلٌ بوسم DET وحدَه",
            "والتسجيلُ يعلنه أخشنَ تشغيلٍ في الثمانية؛ والكتابُ يشترط "
            "دخولَ أل على الجمع واسم الجنس، فالعددُ حدٌّ أعلى لا قياس",
        ),
        (
            "المقامُ غيرُ مقام هذه الشجرة",
            "٧٧٬٤٢٩ كلمةً و٦٬٢٠٨ آيةً، مقابلَ ٧٨٬٢٤٥ و٦٬٢٣٦ ههنا؛ "
            "وفضُّ الفرق يحتاج حدَّ اللفظ وحدَّ الآية ثَمَّ وليسا مُودَعين",
        ),
    ),
)


def record_bytes(record: ForeignLedger = FROZEN_FOREIGN) -> bytes:
    """تسلسلٌ قانونيٌّ للحقول؛ وترتيبُها ترتيبُ تعريفها لا ترتيبُ الهجاء."""

    rows = [
        f"{one.name}{_FIELD_SEPARATOR}{getattr(record, one.name)}"
        for one in fields(record)
    ]
    return _RECORD_SEPARATOR.join(rows).encode("utf-8")


def rederive_record_digest(record: ForeignLedger = FROZEN_FOREIGN) -> str:
    """بصمةُ السجلّ مُشتَقّةً من حقوله؛ وتبديلُ حقلٍ يُغيّرها."""

    return hashlib.sha256(record_bytes(record)).hexdigest()


RECORD_DIGEST: Final[str] = rederive_record_digest()
"""ختمُ سجلّ الأنبوب الخارجيّ؛ وبه يُستشهَد بدل النثر."""


def verify_against_logs(record: ForeignLedger = FROZEN_FOREIGN) -> list[str]:
    """يُعاد اشتقاقُ كلِّ حقلٍ من الملفّات المُودَعة؛ وما خالف يُسمّى."""

    complaints: list[str] = []
    for name in (BUNUD_OUT, ASALIB_OUT, ASALIB_PRED):
        if not (DEPOSITS / name).is_file():
            complaints.append(f"ملفٌّ مُودَعٌ غائب: {name}")
    if complaints:
        return complaints
    bunud = (DEPOSITS / BUNUD_OUT).read_text(encoding="utf-8")
    asalib = (DEPOSITS / ASALIB_OUT).read_text(encoding="utf-8")
    if f"**{record.stand_words}** كلمة" not in bunud:
        complaints.append("المقامُ لا يطابق ملفَّ البنود")
    if f"**{record.stand_words}** كلمة" not in asalib:
        complaints.append("المقامُ لا يطابق ملفَّ الأساليب")
    if f"الآيات {record.stand_verses}" not in asalib:
        complaints.append("عددُ الآيات لا يطابق ملفَّ الأساليب")
    for index, name in enumerate(record.bunud_names):
        count = record.bunud_counts[index]
        if not re.search(rf"ب\d {re.escape(name)}\s+{count}\s", bunud):
            complaints.append(f"{name}: لا شاهدَ في الملفّ لعدده")
        if f"H(البتّ) = {record.bunud_entropies[index]} بت" not in bunud:
            complaints.append(f"{name}: لا شاهدَ في الملفّ لإنتروبيته")
        if f"+{record.bunud_gains[index]}" not in bunud:
            complaints.append(f"{name}: لا شاهدَ في الملفّ لكسبه")
    if f"**H(المتّجه) = {record.vector_entropy}**" not in bunud:
        complaints.append("H(المتّجه) لا شاهدَ لها")
    if f"+{record.vector_gain}" not in bunud:
        complaints.append("كسبُ المتّجه لا شاهدَ له")
    if f"**{record.vector_cells}** من" not in bunud:
        complaints.append("عددُ الخانات المشغولة لا شاهدَ له")
    for count in record.vector_shown:
        if not re.search(rf"[01]{{8}}\s+{count}\s", bunud):
            complaints.append(f"خانةُ {count} لا شاهدَ لها")
    for index, name in enumerate(record.asalib_names):
        if not re.search(
            rf"{re.escape(name)}\s+{record.asalib_counts[index]}\s", asalib
        ):
            complaints.append(f"{name}: لا شاهدَ في الملفّ لعدده")
    for value, label in (
        (record.asalib_entropy, "حدُّ شانون  H"),
        (record.asalib_huffman, "شجرةُ هافمان (المثلى)"),
        (record.asalib_by_frequency, "شجرةُ الترتيب التكراريّ (فحصٌ خطّيّ)"),
        (record.asalib_by_book, "شجرةُ الكتاب (فحصٌ خطّيٌّ بترتيب فصوله)"),
    ):
        if value not in asalib:
            complaints.append(f"{label}: لا شاهدَ في الملفّ لقيمته")
    return complaints
