"""جذرُ الشجرة — **يُشتَقّ منها** لا يُكتَب يدًا، ويحمل اعتمادَه موقَّعًا.

كان `README.md` أشدَّ ملفٍّ يُقرَأ **وأقلَّه حراسةً**: مكتوبًا بيدٍ، لا
مولّدَ له ولا فحصَ يقابله. **فكلُّ رقمٍ فيه كان يَبلى صامتًا** — وذلك عينُ
ما مُنِع في `docs/` بسبعةَ عشرَ مولّدًا وفحصٍ لكلٍّ منها.

فههنا يُولَّد الجذرُ: أعدادُه من الشجرة (الأختامُ وشروطُها، والسجلّاتُ
المُقفَلة، والأعطالُ، والإيداعاتُ، والسقوفُ)، وما يقف مقروءًا من
`tools/write_entry.py` **مصدرًا واحدًا لا نسختين**، وبصمةُ المدوّنة
والمقابلةِ من ختمَيهما. **ولا رقمَ في الجذر يُطبَع بيد.**

وفيه **الاعتماد**: `tools/root_certificate.py` يُقفِل ما يتبنّاه صاحبُ
المستودع فرضًا وما يستثنيه، **موقَّعًا باسمه بالوكالة ومُفصِحًا عنها**.
"""

from __future__ import annotations

import importlib.util
import posixpath
import re
import sys
from pathlib import Path
from typing import Any, Final

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[1]
TOOLS: Final[Path] = REPOSITORY / "tools"
DOCS: Final[Path] = REPOSITORY / "docs"
DEPOSITS: Final[Path] = REPOSITORY / "deposits"
ROOT: Final[Path] = REPOSITORY / "README.md"
CEILING_GUARD: Final[Path] = REPOSITORY / "tests" / "algebra" / "test_ceiling_audit.py"
EASTERN: Final[dict[int, int]] = str.maketrans("0123456789.", "٠١٢٣٤٥٦٧٨٩٫")

PACKAGES: Final[tuple[tuple[str, str], ...]] = (
    (
        "algebra.simplicial",
        "المركّباتُ البسيطة على أيّ مجموعةِ رؤوس، بحدٍّ **مؤشَّر** وأعدادِ "
        "بيتي بكسورٍ صحيحة، ومَعيارِ أويلر شاهدًا مستقلًّا",
    ),
    (
        "algebra.decisions",
        "سجلُّ قراراتٍ بأنواعٍ مغلقة: فرعٌ بلا ثمنٍ لا يُقيَّد، ومُفوَّضٌ "
        "يُفرَّق فيه مَن يملك القرارَ مِن مَن اختار",
    ),
    (
        "algebra.attainability",
        "هل يبلغ اختبارٌ حدَّه بآلته أصلًا؟ أرضيّةُ التباديل، ومخارجُ الرفض "
        "المتاحة، وأدنى تكرارٍ لحدٍّ مُعلَن",
    ),
    (
        "algebra.factor_language",
        "لغاتُ العوامل الممنوعة: التعدادُ الشامل، وانغلاقُ البادئة، "
        "والشجرةُ **مُشتَقّةً** بعُقَدِها وحوافِّها — لا مرسومةً بيد",
    ),
    (
        "algebra.contingency",
        "جدولُ اقترانٍ ٢×٢ بكسورٍ صحيحة: `G` والأرجحيّةُ والنسب، وكُلفةُ "
        "النموذجين بالبتّات مع **فحص المتطابقة** `فرقُ البتّات = G/(2N ln2)`",
    ),
    (
        "algebra.lumping_loss",
        "خسارةُ القسمة بصيغتين مُتطابقتين — `Σ w·KL` و`Σ W·H − Σ w·H` — "
        "وأمثلُ قسمةٍ ببرمجةٍ ديناميكيّةٍ في `O(k·3ⁿ)`، **وفجوةُ الجشع مقيسة**",
    ),
    (
        "algebra.ceiling",
        "سقفُ النسبة قبل حدِّها: `(المقام − الممتنع) ÷ المقام` — ويردُّ حدًّا "
        "فوق سقفه **خلوًّا لا سقوطًا**، ومقيسًا فوق سقفه **عطلًا في أحد الرقمين**",
    ),
    (
        "hawk_dove",
        "لعبةُ الصقر والحمامة بكسورٍ صحيحة: توازنٌ مُشتَقٌّ من شرط "
        "اللامبالاة، و`optimality_gap` موجبٌ دائمًا",
    ),
)
"""ما تفعله كلُّ حزمة؛ والأسماءُ تُقابَل بالشجرة في فحص الجذر."""


