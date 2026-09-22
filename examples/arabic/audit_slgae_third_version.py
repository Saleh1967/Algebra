"""يعرض سلسلةَ النسخ الثلاث، وتصادمَ معرِّف ٥ك، وفحوصَ ما نُشر في قسمَيه."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from alghanem.arabic.slgae_third_version_deposit import (  # noqa: E402
    SLGAE_V3_NAMED_RESIDUALS,
    derive_bridge_gap,
    derive_identifier_collision,
    derive_ordering_check,
    derive_statistic_checks,
    version_chain_digests,
)


def main() -> None:
    print("سلسلةُ النسخ المُودَعة:")
    for index, (path, digest) in enumerate(version_chain_digests(), start=1):
        print(f"  {index}. {path}\n     {digest}")
    print()

    collision = derive_identifier_collision()
    print(
        f"تصادمُ المعرِّف {collision.identifier}: عناوينُ "
        f"«{collision.section_number}» = {collision.heading_occurrences}، "
        f"ومواضعُ المعرِّف = {collision.identifier_occurrences}"
    )
    print(f"اختباراتٌ مشتركةُ الاسم: {collision.shared_test_names or 'لا شيء'}")
    for experiment in collision.experiments:
        print(f"  • {experiment.title}")
        print(f"      البيان: {experiment.data}")
        print(f"      الاختبارات: {'، '.join(experiment.test_names)}")
        print(f"      الحكم: {experiment.verdict}")
    print()

    print("فحوصُ الإحصاءات المنشورة:")
    for check in derive_statistic_checks():
        mark = "متّسق" if check.holds else "غيرُ متّسق"
        print(f"  [{mark}] {check.what_was_checked}")
        print(f"          {check.detail}")
    print()

    order = derive_ordering_check()
    print(
        f"ترتيبُ V3: المتوقَّع {' ≥ '.join(order.predicted)}؛ "
        f"والمرصود {' > '.join(order.observed)}"
    )
    print(
        f"  مطابقٌ للمتوقَّع: {order.matches_prediction} | "
        f"معكوسُه تمامًا: {order.is_exact_reverse}"
    )
    print()

    gap = derive_bridge_gap()
    print("جسرُ «الحلقُ يجرّ الفتح» في القسمين:")
    print(
        f"  الأوّل: {gap.first_with} مقابل {gap.first_without} ← "
        f"نسبة {gap.first_ratio:.3f}، أرجحيّة {gap.first_odds_ratio:.2f}"
    )
    print(
        f"  الثاني: {gap.second_with} مقابل {gap.second_without} ← "
        f"نسبة {gap.second_ratio:.3f}، أرجحيّة {gap.second_odds_ratio:.2f}"
    )
    print(
        f"  الفجوة: ×{gap.ratio_gap:.2f} بالنسبة، و×{gap.odds_ratio_gap:.1f} "
        "بالأرجحيّة"
    )
    print()
    for note in SLGAE_V3_NAMED_RESIDUALS:
        print(note)


if __name__ == "__main__":
    main()
