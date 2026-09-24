"""أوّلُ تشغيلٍ لتعداد الانتقالات على نصٍّ عربيٍّ **مُودَعٍ فعلًا** — لا على المصحف.

**ما هذا النصّ وما ليس هو**: سورةُ الفاتحة بآياتها السبع، مُودَعةً في
`alghanem.arabic.fatiha_source_text` **نقلًا لم يُقابَل**: متنٌ مِلكٌ عامّ،
برسمٍ إملائيٍّ لا عثمانيّ، لم يُقابَل بشاهدٍ رقميٍّ ولا بمصحفٍ مطبوع. وقد
صرّحت وحدتُه بذلك في `TRANSCRIPTION_STANDING`، فكلُّ رقمٍ ههنا **عن هذا
النقل** لا عن مصحفٍ ولا عن طبعةٍ مُسمّاة.

`THE_MACHINE_RUNS_ON_WHAT_EXISTS_AND_SAYS_WHAT_IT_RAN_ON`: وشُغِّلت الآلةُ
عليه لأنّه المتنُ العربيُّ الوحيدُ المُودَعُ في هذه الشجرة. فالمخرَجُ أوّلُ
رقمِ انتقالٍ يخرج منها من نصٍّ حاضرٍ ببصمته — وسَعَتُه تسعٌ وعشرون كلمة.

`MOST_OF_THE_EMPTINESS_HERE_IS_FORCED_BY_THE_DENOMINATOR_NOT_BY_THE_LANGUAGE`:
وأثقلُ ما يُقال في هذا الرقم: من ٤٤١ خانةً خلت ٣٧٥. و**٣٢٧ منها لا يمكن
أن تمتلئ أصلًا**، إذ المواضعُ ١١٤ فلا تُشغَل أكثرُ من ١١٤ خانة. فالخالي
الذي يحتمل أن يحمل خبرًا **ثمانٍ وأربعون لا ثلاثُمئةٍ وخمسٌ وسبعون**؛ ومن
قرأ الأصفارَ كلَّها بنيةً قرأ مقامَه لا لغتَه.

`THE_LEADER_IS_A_MORPHEME_NOT_A_PHONOTACTIC_FACT`: وأعلى انتقالٍ «ال» ستَّ
عشرةَ مرّةً من ١١٤ موضعًا — أي أداةُ التعريف. وذلك نظيرُ ما قِيس على المصحف
في الحمل الوظيفيّ: ما يميّزه الرسمُ صرفٌ وأدواتٌ قبل أن يكون جذورًا.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path
from types import ModuleType

from algebra.provenance import Corpus, Reading

REPOSITORY = Path(__file__).resolve().parents[2]
RUNNER_PATH = REPOSITORY / "examples" / "rasm" / "run_letter_transitions.py"


def _runner() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_letter_transitions", RUNNER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


transitions = _runner()

DEPOSITED_DIGEST = "d435d63a4e49ea03a75344b050df01dd99d5bfb77335c807e2d6309f52174341"
VERSES = 7
WORDS = 29
PLACES = 114


def _lines() -> tuple[str, ...]:
    from alghanem.arabic.fatiha_source_text import FATIHA_LINES, source_sha256

    assert source_sha256() == DEPOSITED_DIGEST
    return FATIHA_LINES


def _words(policy: str) -> list[str]:
    fold, alphabet = transitions.POLICIES[policy]
    drawn: list[str] = []
    for line in _lines():
        for token in line.split():
            letters = transitions.drawn_letters(token, fold, alphabet)
            if letters:
                drawn.append(letters)
    return drawn


def test_the_deposited_text_is_seven_verses_and_its_digest_is_checked() -> None:
    """سبعُ آياتٍ ببصمةٍ تُعاد من حروفها؛ ونقلٌ لم يُقابَل، مُصرَّحٌ به."""

    assert len(_lines()) == VERSES
    assert len(_words("مطويّ")) == WORDS


def test_the_census_closes_on_its_own_positions_under_both_policies() -> None:
    """١١٤ موضعًا في السياستين، ومجموعُ الأزواج يساويها بلا بقيّة."""

    for policy in ("مطويّ", "مفصول"):
        pairs, first, second, places = transitions.census(_words(policy))
        assert places == PLACES
        assert sum(pairs.values()) == places
        assert sum(first.values()) == sum(second.values()) == places


def test_the_inventory_differs_by_policy_and_is_reported_not_assumed() -> None:
    """الجردُ ٢١ حرفًا مطويًّا و٢٣ مفصولًا — فالسياسةُ تبدّل المقام."""

    sizes = {}
    for policy in ("مطويّ", "مفصول"):
        _, first, second, _ = transitions.census(_words(policy))
        sizes[policy] = len(set(first) | set(second))
    assert sizes == {"مطويّ": 21, "مفصول": 23}
    assert sizes["مطويّ"] ** 2 == 441
    assert sizes["مفصول"] ** 2 == 529


def test_most_of_the_empty_cells_could_not_have_been_filled() -> None:
    """٣٢٧ من ٣٧٥ خانةً خاليةٍ ممتنعةٌ بالمقام؛ والباقي ٤٨ هو ما يحتمل خبرًا."""

    pairs, first, second, places = transitions.census(_words("مطويّ"))
    inventory = len(set(first) | set(second))
    cells = inventory**2
    observed = len(pairs)
    empty = cells - observed

    assert cells == 441 and observed == 66 and empty == 375
    forced = cells - places  # لا تُشغَل خاناتٌ أكثرُ من المواضع
    assert forced == 327
    assert empty - forced == 48

    # ونصيبُ الممتنع بالمقام من الخالي كلِّه فوق ثمانين بالمئة
    assert Fraction(forced, empty) > Fraction(4, 5)


def test_the_leading_transition_is_the_article_and_it_stands_alone() -> None:
    """«ال» ستَّ عشرةَ مرّةً، ولا يشاركها أحدٌ الصدارة — والتساوي كان سيُعلَن."""

    pairs, _, _, places = transitions.census(_words("مطويّ"))
    highest, leaders = transitions.tied_leaders(pairs)
    assert highest == 16
    assert leaders == [("ا", "ل")]
    assert len(leaders) == 1  # فلا تساويَ ههنا، ولو كان لأُعلِن
    assert Fraction(highest, places) > Fraction(1, 8)


def test_the_reading_is_stamped_with_this_transcription_not_with_a_mushaf() -> None:
    """الرقمُ مختومٌ بنقلٍ مُسمًّى؛ ومقارنتُه برقم مصحفٍ تُكتَب «عبر مدوّنتين»."""

    text = Corpus(
        name="نقلُ الفاتحة في الشجرة — إملائيٌّ لم يُقابَل",
        digest=DEPOSITED_DIGEST,
        size=WORDS,
        size_unit="كلمة",
    )
    reading = Reading(
        value=Fraction(16, PLACES),
        statistic="نصيبُ أعلى انتقالٍ من مواضع الجوار",
        unit="موضعُ جوار",
        corpus=text,
    )
    assert "نقلُ الفاتحة" in reading.stamp
    assert "موضعُ جوار" in reading.stamp
    assert reading.comparable_with(reading)
