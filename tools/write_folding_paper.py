"""تُكتَب وثيقةُ الطيّ **من الوحدة والشاهد** — لا رقمَ يُطبَع بيد."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Final

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[1]
DOCS: Final[Path] = REPOSITORY / "docs"
PAPER: Final[Path] = DOCS / "الطيُّ-والفكّ.md"
WITNESS: Final[Path] = REPOSITORY / "deposits" / "folding_proof_witness.log"
ASCENT: Final[Path] = REPOSITORY / "deposits" / "folding_ascent_witness.log"
MODULE: Final[Path] = REPOSITORY / "src" / "algebra" / "folding.py"
GUARD: Final[Path] = REPOSITORY / "tests" / "algebra" / "test_folding.py"
EASTERN: Final[dict[int, int]] = str.maketrans("0123456789.", "٠١٢٣٤٥٦٧٨٩٫")


def eastern(one: object) -> str:
    return str(one).translate(EASTERN)


def grouped(one: int) -> str:
    return eastern(f"{one:,}".replace(",", "٬"))


def _folding() -> Any:
    sys.path.insert(0, str(REPOSITORY / "src"))
    from algebra import folding

    return folding


def grab(pattern: str, where: Path = WITNESS) -> str:
    text = where.read_text(encoding="utf-8")
    found = re.search(pattern, text, re.M)
    if found is None:
        raise SystemExit(f"لا شاهدَ في {where.name} لـ{pattern}")
    return found.group(1)


def rose(pattern: str) -> str:
    return grab(pattern, ASCENT)


def render() -> str:
    folding = _folding()
    places = int(grab(r"الحالات: (\d+) \|"))
    alphabet = int(grab(r"الأبجديّة: (\d+)$"))
    blocked = int(grab(r"محجورةٌ \(لا انتقالَ بين أيّ اثنين منها\): (\d+)"))
    free = int(grab(r"وحرّةٌ: (\d+)"))
    folded = int(grab(r"أسطرٌ طُوِيت: (\d+) \|"))
    recovered = int(grab(r"واسترجعت تامّةً: (\d+)"))
    longest = int(grab(r"وأطولُ سطرٍ: (\d+) حالة"))
    biggest = int(grab(r"وأكبرُ دليلٍ: (\d+) بتّة"))
    with_guard = int(grab(r"بالحارس: (\d+) بتّة"))
    without = int(grab(r"بلا حارس: (\d+) بتّة"))
    saved = int(grab(r"فوفَّر الحارسُ: (\d+) بتّة"))
    per_state = grab(r"وللحالة الواحدة: ([\d.]+) بتّة")
    root = grab(r"وجذرُها الأكبر ρ = ([\d.]+)")
    rate = grab(r"log₂ ρ = ([\d.]+)")
    named = grab(r"والمحجورةُ بعينها: (.+)$")
    shape = folding.Guarded(free=3, blocked=1)
    counts = [folding.admissible_count(shape, one) for one in range(6)]
    checks = len(re.findall(r"^def test_", GUARD.read_text(encoding="utf-8"), re.M))

    out: list[str] = []
    add = out.append
    add("# الطيُّ والفكّ — برهانٌ يُطوى ويُفَكّ، لا إنتروبيا")
    add("")
    add("**هذا الملفُّ مُشتَقٌّ** من `src/algebra/folding.py` ومن")
    add("`deposits/folding_proof_witness.log`، **فلا رقمَ فيه يُطبَع بيد**.")
    add("")
    add("## المأخذُ الذي وَلَد هذا العمل")
    add("")
    add("كلُّ ما قِيس في هذه الشجرة قبلَه **إنتروبيا وثمنٌ محجوز**، ولا")
    add("يُستَرجَع من واحدٍ منها **سطرٌ واحد**. فـ`H = 2.6283` عددٌ **لا**")
    add("**يُطوى به شيءٌ ولا يُفَكّ** — وذلك قياسٌ، **وليس برهانًا**.")
    add("")
    add("**والفرقُ حاسم**: المقياسُ يقول «كم»، والبرهانُ يقول «كيف»، **وما**")
    add("**يُفَكّ يُثبِت نفسَه**. فوثيقةٌ تُدَّعى فيها بنيةٌ ولا تُستَرجَع منها")
    add("المادّةُ **دعوًى على المادّة لا وصفٌ لها**.")
    add("")
    add("## المبرهناتُ الثلاث")
    add("")
    add("أبجديّةٌ `Σ = F ⊎ B` فيها `f` حرًّا و`b` محجورًا، **ولا محجوران**")
    add("**متجاوران**.")
    add("")
    add("**١) العدّ**: `T(n) = f·T(n−1) + f·b·T(n−2)` مع `T(0) = 1` و")
    add("`T(1) = f + b`. **وبرهانُه** بالتعويض من `A(n) = f·(A+B)(n−1)`")
    add("و`B(n) = b·A(n−1)`، إذ `A(n−1) = f·T(n−2)`.")
    add("")
    add("**٢) المعدّل**: جذرُ `x² = f·x + f·b` الأكبرُ")
    add("`ρ = (f + √(f² + 4fb)) / 2`، و`T(n)/T(n−1) → ρ`.")
    add("")
    add("**٣) التقابل** — وهو المقصود: `fold` **رتيبٌ** من الجائزات الطولِ `n`")
    add("**على** `{0, …, T(n)−1}`. **وبرهانُه** بالاستقراء: الرموزُ الجائزةُ")
    add("تقسم الجائزاتِ أقسامًا متباينةً حجمُ قسمِ `c` هو `S(n−1, بعدَ c)`،")
    add("**ومجموعُها `T(n)` بالتعريف**؛ والأقسامُ مرتّبةٌ، وبقيّةُ كلّ قسمٍ")
    add("تقابلٌ بفرض الاستقراء. **فيلزم أنّ `unfold` معكوسُه الوحيد.**")
    add("")
    add("**وعند `f = 3` و`b = 1`** — وهو حارسُ «لا محجورَ بعد محجور» في أضيق")
    add("صورةٍ — تكون المتتاليةُ `x² = 3x + 3` وجذرُها `(3 + √21)/2`، وأوّلُ")
    add(f"الأعداد: {' · '.join(grouped(one) for one in counts)}.")
    add("")
    add("## والاستيفاءُ على كلّ الجائزات — لا على عيّنة")
    add("")
    add(f"`tests/algebra/test_folding.py` — **{eastern(checks)}** فحصًا على خمس")
    add("أبجديّات. تُعَدّ **كلُّ** كلمةٍ جائزةٍ حتّى الطول السادس، ويُفحَص:")
    add("")
    add("- أنّ الأدلّةَ **هي `{0,…,T(n)−1}` بلا تكرارٍ ولا فجوة**،")
    add("- وأنّ `unfold(fold(w)) = w` **لكلّ** واحدةٍ منها،")
    add("- وأنّ `fold(unfold(k)) = k` **لكلّ** `k < T(n)`،")
    add("- وأنّ `T(n)` المُشتَقَّ يطابق **عَدًّا مباشرًا** للكلمات.")
    add("")
    add("**ولا عائمَ في الطيّ**: أعدادٌ صحيحةٌ تامّة. وبلوغُ `ρ` يُفحَص")
    add("بـ`ratio_gap` **بكسورٍ صحيحةٍ** تنزل رتيبًا. **وبلا حارسٍ الفجوةُ**")
    add("**صفرٌ تامٌّ من أوّل خطوة** (`T(n) = fⁿ`) — فرقٌ يُقال ولا يُطوى.")
    add("")
    add("## والمجمَّدُ طُوِي وفُكَّ")
    add("")
    add(f"**{grouped(folded)}** سطرًا طُوِيت إلى أعدادٍ صحيحةٍ ثمّ فُكَّت،")
    add(f"**واسترجعت {grouped(recovered)} تامّةً حالةً بحالة** — وإلّا سقط")
    add("التشغيل. ولا مخالفة.")
    add("")
    add("**والحارسُ مكتشَفٌ لا مفترَض**: بُحِثت **كلُّ** طوائف الأبجديّة")
    add(f"الـ{grouped(alphabet)} (**{grouped(2 ** alphabet)}** طائفةً) عن أكبرِ")
    add("طائفةٍ لا انتقالَ بين أيّ اثنين منها داخلَ السطر، **فكانت**")
    add(f"**{grouped(blocked)}**: `{named}`. **فلا واحدةٌ منها تلي واحدةً**")
    add(f"**منها ألبتّة في {grouped(places)} حالة.**")
    add("")
    add(f"فـ`f = {eastern(free)}` و`b = {eastern(blocked)}`، والمتتالية")
    add(f"`x² = {eastern(free)}x + {eastern(free * blocked)}`، و`ρ = {eastern(root)}`،")
    add(f"و`log₂ ρ = {eastern(rate)}`.")
    add("")
    add("| المقدار | العدد |")
    add("|---|---:|")
    add(f"| بالحارس، `⌈log₂ T(n)⌉` مجموعةً | **{grouped(with_guard)}** بتّة |")
    add(f"| بلا حارس | {grouped(without)} بتّة |")
    add(f"| **وفَّر الحارسُ** | **{grouped(saved)}** بتّة |")
    add(f"| للحالة الواحدة | {eastern(per_state)} بتّة |")
    add(f"| أطولُ سطرٍ | {grouped(longest)} حالة |")
    add(f"| أكبرُ دليلٍ | {grouped(biggest)} بتّة |")
    add("")
    add("## والفرقُ عن الإنتروبيا — جنسٌ لا مقدار")
    add("")
    add(f"**{eastern(per_state)} بتّة للحالة أغلى** من كلّ ثمنٍ محجوزٍ قِيس في")
    add("هذه الشجرة. **وذلك ليس عيبًا**:")
    add("")
    add("- **الإنتروبيا** حدٌّ أدنى **لمتوسّطِ** شفرةٍ **احتماليّة**، تحتاج")
    add("  **نموذجًا** وقسمةً محجوزةً وتنعيمًا — **وتُقدَّر ولا تُكتَب**.")
    add("- **وهذا** طولُ شفرةٍ **قائمةٍ بعينها**: لا نموذجَ لها ولا تدريبَ")
    add("  ولا قسمة، **وتُكتَب وتُقرَأ**.")
    add("")
    add("**فالأولى تُقاس والثانيةُ تُبرهَن**، ولا يُطرَح أحدُهما من الآخر.")
    add("")
    add("## والصعودُ: اللفظُ والسطرُ بالتقابل نفسِه")
    add("")
    add("**وعطلٌ في التشغيل الأوّل يُقال** (العطل ٣٢): كان يفكُّ بـ")
    add("`unfold(shape, index, len(word))` — **فالطولُ مُمرَّرٌ من خارج**،")
    add("والاسترجاعُ **بدليلٍ وطولٍ** لا بدليلٍ وحدَه.")
    add("")
    add("**والمبرهنة ٤ تُزيله**: `foldany(w) = off(|w|) + fold(w)` **تقابلٌ**")
    add("**على `ℕ` كلِّها**، فالطولُ يُقرَأ من العدد نفسِه. **والمبرهنة ٥**")
    add("**تُركّب**: كلُّ لفظٍ عددٌ، فمتتاليةُ الألفاظ كلمةٌ على أبجديّةٍ")
    add("سعتُها `A(L)` بلا حارس، فتُطوى بالتقابل نفسِه.")
    add("")
    words = int(rose(r"ألفاظٌ طُوِيت واسترجعت تامّةً: (\d+) من"))
    longest_word = int(rose(r"أطولُ لفظٍ: (\d+) حالة"))
    radix = int(rose(r"فسعةُ أبجديّةِ الألفاظ A\(L\) = (\d+)"))
    width = int(rose(r"وعرضُها: (\d+) بتّة"))
    rows = int(rose(r"أسطرٌ طُوِيت واسترجعت تامّةً \*\*إلى الحالات\*\*: (\d+)"))
    per_line = int(rose(r"أطولُ سطرٍ: (\d+) لفظًا"))
    fixed = int(rose(r"بتّة × \d+: (\d+) بتّة"))
    above = int(rose(r"والسطرُ عددًا واحدًا فوق الألفاظ: (\d+) بتّة"))
    straight = int(rose(r"على الحالات مباشرةً: (\d+) بتّة"))
    boundary = int(rose(r"= (\d+) بتّة$"))
    each = rose(r"وللفظِ الواحد: ([\d.]+) بتّة")
    add(f"**فطُوِيت {grouped(words)} لفظًا واسترجعت تامّةً**، وأطولُها")
    add(f"{grouped(longest_word)} حالة، فسعةُ أبجديّةِ الألفاظ")
    add(f"`A(L) = {grouped(radix)}` وعرضُها **{grouped(width)}** بتّة.")
    add("")
    add(f"**وطُوِيت {grouped(rows)} سطرًا عددًا واحدًا لكلٍّ، واسترجعت**")
    add("**تامّةً إلى الحالات** — يُفَكّ السطرُ فيرجع ألفاظًا ثمّ حالاتٍ،")
    add(f"وأطولُ سطرٍ {grouped(per_line)} لفظًا.")
    add("")
    add("| ما يُكتَب فعلًا | بتّات |")
    add("|---|---:|")
    add(f"| اللفظُ بعرضٍ ثابتٍ {grouped(width)} بتّة | {grouped(fixed)} |")
    add(f"| السطرُ عددًا واحدًا **فوق الألفاظ** | {grouped(above)} |")
    add(f"| السطرُ عددًا واحدًا **على الحالات مباشرةً** | **{grouped(straight)}** |")
    add("")
    add(f"**فثمنُ حملِ حدودِ الألفاظ {grouped(boundary)} بتّة** —")
    add(f"**{eastern(each)} بتّة للفظ الواحد**. **فالتقطيعُ يزيد ما يُكتَب**")
    add("**ولا يُنقِصه**، والزيادةُ هي الحدودُ نفسُها. **وذلك عددٌ لا وصف.**")
    add("")
    add("**وقيدٌ يُقال**: `bit_length` عددٍ واحدٍ طولُه بالضبط، **ومجموعُ**")
    add("**أطوالِ أعدادٍ كثيرةٍ ليس طولَ شفرةٍ لمجراها** — لا يُفَكّ تلاصقُها")
    add("بلا فاصلٍ أو عرضٍ ثابت. فما يُسمّى شفرةً أعلاه **العرضُ الثابتُ أو**")
    add("**العددُ الواحد**.")
    add("")
    add("## ما لا يُدَّعى")
    add("")
    add("- **لا يُسمّى المحجورُ سكونًا ولا الحرُّ حركةً** — صنفان")
    add("  **بالانتقالات المشهودة**، ويقول ذلك باقُ الوحدة بنصّه.")
    add(f"- **وأنّ الـ{grouped(blocked)} تنوينٌ قراءةٌ لا قياس**: المقيسُ أنّ")
    add("  انتقالَها **صفر**، وتسميتُها فوق البايتات.")
    add("- **والمبرهنةُ عامّةٌ، وتطبيقُها على هذا المجمَّد واقعةٌ واحدة.**")
    add("- **ولا يقول الطيُّ إنّ البنيةَ مفهومة** — يقول إنّها **مُستَرجَعة**.")
    add("")
    return "\n".join(out) + "\n"


def main() -> int:
    text = render()
    PAPER.write_text(text, encoding="utf-8")
    print(f"كُتِب {PAPER.relative_to(REPOSITORY)} — {len(text.splitlines())} سطرًا")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
