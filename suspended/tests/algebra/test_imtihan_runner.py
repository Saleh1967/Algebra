"""مُشغِّلُ امتحان المعنى مفحوصًا: يرفض أربعةً، ويقول «لا أحكم» حين يجب.

**ما يُقاس ههنا**: لا معنى ولا عربيّة. تُفحَص **الآلةُ**: أنّ ما اتُّفق عليه
قبل التشغيل صار **شرطَ تشغيلٍ** لا تنبيهًا. وأرقامُ العيّنة مُصطنَعةٌ ولا
تُنقَل إلى شيء.

`A_GUARD_THAT_CAN_BE_SKIPPED_IS_A_COMMENT`: ثلاثةُ شروطٍ قيلت قبل التشغيل —
قسمةٌ باللِّمّة، وتصنيفٌ بـ`k`، ومعنويّةٌ على اللِّمَم. وقولُها لا يُغني: فإن
أمكن تشغيلُ الآلة بدونها فهي تعليقٌ في هامش. فههنا **كلُّها تُرَدّ عند
التشغيل**، ويُفحَص ردُّها.

`THE_ORDER_OF_REPRESENTATIONS_IS_DECLARED_NOT_INFERRED`: أوّلُ تشغيلٍ رتّب
التمثيلاتِ **أبجديًّا**، فخرج الميلُ **سالبًا** على بيانٍ ميلُه موجب — لأنّ
«+نافذة» تسبق «الطبقات» في الترتيب لا في الغنى. والغنى ليس خاصّةً في الاسم.
فصار الترتيبُ مُدخَلًا يُعلَن، ويُرَدّ التشغيلُ بدونه. وهو عيبٌ أخرجته
الآلةُ عن نفسها في أوّل دورة.

`ONE_REPRESENTATION_PRINTS_NUMBERS_AND_WITHHOLDS_THE_VERDICT`: تمثيلٌ واحدٌ
لا يفصل «تمثيلًا خاطئًا» عن «معنًى من خارج»، فالآلةُ تطبع الأرقامَ وتمتنع
عن الحكم صراحةً. والامتناعُ مطبوعٌ لا مسكوتٌ عنه.

`AN_OCCURRENCE_CITATION_IS_NOT_A_READING_CERTIFICATE`: قانونٌ مأخوذٌ من شجرة
الغانم إلى ههنا. فحلُّ موضعٍ في مصدرٍ مُبصَّمٍ يُثبِت الوقوعَ لا الوسم؛ والوسمُ
يحتاج **جهةً تُسمّى وتُقارَن بمُعلِن الدعوى**. وامتحانُ المعنى كان يجري عندي
بمقياسٍ وصفريٍّ وحدودٍ وبلا جهةٍ واسمةٍ مُعلَنةٍ ألبتّة — وهو ثقبٌ لم أُسمِّه،
فصار الآن شرطَ تشغيلٍ: جدولٌ بلا جهةٍ يُرَدّ، وجهةٌ هي المُعلِنُ نفسُه تُرَدّ.

`THE_COMPARISON_UNIT_IS_THE_CHOICE_THAT_WAS_NOT_ENUMERATED`: وفي شجرة الغانم
نفسِها بوّابةٌ ثالثةٌ تقابل مضمونَ الوسم بمضمون الحالة **تطابقًا حرفيًّا بعد
التسوية** (`minimal_complete_fiber.gloss_agrees`)، ولا تُسمّي ذلك اختيارًا ولا
تُعدّه في بقاياها المُسمّاة. وعلى عيّنتي: جاكار يعطي ٢٥٫٠٠٪ والتطابقُ التامُّ
٢٠٫٨٣٪، والميلُ +٦٢٫٥٠ مقابل +٦٦٫٦٧ — أربعُ نقاطٍ من اختيارٍ لم يُعلَن. وهو
الجنسُ نفسُه الذي رُدَّ به عليّ عشرَ مرّات: **مجالٌ لم يُعدَّد**.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPOSITORY = Path(__file__).resolve().parents[2]
RUNNER_PATH = REPOSITORY / "examples" / "maana" / "run_imtihan.py"


def _load() -> object:
    spec = importlib.util.spec_from_file_location("run_imtihan", RUNNER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


RUNNER = _load()


def _material() -> tuple[dict[str, tuple[str, str]], list[object]]:
    glosses = RUNNER.read_glosses_text(RUNNER.SMOKE_GLOSSES)  # type: ignore[attr-defined]
    trials = RUNNER.read_runs_text(RUNNER.SMOKE_RUNS)  # type: ignore[attr-defined]
    return glosses, trials


def _authority() -> object:
    return RUNNER.Authority(  # type: ignore[attr-defined]
        authority_id="كتابٌ_مُصطنَع",
        authority_note="عيّنةُ فحصٍ للآلة",
        declarer_id="مُعلِنٌ_مُصطنَع",
    )


def _report(trials: object, glosses: object, **kwargs: object) -> None:
    kwargs.setdefault("authority", _authority())
    kwargs.setdefault("match", "تداخلُ_جاكار")
    RUNNER.report(trials, glosses, **kwargs)  # type: ignore[attr-defined]


def test_a_split_that_shares_a_lemma_is_refused_by_name() -> None:
    """لِمّةٌ في القسمين تُرَدّ باسمها؛ وجردُ شروحها هو المتسرّب."""

    RUNNER.assert_split_is_by_lemma(  # type: ignore[attr-defined]
        frozenset({"وليّ", "بيّنة"}), frozenset({"أسرى", "كتاب"})
    )
    with pytest.raises(RUNNER.ImtihanError) as raised:  # type: ignore[attr-defined]
        RUNNER.assert_split_is_by_lemma(  # type: ignore[attr-defined]
            frozenset({"وليّ", "بيّنة"}), frozenset({"وليّ", "كتاب"})
        )
    assert "وليّ" in str(raised.value)
    assert "باللِّمّة" in str(raised.value)

    with pytest.raises(RUNNER.ImtihanError):  # type: ignore[attr-defined]
        RUNNER.assert_split_is_by_lemma(frozenset({"وليّ"}), frozenset())  # type: ignore[attr-defined]


def test_the_pooled_report_alone_is_refused() -> None:
    """المجمَّعُ بلا شرائحِ `k` يُخفي صفريًّا يتغيّر عشرةَ أضعاف، فيُرَدّ."""

    glosses, trials = _material()
    with pytest.raises(RUNNER.ImtihanError) as raised:  # type: ignore[attr-defined]
        _report(trials, glosses, pooled_only=True)
    assert "٠٫٥٠" in str(raised.value)
    assert "k" in str(raised.value)


def test_the_representation_order_must_be_declared() -> None:
    """ترتيبٌ غيرُ مُعلَنٍ يُرَدّ؛ وترتيبٌ لا يطابق التمثيلاتِ يُرَدّ كذلك."""

    glosses, trials = _material()
    with pytest.raises(RUNNER.ImtihanError) as raised:  # type: ignore[attr-defined]
        _report(trials, glosses, order=())
    assert "--order" in str(raised.value) or "يُعلَن" in str(raised.value)

    with pytest.raises(RUNNER.ImtihanError):  # type: ignore[attr-defined]
        _report(trials, glosses, order=("الطبقات",))
    with pytest.raises(RUNNER.ImtihanError):  # type: ignore[attr-defined]
        _report(trials, glosses, order=("الطبقات", "الطبقات", "+نافذة"))


def test_the_alphabetical_order_would_have_flipped_the_slope() -> None:
    """الفرزُ بالاسم يعطي «+نافذة» قبل «الطبقات» — وهو عكسُ الغنى.

    وذلك بعينه ما وقع في أوّل دورة: ميلٌ سالبٌ على بيانٍ ميلُه موجب. ولا
    يمسكه فحصٌ إلّا أن يصير الترتيبُ مُدخَلًا.
    """

    representations = {"الطبقات", "+نافذة"}
    alphabetical = tuple(sorted(representations))
    declared = ("الطبقات", "+نافذة")
    assert alphabetical != declared
    assert alphabetical[0] == "+نافذة"  # الأغنى أوّلًا لو فُرِز بالاسم


def test_one_representation_prints_numbers_and_withholds_the_verdict(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """تمثيلٌ واحدٌ: الأرقامُ تُطبَع والحكمُ يمتنع — والامتناعُ مطبوع."""

    glosses, trials = _material()
    single = [trial for trial in trials if trial.representation == "الطبقات"]
    _report(single, glosses, order=("الطبقات",))
    printed = capsys.readouterr().out
    assert "الحكمُ **يمتنع**" in printed
    assert "الميلُ عبر" not in printed
    assert "k=2" in printed  # والشرائحُ تُطبَع رغم امتناع الحكم


def test_a_trial_whose_answer_is_not_among_the_candidates_is_refused() -> None:
    """موضعٌ جوابُه خارجَ المرشَّحين غيرُ قابلٍ للحلّ، فلا يُحتسَب صامتًا."""

    with pytest.raises(RUNNER.ImtihanError) as raised:  # type: ignore[attr-defined]
        RUNNER.Trial(  # type: ignore[attr-defined]
            representation="س", ref="1:1", lemma="ل", gold="g9", ranked=("g1", "g2")
        )
    assert "غيرُ قابلٍ للحلّ" in str(raised.value)

    with pytest.raises(RUNNER.ImtihanError):  # type: ignore[attr-defined]
        RUNNER.Trial(  # type: ignore[attr-defined]
            representation="س", ref="1:1", lemma="ل", gold="g1", ranked=()
        )


def test_the_interval_is_computed_on_lemmas_not_on_positions() -> None:
    """المجالُ من متوسّطات اللِّمَم؛ ولِمّةٌ واحدةٌ لا يُحسَب منها مجال."""

    glosses, trials = _material()
    rich = [trial for trial in trials if trial.representation == "+نافذة"]
    scorer = RUNNER.MATCH_POLICIES["تداخلُ_جاكار"]  # type: ignore[attr-defined]
    means = RUNNER.by_lemma(rich, glosses, scorer)  # type: ignore[attr-defined]
    assert len(means) == 4  # أربعُ لِمَمٍ من ثمانية مواضع
    assert len(means) < len(rich)

    centre, half = RUNNER.clustered_interval(means)  # type: ignore[attr-defined]
    assert 0 <= centre <= 1
    assert half > 0

    with pytest.raises(RUNNER.ImtihanError):  # type: ignore[attr-defined]
        RUNNER.clustered_interval({"وليّ": 0.5})  # type: ignore[attr-defined]


def test_the_overlap_metric_is_jaccard_on_content_words() -> None:
    """تداخلٌ لا مطابقة: «الحجج الواضحات» و«الحجج الواضحة» يشتركان في كلمة."""

    assert RUNNER.overlap("الحجة الواضحة", "الحجة الواضحة") == 1  # type: ignore[attr-defined]
    assert RUNNER.overlap("الحجة الواضحة", "الدليل الساطع") == 0  # type: ignore[attr-defined]

    partial = RUNNER.overlap("الحجة الواضحة", "الحجة الظاهرة")  # type: ignore[attr-defined]
    assert 0 < partial < 1

    # والنصّان الخاليان تداخلُهما صفرٌ لا واحد
    assert RUNNER.overlap("في من على", "عن إلى") == 0  # type: ignore[attr-defined]


def test_the_smoke_run_completes_and_declares_itself_synthetic(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """التشغيلُ يتمّ، ويُصدِّر مخرَجَه بأنّ العيّنةَ مُصطنَعةٌ لا تقول شيئًا."""

    assert RUNNER.main(["--smoke"]) == 0  # type: ignore[attr-defined]
    printed = capsys.readouterr().out
    assert "مُصطنَعة" in printed
    assert "ولا تقول شيئًا عن العربيّة" in printed
    assert "+62.50" in printed  # الميلُ موجبٌ بعد إعلان الترتيب
    assert "صفريٌّ" in printed
    assert "الجهةُ الواسمة" in printed


def test_a_gloss_table_without_a_named_authority_is_refused() -> None:
    """جدولٌ بلا جهةٍ واسمةٍ لا يُقرَأ سندًا — وذلك ما كان ناقصًا عندي."""

    glosses, trials = _material()
    with pytest.raises(RUNNER.ImtihanError) as raised:  # type: ignore[attr-defined]
        RUNNER.report(  # type: ignore[attr-defined]
            trials, glosses, order=("الطبقات", "+نافذة"), match="تداخلُ_جاكار"
        )
    assert "جهةٍ واسمة" in str(raised.value)


def test_an_authority_that_is_the_declarer_is_refused_by_construction() -> None:
    """وسمٌ يكتبه صاحبُ الدعوى على دعواه مردودٌ — وفصلُ الملفّ لا يُغني."""

    with pytest.raises(RUNNER.ImtihanError) as raised:  # type: ignore[attr-defined]
        RUNNER.Authority(  # type: ignore[attr-defined]
            authority_id="الغانم",
            authority_note="الشجرةُ نفسُها",
            declarer_id="الغانم",
        )
    assert "صاحبُ الدعوى" in str(raised.value)

    # وثلاثةُ حقولٍ لا حقلان: مُعلِنُ الدعوى يُكتَب وإلّا لم تقع المقارنة
    for missing in ("authority_id", "authority_note", "declarer_id"):
        texts = {
            "authority_id": "كتاب",
            "authority_note": "بيان",
            "declarer_id": "مُعلِن",
        }
        texts[missing] = "   "
        with pytest.raises(RUNNER.ImtihanError):  # type: ignore[attr-defined]
            RUNNER.Authority(**texts)  # type: ignore[attr-defined]


def test_the_match_policy_must_be_declared_and_named() -> None:
    """سياسةُ المقابلة تُعلَن؛ وغيرُ المُعلَنةِ تُرَدّ باسم المُعلَن منها."""

    glosses, trials = _material()
    with pytest.raises(RUNNER.ImtihanError) as raised:  # type: ignore[attr-defined]
        _report(trials, glosses, order=("الطبقات", "+نافذة"), match="")
    assert "--match" in str(raised.value)

    with pytest.raises(RUNNER.ImtihanError):  # type: ignore[attr-defined]
        _report(trials, glosses, order=("الطبقات", "+نافذة"), match="أقربُ_معنًى")

    assert set(RUNNER.MATCH_POLICIES) == {  # type: ignore[attr-defined]
        "تطابقٌ_تامّ",
        "تداخلُ_جاكار",
    }


def test_the_two_declared_policies_give_two_different_numbers() -> None:
    """٢٥٫٠٠٪ بجاكار و٢٠٫٨٣٪ بالتطابق التامّ — والفرقُ اختيارٌ لا قياس.

    وهو الموضعُ الذي تركته الشجرةُ المقابلةُ غيرَ مُعدَّد: بوّابتُها الثالثة
    تقابل حرفًا بحرفٍ ولا تُسمّي ذلك اختيارًا؛ فجهةٌ مستقلّةٌ تكتب نثرَها لا
    تطابق حرفًا بحرف، فلا تُجاز إلّا أن يُنقَل عنها نصًّا — وحينئذٍ يقيس
    الفحصُ النقلَ لا الموافقة.
    """

    glosses, trials = _material()
    poor = [trial for trial in trials if trial.representation == "الطبقات"]

    numbers = {}
    for name in ("تداخلُ_جاكار", "تطابقٌ_تامّ"):
        scorer = RUNNER.MATCH_POLICIES[name]  # type: ignore[attr-defined]
        means = RUNNER.by_lemma(poor, glosses, scorer)  # type: ignore[attr-defined]
        numbers[name] = round(RUNNER.clustered_interval(means)[0] * 100, 2)  # type: ignore[attr-defined]

    assert numbers["تداخلُ_جاكار"] == 25.00
    assert numbers["تطابقٌ_تامّ"] == 20.83
    assert numbers["تداخلُ_جاكار"] > numbers["تطابقٌ_تامّ"]


def test_the_exact_policy_refuses_an_empty_text_as_a_match() -> None:
    """نصّان خاليان لا يتطابقان: الخلوُّ ليس موافقةً، في السياستين معًا."""

    exact = RUNNER.MATCH_POLICIES["تطابقٌ_تامّ"]  # type: ignore[attr-defined]
    assert exact("الحجة الواضحة", "الحجة الواضحة") == 1
    assert exact("الحجة الواضحة", "الحجة الظاهرة") == 0
    assert exact("  ", "") == 0
    assert RUNNER.overlap("", "") == 0  # type: ignore[attr-defined]
