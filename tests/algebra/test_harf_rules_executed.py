"""الفرقُ بين النسختين **مُشغَّلًا** لا موصوفًا: ما كان، وما زال، وما لم يتبدّل.

**ما يُقاس ههنا وما لا يُقاس**: لا مدوَّنةَ تُقرَأ ولا نسبةَ تُدَّعى. يُقاس
شيءٌ واحد: **سلوكُ الدالّتين على حالاتٍ مُعلَنة**. فكلُّ دعوى قلتُها عن خللٍ
في النسخة الواردة تُصبح ههنا شرطًا يسقط إن كانت كاذبة، وكلُّ إصلاحٍ يُصبح
شرطًا يسقط إن انتكس.

`AN_EXECUTED_CLAIM_OUTLIVES_THE_MESSAGE_THAT_MADE_IT`: قلتُ «مُثبَتٌ بالتنفيذ»
ثلاثَ مرّاتٍ في رسائلَ لا تُشغَّل. والرسالةُ ليست فحصًا: تُقرَأ مرّةً ثمّ
تُنسى، ولا تُنبِّه إن عاد الخللُ. فما ادُّعي تنفيذُه يُودَع مُشغَّلًا أو
لا يُعتَدّ به.

`A_FIX_IS_TWO_ASSERTIONS_NOT_ONE`: «صُلِح» دعوى مركّبة: أنّ الجديدَ صواب،
و**أنّ القديمَ كان خطأً**. فتُفحَص الدالّتان على الحالة الواحدة؛ ولو فُحِصت
الجديدةُ وحدَها لم يُعرَف هل أصلحت شيئًا أم كان سليمًا.

`THE_UNCHANGED_CASES_CARRY_THE_PROOF`: أكثرُ الحالات ههنا **لا يتبدّل فيها
شيء**، وهي الشهادة. فالرقعةُ التي تُبدّل ما لم تُقصَد ليست رقعةً بل نسخةً
أخرى، ولا يُعرَف ذلك إلّا بجدولٍ يُعَدّ فيه الثابتُ كما يُعَدّ المتبدّل.
"""

from __future__ import annotations

import pytest
from harf_rules import (
    ALL_RULES,
    DEFER,
    DEFINITE,
    JARR,
    NASB,
    NO_CASE,
    OUTCOMES,
    RAF,
    SEALED_RULES,
    clean,
    four_way,
    received_irab_of,
    record,
    revised_irab_of,
)

# ------------------------------------------------ حالاتٌ مُعلَنةٌ تُشغَّل عليها
FEMININE_ACCUSATIVE = record("ٱلصَّٰلِحَٰتِ", pos="ism", suffixes=["ات"], prefixes=["ال"])
FEMININE_NOMINATIVE = record("ٱلصَّٰلِحَٰتُ", pos="ism", suffixes=["ات"], prefixes=["ال"])
DIPTOTE = record("إِبْرَٰهِيمَ", pos="ism")
DEFINITE_NOUN = record("ٱلْكِتَٰبَ", pos="ism", prefixes=["ال"])
PREFIXED_DEFINITE = record("بِٱلْغَيْبَ", pos="ism", prefixes=["ب", "ال"])
NUNATED = record("كِتَٰبًا", pos="ism")
PARTICLE = record("مِن", pos="harf")
VERB = record("قَالَ", pos="fi'l")
DEICTIC = record("هَٰذَا", pos="ism", deictic=True)
SOUND_PLURAL = record("ٱلْمُؤْمِنِينَ", pos="ism", suffixes=["ين"], prefixes=["ال"])
MASCULINE_NOMINATIVE = record("ٱلْمُؤْمِنُونَ", pos="ism", suffixes=["ون"], prefixes=["ال"])
PRONOUN_HOST = record("كِتَٰبُهُۥ", pos="ism", suffixes=["ه"])
TWO_LETTER_PRONOUN = record("رَبِّهِمْ", pos="ism", suffixes=["هم"])
BARE_GENITIVE = record("ٱللَّهِ", pos="ism", prefixes=["ال"])
CARRIER_FINAL = record("قَالُوا", pos="ism")

