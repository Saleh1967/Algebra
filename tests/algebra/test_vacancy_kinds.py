"""أجناسُ الخلوّ: الجداءُ يعطي بتّةً، والبتّةُ لا تفرّق بين ستّةِ أحوال.

**ما يُقاس ههنا**: الآلةُ وحدَها. ولا رقمَ لغويًّا في هذا الملفّ.

`THE_PRODUCT_GIVES_ONE_BIT_PER_CELL`: النقطةُ من `Product.points()` تقول
«ههنا خانة» ولا تقول شيئًا عن خلوّها. فالجداءُ **يحوّل غيابًا مجهولًا إلى
غيابٍ موقوع، ثمّ يقف**. وذلك كلُّ ما يفعله، وهو كثير: لا يُسأل عن سببِ خلوِّ
خانةٍ لم تُعدَّد بعد.

`A_VACANCY_KIND_IS_DECLARED_NOT_INFERRED`: وتصنيفُ الخلوّ **فعلٌ ثانٍ** يُعلَن
بشاهده. وثلاثةٌ من الأجناس لا تُدَّعى بلا شاهد: «لا شاهدَ عليها» غيرُ «لم
يُفتَّش عنها»، و«لا تُبلَغ» غيرُ «لم تُطلَب»، و«رُدَّت بقياس» غيرُ «لم تُقَس».
والاستحالةُ شاهدُها ناقضُها، والفحصُ المُعيَّنُ شاهدُه نصُّه.

`THE_LIBRARY_ALREADY_FORBADE_THE_BARE_BIT`: وكانت `Placement` تمنع الخانةَ
العاريةَ من قبل: إمّا نتيجةٌ، وإمّا امتناعٌ **بناقضٍ مُسمًّى**، وإمّا فحصٌ
**مُعيَّن**. فالذي كان ناقصًا ليس منعَ البتّة بل **تفريقَ أسباب البقاء
مفتوحًا**: أمُعيَّنٌ لم يُجرَ، أم مفتَّشٌ عنه فلم يوجد، أم غيرُ مبلوغٍ أصلًا.
"""

from __future__ import annotations

import pytest

from algebra.results import (
    VACANCIES_NEEDING_EVIDENCE,
    Axis,
    Finding,
    Placement,
    Product,
    ResultsError,
    Vacancy,
    vacancy_of_a_bare_cell,
)

FINDING = Finding(
    statement="دعوًى مُصطنَعةٌ لفحص الآلة",
    source="مصدرٌ مُصطنَع",
    unit="وحدةٌ مُصطنَعة",
    null="صفريٌّ مُصطنَع",
    oracle="لا عرّاف",
    invariance="ثابتٌ تحت تبديلٍ مُصطنَع",
    residue="بقيّةٌ مُصطنَعةٌ تُسمّى ولا تُطوى",
)


def test_the_bare_product_yields_exactly_one_kind() -> None:
    """الجداءُ وحدَه يعطي جنسًا واحدًا: «خاليةٌ ولم يُصنَّف خلوُّها»."""

    grid = Product(
        axes=(
            Axis(name="محورٌ أوّل", values=("أ", "ب")),
            Axis(name="محورٌ ثانٍ", values=("س", "ص", "ع")),
        )
    )
    assert grid.size == 6
    assert len(set(grid.points())) == 6

    # وكلُّ نقطةٍ منها، قبل أن تُودَع، جنسُ خلوِّها واحدٌ لا غير
    kinds = {vacancy_of_a_bare_cell() for _ in grid.points()}
    assert kinds == {Vacancy.UNCLASSIFIED}
    assert len(kinds) == 1
    assert len(Vacancy) == 6  # وستّةٌ في المفردة، فالبتّةُ تُسقِط خمسةَ فروق


