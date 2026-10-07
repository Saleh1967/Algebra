"""الإعرابُ بالحرف تحت ختمٍ: شرطٌ سقط، وشرطان لا يُحكَم فيهما بما نُشِر.

**ترتيبُ الأوراق هو الحجّة**: وصل التسجيلُ المسبق (٢٠٢٦-٠٩-٢٣) ومعه المقيسُ
والشيفرةُ المنفَّذة. فالحكمُ يجري على ما سُجّل قبل النظر، لا على ما ظهر بعده.

**ما أُعيد ههنا بالحساب وما أُخِذ على التقرير**: جدولُ البقايا يُعاد **بالضبط**
— الصفوفُ الستّةُ تجمع إلى ٧٬١١٨، والحصصُ الستُّ تُعاد من العدد، وأحجامُ
الأصناف المشتقّةُ من معدّلات الخطأ تجمع إلى ٣٤٬٢٥٢ مقابلَ مقامٍ مُعلَنٍ
٣٤٬٢٥٤ (فرقُ تقريبٍ لا تناقض)، و٧٩٫٢٢٪ تُشتَقّ من ٧٬١١٨ ÷ ٣٤٬٢٥٤ إلى المنزلة
المنشورة. وأمّا **٨٦٫٤٥٪ فمأخوذةٌ على التقرير**: لا مدوَّنةَ تُقرَأ ههنا ولا
مخرَجَ ط٢ يُشغَّل، فلا تُعاد.

`A_CONJUNCTION_MAY_FALL_WHILE_ITS_TERMS_STAND`: التسجيلُ يقول «أ) أكثرُ من ٥
نقاط» و«ب) أكثرُ من ٥ نقاطٍ أُخَر»، فمجموعُهما يستلزم **أكثرَ من ١٠**. والمقيسُ
المنشورُ لهما معًا **+٧٫٢٣**. فإحداهما كاذبةٌ قطعًا، **ولا يُعرَف أيُّهما**:
لأنّ الشرط (هـ) — «كلُّ قاعدةٍ تُقاس على حدة وبالترتيب» — لم يُستوفَ، فنُشرت
زيادتان مجموعتان لا ستّ. والحكمُ على المفردتين `VOID` لا `MET`.

`A_RULE_DECLARED_AND_NOT_IMPLEMENTED_IS_A_SILENT_WITHDRAWAL`: ق٥ (الممنوعُ من
الصرف) مُسجَّلةٌ في التسجيل و**غائبةٌ عن الشيفرة المنفَّذة** — مُثبَتٌ بالتنفيذ
لا بالنظر: «إِبْرَٰهِيمَ» بعد حرف جرٍّ تُعطي `nasb` عبر `L9-R0-tashkil`،
والرايةُ `prev_is_jarr_harf` لا تُقرَأ أصلًا خارجَ فرع ق١.

`THE_DROPPED_RULE_IS_LARGER_THAN_THE_GAP_THAT_SANK_THE_PREDICTION`: أثقلُ ما
ههنا. الفجوةُ إلى الحدّ المُعلَن (٨٨٪) **١٫٥٥ نقطة**، وصنفُ ق٥ الغائبةِ يحمل
٢٠٫٦٪ من الباقي أي **≈٢٫٧٩ نقطة**. فالشرطُ (ج) سقط بفجوةٍ **أصغرَ من القاعدة
التي سُجّلت ولم تُنفَّذ**؛ ولا يُقال «القواعدُ لا تكفي» قبل تنفيذ ما سُجّل.

`A_SECOND_THRESHOLD_IS_NOT_A_SECOND_CHANCE`: التسجيلُ أعلن حدّين — «≥ ٨٨٪»
و«إن قلّ عن ٨٥٪ فالتشخيصُ ناقصٌ وأُعلنه». والمقيسُ ٨٦٫٤٥٪ وقع **بينهما**:
فالتنبّؤُ ساقطٌ، وبندُ الإعلان لم يقع فلا يلزم. والمنطقةُ الوسطى لم تُسمَّ
في التسجيل، وهي عيبٌ في الصياغة يُسمّى لا يُملأ بعد النظر.

`TWO_FIGURES_FOR_ONE_THING_ARE_NOT_A_DIFFERENCE`: ٨٦٫٤٥٪ على ٣٤٬٢٥٤ **كلمةً**
بأساسٍ ٣٧٫٤٤٪، و٩٣٫٦٣٪ المودَعةُ من قبل على مقامٍ مستلزَمٍ ≈١٨٬٠٣٨ **مقطعًا**
بأساسٍ ٣٧٫٣٤٪. فـ«فارقُ ٧٫١٨ نقطة» طرحٌ بين مقامين ووحدتين، ولا يُقرَأ فرقًا
بين القواعد والتعلّم.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.reconciliation import Partition, PrintedFigure, rounds_to
from algebra.signified import Direction, Oracle, Prediction, Verdict, seal

# ------------------------------------------------- الأوراكلُ كما أُعلِن
ORACLE = Oracle(
    name="QAC — الحالةُ الإعرابيّة",
    source="quran-morphology، المصحفُ كلُّه",
    extraction="٣٤٬٢٥٤ كلمةً موسومةً بحالة؛ الوحدةُ كلمةٌ لا مقطع",
)

MARKED_WORDS = 34_254
BASELINE = Fraction("0.3744")  # الأغلبُ nasb
L9_AS_IS = Fraction("0.3455")
AFTER_TASHKIL = Fraction("0.7922")
FINAL = Fraction("0.8645")

# ------------------------------------ بقايا الخطأ بعد قاعدة التشكيل وحدَها
RESIDUAL_TOTAL = 7_118
RESIDUAL = (
    ("ضميرٌ متّصل", 3_015, "0.424", "0.602"),
    ("جمعُ مذكّرٍ سالم", 2_072, "0.291", "0.422"),
    ("جمعُ مؤنّثٍ سالم", 606, "0.085", "0.375"),
    ("علمٌ وممنوعٌ من الصرف", 482, "0.068", "0.135"),
    ("مثنّى", 229, "0.032", "0.640"),
    ("سواها", 714, "0.100", "0.038"),
)

# ------------------------------------------- الشروطُ المُسجَّلةُ قبل النظر
PRED_A = Prediction(
    identifier="أ — ق١ تقشيرُ الضمير وحدَها",
    statistic="زيادةُ الدقّة بالنقاط فوق ٧٩٫٢٢٪",
    threshold=Fraction("0.05"),
    direction=Direction.AT_LEAST,
    falsifies="دعوى أنّ موضعَ القراءة وحدَه يحمل أكبرَ الخطأ",
)
PRED_B = Prediction(
    identifier="ب — ق٢ وق٣ وق٤ وق٦ معًا",
    statistic="زيادةٌ أُخرى بالنقاط",
    threshold=Fraction("0.05"),
    direction=Direction.AT_LEAST,
    falsifies="دعوى أنّ الإعرابَ بالحرف نظامٌ ثانٍ مستقلٌّ يُرفَع بقواعدَ معلنة",
)
PRED_C = Prediction(
    identifier="ج — المجموعُ النهائيّ",
    statistic="دقّةٌ كلّيّةٌ على المدوَّنة",
    threshold=Fraction("0.88"),
    direction=Direction.AT_LEAST,
    falsifies="دعوى أنّ التشخيصَ الثنائيّ (حركةٌ وحرف) يستوفي الباب",
)
PRED_C_FLOOR = Prediction(
    identifier="ج' — بندُ الإعلان",
    statistic="دقّةٌ كلّيّةٌ على المدوَّنة",
    threshold=Fraction("0.85"),
    direction=Direction.AT_LEAST,
    falsifies="لا شيء: بندُ إعلانٍ لا تنبّؤ — دونه يلزم إعلانُ نقص التشخيص",
)
REGISTRY = (PRED_A, PRED_B, PRED_C, PRED_C_FLOOR)


def test_the_residual_table_sums_to_its_declared_total() -> None:
    """الصفوفُ الستّةُ تجمع إلى ٧٬١١٨ بلا بقيّة — أوّلُ شهادةٍ على أنّ العدَّ واحد."""

    parts = tuple(count for _, count, _, _ in RESIDUAL)
    table = Partition(parts=parts, declared_total=RESIDUAL_TOTAL)
    assert table.measured_total == RESIDUAL_TOTAL
    assert table.residue == 0


def test_every_published_share_is_recomputed_from_its_count() -> None:
    """الحصصُ الستُّ تُعاد من العدد إلى المنزلة المنشورة، ولا واحدةَ تتخلّف."""

    for name, count, share, _ in RESIDUAL:
        printed = PrintedFigure(share)
        assert rounds_to(Fraction(count, RESIDUAL_TOTAL), 3) == printed.value, name


def test_the_class_sizes_implied_by_the_error_rates_rebuild_the_corpus() -> None:
    """أحجامُ الأصناف المشتقّةُ من معدّلات الخطأ تجمع إلى المقام — شهادةُ قسمة.

    وهذا ما لا يفعله جدولٌ مُجمَّعٌ من مصادر: ستُّ نسبِ خطأٍ مستقلّةٍ تُعيد
    بناءَ ٣٤٬٢٥٢ من ٣٤٬٢٥٤، وفرقُ اثنين أثرُ التقريب لا تناقض.
    """

    sizes = [Fraction(count) / Fraction(rate) for _, count, _, rate in RESIDUAL]
    rebuilt = round(float(sum(sizes)))
    assert rebuilt == 34_252
    assert abs(rebuilt - MARKED_WORDS) <= 2


def test_the_accuracy_after_the_tashkil_rule_is_reproduced_exactly() -> None:
    """٧٩٫٢٢٪ تُشتَقّ من ٧٬١١٨ ÷ ٣٤٬٢٥٤ — لا تُؤخَذ على التقرير بل تُعاد."""

    measured = 1 - Fraction(RESIDUAL_TOTAL, MARKED_WORDS)
    assert rounds_to(measured, 4) == AFTER_TASHKIL
    assert PrintedFigure("0.7922").value == AFTER_TASHKIL


def test_the_rules_start_below_the_majority_baseline() -> None:
    """L9 كما هي ٣٤٫٥٥٪ **دون** خطّ الأساس ٣٧٫٤٤٪ — وذلك يُطبَع لا يُطوى."""

    assert L9_AS_IS < BASELINE
    assert rounds_to(BASELINE - L9_AS_IS, 4) == Fraction("0.0289")


def test_prediction_c_is_falsified_and_its_floor_clause_does_not_fire() -> None:
    """٨٦٫٤٥٪ دون ٨٨٪ فالتنبّؤُ ساقط، وفوق ٨٥٪ فبندُ الإعلان لم يقع."""

    assert PRED_C.verdict(FINAL) is Verdict.FALSIFIED
    assert PRED_C_FLOOR.verdict(FINAL) is Verdict.MET
    gap = PRED_C.threshold - FINAL
    assert rounds_to(gap, 4) == Fraction("0.0155")


def test_the_pair_of_predictions_falls_although_neither_is_judged() -> None:
    """أ ∧ ب تستلزم أكثرَ من ١٠ نقاط، والمقيسُ لهما معًا +٧٫٢٣ — فإحداهما كاذبة.

    ولا يُعرَف أيُّهما: الشرطُ (هـ) — «كلُّ قاعدةٍ على حدة وبالترتيب» — لم
    يُستوفَ، فالحكمُ على المفردتين `VOID` لا `MET` ولا `FALSIFIED`. وسقفُ كلٍّ
    منهما محسوبٌ من صنفها، والسقفان معًا ١٧٫٢٩ نقطة — فالتنبّؤُ لم يكن محالًا
    قبل النظر، وذلك يُقال إنصافًا.
    """

    joint_measured = FINAL - AFTER_TASHKIL
    assert rounds_to(joint_measured, 4) == Fraction("0.0723")
    assert joint_measured < PRED_A.threshold + PRED_B.threshold

    assert PRED_A.verdict(joint_measured, void=True) is Verdict.VOID
    assert PRED_B.verdict(joint_measured, void=True) is Verdict.VOID

    ceiling_a = Fraction(3_015, MARKED_WORDS)
    ceiling_b = Fraction(2_072 + 606 + 229, MARKED_WORDS)
    assert rounds_to(ceiling_a, 4) == Fraction("0.0880")
    assert rounds_to(ceiling_b, 4) == Fraction("0.0849")
    assert ceiling_a + ceiling_b > PRED_A.threshold + PRED_B.threshold


def test_if_a_holds_then_b_is_falsified_and_the_missing_number_is_one_run() -> None:
    """في الفرع الذي تصدق فيه أ، لا يبقى لـب إلّا ٢٫٢٣ نقطةً فتسقط.

    والرقمُ الذي يفصل بينهما **واحدٌ لم يُنشَر**: زيادةُ ق١ وحدَها. وتحصيلُه
    تشغيلٌ واحدٌ بحذفِ قاعدةٍ، لا دراسةٌ ثانية.
    """

    joint = FINAL - AFTER_TASHKIL
    remainder_for_b = joint - PRED_A.threshold
    assert rounds_to(remainder_for_b, 4) == Fraction("0.0223")
    assert PRED_B.verdict(remainder_for_b) is Verdict.FALSIFIED


def test_the_dropped_rule_is_larger_than_the_gap_that_sank_prediction_c() -> None:
    """ق٥ مُسجَّلةٌ وغائبةٌ، وصنفُها يحمل ≈٢٫٧٩ نقطةً والفجوةُ ١٫٥٥ فقط.

    فلا يُقال «القواعدُ المعلنةُ لا تبلغ الحدّ» قبل تنفيذ ما سُجّل منها؛
    والحكمُ على (ج) يبقى `FALSIFIED` على **هذه النسخة** لا على التشخيص.
    """

    residual_share = 1 - FINAL
    forbidden_from_declension = residual_share * Fraction("0.206")
    assert rounds_to(residual_share, 4) == Fraction("0.1355")
    assert rounds_to(forbidden_from_declension, 4) == Fraction("0.0279")

    gap = PRED_C.threshold - FINAL
    assert forbidden_from_declension > gap
    assert PRED_C.verdict(FINAL + forbidden_from_declension) is Verdict.MET


def test_the_sound_feminine_plural_can_never_be_read_accusative() -> None:
    """«ات» لا تدخل فرعَ اللواحق الحرفيّة، فلا يُفَضّ التباسُها — عيبٌ بنيويّ.

    التسجيلُ أعلن ق٤ («ـَاتِ → {نصب، جرّ}») وق٦ (فضُّ الالتباس)، والشيفرةُ
    تجعل قيمةَ «ات» في `LETTER_SUF` خاليةً فيسقط الفرعُ كلُّه إلى قراءة
    الحركة. فكلُّ منصوبٍ من جمع المؤنّث السالم يُقرَأ مجرورًا **بالبناء**،
    لا خطأً في التمييز. وصنفُه ٦٠٦ أخطاءٍ بمعدّل ٣٧٫٥٪.
    """

    letter_suffixes: dict[str, set[str] | None] = {
        "ون": {"raf'"},
        "ين": {"nasb", "jarr"},
        "ان": {"raf'"},
        "ات": None,
    }
    assert letter_suffixes["ات"] is None
    ambiguous = [
        name for name, cases in letter_suffixes.items() if cases and len(cases) > 1
    ]
    assert ambiguous == ["ين"]  # و«ات» ليست فيها وإن كانت ملتبسةً في اللغة

    class_size = Fraction(606) / Fraction("0.375")
    assert round(float(class_size)) == 1_616


def test_two_figures_for_one_thing_do_not_make_a_difference() -> None:
    """٨٦٫٤٥٪ و٩٣٫٦٣٪ مقامان ووحدتان، فطرحُهما ليس فرقًا بين طريقتين."""

    rule_based_denominator = MARKED_WORDS  # كلمةٌ موسومةٌ بحالة
    learned_denominator = round(1_149 / float(1 - Fraction("0.9363")))  # مقطع
    assert learned_denominator == 18_038
    assert rule_based_denominator != learned_denominator
    assert BASELINE != Fraction("0.3734")  # أساسان مختلفان لبابٍ واحد
    assert rounds_to(Fraction("0.9363") - FINAL, 4) == Fraction("0.0718")


def test_the_lexicon_key_is_an_oracle_and_its_price_is_measured() -> None:
    """مفتاحُ `kind` لا `نوع`: ٦ حروفٍ بدل ١٥، وثمنُه ٠٫٧٥ نقطةٍ مقيسة."""

    with_right_key, with_wrong_key = FINAL, Fraction("0.8570")
    assert rounds_to(with_right_key - with_wrong_key, 4) == Fraction("0.0075")
    assert ORACLE.extraction.startswith("٣٤٬٢٥٤")


def test_the_registry_seals_and_a_changed_threshold_changes_the_seal() -> None:
    """الشروطُ الأربعةُ تُختَم، وتبديلُ حدٍّ واحدٍ بعد النظر يُعرَف بالبصمة."""

    fingerprint = seal(ORACLE, REGISTRY)
    assert len(fingerprint) == 64
    assert seal(ORACLE, REGISTRY) == fingerprint

    softened = Prediction(
        identifier=PRED_C.identifier,
        statistic=PRED_C.statistic,
        threshold=Fraction("0.86"),
        direction=PRED_C.direction,
        falsifies=PRED_C.falsifies,
    )
    assert seal(ORACLE, (PRED_A, PRED_B, softened, PRED_C_FLOOR)) != fingerprint
    assert softened.verdict(FINAL) is Verdict.MET  # ولو خُفِّض الحدُّ لنجا
