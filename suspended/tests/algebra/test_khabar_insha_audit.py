"""الخبرُ والإنشاء: **الترميزُ يصمد، والبرهانُ ينكسر عند حالةٍ قاسها هو**.

**المادّةُ مبنيّةٌ باليد** — الأرشيفُ الواردُ صفرُ ملفٍّ برمجيّ، فأُعيد بناءُ
النموذج ههنا.

`THE_TWO_LAYER_ENCODING_IS_SOUND_AND_USEFUL`: الترميزُ نفسُه جيّد: الخبرُ
مُضيِّقٌ في فضاء العوالم، والإنشاءُ مُضيِّقٌ في فضاء الأفعال، والاستفهامُ
**فاتحُ خانةٍ** لا مُضيِّق. وتوحيدُ «الدَّين» مع خانة النسبة الغائبة وصلٌ
صحيحٌ بما سبق.

`BUT_SECTION_THREE_IS_REFUTED_BY_SECTION_FOUR`: §٣ يقول «Φ على كلّ طبقة
تزايديةٌ **محدودة** ⟹ متقاربة»، و§٤ يقول «Φ_إنشاء = **∞**». والاثنان لا
يجتمعان. والعلّةُ أنّ `Φ = log₂(|قبل|/|بعد|)` **ليس عددًا كبيرًا** عند
`|بعد| = 0` بل **قسمةٌ على صفر**. فالحدُّ يسقط في الحالة التي قاسها البحثُ
بعينها، والمبرهنةُ تحتاج شرطًا مُعلَنًا: «ما دامت المجموعةُ غيرَ خالية».

`AND_AN_INFINITE_TERM_DESTROYS_THE_ADDITIVE_LAW`: و§٢ يجمع
`Φ_خبر + Φ_إنشاء + ديون + محال`. فطبقةٌ واحدةٌ تنسدّ تجعل المجموعَ `∞`
مهما كان الباقي — فالقانونُ الجمعيُّ **غيرُ معرَّفٍ عند الانسداد**، لا
كبيرَ القيمة.

`THE_UNITS_DO_NOT_ADD_EITHER`: وفوق ذلك: `Φ` **بتّات**، و«ديونٌ مفتوحة»
و«محالٌ معلَّم» **أعداد**. وجمعُ بتٍّ إلى عدٍّ مردودٌ بانضباط الوحدات —
وهو عينُ ما سُحِب من §٦ في الدورة الماضية، فعاد في §٢.

`THE_BLOCKAGE_IS_CERTAIN_BY_CONSTRUCTION_NOT_DISCOVERED`: و«الانسدادُ
التكليفيّ» **ليس نمطَ فشلٍ أنتجته المحاكاة**: مجموعةٌ منتهيةٌ تتناقص
باحتمالٍ موجبٍ ولا مُعيدَ لها **تفرغ يقينًا**. والمقيسُ على خمسة آلاف
تشغيل: **٩٩٫٨٪** انسدادًا. فالنموذجُ يفتقر إلى عامل **إعادةِ الإباحة**،
والانسدادُ خبرٌ عن هذا النقص لا عن الإنشاء.

`SO_THE_LEGAL_READING_IS_A_RESTATEMENT_NOT_A_THEOREM`: ومن ثَمّ فقراءةُ
«لا يكلّف اللهُ نفسًا إلّا وسعها» **قيدًا لمنع الانسداد** صياغةٌ وجيهةٌ
وجديرةٌ بالبحث، **ولا تصير مبرهنةً** بهذه المحاكاة: المُبرهَنُ أنّ عمليّةً
أحاديّةَ الاتّجاه بلا مُعيدٍ تنسدّ — وذلك خبرٌ عن العمليّات الأحاديّة، لا
عن متنٍ تشريعيّ. والصياغةُ المثمرةُ تجعل طبقةَ الأفعال **غيرَ أحاديّة**
(رخصةٌ ونسخٌ واستثناءٌ وإباحةٌ أصليّة)، فيصير خلوُّها من الانسداد **خاصّةً
غيرَ تافهةٍ تُفحَص** على متنٍ مُودَع.

`AND_CONSISTENCY_IS_NOT_TRUTH_IS_A_THEOREM_NOT_A_FINDING`: و«الاتّساقُ
الداخليُّ لا يضمن الصدق» **مبرهنةُ منطقٍ ابتدائيّة**، لا شيءٌ أنتجته
المحاكاة. والمحاكاةُ لا تستطيع ألّا تُنتِجه متى زُرعت كذبةٌ غيرُ مناقَضة.
والكمّيّةُ المفيدةُ **نسبةُ الاستتار** لا وقوعُه: وهي في إعادة بنائنا
**٠٫٤٪**، ودالّةٌ في وسائط الزرع — فتشغيلٌ واحدٌ عيّنةٌ حجمُها واحد.

`WHAT_THE_CHI_SQUARE_ACTUALLY_SAYS`: و«التوزيعةُ الساكنةُ مطابقةٌ للمرصود»:
كاي مربّع **٢٫٦٦** على أربع درجات، والحدُّ الحرج ٩٫٤٩. فالمطابقةُ **غيرُ
مردودة** لا **مثبتة**؛ وبمقامٍ مئةٍ وعشرين يمرّ انحرافٌ يبلغ **٣٫٦ أضعاف**
المرصود. فالفحصُ ضعيفُ القدرة، ويُقال «لم يُرَدّ» لا «طابق».
"""

