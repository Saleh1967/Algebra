"""النسخةُ ٢: **الخمسةُ نُفِّذت**، وأربعةٌ جديدةٌ تُصلَح — وأطروحةُ الختام تُنقَض.

**المادّةُ مبنيّةٌ باليد**؛ والأرشيفُ الواردُ صفرُ ملفٍّ برمجيّ (الخامسُ على
التوالي).

`THE_FIVE_REPAIRS_LANDED`: الشرطُ الواحد في §٣ أُضيف فصحّ البرهان؛ والوحداتُ
في §٢ صارت **شعاعًا طبقيًّا** لا مجموعًا؛ والانسدادُ خرج من القانون إلى
**راية عطل**؛ واللازمتان أُعيد تصنيفُهما؛ و§٥ سُمّيت **إعادةَ صياغةٍ لا
برهانًا**. ولا اعتراضَ على واحدةٍ منها.

`BUT_TWENTY_SIX_POINT_NINE_IS_NOT_EXACTLY_ONE_MINUS_NINE_TENTHS_CUBED`:
و«٢٦٫٩٪ = ١−٠٫٩³ **نظريًّا بالضبط**»: والنظريُّ **٢٧٫١٠٪** لا ٢٦٫٩٪.
ومجالُ الثقة على عشرة آلافٍ [٢٦٫٠٣٪، ٢٧٫٧٧٪] **يحويه**، والفرقُ ٠٫٤٥σ.
فالمقيسُ **متّسقٌ** مع النظريّ لا مساوٍ له. و«بالضبط» تُخفي خطأَ المعاينة
بدل أن تنشره — وهو عينُ ما تُصلِحه الوثيقةُ في موضعٍ آخر.

`AND_THE_TWO_RATES_ARE_NOT_DISTINGUISHABLE`: و«بقي انتصارُ الكذب ٢٦٫٤٪»
مقابل ٢٦٫٩٪: الفرقُ **٠٫٥ نقطة** وخطؤه المعياريُّ **٠٫٦٣** — `z = 0.80`.
فالرقمان **رقمٌ واحد**. والدعوى «الفضحُ لا يُصلِح» **صحيحة**، وعرضُهما
عددين مختلفين ليس كذلك.

`THE_NEW_STRUCTURAL_LAW_HAS_A_THREE_LINE_COUNTEREXAMPLE`: و«الفضحُ الداخليُّ
يستلزم **تعدّدَ الشهود على النسبة الواحدة**» — يُنقَض بلا محاكاة: «العالمُ
في {١،٢}» و«العالمُ في {٣،٤}» **نسبتان مختلفتان بلا تكرار**، وناجوهما
∅. فالشرطُ الصحيح: **دعويان لا تجتمعان**، لا تكرارُ الدعوى. و«تعدّدُ
الشهود» خاصّةُ **نموذجهم** وحدَه: أخبارُه الصادقةُ كلُّها تحوي العالمَ
الفعليّ فلا تتناقض أبدًا، فلا يبقى إلّا تكرارُ الكذبة. وهذا **الجنسُ
نفسُه** الذي صُنِّفت به اللازمتان في §٤ — ولم يُصنَّف به.

`AND_THE_DEBT_COORDINATE_IS_SUBADDITIVE_NOT_ADDITIVE`: و«ديونٌ مفتوحة
[بتّاتٌ منتظَرة: كلُّ دَينٍ ≈ إفادةُ جوابه]»: سؤالان عن النسبة نفسِها
مجموعُهما بتّان والمشترَكُ بتٌّ. و`H(A,B) ≤ H(A) + H(B)` — فالديونُ **دون
الجمعيّة**، والمجموعُ يُضاعِف الحساب. والصحيحُ **إنتروبيا المجموعة
المشتركة** لا مجموعُ آحادها.

`A_THIRD_CONSTRUCTIONAL_NECESSITY_WENT_UNFLAGGED`: و«انتصارُ المستتر ٢٦٫٩٪
= الوقوعُ **تمامًا**»: أي أنّ الكذبةَ تنتصر كلّما وقعت — `P(انتصار | كذب) = 1`
بالبناء. فالصفُّ **مكرّرٌ لا نتيجة**، وهو **ثالثُ** اللوازم البنائيّة ولم
يُصنَّف معها.

`ON_A_FINITE_LATTICE_STABILISATION_IS_STRONGER_THAN_CONVERGENCE`: و§٣ يثبت
**التقارب**، والصحيحُ عند فضاءٍ منتهٍ أقوى: متتاليةٌ رتيبةٌ على شبكةٍ
منتهيةٍ **تستقرّ في خطواتٍ منتهية** (لا تزيد عن `|W₀|−1` تناقصًا). فالبرهانُ
يُثبِت أقلَّ ممّا يصدق.

`AND_THE_CLOSING_THESIS_IS_REFUTED_BY_THIS_VERY_CYCLE`: وأطروحةُ الختام —
«في كلّ مرّةٍ كان العطلُ في آلة القياس لا في القانون» — تصدق في الدورتين
الثانية والثالثة، و**تُنقَض في الرابعة**: `Φ` **محدودةٌ ⟹ متقاربة** كانت
**مبرهنةً ناقصةَ الفرض**، لا مسبارًا معطوبًا. والفرقُ ليس لفظيًّا: إصلاحُها
كان **إضافةَ شرطٍ إلى القانون**، لا معايرةَ أداة. فالنمطُ المزعومُ له
شاهدان ونقضٌ واحدٌ **من الدورة التي تُختَم به**.
"""

