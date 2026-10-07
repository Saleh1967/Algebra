"""ميزانُ الكفّات الثلاث: عتبةُ إنقاذٍ أدنى ممّا تحتمل، وكفّةٌ تُخفي نصيبًا.

**ما يُقاس ههنا**: حسابُ ما يلزم من أرقامٍ مُبلَّغةٍ عن ميزانٍ بُني في مكانٍ
آخر. ولا مدوّنةَ تُقرَأ ههنا: المدوّنةُ نثرٌ حديثٌ لمؤلّفٍ واحد، وهي ليست
عندي، وأرقامُها شاهدةٌ عنها لا عن العربيّة — وذلك مُعلَنٌ في تقريره.

`AN_EXPECTATION_ABOVE_A_HALF_DOES_NOT_RESCUE_A_ZERO_FROM_CHANCE`: قيل إنّ
ثلاثةً وأربعين زوجًا خاليةً «لا واحدَ منها مُنقَذٌ بالندرة، لأنّ متوقَّعها
كلَّه فوق ٠٫٥». والعتبةُ **دون ما تحتمله الدعوى بكثير**: خانةٌ متوقَّعُها
٠٫٥ احتمالُ خلوِّها بالصدفة **٦٠٫٧٪** — أي أنّ خلوَّها هو الأرجح. وللقول
إنّ الخلوَّ خبرٌ يلزم متوقَّعٌ فوق ٣ (فيصير ٥٪) أو فوق ٥ (فيصير ٠٫٧٪).

`THE_ONE_NUMBER_THAT_SETTLES_IT_IS_THE_EXPECTED_COUNT_OF_EMPTY_CELLS`:
والفاصلُ ليس عتبةً لكلّ خانةٍ على حدة، بل **عددٌ واحد**: مجموعُ `exp(−E)`
على الخانات كلِّها — أي كم خانةً يُتوقَّع خلوُّها تحت الاستقلال. فإن قارب
ثلاثةً وأربعين فلا خبرَ في الأربعين؛ وإن قارب الصفرَ فكلُّها خبر. وهو سطرٌ
واحدٌ في المحرّك، ويُغني عن العتبة كلِّها.

`A_PAN_THAT_REJECTS_ENTIRELY_HIDES_A_COUNTABLE_SHARE`: وقيل إنّ «الفاعلَ
مرفوع» و«الفتحةَ الغالبة» **ليستا في مادّة الرسم إطلاقًا**. والإطلاقُ لا
يصحّ: للرفع والنصب **ظلٌّ في الرسم غيرُ المشكول** يُعَدّ ولا يُقدَّر —
الأسماءُ الستّة (أبو/أبا/أبي)، والمثنّى (ـان/ـين)، وجمعُ المذكّر السالم
(ـون/ـين)، والأفعالُ الخمسة (ثبوتُ النون وحذفُها). ولتنوين الفتح ظلٌّ كذلك:
يُكتَب ألفًا. فالقاعدةُ **معدومةٌ في المفرد المنصرف**، موجودةٌ في هذه الأبواب.

فحكمُ الكفّة **نسبةٌ لا بتّة**: ما نصيبُ الفاعلِ الواقعِ في بابٍ يُظهِر
رفعَه في الرسم؟ ذلك عددٌ يُعَدّ، وهو نفسُه خبرٌ عن العربيّة. والبتّةُ
تُخفيه — وهو عينُ ما وقع في `Bridge.is_built` قبل فصول: ثنائيّةٌ احتاجت
أربعةَ مواقف.

`THE_TWO_LOAD_FIGURES_ARE_NOT_COMPARABLE_AND_HE_SAID_SO`: و١٫٣٤× وسيطٌ
صرفيٌّ على الوقوعات، و٤٫٦× حمولةٌ وظيفيّةٌ على تمييز الأنواع. ونسبتُهما
٣٫٤٣× **بلا معنًى**، والامتناعُ عن طرحها صوابٌ سبق إليه.
"""

from __future__ import annotations

import math
from fractions import Fraction

from algebra.results import Evidence, trial_for

CORPUS_CHARACTERS = 1_020_673
CORPUS_WORDS = 236_994
CORPUS_TYPES = 26_292

CELLS, EMPTY = 841, 43
RESCUE_THRESHOLD = 0.5

# أبوابٌ يظهر فيها الإعرابُ في الرسم غيرِ المشكول
CASE_VISIBLE_IN_THE_RASM = (
    "الأسماءُ الستّة — أبو/أبا/أبي",
    "المثنّى — ـان/ـين",
    "جمعُ المذكّر السالم — ـون/ـين",
    "الأفعالُ الخمسة — ثبوتُ النون وحذفُها",
    "تنوينُ الفتح — يُكتَب ألفًا",
)


def test_an_expectation_of_a_half_makes_emptiness_the_likelier_outcome() -> None:
    """متوقَّعٌ ٠٫٥ ⇒ احتمالُ الخلوّ ٦٠٫٧٪؛ فالعتبةُ لا تُنقِذ ولا تُدين."""

    assert round(math.exp(-RESCUE_THRESHOLD), 4) == 0.6065
    assert math.exp(-RESCUE_THRESHOLD) > 0.5  # فالخلوُّ هو الأرجح

    ladder = {expected: math.exp(-expected) for expected in (1, 2, 3, 5)}
    assert round(ladder[1], 4) == 0.3679
    assert round(ladder[3], 4) == 0.0498
    assert round(ladder[5], 4) == 0.0067

    # فالعتبةُ التي تجعل الخلوَّ نادرًا (٥٪) هي ٣ لا نصف
    assert ladder[3] < Fraction(5, 100) < ladder[2]
    assert RESCUE_THRESHOLD * 6 == 3