def test_the_three_claimed_kinds_are_refused_without_evidence() -> None:
    """«لا شاهدَ عليها» دعوًى تحتاج شاهدًا هي الأخرى؛ وإلّا فهي «لم يُفتَّش»."""

    assert set(VACANCIES_NEEDING_EVIDENCE) == {
        Vacancy.UNATTESTED,
        Vacancy.UNREACHABLE,
        Vacancy.REFUSED,
    }

    for kind in VACANCIES_NEEDING_EVIDENCE:
        with pytest.raises(ResultsError, match="بلا شاهد"):
            Placement(
                coordinate=("أ", "س"),
                open_test="فحصٌ مُعيَّنٌ يحسم الخانة",
                absence=kind,
            )
        placed = Placement(
            coordinate=("أ", "س"),
            open_test="فحصٌ مُعيَّنٌ يحسم الخانة",
            absence=kind,
            absence_evidence="ما جرى فعلًا، مكتوبًا",
        )
        assert placed.vacancy is kind


def test_an_open_cell_defaults_to_unrun_not_to_unclassified() -> None:
    """خانةٌ تحمل فحصًا مُعيَّنًا خلوُّها **مصنَّف**: مُعيَّنٌ لم يُجرَ."""

    placed = Placement(coordinate=("أ", "س"), open_test="فحصٌ مُعيَّنٌ يحسمها")
    assert placed.vacancy is Vacancy.UNRUN

    # و«غيرُ مصنَّف» جنسُ الخانة العارية من الجداء، فلا يُودَع في خانةٍ مكتوبة
    with pytest.raises(ResultsError, match="العاريةِ من الجداء|العارية"):
        Placement(
            coordinate=("أ", "س"),
            open_test="فحصٌ مُعيَّن",
            absence=Vacancy.UNCLASSIFIED,
        )


def test_a_forbidden_cell_is_impossible_and_admits_no_other_kind() -> None:
    """الامتناعُ جنسُه الاستحالة، ودعوى الامتناع نفسُها هي التصنيف."""

    forbidden = Placement(
        coordinate=("أ", "س"),
        forbidden_because="لا تجتمع القيمتان في موضعٍ واحد",
        refuted_by="موضعٌ واحدٌ تجتمعان فيه يُسقِط الدعوى",
    )
    assert forbidden.vacancy is Vacancy.IMPOSSIBLE

    with pytest.raises(ResultsError, match="جنسُه الاستحالةُ"):
        Placement(
            coordinate=("أ", "س"),
            forbidden_because="لا تجتمعان",
            refuted_by="شاهدٌ يُسقِطها",
            absence=Vacancy.UNATTESTED,
        )


def test_a_filled_cell_has_no_vacancy_to_classify() -> None:
    """المملوءةُ لا خلوَّ لها؛ ومن صنّف خلوَّها صنّف ما ليس فيها."""

    filled = Placement(coordinate=("أ", "س"), finding=FINDING)
    assert filled.vacancy is None

    with pytest.raises(ResultsError, match="مملوءةٌ ويُصنَّف خلوُّها"):
        Placement(coordinate=("أ", "س"), finding=FINDING, absence=Vacancy.UNATTESTED)
    with pytest.raises(ResultsError, match="مملوءةٌ ويُصنَّف خلوُّها"):
        Placement(coordinate=("أ", "س"), finding=FINDING, absence_evidence="شاهد")


def test_evidence_without_a_kind_is_refused_as_well() -> None:
    """شاهدٌ بلا جنسٍ يشهد له نصٌّ معلَّقٌ لا تصنيف."""

    with pytest.raises(ResultsError, match="بلا جنسِ خلوٍّ"):
        Placement(
            coordinate=("أ", "س"),
            open_test="فحصٌ مُعيَّن",
            absence_evidence="شاهدٌ لا يشهد لشيء",
        )

    with pytest.raises(ResultsError, match="مفردته المغلقة"):
        Placement(
            coordinate=("أ", "س"),
            open_test="فحصٌ مُعيَّن",
            absence="لا شاهد",  # type: ignore[arg-type]
        )
