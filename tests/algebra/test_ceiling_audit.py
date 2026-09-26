"""المانعُ هـ) — العطل ٢٦: **حدٌّ فوق سقفٍ شرطٌ لا يُختبَر**.

**العطل**: نسبةٌ أو مقدارٌ بسطُه لا يقبل كلَّ ما في مقامه — لأنّ فيه ما
**يمتنع بالبناء** — سقفُه دون الواحد. فإن كُتِب حدُّه فوق ذلك السقف **لم
يكن قابلًا للتحقّق من أصله**، **وسقوطُه لا يخبر عن المادّة بشيء**.

**والحكمُ الصحيحُ عندها `Vacancy.IMPOSSIBLE` لا `FALSIFIED`** — وليس
الفرقُ لفظيًّا: الساقطُ يُسجَّل خبرًا عن المادّة، **والممتنعُ يُسجَّل في
رصيد ما لم يُختبَر**.

**وكيف انكشف**: من تعليقِ طلب الدمج ‎#45 — شرطٌ يوجب أن تكون «تْ» آخرَ
لفظها بنسبةٍ ما، **ومقامُه يحمل ٨١٧ شطرَ شدّةٍ لا يكون واحدٌ منها آخرًا
بحكم البناء**. فسقفُ نسبته `٠٫٤٥٥٠`، **فإن كان حدُّه فوقه فالشرطُ ممتنع**.
وقد حُقِّق ذلك في `deposits/gemination_ceiling_witness.log`.

**وحدُّ هذا المانعِ مُعلَنٌ صريحًا**: **لا تُحسَب السقوفُ آليًّا** — فحسابُ
سقفِ إحصاءٍ كيفما كان متعذّر. **فيُلزِم المانعُ التصريحَ** بالسقف ويفحص
`الحدُّ ≤ السقف`، ويفحص أنّ المقيسَ لا يفوقه. **فيردُّ الصمتَ وحدًّا فوق
سقفٍ مُصرَّحٍ به، ولا يردُّ سقفًا مُصرَّحًا خطأً.**

**والدَّينُ مكشوفٌ ومقيَّد**: ما لم يُصرَّح بسقفه من الأختام السابقة
معروضٌ بعينه في `CEILING_NOT_DECLARED` — **تسعةٌ وعشرون شرطًا في سبعةَ عشرَ
ملفًّا**، **يُرى ولا ينمو**. وكلُّ ختمٍ جديدٍ يلزمه التصريح.
"""

from __future__ import annotations

from fractions import Fraction

from sealed_reading import read_all

from algebra.ceiling import (
    CeilingError,
    attainable_ceiling,
    threshold_is_reachable,
    verdict_or_vacancy,
)
from algebra.results import Vacancy
from algebra.signified import Direction

# دَينٌ **يُرى ولا ينمو**: شروطٌ من أختامٍ سابقةٍ لم يُصرَّح بسقفها بعد
CEILING_NOT_DECLARED: dict[str, tuple[str, ...]] = {
    "test_arabic_token_run.py": ("ط١٠", "ط١٢", "ط٧"),
    "test_basmala_lifted_run.py": ("ر٥", "ر٨"),
    "test_context_ladder_run.py": ("ق٧", "ق٨"),
    "test_crossing_census_run.py": ("ف٢",),
    "test_discovered_ascent_run.py": ("ك٤",),
    "test_greedy_algebra_run.py": ("ب٤", "ب٦"),
    "test_markov_ladder_run.py": ("ي٥",),
    "test_measured_ranking_run.py": ("ت٤",),
    "test_praise_blame_run.py": ("ش١٢", "ش٦", "ش٧"),
    "test_residue_derivation_run.py": ("و٤",),
    "test_script_floor_run.py": ("ج٤",),
    "test_separation_rule_run.py": ("ص٣",),
    "test_state_cycle_run.py": ("ح١٢", "ح٥", "ح٧", "ح٨"),
    "test_transfer_arrow_run.py": ("ظ٧", "ظ٩"),
    "test_verse_ending_run.py": ("خ٩",),
    "test_vowel_ladder_run.py": ("س٤",),
    "test_word_escalation_run.py": ("ك١١", "ك١٢"),
}
OWING = 29
LEAST_REASON = 25


def _bounded() -> list[tuple[str, str, Fraction]]:
    """(الملفّ، الشرط، الحدّ) لكلّ شرطٍ «لا يقلّ عن» حدُّه بين صفرٍ وواحد."""

    found: list[tuple[str, str, Fraction]] = []
    for one in read_all():
        for two in one.predictions:
            if two.direction is Direction.AT_LEAST and (
                Fraction(0) < two.threshold < Fraction(1)
            ):
                found.append((one.run.name, two.identifier, two.threshold))
    return found


