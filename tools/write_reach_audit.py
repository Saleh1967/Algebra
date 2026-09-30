"""«مدى الإحاطة» — **قياسُ آلاتِ الشجرةِ لضبطِ ما يتجاوز القراءة**.

**السؤالُ الذي يجيب عنه**: إذا كان حجمُ المسألةِ يتجاوز وقتَ الإنسانِ
وقدرتَه على الإحاطة، **فبأيِّ شيءٍ يُعرَف أنّ الجوابَ صحيحٌ لا مُقنِع؟**
فالعينُ لا تُراجِع ١٣١٩٩٠١ بايتًا، ولا ٢٠٠٠ فحصٍ، ولا ٧٢ وديعة. **وما
لا يُراجَع بالعينِ يلزمه آلةٌ تردُّه، لا ثقةٌ تقبله.**

وهذه الوثيقةُ تقيس **ثلاثَ آلاتٍ** موجودةً في هذه الشجرة، لكلٍّ عددٌ
مُشتَقٌّ لا مكتوب:

١. **الختمُ قبلَ التشغيل** — أنّ الشرطَ أُودِع قبلَ أن يُعرَف جوابُه،
   مُثبَتًا بترتيبِ التاريخ لا بتصريحِ كاتبه.
٢. **الحالةُ المُكذِّبة** — أنّ لكلّ دعوًى صورةً لو وقعت لَردَّتها،
   وأنّ تلك الصورةَ مُجرَّبةٌ ساقطةٌ فعلًا.
٣. **البيئةُ الثانية** — أنّ الحارسَ عمل في غيرِ بيئةِ كاتبه. **وحارسٌ
   لم يعمل إلّا على قرصٍ واحدٍ لم يُقَس** (العطل ٣٧).

`A_NUMBER_THAT_FLATTERS_ITS_AUTHOR_IS_MEASURED_WRONG`: وكلُّ عددٍ ههنا
يُحتمَل أن يكون في غيرِ مصلحتي، **وحدُّ طريقةِ عدِّه مكتوبٌ معه**. فما
عُدَّ بنمطِ اسمٍ يُسمّى **حدًّا أدنى** لا عددًا، وما عُدَّ بقراءةِ
البنيةِ يُسمّى مضبوطًا. **ولا يُقال «كلُّ» حيث الطريقةُ تعُدُّ بعضًا.**
"""

from __future__ import annotations

import ast
import re
import subprocess  # noqa: S404
from dataclasses import dataclass
from pathlib import Path
from typing import Final


@dataclass(frozen=True, slots=True)
class Gate:
    """بوّابةُ تخطٍّ مقروءةً: اسمُها، وشرطُها، وملفُّها، وما تشمله."""

    name: str
    where: str
    files: tuple[str, ...]
    condition: str
    covered: int


REPOSITORY: Final[Path] = Path(__file__).resolve().parents[1]
DOCS: Final[Path] = REPOSITORY / "docs"
PAPER: Final[Path] = DOCS / "مدى-الإحاطة.md"
TESTS: Final[Path] = REPOSITORY / "tests"
DEPOSITS: Final[Path] = REPOSITORY / "deposits"
EXAMPLES: Final[Path] = REPOSITORY / "examples"
CORPUS: Final[Path] = REPOSITORY / "quran-simple-enhanced.txt"
EASTERN: Final[dict[int, int]] = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")

# **أنماطُ اسمِ الفحصِ الرادّ** — مُعلَنةٌ لأنّ العدَّ بها حدٌّ أدنى.
REFUSAL: Final[tuple[str, ...]] = (
    "refused",
    "rejected",
    "would_have",
    "falsif",
    "lied",
    "is_not",
    "never",
    "no_",
    "cannot",
    "without",
)

# عباراتُ إعلانِ الصورةِ المُكذِّبةِ في المتن — والعدُّ بها أضيقُ وأصدق.
DECLARED: Final[str] = "مكذِّب"


def eastern(one: object) -> str:
    return str(one).translate(EASTERN)


def grouped(one: int) -> str:
    return eastern(f"{one:,}".replace(",", "٬"))


def _git(*args: str) -> str:
    done = subprocess.run(  # noqa: S603
        ["git", *args],  # noqa: S607
        cwd=REPOSITORY,
        capture_output=True,
        text=True,
        check=False,
    )
    return done.stdout


