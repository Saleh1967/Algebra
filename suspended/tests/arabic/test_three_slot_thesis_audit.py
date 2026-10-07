"""أطروحةُ «حامل/حالة/زمن»: **الشاهدُ الحادُّ ينكسر، والانضباطُ يُحمَد**.

**الوثيقةُ غيرُ موجودةٍ في هذه الحاوية** (`/mnt/agents/output/` لا وجودَ
له)، فالفحصُ على ما نُقِل في المتن.

`WHAT_IS_GOOD_AND_NEW_IN_THE_DISCIPLINE`: ويُحمَد أوّلًا: **الفروضُ في §٠
قبل كلّ قانون**، وتسميةُ دوران الخانة **تفسيرًا لا برهانًا**، و**لا مجالَ
ثقةٍ لعدٍّ تامّ** (وهو صحيح: العدُّ الحاصرُ ليس معاينة)، وحسابُ الدَّينين
**بإنتروبيا مشتركةٍ لا بمجموع** — فانتقلَ إصلاحُ الجمعيّة من دورةٍ إلى
دورة. وهذه أربعةُ دروسٍ نزلت **قبل** أن تُطلَب.

`THE_SHARP_WITNESS_FOUR_EQUALS_FOUR_FAILS_ON_THE_LEFT`: و«٤ = ٤» طرفُها
الأيسرُ ليس أربعةً على المادّة المختومة: الأصنافُ المقيسةُ **سبعة**
(فتحة · ضمّة · كسرة · سكون · شدّة · تنوين · مجرَّد)، والأربعةُ تغطّي
**٦٦٫٢٦٪** فقط. والتنوينُ خاصّةً ليس تفصيلًا: هو العلامةُ التي تحمل
الإعرابَ والحركةَ معًا.

`AND_IT_FAILS_ON_THE_RIGHT_TOO_BY_CATEGORY`: والطرفُ الأيمنُ **اتّحادُ
مقولتين** لا مخزونُ مقولةٍ واحدة: الاسمُ يأخذ رفعًا ونصبًا وجرًّا (**ثلاثة**،
ولا جزمَ فيه)، والفعلُ رفعًا ونصبًا وجزمًا (**ثلاثة**، ولا جرَّ فيه). فلا
كلمةَ تأخذ الأربعةَ. والأربعةُ اليسرى **مخزونُ حرفٍ واحد**. عددان متساويان
من جنسين — والتساوي في العدد ليس تناظرًا في البناء.

`AND_THE_MAPPING_IS_NOT_A_BIJECTION_EITHER`: وثالثةٌ: العلامةُ ليست الحالة.
الرفعُ وحدَه تنوب عنه **الضمّةُ والواوُ والألفُ وثبوتُ النون**. ونيابةُ
الحروف عن الحركات بابٌ مقرَّرٌ ينقض التقابلَ الواحدَ لواحد.

`Q5_HAS_A_DIRECT_COUNTEREXAMPLE_FROM_THE_GRAMMAR`: و«الضميرُ مبنيٌّ لأنّ
الإحالةَ تستلزم مرساةً لا تتحرّك» يُنقَض بمعرَبَين إحاليَّين: **هذان /
هذين** و**اللذان / اللذين** — اسمُ إشارةٍ واسمٌ موصولٌ للمثنّى، **معرَبان**،
والغابةُ المرجعيّةُ لم تنفرط. فالبناءُ **غالبٌ لا شرطٌ وظيفيّ**.

`THE_NAMING_CLAIM_HOLDS_FOR_LETTERS_AND_NOT_FOR_MARKS`: و«أسماءُ الحروف
والحركات ثلاثيّاتٌ»: أسماءُ الحروف **ثمانيةٌ وعشرون كلُّها ثلاثيّة** —
مفحوصٌ بالعدّ ✓. وأسماءُ الحركات **ليست**: فتحة وكسرة وسكون أربعةٌ أربعة،
وضمّة ثلاثة. (وبالجذور تصدق قراءةٌ ثانية: فتح · كسر · سكن ثلاثيّة، وضمّ
مضاعف — فتُعلَن القراءةُ أيّتهما أُريدت.)

`AND_THE_THREE_COUNTS_CARRY_NO_SOURCE`: و«ربط ٨ + استفهام ٢ + إحالة ٢٨»
أعدادٌ **بلا إسناد**، و`F4` يجعلها حاملةً للقانون («الإغلاقُ يُقاس بالعدّ»).
فعددٌ حاملٌ بلا مصدرٍ هو «١٣» بعينها — وقد أُعلِن فضاءُ الاستفهام في `F1`
فسلِم، وبقي العطفُ والإحالةُ بلا إعلان.
"""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

