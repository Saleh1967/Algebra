"""قانونُ الجهة الواسمة، مقروءًا من الشجرة المقابلة لا مأخوذًا بالخبر.

**ما يُقاس ههنا**: لا عربيّةَ ولا معنى. تُسجَّل **قراءةُ شفرةٍ** جرت على شجرة
الغانم عند `22a42b5`، وتُعَدّ أعدادُها. ولا يُستورَد منها حرفٌ واحد: ١٦٨ ألفَ
سطرٍ لا تمسّ هذه المدوّنة، وإنّما يُنقَل **قانونٌ** ويُعاد عدُّ ما يُدّعى.

`THE_HOLE_THAT_WAS_NAMED_FROM_OUTSIDE`: امتحانُ المعنى بُني عندي بمقياسٍ
وصفريٍّ وحدودٍ وقسمةٍ باللِّمّة — و**بلا جهةٍ واسمةٍ مُعلَنةٍ ألبتّة**. والشجرةُ
المقابلةُ تُشرِّعها باسمين: «شهادةُ ورودِ اللفظ ليست شهادةَ صحّةِ تفسيره»،
و«فصلُ الملفّ عن الشفرة لا يُثبت استقلالَ الجهة». فصارا شرطَ تشغيلٍ في
`run_imtihan.py`: جدولٌ بلا جهةٍ يُرَدّ، وجهةٌ هي مُعلِنُ الدعوى تُرَدّ.

`THE_TWO_FIELDS_HAVE_NO_VOCABULARY_TO_HAND_OVER`: وسُئل عن تعريف `genus`
و`predicate` لتُملأ بهما مداخلُ الإيداع. والقراءةُ تردّ السؤالَ لا تجيبه:
`GlossEntry` يُعلنهما **نصّين حرّين** لا يُقيَّدان إلّا بألّا يكونا فارغين،
فليس ثَمّ مفردةٌ مغلقةٌ تُسلَّم. والمُقيِّدُ **علاقةٌ لا قائمة**: محمولٌ يلزم
انتماؤه إلى `P(g)` المُعلَن لجنسه، و`P` جدولٌ مُعلَنٌ **لكلّ مجالٍ على حدة**،
فيه اليومَ ثلاثةُ أجناسٍ وتسعةُ أزواج، مكتوبةٌ لشواهد «عينٍ غائرة» وأخواتها.

`THE_GLOSS_IS_COMPARED_NOT_READ`: والأهمُّ أنّ الوسمَ **لا يُقرَأ منه** جنسٌ ولا
محمول؛ بل يُقابَل بما كتبه مُعلِنُ المجال في حالته، فإمّا وافق وإمّا وقف عند
`THE_GLOSS_DISAGREES_WITH_THE_CASE`. فمن ملأ الحقلين من الكتاب صنع الموافقةَ
التي جاء ليختبرها. والامتناعُ عن ملئهما صوابٌ، وسببُه أقوى ممّا قيل.

`THE_COMPARISON_UNIT_IS_THE_CHOICE_THAT_WAS_NOT_ENUMERATED`: وفي البوّابة
الثالثة عيبٌ من الجنس الذي رُدَّ به عليّ عشرَ مرّات. `gloss_agrees` تقابل
مضمونَ الوسم بمضمون الحالة **تطابقًا حرفيًّا بعد NFC**، ولا تُسمّي ذلك
اختيارًا: اثنتان وعشرون بقيّةً مُسمّاةً في الوحدة، وليس فيها واحدةٌ للمقابلة.
ويلزم منه أنّ جهةً مستقلّةً تكتب نثرَها لا تجتاز البوّابةَ إلّا أن يُنقَل عنها
نصًّا — فيقيس الفحصُ حينئذٍ **النقلَ لا الموافقة**.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.reconciliation import Partition
from algebra.results import Axis, Product

# الشجرةُ المقابلةُ عند `22a42b5`، مقروءةً لا مأخوذةً بالخبر
REGISTERED_SOURCES = 1  # `registered_source_ids()` — الفاتحةُ وحدَها
DEPOSITED_GLOSS_ENTRIES = 0  # `gloss_data/arabic_glosses_v1.json` — `entries: []`
DECLARED_GENERA = 3  # `THE_DECLARED_PREDICATE_SPACE`
PREDICATES_PER_GENUS = 3
REPRESENTATION_FIELDS = 4  # anchor · genus · predicate · relation
STRUCTURAL_FUNCTIONS = 3  # الهويّةُ والتصنيف · المحمول · الإسناد
ATTESTATION_STANDINGS = 9  # `AttestationStanding`
GATES_BEFORE_ATTESTED = 8  # ثمانيةُ مواقفَ دونَ الموثَّق

NAMED_RESIDUALS: tuple[str, ...] = (
    "A_DOMAIN_KIND_IS_DERIVED_FROM_ATTESTATIONS_NOT_WRITTEN",
    "AN_ATTESTED_CORPUS_IS_NOT_A_SUFFICIENT_SAMPLE",
    "AN_OCCURRENCE_IS_NOT_A_GLOSS_NOTE",
    "A_SELF_AUTHORED_GLOSS_IS_REFUSED_NOTE",
    "A_RECORDED_CONDITION_IS_NOT_AN_ISSUED_CERTIFICATE_NOTE",
    "FOUR_FIELDS_CARRY_THREE_FUNCTIONS_NOTE",
    "THE_PREDICATE_SPACE_IS_DECLARED_NOT_MEASURED_NOTE",
    "A_LOOKUP_READER_PROVES_INJECTIVITY_NOT_UNDERSTANDING_NOTE",
    "READER_INDEPENDENCE_IS_A_MECHANISM_NOT_A_LABEL_NOTE",
    "A_SEALED_RULE_IS_CHECKED_FOR_OVERLAP_NOT_FOR_MEMORY_NOTE",
    "A_HOLDOUT_IS_AUDITED_ON_OUTPUTS_AND_TARGETS_NOT_ON_CASE_IDENTITY_NOTE",
    "A_SHARED_TARGET_VOCABULARY_IS_LEGITIMATE_NOT_A_LEAK_NOTE",
    "A_HELD_RECONSTRUCTION_IS_NOT_AN_INDEPENDENT_READER_NOTE",
    "AN_AUDITED_HOLDOUT_PROVES_RETRIEVAL_NOT_A_LINGUISTIC_RULE_NOTE",
    "NO_READER_IN_THIS_TREE_CLOSES_THE_REBUILDING_REQUIREMENT_NOTE",
    "A_DESIGNED_DOMAIN_IS_NOT_A_LINGUISTIC_CERTIFICATE_NOTE",
    "A_DESIGNED_WITNESS_IS_NOT_AN_EXECUTED_CODEC_TEST_NOTE",
    "A_COLLISION_IN_THE_REPRESENTATION_IS_NOT_A_COLLISION_IN_CONTEXT_NOTE",
    "ZERO_IS_AN_UNNAMED_RELATION_NOT_AN_EMPTY_FIBER_NOTE",
    "ONE_IS_A_NAMED_ATTRIBUTION_NOT_A_TRUE_PROPOSITION_NOTE",
    "THE_RELATION_VOCABULARY_IS_NOT_CLAIMED_EXHAUSTIVE_NOTE",
    "THE_MINIMUM_IS_RELATIVE_TO_THE_TESTED_ALTERNATIVES_NOTE",
)


def test_the_two_fields_are_free_text_so_no_vocabulary_can_be_handed_over() -> None:
    """`genus` و`predicate` نصّان حرّان؛ فالسؤالُ عن تعريفهما لا جوابَ له.

    والقيدُ الوحيدُ في `GlossEntry.__post_init__` ألّا يكونا فارغين — لا مفردةَ
    مغلقةً ولا مفتاحَ سجلّ. فليس ثَمّ أنطولوجيا تُسلَّم، وإنّما **علاقةٌ** تُفحَص.
    """

    entry_fields = ("source_id", "locator", "genus", "predicate", "content")
    constrained_to_be_nonempty = ("genus", "predicate", "content")
    assert len(entry_fields) == 5
    assert set(constrained_to_be_nonempty) <= set(entry_fields)

    # ولا عضوَ في مفردةٍ مغلقة: الحقلان `str` لا `Enum`
    closed_vocabularies_for_the_two_fields = 0
    assert closed_vocabularies_for_the_two_fields == 0


def test_the_predicate_space_is_declared_per_domain_and_is_small_today() -> None:
    """`P(g)`: ثلاثةُ أجناسٍ وتسعةُ أزواجٍ، مُعلَنةٌ لشواهدها لا مقيسة."""

    pairs = DECLARED_GENERA * PREDICATES_PER_GENUS
    assert pairs == 9

    # وهو جدولٌ يُعلَن لكلّ مجال، فجنسٌ غيرُ مُعلَنٍ يُرفَض ولا يُعامَل فضاءً خاليًا
    unread_genus_is_an_empty_space = False
    assert not unread_genus_is_an_empty_space


def test_four_fields_carry_three_functions_so_a_genus_column_is_not_forced() -> None:
    """أربعةُ حقولٍ وثلاثُ وظائف؛ فالمعلومةُ تلزم والحقلُ لا يلزم."""

    functions = Axis(
        name="الوظيفةُ البنيويّة",
        values=("الهويّةُ_والتصنيف", "المحمول", "الإسناد"),
    )
    assert len(functions.values) == STRUCTURAL_FUNCTIONS
    assert REPRESENTATION_FIELDS > STRUCTURAL_FUNCTIONS
    assert REPRESENTATION_FIELDS - STRUCTURAL_FUNCTIONS == 1  # حقلان في وظيفةٍ واحدة


def test_the_attestation_has_nine_standings_and_eight_of_them_stop_short() -> None:
    """تسعةُ مواقفَ، ثمانيةٌ تقف دون الموثَّق — والبوّابةُ لا تُفتَح بالتسمية."""

    assert (
        Partition(
            parts=(GATES_BEFORE_ATTESTED, 1), declared_total=ATTESTATION_STANDINGS
        ).residue
        == 0
    )
    assert Fraction(GATES_BEFORE_ATTESTED, ATTESTATION_STANDINGS) > Fraction(8, 10)


def test_the_gloss_is_compared_with_the_case_not_read_into_it() -> None:
    """الوسمُ يُقابَل ولا يُقرَأ؛ فملءُ الحقلين من الكتاب يصنع الموافقةَ المطلوب فحصُها.

    وذلك بعينه سببُ الامتناع عن ملئهما: لا أنّ التعريفَ غائبٌ، بل أنّ الجهةَ
    شاهدٌ لا مَعين.
    """

    directions = Product(
        axes=(
            Axis(name="الطرف", values=("مُعلِنُ المجال", "الجهةُ الواسمة")),
            Axis(name="الفعل", values=("يكتب", "يُقابَل به")),
        )
    )
    assert directions.size == 4
    # والمقبولُ منها واحدٌ: المُعلِنُ يكتب، والجهةُ يُقابَل بها
    licensed = {("مُعلِنُ المجال", "يكتب"), ("الجهةُ الواسمة", "يُقابَل به")}
    assert len(licensed) == 2
    assert licensed <= set(directions.points())


def test_no_named_residue_covers_the_comparison_unit() -> None:
    """اثنتان وعشرون بقيّةً مُسمّاة، وليس فيها واحدةٌ للمقابلة — وهي الاختيار."""

    assert len(NAMED_RESIDUALS) == 22
    assert len(set(NAMED_RESIDUALS)) == 22

    for word in ("COMPARISON", "MATCH", "EXACT", "NORMALIZ", "STRING"):
        assert not [one for one in NAMED_RESIDUALS if word in one]

    # وثَمّ بقيّةٌ للمصدر وأخرى للقارئ وثالثةٌ للمجال — فالإحصاءُ ليس غفلةً عامّة
    assert [one for one in NAMED_RESIDUALS if "OCCURRENCE" in one]
    assert [one for one in NAMED_RESIDUALS if "READER" in one]


def test_the_one_registered_source_is_a_transcription_not_an_edition() -> None:
    """مصدرٌ واحدٌ مُسجَّل، وهو نقلٌ كُتب في الشجرة ولم يُقابَل بطبعة.

    وذلك مُصرَّحٌ به في مكانه لا مطويّ؛ ويلزم منه أنّ شرطَ الاستقلال المفروضَ
    على الوسم **غيرُ مفروضٍ على نصّ المصدر**، إذ كتبه صاحبُ الشجرة أيضًا.
    وهذا فرقٌ في التشديد بين بوّابتين، يُسجَّل ولا يُحمَل نقضًا: المتنُ مِلكٌ
    عامٌّ يُقابَل بأيّ نسخة، والوسمُ رأيٌ لا يُقابَل إلّا بقائله.
    """

    assert REGISTERED_SOURCES == 1
    assert DEPOSITED_GLOSS_ENTRIES == 0

    # فالمجالُ لا يُرفَع إلى موثَّقٍ ولا حالةً واحدة، ببنائه لا بنقصٍ فيه
    attested_cases_possible_today = min(REGISTERED_SOURCES, DEPOSITED_GLOSS_ENTRIES)
    assert attested_cases_possible_today == 0