def test_the_deciding_number_is_the_expected_count_not_a_per_cell_floor() -> None:
    """المتوقَّعُ من الخانات الخالية = Σ exp(−E)، ويُقارَن بالثلاثة والأربعين."""

    # مثالٌ صناعيٌّ يبيّن أنّ ٤٣ خانةً خاليةً قد تنشأ بلا مانع
    illustrative = [1.0] * 60 + [8.0] * (CELLS - 60)
    expected_empty = sum(math.exp(-one) for one in illustrative)
    assert round(expected_empty, 1) == 22.3
    assert 0 < expected_empty < EMPTY  # فالصدفةُ وحدَها تُخرِج عشراتٍ

    # وحدّان يفصلان الحكم: قريبٌ من ٤٣ ⇒ لا خبر، قريبٌ من صفر ⇒ كلُّها خبر
    assert EMPTY / CELLS < Fraction(6, 100)
    assert round(EMPTY / CELLS * 100, 2) == 5.11
    assert CELLS == 29**2  # ثمانيةٌ وعشرون حرفًا وفراغ


def test_a_rarity_floor_needs_letters_rarer_than_prose_provides() -> None:
    """E دون نصفٍ يقتضي حرفين تردُّدُ كلٍّ منهما دون ٠٫٠٧٪ — وذلك نادرٌ نثرًا."""

    adjacent = CORPUS_CHARACTERS - 1
    product_floor = RESCUE_THRESHOLD / adjacent
    assert round(product_floor * 1e7, 2) == 4.90

    symmetric = math.sqrt(product_floor)
    assert round(symmetric * 100, 3) == 0.070

    # فقولُه إنّ متوقَّعها كلَّه فوق نصفٍ **صحيحٌ حسابيًّا** على مدوّنةٍ بهذا الحجم
    assert symmetric < 0.001
    # ولا يلزم منه ما بُني عليه، وذلك موضعُ الاعتراض لا الحساب


def test_the_rasm_pan_hides_a_countable_share_of_the_case_rule() -> None:
    """خمسةُ أبوابٍ يظهر فيها الإعرابُ في الرسم؛ فالحكمُ نسبةٌ لا بتّة."""

    assert len(CASE_VISIBLE_IN_THE_RASM) == 5
    assert len(set(CASE_VISIBLE_IN_THE_RASM)) == 5
    for door in CASE_VISIBLE_IN_THE_RASM:
        assert "—" in door  # ولكلٍّ علامتُه المكتوبةُ مُسمّاة

    # والمعدومُ هو المفردُ المنصرف، لا القاعدةُ كلُّها
    absent_in = "المفردُ المنصرفُ غيرُ المنوَّن"
    assert absent_in not in CASE_VISIBLE_IN_THE_RASM

    # فالسؤالُ الذي يفتحه هذا عددٌ: ما نصيبُ الفاعل الواقع في هذه الأبواب؟
    open_question = "نصيبُ الفاعل الواقعِ في بابٍ يُظهِر رفعَه في الرسم"
    assert " أو " not in open_question


def test_the_two_load_figures_sit_in_different_units() -> None:
    """١٫٣٤× و٤٫٦× مقياسان لا مقياس، ونسبتُهما لا تُقرَأ."""

    proxy, functional = Fraction("1.34"), Fraction("4.6")
    assert proxy != functional
    assert round(float(functional / proxy), 2) == 3.43

    units = ("نصيبٌ من الوقوعات في أدواتٍ صرفيّة", "نصيبٌ من تمييز الأنواع")
    assert len(set(units)) == 2
    # والامتناعُ عن الطرح صوابٌ سبق إليه، وهو تطبيقُ درسٍ لا اتّباعُ عادة


def test_the_stipulated_kind_is_excluded_from_matter_not_judged_false() -> None:
    """«الكلامُ اسمٌ وفعلٌ وحرف» تُروى ولا تُوزَن؛ وإخراجُها غيرُ تكذيبها."""

    assert trial_for(Evidence.STIPULATED) != trial_for(Evidence.ATTESTED)
    assert "النسبةُ" in trial_for(Evidence.STIPULATED)

    # وتقسيمُ المفردات تسميةٌ محضةٌ فلا ظلَّ لها يُعَدّ…
    naming = "الكلامُ اسمٌ وفعلٌ وحرف"
    # …بخلاف الوصف الذي تحته ظلٌّ، وقد وُزِن في الكفّة الثانية
    describing = "الفاعلُ مرفوع"
    assert naming != describing
    assert round(33_725 / 41_205 * 100, 2) == 81.85


def test_the_sealed_item_comes_first_by_commitment_not_by_taste() -> None:
    """التعريبُ أوّلًا لأنّه **مختومٌ** — ولا يُفتَح بندٌ قبل المختوم."""

    sealed = "3a7ccdc9738738a5c482467313e2fd62acad31bd16a1e5be7c8d47737dbc322c"
    assert len(sealed) == 64
    assert set(sealed) <= set("0123456789abcdef")

    order = ("العددُ المؤجَّل في التعريب", "الأوزانُ من الجذور")
    assert order[0] != order[1]
    assert len(order) == 2

    # والثاني له قياسٌ أوّلُ في هذا المستودع سلفًا: توليدٌ طابق ٤٣٫٨٢٪
    generated, baseline = Fraction("0.4382"), Fraction("0.1786")
    assert generated > baseline * 2
    assert round(float(generated / baseline), 2) == 2.45