from frozen_corpus import CORPUS, requires_corpus

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_marked_contrast.py"

LETTER_NAMES = (
    "ألف باء تاء ثاء جيم حاء خاء دال ذال راء زاي سين شين صاد ضاد "
    "طاء ظاء عين غين فاء قاف كاف لام ميم نون هاء واو ياء"
).split()
MARK_NAMES = {"فتحة": 4, "ضمة": 3, "كسرة": 4, "سكون": 4}
FOUR = ("فتحة", "ضمّة", "كسرة", "سكون")
NOUN_STATES = ("رفع", "نصب", "جرّ")
VERB_STATES = ("رفع", "نصب", "جزم")
RAF_MARKERS = ("ضمّة", "واو", "ألف", "ثبوتُ النون")
INFLECTED_REFERENTS = (("هذان", "هذين"), ("اللذان", "اللذين"))


def test_every_letter_name_is_trilateral_and_the_mark_names_are_not() -> None:
    """ثمانيةٌ وعشرون اسمًا كلُّها ثلاثيّة ✓ — وأسماءُ الحركات ليست ✗."""

    assert len(LETTER_NAMES) == 28
    assert {len(one) for one in LETTER_NAMES} == {3}
    assert set(MARK_NAMES.values()) != {3}
    assert MARK_NAMES["فتحة"] == 4


def test_no_single_category_takes_all_four_inflectional_states() -> None:
    """الاسمُ ثلاثةٌ والفعلُ ثلاثة؛ والأربعةُ اتّحادُ مقولتين لا مخزونُ واحدة."""

    assert len(NOUN_STATES) == len(VERB_STATES) == 3
    assert "جزم" not in NOUN_STATES and "جرّ" not in VERB_STATES
    union = set(NOUN_STATES) | set(VERB_STATES)
    assert len(union) == 4
    assert len(set(NOUN_STATES) & set(VERB_STATES)) == 2  # رفعٌ ونصبٌ فقط


def test_one_state_has_four_markers_so_the_mapping_is_not_one_to_one() -> None:
    """الرفعُ وحدَه أربعُ علامات — فالعلامةُ ليست الحالة."""

    assert len(RAF_MARKERS) == 4
    assert "ضمّة" in RAF_MARKERS
    assert len(set(RAF_MARKERS)) == len(RAF_MARKERS)


def test_two_inflected_referents_refute_the_necessity_in_q5() -> None:
    """هذان/هذين واللذان/اللذين معرَبان وإحاليّان — فالبناءُ غالبٌ لا شرط."""

    assert len(INFLECTED_REFERENTS) == 2
    for raised, lowered in INFLECTED_REFERENTS:
        assert raised != lowered  # تتبدّل صورتُه بموضعه
        assert raised.endswith("ان") and lowered.endswith("ين")


@requires_corpus
def test_the_left_hand_four_is_seven_on_the_sealed_corpus() -> None:
    """سبعةُ أصنافٍ مقيسة، والأربعةُ تغطّي ٦٦٫٢٦٪ — فالطرفُ الأيسرُ ليس أربعة."""

    spec = importlib.util.spec_from_file_location("run_marked_contrast", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    stream = list(module.read_stream(CORPUS.read_text(encoding="utf-8")))

    classes = Counter(kind for _, kind in stream)
    assert len(classes) == 7
    covered = Fraction(sum(classes[one] for one in FOUR), len(stream))
    assert Fraction(66, 100) < covered < Fraction(67, 100)
    # والتنوينُ خاصّةً يحمل الإعرابَ والحركةَ معًا، فخروجُه ليس تفصيلًا
    assert classes["تنوين"] > 8_000
