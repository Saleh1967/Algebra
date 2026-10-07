"""تُكتَب وثيقةُ الأنبوب الخارجيّ **من السجلّ المُقفَل** — لا من نثر.

ولا يُكتَب رقمٌ لا يُقابِله حقلٌ في `tools/foreign_ledger_seal.py`، وكلُّ
حقلٍ منه مفحوصٌ بإعادة اشتقاقه ومقابَلٌ بالملفّات المُودَعة.
"""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[1]
SEAL = REPOSITORY / "tools" / "foreign_ledger_seal.py"
PAPER = REPOSITORY / "docs" / "سجلٌّ-من-أنبوبٍ-آخر.md"
EASTERN = str.maketrans("0123456789.", "٠١٢٣٤٥٦٧٨٩٫")

THIS_TREE_WORDS = 78_245
THIS_TREE_LINES = 6_236


def eastern(one: object) -> str:
    return str(one).translate(EASTERN)


def grouped(one: int) -> str:
    return eastern(f"{one:,}".replace(",", "٬"))


def _seal() -> Any:
    spec = importlib.util.spec_from_file_location("foreign_ledger_seal", SEAL)
    if spec is None or spec.loader is None:
        raise SystemExit("لا قارئَ لسجلّ الأنبوب الخارجيّ")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def render() -> str:
    tool = _seal()
    r = tool.FROZEN_FOREIGN
    complaints = tool.verify_against_logs()
    if complaints:
        raise SystemExit(f"لا تُكتَب وثيقةٌ على سجلٍّ مخالف: {complaints}")

    out: list[str] = []
    add = out.append
    add("# سجلٌّ من أنبوبٍ آخر — ما أُعيد اشتقاقُه، وما حُدَّ، وما بقي دَينًا")
    add("")
    add(f"**ختمُ السجلّ**: `{tool.RECORD_DIGEST[:8]}…` — مُشتَقٌّ من حقوله.")
    add("")
    add("**هذا تشغيلٌ لم تُجرِه هذه الشجرة.** أُودِعت ملفّاتُه الأربعةُ")
    add("**بايتةً بايتة**، ولم يُمَسّ فيها حرف. **ولا أوقّع تأويلَه**:")
    add("لا أنّ وسومَ QAC تكشف دلالةً أصوليّة، ولا أنّ بنودَ الكتاب ثمانية،")
    add("ولا أنّ الأساليبَ ثمانية. **والتسجيلان المُودَعان ينفيان ذلك عن**")
    add("**نفسيهما بنصّهما**، ويُنقَل نفيُهما كما هو.")
    add("")
    add("**وما فعلتُه**: أعدتُ اشتقاقَ **كلِّ رقمٍ يسمح المنشورُ بإعادة**")
    add("**اشتقاقه** من الأعداد المطبوعة نفسِها. وما لا يسمح **حُدَّ بحدّين**.")
    add("")
    add("## المقامُ غيرُ مقام هذه الشجرة — ويُقال أوّلًا")
    add("")
    add("| | هذه الشجرة | الأنبوبُ المُودَع |")
    add("|---|---|---|")
    add(f"| الكلمات | **{grouped(THIS_TREE_WORDS)}** | **{grouped(r.stand_words)}** |")
    here, there = grouped(THIS_TREE_LINES), grouped(r.stand_verses)
    add(f"| الأسطر/الآيات | **{here}** | **{there}** |")
    add("")
    add("**فلا يُنقَل رقمٌ من أحدهما إلى الآخر بلا تحويل**، والفرقُ **يُسمّى**")
    add("**ولا يُخمَّن**: فضُّه يحتاج حدَّ اللفظِ وحدَّ الآيةِ هناك، وليسا مُودَعين.")
    add("")
    add("## ما أُعيد اشتقاقُه فطابق")
    add("")
    add("| الحقل | المطبوع | المُشتَقُّ ههنا |")
    add("|---|---|---|")
    for index, name in enumerate(r.bunud_names):
        mine = tool.bit_entropy(r.bunud_counts[index] / r.stand_words)
        shown = eastern(r.bunud_entropies[index])
        add(
            f"| H(بتّ {name}) من عدده {grouped(r.bunud_counts[index])} "
            f"| {shown} | {eastern(f'{mine:.4f}')} |"
        )
    shares = r.asalib_shares()
    walked = math.fsum(one * two for one, two in zip(shares, r.asalib_code_lengths))
    linear = math.fsum(one * (index + 1) for index, one in enumerate(shares))
    booked = math.fsum(one * two for one, two in zip(shares, r.asalib_book_ranks))
    mine_h = tool.entropy(shares)
    add(
        f"| H(الأسلوب) من الأعداد | {eastern(r.asalib_entropy)} "
        f"| {eastern(f'{mine_h:.4f}')} |"
    )
    add(
        f"| عمقُ هافمان | {eastern(r.asalib_huffman)} " f"| {eastern(f'{walked:.4f}')} |"
    )
    add(
        f"| عمقُ الترتيب التكراريّ | {eastern(r.asalib_by_frequency)} "
        f"| {eastern(f'{linear:.4f}')} |"
    )
    add(
        f"| عمقُ ترتيب الكتاب | {eastern(r.asalib_by_book)} "
        f"| {eastern(f'{booked:.4f}')} |"
    )
    add("")
    add("**وحدُّ شانون محفوظٌ في الموضعين**: `H ≤ هافمان < H + 1`.")
    add("**ومجموعُ كرافت لشجرة الأساليب واحدٌ تامٌّ** — فالشجرةُ مستنفِدة.")
    add("**ورموزُ البنود سليمةُ البادئة**، ومجموعُ كرافت للمنشور منها دون")
    add("الواحد **لأنّ المنشورَ ستٌّ من أربعَ عشرة**، والبقيّةُ لها فسحتُها.")
    add("")
    add("## وما لا يُعاد اشتقاقُه — فيُحَدُّ بحدّين")
    add("")
    low, high = r.vector_bounds()
    hidden = r.vector_cells - len(r.vector_shown)
    left = r.stand_words - sum(r.vector_shown)
    add(f"جردُ المتّجه يُنشَر **{eastern(len(r.vector_shown))}** خاناتٍ من")
    add(f"**{eastern(r.vector_cells)}** مشغولة، فتبقى **{grouped(left)}** كلمةً")
    add(f"في **{eastern(hidden)}** خاناتٍ لا تُعرَف أنصبتُها. **فلا تُعاد**")
    add("**`H(المتّجه)` حسابًا تامًّا**، وإنّما يُشتَقُّ لها حدّان من المنشور:")
    add("")
    add(f"- **الأعلى** (البقيّةُ موزّعةٌ بالسواء): **{eastern(f'{high:.4f}')}**")
    add(
        f"- **الأدنى** (مكدَّسةٌ ما استطاعت دون أصغرِ منشورة): "
        f"**{eastern(f'{low:.4f}')}**"
    )
    add(f"- **والمطبوع**: **{eastern(r.vector_entropy)}** — **داخلَ الحدّين**.")
    add("")
    add("**وهذا ليس تصديقًا ولا تكذيبًا**: هو **كلُّ ما يسمح به المنشور**.")
    add("")
    add("## فرقُ المنزلة الأخيرة — ترتيبُ تقريبٍ لا خلافُ حساب")
    add("")
    exact = math.fsum(tool.bit_entropy(one / r.stand_words) for one in r.bunud_counts)
    printed = math.fsum(float(one) for one in r.bunud_entropies)
    gains = math.fsum(float(one) for one in r.bunud_gains)
    add(f"مجموعُ الإنتروبيات **قبل** التقريب **{eastern(f'{exact:.6f}')}**،")
    add(f"فيُطبَع **{eastern(f'{round(exact, 4):.4f}')}**؛ ومجموعُ المنشور")
    add(f"بأربع منازلَ **{eastern(f'{printed:.4f}')}**. **وكلاهما صحيح**،")
    add("والفرقُ **وحدةٌ في المنزلة الرابعة**. وكذلك مجموعُ الكسب: المنشورُ")
    add(f"**{eastern(r.vector_gain)}** للمتّجه، ومجموعُ أرقام البتّات")
    add(f"**{eastern(f'{gains:.4f}')}**. **ويُبَيَّن ولا يُطوى.**")
    add("")
    add("## الدُّيونُ — مُسمّاةٌ بأرقامها")
    add("")
    for name, why in r.debts:
        add(f"- **{name}** — {why}.")
    add("")
    add("## ما لا يُدَّعى بهذا السجلّ")
    add("")
    add("**أنّ الأرقامَ صحيحةٌ لا يعني أنّ القياسَ صحيح.** المُعاد ههنا")
    add("**حسابُ الأنبوب على أعداده**، لا **أعدادُه على المصحف**: تلك")
    add("تحتاج مدوّنتَه ووسومَه، **وليسا مُودَعين**. فما طابق ههنا **طابق**")
    add("**حسابًا**، ولا يُقال إنّه طابق قياسًا.")
    add("")
    return "\n".join(out) + "\n"


def main() -> int:
    PAPER.write_text(render(), encoding="utf-8")
    print(f"كُتِب {PAPER.relative_to(REPOSITORY)} — {len(render().splitlines())} سطرًا")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
