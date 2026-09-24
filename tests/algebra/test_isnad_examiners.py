"""ممتحِنان لج٩ لأوّل مرّة: حسابُ ما يلزم من أرقامهما، وما لا يلزم.

**ما يُقاس ههنا**: لا اتّفاقَ ولا عربيّة. لا مِتنَ في هذه الجلسة ولا شجرة،
فالاتّفاقُ **لا يُقاس**. ويُحسَب ما تلزم به الأرقامُ المنشورةُ وحدَها.

`TWO_EXAMINERS_IS_THE_NEW_THING_NOT_THE_NUMBERS`: وأهمُّ ما في الخبر ليس رقمًا
بل **بنيةً**: لم يجتمع لجسرٍ واحدٍ في هذا المشروع ممتحِنان مستقلّان قطّ. ط٧
وط٩ ممتحِنُهما واحدٌ (QAC)، والدلالةُ ممتحِنُها واحدٌ (الغريب). ومع ممتحِنٍ
واحدٍ لا يُفصَل «النظامُ أخطأ» عن «الممتحِنُ اختار»، والثاني يفتح ذلك الفصل.

`THE_TWO_COVERAGES_DO_NOT_BOUND_THE_INTERSECTION`: ٣٨٬٨٠٥ + ٣٢٬٦١٧ = ٧١٬٤٢٢
وهي **دون** ٧٧٬٤٢٨ بستّةِ آلافٍ وستّة. فحدُّ التقاطع الأدنى **صفر**: ليس في
النسبتين ما يضمن تقاطعًا أصلًا. فمقامُ الاتّفاق يُحسَب بالوصل على المرجع، ولا
يُشتَقّ من ٥٠٫١٪ و٤٢٫١٪ بحال.

`A_MAPPING_IS_NOT_A_TRANSLATION_OF_NAMES`: ونسبُ المقابلات الثلاث الظاهرة:
`subj`/فاعل = ١٫٥٢ · `pred`/خبر = ٠٫٥١ · `gen`/مضاف إليه = ٣٫٧٦. واحدةٌ فوق
الواحد وواحدةٌ دونه وواحدةٌ قريبةٌ من أربعة — ولو كان الخلافُ في الأسماء وحدَها
لتقاربت النسبُ. فالمفردتان **تقسمان المجال قسمتين مختلفتين**، وجدولُ المقابلة
دعوًى نحويّةٌ تُعلَن وتُنقَض، لا معجمُ ترجمة.

`MOST_OF_BOTH_EXAMINERS_CARRIES_NO_LISTED_LABEL`: والوظائفُ العشرُ المنشورةُ
تغطّي ٢١٬١١٣ من ٣٨٬٨٠٥ = **٥٤٫٤٪** من الجدول، والعلاقاتُ الخمسُ تغطّي ٢٣٬٧٣٥
من ٣٢٬٦١٧ = **٧٢٫٨٪** من الشجرة. فسبعةَ عشرَ ألفًا وثمانيةُ آلافٍ خارجَ
الجردين المنشورين، وهي تدخل المقامَ أو تخرج منه **بإعلان**.

`THE_GOVERNOR_IS_THE_QUESTION_AND_IT_IS_THE_RARE_FIELD`: وسؤالُ ج٩ «ما الذي
جعلها مرفوعة؟» — أي **العامل**. وهو مُسمًّى صراحةً في ١٢٫٥٣٪ من الجدول و٢٨٫٠٢٪
من الميسّر. فالوظيفةُ موسومةٌ كثيرًا والعاملُ أندرُ **بمرّتين إلى ثمانِ مرّات**.
ومن قاس الوظيفةَ وسمّاه قياسًا للعامل بدّل السؤال.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.reconciliation import Partition, rounds_to

MUSHAF = 77_428
JADWAL, MUYASSAR, QAC_WORDS = 38_805, 6_946, 32_617
QAC_TREES = 7_373
JADWAL_CANDIDATES = 177_835
JADWAL_GOVERNOR, MUYASSAR_GOVERNOR = 4_863, 1_946

BOOK_FUNCTIONS: dict[str, int] = {
    "فاعل": 5_073,
    "خبر": 3_426,
    "مفعول به": 2_731,
    "مبتدأ": 2_530,
    "نعت": 1_675,
    "حال": 1_606,
    "مضاف إليه": 1_458,
    "ظرف": 1_328,
    "معطوف": 655,
    "بدل": 631,
}
QAC_RELATIONS: dict[str, int] = {
    "subj": 7_694,
    "gen": 5_481,
    "obj": 4_907,
    "poss": 3_912,
    "pred": 1_741,
}


def test_the_two_coverages_permit_an_empty_intersection() -> None:
    """٣٨٬٨٠٥ + ٣٢٬٦١٧ = ٧١٬٤٢٢ < ٧٧٬٤٢٨ — فحدُّ التقاطع الأدنى صفر."""

    assert JADWAL + QAC_WORDS == 71_422
    assert JADWAL + QAC_WORDS < MUSHAF
    assert MUSHAF - (JADWAL + QAC_WORDS) == 6_006

    lower = max(0, JADWAL + QAC_WORDS - MUSHAF)
    upper = min(JADWAL, QAC_WORDS)
    assert (lower, upper) == (0, 32_617)

    assert rounds_to(Fraction(JADWAL, MUSHAF) * 100, 1) == Fraction("50.1")
    assert rounds_to(Fraction(QAC_WORDS, MUSHAF) * 100, 1) == Fraction("42.1")


def test_the_three_apparent_counterparts_disagree_in_three_directions() -> None:
    """١٫٥٢ و٠٫٥١ و٣٫٧٦ — فوقَ الواحد ودونَه وقريبًا من أربعة."""

    ratios = {
        "subj/فاعل": Fraction(QAC_RELATIONS["subj"], BOOK_FUNCTIONS["فاعل"]),
        "pred/خبر": Fraction(QAC_RELATIONS["pred"], BOOK_FUNCTIONS["خبر"]),
        "gen/مضاف إليه": Fraction(QAC_RELATIONS["gen"], BOOK_FUNCTIONS["مضاف إليه"]),
    }
    assert rounds_to(ratios["subj/فاعل"], 2) == Fraction("1.52")
    assert rounds_to(ratios["pred/خبر"], 2) == Fraction("0.51")
    assert rounds_to(ratios["gen/مضاف إليه"], 2) == Fraction("3.76")

    assert ratios["pred/خبر"] < 1 < ratios["subj/فاعل"] < ratios["gen/مضاف إليه"]
    assert max(ratios.values()) / min(ratios.values()) > 7


def test_the_listed_labels_cover_only_part_of_each_examiner() -> None:
    """٥٤٫٤٪ من الجدول و٧٢٫٨٪ من الشجرة؛ والباقي يدخل المقامَ بإعلان."""

    book = sum(BOOK_FUNCTIONS.values())
    tree = sum(QAC_RELATIONS.values())
    assert book == 21_113
    assert tree == 23_735

    assert rounds_to(Fraction(book, JADWAL) * 100, 1) == Fraction("54.4")
    assert rounds_to(Fraction(tree, QAC_WORDS) * 100, 1) == Fraction("72.8")

    assert Partition(parts=(book, JADWAL - book), declared_total=JADWAL).residue == 0
    assert (
        Partition(parts=(tree, QAC_WORDS - tree), declared_total=QAC_WORDS).residue == 0
    )
    assert JADWAL - book == 17_692
    assert QAC_WORDS - tree == 8_882


def test_the_nominal_sentence_is_the_pair_that_bridge_nine_declares() -> None:
    """مبتدأٌ + خبرٌ = ٥٬٩٥٦، وهما جردُ «الجملةِ الاسميّة» في ج٩ بعينه."""

    nominal = BOOK_FUNCTIONS["مبتدأ"] + BOOK_FUNCTIONS["خبر"]
    assert nominal == 5_956
    assert BOOK_FUNCTIONS["خبر"] > BOOK_FUNCTIONS["مبتدأ"]  # وخبرٌ بلا مبتدأٍ ظاهر
    assert BOOK_FUNCTIONS["خبر"] - BOOK_FUNCTIONS["مبتدأ"] == 896


def test_the_governor_is_far_rarer_than_the_function() -> None:
    """العاملُ مُسمًّى في ١٢٫٥٣٪ و٢٨٫٠٢٪؛ والوظيفةُ في ٥٤٫٤٪ — فالسؤالُ أندرُ."""

    jadwal = Fraction(JADWAL_GOVERNOR, JADWAL)
    muyassar = Fraction(MUYASSAR_GOVERNOR, MUYASSAR)
    assert rounds_to(jadwal * 100, 2) == Fraction("12.53")
    assert rounds_to(muyassar * 100, 2) == Fraction("28.02")
    assert muyassar > jadwal * 2

    functions = Fraction(sum(BOOK_FUNCTIONS.values()), JADWAL)
    assert functions > jadwal * 4  # فالوظيفةُ أوفرُ من العامل أربعَ مرّاتٍ فأكثر


def test_the_extraction_is_declared_coarse_before_any_number_is_read() -> None:
    """٣٨٬٨٠٥ من ١٧٧٬٨٣٥ مرشَّحًا = ٢١٫٨٢٪ — مجموعةٌ نظيفةٌ لا استخراجٌ تامّ."""

    kept = Fraction(JADWAL, JADWAL_CANDIDATES)
    assert rounds_to(kept * 100, 2) == Fraction("21.82")
    assert kept < Fraction(1, 4)

    # والمردودُ ليس عيبًا مكتومًا: ١٣٩٬٠٣٠ نثرًا بين قوسين لا لفظًا مقتبَسًا
    assert JADWAL_CANDIDATES - JADWAL == 139_030
    assert (
        Partition(
            parts=(JADWAL, JADWAL_CANDIDATES - JADWAL),
            declared_total=JADWAL_CANDIDATES,
        ).residue
        == 0
    )


def test_the_tree_has_more_words_than_edges_because_roots_carry_none() -> None:
    """٧٬٣٧٣ شجرةً و٣٢٬٦١٧ كلمة: ٤٫٤٢ كلمةً لكلّ شجرة، وجذرٌ لكلٍّ بلا حافّة."""

    per_tree = Fraction(QAC_WORDS, QAC_TREES)
    assert round(float(per_tree), 2) == 4.42

    # وحدُّ الحوافِّ الأعلى: كلمةٌ لكلٍّ إلّا الجذور
    edges_at_most = QAC_WORDS - QAC_TREES
    assert edges_at_most == 25_244
    assert sum(QAC_RELATIONS.values()) < edges_at_most
    assert edges_at_most - sum(QAC_RELATIONS.values()) == 1_509
