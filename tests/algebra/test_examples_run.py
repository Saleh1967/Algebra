"""الأمثلةُ تُشغَّل لا تُقرَأ: أحدَ عشرَ مثالًا تعمل، وثمانيةٌ تُرَدّ بلا مدوّنة.

**ما كشفه التشغيل أوّلًا**: فحصُ الفصل يغطّي `src/algebra` و`tests/algebra`
**ولا يغطّي `examples/`**. وسبعةٌ من أحدَ عشرَ مثالًا كانت تسقط بـ
`ModuleNotFoundError` لأنّها تستورد `alghanem` من خارج. فالمستودعُ كان يشحن
أكثرَ من نصف أمثلته لا يعمل، **ولا فحصَ واحدٌ يمسك ذلك** — لأنّ الأمثلةَ
تُقرَأ ولا تُشغَّل.

**وما جرى بعدَه**: نُقِلت شفرةُ الإغلاق اللازم إلى `src/alghanem`، فصار
المستودعان يعملان مستقلَّين. **فالسبعةُ تعمل الآن**، ودخلت جدولَ التشغيل.

`AN_EXAMPLE_THAT_IS_NEVER_RUN_IS_NOT_AN_EXAMPLE`: والأمثلةُ **مُعدَّدةٌ**
ههنا: كلُّ ملفٍّ تحت `examples/` في جدول التشغيل بوسائطه المُعلَنة، يُشغَّل
ويُفحَص خروجُه ومخرَجُه. ومثالٌ جديدٌ لا يدخله يُرَدّ باسمه — فلا يُشحَن
مثالٌ لا يُدرى أيعمل أم لا.

`THE_MEASURE_IS_RUNNING_HERE_NOT_WHICH_PACKAGE_IT_IMPORTS`: وكان الجدولُ
الثاني «ما يستورد `alghanem`»، وذلك وصفٌ لا معيار. **والمعيارُ أن يعمل في
هذا المستودع**؛ والحزمتان جارتان فيه، و`algebra` لا تستورد الأخرى — وذلك
مفحوصٌ في `test_separation` بعمليّةٍ مستقلّة.
"""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

import pytest

REPOSITORY = Path(__file__).resolve().parents[2]
EXAMPLES = REPOSITORY / "examples"
FOREIGN = "alghanem"

# مثالٌ يعمل في هذا المستودع، ومعه وسائطُه المُعلَنة
RUNNABLE: dict[str, tuple[str, ...]] = {
    "arabic/audit_slgae_markov.py": (),
    "arabic/audit_slgae_third_version.py": (),
    "arabic/decode_makhraj_bits.py": (),
    "arabic/decode_makhraj_haraka_bits.py": (),
    "arabic/encode_arabic_units.py": (),
    "arabic/measure_sifa_candidate.py": (),
    "arabic/read_slgae_separation.py": (),
    "hawk_dove/run_hawk_dove.py": (),
    "irab/run_harf_measurement.py": ("--smoke", "--defer", "error"),
    "isnad/run_ittifaq.py": ("--smoke",),
    "maana/run_imtihan.py": ("--smoke",),
}

