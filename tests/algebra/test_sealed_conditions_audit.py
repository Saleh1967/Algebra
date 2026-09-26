"""أربعةُ موانعَ آليّةٍ لأربعةِ أعطالٍ كانت **بلا مانع** — ٧ و٨ و١٢ و١٧.

كان في سجلّ الأعطال أربعةٌ مكتوبٌ عندها صراحةً «**لا مانعَ آليًّا بعدُ**»،
أي أنّ تكرارَها ممكنٌ ولا يردُّه شيءٌ غيرُ النيّة. **والنيّةُ ليست بوّابة.**
فههنا تُنصَب لها موانعُ **تُشتَقُّ من الشجرة**، ولا يُستثنى منها إلّا ما
يُسمّى بالاسم في جدولٍ معروض.

- **المانعُ أ) — العطل ٧ (إغفالُ تسجيل ما يُحكَم به)**: كلُّ شرطٍ مختومٍ
  **يُحكَم به في تشغيله**. فشرطٌ يُكتَب ثمّ لا يُحكَم به عددٌ لم يُسجَّل،
  والشرحُ لا يسدُّ مسدَّه. وقد ردَّ هذا المانعُ `ل٥` أوّلَ نصبه: كان مكتوبًا
  في `34133d54…` وحكمُه في الشرح وحدَه، فصار يُعَدُّ الآن من المدوّنة سطرًا
  سطرًا في `test_huffman_ascent_run`.

- **المانعُ ب) — العطل ٨ (تعليلٌ خاطئ تحت شرطٍ مرّ)**: شطران.
  **الأوّلُ** أنّ كلَّ تشغيلٍ يحمل `REASONING_NOT_SUPPORTED` — الشروطَ التي
  **مرّت وتعليلُها لم يُؤيَّد بالقياس** — وإن كان فارغًا، كي يُسأل السؤالُ
  في كلّ مرّةٍ ولا يُطوى بالسكوت. **والثاني** أنّ كلَّ عددٍ ذي ثلاث منازلَ
  دالّةٍ فأكثرَ يُروى في **شرح** التشغيل يجب أن يُوجَد في **متنه** أو في
  **سجلٍّ يستشهد به**؛ وما ليس كذلك اليومَ **معروضٌ بعينه** في
  `NARRATED_WITHOUT_A_WITNESS` — أربعون عددًا، دَينٌ **يُرى ولا ينمو**.

  **وحدُّ هذا المانعِ مُعلَن**: يمنع أن **يُروى عددٌ بلا شاهد**، ولا يمنع أن
  **يُروى تعليلٌ لم يُقَس**. وذاك يبقى على القاعدة المكتوبة في العطل ١١:
  «لا تُنشَر آليّةٌ لم تُقَس» — قاعدةً مكتوبةً لا بوّابةً آليّة، ولا أدّعي
  غيرَ ذلك.

- **المانعُ ج) — العطل ١٢ (معنًى مختومٌ للسقوط لم يتحقّق)**: كلُّ شرطٍ يسقط
  يجب أن يُقتبَس **نصُّ ما عُلِّق على سقوطه** في تشغيله نفسِه، مطابقًا لنصّ
  الختم. فنصُّ `falsifies` **دعوًى ثانيةٌ معرَّضةٌ للسقوط**، وإعلانُ سقوطها
  يقع **عند موضع السقوط** لا في شرحٍ لاحق.

- **المانعُ د) — العطل ١٧ (نافذةٌ واحدةٌ لا تُلزِم الذراعين بالسواء)**: كلُّ
  ختمٍ يدّعي **عزلًا** يجب أن يُصرّح تشغيلُه بـ`THE_BOUND_BINDS_BOTH_ARMS`:
  أيَعَضُّ الحدُّ المُعلَنُ الذراعين بالسواء؟ — `True` أو `False` **مقيسًا
  بشاهد**، أو `Vacancy.UNRUN` **مُصنَّفًا**. ولا يُترَك السؤالُ بلا جواب.
  وقد ردَّ هذا المانعُ عزلًا ثانيًا لم يكن مشكوكًا فيه: في
  `test_marking_contrast_run` — العمقُ ٢٤ في الذراعين، ونصيبُ المرفوضات
  **٠٫٣٢٥٩ مقابلَ ٠٫٧٢٣٣**.

**وما لا يُمنَع يُقال**: هذه الموانعُ تحرس **الشكلَ** — أن يُحكَم، وأن
يُقتبَس، وأن يُصرَّح، وأن يُشهَد للعدد. ولا تحرس **الصوابَ**: شرطٌ يُحكَم به
بعددٍ خاطئ يمرُّ عليها، ومعنًى يُقتبَس ثمّ يُساء فهمُه يمرُّ عليها. فهي تردُّ
**الصمتَ**، لا الخطأ.
"""

from __future__ import annotations

import ast
import re

from sealed_reading import ARABIC, OUT_OF_REACH, REPOSITORY, Sealed, read_all

