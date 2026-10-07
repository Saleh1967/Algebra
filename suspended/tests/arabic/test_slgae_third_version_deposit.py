"""النسخةُ الثالثة: ثلاثُ بصماتٍ متمايزة، ومعرِّفٌ متصادم، وفحوصٌ على المنشور.

يُثبِت هذا الاختبارُ ثمانيةَ أشياء: أنّ النسخَ الثلاثَ مُودَعةٌ ببصماتٍ متمايزةٍ
مقروءةٍ من ملفّاتها، وأنّ عددَ مواضع الرقم والمعرِّف يُقرأ من بايتات الملفّ لا
يُكتَب، وأنّ التجربتين لا تشتركان في اسمِ اختبارٍ واحد فافتراقُهما بنيويّ،
وأنّ إحصاءاتِ القسمين متّسقةٌ بعضُها مع بعض، وأنّ ترتيبَ V3 سقط **وليس معكوسَ
المتوقَّع**، وأنّ جسرَي الحلق يتّفقان اتّجاهًا ويفترقان مقدارًا بفارقٍ محسوب،
وأنّ الأرجحيّةَ تُظهِر من الفارق ما تُخفيه النسبة، وأنّ مقابلةَ ترتيبين على
فئتين مختلفتين تُرَدّ.

ويُثبِت معها أنّ التصادمَ **أُغلق تسميةً لا تصحيحًا**: لكلّ قسمٍ معرِّفٌ متمايزٌ
واردٌ في وثيقة التمييز ومقروءٌ من بايتاتها، وأنّ العددَ في المُودَع بقي اثنين،
وأنّ الإحالةَ القديمةَ تتعيّن باسم اختبارها وما لا يتعيّن يُرَدّ، وأنّ إعادةَ
المعرِّف المتصادم اسمًا مُميَّزًا مردودةٌ بالبناء.
"""

from __future__ import annotations

import hashlib

import pytest

from alghanem.arabic.slgae_deposit import SlgaeDepositError
from alghanem.arabic.slgae_third_version_deposit import (
    COLLIDING_IDENTIFIER,
    COLLIDING_SECTION_NUMBER,
    THIRD_VERSION_EXPERIMENTS,
    V3_PREDICTED_ORDER,
    OrderingCheck,
    SectionExperiment,
    derive_bridge_gap,
    derive_identifier_collision,
    derive_ordering_check,
    derive_statistic_checks,
    disambiguation_digest,
    disambiguation_path,
    resolve_colliding_citation,
    slgae_v3_digest,
    slgae_v3_path,
    version_chain_digests,
)


def test_the_three_versions_are_deposited_with_distinct_digests() -> None:
    """النسخُ الثلاثُ مُودَعةٌ معًا، وبصماتُها مقروءةٌ من الملفّات ومتمايزة."""

    chain = version_chain_digests()

    assert len(chain) == 3
    assert len({digest for _path, digest in chain}) == 3
    assert slgae_v3_digest() == hashlib.sha256(slgae_v3_path().read_bytes()).hexdigest()


def test_the_collision_is_counted_from_the_bytes_not_written() -> None:
    """عددُ مواضع الرقم والمعرِّف يُقرأ من الملفّ، والتصادمُ مُشتَقٌّ منه."""

    collision = derive_identifier_collision()
    text = slgae_v3_path().read_text(encoding="utf-8")

    assert collision.identifier == COLLIDING_IDENTIFIER
    assert collision.section_number == COLLIDING_SECTION_NUMBER
    assert collision.heading_occurrences == 2
    assert collision.identifier_occurrences == text.count(COLLIDING_IDENTIFIER) == 2
    assert collision.is_a_collision


def test_the_two_experiments_share_no_test_name() -> None:
    """التجربتان تحت معرِّفٍ واحدٍ ولا تشتركان في اسمِ اختبارٍ واحد."""

    collision = derive_identifier_collision()
    first, second = THIRD_VERSION_EXPERIMENTS

    assert collision.shared_test_names == ()
    assert first.test_names == ("P1", "P2", "P3")
    assert second.test_names == ("V0", "V1", "V2", "V3")
    assert first.data != second.data


def test_the_published_statistics_are_internally_consistent() -> None:
    """إحصاءاتُ القسمين يصدّق بعضُها بعضًا: F والعتبةُ وp، وARI، والنقاء."""

    checks = derive_statistic_checks()

    assert len(checks) == 3
    assert all(check.holds for check in checks)
    assert all(check.detail.strip() for check in checks)


def test_the_failed_order_is_not_the_reverse_of_the_prediction() -> None:
    """ترتيبُ V3 سقط، والمرصودُ ليس معكوسَ المتوقَّع أيضًا."""

    check = derive_ordering_check()

    assert check.predicted == V3_PREDICTED_ORDER
    assert check.observed == ("لساني", "خيشومي", "أسناني")
    assert not check.matches_prediction
    assert not check.is_exact_reverse