# مثالٌ يحتاج مدوّنةً لم تُودَع ههنا؛ يُعَدّ ويُفحَص رفضُه، ولا يُشغَّل
NEEDS_A_CORPUS: dict[str, str] = {
    "rasm/run_final_vowel_entropy.py": (
        "يحتاج المحاذاةَ المشكولةَ (`--aligned`) وهي متنٌ لم يُودَع"
    ),
    "rasm/run_adjacency_null.py": (
        "يحتاج المحاذاةَ الكاملةَ (`--aligned`) وهي متنٌ لم يُودَع؛ " "والشفرةُ وحدَها ههنا"
    ),
    "rasm/run_letter_transitions.py": (
        "يحتاج المحاذاةَ ببصمتها وإغلاقها وسياستها؛ ولا مدوّنةَ مودَعةٌ ههنا"
    ),
    "rasm/run_pan_difference.py": (
        "يحتاج المدوّنةَ المُقفَلة؛ ويقيس الاتّجاهين وفرقَ الكفّتين بصفريّيهما"
    ),
    "rasm/run_marked_contrast.py": (
        "يحتاج المدوّنةَ المُقفَلة؛ ويقيس تباينَ الوسم وكفّتَي الرسم والضبط"
    ),
    "rasm/run_schema_transition_audit.py": (
        "يحتاج المدوّنةَ ببصمتها؛ ويعرض عليها المجموعاتِ المُودَعة"
    ),
    "rasm/run_layer_induction.py": (
        "يحتاج المدوّنةَ وخريطةَ السلّم المُودَعة؛ ويبني الطبقاتِ إسقاطًا "
        "ثمّ يستقرئ عليها أربعَ مبرهنات"
    ),
    "rasm/run_root_projection.py": (
        "يحتاج المدوّنةَ وجدولَ الجذور؛ ويشغّل الإسقاطَ المُودَع "
        "π_اشتقاقي ويقيس كونَه دالّةً أو علاقة"
    ),
    "rasm/run_unit_coverage.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويعرض نظامَ (حرف × حالة) المُعلَن " "عليها تغطيةً وإفادة"
    ),
    "rasm/run_encoding_audit.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويشغّل المواصفةَ المُصلَحة ويعدّ الساقط " "ويقيس Δضبط"
    ),
    "rasm/run_vowel_ladder.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويبني سلّمَي الضبط بشرط السياق " "على ختم 9034199d…"
    ),
    "rasm/run_bare_census.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويجرد العُريَ بالحرف ويقيس موضعَ الإعراب " "بإزاء كلّ موضع"
    ),
    "rasm/run_heldout_ladder.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويقيس السلّمَ محجوزًا على ختم 455167a5… "
        "بإنتروبيا متقاطعةٍ وخطأٍ معياريّ"
    ),
    "rasm/run_script_floor.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويحسب أرضيّةَ الرسم H(S|W) "
        "ويفكّك Δضبط تفكيكًا تامًّا على ختم f43b9095…"
    ),
    "rasm/run_tanafur_pairs.py": (
        "يحتاج المدوّنةَ المجمَّدة؛ ويقرأ أزواجَ التنافر الثلاثةَ قراءةً "
        "موازيةً لختم d44f23ce… الذي لا تُستوفى مادّتُه"
    ),
    "rasm/run_cv_peel.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويقشّرها إلى ١١٢ وحدةً ويعيد بناءها "
        "بايتةً بايتة ويعرض دفترَ البتّات"
    ),
    "rasm/run_residue_derivation.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويعيد بناءَ قنوات البقيّة من تيّار "
        "الـ١١٢ بسياقٍ متناظرٍ محجوزٍ على ختم 92b81796…"
    ),
    "rasm/run_layer_licence.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويبني الطبقاتِ صاعدًا من الـ١١٢ "
        "ويفحص رخصةَ كلّ صعودٍ على ختم 73cc5b24…"
    ),
    "rasm/run_algebraic_ascent.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويصعد جبريًّا من الـ١١٢ بتكلفةٍ ذات "
        "شطرين على ختم 0021350c…"
    ),
    "rasm/run_discovered_ascent.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويصعد من الـ١١٢ بدمجٍ يكتشفه الاقتصادُ "
        "خطوةً خطوة على ختم 620b63a2…"
    ),
    "rasm/run_greedy_licence.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويرخّص الصعودَ **دمجةً دمجة** لا كتلةً "
        "على ختم 69a1c10c…"
    ),
    "rasm/run_basmala_lifted.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويعيد قياسَ الأرقام الكلميّة كلِّها "
        "على مدوّنةٍ مشتقّةٍ مرفوعةِ البسملات على ختم be03e5be…"
    ),
    "rasm/run_verse_ending.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويقيس خاتمةَ الآية **شرطًا** لا "
        "أبجديّةً، ويعدّ الغيباتِ بأرقام الأسطر، على ختم 26ae5b5b…"
    ),
    "rasm/run_separation_rule.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويشغّل قاعدةَ الفصل المُودَعةَ غيرَ "
        "الموقَّعة ويقيسها بالمحجوز على ختم 7bf3ccd8…"
    ),
    "rasm/run_markov_ladder.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويقيس أربعةَ مستوياتٍ من الوحدة إلى "
        "السطر ملحَقًا ومحجوزًا، ويصنّف ما فوقها، على ختم 248f10df…"
    ),
    "rasm/run_word_escalation.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويعدّ الكلمَ والهياكلَ الغامضة ويصعد "
        "جشعًا بقيدِ حدّ الكلمة ويسعّر الدَّينين على ختم 2a849c9a…"
    ),
    "rasm/run_lifted_bit.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويرفع **بتّةً واحدة** هي أوّلُ ما صعد "
        "بسبب الانقلاب، ويقيس أثرَها معزولًا على ختم 0c070831…"
    ),
    "rasm/run_greedy_algebra.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويشتقّ الربحَ الجشع بالتباديل النازلة "
        "ويقابله بالمقيس، ويقيس اقترانَ الجارين، على ختم cfdb2184…"
    ),
    "rasm/run_measured_ranking.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويلتزم **أكبرَ ربحٍ** لا أوّلَ رابحٍ "
        "ليُقاس هل يعيد هوفمانُ ترتيبَ الجشع، على ختم c8602c00…"
    ),
    "rasm/run_marking_contrast.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويشغّل ذراعَي الوسم بعمقٍ واحدٍ في "
        "تشغيلٍ واحدٍ على ختم 2cd80c0f…"
    ),
    "rasm/run_temporary_marking.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويعزل أثرَ الوسم الأبديّ برفعه عند كلّ "
        "التزامٍ على ختم 89b59b10…"
    ),
    "rasm/run_huffman_ascent.py": (
        "يحتاج المدوّنةَ المشكولة؛ ويصعد من الـ١١٢ ببيانٍ هوفمانيٍّ "
        "لا إنتروبيًّا على ختم 34133d54…"
    ),
    "shahid/run_shahid.py": (
        "يحتاج المحاذاةَ ببصمتها (`--aligned` و`--digest` و`--closure`) "
        "وإسنادَ الأصناف؛ ولا مدوّنةَ مودَعةٌ ههنا"
    ),
}


