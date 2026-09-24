"""مُشغِّلُ «الشاهد» مُجرًّى على مادّةٍ مصنوعة: يُرَدّ حيث يجب، ويحسب ما وُعِد.

**ولا مدوّنةَ ههنا**: المادّةُ أسطرٌ تُكتَب في هذا الملفّ، وبصمتُها تُحسَب من
بايتاتها لحظةَ الكتابة. فما يُفحَص **آلةُ التشغيل** لا رقمٌ عن العربيّة.

`THE_REFUSALS_ARE_THE_POINT_OF_THIS_FILE`: أربعةُ مواضعَ ترُدّ: بصمةٌ لا
تطابق البايتات، وإغلاقٌ لا يطابق عددَ الصفوف، وصنفٌ خارج الخمسة المختومة،
ونوعُ سطحٍ لم يُعلَن. وكلُّ واحدٍ منها يفصل بين «شُغِّل على مدوّنةٍ» وبين
«شُغِّل على ما وقع في اليد».

`AN_EDGE_DOES_NOT_CROSS_A_VERSE`: والإطارُ المحليُّ لا يعبر الآية، فآخرُ
كلمةٍ في آيةٍ وأوّلُ كلمةٍ في التي تليها **ليسا جارين**. ولو عبر لصُنِعت
جيرةٌ من حدٍّ لا من استعمال.
"""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

REPOSITORY = Path(__file__).resolve().parents[2]
RUNNER_PATH = REPOSITORY / "examples" / "shahid" / "run_shahid.py"


def _runner() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_shahid", RUNNER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


shahid = _runner()

# آيةٌ من أربع كلمات، ومركزان يتبادلان الموضعَ بين «س» و«ل»
VERSES: tuple[tuple[str, ...], ...] = (
    ("س", "م", "ل", "ك"),
    ("س", "ن", "ل", "ك"),
    ("س", "م", "ل", "د"),
    ("س", "ن", "ل", "د"),
) * 4

CLASS_ROWS = (
    ("س", "جار"),
    ("ل", "فعل"),
    ("ك", "معرفة"),
    ("د", "ضمير"),
)


def _write_alignment(folder: Path) -> tuple[Path, str, int]:
    lines = ["loc\tsurface"]
    count = 0
    for verse_index, verse in enumerate(VERSES, start=1):
        for word_index, surface in enumerate(verse, start=1):
            lines.append(f"1:{verse_index}:{word_index}\t{surface}")
            count += 1
    path = folder / "aligned.tsv"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return path, digest, count


def _write_classes(folder: Path, rows: tuple[tuple[str, str], ...]) -> Path:
    path = folder / "classes.tsv"
    path.write_text(
        "surface\tclass\n" + "".join(f"{one}\t{two}\n" for one, two in rows),
        encoding="utf-8",
    )
    return path


def _arguments(folder: Path, **changes: object) -> object:
    path, digest, count = _write_alignment(folder)
    settings = {
        "aligned": path,
        "closure": count,
        "digest": digest,
        "classes": _write_classes(folder, CLASS_ROWS),
        "surface_kind": "رسم-خام",
        "seed": 20_260_924,
        "draws": 200,
    }
    settings.update(changes)
    parser = shahid.build_argument_parser()
    return parser.parse_args(
        [
            "--aligned",
            str(settings["aligned"]),
            "--closure",
            str(settings["closure"]),
            "--digest",
            str(settings["digest"]),
            "--classes",
            str(settings["classes"]),
            "--surface-kind",
            str(settings["surface_kind"]),
            "--seed",
            str(settings["seed"]),
            "--draws",
            str(settings["draws"]),
        ]
    )


def test_a_digest_that_does_not_match_the_bytes_is_refused(tmp_path: Path) -> None:
    """بصمةٌ مُعلَنةٌ لا تطابق البايتات: مدوّنتان لا مدوّنة، فيُرَدّ التشغيل."""

    arguments = _arguments(tmp_path, digest="0" * 64)
    with pytest.raises(shahid.ShahidError) as raised:
        shahid.run(arguments)
    assert "مدوّنتان لا مدوّنة" in str(raised.value)