def tracked(relative: str) -> bool:
    """أمتعقَّبٌ في الشجرة؟ — **فغيرُ المتعقَّبِ غائبٌ عن كلّ نسخةٍ جديدة**."""

    return bool(_git("ls-files", "--", relative).strip())


def test_files() -> list[Path]:
    return sorted(TESTS.rglob("test_*.py"))


def definitions() -> int:
    """عددُ تعريفاتِ `def test_` — لا عددُ ما يُجمَع (فالتوسيعُ يزيده)."""

    total = 0
    for path in test_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=path.name)
        total += sum(
            1
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
        )
    return total


def refusing() -> tuple[int, int]:
    """(بنمطِ الاسم، بإعلانٍ في المتن) — **الأوّلُ حدٌّ أدنى بنمط**."""

    by_name = 0
    by_text = 0
    for path in test_files():
        body = path.read_text(encoding="utf-8")
        tree = ast.parse(body, filename=path.name)
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue
            if not node.name.startswith("test_"):
                continue
            if any(one in node.name for one in REFUSAL):
                by_name += 1
            told = ast.get_docstring(node) or ""
            if DECLARED in told:
                by_text += 1
    return by_name, by_text


def _module_strings(tree: ast.Module) -> dict[str, list[str]]:
    """إسناداتُ الوحدةِ كلُّها، ولكلٍّ نصوصُها — لتُحَلَّ أسماءُ الشرط."""

    found: dict[str, list[str]] = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        names = [one.id for one in node.targets if isinstance(one, ast.Name)]
        texts = [
            one.value
            for one in ast.walk(node.value)
            if isinstance(one, ast.Constant) and isinstance(one.value, str)
        ]
        for name in names:
            found[name] = texts
    for node in tree.body:
        if not isinstance(node, ast.AnnAssign) or node.value is None:
            continue
        if not isinstance(node.target, ast.Name):
            continue
        found[node.target.id] = [
            one.value
            for one in ast.walk(node.value)
            if isinstance(one, ast.Constant) and isinstance(one.value, str)
        ]
    return found


def _condition_of(node: ast.Assign) -> ast.expr | None:
    """عقدةُ شرطِ `pytest.mark.skipif` — **العقدةُ وحدَها لا نافذةُ محارف**.

    **العطلُ الذي عالجه**: قرأتُ الشرطَ أوّلَ مرّةٍ بنافذةِ ٤٠٠ محرفٍ
    بعد اسمِ البوّابة، فانسابت إلى التعريفِ الذي يليه **فنسبت إلى
    `requires_corpus` ملفًّا ليس لها**، وأعطت عددًا كاذبًا. ونافذةُ
    محارفَ ليست قراءةً — وهذا عينُ ما تنهى عنه هذه الوثيقةُ في حدِّها.
    """

    call = node.value
    if not isinstance(call, ast.Call) or not call.args:
        return None
    seen = ast.unparse(call.func)
    if not seen.endswith("mark.skipif"):
        return None
    return call.args[0]


def decorated(where: Path, name: str) -> int:
    """كم فحصًا يشمله المُزيِّنُ `name` في هذا الملفّ — **بعقدةِ التزيين**.

    **العطلُ الذي عالجه**: عددتُ أوّلَ مرّةٍ بـ`@name` نصًّا، **فعدَّ
    الاسمَ حيث يُذكَر في نصٍّ أو تصريحٍ لا حيث يُزيِّن**. فحارسي في
    `test_ci_workflow.py` يشترط `body.count("@needs_history") == 3`،
    فعُدَّ ذكرُه تزيينًا وزاد العددُ واحدًا بلا سبب. **والعقدةُ تُفرِّق
    بين الذكرِ والفعل، والنصُّ لا يُفرِّق.**
    """

    tree = ast.parse(where.read_text(encoding="utf-8"), filename=where.name)
    whole = any(
        isinstance(node, ast.Assign)
        and any(
            one.id == "pytestmark" for one in node.targets if isinstance(one, ast.Name)
        )
        and isinstance(node.value, ast.Name)
        and node.value.id == name
        for node in tree.body
    )
    tests = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
    ]
    if whole:
        return len(tests)
    return sum(
        1
        for node in tests
        for one in node.decorator_list
        if isinstance(one, ast.Name) and one.id == name
    )


