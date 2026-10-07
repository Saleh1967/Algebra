"""المسحُ المُسجَّلُ أُعيد قياسُه من البايتات: أربعُ مرايا تطابق، وسادستان جديدتان.

**ما جرى**: أُذِن بجلب البايتات، فرُدَّ المصدرُ القانونيُّ (`tanzil.net`)
بسياسة الشبكة في هذه البيئة. ومرايا GitHub مفتوحةٌ فجُلِبت واحدةٌ منها
واستُخرِجت **بايتاتُها** فقِيست أطوالُها وبصماتُها في هذه الشجرة.

`A_RECORDED_SURVEY_IS_WORTH_MORE_WHEN_SOMEONE_ELSE_MEASURES_IT`: وكان مسحُ
المرايا **رقمًا منقولًا عن تقرير** لا مُعادًا ههنا — كسائر ما نُنبّه عليه.
فأُعيد: أربعةُ صفوفٍ من الخمسة المُسجَّلة خرجت **مطابقةً طولًا وبصمةً**،
ولم يُعدَّل صفٌّ ولا حرف. فالسجلُّ مُصدَّقٌ من مصدرٍ ثانٍ لا من كاتبه.

`AND_THE_GATE_STAYS_SHUT_BY_MEASUREMENT_NOT_BY_REPORT`: ولا واحدةٌ من
السّتّ تبلغ ١٬٣١٩٬٩٠١ ولا تبدأ بصمتُها بـ`37633090`. فقولُ «الشبكةُ لا
تُغني» صار **مقيسًا ههنا** بعد أن كان منقولًا: البوّابةُ مغلقةٌ بالعدّ.

`TWO_ROWS_THE_SURVEY_DID_NOT_HOLD`: وخرج ملفّان لم يكونا في المسح المُسجَّل
— `quran-simple-clean.txt` و`quran-uthmani-min.txt` — فيُسمَّيان ههنا
مقيسَين لا منقولَين، ويبقى المُسجَّلُ كما هو: **الزيادةُ تُعلَن ولا تُدسّ
في سجلٍّ مختوم**.
"""

from __future__ import annotations

from alghanem.arabic.compression_model_preregistration import FROZEN_CORPUS
from alghanem.arabic.quran_corpus_word_total import SURVEYED_MIRRORS

# ما قِيس ههنا من بايتاتٍ مجلوبة: (الاسم، الطول، مقدّمةُ البصمة)
MEASURED: tuple[tuple[str, int, str], ...] = (
    ("drnesr/QuranDataset — quran-simple-enhanced.txt", 1_331_429, "31a71ecae9273530"),
    ("drnesr/QuranDataset — quran-simple.txt", 1_337_820, "7b2b601fa5e9b825"),
    ("drnesr/QuranDataset — quran-simple-min.txt", 1_160_550, "9afe44e4717223c1"),
    ("drnesr/QuranDataset — quran-uthmani.txt", 1_370_238, "9cae2cb7e075379e"),
)

# ملفّان لم يحملهما المسحُ المُسجَّل، مقيسان ههنا لا منقولان
MEASURED_BEYOND_THE_SURVEY: tuple[tuple[str, int, str], ...] = (
    ("drnesr/QuranDataset — quran-simple-clean.txt", 781_166, "151cf60e699b2479"),
    ("drnesr/QuranDataset — quran-uthmani-min.txt", 1_172_176, "988b779da45b2448"),
)


def test_four_recorded_rows_are_reproduced_byte_for_byte() -> None:
    """أربعةُ صفوفٍ من الخمسة المُسجَّلة تطابق ما قِيس ههنا، طولًا وبصمةً."""

    recorded = {
        one.mirror_name: (one.mirror_byte_length, one.mirror_sha256_prefix)
        for one in SURVEYED_MIRRORS
    }
    assert len(recorded) == 5

    for name, length, prefix in MEASURED:
        assert name in recorded, name
        assert recorded[name] == (length, prefix), name

    assert len(MEASURED) == 4
    # والخامسُ (rizaumami) لم يُجلَب ههنا، فيبقى منقولًا ولا يُدَّعى قياسُه
    unmeasured = set(recorded) - {name for name, _, _ in MEASURED}
    assert len(unmeasured) == 1
    assert "rizaumami" in next(iter(unmeasured))


def test_no_measured_mirror_opens_the_frozen_gate() -> None:
    """لا طولَ يبلغ ١٬٣١٩٬٩٠١ ولا بصمةَ تبدأ بـ`37633090` — والبوّابةُ مغلقةٌ بالعدّ."""

    assert FROZEN_CORPUS.byte_length == 1_319_901
    assert FROZEN_CORPUS.sha256_hex.startswith("37633090")

    for name, length, prefix in (*MEASURED, *MEASURED_BEYOND_THE_SURVEY):
        assert length != FROZEN_CORPUS.byte_length, name
        assert not FROZEN_CORPUS.sha256_hex.startswith(prefix), name

    lengths = {length for _, length, _ in (*MEASURED, *MEASURED_BEYOND_THE_SURVEY)}
    assert len(lengths) == 6  # ستُّ مدوّناتٍ متمايزةٌ بأطوالها، ولا واحدةَ هي المطلوبة


def test_the_two_new_rows_are_declared_and_not_folded_into_the_record() -> None:
    """الزيادةُ تُعلَن في جدولها ولا تُدسّ في سجلٍّ مختومٍ كُتِب قبلها."""

    recorded = {one.mirror_name for one in SURVEYED_MIRRORS}
    for name, _, _ in MEASURED_BEYOND_THE_SURVEY:
        assert name not in recorded, name

    assert len(MEASURED_BEYOND_THE_SURVEY) == 2
    assert len(SURVEYED_MIRRORS) == 5  # والسجلُّ لم يُمَسّ


def test_every_prefix_is_sixteen_hexadecimal_places() -> None:
    """مقدّماتُ البصمات ستَّ عشرةَ خانةً ستّةَ عشريّة، ولا واحدةَ تتكرّر."""

    prefixes = [prefix for _, _, prefix in (*MEASURED, *MEASURED_BEYOND_THE_SURVEY)]
    assert len(set(prefixes)) == len(prefixes) == 6
    for prefix in prefixes:
        assert len(prefix) == 16
        assert set(prefix) <= set("0123456789abcdef")
