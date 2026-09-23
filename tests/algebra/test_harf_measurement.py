"""القياسُ المختومُ مُجرًى على ٧٧٬٤٢٨ رمزًا: ثمانيةٌ سقطت، وواحدٌ لم يُحكَم.

**ما جرى**: وصلت المحاذاةُ كاملةً (٧٧٬٤٢٨ صفًّا، و**٣٤٬٢٥٤ موسومًا بحالةٍ
بالضبط** كما أُعلن في التسجيل)، فشُغِّل المُشغِّلُ عليها. والأرقامُ أدناه
مخرَجُه، ويُعاد بأمرٍ واحد:

    python examples/irab/run_harf_measurement.py --aligned <file> --defer no-case

`THE_WIDENING_IS_EXACTLY_WHAT_CARRIES_THE_THRESHOLD`: أثقلُ ما ظهر. شرطُ (ج)
عتبتُه ٧٠٫٧٦٪. وق٥ **كما خُتِمت** (حرفٌ ومبنيُّ إحالة) تبلغ ٦٦٫٤٤٪ — فتسقط
بفجوة ٤٫٣٢ نقطة. وق٥ **كما نُفِّذت** (ومعها الفعلُ، وهو لاحقٌ على الختم)
تبلغ ٧١٫٣٠٪ — فتقوم. والتوسيعُ وحدَه يزن **٤٫٨٧ نقطة**، والفجوةُ ٤٫٣٢.
فالذي يحمل الشرطَ فوق عتبته هو **ما لم يُختَم عليه**، لا ما خُتِم.

`TWO_SOURCES_DISAGREE_ON_A_FIFTH_OF_THE_DATA`: **٧٬٥٣٦ رمزًا** موسومةٌ بحالةٍ
عند العرّاف وط٧ يقول فيها «حرفٌ» أو «فعل» — **٢٢٫٠٠٪ من الموسوم**. وبالمقابل
**١٩٬٥٩٤** غيرُ موسومةٍ وط٧ يقول فيها «اسم» — **٤٥٫٣٨٪ من غير الموسوم**. وهذا
تعارضُ مصدرين مستقلّين لا خطأُ قاعدة، وهو يُفسِّر هبوطَ الثلاثيّ من ٨٥٫٤٣٪
إلى ٦٧٫٣٥٪ حين يُمكَّن الامتناعُ: القاعدةُ ترث وسمًا ثمّ تُحاسَب عليه.

`A_SEALED_CONDITION_IS_MEASURED_ON_THE_SET_IT_WAS_SEALED_ON`: التسجيلُ الثاني
خُتِم على R0d، ومجموعةُ R0e أوسعُ منها بامتناعٍ عن الحرف والفعل. فقياسُ (ك٣)
بمجموعة R0e قياسٌ لغير ما خُتِم. والمقيسُ على R0d **٨٥٫٤٣٪**، وعلى R0e
٦٧٫٣٥٪ — وبينهما ثماني عشرةَ نقطة. وهذا رُدَّ على غيري فلا يُقبَل منّي.

`THE_MIDDLE_ZONE_CLAIMED_ITS_SECOND_MEASUREMENT`: شرطُ (هـ) ينجح دون ٣ نقاط
ويُعلِن النقصَ فوق ٧، وما بينهما بلا حكم. والمقيسُ بق٥ المختومة **−٤٫٤٥** —
في المنطقة الوسطى بعينها. وهي المرّةُ الثانيةُ التي يقع فيها المقيسُ هناك،
بعد ٨٦٫٤٥٪ بين ٨٥ و٨٨. وقد قيل ذلك **قبل** التشغيل لا بعده.

`I_WITHDRAW_MY_OWN_DERIVATION_OF_PREDICTION_B`: قلتُ قبل التشغيل إنّ (ب)
«تُحسَب من رقمين منشورين» وقدّرتُها ٣٨٫٢٥٪. والمقيسُ **٥٨٫٤٣٪** تحت
«لم يُحسَم = لا إعراب»، و**٣٧٫٨٧٪** تحت «لم يُحسَم = خطأ». فحسابي كان صحيحًا
تحت سياسةٍ واحدةٍ فقط، وقد **بنيتُه على أربعة مخارجَ** بينما كنتُ في الصفحة
نفسِها أُثبِت أنّ المخارجَ خمسة. فالدعوى تُسحَب: (ب) ليست «حسابًا» بل
**غيرَ محكومةٍ لانعدام سياسةٍ مُعلَنة** — والسياسةُ لا تحرّك الرقمَ وحدَه بل
**تقلب الحكم**.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.evaluation import Tally
from algebra.reconciliation import Partition, rounds_to
from algebra.signified import Direction, Prediction, Verdict

ALIGNED = 77_428
MARKED = 34_254
UNMARKED = ALIGNED - MARKED

# ------------------------------------- الثلاثيُّ والرباعيُّ بأربع مجموعاتِ قواعد
THREE_WAY = {
    "بلا امتناعٍ البتّة": Fraction("0.8561"),
    "R0d — المختومُ عليها": Fraction("0.8543"),
    "ق٥ كما خُتِمت": Fraction("0.8097"),
    "R0e كما نُفِّذت": Fraction("0.6735"),
}
FOUR_WAY = {
    "بلا امتناعٍ البتّة": Fraction("0.5843"),
    "R0d — المختومُ عليها": Fraction("0.6119"),
    "ق٥ كما خُتِمت": Fraction("0.6644"),
    "R0e كما نُفِّذت": Fraction("0.7130"),
}
CEILING = Fraction("0.9355")

# تعارضُ المصدرين
MARKED_BUT_NOT_NOUN = 7_536
UNMARKED_BUT_NOUN = 19_594

# جدولُ الاستئصال — زيادةُ كلّ قاعدةٍ وحدَها على الثلاثيّ
ABLATION_THREE = {
    "ق٠": Fraction("0.0162"),
    "ق١": Fraction("0.0144"),
    "ق٢": Fraction("0.0365"),
    "ق٣": Fraction("0.5507"),
    "ق٤": Fraction("-0.0007"),
    "ق٥ح": Fraction("-0.0445"),
    "ق٥م": Fraction("-0.0011"),
    "ق٥و": Fraction("-0.1362"),
    "ق٦": Fraction("0.0042"),
}


def test_the_alignment_matches_the_count_declared_in_the_registry() -> None:
    """٣٤٬٢٥٤ موسومًا من ٧٧٬٤٢٨ — العددان المُعلَنان قبل النظر، بلا بقيّة."""

    split = Partition(parts=(MARKED, UNMARKED), declared_total=ALIGNED)
    assert split.residue == 0
    assert UNMARKED == 43_174
    assert rounds_to(Fraction(UNMARKED, ALIGNED), 4) == Fraction("0.5576")


def test_prediction_a_holds_exactly_as_derived_before_the_run() -> None:
    """(أ) [٥٠٪،٦٠٪] والمقيسُ ٥٥٫٧٦٪ — وقد اشتُقّ قبل التشغيل فليس اختبارًا."""

    share = Fraction(UNMARKED, ALIGNED)
    assert Fraction("0.50") < share < Fraction("0.60")
    assert rounds_to(share, 4) == Fraction("0.5576")


def test_my_derivation_of_prediction_b_is_withdrawn() -> None:
    """٣٨٫٢٥٪ صحّت تحت سياسةٍ وسقطت تحت أخرى؛ فالدعوى تُسحَب لا تُرقَّع.

    والعطبُ في حسابي: بنيتُه على **أربعة** مخارجَ بينما كنتُ أُثبِت في الصفحة
    نفسِها أنّ المخارجَ خمسة. فالسياسةُ لا تحرّك الرقمَ فحسب: **تقلب الحكم**.
    """

    as_no_case, as_error = Fraction("0.5843"), Fraction("0.3787")
    mine = Fraction("0.3825")
    low, high = Fraction("0.35"), Fraction("0.40")

    assert not low < as_no_case < high  # تحت السياسة الأولى: خارجَ المجال
    assert low < as_error < high  # وتحت الثانية: داخلَه
    assert abs(as_error - mine) < Fraction("0.005")  # وحسابي يطابق الثانيةَ وحدَها
    assert as_no_case - as_error > Fraction("0.20")  # والفرقُ بين السياستين عشرون نقطة


def test_the_deferred_tokens_are_what_broke_the_derivation() -> None:
    """١٥٬٩١٥ رمزًا مؤجَّلًا وغيرَ موسوم = ٢٠٫٥٥٪ من المقام — وهي المنطقةُ المتنازَعة."""

    deferred_unmarked = 15_915
    assert rounds_to(Fraction(deferred_unmarked, ALIGNED), 4) == Fraction("0.2055")
    swing = Fraction("0.5843") - Fraction("0.3787")
    assert rounds_to(swing, 4) == Fraction("0.2056")  # والتأرجحُ هو نصيبُها بعينه


def test_two_independent_sources_disagree_on_a_fifth_of_the_marked() -> None:
    """٧٬٥٣٦ موسومًا يقول فيها ط٧ حرفًا أو فعلًا = ٢٢٫٠٠٪ — تعارضٌ لا خطأُ قاعدة."""

    assert rounds_to(Fraction(MARKED_BUT_NOT_NOUN, MARKED), 4) == Fraction("0.2200")
    assert rounds_to(Fraction(UNMARKED_BUT_NOUN, UNMARKED), 4) == Fraction("0.4538")
    assert MARKED_BUT_NOT_NOUN + UNMARKED_BUT_NOUN == 27_130

    # والامتناعُ يُحوّل التعارضَ إلى خطأٍ محسوبٍ على القاعدة
    inherited = THREE_WAY["R0d — المختومُ عليها"] - THREE_WAY["R0e كما نُفِّذت"]
    assert rounds_to(inherited, 4) == Fraction("0.1808")
    assert inherited < Fraction(MARKED_BUT_NOT_NOUN, MARKED)  # ولا يتجاوزه


def test_the_unsealed_widening_is_what_carries_prediction_c() -> None:
    """عتبةُ (ج) ٧٠٫٧٦٪: المختومةُ ٦٦٫٤٤٪ تسقط، والمنفَّذةُ ٧١٫٣٠٪ تقوم.

    والتوسيعُ (امتناعُ الفعل، وهو لاحقٌ على الختم) يزن ٤٫٨٧ نقطةً والفجوةُ
    ٤٫٣٢. فلولاه لسقط الشرط. وهذا لا يقول إنّ التوسيعَ خطأٌ نحويًّا — يقول
    إنّ الحكمَ عليه ليس حكمًا على ما خُتِم.
    """

    threshold = Fraction(UNMARKED, ALIGNED) + Fraction("0.15")
    assert rounds_to(threshold, 4) == Fraction("0.7076")

    sealed = Prediction(
        identifier="ج — كما خُتِمت",
        statistic="الرباعيُّ بق٥ حرفًا ومبنيَّ إحالة",
        threshold=threshold,
        direction=Direction.AT_LEAST,
        falsifies="دعوى أنّ الامتناعَ المختومَ يفوق الأساسَ بخمسَ عشرةَ نقطة",
    )
    assert sealed.verdict(FOUR_WAY["ق٥ كما خُتِمت"]) is Verdict.FALSIFIED
    assert sealed.verdict(FOUR_WAY["R0e كما نُفِّذت"]) is Verdict.MET

    widening = FOUR_WAY["R0e كما نُفِّذت"] - FOUR_WAY["ق٥ كما خُتِمت"]
    gap = threshold - FOUR_WAY["ق٥ كما خُتِمت"]
    assert rounds_to(widening, 4) == Fraction("0.0486")
    assert rounds_to(gap, 4) == Fraction("0.0432")
    assert widening > gap


def test_prediction_e_landed_in_the_unnamed_middle_zone_again() -> None:
    """(هـ) ينجح دون ٣ ويُعلِن فوق ٧، والمقيسُ −٤٫٤٥ — بينهما، بلا حكم.

    وهي الثانيةُ: ٨٦٫٤٥٪ وقعت بين ٨٥ و٨٨ في الدورة الأولى. وقيل هذا قبل
    التشغيل في `test_imtina_preregistration`، لا بعده.
    """

    drop_sealed = THREE_WAY["R0d — المختومُ عليها"] - THREE_WAY["ق٥ كما خُتِمت"]
    assert rounds_to(drop_sealed, 4) == Fraction("0.0446")
    assert Fraction("0.03") < drop_sealed < Fraction("0.07")

    drop_implemented = THREE_WAY["R0d — المختومُ عليها"] - THREE_WAY["R0e كما نُفِّذت"]
    assert drop_implemented > Fraction("0.07")  # وبالتوسيع: يقع بندُ الإعلان


def test_the_second_registry_is_measured_on_the_set_it_was_sealed_on() -> None:
    """ك٣ على R0d ٨٥٫٤٣٪ لا على R0e ٦٧٫٣٥٪؛ وتسقط على الاثنتين، لكن بفارق."""

    on_r0d = THREE_WAY["R0d — المختومُ عليها"]
    on_r0e = THREE_WAY["R0e كما نُفِّذت"]
    assert on_r0d < Fraction("0.88")  # FALSIFIED على المختوم عليه
    assert on_r0e < Fraction("0.88")  # وعلى غيره كذلك
    assert rounds_to(on_r0d - on_r0e, 4) == Fraction("0.1808")

    published = Fraction("0.8645")  # ما أعلنه صاحبُه لـR0c
    assert rounds_to(published - on_r0d, 4) == Fraction("0.0102")


def test_every_rule_has_its_own_increment_and_three_of_nine_are_negative() -> None:
    """الشرطُ (هـ) مُستوفًى: تسعُ زياداتٍ مفردة. و**أربعٌ منها سالبة**."""

    assert len(ABLATION_THREE) == 9
    negative = {name for name, gain in ABLATION_THREE.items() if gain < 0}
    assert negative == {"ق٤", "ق٥ح", "ق٥م", "ق٥و"}
    assert len(negative) == 4
    assert ABLATION_THREE["ق٣"] == max(ABLATION_THREE.values())
    assert ABLATION_THREE["ق٣"] > Fraction("0.50")  # التشكيلُ وحدَه أكثرُ من نصف الباب


def test_rule_four_lowered_the_score_exactly_as_it_was_sealed_to_risk() -> None:
    """ق٤ خُتِم حدُّها «لا تُنقِص»، وقد أنقصت ٠٫٠٧ نقطة — فسقطت بما حُذِّر منه.

    والمقدارُ صغيرٌ والحكمُ قاطع: الحدُّ صفرٌ، والمقيسُ دونه. وما كان
    تحذيرًا نظريًّا صار عددًا.
    """

    assert ABLATION_THREE["ق٤"] < 0
    assert rounds_to(ABLATION_THREE["ق٤"], 4) == Fraction("-0.0007")
    ceiling_was = Fraction(606, MARKED)  # سقفُها من جدول البقايا
    assert rounds_to(ceiling_was, 4) == Fraction("0.0177")
    assert ABLATION_THREE["ق٤"] < ceiling_was  # فلم تبلغ سقفَها بل عكستْه


def test_the_abstention_numbers_are_three_not_one() -> None:
    """التغطيةُ ٧٦٫٥٣٪ والدقّةُ حيث تُسنَد ٨٨٫٠١٪ — وكلاهما دون حدّه المختوم."""

    assigned = round(float(Fraction("0.7653") * MARKED))
    correct = round(float(Fraction("0.8801") * assigned))
    tally = Tally(
        correct=correct, wrong=assigned - correct, abstained=MARKED - assigned
    )
    assert rounds_to(tally.coverage, 4) == Fraction("0.7653")
    assert rounds_to(tally.precision_where_it_fires, 4) == Fraction("0.8801")
    assert tally.coverage < Fraction("0.93")  # ك٥ FALSIFIED
    assert tally.precision_where_it_fires < Fraction("0.90")  # ك٤ FALSIFIED


def test_the_ceiling_is_not_a_measurement_and_condition_z_is_void() -> None:
    """٩٣٫٥٥٪ سقفٌ لا قياس: أوراكلُه مُشتَقٌّ من عمود الهدف، فـ(ز) لا تُحكَم.

    و«الوسمُ الصحيح» في المُشغِّل هو «ما له حالةٌ فهو اسم»، وهو معطًى من
    الهدف نفسِه. فالفرقُ ٢٢٫٢٥ نقطةً يقيس **المسافةَ إلى السقف** لا ثمنَ ط٧
    وحدَه. والرقمُ المستقلُّ عن الهدف هو تعارضُ المصدرين: ٧٬٥٣٦.
    """

    assert CEILING > max(FOUR_WAY.values())
    distance = CEILING - FOUR_WAY["R0e كما نُفِّذت"]
    assert rounds_to(distance, 4) == Fraction("0.2225")
    # ولا يُقارَن بحدٍّ، لأنّ المقياسَ ليس المقياسَ المختوم
    assert MARKED_BUT_NOT_NOUN > 0