PROBES = (
    (FEMININE_ACCUSATIVE, False, "جمعُ مؤنّثٍ سالم في موضع نصب"),
    (FEMININE_ACCUSATIVE, True, "جمعُ مؤنّثٍ سالم بعد حرف جرّ"),
    (FEMININE_NOMINATIVE, False, "جمعُ مؤنّثٍ سالم مرفوع"),
    (DIPTOTE, True, "ممنوعٌ من الصرف بعد حرف جرّ"),
    (DIPTOTE, False, "ممنوعٌ من الصرف بلا حرف جرّ"),
    (DEFINITE_NOUN, True, "معرَّفٌ بـ«ال» بعد حرف جرّ"),
    (PREFIXED_DEFINITE, True, "معرَّفٌ عليه سابقةٌ بعد حرف جرّ"),
    (NUNATED, True, "منوَّنٌ بالفتح بعد حرف جرّ"),
    (PARTICLE, False, "حرفٌ عند ط٧"),
    (VERB, False, "فعلٌ عند ط٧"),
    (DEICTIC, False, "مبنيُّ إحالة من معاجم ط٣"),
    (SOUND_PLURAL, True, "جمعُ مذكّرٍ سالم بعد حرف جرّ"),
    (SOUND_PLURAL, False, "جمعُ مذكّرٍ سالم بلا حرف جرّ"),
    (MASCULINE_NOMINATIVE, False, "جمعُ مذكّرٍ سالم مرفوع"),
    (PRONOUN_HOST, False, "مضافٌ إلى ضميرٍ مرفوع"),
    (TWO_LETTER_PRONOUN, True, "ضميرٌ من حرفين"),
    (BARE_GENITIVE, True, "بلا لاحقةٍ — لا تُقشَّر هاؤه"),
    (CARRIER_FINAL, False, "ألفٌ حاملةٌ في الآخر"),
)


def _received(rec: dict[str, object], jarr: bool) -> str | None:
    return received_irab_of(rec, jarr)[0]


def _revised(rec: dict[str, object], jarr: bool) -> str:
    return revised_irab_of(rec, jarr)[0]


def test_the_sound_feminine_plural_was_unreachable_and_now_is_not() -> None:
    """كان المنصوبُ يُقرَأ مجرورًا **مهما كان الموضع**؛ والآن يُفَضّ بالموضع.

    والشهادةُ في الجمع لا في الفرد: الواردةُ تُعطي `jarr` في الحالين — فلا
    يفرّق بينهما شيء — والمنقّحةُ تفرّق. وهذا هو معنى «خطأٌ بالبناء»: ليس
    تمييزًا يخطئ بل موضعًا لا يُبلَغ أصلًا.
    """

    assert _received(FEMININE_ACCUSATIVE, False) == JARR
    assert _received(FEMININE_ACCUSATIVE, True) == JARR
    assert _revised(FEMININE_ACCUSATIVE, False) == NASB
    assert _revised(FEMININE_ACCUSATIVE, True) == JARR

    assert _received(FEMININE_NOMINATIVE, False) == RAF
    assert _revised(FEMININE_NOMINATIVE, False) == RAF  # والمرفوعُ لم يتبدّل


def test_the_diptote_rule_was_already_present_and_is_left_alone() -> None:
    """ق٦ موجودةٌ في النسخة الواردة، فلا تُحسَب في رصيد هذه الرقعة.

    وأقولُها لأنّي أصلحتُها في النسخة **السابقة** (R0d) حين كانت غائبة، ثمّ
    وصلت نسخةٌ تحملها. فالرقعةُ لا تدّعي ما سبقها إليه صاحبُها: الاثنتان
    تُعطيان `jarr` ههنا، والفرقُ الوحيدُ في **حارس «ال»** لا في القاعدة.
    """

    assert _received(DIPTOTE, True) == JARR
    assert _revised(DIPTOTE, True) == JARR

    for rec, jarr in ((DIPTOTE, False), (DEFINITE_NOUN, True), (NUNATED, True)):
        assert _received(rec, jarr) == NASB
        assert _revised(rec, jarr) == NASB


def test_the_definite_prefix_is_read_from_layer_two_not_from_the_surface() -> None:
    """`startswith` يُخطئ كلَّ معرَّفٍ عليه سابقة، وط٢ يعرف السوابق.

    وهذا ليس تحسينَ أسلوب: الواردةُ تُطلِق ق٦ على «بِٱلْغَيْبَ» لأنّها لا ترى
    «ال»، والمنقّحةُ تكفّ. والاثنتان تختلفان في المخرَج، فالفرقُ مقيسٌ لا موصوف.
    """

    surface = clean(str(PREFIXED_DEFINITE["surface"]))
    assert not surface.startswith(("ال", "ٱل"))  # ما يراه النظرُ في السطح
    assert any(one in DEFINITE for one in PREFIXED_DEFINITE["prefixes"])  # وما يقوله ط٢

    assert _received(PREFIXED_DEFINITE, True) == JARR  # ق٦ انطلقت خطأً
    assert _revised(PREFIXED_DEFINITE, True) == NASB  # وكفّت


def test_the_sealed_rule_and_its_widening_differ_on_verbs_alone() -> None:
    """ق٥ المختومةُ تمتنع عن الحرف والمبنيّ، وق٥و تزيد الفعل — ولا شيءَ غيرَه."""

    differ = [
        label
        for rec, jarr, label in PROBES
        if revised_irab_of(rec, jarr, rules=SEALED_RULES)[0]
        != revised_irab_of(rec, jarr, rules=ALL_RULES)[0]
    ]
    assert differ == ["فعلٌ عند ط٧"]

    assert revised_irab_of(VERB, rules=SEALED_RULES)[0] != NO_CASE
    assert revised_irab_of(VERB, rules=ALL_RULES)[0] == NO_CASE
    assert revised_irab_of(PARTICLE, rules=SEALED_RULES)[0] == NO_CASE
    assert revised_irab_of(DEICTIC, rules=SEALED_RULES)[0] == NO_CASE


