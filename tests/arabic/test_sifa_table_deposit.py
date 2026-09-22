"""عقدُ إيداعِ جدول الصفة: شروطٌ مبنيّةٌ، وقياسُ فصلٍ يُشغَّل، وعقدٌ باقٍ فارغًا.

**ولا صفةَ عربيّةً واحدةً في هذا الملفّ**: مرشَّحاتُ الاختبار مبنيّةٌ آليًّا من
نقاط اليونيكود — لا من صوتيّات العربيّة — لأنّ جدولًا يُكتَب في جلسةٍ هو ما
قام الحاجزُ ليمنعه. فهي شواهدُ على **آلة القياس** لا على اللغة، ولا يُقرأ
منها حرفٌ واحدٌ خبرًا عن صفةٍ من صفاته.

يُثبِت هذا الاختبارُ تسعةَ أشياء: أنّ العقدَ يرفض مرشَّحًا ناقصَ التغطية أو
مكرَّرَ الحرف أو ذا حرفٍ غيرِ مرقَّمٍ أو صفٍّ فارغ، وأنّ مرشَّحًا لا يفرّق
يُخرِج كسبًا صفرًا، وأنّ مرشَّحًا يفرّق كلَّ حرفٍ يُغلِق الخانات كلَّها بكسب
عشرين، وأنّ بينهما درجةً تُقاس لا تُوصَف، وأنّ الإيداعَ يرفض نسبةً ناقصةً
وتصريحًا فارغًا، وأنّ البصمةَ تُعاد اشتقاقًا فتتحرّك بتحرّك البايتات، وأنّ
`DEPOSITED_SIFA_TABLES` فارغةٌ والحاجزَ قائمٌ وشرطَ الرفع غيرَ مستوفًى.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.classical_makharij_table import CLASSICAL_ORDINAL
from alghanem.arabic.gflk_feature_table_import_barrier import ImportBarrierStanding
from alghanem.arabic.makharij_edition_citation import (
    EditionCitation,
    MakharijEditionError,
)
from alghanem.arabic.sifa_table_deposit import (
    DEPOSITED_SIFA_TABLES,
    SIFA_OPEN_QUESTION_IDENTIFIER,
    CandidateSifaTable,
    DepositedSifaTable,
    SifaTableError,
    barrier_lift_report,
    separation_over,
    sifa_barrier_standing,
)

_RANKED_LETTERS: tuple[str, ...] = tuple(sorted(CLASSICAL_ORDINAL))


def _degenerate_candidate() -> CandidateSifaTable:
    """مرشَّحٌ آليٌّ يعطي كلَّ حرفٍ الصفةَ نفسَها: لا يفرّق شيئًا."""

    return CandidateSifaTable(
        rows=tuple((letter, ("صفةٌ واحدةٌ للجميع",)) for letter in _RANKED_LETTERS)
    )


def _total_candidate() -> CandidateSifaTable:
    """مرشَّحٌ آليٌّ يعطي كلَّ حرفٍ صفةً من نقطته: يفرّق كلَّ حرف."""

    return CandidateSifaTable(
        rows=tuple((letter, (f"نقطة-{ord(letter):04X}",)) for letter in _RANKED_LETTERS)
    )


def _parity_candidate() -> CandidateSifaTable:
    """مرشَّحٌ آليٌّ يقسم على زوجيّة النقطة: يفرّق بعضًا ويترك بعضًا."""

    return CandidateSifaTable(
        rows=tuple(
            (letter, (f"زوجيّة-{ord(letter) % 2}",)) for letter in _RANKED_LETTERS
        )
    )


def _citation() -> EditionCitation:
    return EditionCitation(
        work_title="عنوانٌ للاختبار",
        editor="محقّقٌ للاختبار",
        publisher="ناشرٌ للاختبار",
        edition_year="سنةٌ للاختبار",
        volume="جزءٌ للاختبار",
        page="صفحةٌ للاختبار",
        deposited_quotation="مُقتبَسٌ للاختبار",
    )


def test_a_candidate_outside_its_condition_is_refused() -> None:
    """التغطيةُ التامّةُ شرطُ بناءٍ: النقصُ والتكرارُ والدخيلُ والفراغُ تُرَدّ."""

    with pytest.raises(SifaTableError, match="بلا صفّ"):
        CandidateSifaTable(rows=tuple((c, ("س",)) for c in _RANKED_LETTERS[:-1]))
    with pytest.raises(SifaTableError, match="في صفَّين"):
        CandidateSifaTable(
            rows=(*((c, ("س",)) for c in _RANKED_LETTERS), (_RANKED_LETTERS[0], ("ص",)))
        )
    with pytest.raises(SifaTableError, match="لا رتبةَ له"):
        CandidateSifaTable(
            rows=(*((c, ("س",)) for c in _RANKED_LETTERS), ("ا", ("ص",)))
        )
    with pytest.raises(SifaTableError, match="بلا صفةٍ واحدة"):
        CandidateSifaTable(
            rows=tuple(
                (c, () if c == _RANKED_LETTERS[0] else ("س",)) for c in _RANKED_LETTERS
            )
        )


def test_a_candidate_that_separates_nothing_gains_nothing() -> None:
    """مرشَّحٌ بصفةٍ واحدةٍ للجميع يُبقي العشرين معلَّقةً، وكسبُه صفر."""

    report = separation_over(_degenerate_candidate())

    assert report.letters_unresolved_before == 20
    assert report.letters_unresolved_after == 20
    assert report.separation_gain == 0
    assert report.classes_closed == 0
    assert report.classes_open == 8
    assert not report.closes_every_class


def test_a_candidate_that_separates_every_letter_closes_every_class() -> None:
    """مرشَّحٌ بصفةٍ لكلّ حرفٍ يُغلِق الخانات الثماني، وكسبُه عشرون."""

    report = separation_over(_total_candidate())

    assert report.letters_unresolved_after == 0
    assert report.separation_gain == 20
    assert report.classes_open == 0
    assert report.classes_closed == 8
    assert report.closes_every_class


def test_a_partial_candidate_is_measured_not_described() -> None:
    """بين الطرفين درجةٌ تُقاس: كسبٌ فوق الصفر ودون العشرين، وخاناتٌ باقية."""

    report = separation_over(_parity_candidate())

    assert 0 < report.separation_gain < 20
    assert report.classes_open > 0
    assert report.letters_unresolved_after == sum(
        len(group) for row in report.per_class for group in row.tied_groups
    )


def test_each_class_row_counts_every_letter_once() -> None:
    """كلُّ حرفٍ في الخانة إمّا منفردٌ وإمّا في تعادلٍ، ولا يُعَدُّ مرّتين."""

    for row in separation_over(_parity_candidate()).per_class:
        counted = len(row.separated_letters) + sum(
            len(group) for group in row.tied_groups
        )
        assert counted == len(row.letters)
        assert row.is_closed == (not row.tied_groups)


def test_a_deposit_without_a_full_citation_or_declaration_is_refused() -> None:
    """النسبةُ الناقصةُ تُرَدُّ في نوعها، والتصريحُ الفارغُ يُرَدُّ في الإيداع."""

    with pytest.raises(MakharijEditionError, match="الصفحة"):
        EditionCitation(
            work_title="عنوان",
            editor="محقّق",
            publisher="ناشر",
            edition_year="سنة",
            volume="جزء",
            page="   ",
            deposited_quotation="مُقتبَس",
        )
    with pytest.raises(SifaTableError, match="تصريحُ النسبة"):
        DepositedSifaTable(
            citation=_citation(),
            table=_total_candidate(),
            attribution_declaration="  ",
        )


def test_the_digest_is_rederived_and_moves_with_the_bytes() -> None:
    """البصمةُ تُشتَقّ من البايتات عند كلّ نداء، فتختلف باختلاف الصفوف."""

    deposit = DepositedSifaTable(
        citation=_citation(),
        table=_total_candidate(),
        attribution_declaration="جدولٌ منسوبٌ إلى مصدره، وليس دعوى هذه الشجرة.",
    )

    assert deposit.rederive_table_digest() == deposit.rederive_table_digest()
    assert (
        deposit.rederive_table_digest()
        != _degenerate_candidate().rederive_table_digest()
    )
    assert deposit.as_canonical_content()["table_digest"] == (
        deposit.rederive_table_digest()
    )


def test_no_sifa_table_has_reached_this_tree() -> None:
    """العقدُ مبنيٌّ والإيداعُ فارغ: لم تصل صفحةُ طبعةٍ بعينها."""

    assert DEPOSITED_SIFA_TABLES == ()


def test_the_barrier_stands_and_its_lift_condition_is_not_met() -> None:
    """شرطُ الرفع غيرُ مستوفًى بنودًا، والمنزلةُ مقروءةٌ من موضعها لا منسوخة."""

    report = barrier_lift_report()

    assert report.standing is ImportBarrierStanding.OPEN
    assert sifa_barrier_standing() is ImportBarrierStanding.OPEN
    assert report.deposits == 0
    assert not report.condition_is_met
    assert not any(condition.is_met for condition in report.conditions)
    assert report.open_question_identifier == SIFA_OPEN_QUESTION_IDENTIFIER