def gates() -> list[Gate]:
    """بوّاباتُ التخطّي، ولكلٍّ ما تتوقّف عليه — مقروءًا بـ`ast`.

    والملفُّ الذي تتوقّف عليه يُستخرَج بحلِّ أسماءِ الشرطِ إلى إسناداتِ
    وحدتها، فـ`not ROOT_TABLE.is_file()` تُحَلُّ إلى نصِّ `ROOT_TABLE`.
    **وشرطٌ لا يبلغ اسمَ ملفٍّ يُسمّى «بيئةً لا ملفًّا» ولا يُفترَض فيه.**
    """

    found: list[Gate] = []
    for path in sorted(TESTS.rglob("*.py")):
        body = path.read_text(encoding="utf-8")
        tree = ast.parse(body, filename=path.name)
        strings = _module_strings(tree)
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            condition = _condition_of(node)
            if condition is None:
                continue
            name = next(
                (one.id for one in node.targets if isinstance(one, ast.Name)), ""
            )
            used = {one.id for one in ast.walk(condition) if isinstance(one, ast.Name)}
            files = sorted(
                {
                    text
                    for one in used
                    for text in strings.get(one, [])
                    if re.fullmatch(r"[A-Za-z0-9_.\-]+\.(csv|txt|json|md)", text)
                }
            )
            covered = sum(decorated(one, name) for one in test_files())
            found.append(
                Gate(
                    name=name,
                    where=str(path.relative_to(REPOSITORY)),
                    files=tuple(files),
                    condition=ast.unparse(condition),
                    covered=covered,
                )
            )
    return found


def listed() -> dict[str, tuple[str, ...]]:
    """قوائمُ التخطّي المُسمّاةُ في `tests/arabic/conftest.py`.

    فالتخطّي ثَمَّ **بأسماءِ الفحوصِ لا بمُزيِّن**، فلا يُعَدُّ بـ`@`.
    """

    where = TESTS / "arabic" / "conftest.py"
    tree = ast.parse(where.read_text(encoding="utf-8"), filename=where.name)
    out: dict[str, tuple[str, ...]] = {}
    for node in tree.body:
        target = None
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            target = node.target.id
        elif isinstance(node, ast.Assign):
            target = next(
                (one.id for one in node.targets if isinstance(one, ast.Name)), None
            )
        value = getattr(node, "value", None)
        if target is None or value is None:
            continue
        names = tuple(
            sorted(
                one.value
                for one in ast.walk(value)
                if isinstance(one, ast.Constant)
                and isinstance(one.value, str)
                and "::" in one.value
            )
        )
        if names:
            out[target] = names
    return out


def unreachable(rows: list[Gate]) -> list[Gate]:
    """بوّاباتٌ **لا تُنال في نسخةٍ جديدة**: تتوقّف على غيرِ متعقَّب."""

    return [
        row for row in rows if row.files and not all(tracked(one) for one in row.files)
    ]


def corpus_size() -> tuple[int, int]:
    raw = CORPUS.read_bytes()
    return len(raw), len(raw.decode("utf-8").splitlines())


def merged() -> list[Gate]:
    """البوّاباتُ مجموعةً باسمها — فبوّابتان باسمٍ واحدٍ وشرطٍ واحدٍ واحدة."""

    out: dict[str, Gate] = {}
    for row in gates():
        kept = out.get(row.name)
        if kept is None:
            out[row.name] = row
            continue
        joined = f"{kept.where} · {row.where}"
        out[row.name] = Gate(
            name=kept.name,
            where=joined,
            files=kept.files,
            condition=kept.condition,
            covered=kept.covered,
        )
    return [out[one] for one in sorted(out)]


def census() -> dict[str, int]:
    """إحصاءُ ما لا يعمل في نسخةٍ جديدة — **ويُصالَح بعددٍ مستقلّ**."""

    rows = merged()
    by_mark = sum(one.covered for one in unreachable(rows))
    named = listed()
    by_list = len(named.get("NEEDS_THE_ROOT_TABLE", ()))
    always = len(named.get("MEASURES_THE_TREE_IT_LIVES_IN", ()))
    return {
        "بالمُزيِّن": by_mark,
        "بالقائمة": by_list,
        "متنٌ غائب": by_mark + by_list,
        "تُخطّى في كلّ بيئة": always,
        "المجموع": by_mark + by_list + always,
    }