def test_a_closure_that_does_not_match_the_rows_is_refused(tmp_path: Path) -> None:
    """إغلاقٌ يخالف عددَ الصفوف يُعلَن ولا يُطوى — كإغلاق ٧٧٬٤٢٩."""

    path, digest, count = _write_alignment(tmp_path)
    arguments = _arguments(tmp_path, closure=count + 1)
    assert arguments.digest == digest and arguments.aligned == path
    with pytest.raises(shahid.ShahidError) as raised:
        shahid.run(arguments)
    assert "في الإغلاق المُعلَن" in str(raised.value)


def test_a_class_outside_the_sealed_five_is_refused(tmp_path: Path) -> None:
    """الأصنافُ خمسةٌ في الختم؛ وسادسٌ يُرَدّ ولا يُطوى في «سواه»."""

    arguments = _arguments(tmp_path)
    _write_classes(tmp_path, (*CLASS_ROWS, ("ه", "اسمُ إشارة")))
    with pytest.raises(shahid.ShahidError) as raised:
        shahid.run(arguments)
    assert "خارج الخمسة المختومة" in str(raised.value)


def test_the_surface_kind_has_no_default(tmp_path: Path) -> None:
    """«أرسمٌ خامٌ أم مخرَجُ تطبيع؟» قرارٌ يُعلَن، وغيابُه يُسقِط التشغيل."""

    path, digest, count = _write_alignment(tmp_path)
    parser = shahid.build_argument_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(
            [
                "--aligned",
                str(path),
                "--closure",
                str(count),
                "--digest",
                digest,
                "--classes",
                str(_write_classes(tmp_path, CLASS_ROWS)),
                "--seed",
                "1",
            ]
        )


def test_a_frame_does_not_cross_a_verse(tmp_path: Path) -> None:
    """آخرُ كلمةٍ في آيةٍ وأوّلُ التي تليها ليسا في إطارٍ واحد."""

    rows = [("1:1:1", "أ"), ("1:1:2", "ب"), ("1:2:1", "ج"), ("1:2:2", "د")]
    built = shahid.frames(rows)
    assert built[1] == ("أ", "ب", shahid.EDGE)
    assert built[2] == (shahid.EDGE, "ج", "د")

    # ولا حافّةَ تُصنَع من طرفٍ حدُّه فراغ
    assert shahid.neighbours(built) == set()


def test_two_centres_in_one_frame_are_neighbours(tmp_path: Path) -> None:
    """«س _ ل» تجمع «م» و«ن»: شاهدُ إحلالٍ مرصودٌ لا علاقةٌ مفترضة."""

    _, _, _ = _write_alignment(tmp_path)
    rows = [
        (f"1:{verse}:{word}", surface)
        for verse, text in enumerate(VERSES, start=1)
        for word, surface in enumerate(text, start=1)
    ]
    edges = shahid.neighbours(shahid.frames(rows))
    assert frozenset(("م", "ن")) in edges
    assert all(len(edge) == 2 for edge in edges)


def test_the_signature_cell_is_a_pair_not_a_margin(tmp_path: Path) -> None:
    """خانةُ التوقيع زوجٌ (صنفُ السابق، صنفُ اللاحق) — جدولٌ لا هامشان."""

    rows = [
        (f"1:{verse}:{word}", surface)
        for verse, text in enumerate(VERSES, start=1)
        for word, surface in enumerate(text, start=1)
    ]
    classes = dict(CLASS_ROWS)
    table = shahid.signatures(shahid.frames(rows), classes)
    cells = {cell for counter in table.values() for cell in counter}
    assert all(isinstance(cell, tuple) and len(cell) == 2 for cell in cells)
    assert ("جار", "فعل") in table["م"]


def test_a_full_run_prints_the_five_conditions_with_its_stamp(tmp_path: Path) -> None:
    """خمسةُ شروطٍ مطبوعةٌ، ومعها الختمُ والنسبةُ — ولا z بلا قسمة."""

    lines = shahid.run(_arguments(tmp_path))
    joined = "\n".join(lines)
    for mark in ("ش١", "ش٢", "ش٣", "ش٤", "ش٥"):
        assert mark in joined
    assert shahid.SEAL[:12] in joined
    assert "النسبة:" in joined and "رسم-خام" in joined

    # ولا يُطبَع z إلّا مقسومًا على جذر الحوافّ للعقدة
    assert "ولا يُطبَع z إلّا مقسومًا" in joined


