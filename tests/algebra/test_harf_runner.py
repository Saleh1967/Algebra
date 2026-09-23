"""المُشغِّلُ مفحوصٌ بلا مدوَّنة: يقول «نعم» ويقول «لا»، ويرفض ما يجب رفضُه.

**ما يُقاس ههنا وما لا يُقاس**: لا عربيّةَ ههنا. تُفحَص **الآلةُ**: أنّ سطرًا
ناقصَ الأعمدة يُرَدّ باسمه، وأنّ مصيرَ «لم يُحسَم» لا يُؤخَذ صمتًا، وأنّ
البصماتِ في المُشغِّل هي بصماتُ التسجيلات نفسِها، وأنّ الأحكامَ تسقط كما
تقوم. وأرقامُ العيّنة مُصطنَعةٌ ولا تُنقَل إلى شيء.

`A_HARNESS_THAT_ONLY_SAYS_YES_IS_NOT_A_HARNESS`: عيّنةُ فحصٍ كلُّ أحكامها
`MET` لا تفرّق بين آلةٍ تحكم وآلةٍ تُصدِّق كلَّ شيء. فالعيّنةُ تحمل حالاتٍ
**معاكسةً مقصودة**، ويُفحَص أنّ من الأحكام ما يسقط.

`THE_SEALED_FINGERPRINT_TRAVELS_WITH_THE_THRESHOLD`: بصمةُ التسجيل مكتوبةٌ
في المُشغِّل، ومطابقتُها لبصمة التسجيل مفحوصةٌ ههنا. فلو خُفِّض حدٌّ في
المُشغِّل لانفصلت البصمةُ عن حدِّها، والفحصُ يمسكها.

`THE_PREREGISTERED_RISK_IS_MECHANICAL_NOT_RHETORICAL`: خُتِم أنّ ق٤ قد
**تُنقِص** لأنّ مجرورَ جمعِ المؤنّث بالإضافة سيُقرَأ منصوبًا. والعيّنةُ تحمل
هذه الحالةَ فتُخرِج زيادةً **سالبةً** وحكمًا ساقطًا. وذلك لا يقول شيئًا عن
المصحف؛ يقول إنّ الآليّةَ التي حُذِّر منها **قائمةٌ وقابلةٌ للقياس**.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

import pytest
from test_harf_patch_registry import ORACLE as SECOND_ORACLE
from test_harf_patch_registry import REGISTRY as SECOND_REGISTRY
from test_imtina_preregistration import EXTRA as THIRD_REGISTRY
from test_imtina_preregistration import ORACLE as THIRD_ORACLE

from algebra.signified import seal

REPOSITORY = Path(__file__).resolve().parents[2]
RUNNER_PATH = REPOSITORY / "examples" / "irab" / "run_harf_measurement.py"


def _load() -> object:
    spec = importlib.util.spec_from_file_location("run_harf_measurement", RUNNER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # `dataclass` يقرأ الوحدةَ من السجلّ
    spec.loader.exec_module(module)
    return module


RUNNER = _load()


def test_a_short_line_is_refused_by_name_not_padded() -> None:
    """سبعةُ أعمدةٍ مُعلَنة؛ وستّةٌ تُرَدّ برقم السطر لا تُكمَّل صمتًا."""

    with pytest.raises(ValueError) as raised:
        RUNNER.parse_alignment("ا\t\t\tism\t0\t0")  # type: ignore[attr-defined]
    assert "السطرُ 1" in str(raised.value)
    assert "سبعة" in str(raised.value)

    with pytest.raises(ValueError):
        RUNNER.parse_alignment("# تعليقٌ وحدَه")  # type: ignore[attr-defined]


def test_the_smoke_sample_is_read_whole_and_carries_both_kinds() -> None:
    """خمسةٌ وعشرون رمزًا، خمسةَ عشرَ موسومًا وعشرةٌ غيرُ موسوم، وفيها معاكسات."""

    tokens = RUNNER.parse_alignment(RUNNER.SMOKE)  # type: ignore[attr-defined]
    assert len(tokens) == 25
    marked = [one for one in tokens if one.gold]
    assert len(marked) == 15
    assert len(tokens) - len(marked) == 10


def test_the_harness_says_no_as_well_as_yes() -> None:
    """من الأحكام ما يقوم ومنها ما يسقط — وإلّا لم تكن آلةَ حكم."""

    tokens = RUNNER.parse_alignment(RUNNER.SMOKE)  # type: ignore[attr-defined]
    three = RUNNER.three_way(tokens, RUNNER.ALL_RULES)  # type: ignore[attr-defined]
    assert three < Fraction("0.88")  # ك٣ يسقط على هذه العيّنة
    assert three > Fraction("0.50")  # ولا تسقط كلُّها، فليست الآلةُ نافيةً دائمًا


def test_the_preregistered_risk_of_rule_four_is_reproduced_as_a_negative_gain() -> None:
    """ق٤ تُنقِص حين يكون مجرورُ جمعِ المؤنّث بالإضافة — كما خُتِم قبل التشغيل.

    والعيّنةُ مُصطنَعةٌ عمدًا لتحمل هذه الحالة. فالرقمُ لا يُنقَل إلى مدوَّنة؛
    والمنقولُ أنّ **الآليّةَ قائمة**، وأنّ حدَّ ك٢ («لا تُنقِص») يمسكها.
    """

    tokens = RUNNER.parse_alignment(RUNNER.SMOKE)  # type: ignore[attr-defined]
    table = RUNNER.ablation(tokens, RUNNER.NO_CASE)  # type: ignore[attr-defined]
    gain_three, _ = table["ق٤"]
    assert gain_three < 0
    assert gain_three < Fraction(0)  # وهو حدُّ ك٢ بعينه


def test_every_rule_appears_in_the_ablation_table() -> None:
    """الشرطُ (هـ) مُستوفًى بالبناء: لكلّ رايةٍ سطرٌ، ولا مجموعَ بلا تفصيل."""

    tokens = RUNNER.parse_alignment(RUNNER.SMOKE)  # type: ignore[attr-defined]
    table = RUNNER.ablation(tokens, RUNNER.NO_CASE)  # type: ignore[attr-defined]
    assert set(table) == set(RUNNER.ALL_RULES)  # type: ignore[attr-defined]
    assert len(table) == 9  # ق٥ انقسمت ثلاثًا: حرفٌ ومبنيٌّ وفعل


def test_the_renumbering_trap_is_mapped_not_guessed() -> None:
    """«ك١ — ق٥ الممنوعُ من الصرف» في التسجيل، وق٥ اليومَ هي الامتناع.

    فالخريطةُ تنصّ على أنّ ك١ تُقاس بـ**ق٦**؛ ولو قُرئ الرقمُ حرفيًّا لقِيس
    شرطُ الممنوع من الصرف على قاعدة الامتناع. ورقمُ القاعدة ليس اسمًا ثابتًا.
    """

    mapping = RUNNER.SEALED_TO_CURRENT  # type: ignore[attr-defined]
    entry = next(key for key in mapping if key.startswith("ك١"))
    assert mapping[entry] == ("ق٦",)
    assert "ق٥ في التسجيل" in entry


def test_the_fingerprints_in_the_runner_are_the_registries_own() -> None:
    """بصمتا المُشغِّل محسوبتان من التسجيلين لا منقولتين بالنظر."""

    assert RUNNER.SECOND_SEAL == seal(SECOND_ORACLE, SECOND_REGISTRY)  # type: ignore[attr-defined]
    assert RUNNER.THIRD_SEAL == seal(THIRD_ORACLE, THIRD_REGISTRY)  # type: ignore[attr-defined]


def test_the_defer_policy_has_no_default_at_the_command_line() -> None:
    """`--defer` مطلوب؛ وتشغيلٌ بلا إعلانِ مصير «لم يُحسَم» يُرَدّ."""

    with pytest.raises(SystemExit):
        RUNNER.main(["--smoke"])  # type: ignore[attr-defined]
    with pytest.raises(SystemExit):
        RUNNER.main(["--defer", "no-case"])  # لا مدخلَ ولا فحص


def test_the_two_defer_policies_give_different_four_way_numbers() -> None:
    """مصيرُ «لم يُحسَم» يحرّك الرباعيَّ فعلًا — فليس القرارُ تفصيلًا."""

    tokens = RUNNER.parse_alignment(RUNNER.SMOKE)  # type: ignore[attr-defined]
    as_no_case = RUNNER.four_way_score(  # type: ignore[attr-defined]
        tokens, RUNNER.ALL_RULES, RUNNER.NO_CASE
    )
    as_error = RUNNER.four_way_score(  # type: ignore[attr-defined]
        tokens, RUNNER.ALL_RULES, "خطأ"
    )
    assert as_no_case != as_error
    assert as_no_case > as_error


def test_the_smoke_run_completes_and_prints_its_own_disclaimer(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """التشغيلُ يتمّ، ويُصدّر مخرَجَه بأنّ العيّنةَ مُصطنَعةٌ لا تقول شيئًا."""

    assert RUNNER.main(["--smoke", "--defer", "no-case"]) == 0  # type: ignore[attr-defined]
    printed = capsys.readouterr().out
    assert "مُصطنَعة" in printed
    assert "ولا يقول شيئًا عن العربيّة" in printed
    assert "MET" in printed and "FALSIFIED" in printed
    assert printed.count("ff690f9f") == 7  # سبعةُ أحكامٍ من التسجيل الثاني
    assert printed.count("ee1f32ef") == 2  # واثنان من الثالث