from algebra.results import Vacancy

ISOLATION_CLAIMS: tuple[str, ...] = (
    "لا يفترقان إلّا",
    "التغييرُ واحد",
    "المتغيّرُ واحد",
    "متغيّرٌ واحد",
    "عزل",
)
"""عباراتُ دعوى العزل؛ كلُّها مأخوذةٌ من متون الأختام لا مُخترَعة."""

NARRATED_WITHOUT_A_WITNESS: dict[str, tuple[str, ...]] = {
    "test_algebraic_ascent_run.py": (
        "0.8872",
        "112.0",
        "11953.0",
        "1406634.0",
        "1724461.0",
    ),
    "test_basmala_lifted_run.py": ("3056.0",),
    "test_crossing_census_run.py": ("485.0",),
    "test_discovered_ascent_run.py": (
        "0.8933",
        "277.0",
        "290.0",
        "311.0",
        "323.0",
        "334.0",
        "339.0",
        "418.0",
        "453.0",
        "455.0",
        "480.0",
        "481.0",
        "520.0",
        "21350.0",
    ),
    "test_heldout_ladder_run.py": ("0.0179", "0.0823", "9034199.0"),
    "test_layer_licence_run.py": ("0.7761", "3493.0"),
    "test_residue_derivation_run.py": (
        "0.2445",
        "0.2739",
        "0.4352",
        "0.5563",
        "0.794",
        "1538.0",
        "2657.0",
        "3918.0",
        "6743.0",
        "21454.0",
        "22034.0",
        "25013.0",
    ),
    "test_separation_rule_run.py": ("2.12",),
    "test_vowel_ladder_run.py": ("366.0",),
}
"""أعدادٌ رُويت في الشروح ولا شاهدَ لها في المتن ولا في سجلٍّ مستشهَدٍ به.

**وهي دَينٌ لا براءة**: تُعرَض بأعيانها كي **تُرى**، ولا يدخلها عددٌ جديدٌ
إلّا بيدٍ تكتبه. فالمانعُ يمنع **النموَّ**، والجدولُ يُنقِص بالإصلاح لا
بالسكوت. ومجموعُها اليومَ **أربعون**، والعددُ مفحوصٌ أدناه كي لا يزيد صمتًا.
"""

LEAST_QUOTE = 10
"""أقصرُ ما يُقبَل اقتباسًا من نصّ السقوط — كلمةٌ واحدةٌ لا تكفي شاهدًا."""

EASTERN = str.maketrans("٠١٢٣٤٥٦٧٨٩٬٫", "0123456789,.")
CITED = re.compile(r'(deposits|docs)[/"\s]+/?\s*"?([^\s"`)]+\.(?:log|md))')


def _figures(text: str) -> set[str]:
    """كلُّ عددٍ ذي ثلاث منازلَ دالّةٍ فأكثر، مُسوًّى إلى صورةٍ واحدة.

    والتسويةُ لازمة: الشرحُ يكتب `٨٬٥٠٧` والمتنُ يكتب `8_507.0`، وهما عددٌ
    واحد. فلولا التسويةُ لعُدَّ الشاهدُ غائبًا وهو حاضر.
    """

    plain = text.translate(EASTERN).replace(",", "").replace("_", "")
    found: set[str] = set()
    for one in re.findall(r"\d+(?:\.\d+)?", plain):
        if len(one.replace(".", "").lstrip("0")) >= 3:
            found.add(repr(float(one)))
    return found


def _outside_the_docstring(one: Sealed) -> str:
    tree = ast.parse(one.body)
    head = tree.body[0] if tree.body else None
    begins = (
        (head.end_lineno or 0)
        if isinstance(head, ast.Expr) and isinstance(head.value, ast.Constant)
        else 0
    )
    return "\n".join(one.body.splitlines()[begins:])


def _witnessed(one: Sealed) -> set[str]:
    """ما للتشغيل من شاهد: متنُه، وكلُّ سجلٍّ أو وثيقةٍ يستشهد بها باسمها."""

    found = _figures(_outside_the_docstring(one))
    for where, name in CITED.findall(one.body):
        path = REPOSITORY / where / name
        if path.exists():
            found |= _figures(path.read_text(encoding="utf-8"))
    return found


def test_every_run_either_binds_its_conditions_or_is_named_out_of_reach() -> None:
    """لا تشغيلَ يفلت من الموانع صمتًا: إمّا يُقرَأ وإمّا يُسمّى."""

    read = {one.run.name for one in read_all()}
    every = {one.name for one in ARABIC.glob("test_*_run.py")}
    assert read, "لم يُقرَأ تشغيلٌ واحد — القراءةُ نفسُها معطوبة"
    assert read | OUT_OF_REACH == every, sorted(every - (read | OUT_OF_REACH))
    assert not read & OUT_OF_REACH, sorted(read & OUT_OF_REACH)
    assert len(read) == 28


