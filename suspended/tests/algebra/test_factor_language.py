"""لغاتُ العوامل الممنوعة: الشجرةُ مبرهنةٌ بالتعداد، لا مرسومةٌ بيد.

يُثبِت هذا الاختبارُ تسعةَ أشياء: أنّ منعَ `VV` و`CC` و`CV` على أبجديّةٍ من
حرفين يُخرِج **`{ε, V, C, VC}` ولا خامس** بالتعداد الشامل، وأنّ الانتقالَ
المسموحَ واحدٌ (`V→C`) فالمخطَّطُ بلا دورة، وأنّ المجموعةَ **منغلقةٌ على
البادئة** فتقابل شجرةً، وأنّ للشجرة أربعَ عُقَدٍ و**ثلاثَ حوافّ** وعمقًا اثنين
وأنّ `|E| = |V| − 1`، وأنّ ولدَي الجذر `V` و`C` ولـ`V` ولدٌ واحدٌ ولـ`C` لا ولد،
وأنّ لغةً فيها دورةٌ في مخطَّطها **تُرفَض** بدل أن تُعَدّ إلى ما لا نهاية،
وأنّ مجموعةً غيرَ منغلقةٍ على البادئة تُرفَض شجرةً، وأنّ حذفَ منعٍ واحدٍ يفتح
اللغةَ فورًا — فالمسلَّماتُ الأربعُ كلُّها حاملة.
"""

from __future__ import annotations

import pytest

from algebra.factor_language import (
    FACTOR_LANGUAGE_NAMED_RESIDUALS,
    FactorLanguage,
    FactorLanguageError,
    Trie,
    avoids,
    is_prefix_closed,
)

SYLLABLE_TAIL = FactorLanguage(
    alphabet=("V", "C"), forbidden=frozenset({"VV", "CC", "CV"})
)


def test_the_language_is_exactly_the_four_words() -> None:
    """`w ∈ {ε, V, C, VC}` ولا خامس — بالتعداد الشامل لا بالبرهان نثرًا."""

    assert SYLLABLE_TAIL.words() == frozenset({"", "V", "C", "VC"})


def test_only_one_transition_survives_and_the_graph_is_acyclic() -> None:
    """بعد `V` لا يجوز إلّا `C`، وبعد `C` لا يجوز شيء؛ فلا دورةَ فلا لانهاية."""

    assert SYLLABLE_TAIL.allowed_transitions() == (("V", "C"),)
    assert SYLLABLE_TAIL.transition_graph_is_acyclic()


def test_the_set_is_prefix_closed_so_a_tree_exists() -> None:
    """انغلاقُ البادئة مفحوصٌ، وهو شرطُ وجود الشجرة لا وصفٌ لها."""

    assert is_prefix_closed(SYLLABLE_TAIL.words())
    assert avoids("VC", SYLLABLE_TAIL.forbidden)
    assert not avoids("CV", SYLLABLE_TAIL.forbidden)


def test_the_tree_has_four_nodes_and_three_edges() -> None:
    """أربعُ عُقَدٍ وثلاثُ حوافّ وعمقُ اثنين، و`|E| = |V| − 1`."""

    tree = SYLLABLE_TAIL.trie()
    assert tree.nodes == 4
    assert len(tree.edges) == 3
    assert tree.depth == 2
    assert tree.edge_count_matches_node_count()


def test_the_shape_of_the_tree_is_forced() -> None:
    """ولدا الجذر `V` و`C`، ولـ`V` ولدٌ واحدٌ، ولـ`C` لا ولد."""

    tree = SYLLABLE_TAIL.trie()
    assert tree.children_of("") == ("C", "V")
    assert tree.children_of("V") == ("VC",)
    assert tree.children_of("C") == ()
    assert tree.edges == (("", "C"), ("", "V"), ("V", "VC"))


def test_every_forbidden_factor_carries_weight() -> None:
    """حذفُ أيِّ منعٍ يزيد اللغةَ؛ فالمسلَّماتُ الثلاثُ لا حشوَ فيها."""

    for dropped in ("VV", "CC", "CV"):
        loosened = FactorLanguage(
            alphabet=SYLLABLE_TAIL.alphabet,
            forbidden=frozenset(SYLLABLE_TAIL.forbidden - {dropped}),
        )
        if loosened.transition_graph_is_acyclic():
            assert loosened.words() > SYLLABLE_TAIL.words()
        else:
            with pytest.raises(FactorLanguageError):
                loosened.words()


def test_a_cyclic_language_is_refused_not_enumerated() -> None:
    """لغةٌ لانهائيّةٌ تُرَدُّ عند الطلب، ولا يُدار التعدادُ إلى ما لا نهاية."""

    unbounded = FactorLanguage(alphabet=("a", "b"), forbidden=frozenset({"ab"}))
    assert not unbounded.transition_graph_is_acyclic()
    with pytest.raises(FactorLanguageError):
        unbounded.words()


def test_a_set_that_is_not_prefix_closed_is_not_a_tree() -> None:
    """مجموعةٌ بلا بادئاتها لا تقابل شجرةً، ولا تُكمَّل صمتًا."""

    with pytest.raises(FactorLanguageError):
        Trie(words=frozenset({"", "VC"}))
    with pytest.raises(FactorLanguageError):
        Trie(words=frozenset({"V", "VC"}))
    with pytest.raises(FactorLanguageError):
        FactorLanguage(alphabet=("V",), forbidden=frozenset({"X"}))


def test_named_residuals_are_deposited() -> None:
    """البواقي المُسمّاةُ ثلاثٌ، ولا مكرَّرَ فيها."""

    assert len(FACTOR_LANGUAGE_NAMED_RESIDUALS) == 3
    assert len(set(FACTOR_LANGUAGE_NAMED_RESIDUALS)) == 3
