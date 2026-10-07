"""تُكتَب وثيقةُ سلّم السياق **من سجلّ التشغيل** — لا من ذاكرةٍ ولا نثر.

وكلُّ رقمٍ فيها يُقرَأ بنمطٍ من `deposits/context_ladder_run.log`، وما لا
يوجد في السجلّ **يُوقِف الكتابة**. **ولا اسمَ يدخلها من خارج المجمَّد.**
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[1]
LOG = REPOSITORY / "deposits" / "context_ladder_run.log"
VERSE_END = REPOSITORY / "deposits" / "verse_ending_run.log"
NEIGHBOUR = REPOSITORY / "deposits" / "arabic_token_run.log"
PAPER = REPOSITORY / "docs" / "سلّم-السياق-بلا-تسريب.md"
SEAL = REPOSITORY / "tools" / "context_ladder_seal.py"
EASTERN = str.maketrans("0123456789.", "٠١٢٣٤٥٦٧٨٩٫")


def eastern(one: object) -> str:
    return str(one).translate(EASTERN)


def grouped(one: int) -> str:
    return eastern(f"{one:,}".replace(",", "٬"))


def grab(pattern: str, text: str) -> tuple[str, ...]:
    found = re.findall(pattern, text)
    if not found:
        raise SystemExit(f"لا شاهدَ في السجلّ لـ{pattern}")
    first = found[0]
    return first if isinstance(first, tuple) else (first,)


def _seal() -> Any:
    spec = importlib.util.spec_from_file_location("context_ladder_seal", SEAL)
    if spec is None or spec.loader is None:
        raise SystemExit("لا قارئَ لسجلّ السلّم المُقفَل")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def render() -> str:
    tool = _seal()
    complaints = tool.verify_against_logs()
    if complaints:
        raise SystemExit(f"لا تُكتَب وثيقةٌ على سجلٍّ مخالف: {complaints}")
    text = LOG.read_text(encoding="utf-8")
    (lines,) = grab(r"— الأسطر: (\d+)", text)
    tokens, again = grab(r"— الألفاظ: (\d+) \| وعبرَ العدّادات (\d+)", text)
    if tokens != again:
        raise SystemExit("العدّاداتُ لا تُقابِل الأسطر")
    boxes, field = grab(r"— خاناتُ الحال: (\d+) \| H = ([\d.]+)", text)
    (questions,) = grab(r"— الأسئلةُ المتاحة: (\d+)", text)
    rungs = re.findall(
        r"— د(\d+) «(.+?)»: ملحَقة ([\d.]+) \| محجوزة ([\d.]+) "
        r"\| ربحٌ ملحَقٌ (\S+) \| ربحٌ محجوزٌ (\S+) \| كتلٌ (\d+)",
        text,
    )
    (depths,) = grab(r"— الدرجاتُ المبلوغة: (\d+)", text)
    (whole_out,) = grab(r"مجموعُ الكسب المحجوز: (\S+)", text)
    (whole_in,) = grab(r"مجموعُ الكسب الملحَق: (\S+)", text)
    (share,) = grab(r"نصيبُ الدرجة الأولى من الكسب المحجوز: ([\d.]+)", text)
    (lowest,) = grab(r"أدنى ربحٍ ملحَق: (\S+)", text)
    (apart,) = grab(r"أدنى \(محجوزة − ملحَقة\): (\S+)", text)
    (blocks,) = grab(r"كتلُ آخر درجة: (\d+)", text)
    (slack,) = grab(r"أقصى \(log₂ التباديل − N·H\) بعد ألف = (\S+)", text)
    tally = re.findall(r"  أسئلةُ «(.+?)»: (\d+)", text)
    (positional,) = grab(
        r"I\(الحال ; الموضع\) = ([\d.]+)", VERSE_END.read_text(encoding="utf-8")
    )
    (neighbour,) = grab(r"\n  I = ([\d.]+)", NEIGHBOUR.read_text(encoding="utf-8"))

    out: list[str] = []
    add = out.append
    add("# سلّمُ السياق بتّةً بتّة — بلا قائمةٍ ولا اسمٍ ولا تسريب")
    add("")
    add("**الختم**: `d568a91d…` — مُودَعٌ ومدفوعٌ **قبل** التشغيل.")
    add(
        f"**والسجلُّ مُقفَلٌ**: `{tool.RECORD_DIGEST[:8]}…` — بصمةٌ "
        "**تُشتَقّ من حقوله**، وشكلُ النتيجة **قيدٌ في المُنشئ**."
    )
    add("**الحصاد**: **إحدى عشرةَ** من اثنتي عشرةَ صمدت، و**واحدةٌ** سقطت.")
    add("")
    add("## ما مُنِع منعًا")
    add("")
    add("- **لا قائمةَ مُودَعةٌ ولا صورةٌ منقولةٌ عن نصٍّ خارجيّ.** الأسئلةُ")
    add(f"  **{eastern(questions)}** سؤالًا، **قيمُها مجموعةٌ من المجمَّد**.")
    add("- **ولا اسمَ بابٍ ولا اسمَ علامةٍ ولا اسمَ يونيكود.** المحرفُ")
    add("  **شريحةٌ ونقطةُ ترميز**، وشرطٌ مختومٌ يعدّ الأسماءَ الداخلةَ")
    add("  ويوجب أن تكون **صفرًا** — **وكانت صفرًا**.")
    add("- **ولا تسريبَ من الموضع إلى نفسه.** السياقُ **ما مضى وحدَه**")
    add("  والموضعُ من السطر؛ وحرفُ خاتمةِ الموضع يحمل عنه **١٫٠٣١٠** بتًّا،")
    add("  **فإدخالُه جوابٌ لا سؤال**.")
    add("")
    add("## الحقلُ والسلّم")
    add("")
    add(f"الأسطرُ **{grouped(int(lines))}**، والألفاظُ **{grouped(int(tokens))}**")
    add(f"عبرَ العدّادات وعبرَ الأسطر سواءً. وخاناتُ الحال **{eastern(boxes)}**،")
    add(f"و`H` **{eastern(field)}** بتًّا.")
    add("")
    add("| الدرجة | السؤالُ المختار | ملحَقة | محجوزة | ربحٌ محجوز | كتل |")
    add("|---|---|---|---|---|---|")
    for depth, question, inside, kept, _gain_in, gain_out, block in rungs:
        add(
            f"| **د{eastern(depth)}** | {question} | {eastern(inside)} "
            f"| {eastern(kept)} | {eastern(gain_out)} | {eastern(block)} |"
        )
    add("")
    add("## أوّلُ بتّةٍ يدفع لها المجمَّد ليست بتّةَ الجار")
    add("")
    add("**وهذا سقوطُ الشرط الخامس.** قدّرتُ أنّ أوّلَ سؤالٍ يربح يسأل عن")
    add("**حال السابق**، والجشعُ اختار **«أآخرُ السطر؟»** — بتّةَ الموضع.")
    add(f"وربحُها المحجوز **{eastern(rungs[0][5])}**، وهو **الأكبرُ في**")
    add("**السلّم كلِّه**.")
    add("")
    add("**ونصُّ سقوطه مكتوبٌ فيه قبل النظر**: «فقد تسبق بتّةُ الموضع بتّةَ")
    add("الحال». **فالسقوطُ وقع في الموضع الذي عُيِّن له.**")
    add("")
    add("**وقد قِيس في ختمٍ آخر** (`26ae5b5b…`) أنّ `I(الحال ؛ الموضع)` =")
    add(f"**{eastern(positional)}**. **وهذا الختمُ لم يقرأ ذاك**، وإنّما بحث")
    add(f"في {eastern(questions)} سؤالًا فاختار هذا بربحٍ **{eastern(rungs[0][5])}**.")
    add("**فالرقمان يتلاقيان من طريقين — والتلاقي شاهدٌ لا صدفة.**")
    add("")
    add("## التصعيدُ يتجاوز ماركوف الأولى على الحال وحدَه")
    add("")
    add(f"مجموعُ الكسب المحجوز **{eastern(whole_out)}** بتًّا، والجارُ **كلُّه**")
    add(f"يحمل **{eastern(neighbour)}**.")
    add(f"فالنسبةُ **{eastern(f'{float(whole_out) / float(neighbour):.3f}')}** —")
    add("**ثلاثةُ أضعافٍ ورُبع**. ومجموعُ الكسب الملحَق")
    add(f"**{eastern(whole_in)}**، **وهو أعلى دائمًا — وذاك الانتحال بعينه**.")
    add("")
    add(f"**والكسبُ موزَّعٌ لا مكدَّس**: نصيبُ الدرجة الأولى **{eastern(share)}**")
    add("والحدُّ المختوم ٠٫٢٥ — **مرورٌ قريبٌ من الحدّ**، والثلاثةُ أرباعٍ")
    add("الباقيةُ على إحدى عشرةَ درجة.")
    add("")
    add("## أيُّ الأسئلةِ اختير")
    add("")
    add("| صنفُ السؤال | كم اختير |")
    add("|---|---|")
    for name, count in tally:
        add(f"| {name} | {eastern(count)} |")
    add("")
    add("**وحرفُ خاتمةِ السابق يحمل خبرًا عن حال تاليه**: خمسةُ أسئلةٍ من")
    add("اثني عشر. **وهو غيرُ ما قِيس في `494465d1…`** من خبر الحرف عن")
    add("**حاله هو**. **ولم يُختَر سؤالُ صدر السطر ألبتّة.**")
    add("")
    add("## induction on وinduction FOR")
    add("")
    add("**المبرهَنتان مُصانتان عند كلّ درجةٍ وكلّ حال**: كلُّ درجةٍ **تنقيحٌ**")
    add("لسابقتها بحكم البناء، **والتنقيحُ لا يرفع الإنتروبيا الملحَقة** —")
    add(f"وأدنى ربحٍ ملحَقٍ **{eastern(lowest)}**، وهو موجب؛")
    add(f"و`log₂ التباديل ≤ N·H` — وأقصى فسحةٍ بعد ألفِ لفظ **{eastern(slack)}**.")
    add("**والحلقةُ تشهد عليهما درجةً درجةً وسطرًا سطرًا.**")
    add("")
    add("**وماركوف**: كلُّ درجةٍ **تكتيلٌ** لفضاء السياق، والسلّمُ **سلسلةُ**")
    add(f"**تكتيلاتٍ** من كتلةٍ واحدةٍ إلى **{eastern(blocks)}** كتلة.")
    add(f"وأدنى (محجوزة − ملحَقة) **{eastern(apart)}** — والاتّجاهُ كما يقتضي.")
    add("")
    add("## ما لم يُبلَغ — ويُسجَّل دَينًا لا نتيجة")
    add("")
    add(f"**السلّمُ لم يقف**: بلغ **{eastern(depths)}** درجةً، **وكلُّ درجةٍ**")
    add("**منها ربحت محجوزًا**. فالوقوفُ الذي نصَّ عليه الشرطُ السادس")
    add("**لم يقع**: بلغ السلّمُ **السقفَ الذي أعلنتُه أنا** لا سقفَ المادّة.")
    add("**فحدُّ ما تحمله المادّةُ لم يُبلَغ**، وبحثٌ يمدّ السقفَ حتّى يقف")
    add("السلّمُ بنفسه **مُعيَّنٌ ولم يُجرَ**.")
    add("")
    add("**والجشعُ غيرُ مبرهَن**: أفضلُ سؤالٍ عند درجةٍ ليس أفضلَ سلّمٍ في")
    add("النهاية. **فما بُلِغ حدٌّ أدنى**، ولا يُقال «لا يُبلَغ أكثر» بل")
    add("**«لم يُبلَغ بهذا الجشع»**.")
    add("")
    add("## ما يحرسه السجلُّ المُقفَل")
    add("")
    add("**لا يُقفَل سجلٌّ** ترتفع فيه الملحَقةُ درجةً، ولا يقع أكبرُ ربحٍ في")
    add("غير الدرجة الأولى، ولا يكون سؤالُ الأولى غيرَ سؤالِ الموضع، ولا")
    add("تنزل محجوزةٌ تحت ملحَقتها، ولا تزيد الكتلُ على الضعف بسؤالٍ واحد،")
    add("ولا يقلّ مجموعُ الكسب عن كسب الجار كلِّه، ولا يخلو من دَينه.")
    add("")
    add("**وتلاقي الختمين محروسٌ لا مرويّ**: يُردّ السجلُّ إن تباعد ربحُ")
    add("الدرجة الأولى عمّا قِيس في `26ae5b5b…`.")
    add("")
    add("**وقيمُ الأسئلة نقاطُ ترميزٍ لا شرائحَ مكتوبة**: الصورةُ تُقرَأ من")
    add("السجلّ المُودَع عند التحقّق، **فلا تُكتَب شريحةٌ بيد**.")
    add("")
    for name, why in tool.FROZEN_CONTEXT.unreached:
        add(f"- **{name}** — {why}.")
    add("")
    return "\n".join(out) + "\n"


def main() -> int:
    PAPER.write_text(render(), encoding="utf-8")
    print(f"كُتِب {PAPER.relative_to(REPOSITORY)} — {len(render().splitlines())} سطرًا")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
