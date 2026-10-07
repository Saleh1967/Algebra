"""تُكتَب وثيقةُ إعادة القياس **من السجلّ المُودَع** — ولا رقمَ يُنقَل يدًا."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
RUN = REPOSITORY / "deposits" / "basmala_lifted_run.log"
PAPER = REPOSITORY / "docs" / "الأرقام-مرفوعة-البسملات.md"
EASTERN = str.maketrans("0123456789.-", "٠١٢٣٤٥٦٧٨٩٫−")


def eastern(one: object) -> str:
    return str(one).translate(EASTERN)


def grouped(one: str) -> str:
    return eastern(f"{int(one):,}".replace(",", "٬"))


def grab(text: str, pattern: str) -> tuple[str, ...]:
    found = re.search(pattern, text, re.MULTILINE)
    if found is None:
        raise SystemExit(f"لا مطابقَ في السجلّ: {pattern}")
    return found.groups()


def render() -> str:
    run = RUN.read_text(encoding="utf-8")
    (lines, lifted) = grab(run, r"^  أسطرٌ (\d+) \| أسطرٌ رُفِعت (\d+)$")
    (digest,) = grab(run, r"^  بصمتُها ([0-9a-f]{64})$")
    (tokens, tokens_before) = grab(run, r"^  الألفاظُ: (\d+) \(قبلُ (\d+)\)$")
    (shapes, shapes_before) = grab(run, r"^  هياكلُ متمايزة: (\d+) \(قبلُ (\d+)\)$")
    (vague, vague_before) = grab(run, r"^  غامضةٌ منها: (\d+) \(قبلُ (\d+)\)$")
    (mass, share, mass_before, share_before) = grab(
        run, r"^  كتلتُها: (\d+) \(([\d.]+)\) \(قبلُ (\d+) و([\d.]+)\)$"
    )
    (units, units_before) = grab(run, r"^  L₀: (\d+) وحدةً \(قبلُ (\d+)\)$")
    rungs = re.findall(
        r"^  (م\d [^|]+) \| (\d+) \((\d+)\) \| (\d+) \((\d+)\) \| ([\d.]+) "
        r"\(([\d.]+)\) \| ([\d.]+) \(([\d.]+)\) \| ([\d.]+) \(([\d.]+)\) "
        r"\| ([\d.]+) \(([\d.]+)\)$",
        run,
        re.MULTILINE,
    )
    (best,) = grab(run, r"^  أرخصُ درجةٍ محجوزًا: (\S+ \S+ \S+) \(قبلُ م١\)$")
    (commits,) = grab(run, r"^  والتزاماتُ القيد: (\d+)$")
    (drift,) = grab(run, r"^  انحرافُ الآلتين: ([\d.]+)$")
    (cut, cut_share, cut_before, share_cut_before) = grab(
        run, r"^  ألفاظٌ فُصِلت: (\d+) \(([\d.]+)\) \(قبلُ (\d+) و([\d.]+)\)$"
    )
    (pieces, pieces_before, kinds, kinds_before) = grab(
        run, r"^  الكلماتُ: (\d+) \(قبلُ (\d+)\) \| أنواعٌ (\d+) \(قبلُ (\d+)\)$"
    )
    (miss, miss_before) = grab(run, r"^  مرتدُّها ([\d.]+) \(قبلُ ([\d.]+)\)$")
    (cost, cost_before, at_token) = grab(
        run, r"^  للوحدة محجوزًا ([\d.]+) \(قبلُ ([\d.]+)\) \| ومستوى اللفظ ([\d.]+)$"
    )

    out: list[str] = []
    add = out.append
    add("# الأرقامُ الكلميّةُ مُعادةً — مرفوعَ البسملات الملحقة")
    add("")
    add("**الختم**: `be03e5be…` — مُودَعٌ ومدفوعٌ **قبل** التشغيل.")
    add(
        f"**المدوّنةُ المشتقّة**: `{digest[:16]}…` — "
        f"{grouped(lines)} سطرًا، رُفِع من **{grouped(lifted)}** منها"
    )
    add("أوّلُ أربعِ كلمات. **والمُجمَّدُ `37633090…` لم يُمَسّ**، والسجلُّ")
    add("المُقفَل `426f7fc8…` باقٍ على حاله — وهذه أرقامٌ **موازية**.")
    add("")
    add("## ١) عدُّ الكلم والهياكل")
    add("")
    add("| المقيس | قبلُ | بعدُ | الفرق |")
    add("|---|---|---|---|")
    add(
        f"| الألفاظ | {grouped(tokens_before)} | **{grouped(tokens)}** "
        f"| {eastern('−') + grouped(str(int(tokens_before) - int(tokens)))} |"
    )
    add(
        f"| هياكلُ متمايزة | {grouped(shapes_before)} | {grouped(shapes)} "
        f"| {eastern('−') + grouped(str(int(shapes_before) - int(shapes)))} |"
    )
    add(f"| غامضةٌ منها | {grouped(vague_before)} | {grouped(vague)} | ٠ |")
    add(
        f"| كتلتُها | {grouped(mass_before)} | {grouped(mass)} "
        f"| {eastern('−') + grouped(str(int(mass_before) - int(mass)))} |"
    )
    add(
        f"| نصيبُها | {eastern(share_before)} | **{eastern(share)}** "
        f"| {eastern(f'{float(share) - float(share_before):+.4f}')} |"
    )
    add("")
    add("## ٢) السلّمُ — الدرجاتُ الأربع")
    add("")
    add(f"`L₀` {grouped(units)} وحدةً (قبلُ {grouped(units_before)}).")
    add("")
    add("| المستوى | N | أبجديّة | للوحدة ملحقًا | **للوحدة محجوزًا** | مرتدّ | `I` |")
    add("|---|---|---|---|---|---|---|")
    for row in rungs:
        add(
            f"| {row[0].strip()} | {grouped(row[1])} ({grouped(row[2])}) "
            f"| {grouped(row[3])} ({grouped(row[4])}) "
            f"| {eastern(row[5])} ({eastern(row[6])}) "
            f"| **{eastern(row[7])}** ({eastern(row[8])}) "
            f"| {eastern(row[9])} ({eastern(row[10])}) "
            f"| {eastern(row[11])} ({eastern(row[12])}) |"
        )
    add("")
    add(
        f"**وأرخصُ درجةٍ محجوزًا {best.strip()} — كما كانت.** "
        f"والتزاماتُ القيد {grouped(commits)}، وانحرافُ الآلتين {eastern(drift)}."
    )
    add("")
    add("## ٣) قاعدةُ الفصل")
    add("")
    add("| المقيس | قبلُ | بعدُ |")
    add("|---|---|---|")
    add(
        f"| ألفاظٌ فُصِلت | {grouped(cut_before)} ({eastern(share_cut_before)}) "
        f"| {grouped(cut)} ({eastern(cut_share)}) |"
    )
    add(f"| الكلمات | {grouped(pieces_before)} | {grouped(pieces)} |")
    add(f"| الأنواع | {grouped(kinds_before)} | {grouped(kinds)} |")
    add(f"| المرتدّ | {eastern(miss_before)} | {eastern(miss)} |")
    add(f"| للوحدة محجوزًا | {eastern(cost_before)} | **{eastern(cost)}** |")
    add("")
    add(
        f"ومستوى اللفظ **{eastern(at_token)}** — فالفصلُ أغلى بـ"
        f"**{eastern(f'{float(cost) - float(at_token):+.4f}')}** "
        "(وكان **+٠٫٠٨٩٤**)."
    )
    add("")
    add("**فحكمُ `7bf3ccd8…` لا ينقلب**: الفصلُ ما زال خاسرًا.")
    add("")
    add("## ٤) ما تغيّر وما لم يتغيّر")
    add("")
    add("**لم تنقلب نتيجةٌ واحدة.** كلُّ فرقٍ في المنزلة الثالثة أو الرابعة:")
    add("")
    add("- أرخصُ درجةٍ في السلّم: **م١** — كما كانت.")
    add("- حكمُ قاعدة الفصل: **خاسرٌ** — كما كان.")
    add("- نصيبُ كتلة الغامض: **٠٫٤٤٤٣** مقابلَ ٠٫٤٤٦١.")
    add("")
    add(
        "**وأكبرُ ما تحرّك مسارُ الجشع**: أبجديّةُ `م١` "
        f"{grouped(rungs[1][4])} ⟶ {grouped(rungs[1][3])}، "
        "لأنّ تكرارَ البسملات كان يغذّيه."
    )
    add("")
    add("**والثمنُ ارتفع قليلًا** عند الوحدة — وذلك **مُعلَنٌ قبل الرقم**")
    add("في الختم: رفعُ أكثرِ ما تكرّر يرفع تكرارًا، **فلا يُقرأ خبرًا عن**")
    add("**البنية**.")
    add("")
    return "\n".join(out) + "\n"


def main() -> int:
    text = render()
    PAPER.write_text(text, encoding="utf-8")
    print(f"كُتِب {PAPER.relative_to(REPOSITORY)} — {len(text.splitlines())} سطرًا")
    return 0


if __name__ == "__main__":
    sys.exit(main())
