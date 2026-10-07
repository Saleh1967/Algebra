"""تسجيلٌ مسبقٌ تحت المخرج: مانعٌ قائم، ومَسبارانِ بشرطَي إبطالهما، وعمقٌ غيرُ متساوٍ.

يُثبِت هذا الاختبارُ تسعةَ أشياء: أنّ التسجيلَ غيرُ قابلٍ للتشغيل اليومَ وأنّ
مصادرَ الإشارة فارغة، وأنّ الباقيَ المانعَ يحمل شرطَ رفعه، وأنّ كلَّ طورٍ يحمل
حدَّه «ما ليس هو» شرطَ إنشاء، وأنّ مسارَ الصامت يزيد طورًا واحدًا والزائدُ هو
مرشّحُ حدّ الإغلاق، وأنّ لكلّ مَسبارٍ شرطَ إبطالٍ يفارق شرطَ تأكيده، وأنّ
مَسبارًا بلا مُبطِلٍ يُرَدُّ عند الإنشاء، وأنّ ترتيبَ المواضع سبعةٌ هندسيّةٌ
لا اشتقاقٌ سببيّ، وأنّ رمزًا غيرَ مُسجَّلٍ يُرَدُّ لا يُحمَل على أقربه، وأنّ
الوحدةَ تُصرّح بألّا تُسمّى حزمة.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.pre_articulatory_preregistration import (
    BLOCKING_RESIDUAL,
    CONSTRICTION_GEOMETRY,
    DEPOSITED_SIGNAL_SOURCES,
    IT_IS_NOT_A_BUNDLE_NOTE,
    PRE_ARTICULATORY_CHAIN,
    PRE_ARTICULATORY_NAMED_RESIDUALS,
    PROBES,
    STRUCTURE_NAME,
    THE_TWO_PATHS_ARE_NOT_EQUALLY_DEEP_NOTE,
    Branch,
    ChainStage,
    MechanicalProbe,
    PreArticulatoryError,
    branch_depth_asymmetry,
    branch_stages,
    derive_branch_depths,
    is_testable_today,
    probe_named,
)


def test_nothing_here_can_be_run_today() -> None:
    """مصادرُ الإشارة فارغة، فلا شيءَ من هذا يُشغَّل؛ والمانعُ مُشتَقٌّ لا مكتوب."""

    assert DEPOSITED_SIGNAL_SOURCES == ()
    assert not is_testable_today()


def test_the_blocking_residual_carries_what_lifts_it() -> None:
    """باقٍ بلا شرطِ رفعٍ باقٍ يُرفَع متى شاء رافعُه، فالشرطُ مكتوبٌ معه."""

    assert BLOCKING_RESIDUAL.code == "NO_SIGNAL_HAS_REACHED_THIS_TREE"
    assert "لا بايتَ صوتٍ واحد" in BLOCKING_RESIDUAL.what_blocks
    assert "مُبصَّمة" in BLOCKING_RESIDUAL.what_lifts_it


def test_every_stage_carries_its_own_limit() -> None:
    """كلُّ طورٍ يحمل «ما ليس هو»؛ وطورٌ بلا حدٍّ يُرَدُّ عند الإنشاء."""

    assert len(PRE_ARTICULATORY_CHAIN) == 10
    assert all(stage.what_it_is_not.strip() for stage in PRE_ARTICULATORY_CHAIN)

    with pytest.raises(PreArticulatoryError, match="ما ليس هو الطور"):
        ChainStage(
            order=0,
            name="طور",
            what_it_is="شيء",
            what_it_is_not="   ",
            branch=Branch.SHARED,
        )


def test_the_consonant_path_is_one_stage_deeper() -> None:
    """الفرقُ طورٌ واحد، والزائدُ مرشّحُ حدّ الإغلاق بلا نظيرٍ صائتيّ."""

    depths = dict(derive_branch_depths())

    assert depths[Branch.VOCALIC] == 2
    assert depths[Branch.CONSONANTAL] == 3
    assert branch_depth_asymmetry() == 1
    assert "مرشّحُ حدّ الإغلاق" in THE_TWO_PATHS_ARE_NOT_EQUALLY_DEEP_NOTE

    names = [stage.name for stage in branch_stages(Branch.CONSONANTAL)]
    assert any("حدّ الإغلاق" in name for name in names)


def test_each_probe_separates_confirmation_from_falsification() -> None:
    """لكلّ مَسبارٍ شرطُ إبطالٍ غيرُ فارغٍ يفارق شرطَ تأكيده."""

    assert len(PROBES) == 2
    for probe in PROBES:
        assert probe.what_would_falsify.strip()
        assert probe.what_would_confirm.strip() != probe.what_would_falsify.strip()
        assert probe.instrument_required.strip()


def test_a_probe_without_a_falsifier_is_refused() -> None:
    """مَسبارٌ يُثبَّت مهما جاءت البياناتُ سؤالٌ لا اختبار، فيُرَدّ."""

    with pytest.raises(PreArticulatoryError, match="بلا شرطِ إبطال"):
        MechanicalProbe(
            symbol="س",
            name="مَسبار",
            question="سؤال",
            what_would_confirm="تأكيد",
            what_would_falsify="  ",
            instrument_required="أداة",
        )
    with pytest.raises(PreArticulatoryError, match="لا يفصلان"):
        MechanicalProbe(
            symbol="س",
            name="مَسبار",
            question="سؤال",
            what_would_confirm="النصُّ نفسُه",
            what_would_falsify="النصُّ نفسُه",
            instrument_required="أداة",
        )


def test_the_two_probes_ask_different_mechanical_questions() -> None:
    """الهمزةُ تسأل عن الإغلاق، والعينُ عن التضييق مع بقاء الجريان."""

    hamza = probe_named("ء")
    ain = probe_named("ع")

    assert "الإغلاق" in hamza.question
    assert "جاريًا" in ain.question or "الجريان" in ain.question
    assert hamza.what_would_falsify != ain.what_would_falsify

    with pytest.raises(PreArticulatoryError, match="لا مَسبارَ مُسجَّل"):
        probe_named("ب")


def test_the_place_order_is_seven_geometric_positions() -> None:
    """المواضعُ سبعةٌ مرتّبةٌ هندسيًّا من الحنجرة إلى الشفتين، بلا تكرار."""

    assert len(CONSTRICTION_GEOMETRY) == 7
    assert len(set(CONSTRICTION_GEOMETRY)) == 7
    assert CONSTRICTION_GEOMETRY[0] == "حنجريّ"
    assert CONSTRICTION_GEOMETRY[-1] == "شفويّ"


def test_the_structure_declines_the_name_bundle() -> None:
    """التسميةُ بنيةٌ ليفيّةٌ مرخَّصة، والسببُ أنّ التفاهةَ ليست البوّابة."""

    assert "حزمة" not in STRUCTURE_NAME
    assert "Licensed Phonetic Fiber Structure" in STRUCTURE_NAME
    assert "LocalTrivialityIsNotTheGate" in IT_IS_NOT_A_BUNDLE_NOTE
    assert len(PRE_ARTICULATORY_NAMED_RESIDUALS) == 9