from __future__ import annotations

import math

TRIALS = 10_000
THEORETICAL = 1 - 0.9**3
MEASURED, AFTER_REPEAT = 0.269, 0.264


def test_the_theoretical_rate_is_twenty_seven_point_one_not_twenty_six_point_nine() -> (
    None
):
    """النظريُّ ٠٫٢٧١٠ والمقيسُ ٠٫٢٦٩ — متّسقان، وليسا متساويين."""

    assert abs(THEORETICAL - 0.2710) < 1e-9
    assert THEORETICAL != MEASURED
    error = math.sqrt(MEASURED * (1 - MEASURED) / TRIALS)
    assert MEASURED - 1.96 * error < THEORETICAL < MEASURED + 1.96 * error
    assert abs(THEORETICAL - MEASURED) / error < 0.5  # نصفُ انحرافٍ معياريّ


def test_the_two_published_rates_are_one_rate() -> None:
    """٢٦٫٩٪ و٢٦٫٤٪: `z = 0.80` — فرقٌ لا يُقرَأ."""

    spread = math.sqrt(
        MEASURED * (1 - MEASURED) / TRIALS + AFTER_REPEAT * (1 - AFTER_REPEAT) / TRIALS
    )
    score = (MEASURED - AFTER_REPEAT) / spread
    assert abs(score) < 1.96
    assert abs(score - 0.80) < 0.05


def test_internal_exposure_does_not_require_a_repeated_claim() -> None:
    """خبران مختلفان بلا تكرارٍ يُفرِغان الناجين — فالشرطُ عدمُ الاجتماع."""

    worlds = set(range(8))
    first, second = {1, 2}, {3, 4}
    assert first != second  # لا تكرارَ على النسبة الواحدة
    assert first <= worlds and second <= worlds
    assert not (first & second)  # ومع ذلك: ناجون = ∅

    # وفي نموذجهم يمتنع ذلك: كلُّ خبرٍ صادقٍ يحوي العالمَ الفعليّ
    actual = 5
    truthful = [{5, 1, 2}, {5, 3}, {0, 5, 7}]
    assert all(actual in one for one in truthful)
    survivors = set(worlds)
    for one in truthful:
        survivors &= one
    assert survivors == {actual}  # فلا تناقضَ بين صادقين أبدًا


def test_the_debt_coordinate_is_subadditive() -> None:
    """سؤالان على النسبة نفسِها: مجموعُهما بتّان والمشترَكُ بتّ."""

    single = 1.0
    naive_sum = single + single
    joint = 1.0  # إنتروبيا المجموعة المشتركة
    assert joint < naive_sum
    assert joint <= single + single  # H(A,B) ≤ H(A) + H(B)


def test_a_finite_monotone_chain_stabilises_rather_than_merely_converges() -> None:
    """على شبكةٍ منتهيةٍ الاستقرارُ في خطواتٍ منتهية — أقوى من التقارب."""

    start = 8
    sizes = [start]
    while sizes[-1] > 1:
        sizes.append(sizes[-1] - 1)
    assert sizes[-1] == 1
    assert len(sizes) - 1 == start - 1  # عددُ التناقصات محدودٌ بالبناء


def test_the_closing_thesis_has_a_counterexample_in_its_own_cycle() -> None:
    """شاهدان ونقض: §٣ كان **مبرهنةً ناقصةَ الفرض**، لا مسبارًا معطوبًا."""

    cycles = {
        "كاشفُ الابتلاع": "مسبار",
        "الاستقراءُ المنطقيّ": "مسبار",
        "الخبرُ والإنشاء": "قانون",
    }
    assert list(cycles.values()).count("مسبار") == 2
    assert list(cycles.values()).count("قانون") == 1
    assert cycles["الخبرُ والإنشاء"] != "مسبار"