def render() -> str:
    total = definitions()
    by_name, by_text = refusing()
    rows = merged()
    counted = census()
    size, lines = corpus_size()
    runs = len(list(EXAMPLES.rglob("run_*.py")))
    kept = len([one for one in DEPOSITS.iterdir() if one.is_file()])

    out: list[str] = ["# مدى الإحاطة", ""]
    out += [
        "**مولَّدٌ بـ`tools/write_reach_audit.py`.** لا يُحرَّر بيد.",
        "",
        "## السؤال",
        "",
        "إذا تجاوز حجمُ المسألةِ وقتَ الإنسانِ وقدرتَه على الإحاطة،",
        "**فبأيِّ شيءٍ يُعرَف أنّ الجوابَ صحيحٌ لا مُقنِع؟**",
        "",
        "## ما لا يبلغه الإنسانُ قراءةً — في هذه الشجرةِ وحدَها",
        "",
        "| | |",
        "|---|---:|",
        f"| بايتاتُ المدوّنة | {grouped(size)} |",
        f"| أسطرُها | {grouped(lines)} |",
        f"| تعريفاتُ `def test_` | {grouped(total)} |",
        f"| تشغيلاتُ الأمثلة | {grouped(runs)} |",
        f"| الودائع | {grouped(kept)} |",
        "",
        "**ولا واحدَ من هذه يُراجَع بالعين.** فالآلةُ ليست تسريعًا",
        "لمراجعةٍ ممكنة، بل **بديلٌ عن مراجعةٍ متعذّرة** — ولهذا يلزمها",
        "أن تردَّ، لا أن تُطمئن.",
        "",
        "## الآلةُ الأولى: الختمُ قبلَ التشغيل",
        "",
        "الشرطُ يُودَع ويُدفَع **قبلَ** أن يُعرَف جوابُه، فترتيبُه في",
        "التاريخ قابلٌ للإثبات. ومقياسُه في `tools/seal_chain.py`:",
        "**المرساةُ دفعةٌ في التاريخ لا تاريخٌ مكتوب** — فالمكتوبُ يُكتَب",
        "بيدٍ، والدفعةُ لا.",
        "",
        "**وحدُّها مُعلَنٌ ثَمَّ**: تُثبِت أنّ البصمةَ كانت في تلك الدفعة،",
        "**لا أنّ التشغيلَ تلا الختمَ**.",
        "",
        "## الآلةُ الثانية: الحالةُ المُكذِّبة",
        "",
        "**دعوًى بلا صورةٍ تردُّها ليست دعوًى.** فتُصطنَع الصورةُ التي لو",
        "وقعت لَسقط الحارس، **وتُجرَّب فتسقط فعلًا** — وإلّا حرسَ ما لا",
        "يقع.",
        "",
        "| طريقةُ العدّ | العدد | من | حدُّها |",
        "|---|---:|---:|---|",
        f"| نمطُ اسمِ الفحص | {grouped(by_name)} | {grouped(total)} |"
        " **حدٌّ أدنى**: يُفلِت الرادَّ باسمٍ لا يحمل النمط |",
        f"| إعلانٌ صريحٌ في متنِ الفحص | {grouped(by_text)} | {grouped(total)} |"
        " **أضيقُ وأصدق**: لا يُعَدُّ إلّا ما صُرِّح به |",
        "",
        "والأنماطُ المعدودةُ مُعلَنةٌ في المولّد: "
        + "، ".join(f"`{one}`" for one in REFUSAL)
        + ".",
        "",
        f"**والفرقُ بين {grouped(by_name)} و{grouped(by_text)} هو الفجوة**:",
        "أكثرُ الردِّ ههنا **مفعولٌ غيرُ مُصرَّحٍ به**. وردٌّ لا يُعلَن لا",
        "يُحتَجُّ به على منهج، **وإن كان يعمل**. فمن يقرأ الشجرةَ بعدي لا",
        "يرى أيَّ دعوًى مضمونةٌ بصورةٍ مُجرَّبة.",
        "",
        "## الآلةُ الثالثة: البيئةُ الثانية",
        "",
        "**حارسٌ لم يعمل إلّا على قرصِ كاتبه لم يُقَس.** ومقيسٌ لا",
        "مُدَّعى: العطلُ ٣٧ كان بصمةَ سلسلةِ الأختامِ تتبع إصدارَ `git`،",
        "**ولم يظهر حتّى عمل حارسُها في بيئةٍ ثانيةٍ أوّلَ مرّة**.",
        "",
        "| البوّابة | شرطُها | الملفّ | متعقَّب؟ | تشمل |",
        "|---|---|---|:---:|---:|",
    ]
    for row in rows:
        where = "، ".join(f"`{one}`" for one in row.files) or "**بيئةٌ لا ملفّ**"
        if not row.files:
            mark = "—"
        else:
            mark = "نعم" if all(tracked(one) for one in row.files) else "**لا**"
        out.append(
            f"| `{row.name}` | `{row.condition}` | {where} | {mark} |"
            f" {grouped(row.covered)} |"
        )

    out += [
        "",
        "وقائمتان في `tests/arabic/conftest.py` تُخطّيان **بأسماءِ الفحوصِ",
        "لا بمُزيِّن**، فلا تُعَدّان بـ`@`:",
        "",
        "| القائمة | فحوص |",
        "|---|---:|",
        f"| `NEEDS_THE_ROOT_TABLE` | {grouped(counted['بالقائمة'])} |",
        f"| `MEASURES_THE_TREE_IT_LIVES_IN` | {grouped(counted['تُخطّى في كلّ بيئة'])} |",
        "",
        "### المصالحةُ بعددٍ مستقلّ",
        "",
        "وهذه الأعدادُ مُشتَقّةٌ من **بنيةِ الشجرة**، لا من تشغيل. فتُقابَل",
        "بما طبعه Runner في الطلب ٦١، وهو قياسٌ في بيئةٍ أخرى بأداةٍ أخرى:",
        "",
        "| | |",
        "|---|---:|",
        f"| بالمُزيِّن، على متنٍ غيرِ متعقَّب | {grouped(counted['بالمُزيِّن'])} |",
        f"| بالقائمةِ المُسمّاة | {grouped(counted['بالقائمة'])} |",
        f"| **فمتنٌ غائبٌ جملةً** | **{grouped(counted['متنٌ غائب'])}** |",
        f"| وتُخطّى في كلّ بيئةٍ لسببٍ بنيويّ | {grouped(counted['تُخطّى في كلّ بيئة'])} |",
        f"| **المجموعُ المتوقَّع** | **{grouped(counted['المجموع'])}** |",
        "| وما طبعه Runner | ٣٢ |",
        "",
        "**فتصالحَ العددان.** وليست هذه مصادفةً تُستحسَن بل **شرطٌ**:",
        "لو تفارقا لكان أحدُ القياسين خاطئًا، **ولا يُعرَف أيُّهما بلا",
        "ثالث**.",
        "",
        "## وأيُّها أضعف",
        "",
        "**الثانيةُ في إعلانها، والثالثةُ في مداها.**",
        "",
        f"- الردُّ **يعمل** في {grouped(by_name)} موضعًا على الأقلّ،"
        f" **ويُعلَن** في {grouped(by_text)}.",
        f"- و{grouped(counted['متنٌ غائب'])} فحصًا لم يبلغها إلّا قرصٌ واحد."
        " **وذاك ليس خطأً في الفحوصِ بل في إيداعِ متنِها** — وهو مكتوبٌ",
        "  لا مرفوع.",
        "",
        "**وحدُّ هذا العدِّ مُعلَن**: يُقرَأ الشرطُ بـ`ast` لا بنافذةِ",
        "محارف. وقد قرأتُه أوّلَ مرّةٍ بنافذةِ ٤٠٠ محرفٍ فانسابت إلى",
        "التعريفِ الذي يليه، **فنسبت إلى `requires_corpus` ملفًّا ليس لها",
        f"وأعطت {grouped(426)} بدلَ {grouped(counted['بالمُزيِّن'])}**."
        " ونافذةُ محارفَ ليست قراءةً.",
        "",
        "**ولا تُرفَع فجوةٌ بذكرها.** وهذه الوثيقةُ تقيس، والرفعُ دفعاتٌ",
        "تليها — كلٌّ منها بختمٍ قبلَ تشغيله.",
        "",
    ]
    return "\n".join(out) + "\n"


def main() -> int:
    PAPER.write_text(render(), encoding="utf-8")
    print(f"أُودِع: {PAPER.relative_to(REPOSITORY)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
