"""يقرأ شرطَ رفع حاجز جدول الصفة، ويقيس قوّةَ فصلِ مرشَّحٍ يُمرَّر من خارج الشجرة.

الاستعمال:

    python examples/arabic/measure_sifa_candidate.py [مسارُ ملفّ المرشَّح]

وملفُّ المرشَّح نصٌّ بترميز UTF-8، في كلّ سطرٍ حرفٌ ثمّ جدولةٌ ثمّ صفاتُه
مفصولةً بفاصلة، بأسمائها كما نطق بها المصدر:

    ط\tمجهورة,شديدة,مطبقة

ولا يُودَع الملفُّ بقراءته: القياسُ قياسٌ، والإيداعُ يحتاج نسبةً كاملةً بجزئها
وصفحتها. ومن غير مسارٍ يُطبَع تقريرُ الشرط وحدَه.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from alghanem.arabic.sifa_table_deposit import (  # noqa: E402
    DEPOSITED_SIFA_TABLES,
    SIFA_TABLE_NAMED_RESIDUALS,
    CandidateSifaTable,
    barrier_lift_report,
    separation_over,
)

_FIELD_SEPARATOR: str = "\t"
_FEATURE_SEPARATOR: str = ","


def read_candidate(path: Path) -> CandidateSifaTable:
    """اقرأ مرشَّحًا من ملفّ؛ وسطرٌ خارجَ الشكل يُرَدُّ بموضعه لا يُتجاوَز."""

    rows: list[tuple[str, tuple[str, ...]]] = []
    for number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        stripped = line.strip()
        if not stripped:
            continue
        if _FIELD_SEPARATOR not in stripped:
            raise SystemExit(f"سطر {number}: لا جدولةَ فيه بين الحرف وصفاته.")
        letter, raw = stripped.split(_FIELD_SEPARATOR, 1)
        features = tuple(
            part.strip() for part in raw.split(_FEATURE_SEPARATOR) if part.strip()
        )
        rows.append((letter.strip(), features))
    return CandidateSifaTable(rows=tuple(rows))


def print_barrier_report() -> None:
    report = barrier_lift_report()
    print(f"منزلةُ الحاجز: {report.standing.value}")
    print(f"الجداولُ المُودَعة: {report.deposits}")
    print(f"السؤالُ المفتوح: {report.open_question_identifier}")
    print()
    for condition in report.conditions:
        mark = "مستوفًى" if condition.is_met else "باقٍ"
        print(f"[{mark}] {condition.requirement}")
        print(f"        يستوفيه: {condition.what_satisfies_it}")
    print()
    print(f"شرطُ الرفع مستوفًى: {'نعم' if report.condition_is_met else 'لا'}")


def print_separation(candidate: CandidateSifaTable) -> None:
    report = separation_over(candidate)
    print()
    print(f"بصمةُ المرشَّح = {report.candidate_digest}")
    print(
        f"معلَّقٌ قبل الصفات: {report.letters_unresolved_before}، "
        f"وبعدها: {report.letters_unresolved_after}، "
        f"وكسبُ الفصل: {report.separation_gain}"
    )
    print(
        f"الخاناتُ المُغلَقة: {report.classes_closed}، "
        f"والباقيةُ مفتوحةً: {report.classes_open}"
    )
    print()
    print("الخانة | حروفُها | ما انفرد | ما بقي متعادلًا")
    print("-" * 70)
    for row in report.per_class:
        tied = " / ".join("".join(group) for group in row.tied_groups) or "—"
        separated = " ".join(row.separated_letters) or "—"
        print(f"{row.makhraj_rank:>2} | {' '.join(row.letters)} | {separated} | {tied}")
    print()
    print("والقياسُ قياسٌ: لم يُودَع هذا المرشَّحُ ولم تُنسَب إليه طبعة.")


def main() -> None:
    print_barrier_report()
    if len(sys.argv) > 2:
        raise SystemExit("مسارٌ واحدٌ للمرشَّح لا أكثر.")
    if len(sys.argv) == 2:
        print_separation(read_candidate(Path(sys.argv[1])))
    else:
        print()
        print("لا مسارَ مرشَّحٍ مُمرَّر: طُبِع تقريرُ الشرط وحدَه.")
    print()
    print(f"الجداولُ المُودَعة في الشجرة: {len(DEPOSITED_SIFA_TABLES)}")
    for note in SIFA_TABLE_NAMED_RESIDUALS:
        print(note)


if __name__ == "__main__":
    main()