def test_the_column_is_named_and_carries_its_own_digest(tmp_path: Path) -> None:
    """عمودان في ملفٍّ واحدٍ بمفتاحٍ واحد، ولكلٍّ بصمة — فلا نقطةَ سقوطٍ واحدة."""

    lines = ["loc\tsurface\tsurface_phon"]
    for verse_index, verse in enumerate(VERSES, start=1):
        for word_index, one in enumerate(verse, start=1):
            lines.append(f"1:{verse_index}:{word_index}\t{one}\t{one}ـ")
    path = tmp_path / "two.tsv"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    rows = sum(len(one) for one in VERSES)

    raw = shahid.read_alignment(path, rows, digest, "surface")
    normalised = shahid.read_alignment(path, rows, digest, "surface_phon")
    assert [one for _, one in raw] != [one for _, one in normalised]
    assert shahid.column_digest([one for _, one in raw]) != shahid.column_digest(
        [one for _, one in normalised]
    )

    # وعمودٌ لا يوجد يُرَدّ باسمه ولا يُخمَّن
    with pytest.raises(shahid.ShahidError) as raised:
        shahid.read_alignment(path, rows, digest, "سطح")
    assert "لا عمودَ باسم" in str(raised.value)


def test_the_run_prints_declared_descriptions_apart_from_the_conditions(
    tmp_path: Path,
) -> None:
    """صدرٌ للشروط المختومة وصدرٌ للأوصاف — والوصفُ البعديُّ لا يصير شرطًا."""

    lines = shahid.run(_arguments(tmp_path))
    joined = "\n".join(lines)
    assert "— الشروطُ الخمسةُ المختومة —" in joined
    assert "— مقاماتٌ وأوصافٌ مُعلَنةٌ لا شروط —" in joined

    for description in (
        "نصيبُ العقد التي لها شاهدُ إحلالٍ أصلًا",
        "الدرجة: وسيطًا",
        "الفرقُ المقترنُ للعقدة",
        "إنتروبيا أحجام الفرق",
        "نصيبُ أكثر الإطارات تكرارًا",
    ):
        assert description in joined

    # وحكمُ ت٣ يُطبَع بش٥ لا وحدَه
    assert "ت٣: " in joined
    assert "بش٥" in joined


def test_the_paired_difference_is_measured_per_node_not_per_edge(
    tmp_path: Path,
) -> None:
    """وحدةُ الاستقلال العقدة: الفرقُ يُحسَب لكلّ عقدةٍ ثمّ تُعاود العقدُ لا الحوافّ."""

    rows = [
        (f"1:{verse}:{word}", surface)
        for verse, text in enumerate(VERSES, start=1)
        for word, surface in enumerate(text, start=1)
    ]
    built = shahid.frames(rows)
    edges = shahid.neighbours(built)
    held = shahid.signatures(built, dict(CLASS_ROWS))

    differences = shahid.paired_differences(edges, held, 1, 50)
    assert set(differences) <= set(held)
    assert len(differences) <= len(held)

    mean, low, high = shahid.clustered_interval(differences, 1, 200)
    assert low <= mean <= high


def test_the_degree_profile_counts_nodes_without_any_witness(tmp_path: Path) -> None:
    """عقدةٌ بلا حافّةٍ تُعَدّ في المقام: وسيطُ صفرٍ يعني نصفَ المفردات خارج القياس."""

    edges = {frozenset(("أ", "ب"))}
    median, mean, witnessed, highest = shahid.degree_profile(
        edges, {"أ", "ب", "ج", "د"}
    )
    assert median == 0.5  # اثنتان من أربعٍ بلا شاهد، فالوسيطُ بينهما
    assert mean == 0.5
    assert witnessed == 0.5
    assert highest == 1