def test_every_sealed_condition_is_judged_in_its_own_run() -> None:
    """أ) شرطٌ يُكتَب ولا يُحكَم به عددٌ لم يُسجَّل — العطل ٧."""

    silent = {
        one.run.name: sorted(one.marks() - one.judged())
        for one in read_all()
        if one.marks() - one.judged()
    }
    assert not silent, silent
    assert sum(len(one.marks()) for one in read_all()) >= 140


def test_every_run_names_the_reasoning_its_measurement_did_not_support() -> None:
    """ب١) شرطٌ يمرُّ بتعليلٍ خاطئ ليس تأييدًا — والسؤالُ يُسأل كلَّ مرّة."""

    missing: list[str] = []
    named: dict[str, tuple[str, ...]] = {}
    for one in read_all():
        module = __import__(one.run.stem)
        found = getattr(module, "REASONING_NOT_SUPPORTED", None)
        if not isinstance(found, tuple) or any(
            not isinstance(two, str) for two in found
        ):
            missing.append(one.run.name)
            continue
        astray = set(found) - one.marks()
        assert not astray, f"{one.run.name}: {sorted(astray)}"
        assert not set(found) & one.falsified(), one.run.name  # مرَّ لا سقط
        if found:
            named[one.run.name] = found
    assert not missing, missing
    assert named == {
        "test_huffman_ascent_run.py": ("ل٤",),
        "test_context_ladder_run.py": ("ق٦",),
        "test_state_cycle_run.py": ("ح٣", "ح٤"),
        "test_stirling_greedy_run.py": ("غ٢", "غ٩"),
        "test_transfer_arrow_run.py": ("ظ٧",),
        "test_pausal_split_run.py": ("و٩", "و١٠"),
        "test_morph_residue_run.py": ("ص١١",),
    }, named


def test_no_run_narrates_a_figure_that_has_no_witness_anywhere() -> None:
    """ب٢) عددٌ يُروى في الشرح ولا شاهدَ له — دَينٌ معروضٌ لا ينمو."""

    astray: dict[str, list[str]] = {}
    stale: dict[str, list[str]] = {}
    for one in read_all():
        told = _figures(one.docstring)
        spared = set(NARRATED_WITHOUT_A_WITNESS.get(one.run.name, ()))
        bare = told - _witnessed(one)
        if bare - spared:
            astray[one.run.name] = sorted(bare - spared)
        if spared - bare:
            stale[one.run.name] = sorted(spared - bare)
    assert not astray, astray
    assert not stale, stale  # ولا يُترَك في الجدول ما بَرِئ
    assert sum(len(one) for one in NARRATED_WITHOUT_A_WITNESS.values()) == 40


def test_every_fallen_condition_quotes_what_fell_with_it() -> None:
    """ج) نصُّ `falsifies` دعوًى ثانيةٌ تسقط معه — العطل ١٢."""

    unquoted: dict[str, list[str]] = {}
    for one in read_all():
        bad = sorted(
            two
            for two in one.falsified()
            if not one.quotes(one.falsifies(two), LEAST_QUOTE)
        )
        if bad:
            unquoted[one.run.name] = bad
    assert not unquoted, unquoted
    assert sum(len(one.falsified()) for one in read_all()) == 53


def test_every_claim_of_isolation_answers_whether_its_bound_binds_alike() -> None:
    """د) حدٌّ واحدٌ في قيمته قد يكون مختلفًا في أثره — العطل ١٧."""

    silent: list[str] = []
    answered: dict[str, object] = {}
    for one in read_all():
        seal = ARABIC / one.run.name.replace("_run.py", "_seal.py")
        text = seal.read_text(encoding="utf-8") if seal.exists() else ""
        if not any(two in text for two in ISOLATION_CLAIMS):
            continue
        module = __import__(one.run.stem)
        answer = getattr(module, "THE_BOUND_BINDS_BOTH_ARMS", None)
        witness = getattr(module, "THE_BOUND_EVIDENCE", "")
        if not (isinstance(answer, bool) or answer is Vacancy.UNRUN):
            silent.append(one.run.name)
            continue
        if len(witness) < 40:
            silent.append(f"{one.run.name} — شاهدٌ دون أربعين حرفًا")
            continue
        answered[one.run.name] = answer
    assert not silent, silent
    assert len(answered) == 4, sorted(answered)
    assert sum(one is False for one in answered.values()) == 3
    assert sum(one is True for one in answered.values()) == 1


def test_the_four_guards_are_named_in_the_register_of_flaws() -> None:
    """ما صار له مانعٌ يُشطَب من «بلا مانع» في سجلّ الأعطال، بالاسم."""

    register = REPOSITORY / "docs" / "سجل-الأعطال.md"
    text = register.read_text(encoding="utf-8")
    for guard in ("أ)", "ب)", "ج)", "د)"):
        assert f"**المانعُ {guard}**" in text, guard
    assert "test_sealed_conditions_audit" in text
    assert "بلا مانع" in text  # والقاعدةُ نفسُها تبقى مكتوبة
