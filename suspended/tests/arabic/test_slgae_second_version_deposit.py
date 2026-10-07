"""النسخةُ الثانية: بصمتان متمايزتان، ومراتبُ مُسجَّلة، وجدولٌ لا يُعيد بناءَ نفسه.

يُثبِت هذا الاختبارُ تسعةَ أشياء: أنّ النسختين مُودَعتان ببصمتين متمايزتين
مقروءتين من ملفَّيهما، وأنّ مراتبَ الادّعاء الأربعَ كلَّها مُسجَّلةٌ وأنّ
قائمةَ الصوامت في مرتبة «اختيار مني»، وأنّ موضعَ تغيّرٍ بلا فرقٍ يُرَدّ، وأنّ
«لا مشاهدة» تُسجَّل بغياب القيمة لا بصفر، وأنّ λ المنشورةَ لا تقع في مجال
تقريبها في المستويات الثلاثة المفحوصة، وأنّ `γ/β` تُحسَب في مستويين ويتعذّر
في مستويين بسببَين مُسمّيَين، وأنّ المحسوبَين لا يبلغان 1.55 المذكورة، وأنّ
رتابةَ العمودين — وهي دعوى الوثيقة نفسها — تصمد بالفحص، وأنّ حسابَ الحصاد
يوزّع المستوياتِ بلا بقيّة.
"""

from __future__ import annotations

import hashlib
import math

import pytest

from alghanem.arabic.slgae_deposit import SlgaeDepositError
from alghanem.arabic.slgae_second_version_deposit import (
    CLAIM_TIERS,
    MARKOV_LEVELS,
    REPORTED_GAMMA_OVER_BETA,
    SECOND_VERSION_AMENDMENTS,
    ClaimTier,
    MarkovLevelRow,
    VersionAmendment,
    both_version_digests,
    derive_lambda_reconstructions,
    derive_ratio_checks,
    markov_audit,
    slgae_v2_digest,
    slgae_v2_path,
)


def test_both_versions_are_deposited_with_distinct_digests() -> None:
    """النسختان مُودَعتان معًا، وبصمتاهما مقروءتان من الملفَّين ومتمايزتان."""

    digests = both_version_digests()

    assert len(digests) == 2
    assert digests[0][1] != digests[1][1]
    assert slgae_v2_digest() == hashlib.sha256(slgae_v2_path().read_bytes()).hexdigest()


def test_all_four_tiers_are_recorded_as_the_author_named_them() -> None:
    """المراتبُ الأربعُ مُسجَّلةٌ، وقائمةُ الصوامت في «اختيار مني»."""

    tiers = {claim.tier for claim in CLAIM_TIERS}

    assert tiers == set(ClaimTier)
    choice = next(
        claim for claim in CLAIM_TIERS if claim.tier is ClaimTier.AUTHORS_CHOICE
    )
    assert "الصوامت الـ26" in choice.claim


def test_an_amendment_without_a_difference_is_refused() -> None:
    """لا يُسجَّل تغيّرٌ حيث لا تغيّر، وكلُّ موضعٍ مُسجَّلٍ يحمل فرقًا."""

    with pytest.raises(SlgaeDepositError, match="لا يُسجَّل تغيّرٌ حيث لا تغيّر"):
        VersionAmendment(
            locus="موضع",
            first_version_said="النصُّ نفسُه",
            second_version_says="النصُّ نفسُه",
            what_the_tree_reads="لا شيء",
        )

    assert len(SECOND_VERSION_AMENDMENTS) == 5
    for amendment in SECOND_VERSION_AMENDMENTS:
        assert amendment.first_version_said != amendment.second_version_says


def test_an_unobserved_cell_is_absent_not_zero() -> None:
    """«لا مشاهدة» غيابُ قيمةٍ لا صفرٌ، وخلطُهما يُدخِل رقمًا لم يُقَس."""

    anchor = MARKOV_LEVELS[0]

    assert anchor.identity_exp is None
    assert anchor.identity_is_unobserved

    with pytest.raises(SlgaeDepositError, match="لا مشاهدة"):
        MarkovLevelRow(
            level="مستوى",
            same_block_exp=0.5,
            identity_exp=0.0,
            reported_lambda=0.5,
            identity_is_unobserved=True,
        )


def test_the_published_lambda_is_not_reconstructible_from_the_table() -> None:
    """λ المنشورةُ خارجَ مجال تقريبها في المستويات الثلاثة المفحوصة."""

    reconstructions = derive_lambda_reconstructions()
    anchor = reconstructions[0]

    assert anchor.is_anchor
    assert math.isclose(anchor.derived, 1.0)

    checked = [item for item in reconstructions if not item.is_anchor]
    assert len(checked) == 3
    assert not any(item.reported_inside_interval for item in checked)


def test_the_ratio_is_computable_in_two_levels_and_named_in_two() -> None:
    """`γ/β` تُحسَب في مستويين، ويتعذّر في مستويين بسببَين مُسمّيَين."""

    checks = derive_ratio_checks()
    computable = [check for check in checks if check.value is not None]
    unavailable = [check for check in checks if check.value is None]

    assert len(computable) == 2
    assert len(unavailable) == 2
    assert "لا مشاهدة" in unavailable[0].unavailable_because
    assert "لا يُقسَم عليه" in unavailable[1].unavailable_because


def test_neither_computable_ratio_reaches_the_reported_constant() -> None:
    """المحسوبان دون 1.55 المذكورة، والفرقُ يُسجَّل ولا يُسمّى خطأ."""

    values = [check.value for check in derive_ratio_checks() if check.value is not None]

    assert REPORTED_GAMMA_OVER_BETA == 1.55
    assert all(value < REPORTED_GAMMA_OVER_BETA for value in values)
    assert all(abs(value - REPORTED_GAMMA_OVER_BETA) > 0.05 for value in values)


def test_the_documents_own_monotonicity_claims_hold() -> None:
    """دعوى الوثيقة: القوّةُ تتناقص رتيبًا وأثرُ الكتلة يتلاشى — تصمد بالفحص."""

    reading = markov_audit()

    assert reading.same_block_is_monotone_increasing
    assert reading.reported_lambda_is_monotone_decreasing


def test_the_audit_accounts_for_every_level_without_remainder() -> None:
    """المستوياتُ موزّعةٌ بلا بقيّة: مرساةٌ وداخلٌ وخارج، وحُسِب وتعذّر."""

    reading = markov_audit()

    assert reading.levels == len(MARKOV_LEVELS) == 4
    assert reading.anchor_levels == 1
    assert reading.lambdas_inside_rounding == 0
    assert reading.lambdas_outside_rounding == 3
    assert reading.ratio_levels_computable == 2
    assert reading.ratio_levels_unavailable == 2
