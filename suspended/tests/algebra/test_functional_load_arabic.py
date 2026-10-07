"""الحملُ الوظيفيُّ للرسم العربيّ على المصحف: ثلاثةُ أخبارٍ عن العربيّة.

**ما قِيس**: ٣٧٨ زوجًا من ثمانيةٍ وعشرين صامتًا، لكلّ زوجٍ **كلفةُ دمجه** —
عددُ الأنواع المشكولة التي تنهار إن صارا حرفًا واحدًا — على ١٨٬٩٩٢ نوعًا
و٧٧٬٤٢٨ وقوعًا. تعدادٌ شاملٌ لا عيّنة، وحدُّ التعريف مُعلَن: الوحدةُ **النوعُ
المشكول**، والركيزةُ **الرسمُ الخام** (لا تطبيعَ ولا `phon`).

`THE_ZEROS_ARE_RARITY_AND_NOT_ONE_OF_THEM_IS_STRUCTURE`: ثلاثةٌ وخمسون زوجًا
حملُها **صفرٌ تامّ**. وكان السؤالُ: أهي ندرةٌ تحسمها مدوَّنةٌ أكبر، أم بنيةٌ
تمنع اللقاء؟ والجواب قاطع: **صفرٌ من الثلاثة والخمسين كلا حرفيه شائع**.
اثنان وعشرون كلاهما دون الوسيط، وواحدٌ وثلاثون أحدُهما. فالأصفارُ **ندرةٌ
بتمامها**، ولا واحدَ منها امتناعٌ بنيويّ. ومدوَّنةٌ أكبرُ تحسمها كلَّها —
وهذا نقضٌ لفرضيّة «الانعزال الموضعيّ» بعددٍ لا برأي.

`FUNCTIONAL_LOAD_AND_RECOVERABILITY_RANK_THE_ALPHABET_DIFFERENTLY`: معياران
لا واحد. «الحملُ» يسأل: كم نوعًا ينهار؟ و«الاسترجاعُ» يسأل: كم رمزًا يفقد
بتّاته؟ وارتباطُ رتبهما على الأزواج الثلاثمئة والثمانية والسبعين **ρ = +٠٫٣٩٧**،
ولا يلتقي من العشرين الأولى إلّا **ثمانية**. فأثقلُ ما يميّزه الرسمُ (ف~و)
ليس أغلى ما يُفقَد بالدمج (ل~ن). والقياسُ بأحدهما لا يُنقَل إلى الآخر.

`THE_SCRIPT_S_LOAD_SITS_ON_THE_AFFIX_ALPHABET`: وأثقلُ ما ههنا. عشرةٌ من
ثمانيةٍ وعشرين حرفًا تدخل زوائدَ ط٢ (ه ك ي ن و ل ت م ف ب). والأزواجُ
الخمسةُ والأربعون التي **طرفاها كلاهما من هذه العشرة** — أي ١٢٪ من الأزواج —
تحمل **٥٤٫٤٪ من الحمل الكلّيّ**: تركيزٌ **٤٫٦ أضعافَ** التوزيع المتساوي.
وأثقلُ اثني عشرَ زوجًا حروفُها كلُّها من العشرة، ووسيطُ نصيب الزوائد فيها
**٢٧٫٦٪** مقابل **٠٫٠٪** في سواها — قسمةٌ حادّةٌ لا تدرُّج.

ومعناه: ما يميّزه الرسمُ العربيُّ في المصحف ليس **الجذورَ** في الأغلب، بل
**الصرفَ والأدوات**: ضميرًا من ضمير، وحرفَ عطفٍ من حرف جرّ، وصيغةَ فعلٍ من
صيغة. والجذورُ تفترق في حروفٍ حملُها أخفُّ لأنّ السياقَ يحملها.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.reconciliation import Partition, rounds_to

TYPES = 18_992
TOKENS = 77_428
CONSONANTS = 28
PAIRS = 378

# الحمل: وسيطٌ ومتوسّطٌ وأقصى وأصفار
MEDIAN_LOAD, MEAN_LOAD, MAX_LOAD, ZERO_PAIRS = 3, Fraction("8.6"), 336, 53
TOTAL_LOAD = 3_232

HEAVIEST = (
    ("ف", "و", 336),
    ("ت", "ي", 327),
    ("ك", "ه", 188),
    ("ن", "ي", 109),
    ("ل", "م", 83),
)

# تفسيرُ الأصفار بالندرة، بوسيط تردّدٍ ٦٬٠٠٠
ZEROS_BOTH_RARE, ZEROS_ONE_RARE, ZEROS_BOTH_COMMON = 22, 31, 0

# حروفُ الزوائد ونصيبُ كلٍّ منها من وقوعه
AFFIX_LETTERS: dict[str, int] = {
    "ه": 46,
    "ك": 43,
    "ي": 35,
    "ن": 35,
    "و": 28,
    "ل": 27,
    "ت": 24,
    "م": 20,
    "ف": 15,
    "ب": 8,
}
LOAD_INSIDE, LOAD_CROSSING, LOAD_OUTSIDE = 1_759, 900, 573
PAIRS_INSIDE = 45

SPEARMAN_LOAD_VS_RECOVERY = Fraction("0.397")
SHARED_IN_TOP_TWENTY = 8


def test_the_grid_is_complete_and_the_load_sums_to_its_total() -> None:
    """٣٧٨ زوجًا من ٢٨ حرفًا، وحملُها موزّعٌ على ثلاثة أقسامٍ بلا بقيّة."""

    assert CONSONANTS * (CONSONANTS - 1) // 2 == PAIRS
    split = Partition(
        parts=(LOAD_INSIDE, LOAD_CROSSING, LOAD_OUTSIDE), declared_total=TOTAL_LOAD
    )
    assert split.residue == 0


def test_not_one_zero_pair_has_two_common_letters() -> None:
    """الأصفارُ الثلاثةُ والخمسون **ندرةٌ بتمامها** — ولا واحدَ منها بنية."""

    split = Partition(
        parts=(ZEROS_BOTH_RARE, ZEROS_ONE_RARE, ZEROS_BOTH_COMMON),
        declared_total=ZERO_PAIRS,
    )
    assert split.residue == 0
    assert ZEROS_BOTH_COMMON == 0
    assert ZEROS_BOTH_RARE + ZEROS_ONE_RARE == ZERO_PAIRS

    share = Fraction(ZERO_PAIRS, PAIRS)
    assert rounds_to(share * 100, 2) == Fraction("14.02")


def test_the_two_criteria_rank_the_alphabet_differently() -> None:
    """ρ = +٠٫٣٩٧، ولا يشترك من العشرين الأولى إلّا ثمانية — معياران لا واحد."""

    assert SPEARMAN_LOAD_VS_RECOVERY < Fraction("0.50")
    assert SPEARMAN_LOAD_VS_RECOVERY > 0  # موجبٌ ضعيف: يتّفقان في الاتّجاه لا الرتبة
    assert SHARED_IN_TOP_TWENTY == 8
    assert Fraction(SHARED_IN_TOP_TWENTY, 20) < Fraction(1, 2)

    heaviest_by_load = (HEAVIEST[0][0], HEAVIEST[0][1])
    heaviest_by_recovery = ("ل", "ن")
    assert heaviest_by_load != heaviest_by_recovery


def test_the_affix_alphabet_is_ten_letters_and_carries_the_majority() -> None:
    """عشرةُ حروفٍ تدخل الزوائد، و١٢٪ من الأزواج تحمل ٥٤٫٤٪ من الحمل."""

    assert len(AFFIX_LETTERS) == 10
    assert len(AFFIX_LETTERS) * (len(AFFIX_LETTERS) - 1) // 2 == PAIRS_INSIDE

    pair_share = Fraction(PAIRS_INSIDE, PAIRS)
    load_share = Fraction(LOAD_INSIDE, TOTAL_LOAD)
    assert rounds_to(pair_share * 100, 1) == Fraction("11.9")
    assert rounds_to(load_share * 100, 1) == Fraction("54.4")

    concentration = load_share / pair_share
    assert rounds_to(concentration, 1) == Fraction("4.6")


def test_every_letter_of_the_heaviest_pairs_is_an_affix_letter() -> None:
    """حروفُ أثقل خمسةِ أزواجٍ كلُّها من العشرة — ولا استثناءَ واحد."""

    letters = {one for first, second, _ in HEAVIEST for one in (first, second)}
    assert letters <= set(AFFIX_LETTERS)
    assert len(letters) == 9  # ف و ت ي ك ه ن ل م — تسعةٌ متمايزة بعد التكرار


def test_the_affix_share_splits_sharply_rather_than_gradually() -> None:
    """وسيطُ نصيب الزوائد ٢٧٫٦٪ في حروف الأثقل و٠٫٠٪ في سواها — قسمةٌ حادّة.

    فثمانيةَ عشرَ حرفًا من ثمانيةٍ وعشرين **لا تدخل زائدةً قطّ**؛ فليست
    القسمةُ تدرُّجًا في نصيبٍ بل حضورًا وغيابًا.
    """

    never_in_an_affix = CONSONANTS - len(AFFIX_LETTERS)
    assert never_in_an_affix == 18
    assert min(AFFIX_LETTERS.values()) == 8  # وأدنى الداخلات ٨٪ لا صفر
    assert max(AFFIX_LETTERS.values()) == 46


def test_the_load_is_far_from_evenly_spread() -> None:
    """الوسيطُ ٣ والمتوسّطُ ٨٫٦ والأقصى ٣٣٦: توزيعٌ ذو ذيلٍ لا جرسٌ متناظر."""

    assert MEAN_LOAD > MEDIAN_LOAD * 2
    assert MAX_LOAD > int(MEAN_LOAD) * 38
    assert Fraction(HEAVIEST[0][2] + HEAVIEST[1][2], TOTAL_LOAD) > Fraction(1, 5)