def test_the_ceiling_is_arithmetic_and_a_threshold_above_it_is_impossible() -> None:
    """المبرهنةُ الصغيرة: `(المقام − الممتنع) ÷ المقام`، وفوقَها امتناع."""

    assert attainable_ceiling(1_499, 817) == Fraction(682, 1_499)
    assert attainable_ceiling(10, 0) == Fraction(1)
    assert attainable_ceiling(10, 10) == Fraction(0)
    ceiling = attainable_ceiling(1_499, 817)
    assert not threshold_is_reachable(Fraction(1, 2), ceiling)
    assert threshold_is_reachable(Fraction(1, 4), ceiling)
    assert (
        verdict_or_vacancy(Fraction(1, 2), ceiling, Fraction(0)) is Vacancy.IMPOSSIBLE
    )
    assert verdict_or_vacancy(Fraction(1, 4), ceiling, Fraction(1, 5)) is None
    for bad in ((0, 0), (10, 11), (10, -1)):
        try:
            attainable_ceiling(*bad)
        except CeilingError:
            continue
        raise AssertionError(bad)


def test_a_measured_value_above_its_ceiling_is_refused() -> None:
    """مقيسٌ فوق سقفه يعني أنّ أحدَ الرقمين خطأ — فيُردّ ولا يُمرَّر."""

    ceiling = attainable_ceiling(100, 40)
    try:
        verdict_or_vacancy(Fraction(1, 2), ceiling, Fraction(7, 10))
    except CeilingError as complaint:
        assert "فوق سقفه" in str(complaint)
        return
    raise AssertionError("مرَّ مقيسٌ فوق سقفه")


def test_every_bounded_condition_declares_its_ceiling_or_is_owed() -> None:
    """كلُّ شرطٍ محدودٍ إمّا صرَّح بسقفه **وإمّا معروضٌ دَينًا** — ولا ثالث."""

    astray: dict[str, list[str]] = {}
    stale: dict[str, list[str]] = {}
    for name in {one for one, _, _ in _bounded()}:
        module = __import__(name.removesuffix(".py"))
        declared = set(getattr(module, "CEILINGS", {}))
        here = {two for one, two, _ in _bounded() if one == name}
        owed = set(CEILING_NOT_DECLARED.get(name, ()))
        missing = sorted(here - declared - owed)
        if missing:
            astray[name] = missing
        both = sorted(declared & owed)
        if both:
            stale[name] = both
    assert not astray, astray
    assert not stale, stale  # ولا يُترَك في الدَّين ما صُرِّح به
    assert sum(len(one) for one in CEILING_NOT_DECLARED.values()) == OWING


def test_no_owed_entry_names_a_condition_that_is_not_bounded() -> None:
    """ولا يُحشَى الدَّينُ بشرطٍ ليس محدودًا — فالجدولُ يُقابَل بالشجرة."""

    real = {(one, two) for one, two, _ in _bounded()}
    for name, owing in CEILING_NOT_DECLARED.items():
        for one in owing:
            assert (name, one) in real, (name, one)


def test_every_declared_ceiling_holds_its_threshold_and_is_reasoned() -> None:
    """السقفُ المُصرَّحُ يفوق حدَّه، **ولكلٍّ سببٌ مكتوبٌ لا صمت**."""

    seen = 0
    for name, identifier, threshold in _bounded():
        module = __import__(name.removesuffix(".py"))
        table = getattr(module, "CEILINGS", {})
        if identifier not in table:
            continue
        ceiling, why = table[identifier]
        assert isinstance(ceiling, Fraction), (name, identifier)
        assert ceiling > 0, (name, identifier)
        assert threshold_is_reachable(threshold, min(ceiling, Fraction(1))) or (
            ceiling > 1
        ), (name, identifier, threshold, ceiling)
        assert threshold <= ceiling, (name, identifier, threshold, ceiling)
        assert len(why) >= LEAST_REASON, (name, identifier, why)
        seen += 1
    assert seen == len(_bounded()) - OWING
    assert seen == 6


def test_the_guard_says_what_it_does_not_do() -> None:
    """حدُّ المانعِ مُعلَن: يردُّ الصمتَ وحدًّا فوق سقفٍ، لا سقفًا خاطئًا."""

    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "**لا تُحسَب السقوفُ آليًّا**" in text
    assert "ولا يردُّ سقفًا مُصرَّحًا خطأً" in text
    assert "**تسعةٌ وعشرون شرطًا في سبعةَ عشرَ ملفًّا**" in text
    assert "**يُرى ولا ينمو**" in text
