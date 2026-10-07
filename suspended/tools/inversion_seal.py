"""تجميدُ الانقلاب: سجلٌّ واحدٌ يحمل الرصدَ والاشتقاقَ، ببصمةٍ تُعاد.

**العطلُ الذي يعالجه**: صار «انقلابُ الربح» يُذكَر **نثرًا** — «الأكثرُ
وقوعًا ليس الأكبرَ ربحًا»، «الترتيبُ معاكس». والنثرُ يتبدّل ولا يُعرَف
تبدّلُه، فيُستشهَد به بعد جلساتٍ كأنّه محسوم، أو يُنقَل رقمٌ منه بذيلٍ
مُختلَق كما وقع في العطل ١٦. فيُجمَع ههنا في **سجلٍّ مُقفَلٍ ببصمةٍ واحدة**.

`THE_RECORD_IS_REDERIVED_NOT_TRANSCRIBED`: وبصمةُ السجلّ **تُشتَقّ من
حقوله** عند كلّ تشغيل، فتبديلُ حقلٍ يُغيّرها ويُسقِط الفحص.

`EVERY_FIELD_IS_CHECKED_AGAINST_THE_DEPOSITED_LOGS`: وحقولُه كلُّها
**مقيسة**، لا موقَّعَ فيها؛ ويُعاد التحقّقُ منها في `verify_against_logs`
بمطابقة **نصّ السجلّات المُودَعة** حرفًا بحرف. فما لم يوجد في سجلٍّ
**لا يدخل السجلَّ المُقفَل**.

`THE_CLAIM_IS_ENFORCED_BY_THE_TYPE_NOT_BY_THE_PROSE`: والانقلابُ نفسُه
**شرطُ بناءٍ** لا وصفًا: لا يُقفَل سجلٌّ يكون فيه ارتباطُ العدد الخام أقوى
من ارتباط المشتَقّ، ولا يكون فيه وسيطُ الرتبة المختارة في النصف الأعلى،
ولا تختلف فيه `I` عن `Σ p·PMI`. **فمن بدّل رقمًا ليُلطّف النتيجةَ رُدَّ
سجلُّه**، ومن بدّله ليُصحّحه تبدّلت بصمتُه وظهر التبديل.

**ولا اسمَ لغويٌّ يدخل**: بتّاتٌ ووقوعاتٌ ورتبٌ وارتباطات.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, fields
from fractions import Fraction
from pathlib import Path
from typing import Final

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[1]
DEPOSITS: Final[Path] = REPOSITORY / "deposits"

_FIELD_SEPARATOR: Final[str] = "\x1f"
_RECORD_SEPARATOR: Final[str] = "\x1e"

ALGEBRA_LOG: Final[str] = "greedy_algebra_run.log"
RANKING_LOG: Final[str] = "measured_ranking_run.log"
RANK_LOG: Final[str] = "measured_ranking_rank.log"


class InversionSealError(ValueError):
    """رُدَّ سجلٌّ لا يحمل الانقلابَ، أو خالف السجلّاتِ في حقلٍ مقيس."""


@dataclass(frozen=True, slots=True)
class SealedInversion:
    """سجلُّ الانقلاب مُقفَلًا: ما رُصِد، وما اشتُقّ، وما يسعه ماركوف."""

    base_units: int
    corpus_units: int
    search_depth: int
    states: int
    rank_agreed: int
    choice_agreed: int
    median_chosen_rank: int
    edge_share: str
    median_count_chosen: int
    median_count_first: int
    pairs_looked: int
    rho_count: str
    rho_pmi: str
    rho_leading: str
    rho_derived: str
    rho_count_pmi: str
    sign_agreed: int
    threshold_agreed: int
    threshold_bits: str
    median_relative_error: str
    mutual_information: str
    sum_p_pmi: str
    adjacency_places: int
    first_order_ceiling: int
    block_saving: int
    ceiling_ratio: str
    stirling_low: str
    stirling_high: str

    def __post_init__(self) -> None:
        for one in fields(self):
            value = getattr(self, one.name)
            if isinstance(value, int) and value <= 0:
                raise InversionSealError(f"حقلٌ مقيسٌ غيرُ موجب: {one.name}.")
        if float(self.rho_derived) <= float(self.rho_count):
            raise InversionSealError(
                "لا يُقفَل سجلٌّ يكون فيه العددُ الخامُ أقربَ إلى الربح "
                "من المشتَقّ — فذاك نقضُ الانقلاب لا تسجيلُه."
            )
        if float(self.rho_leading) <= float(self.rho_count):
            raise InversionSealError("التقريبُ يجب أن يسبق العددَ الخام.")
        if float(self.rho_count_pmi) >= 0.25:
            raise InversionSealError(
                "الانقلابُ مشروطٌ باستقلالِ العدد عن الاقتران تقريبًا."
            )
        if self.mutual_information != self.sum_p_pmi:
            raise InversionSealError("`Σ p·PMI` هي `I` هويّةً، فلا تختلفان.")
        if self.median_chosen_rank * 2 <= self.search_depth:
            raise InversionSealError(
                "وسيطُ الرتبة المختارة في النصف الأدنى — فلا انقلابَ يُسجَّل."
            )
        if self.median_count_chosen >= self.median_count_first:
            raise InversionSealError("الربحُ الأكبرُ يجب أن يقع في الأندر.")
        if self.rank_agreed * 10 >= self.states:
            raise InversionSealError("توافقُ الرتبة أكبرُ من أن يُسمّى انقلابًا.")
        for named in ("sign_agreed", "threshold_agreed"):
            if int(getattr(self, named)) > self.pairs_looked:
                raise InversionSealError(f"موافقاتٌ تجاوز المقيس: {named}.")
        if Fraction(self.threshold_agreed, self.pairs_looked) < Fraction(8, 10):
            raise InversionSealError("عتبةُ الاقتران لا تُسجَّل دون أربعة أخماس.")
        if float(self.ceiling_ratio) <= 1:
            raise InversionSealError(
                "سجلُّ الانقلاب يحمل تجاوزَ الرتبة الأولى؛ ونسبةٌ دون الواحد "
                "خبرٌ آخرُ يُسجَّل بسجلٍّ آخر."
            )
        if not 0 < float(self.stirling_low) < float(self.stirling_high):
            raise InversionSealError("حدُّ ستيرلنغ موجبٌ ويتّسع، أو فالقياسُ عطل.")


FROZEN_INVERSION: Final[SealedInversion] = SealedInversion(
    base_units=112,
    corpus_units=364_747,
    search_depth=24,
    states=1_530,
    rank_agreed=27,
    choice_agreed=28,
    median_chosen_rank=22,
    edge_share="0.4500",
    median_count_chosen=236,
    median_count_first=405,
    pairs_looked=200,
    rho_count="0.1805",
    rho_pmi="0.9221",
    rho_leading="0.9655",
    rho_derived="0.9759",
    rho_count_pmi="0.1872",
    sign_agreed=187,
    threshold_agreed=190,
    threshold_bits="1.4427",
    median_relative_error="0.1997",
    mutual_information="1.303600",
    sum_p_pmi="1.303600",
    adjacency_places=358_511,
    first_order_ceiling=467_355,
    block_saving=824_618,
    ceiling_ratio="1.7644",
    stirling_low="0.001969",
    stirling_high="0.059482",
)


def record_bytes(record: SealedInversion = FROZEN_INVERSION) -> bytes:
    """تسلسلٌ قانونيٌّ للحقول؛ وترتيبُها ترتيبُ تعريفها لا ترتيبُ الهجاء."""

    rows = [
        f"{one.name}{_FIELD_SEPARATOR}{getattr(record, one.name)}"
        for one in fields(record)
    ]
    return _RECORD_SEPARATOR.join(rows).encode("utf-8")


def rederive_record_digest(record: SealedInversion = FROZEN_INVERSION) -> str:
    """بصمةُ السجلّ مُشتَقّةً من حقوله؛ وتبديلُ حقلٍ يُغيّرها."""

    return hashlib.sha256(record_bytes(record)).hexdigest()


RECORD_DIGEST: Final[str] = rederive_record_digest()
"""ختمُ سجلّ الانقلاب؛ وبه يُستشهَد بدل النثر."""


def _witness(name: str) -> str:
    path = DEPOSITS / name
    if not path.is_file():
        raise InversionSealError(f"سجلٌّ مُودَعٌ غائب: {name}.")
    return path.read_text(encoding="utf-8")


def verify_against_logs(record: SealedInversion = FROZEN_INVERSION) -> list[str]:
    """يُعاد اشتقاقُ كلِّ حقلٍ من السجلّات المُودَعة؛ وما خالف يُسمّى."""

    algebra = _witness(ALGEBRA_LOG)
    ranking = _witness(RANKING_LOG)
    ranks = _witness(RANK_LOG)
    wanted: list[tuple[str, str, str]] = [
        ("base_units", algebra, f"أبجديّة {record.base_units} "),
        ("corpus_units", algebra, f"L₀: {record.corpus_units} وحدةً"),
        ("search_depth", ranking, f"أعلى {record.search_depth} مقترَحٍ متاح"),
        (
            "states",
            ranking,
            f"توافقُ الرتبة الأولى: {record.rank_agreed} من {record.states}",
        ),
        (
            "choice_agreed",
            ranking,
            f"توافقُ القرار: {record.choice_agreed} من {record.states}",
        ),
        ("median_chosen_rank", ranks, f"وسيطُ الرتبة: {record.median_chosen_rank}"),
        (
            "median_count_chosen",
            ranks,
            f"«أكبرُ ربحًا»:  وسيطٌ {record.median_count_chosen}",
        ),
        (
            "median_count_first",
            ranks,
            f"«أوّلُ رابح»:  وسيطٌ {record.median_count_first}",
        ),
        ("pairs_looked", algebra, f"أزواجٌ مقيسة: {record.pairs_looked}"),
        ("rho_count", algebra, f"ρ(الوقوع، الربحِ المقيس)   = +{record.rho_count}"),
        ("rho_pmi", algebra, f"ρ(PMI، الربحِ المقيس)      = +{record.rho_pmi}"),
        (
            "rho_leading",
            algebra,
            f"ρ(التقريبِ، الربحِ المقيس) = +{record.rho_leading}",
        ),
        (
            "rho_derived",
            algebra,
            f"ρ(المشتَقّ، الربحِ المقيس)  = +{record.rho_derived}",
        ),
        (
            "rho_count_pmi",
            algebra,
            f"ρ(الوقوع، PMI)             = +{record.rho_count_pmi}",
        ),
        (
            "sign_agreed",
            algebra,
            f"توافقُ الإشارة: {record.sign_agreed} من {record.pairs_looked}",
        ),
        (
            "threshold_agreed",
            algebra,
            f"توافقٌ {record.threshold_agreed} من {record.pairs_looked}",
        ),
        ("threshold_bits", algebra, f"عتبةُ PMI > log₂e ({record.threshold_bits})"),
        (
            "median_relative_error",
            algebra,
            f"وسيطٌ {record.median_relative_error} | أدنى",
        ),
        (
            "mutual_information",
            algebra,
            f"I(Xₜ;Xₜ₊₁) = {record.mutual_information} بتًّا",
        ),
        ("sum_p_pmi", algebra, f"Σ p·PMI    = {record.sum_p_pmi}"),
        ("adjacency_places", algebra, f"مواضعُ الجوار {record.adjacency_places}"),
        (
            "first_order_ceiling",
            algebra,
            f"السقفُ من الرتبة الأولى {record.first_order_ceiling} بتًّا",
        ),
        ("block_saving", algebra, f"فالمُوفَّرُ: {record.block_saving} بتًّا"),
        (
            "ceiling_ratio",
            algebra,
            f"النسبةُ المُوفَّر ÷ السقف: {record.ceiling_ratio}",
        ),
        (
            "stirling_low",
            algebra,
            f"الفرقُ للرمز الواحد:            +{record.stirling_low}",
        ),
        ("stirling_high", algebra, f"للرمز +{record.stirling_high} |"),
    ]
    complaints = [
        f"{name}: لا شاهدَ في السجلّ لـ«{needle}»"
        for name, haystack, needle in wanted
        if needle not in haystack
    ]
    if not 0 < float(record.edge_share) < 1:
        complaints.append("edge_share: نصيبُ الحافّة خارجَ [٠، ١].")
    edge = 0.0
    for line in ranks.splitlines():
        hit = line.strip()
        for rank in (record.search_depth - 1, record.search_depth):
            if hit.startswith(f"رتبةُ {rank}:"):
                edge += float(hit.rsplit("(", 1)[1].rstrip(")"))
    if f"{edge:.4f}" != record.edge_share:
        complaints.append(
            f"edge_share: المُعاد اشتقاقُه {edge:.4f} والمسجَّلُ {record.edge_share}"
        )
    return complaints