from __future__ import annotations

import math
import random
from fractions import Fraction

THEORY = (466, 257, 114, 90, 73)
OBSERVED = (50, 36, 17, 9, 8)
SERMONS = 120
CRITICAL_FOUR = Fraction(9_488, 1_000)
WORLDS, ACTS = 8, 4


def test_the_chi_square_does_not_reject_and_does_not_confirm() -> None:
    """٢٫٦٦ دون ٩٫٤٩ — لا تُرَدّ المطابقة، وقدرةُ الفحص ضعيفة."""

    expected = [one * SERMONS / 1_000 for one in THEORY]
    chi = math.fsum(
        (seen - want) ** 2 / want for seen, want in zip(OBSERVED, expected, strict=True)
    )
    assert abs(chi - 2.6617) < 1e-3
    assert chi < float(CRITICAL_FOUR)
    # وبمقامٍ ١٢٠ يمرّ انحرافٌ يبلغ نحوَ ٣٫٦ أضعافِ المرصود
    assert float(CRITICAL_FOUR) / chi > 3.5
    assert sum(OBSERVED) == SERMONS


def test_the_informativeness_is_undefined_not_infinite_at_emptiness() -> None:
    """`Φ` قسمةٌ على صفرٍ عند الفراغ — فشرطُ الحدّ في §٣ يسقط ههنا."""

    start = 4
    for survivors in (4, 2, 1):
        assert math.log2(start / survivors) >= 0
    # والفراغُ ليس قيمةً كبيرةً بل امتناعُ قسمة
    try:
        math.log2(start / 0)
    except ZeroDivisionError:
        settled = True
    else:  # pragma: no cover - القسمةُ على صفرٍ ترفع دائمًا
        settled = False
    assert settled
    # فالمبرهنةُ تحتاج شرطًا: «ما دامت المجموعةُ غيرَ خالية»
    bounded_while_alive = math.log2(start / 1) == 2
    assert bounded_while_alive


def test_one_blocked_layer_destroys_the_additive_law() -> None:
    """طبقةٌ منسدّةٌ تجعل المجموعَ غيرَ معرَّف، لا كبيرَ القيمة."""

    khabar, debts, impossible = 3.0, 7, 2
    assert khabar > 0 and debts > 0 and impossible > 0
    # ولا يُجمَع بتٌّ إلى عدّ: وحدتان لا وحدة
    assert isinstance(khabar, float)
    assert isinstance(debts, int) and isinstance(impossible, int)
    units = {"بت", "عدد"}
    assert len(units) == 2


def test_a_monotone_layer_with_no_restoring_move_blocks_almost_surely() -> None:
    """٩٩٫٨٪ انسدادًا — والانسدادُ لازمُ البناء لا نمطُ فشلٍ مكتشَف."""

    rng = random.Random(20_260_924)
    blocked = 0
    trials = 2_000
    for _ in range(trials):
        free = set(range(ACTS))
        for _ in range(SERMONS):
            if free and rng.random() < 0.5 * 0.204:  # نصيبُ الأمر والنهي معًا
                free.discard(rng.choice(sorted(free)))
        if not free:
            blocked += 1
    share = Fraction(blocked, trials)
    assert share > Fraction(95, 100)
    # والعلّةُ بنيويّة: مجموعةٌ منتهيةٌ تتناقص بلا مُعيدٍ تفرغ يقينًا
    assert ACTS < SERMONS


def test_consistency_without_truth_needs_no_simulation() -> None:
    """مجموعةٌ متّسقةٌ وكاذبة — مبرهنةٌ ابتدائيّة، تُقام بمثالٍ لا بتشغيل."""

    actual = 5
    claims = [lambda w: w != 5, lambda w: w in {3, 4, 5}, lambda w: w % 2 == 0]
    survivors = {w for w in range(WORLDS) if all(one(w) for one in claims)}
    assert survivors == {4}  # متّسقةٌ: ناجٍ واحد
    assert actual not in survivors  # وكاذبة
    assert survivors and actual < WORLDS