def test_the_oracle_tag_separates_the_rule_from_the_layer_that_feeds_it() -> None:
    """ق٥ ترث خطأ ط٧؛ ووسمٌ صحيحٌ يعطي سقفَها وحدَها، والفرقُ ثمنُ ط٧ مقيسًا."""

    mislabelled = record("كِتَٰبُ", pos="harf")  # اسمٌ وسمه ط٧ حرفًا
    assert revised_irab_of(mislabelled)[0] == NO_CASE
    assert revised_irab_of(mislabelled, oracle_pos="ism")[0] == RAF


def test_the_fifth_outcome_is_named_and_never_collapses_into_none() -> None:
    """الواردةُ تُعيد `None` فيلتبس بالامتناع؛ والمنقّحةُ تُسمّي المخرجَ الخامس."""

    assert _received(CARRIER_FINAL, False) is None
    assert _revised(CARRIER_FINAL, False) == DEFER
    assert DEFER != NO_CASE
    assert len(OUTCOMES) == 5

    for rec, jarr, label in PROBES:
        assert _revised(rec, jarr) in OUTCOMES, label
        assert _revised(rec, jarr) is not None, label


def test_the_four_way_conversion_refuses_to_run_without_a_declared_decision() -> None:
    """مصيرُ «لم يُحسَم» قرارٌ يُعلَن، ولا يُؤخَذ صمتًا بقيمةٍ افتراضيّة."""

    with pytest.raises(TypeError):
        four_way(DEFER)  # type: ignore[call-arg]
    with pytest.raises(ValueError):
        four_way(DEFER, defer_counts_as="ربّما")

    assert four_way(DEFER, defer_counts_as=NO_CASE) == NO_CASE
    assert four_way(DEFER, defer_counts_as="خطأ") == "خطأٌ مُعلَن"
    assert four_way(RAF, defer_counts_as="خطأ") == RAF  # وما حُسِم لا يتأثّر


def test_exactly_three_of_eighteen_cases_changed_and_the_rest_held() -> None:
    """ثلاثٌ تبدّلت من ثماني عشرة، وخمسَ عشرةَ ثبتت — والثابتُ هو الشهادة."""

    changed = [
        label
        for rec, jarr, label in PROBES
        if _received(rec, jarr) != _revised(rec, jarr)
    ]
    assert changed == [
        "جمعُ مؤنّثٍ سالم في موضع نصب",
        "معرَّفٌ عليه سابقةٌ بعد حرف جرّ",
        "ألفٌ حاملةٌ في الآخر",
    ]
    assert len(PROBES) - len(changed) == 15


def test_the_last_change_is_a_renaming_not_a_new_judgement() -> None:
    """ثالثُها ليس تبدُّلَ حكم: `None` صارت «لم يُحسَم»، والحكمُ واحد.

    فالمتبدّلُ حقًّا **اثنان**، والثالثُ تسميةٌ لما كان بلا اسم. ويُفصَل
    ذلك بالعدّ كيلا يُحسَب في رصيد الرقعة ما ليس منه.
    """

    assert _received(CARRIER_FINAL, False) is None
    assert _revised(CARRIER_FINAL, False) == DEFER

    real = [
        label
        for rec, jarr, label in PROBES
        if _received(rec, jarr) != _revised(rec, jarr)
        and _received(rec, jarr) is not None
    ]
    assert len(real) == 2


def test_removing_any_rule_changes_something_so_none_is_dead_weight() -> None:
    """كلُّ قاعدةٍ من الثماني يتبدّل بحذفها مخرَجٌ على الأقلّ — فلا قاعدةَ عاطلة.

    وهذا هو الشرط (هـ) مُشغَّلًا على عيّنةٍ صغيرة: لا يُنشَر مجموعٌ بلا
    تفصيله، والتفصيلُ يبدأ بأن يكون للحذف أثرٌ يُعَدّ.
    """

    full = [_revised(rec, jarr) for rec, jarr, _ in PROBES]
    effects: dict[str, int] = {}
    for rule in ALL_RULES:
        without = tuple(one for one in ALL_RULES if one != rule)
        got = [revised_irab_of(rec, jarr, rules=without)[0] for rec, jarr, _ in PROBES]
        effects[rule] = sum(1 for a, b in zip(full, got, strict=True) if a != b)

    assert set(effects) == set(ALL_RULES)
    assert all(count > 0 for count in effects.values()), effects
    assert effects["ق٥و"] == 1  # التوسيعُ يمسّ الفعلَ وحدَه في هذه العيّنة
    assert effects["ق٣"] == max(effects.values())  # والتشكيلُ أوسعُها أثرًا
