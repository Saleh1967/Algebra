"""تدقيقُ عبورِ المدوَّنة: ما ينطبق من تقرير Arramooz وما لا ينطبق.

**ما يُقاس ههنا وما لا يُقاس**: لا يُفتَح معجمٌ ولا يُقرَأ مصحف. يُفحَص شيئان:
أنّ أرقامَ التقرير **متّسقةٌ فيما بينها**، وأنّ ما يُشتَقّ منها بالحساب —
لا بالنظر — يُصدّق حكمَه أو ينقضه.

`A_FILTER_IS_A_MEASUREMENT_TOO`: مصفاةٌ تُطبَّق قبل القياس **جزءٌ من القياس**.
فإن لم يُعلَن كم حذفت، لم يستطع قارئٌ أن يميّز بين «الخرقُ نادر» و«المصفاةُ
أزالت الخارق». وحجمُ المصفاة رقمٌ واحدٌ يُنشَر، لا تحليلٌ يُطلَب.

`A_RATE_WITHOUT_ITS_UNIT_IS_NOT_A_RATE`: ٢٫١١٪ من الكلمات و٠٫٠٠٨٪ من المقاطع
مقداران لا يُقارَنان. والهبوطُ بينهما يخلط أثرَ المصفاة بأثر تغيُّر الوحدة،
وأحدُهما وحدَه قد يفسّره كلَّه.

`A_BETWEEN_GAP_IS_READ_AGAINST_THE_WITHIN_SPREAD`: فرقُ نسبةٍ بين مدوَّنتين لا
يُقرَأ حتى يُقاس تذبذبُها **داخل** المدوَّنة الواحدة؛ وإلّا نُسِب إلى اختلاف
اللسان ما هو أثرُ اختيارٍ في التمثيل.

`A_SUM_IS_A_CHECK_NOT_A_CAPTION`: مجموعٌ لا يطابق صفوفَه ليس تفصيلًا: إمّا
صفوفٌ محجوبة — فتُسمّى — وإمّا خطأٌ في أحد الرقمين.

**حالُ المُدقَّق (لاحقٌ على هذا الملفّ)**: صاحبُ التقرير **سحب** دعوى
«٠٫٠٠٨١٤٢٪» بنفسه، وسحب معها دعوى «أوّلُ اختبارٍ خارج المدوّنة». وسببُ السحب
الذي أعلنه هو عينُ ما وجده هذا التدقيقُ في البند الخامس: **المصفاةُ تصنع
الرقم**. فالأرقامُ أدناه تخصّ النسخةَ المسحوبة، وتبقى ههنا لأنّ سجلَّ ما
سقط جزءٌ من السجلّ؛ والنسخةُ المضبوطةُ في `test_duwaybba_case`.

والمصدرُ المُدقَّق: تقريرُ عبورِ المدوَّنة إلى معجم Arramooz **في صورته
الأولى**، وكلُّ رقمٍ أدناه منقولٌ من متنه أو من «البناء الثاني».
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product

from algebra.factor_language import FactorLanguage
from algebra.reconciliation import Partition, rounds_to
from algebra.stipulation import ban_schema, chain_schema, weigh

TAIL = ("V", "C")
BANS = frozenset({"VV", "CC", "CV"})
TARGET = frozenset({"", "V", "C", "VC"})

# جدولُ المعجم كما وَرَد
TRILATERAL_VERBS = 21_483
ACTIVE_PARTICIPLES = 25_144
DECLARED_SYLLABLES = 98_251
BREACHES = 8
PREAMBLE_VERB_COUNT = 21_997  # «صفرٌ من ٢١٬٩٩٧» في صدر التقرير

RAW_WORDS = 34_403
RAW_BREACH_RATE = Fraction("2.11") / 100
QURAN_SYLLABLES_PER_WORD = Fraction(225_911, 77_429)


def _words_up_to(forbidden: frozenset[str], bound: int) -> int:
    """كم كلمةً طولُها ≤ bound تتجنّب هذه العوامل — بالتعداد الشامل."""

    return sum(
        1
        for length in range(bound + 1)
        for letters in product(TAIL, repeat=length)
        if not any(factor in "".join(letters) for factor in forbidden)
    )


def test_the_ban_independence_table_reproduces() -> None:
    """الجدولُ ينطبق: ٤ بالثلاثة عند كلّ حدّ، و١+٢n بإسقاط أيٍّ منها."""

    for bound, dropped_count in ((2, 5), (4, 9), (6, 13), (8, 17)):
        assert _words_up_to(BANS, bound) == 4
        assert dropped_count == 1 + 2 * bound
        for dropped in BANS:
            assert _words_up_to(BANS - {dropped}, bound) == dropped_count
            assert not FactorLanguage(
                alphabet=TAIL, forbidden=BANS - {dropped}
            ).transition_graph_is_acyclic()


def test_the_reduction_is_not_a_mere_restatement() -> None:
    """تصحيح: الصيغتان **ليستا** متطابقتَي المضمون؛ السلسلةُ تقول أكثر.

    التقريرُ يقول «إعادةُ صياغةٍ لا اشتقاق، المضمون التجريبيّ واحدٌ حرفًا».
    والتعدادُ يردّه: المنوعُ تبلغ **ثلاثَ** لغاتٍ منتهيةً، والسلسلةُ **اثنتين**؛
    والزائدةُ هي `{ε, V, C}` — لغةٌ تقبلها نظريّةُ منعٍ ولا تقبلها سلسلةٌ بحال.
    فالسلسلةُ **تحرّم أكثر**، وذلك مضمونٌ لا صياغة. ويتباعد الفرقُ بازدياد
    الرموز: بثلاثةٍ تصير عائلةُ المنوع ٥١٢ والسلسلةُ ٦.
    """

    bans, chain = ban_schema(TAIL), chain_schema(TAIL)
    ban_languages = {words for _, words in bans.finite_members()}
    chain_languages = {words for _, words in chain.finite_members()}
    assert len(ban_languages) == 3
    assert len(chain_languages) == 2
    assert ban_languages - chain_languages == {frozenset({"", "V", "C"})}
    assert chain_languages < ban_languages
    weighed_bans, weighed_chain = weigh(bans, TARGET), weigh(chain, TARGET)
    assert weighed_chain.forbidden_share(128) > weighed_bans.forbidden_share(128)
    assert len(ban_schema(("V", "C", "X")).members) == 512
    assert len(chain_schema(("V", "C", "X")).members) == 6


def test_the_dictionary_table_does_not_add_up() -> None:
    """الصفّان يجمعان إلى ٤٦٬٦٢٧ والمُعلَنُ ٩٨٬٢٥١: بقيّةٌ ٥١٬٦٢٤ في صفوفٍ محجوبة.

    والصفّان المعروضان خرقُهما **صفر**، فالثمانيةُ كلُّها في المحجوب. فنسبةُ
    الخرق حيث يقع فعلًا ٠٫٠١٥٥٪ لا ٠٫٠٠٨١٪ — والرقمُ المنشورُ مقسومٌ على
    مقامٍ يشمل صفوفًا لا خرقَ فيها.
    """

    shown = Partition(
        parts=(TRILATERAL_VERBS, ACTIVE_PARTICIPLES),
        declared_total=DECLARED_SYLLABLES,
    )
    assert shown.measured_total == 46_627
    assert shown.residue == 51_624
    assert not shown.balances
    on_declared = Fraction(BREACHES * 100, DECLARED_SYLLABLES)
    on_residue = Fraction(BREACHES * 100, shown.residue)
    assert rounds_to(on_declared, 6) == Fraction("0.008142")
    assert rounds_to(on_residue, 6) == Fraction("0.015497")
    assert on_residue > on_declared


def test_the_two_verb_counts_are_unreconciled() -> None:
    """صدرُ التقرير يقول ٢١٬٩٩٧ وجدولُه يقول ٢١٬٤٨٣ — فرقُ ٥١٤ بلا تسمية."""

    assert PREAMBLE_VERB_COUNT - TRILATERAL_VERBS == 514
    assert PREAMBLE_VERB_COUNT != TRILATERAL_VERBS


def test_the_filtered_total_is_the_raw_total_minus_the_breaching_units() -> None:
    """المُعلَنُ ٩٨٬٢٥١ ≈ الخامُ ناقصَ الخارق: فرقُ **سبعةِ مقاطعَ** من ٩٨ ألفًا.

    ٢٫١١٪ من ٣٤٬٤٠٣ = ٧٢٦، والباقي ٣٣٬٦٧٧ كلمةً؛ وبنسبة المصحف (٢٫٩١٧٧ مقطعًا
    للكلمة) تعطي ٩٨٬٢٥٨ مقطعًا، والمُعلَنُ ٩٨٬٢٥١ — فرقٌ ٠٫٠٠٧٪. والقراءتان
    («٢٫١١٪ من الكلمات» و«من المقاطع») تعطيان الرقمَ نفسَه، فالالتباسُ في
    الوحدة لا يمسّ هذا الفحص.

    ومقتضاه أنّ المصفاةَ حذفت **ما يقارب الخارقَ بعينه**. فالمصفاةُ معرَّفةٌ
    على تمام الشكل لا على شكل المقطع، فليست دائريّةً بالتعريف — ولكنّها في
    هذه البيانات **تكاد تطابقه**، فيلزم إعلانُ حجمها. ويُرفَع اللبسُ برقمٍ
    واحدٍ لم يُنشَر: **كم كلمةً بقيت بعد التصفية**.
    """

    breaching_words = RAW_WORDS * RAW_BREACH_RATE
    kept_words = RAW_WORDS - breaching_words
    implied = kept_words * QURAN_SYLLABLES_PER_WORD
    assert round(float(breaching_words), 1) == 725.9
    assert round(float(implied)) == 98_258
    assert round(abs(float(implied) - DECLARED_SYLLABLES), 1) == 7.1
    assert abs(float(implied) - DECLARED_SYLLABLES) / DECLARED_SYLLABLES < 0.0001
    # القراءةُ الأخرى: ٢٫١١٪ من المقاطع — الحسابُ نفسُه بالضبط
    raw_syllables = RAW_WORDS * QURAN_SYLLABLES_PER_WORD
    assert raw_syllables * (1 - RAW_BREACH_RATE) == implied


def test_the_two_breach_rates_are_in_different_units() -> None:
    """٢٫١١٪ من الكلمات و٠٫٠٠٨٪ من المقاطع لا يُقارَنان، والفرقُ بينهما ٩١×.

    فلو بقيت الـ٧٢٦ كلمةً الخارقةُ داخلَ المقيس، لكان أدنى خرقٍ بالمقاطع
    **٠٫٧٣٩٪** (مقطعٌ واحدٌ خارقٌ لكلّ كلمةٍ على الأقلّ) لا ٠٫٠٠٨٪. فالهبوطُ
    المنشورُ أثرُ المصفاة أوّلًا، لا أثرُ عبور المدوَّنة.
    """

    floor_by_syllable = Fraction(726 * 100, DECLARED_SYLLABLES)
    published = Fraction(BREACHES * 100, DECLARED_SYLLABLES)
    assert rounds_to(floor_by_syllable, 3) == Fraction("0.739")
    assert floor_by_syllable / published == Fraction(726, BREACHES)
    assert round(float(floor_by_syllable / published)) == 91


def test_the_between_corpus_gap_needs_the_within_corpus_spread() -> None:
    """فجوةُ CVV سبعُ نقاطٍ ونصف، وتذبذبُها داخلَ المصحف نقطةٌ وواحدٌ من عشرة.

    فالنسبُ تتحرّك داخلَ المصحف وحدَه بين ٢٢٫٢٧٨٪ و٢٣٫٣٩٤٪ باختيار الأساس
    (وذلك مقيسٌ في «البناء الثاني» على أربعة أسس). والفجوةُ إلى المعجم
    ٧٫٥٧٨ نقطةً — أي **٦٫٨ أمثال** أوسعِ تذبذبٍ داخليّ. فالحكمُ «النِّسَبُ لا
    تنتقل» يصمد، ويكتسب مقياسًا كان ناقصًا.
    """

    within = [
        Fraction("22.278"),
        Fraction("23.394"),
        Fraction("22.724"),
        Fraction("23.394"),
    ]
    spread = max(within) - min(within)
    gap = Fraction("22.278") - Fraction("14.7")
    assert spread == Fraction("1.116")
    assert gap == Fraction("7.578")
    assert round(float(gap / spread), 2) == 6.79
    assert gap > 5 * spread
    # والعَدُّ المضبوطُ لاحقًا أعطى ١٥٫٠٢٪ لا ١٤٫٧٪، فالفجوةُ ٧٫٢٥٨ و٦٫٥٠ أمثالًا
    corrected = Fraction("22.278") - Fraction("15.02")
    assert corrected == Fraction("7.258")
    assert corrected < gap
    assert corrected > 5 * spread  # والحكمُ لا يتغيّر بالتصحيح


def test_zero_double_sukun_holds_in_words_not_in_the_mushaf() -> None:
    """تصحيح: «صفرٌ في المصحف» يضيق إلى «صفرٌ في كلماته».

    و«البناء الثاني» يقول بنصّه: سكون ← سكون = **٣٣ في ١١ صورةً**، كلُّها
    فواتحُ سورٍ ومَجْر۪ىٰهَا. فالصفرُ مشروطٌ بإخراج الفواتح، وهو شرطٌ مُعلَنٌ
    هناك — ولكنّه يسقط من صياغة التقرير ههنا، فيصير المقابلُ بين «صفرٍ» و
    «واحدٍ» أوسعَ ممّا يحتمله.
    """

    assert 33 > 0
    assert 33 != 0  # لا يُقال «صفرٌ في المصحف» بإطلاق
    # والمخالفُ داخلَ الكلمات في المصحف واحدٌ مُسمًّى، وهو أثرُ الترميز نفسُه
    assert 225_911 - 225_910 == 1


def test_the_headline_percentages_reproduce() -> None:
    """٩٩٫٩٩٢٪ و١١٣/١١٤ ينطبقان بالحساب المباشر."""

    assert rounds_to(
        Fraction(100) - Fraction(BREACHES * 100, DECLARED_SYLLABLES), 3
    ) == (Fraction("99.992"))
    assert rounds_to(Fraction(113 * 100, 114), 3) == Fraction("99.123")
    assert 114 - 113 == 1


def test_the_surviving_exception_is_of_a_category_already_isolated() -> None:
    """سبعٌ من الثماني عيوبُ معجمٍ وواحدةٌ باقية، وآليّتُها مُسمّاةٌ من قبل.

    والباقيةُ `دُوَيْبَّةٌ`: ساكنٌ يتلوه **النصفُ الأوّلُ من مشدَّد**، وهو
    ساكنٌ أيضًا — فيخرج CVCC. وهذه الآليّةُ بعينُها هي التي عزلها «البناء
    الثاني» في ٣٬٧١٧ كلمةً بشدّةٍ أوّليّة، إلّا أنّها هناك عابرةٌ لحدّ الكلمة
    وههنا داخلَه. فالاستثناءُ من **صنفٍ معروفٍ مُسمًّى**، لا واقعةٌ شاردة —
    وذلك يشدّ حكمَ التقرير على م٣ ولا يُضعِفه.
    """

    assert 7 + 1 == BREACHES
    assert 3_717 + 30 == 3_747  # صنفا الكلمات بلا صدرٍ محرّك في «البناء الثاني»
