"""الاتّفاقُ مقيسًا على الملفّين: ثلاثةٌ تُصدَّق، وواحدٌ يُنقَض بمقامه.

**ما جرى**: قرأتُ الملفّين المُرسَلين ووصَلتهما على `(سورة، آية، كلمة)`
وحسبتُ الاتّفاقَ بجدول المقابلة المسجَّل قبل النظر. والبصمتان:
`265a30b6…` لـQAC و`3fa9a1be…` للجدول. والملفّان **لا يُودَعان** ههنا —
متناهما لناشريهما — وإنّما تُودَع أرقامُ التشغيل وبصمتُ مصدرها.

`THREE_OF_FOUR_REPRODUCE_TO_THE_LAST_DIGIT`: حجمُ الوصل **٦٬٦٢٠** كما قِيل،
و«على الكلّ» **٥١٫٢٨٪** وكابّا **+٠٫٤٤٢٥** كما قِيلا، والسبعةُ سطرًا كلُّها
تُعاد إلى منزلتين. فالقياسُ مُصدَّقٌ بحسابٍ مستقلّ.

`THE_FOURTH_IS_A_THIRD_DENOMINATOR_NOT_A_SECOND`: وأمّا «على المشمول» فمقامُه
**٤٬٩٦٥**، وهو عددُ ما وسمُ **QAC وحدَه** داخلَ جرده — لا ما وسمُ الطرفين
داخلَ الجردين، وذلك **٤٬٢٧٢**. والبسطُ في الثلاثة **٣٬٣٩٥ بعينه**:

    ٣٣٩٥ / ٤٢٧٢ = ٧٩٫٤٧٪ · كابّا +٠٫٧٣٤٥   ← الجردان معًا
    ٣٣٩٥ / ٤٩٦٥ = ٦٨٫٣٨٪ · كابّا +٠٫٦١٠٢   ← جردُ QAC وحدَه (المنشور)
    ٣٣٩٥ / ٦٦٢٠ = ٥١٫٢٨٪ · كابّا +٠٫٤٤٢٥   ← الوصلُ كلُّه

`THE_VERDICT_ON_A_SEALED_PREDICTION_TURNS_ON_THAT_CHOICE`: والتنبّؤ (ج) حدُّه
[٠٫٣٠ ، ٠٫٧٠]. فعلى المقام المنشور **متحقّق** (+٠٫٦١٠٢)، وعلى الجردين معًا
**ساقط** (+٠٫٧٣٤٥ فوق ٠٫٧٠). ولم يبلغ ٠٫٨٠ في أيٍّ منهما، **فالخلاصةُ
باقية**: الممتحِنان مستقلّان. والساقطُ **التنبّؤُ لا الخلاصة**، وذلك هو
الفرقُ الذي يُحفَظ.

`THE_FILES_ARE_A_SUBSET_OF_THE_PUBLISHED_CENSUS`: وكلُّ وسمٍ في الملفّين
**دون** عدده المنشور: خمسةُ وسومِ QAC ١٦٬٣٦٦ مقابلَ ٢٣٬٧٣٥، وعشرةُ وسوم
الجدول ١٥٬٥٦٦ مقابلَ ٢١٬١١٣. وخمسةَ عشرَ فرقًا **كلُّها في اتّجاهٍ واحد** —
وتلك صورةُ جزءٍ لا صورةُ خطأ. فالأرقامُ ههنا على الجزء المُرسَل، والتغطياتُ
المنشورةُ على الكلّ، ولا تُخلَط الاثنتان.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.reconciliation import Partition, rounds_to

QAC_DIGEST = "265a30b69b9f95e57f7884fd7b4946eb2a5374cdc20db07fb87238a5e5fe59de"
BOOK_DIGEST = "3fa9a1bee07abcb18b7c7038b9f70682c7f86d3cfe09c3201b78a081aa7a6fab"

QAC_ROWS, BOOK_ROWS = 23_754, 16_243
JOIN = 6_620
NUMERATOR = 3_395

BOTH, QAC_ONLY, ALL = 4_272, 4_965, 6_620
OUTSIDE_QAC_IN_JOIN, OUTSIDE_BOOK_IN_JOIN = 1_655, 1_456

KAPPA = {
    "الجردان معًا": Fraction("0.7345"),
    "جردُ QAC وحدَه": Fraction("0.6102"),
    "الوصلُ كلُّه": Fraction("0.4425"),
}

# (مصاب، مقام) لكلّ سطرٍ من جدول المقابلة المسجَّل
BY_ROW: dict[str, tuple[int, int]] = {
    "subj↔فاعل": (1_263, 1_398),
    "obj↔مفعول به": (876, 1_103),
    "poss↔مضاف إليه": (600, 774),
    "conj↔معطوف": (62, 90),
    "adj↔نعت": (318, 543),
    "pred↔خبر": (261, 447),
    "gen↔مضاف إليه": (15, 610),
}

SEALED_RANGE = (Fraction("0.30"), Fraction("0.70"))
INDEPENDENCE_ALARM = Fraction("0.80")


def test_the_join_is_the_first_number_and_it_reproduces() -> None:
    """٦٬٦٢٠ — محسوبًا بالوصل لا مشتقًّا من تغطيتين، ومطابقًا للمنشور."""

    assert JOIN == 6_620
    assert JOIN < min(QAC_ROWS, BOOK_ROWS)
    assert JOIN > 5_000  # فليس «ضعيفًا» بحدّ التسجيل

    # والتنبّؤ (أ) «> ١٠٬٠٠٠» ساقطٌ، وقد أُعلِن قبل أن يُسأل عنه
    assert JOIN < 10_000


def test_one_numerator_carries_three_denominators() -> None:
    """٣٬٣٩٥ إصابةً في الثلاثة؛ والذي يتغيّر المقامُ وحدَه."""

    assert BOTH < QAC_ONLY < ALL
    assert ALL - OUTSIDE_QAC_IN_JOIN == QAC_ONLY

    # والفرقُ بين المقامين الأضيقين ٦٩٣: صفوفٌ وسمُ QAC فيها داخلٌ ووسمُ
    # الجدول خارج. وهي دونَ ١٬٤٥٦ لأنّ بعضَ الخارجِ من الجدول خارجٌ من
    # الطرفين معًا، فلا يدخل المقامَ الثاني أصلًا.
    assert QAC_ONLY - BOTH == 693
    assert 0 < QAC_ONLY - BOTH < OUTSIDE_BOOK_IN_JOIN
    assert OUTSIDE_BOOK_IN_JOIN - (QAC_ONLY - BOTH) == 763

    rates = {
        name: Fraction(NUMERATOR, denominator)
        for name, denominator in (("معًا", BOTH), ("QAC", QAC_ONLY), ("الكلّ", ALL))
    }
    assert rounds_to(rates["معًا"] * 100, 2) == Fraction("79.47")
    assert rounds_to(rates["QAC"] * 100, 2) == Fraction("68.38")
    assert rounds_to(rates["الكلّ"] * 100, 2) == Fraction("51.28")

    # وبين أوسعِ النسب وأضيقها ثمانٍ وعشرون نقطة، ببسطٍ لم يتحرّك
    assert rounds_to((rates["معًا"] - rates["الكلّ"]) * 100, 2) == Fraction("28.19")


def test_the_sealed_prediction_on_kappa_turns_on_the_denominator() -> None:
    """[٠٫٣٠ ، ٠٫٧٠]: متحقّقٌ على المقام المنشور، ساقطٌ على الجردين معًا."""

    low, high = SEALED_RANGE
    assert low <= KAPPA["جردُ QAC وحدَه"] <= high
    assert not (low <= KAPPA["الجردان معًا"] <= high)
    assert KAPPA["الجردان معًا"] > high
    assert low <= KAPPA["الوصلُ كلُّه"] <= high

    # ولم يبلغ أيٌّ منها حدَّ الإنذار، فالخلاصةُ باقيةٌ والساقطُ التنبّؤ
    assert max(KAPPA.values()) < INDEPENDENCE_ALARM
    assert INDEPENDENCE_ALARM - max(KAPPA.values()) == Fraction("0.0655")


def test_every_row_of_the_sealed_mapping_reproduces() -> None:
    """سبعةُ أسطرٍ، وكلُّها تُعاد إلى منزلتين من أرقام الملفّين."""

    published = {
        "subj↔فاعل": "90.34",
        "obj↔مفعول به": "79.42",
        "poss↔مضاف إليه": "77.52",
        "conj↔معطوف": "68.89",
        "adj↔نعت": "58.56",
        "pred↔خبر": "58.39",
        "gen↔مضاف إليه": "2.46",
    }
    assert set(published) == set(BY_ROW)
    for name, (hits, total) in BY_ROW.items():
        assert rounds_to(Fraction(hits, total) * 100, 2) == Fraction(published[name])

    # ومجموعُ الأسطر هو البسطُ والمقامُ الثاني بعينهما
    assert sum(hits for hits, _ in BY_ROW.values()) == NUMERATOR
    assert sum(total for _, total in BY_ROW.values()) == QAC_ONLY


def test_the_fourth_prediction_holds_by_a_factor_of_twenty_four() -> None:
    """`gen` أدنى الأسطر، ودونَ أقربِها بأربعةٍ وعشرين ضعفًا — لا بفارقٍ طفيف."""

    rates = {name: Fraction(hits, total) for name, (hits, total) in BY_ROW.items()}
    lowest = min(rates, key=lambda name: rates[name])
    assert lowest == "gen↔مضاف إليه"

    others = [value for name, value in rates.items() if name != lowest]
    assert rates[lowest] * 23 < min(others)
    assert round(float(min(others) / rates[lowest]), 1) == 23.7

    # والسببُ مقروءٌ من الزوج: `poss` هو المضافُ إليه، و`gen` المجرورُ بالحرف
    assert rates["poss↔مضاف إليه"] > rates[lowest] * 30


def test_the_delivered_files_are_a_subset_of_the_published_census() -> None:
    """خمسةَ عشرَ فرقًا كلُّها في اتّجاهٍ واحد — صورةُ جزءٍ لا صورةُ خطأ."""

    qac_published, qac_in_file = 23_735, 16_366
    book_published, book_in_file = 21_113, 15_566
    assert qac_in_file < qac_published
    assert book_in_file < book_published

    assert (
        Partition(
            parts=(qac_in_file, qac_published - qac_in_file),
            declared_total=qac_published,
        ).residue
        == 0
    )
    assert qac_published - qac_in_file == 7_369
    assert book_published - book_in_file == 5_547

    # والملفّان أنفسُهما أوسعُ من الجردين، إذ فيهما وسومٌ خارجَهما
    assert QAC_ROWS > qac_in_file
    assert BOOK_ROWS > book_in_file


def test_the_source_is_named_by_digest_not_by_title() -> None:
    """بصمتان تُودَعان والملفّان لا يُودَعان؛ فالمتنُ لناشره والرقمُ لمصدره."""

    for digest in (QAC_DIGEST, BOOK_DIGEST):
        assert len(digest) == 64
        assert digest == digest.lower()
        assert set(digest) <= set("0123456789abcdef")
    assert QAC_DIGEST != BOOK_DIGEST
