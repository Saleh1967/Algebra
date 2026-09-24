"""أجناسُ الدليل الثلاثة: لكلٍّ مِقامُ برهانٍ غيرُ مِقام أخيه.

**الفكرةُ ليست لي**: وردت في رسالةٍ تقول إنّ معرفةَ العربيّة اليوم خليطُ ثلاثة
مصادرَ مختلفةِ التكوين تُدرَّس ككتلةٍ واحدة — مشهودٌ، واصطلاحٌ، واستنتاج —
وأنّ أكثرَ ما سقط من دعاوى هذه الجلسة سقط من **خلطِ مِقاماتها**. وهو تشخيصٌ
صحيح، وأُودِع ههنا آلةً لا كلامًا.

`A_CLAIM_IS_TRIED_BY_THE_EVIDENCE_OF_ITS_OWN_KIND`: فالمشهودُ يُعَدّ على
بايتاتٍ مُبصَّمة، والاصطلاحُ يُنسَب إلى واضعه ونصِّه، والاستنتاجُ يُختبَر
بمقامٍ مُعلَنٍ وصفريٍّ مُسمّى. وثلاثةُ مِقاماتٍ لا واحد.

`BUT_A_STIPULATION_THAT_DESCRIBES_A_PATTERN_HAS_A_SHADOW_THAT_COUNTS`: وفي
الرسالة موضعٌ أُخالف فيه. قيل إنّ «الفاعلَ مرفوع» **ليست قابلةً للتأييد أو
النقض بالعدّ** لأنّها خبرٌ عن مدوّنة الصرفيّين. والتسميةُ كذلك حقًّا: «سَمِّ
هذا فاعلًا» لا يُنقَض بعدّ. **لكنّ الجملةَ تصف نمطًا في نصّ**، ونصيبُ
موافقتها **يُعَدّ** — وقد عُدَّ في هذا المستودع: ٨١٫٨٥٪ على ٤١٬٢٠٥ وحدة.
والعدُّ لا يَنقُض الاصطلاحَ بل يقيس **كفايتَه**؛ ومن أعفى الاصطلاحَ من العدّ
بإطلاقٍ أعفى معه كلَّ وصفٍ لبس ثوبَه. فالحدُّ الصحيح: **التسميةُ لا تُعَدّ،
والوصفُ الذي تحتها يُعَدّ**، والخلطُ بينهما هو الثغرة.

`THE_FOURTH_RULE_WAS_ALREADY_BUILT`: وقيل إنّ آلةَ الرفض تعُدّ الخانات
المملوءةَ ولا تُعلِن الفارغة. وذلك ما كان صحيحًا **قبل فصلين**: `Vacancy`
تُعدِّد ستّةَ أجناسٍ للخلوّ، وثلاثةٌ منها لا تُدَّعى بلا شاهد، و`UNCLASSIFIED`
هو ما يعطيه الجداءُ وحدَه. فالخطوةُ المطلوبةُ مبنيّةٌ ومفحوصة.
"""

from __future__ import annotations

import pytest

from algebra.results import (
    EVIDENCE_TRIALS,
    Evidence,
    ResultsError,
    Vacancy,
    a_stipulation_has_a_measurable_shadow,
    trial_for,
)


def test_the_three_kinds_have_three_different_trials() -> None:
    """ثلاثةُ أجناسٍ وثلاثةُ مِقامات، ولا يُجرَّب جنسٌ بمِقام غيره."""

    assert len(Evidence) == 3
    assert set(EVIDENCE_TRIALS) == set(Evidence)
    assert len(set(EVIDENCE_TRIALS.values())) == 3

    assert "العدُّ" in trial_for(Evidence.ATTESTED)
    assert "النسبةُ" in trial_for(Evidence.STIPULATED)
    assert "اختبارٌ" in trial_for(Evidence.INFERRED)

    with pytest.raises(ResultsError, match="مفردته المغلقة"):
        trial_for("مشهود")  # type: ignore[arg-type]


def test_a_stipulation_that_describes_a_pattern_is_countable() -> None:
    """«الفاعلُ مرفوع» يصف نمطًا، ونصيبُ موافقته يُعَدّ — وقد عُدَّ ههنا."""

    naming_only = "يُسمّى هذا الموضعُ فاعلًا"
    describing = "الفاعلُ مرفوع"
    assert a_stipulation_has_a_measurable_shadow(describing)

    # والعدُّ وقع فعلًا في هذا المستودع: الضبطُ الرباعيُّ على ٤١٬٢٠٥ وحدة
    measured, denominator = 33_725, 41_205
    assert 0 < measured < denominator
    assert round(measured / denominator * 100, 2) == 81.85

    # والعدُّ لا يَنقُض الاصطلاحَ: ١٨٪ مخالفةً لا تُلغي التسمية، بل تقيس كفايتَها
    assert denominator - measured == 7_480
    assert naming_only != describing


def test_mixing_the_trials_is_the_defect_the_letter_names() -> None:
    """استنتاجٌ يُجرَّب بمِقام مشهودٍ، أو اصطلاحٌ يُروى كأنّه مشهود."""

    wrong = (
        (Evidence.INFERRED, Evidence.ATTESTED),
        (Evidence.STIPULATED, Evidence.ATTESTED),
    )
    for claim, borrowed in wrong:
        assert trial_for(claim) != trial_for(borrowed)

    right = [(kind, trial_for(kind)) for kind in Evidence]
    assert len(right) == 3
    assert len({trial for _, trial in right}) == 3


def test_the_enumeration_of_emptiness_already_exists() -> None:
    """الخانةُ الفارغةُ مُعدَّدةٌ منذ فصلين: ستّةُ أجناسٍ لا مملوءٌ وفارغ."""

    assert len(Vacancy) == 6
    assert Vacancy.UNCLASSIFIED in set(Vacancy)
    assert Vacancy.IMPOSSIBLE is not Vacancy.UNATTESTED
    assert Vacancy.UNREACHABLE is not Vacancy.REFUSED
    # فالبتّةُ الواحدةُ كانت تُسقِط خمسةَ فروق، وقد عُدَّت
    assert len(Vacancy) - 1 == 5
