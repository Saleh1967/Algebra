"""«وحداتُ المعياريّة» — **جدولٌ ممسوحٌ بـ`ast` لا مكتوبٌ بيد**.

**العطلُ الذي تتجنّبه**: سُئلتُ أن أُعيد صياغةَ مكتبةِ بايثون المعياريّةِ
كلِّها. فقستُ أوّلًا: **٣٠٣ وحدة · ٦٥١ ملفًّا · ٢٩٨٣٧٧ سطرًا**. ورفضتُ
الصياغةَ لأنّ ما لا يُقرَأ لم يُكتَب. **والبديلُ المقيسُ هو هذا الجدول**:
ما تستورده الشجرةُ فعلًا، من أيِّ طبقة، وما لا تُعطيه الوحدةُ من الضمان.

**والاستيرادُ مقروءٌ بـ`ast` لا بـ`grep`**: `grep` يرى كلمةَ `import`
في تعليقٍ ونصٍّ، و`ast` لا يرى إلّا عقدةَ استيرادٍ حقيقيّة.

**وعمودُ «لا تُعطيه» مكتوبٌ بيد، وهذا مُعلَن**: فهو حكمٌ لا قياس.
وحارسُه أنّ كلَّ وحدةٍ مستورَدةٍ يلزمها مُدخَل — **فاستيرادٌ جديدٌ
بغيرِ مُدخَلٍ يُسقِط الفحصَ** لا يمرُّ صامتًا.

`AN_UNEXERCISED_PERMISSION_IS_A_PERMISSION_TOO_WIDE`: قائمةُ المسموحِ
في `src/algebra` تُقابَل بما يُستورَد فعلًا، والفرقُ يُطبَع. فرخصةٌ
لم تُستعمَل رخصةٌ يمكن تضييقُها، **ولا تُضيَّق ما لم تُقَس**.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import Final

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[1]
DOCS: Final[Path] = REPOSITORY / "docs"
PAPER: Final[Path] = DOCS / "وحدات-المعياريّة.md"
AUDIT: Final[Path] = REPOSITORY / "tests" / "algebra" / "test_package_self_audit.py"
EASTERN: Final[dict[int, int]] = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")

# الطبقاتُ بمسارِها لا باسمِها: المسارُ في الشجرة، والاسمُ للعرض.
LAYERS: Final[tuple[tuple[str, str], ...]] = (
    ("src/algebra", "الجبر"),
    ("src/hawk_dove", "الصقر"),
    ("src/alghanem", "النقل"),
    ("tools", "الأدوات"),
    ("tests", "الفحوص"),
    ("examples", "الأمثلة"),
)

# **ما لا تُعطيه الوحدة**: حكمٌ مكتوبٌ بيد، لا قياس. وكلُّ سطرٍ هو
# الضمانُ الذي يظنُّه القارئُ حاصلًا وليس بحاصل.
WITHHELD: Final[dict[str, str]] = {
    "__future__": "لا تُغيِّر سلوكًا وقتَ التشغيل؛ `annotations` تُؤخِّر التقييم فقط.",
    "abc": "لا تمنع إنشاءَ فرعٍ ناقصٍ قبلَ الاستدعاء؛ الخطأُ وقتَ الإنشاء لا وقتَ التعريف.",
    "argparse": "لا تتحقّق من معنى القيمة، بل من نوعِها؛ و«عددٌ صحيح» ليس «عددًا مقبولًا».",
    "ast": "لا تُقيّم؛ تُعطي الشكلَ لا الأثر. وفرعٌ ميتٌ في الشجرةِ عقدةٌ كغيرِه.",
    "collections": (
        "`Counter` لا تُرتّب عند التساوي إلّا بترتيبِ الإدخال؛ " "فالترتيبُ عَرَضٌ لا عقد."
    ),
    "contextlib": "لا تضمن تنفيذَ الخروجِ عند `os._exit` ولا عند إشارةٍ قاتلة.",
    "copy": "`deepcopy` لا تنسخ ما لا يُنسَخ (مِقبضُ ملفٍّ، قِفل)؛ تُخفِق أو تُشارِك.",
    "csv": "لا تُحدِّد الترميز؛ تقرأ ما يُعطيه الملفُّ المفتوح. **ومصدرُ التصحيفِ هنا**.",
    "dataclasses": (
        "`frozen=True` تمنع الإسنادَ لا التغييرَ في الداخل؛ "
        "قائمةٌ داخلَها تبقى قابلةً للتغيير."
    ),
    "datetime": (
        "لا تُثبِت وقتًا؛ تقرأ ساعةَ الجهاز. "
        "**ولهذا مرساةُ السلسلةِ بصمةُ إيداعٍ لا تاريخٌ مكتوب**."
    ),
    "decimal": (
        "عشريّةٌ مضبوطةُ الأساسِ عشرةً، لا كسرٌ نسبيّ؛ " "و`1/3` فيها مقرَّبةٌ كما في الثنائيّ."
    ),
    "enum": (
        "لا تمنع قيمةً خارجَ الأعضاء من المرورِ في تلميحِ نوع؛ "
        "التلميحُ لا يُفحَص وقتَ التشغيل."
    ),
    "fractions": "مضبوطةٌ بلا حدّ، **وبثمنٍ**: المقامُ ينمو، والنموُّ وقتٌ وذاكرةٌ لا خطأ.",
    "functools": "`lru_cache` تُمسك المُدخَلاتِ فلا تُجمَع؛ وذاكرةٌ لا تُحَدُّ عطلٌ لا تحسين.",
    "hashlib": "لا تُوثّق؛ تُبصِم. **وبصمةٌ بلا توقيعٍ تُثبِت الهُويّةَ لا النِّسبة**.",
    "heapq": "كومةُ أصغرٍ فقط؛ و«أكبر» تُنال بقلبِ الإشارةِ — وقلبُها على `Fraction` سليم.",
    "importlib": "تُنفّذ الوحدةَ عند التحميل؛ فاستيرادُ ملفٍّ لقياسِه **يُشغّله**.",
    "io": "لا تضمن ذرّيّةَ الكتابة؛ كتابةٌ نصفُها على القرصِ حالةٌ ممكنة.",
    "itertools": "مولّداتٌ تُستهلَك مرّةً؛ والمرورُ الثاني على مولّدٍ فراغٌ لا خطأ.",
    "json": (
        "لا تحفظ ترتيبَ المفاتيحِ إلّا بـ`sort_keys`، " "ولا تُميّز `1` من `1.0` بعد الدورة."
    ),
    "math": "على `float` لا على الكسر؛ فـ`math.sqrt` تُقرِّب، **وحدُّ الضبطِ ٢⁵³**.",
    "os": "لا تُجرِّد اختلافَ الأنظمة؛ وصلاحيّاتُ الملفِّ ومحارفُ المسارِ تبقى محلّيّة.",
    "pathlib": "لا تتحقّق من الوجود؛ `Path` نصٌّ مُبنيَنٌ لا مِقبضُ ملفّ.",
    "posixpath": "قواعدُ POSIX صريحةً؛ تُستعمَل حين يُقصَد شكلُ المسارِ لا مسارُ الجهاز.",
    "random": "**زائفةٌ لا عشوائيّة**؛ ومن لم يُودِع البذرةَ لم يُودِع التجربة.",
    "re": "`\\w` **لا يشمل الحركاتَ العربيّة**؛ فقسمةُ النصِّ بها تُضاعِف الألفاظَ ٣٫٥ مرّة.",
    "shutil": "لا تضمن ذرّيّةَ النقلِ بين نظامَي ملفّات؛ النقلُ صار نسخًا ثمّ حذفًا.",
    "statistics": "لا تُعلِم بعيّنةٍ صغيرةٍ جدًّا؛ متوسّطُ اثنين متوسّطٌ كمتوسّطِ ألف.",
    "subprocess": "لا تفحص رمزَ الخروجِ إلّا بـ`check=True`؛ **وسقوطٌ بلا فحصٍ نجاحٌ كاذب**.",
    "sys": "`stdlib_module_names` أسماءٌ لا مِلفّات؛ والوحدةُ المبنيّةُ داخلًا بلا ملفّ.",
    "types": "`MappingProxyType` تمنع الكتابةَ على الغلافِ لا على الأصل.",
    "typing": (
        "**لا تُفحَص وقتَ التشغيل**؛ فتلميحٌ صادقٌ ودالّةٌ كاذبةٌ يمرّان معًا. "
        "و`mypy` هو الفحص."
    ),
    "unicodedata": (
        "تُطبِّع بجدولِ إصدارِها، و`NFC` **تقلب الشدّةَ والتنوين** "
        "بصنفِ الدمج ٣٣ مقابل ٢٧–٢٩."
    ),
}


def eastern(one: object) -> str:
    return str(one).translate(EASTERN)


def grouped(one: int) -> str:
    return eastern(f"{one:,}".replace(",", "٬"))


def layer_of(relative: str) -> str | None:
    for prefix, name in LAYERS:
        if relative.startswith(prefix):
            return name
    return None


def imports_of(tree: ast.AST) -> list[str]:
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.extend(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            found.append(node.module.split(".")[0])
    return found


def scan() -> tuple[dict[str, dict[str, int]], int]:
    """يمسح الشجرةَ بـ`ast`، فيُعطي {وحدة: {طبقة: عدد}} وعددَ الملفّات."""

    standard = set(sys.stdlib_module_names)
    use: dict[str, dict[str, int]] = {}
    seen = 0
    for path in sorted(REPOSITORY.rglob("*.py")):
        relative = path.relative_to(REPOSITORY).as_posix()
        layer = layer_of(relative)
        if layer is None:
            continue
        seen += 1
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=relative)
        for name in imports_of(tree):
            if name in standard:
                use.setdefault(name, {})
                use[name][layer] = use[name].get(layer, 0) + 1
    return use, seen


def allowlist() -> frozenset[str]:
    """قائمةُ المسموحِ في `src/algebra`، مقروءةً من الحارسِ نفسِه.

    **لا تُنسَخ باليد**: نسخةٌ ثانيةٌ تختلف عن الأصلِ ولو مرّت في كليهما.
    """

    tree = ast.parse(AUDIT.read_text(encoding="utf-8"), filename=AUDIT.name)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if "standard" not in targets or not isinstance(node.value, ast.Set):
            continue
        names = [
            one.value
            for one in node.value.elts
            if isinstance(one, ast.Constant) and isinstance(one.value, str)
        ]
        if names:
            return frozenset(names)
    raise SystemExit(f"لا قائمةَ مسموحٍ في {AUDIT.name}")


def undocumented(use: dict[str, dict[str, int]]) -> tuple[str, ...]:
    """وحداتٌ مستورَدةٌ بلا مُدخَلٍ في «لا تُعطيه»."""

    return tuple(sorted(name for name in use if name not in WITHHELD))


def render() -> str:
    use, files = scan()
    permitted = allowlist()
    algebra_uses = frozenset(name for name, rows in use.items() if "الجبر" in rows)
    unexercised = tuple(sorted(permitted - algebra_uses))
    total = len(sys.stdlib_module_names)

    lines: list[str] = ["# وحداتُ المعياريّة", ""]
    lines += [
        "**مولَّدٌ بـ`tools/write_module_map.py`.** لا يُحرَّر بيد: يُعاد توليدُه",
        "ويُقابَل المكتوبُ بالمولَّد في فحص.",
        "",
        "## القياسُ أوّلًا",
        "",
        f"- وحداتُ المعياريّةِ في هذا المفسّر: **{eastern(total)}**",
        f"- ما تستورده الشجرةُ منها: **{eastern(len(use))}**"
        f" — أي {eastern(round(100 * len(use) / total))}٪",
        f"- ملفّاتُ `.py` الممسوحة: **{grouped(files)}**",
        "",
        "فمن قال «أُعيد صياغةَ المعياريّةِ كلِّها» لزمه قراءةُ",
        f"**{eastern(total)}** وحدةٍ لم يقرأها. **وما لم يُقرَأ لم يُكتَب.**",
        "",
        "## الرخصةُ في `src/algebra` أوسعُ من الاستعمال",
        "",
        f"- مسموحٌ في الحارس: **{eastern(len(permitted))}**",
        f"- مستعمَلٌ فعلًا في الجبر: **{eastern(len(algebra_uses))}**",
        f"- رخصةٌ لم تُستعمَل: **{eastern(len(unexercised))}**"
        f" — {'، '.join(f'`{one}`' for one in unexercised) or 'لا شيء'}",
        "",
        "**ورخصةٌ لم تُستعمَل رخصةٌ يمكن تضييقُها.** ولا تُضيَّق ههنا",
        "بلا سبب: التضييقُ حكمٌ، وهذا الجدولُ قياسُه.",
        "",
        "## الجدول",
        "",
        "| الوحدة | استيرادات | الطبقات | في الجبر؟ | **ما لا تُعطيه** |",
        "|---|---:|---|:---:|---|",
    ]
    for name in sorted(use):
        rows = use[name]
        count = grouped(sum(rows.values()))
        where = " · ".join(f"{k} {eastern(v)}" for k, v in sorted(rows.items()))
        if name in algebra_uses:
            mark = "مُستعمَل"
        elif name in permitted:
            mark = "مسموح"
        else:
            mark = "**ممنوع**"
        note = WITHHELD.get(name, "—")
        lines.append(f"| `{name}` | {count} | {where} | {mark} | {note} |")

    lines += [
        "",
        "## الممنوعُ في الجبرِ وحيثُ يُستعمَل",
        "",
    ]
    outside = sorted(name for name in use if name not in permitted)
    for name in outside:
        where = " · ".join(f"{k} {eastern(v)}" for k, v in sorted(use[name].items()))
        lines.append(f"- `{name}` — {where}")
    lines += [
        "",
        f"فهذه **{eastern(len(outside))}** وحدةً ممنوعةٌ في `src/algebra`",
        "وتُستعمَل خارجَه. وأظهرُها `unicodedata`: **لا تُستورَد في الجبرِ بتّةً**،",
        "لأنّ جدولَ التطبيعِ يتغيّر بإصدارِ المفسّر، والقياسُ لا يُبنى على",
        "جدولٍ متحرّك. **ولهذا بُنيت `algebra.rasm` بنقاطِ الترميزِ وحدَها.**",
        "",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    missing = undocumented(scan()[0])
    if missing:
        raise SystemExit("وحداتٌ بلا مُدخَلٍ في «لا تُعطيه»: " + "، ".join(missing))
    PAPER.write_text(render(), encoding="utf-8")
    print(f"أُودِع: {PAPER.relative_to(REPOSITORY)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