def test_the_two_bridges_agree_in_direction_and_differ_in_magnitude() -> None:
    """الجسران يجرّان الفتحَ معًا، ويفترقان مقدارًا بفارقٍ محسوبٍ لا موصوف."""

    gap = derive_bridge_gap()

    assert gap.first_with > gap.first_without
    assert gap.second_with > gap.second_without
    assert gap.first_ratio == pytest.approx(1.148, abs=0.001)
    assert gap.second_ratio == pytest.approx(4.765, abs=0.001)
    assert gap.ratio_gap == pytest.approx(4.15, abs=0.01)


def test_the_odds_ratio_shows_what_the_plain_ratio_hides() -> None:
    """الأرجحيّةُ تُظهِر فارقًا أكبرَ ممّا تُظهِره النسبةُ وحدَها."""

    gap = derive_bridge_gap()

    assert gap.first_odds_ratio == pytest.approx(1.39, abs=0.01)
    assert gap.second_odds_ratio == pytest.approx(20.81, abs=0.01)
    assert gap.odds_ratio_gap > gap.ratio_gap
    assert gap.odds_ratio_gap == pytest.approx(15.0, abs=0.1)


def test_two_orders_over_different_categories_are_refused() -> None:
    """مقابلةُ ترتيبين لا يشتركان في أعضائهما تُرَدّ، ولا تُحمَل على أقربهما."""

    with pytest.raises(SlgaeDepositError, match="فئتين مختلفتين"):
        OrderingCheck(
            predicted=("أ", "ب"),
            observed=("ب", "ج"),
            matches_prediction=False,
            is_exact_reverse=False,
        )


def test_each_section_carries_a_distinct_identifier_after_the_closure() -> None:
    """التمييزُ أعطى كلَّ قسمٍ اسمًا؛ والمعرِّفان متمايزان ولا أحدَ منهما المتصادم."""

    first, second = THIRD_VERSION_EXPERIMENTS

    assert first.assigned_identifier == "MAKHRAJ-INHERITS-VOWELS-AR-1"
    assert second.assigned_identifier == "VOWEL-FIRST-BIRTH-CHAIN-AR-1"
    assert first.assigned_identifier != second.assigned_identifier
    assert COLLIDING_IDENTIFIER not in {
        first.assigned_identifier,
        second.assigned_identifier,
    }


def test_the_closure_is_read_from_the_document_bytes_not_written_here() -> None:
    """المعرِّفان واردان في وثيقة التمييز، والإغلاقُ مُشتَقٌّ من بايتاتها."""

    collision = derive_identifier_collision()
    document = disambiguation_path().read_text(encoding="utf-8")

    assert collision.closing_identifiers_in_document == collision.assigned_identifiers
    assert all(identifier in document for identifier in collision.assigned_identifiers)
    assert (
        disambiguation_digest()
        == hashlib.sha256(disambiguation_path().read_bytes()).hexdigest()
    )
    assert collision.is_closed


def test_the_deposit_is_untouched_by_the_closure() -> None:
    """الإغلاقُ تسميةٌ بعد اليوم: بايتاتُ المُودَع كما هي، والعددُ باقٍ اثنين."""

    collision = derive_identifier_collision()

    assert collision.is_a_collision
    assert collision.heading_occurrences == 2
    assert collision.identifier_occurrences == 2


def test_an_old_citation_is_resolved_by_the_test_name_beside_it() -> None:
    """الإحالةُ القديمةُ ناقصةٌ لا خاطئة: اسمُ الاختبار يعيّن قسمَها."""

    first, second = THIRD_VERSION_EXPERIMENTS

    assert resolve_colliding_citation("P1") is first
    assert resolve_colliding_citation("v0") is second
    assert resolve_colliding_citation(" V3 ") is second


def test_a_citation_that_names_no_test_is_refused_not_guessed() -> None:
    """ما لا يتعيّن يُرَدّ، ولا يُحمَل على أقرب القسمين."""

    with pytest.raises(SlgaeDepositError, match="لا تُخمَّن"):
        resolve_colliding_citation("")

    with pytest.raises(SlgaeDepositError, match="لا تُخمَّن"):
        resolve_colliding_citation("P9")


def test_reusing_the_colliding_identifier_as_a_distinct_name_is_refused() -> None:
    """إعادةُ المعرِّف المتصادم اسمًا مُميَّزًا تُبقي التصادمَ فتُرَدّ بالبناء."""

    with pytest.raises(SlgaeDepositError, match="المعرِّفُ المتصادمُ نفسُه"):
        SectionExperiment(
            title="قسمٌ",
            data="بيانٌ",
            test_names=("P1",),
            verdict="حكمٌ",
            assigned_identifier=COLLIDING_IDENTIFIER,
        )

    with pytest.raises(SlgaeDepositError, match="معرِّفٍ مُميَّز"):
        SectionExperiment(
            title="قسمٌ",
            data="بيانٌ",
            test_names=("P1",),
            verdict="حكمٌ",
            assigned_identifier="   ",
        )