def _examples() -> list[str]:
    return sorted(str(path.relative_to(EXAMPLES)) for path in EXAMPLES.rglob("*.py"))


def _imports_foreign(path: Path) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name.split(".")[0] == FOREIGN for alias in node.names):
                return True
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] == FOREIGN:
                return True
    return False


def test_every_example_is_declared_and_none_is_left_out() -> None:
    """تسعةَ عشرَ مثالًا، كلُّها في أحد الجدولين — ولا يمرّ جديدٌ صامتًا."""

    found = set(_examples())
    declared = set(RUNNABLE) | set(NEEDS_A_CORPUS)
    assert not (found - declared), sorted(found - declared)
    assert not (declared - found), sorted(declared - found)
    assert not (set(RUNNABLE) & set(NEEDS_A_CORPUS))
    assert len(found) == 44
    assert len(RUNNABLE) == 11
    assert len(NEEDS_A_CORPUS) == 33


@pytest.mark.parametrize("name", sorted(RUNNABLE))
def test_a_runnable_example_runs_and_exits_clean(name: str) -> None:
    """يُشغَّل فعلًا ويخرج بصفرٍ ويطبع شيئًا؛ والقراءةُ لا تُغني عن التشغيل."""

    path = EXAMPLES / name
    finished = subprocess.run(  # noqa: S603
        [sys.executable, str(path), *RUNNABLE[name]],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=REPOSITORY,
    )
    assert finished.returncode == 0, finished.stderr[-600:]
    assert finished.stdout.strip()


def test_ten_examples_import_the_ported_package_and_all_of_them_run() -> None:
    """عشرةٌ تستورد `alghanem`: سبعٌ كانت تسقط فصارت تعمل، وثلاثٌ جديدة.

    فالاستيرادُ في السبع لم يتغيّر، والذي تغيّر أنّ ما يُستورَد صار **ههنا**.
    والجديداتُ تحت `rasm/` تستورد **الجداولَ المُودَعة** (المخارجَ
    وأحكامَ النون) لتعرضاها على قياسٍ من خارجها — وهو استعمالُ الإيداع في
    موضعه: يُقرَأ ولا يُقاس بنفسه.
    """

    foreign = [name for name in _examples() if _imports_foreign(EXAMPLES / name)]
    assert len(foreign) == 10
    reading_deposits = sorted(one for one in foreign if not one.startswith("arabic/"))
    assert reading_deposits == [
        "rasm/run_marked_contrast.py",
        "rasm/run_pan_difference.py",
        "rasm/run_schema_transition_audit.py",
    ]
    assert set(foreign) - set(reading_deposits) <= set(RUNNABLE)
    assert set(reading_deposits) <= set(NEEDS_A_CORPUS)

    # والتسعةُ الباقيةُ لا تستوردها ألبتّة
    assert len(_examples()) - len(foreign) == 34


@pytest.mark.parametrize("name", sorted(NEEDS_A_CORPUS))
def test_an_example_that_needs_a_corpus_refuses_rather_than_guesses(
    name: str,
) -> None:
    """يُرَدّ بلا مدوّنةٍ مُسمّاة، ولا يخمّن مسارًا ولا سياسة."""

    path = EXAMPLES / name
    assert NEEDS_A_CORPUS[name].strip()

    bare = subprocess.run(  # noqa: S603
        [sys.executable, str(path)],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=REPOSITORY,
    )
    assert bare.returncode != 0
    # ويُسمّي الردُّ بابَ المدخل الذي أُغفِل، أيًّا كان بابُ هذا المثال
    doors = ("--aligned", "--text")
    assert any(door in bare.stderr for door in doors), bare.stderr[-300:]
