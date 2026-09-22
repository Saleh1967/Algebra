"""يعرض بصمتَي النسختين، ومراتبَ الادّعاء، ومواضعَ التقييد، وتدقيقَ جدول ماركوف."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from alghanem.arabic.slgae_second_version_deposit import (  # noqa: E402
    CLAIM_TIERS,
    MARKOV_LEVELS,
    REPORTED_GAMMA_OVER_BETA,
    SECOND_VERSION_AMENDMENTS,
    SLGAE_V2_NAMED_RESIDUALS,
    both_version_digests,
    derive_lambda_reconstructions,
    derive_ratio_checks,
    markov_audit,
)


def main() -> None:
    print("النسختان المُودَعتان:")
    for path, digest in both_version_digests():
        print(f"  {path}\n    {digest}")
    print()

    print("مراتبُ الادّعاء كما سمّاها صاحبُ الوثيقة:")
    for claim in CLAIM_TIERS:
        print(f"  [{claim.tier.value}] {claim.tier_meaning}")
    print()

    print(f"مواضعُ التقييد بين النسختين: {len(SECOND_VERSION_AMENDMENTS)}")
    for amendment in SECOND_VERSION_AMENDMENTS:
        print(f"  • {amendment.locus}")
        print(f"      الأولى: {amendment.first_version_said}")
        print(f"      الثانية: {amendment.second_version_says}")
    print()

    print("جدولُ ٥ي كما نُشر:")
    print("  المستوى | exp(β) | exp(γ) | λ المنشور")
    for row in MARKOV_LEVELS:
        identity = (
            "لا مشاهدة" if row.identity_exp is None else f"{row.identity_exp:.2f}"
        )
        print(
            f"  {row.level:<16} | {row.same_block_exp:>4.2f} | {identity:>9} | "
            f"{row.reported_lambda:>4.2f}"
        )
    print()

    print("إعادةُ بناء λ من عمود exp(β) بفرض λ(L1) = 1:")
    print("  المستوى | المنشور | المشتقّ | الفرق | مجالُ التقريب | داخله؟")
    for item in derive_lambda_reconstructions():
        verdict = (
            "مرساة"
            if item.is_anchor
            else ("نعم" if item.reported_inside_interval else "لا")
        )
        print(
            f"  {item.level:<16} | {item.reported:>5.2f} | {item.derived:>7.4f} | "
            f"{item.difference:+.4f} | [{item.interval_low:.4f}, "
            f"{item.interval_high:.4f}] | {verdict}"
        )
    print()

    print(f"قسمةُ γ/β (المذكورة في الوثيقة: {REPORTED_GAMMA_OVER_BETA}):")
    for check in derive_ratio_checks():
        value = (
            f"{check.value:.3f}"
            if check.value is not None
            else f"تعذّر — {check.unavailable_because}"
        )
        print(f"  {check.level:<16} {value}")
    print()

    reading = markov_audit()
    print(
        f"الحصاد: مستوياتٌ {reading.levels} = مرساةٌ {reading.anchor_levels} + "
        f"داخلَ المجال {reading.lambdas_inside_rounding} + خارجَه "
        f"{reading.lambdas_outside_rounding}"
    )
    print(
        f"قسمةُ γ/β: محسوبةٌ في {reading.ratio_levels_computable}، ومتعذّرةٌ في "
        f"{reading.ratio_levels_unavailable}"
    )
    print(
        f"رتابةُ exp(β) صاعدةً: {reading.same_block_is_monotone_increasing}؛ "
        f"ورتابةُ λ هابطةً: {reading.reported_lambda_is_monotone_decreasing}"
    )
    print()
    for note in SLGAE_V2_NAMED_RESIDUALS:
        print(note)


if __name__ == "__main__":
    main()