def eastern(one: object) -> str:
    return str(one).translate(EASTERN)


def grouped(one: int) -> str:
    return eastern(f"{one:,}".replace(",", "٬"))


def _tool(name: str) -> Any:
    path = TOOLS / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"لا قارئَ لـ{name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def ceilings() -> tuple[int, int, int]:
    """(المُصرَّحُ بها، الكلُّ، المُصنَّف) — مقروءةً من المانع لا مظنونة."""

    text = CEILING_GUARD.read_text(encoding="utf-8")
    classified = re.search(r"^CLASSIFIED = (\d+)$", text, re.M)
    declared = re.search(r"^    assert seen == (\d+)$", text, re.M)
    if classified is None or declared is None:
        raise SystemExit("لا عددَ للسقوف في المانع هـ)")
    said, left = int(declared.group(1)), int(classified.group(1))
    return (said, said + left, left)


def from_root(where: str) -> str:
    """مسارُ المدخل نسبةً إلى الجذر — فالإشاراتُ لا تُعلَّق."""

    return posixpath.normpath(posixpath.join("docs", where))


def render() -> str:
    entry = _tool("write_entry.py")
    index = _tool("write_seal_index.py")
    rerun = _tool("rerun_audit_seal.py")
    corpus = _tool("corpus_seal.py")
    adoption = _tool("root_certificate.py")

    seals = index.gather()
    marks = sum(int(one["count"]) for one in seals)
    records = index.records()
    flaws = re.findall(
        r"^## [٠-٩]+\) ",
        (DOCS / "سجل-الأعطال.md").read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    made = entry.generated()
    papers = sorted({one.name for one in DOCS.glob("*.md")})
    logs = sorted(DEPOSITS.glob("*.log"))
    said, whole, left = ceilings()
    frozen = rerun.FROZEN_RERUN
    compared_bytes = sum(two for _, two, _ in frozen.rows)
    grain = corpus.FROZEN_RECORD
    sealed = adoption.FROZEN_ADOPTION

    out: list[str] = []
    add = out.append
    add("# Algebra")
    add("")
    add("**جذرُ المشروع — مُشتَقٌّ من الشجرة، ومعتمَدٌ موقَّعًا.**")
    add("")
    add("يُولَّد هذا الملفُّ بـ`tools/write_root.py`، ويحرس")
    add("`tests/algebra/test_root_is_certified.py` أنّ المكتوبَ مطابقٌ لما")
    add("يولّده — **فلا رقمَ فيه يُحرَّر بيد، ولا رقمَ يَبلى صامتًا**.")
    add("")
    add("## القاعدةُ الواحدة")
    add("")
    add("**الشرطُ يُكتَب ويُدفَع قبل التشغيل، والترتيبُ في تاريخ المستودع.**")
    add("ولا يُعاد تفسيرُ شرطٍ بعد رؤية رقمه؛ وما لم يُقَس **يُقال إنّه لم**")
    add("**يُقَس**؛ وما لا مانعَ له آليًّا **يُقال إنّه بلا مانع**.")
    add("")
    add("**والبوّابةُ واحدة**: `bash tools/verify.sh` — بلا أنبوبٍ حول الفحص،")
    add("فرمزُ خروجها رمزُ ما سقط.")
    add("")
    add("## الحالُ عددًا")
    add("")
    add("| المقيس | العدد |")
    add("|---|---|")
    add(f"| أختامٌ مُسجَّلةٌ قبل النظر | **{grouped(len(seals))}** |")
    add(f"| شروطٌ فيها | **{grouped(marks)}** |")
    add(f"| سجلّاتٌ مُقفَلةٌ ببصمةٍ تُعاد | {grouped(len(records))} |")
    add(f"| أعطالٌ مُسجَّلةٌ على الآلة | **{grouped(len(flaws))}** |")
    add(f"| سجلّاتُ تشغيلٍ مُودَعةٌ ومتعقَّبة | **{grouped(len(logs))}** |")
    add(f"| وثائقُ في `docs/` | {grouped(len(papers))} |")
    add(f"| منها مولَّدةٌ ومحروسة | **{grouped(len(made))}** |")
    add(f"| سقوفٌ مُصرَّحٌ بها من {grouped(whole)} | **{grouped(said)}** |")
    add(f"| ومنها مُصنَّفٌ بسببه لا مُصفَّر | {grouped(left)} |")
    add("")
    add("**والمدخلُ** — ما يقف وأين يُقرَأ، مُشتَقًّا كذلك:")
    add("[`docs/مدخل.md`](docs/مدخل.md).")
    add("")
    add("## على أيّ بايتاتٍ يُقاس")
    add("")
    add(
        f"مدوّنةٌ **مُجمَّدةٌ ببصمة** `{grain.sha256_hex[:8]}…` — "
        f"**{grouped(grain.ayah_lines)}** سطرًا "
        f"و**{grouped(grain.byte_length)}** بايتة."
    )
    add("**ولا تُحمَل في هذه الشجرة**: تُستقبَل ببصمتها عند كلّ جلسة،")
    add("و`.gitignore` يستثني مقاصدَها.")
    add("")
    add("**والحرفُ يُقتطَع من المدوّنة ولا يُطبَع** — فالضبطُ والهمزُ والشدّةُ")
    add("تُقرَأ كما أُودِعت، ولا يدخل قياسًا حرفٌ كتبناه.")
    add("")
    add(
        f"**وكلُّ سجلٍّ يُعاد ويُقابَل بتًّا ببت**: {grouped(frozen.compared)} "
        f"سجلًّا، **{grouped(frozen.matched)}** مطابقًا، **صفرُ مخالفة** —"
    )
    add(f"{grouped(compared_bytes)} بايتةً مُقابَلة، وختمُ المقابلة")
    add(f"`{rerun.RECORD_DIGEST[:8]}…` (`tools/rerun_audit.py`).")
    add("")
    add("## ما يقف — وتفصيلُه في المدخل")
    add("")
    for number, (title, _body, where) in enumerate(entry.STANDING, start=1):
        name = where.rsplit("/", 1)[-1]
        add(f"**{eastern(number)}. {title}** — [`{name}`]({from_root(where)})")
        add("")
    add("## الحزمةُ — ما يُبرهَن بالحساب وحدَه")
    add("")
    add("| الحزمة | ما تفعله |")
    add("|---|---|")
    for name, does in PACKAGES:
        add(f"| `{name}` | {does} |")
    add("")
    add("**ولا كسرَ عائمٌ في الحزمة إلّا عند اللوغاريتم**، ولا استيرادَ من")
    add("طرفٍ ثالث — ويفحص ذلك `tests/algebra/test_package_self_audit.py`")
    add("على الشجرة لا على الوعد.")
    add("")
    add("## الاعتماد — موقَّعٌ وكالةً باسم صاحب المستودع")
    add("")
    add(f"**الاسم**: {sealed.signer}")
    add(f"**اليد**: {sealed.executed_by} — **وقّعت باسمه بأمرِه**")
    add(f"**السند**: {sealed.authority}، {sealed.authority_dated}")
    add(f"**الصائغ**: {sealed.drafter}")
    add(f"**ختمُ الاعتماد**: `{adoption.RECORD_DIGEST[:8]}…` —")
    add("`tools/root_certificate.py`")
    add("")
    for one in adoption.DISCLOSURE:
        add(f"{one}.")
    add("")
    add("فمن قرأ توقيعًا لا يعلم أنّه بالوكالة **فقد قُرِئ عليه غيرُ الواقع**؛")
    add("ومن قرأ تصديقَ مؤلِّفٍ على ما ألَّف **شهادةً مستقلّةً فقد زاد فيها**.")
    add("**والاعتمادُ يُدخِل الجذرَ في دائرة النقض ولا يُخرِجه منها.**")
    add("")
    add(f"### ما اعتُمِد — {eastern(len(sealed.certifies))} بنودٍ")
    add("")
    for number, one in enumerate(sealed.certifies, start=1):
        add(f"{eastern(number)}. {one}.")
    add("")
    add(f"### وما لم يُعتمَد — {eastern(len(sealed.withheld))} بنودٍ تُسمّى")
    add("")
    add("**كي لا تُظَنَّ معتمَدةً بالسكوت.** فتوقيعٌ بلا استثناءٍ يُقرَأ")
    add("تصديقًا على كلّ ما في الشجرة، **وذلك أوسعُ ممّا حُقِّق**:")
    add("")
    for number, one in enumerate(sealed.withheld, start=1):
        add(f"{eastern(number)}. {one}.")
    add("")
    add("## ما ليس في هذه الشجرة")
    add("")
    add("**لا دعوى على العربيّة، ولا استيرادَ من `alghanem` في `src/algebra`.**")
    add("ولكلِّ وحدةٍ باقٍ مُسمًّى يقول ما لا تقوله:")
    add("`THIS_MODULE_CLAIMS_NOTHING_ABOUT_ANY_LANGUAGE` في `simplicial`،")
    add("ونظيرُه في الباقيتَين.")
    add("")
    add("**والفصلُ عن `Saleh1967/Alghanem` قائمٌ بالبناء**: اسمُ التوزيعة صار")
    add("`algebra`، وحزمةُ `src/algebra` لا تستورد من `alghanem` ولا تقرأ")
    add("بايتاتِ مدوّنة، وما نُقِل **عُمِّم وقُيِّد**. و`src/alghanem` **نقلٌ")
    add("مغلقٌ مُبصَّم** (٢٠٢٦-٠٩-٢٤): التزامُ مصدره وبصمةُ كلّ ملفٍّ في")
    add("`src/alghanem/PORT_MANIFEST.json`، **فالتباعدُ عن الأصل يُعلَن ولا**")
    add("**يقع صمتًا**. والتفصيلُ في `src/alghanem/TRANSFER_NOTICE.md`.")
    add("")
    add("## التشغيل")
    add("")
    add("```")
    add('python -m pip install -e ".[dev]"')
    add("bash tools/verify.sh")
    add("```")
    add("")
    add("**والمتونُ تُستقبَل من الشجرة المجاورة ببصمتها**:")
    add("")
    add("```")
    add("python tools/intake_corpus.py --source-root <جذرُ Saleh1967/Alghanem>")
    add("```")
    add("")
    add("والمستقبَلاتُ مسرودةٌ في `tools/intake_corpus.py` باسمها وطولها")
    add("وبصمتها، **ولا يُنقَل ما لم يُطابِق الاثنين معًا**.")
    add("")
    return "\n".join(out) + "\n"


def main() -> int:
    text = render()
    ROOT.write_text(text, encoding="utf-8")
    print(f"كُتِب {ROOT.relative_to(REPOSITORY)} — {len(text.splitlines())} سطرًا")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
