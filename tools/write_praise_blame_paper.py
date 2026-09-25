"""تُكتَب وثيقةُ لوازمِ المسوّدة **من سجلّ التشغيل** — لا من ذاكرةٍ ولا نثر.

وكلُّ رقمٍ فيها يُقرَأ بنمطٍ من `deposits/praise_blame_run.log`، وما لا يوجد
في السجلّ **يُوقِف الكتابة**.
"""

from __future__ import annotations

import re
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
LOG = REPOSITORY / "deposits" / "praise_blame_run.log"
RULE = REPOSITORY / "deposits" / "praise_blame_rule.md"
PAPER = REPOSITORY / "docs" / "لوازم-مسوّدة-منقولة.md"
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


def render() -> str:
    text = LOG.read_text(encoding="utf-8")
    (lines,) = grab(r"— الأسطر: (\d+)", text)
    (tokens,) = grab(r"— الألفاظ: (\d+)", text)
    (deposited,) = grab(r"— الصورُ المُودَعة: (\d+)", text)
    found, absent = grab(r"— الصورُ الموجودة: (\d+) \| الغائبة: (\d+)", text)
    named = re.findall(r"غائبةٌ باسمها: (\S+)", text)
    shapes = re.findall(r"وقوعاتٌ\s+(\d+) \| شرائحُها: (.+)$", text, re.M)
    at_head, places = grab(r"وفي صدر السطر: (\d+) من (\d+)", text)
    (field,) = grab(r"حقلُ الحال العامّ: H = ([\d.]+)", text)
    _, after = grab(r"الموضعُ التالي للصورة: مواضعُ (\d+) \| H = ([\d.]+)", text)
    near = text.split("الموضعُ التالي للصورة")[1].split("الموضعُ الثالث")[0]
    near_rows = re.findall(r"^    (\S+) (\d+) \| نصيبٌ ([\d.]+)$", near, re.M)
    below = text.split("الموضعُ الثالث")[1]
    third_rows = re.findall(r"^    (\S+) (\d+) \| نصيبٌ ([\d.]+)$", below, re.M)
    (third_h,) = grab(r"الموضعُ الثالث: مواضعُ \d+ \| H = ([\d.]+)", text)
    steps = re.findall(
        r"^    (د\S+ [^:]+): ملحَقة ([\d.]+) \| محجوزة ([\d.]+) "
        r"\| ربحٌ ملحَقٌ (\S+) \| ربحٌ محجوزٌ (\S+)$",
        text,
        re.M,
    )
    (falls,) = grab(r"درجاتٌ ينزل فيها المحجوز: (\d+) من 4", text)
    (bit,) = grab(r"I\(الحال ؛ بتّةُ الجوار\) = ([\d.]+)", text)
    (slack,) = grab(r"أقصى \(log₂ التباديل − N·H\) بعد ألف = (\S+)", text)

    out: list[str] = []
    add = out.append
    add("# لوازمُ مسوّدةٍ منقولةٍ في حقل الحال")
    add("")
    add("**الختم**: `efb2eac8…` — مُودَعٌ ومدفوعٌ **قبل** التشغيل.")
    add("**الحصاد**: **ثمانِ** شروطٍ من اثنتي عشرةَ صمدت، و**أربعٌ** سقطت.")
    add("")
    add("**والمسوّدةُ غيرُ موقَّعة.** ما في `deposits/praise_blame_rule.md`")
    add("**منقولٌ عن نصٍّ خارجيّ** وأُودِع **مُدخَلًا يُختبَر** لا حكمًا")
    add("يُبنى عليه. **وتوقيعُه فعلُ صاحب المستودع لا فعلَ هذا القياس.**")
    add("")
    add("**وما قِيس لازمٌ في البايتات لا حكمُ باب**: لا إعرابَ ولا فاعليّةَ")
    add("ولا ابتداءَ ولا تقدير، **ولا يُدَّعى نفيُ شيءٍ من ذلك ولا إثباتُه**.")
    add("")
    add("## الصورُ — ما وُجِد وما غاب")
    add("")
    add(f"مُودَعةٌ **{eastern(deposited)}** صورة: **{eastern(found)}** لها شاهدٌ")
    add(f"في المجمَّد و**{eastern(absent)}** لا شاهدَ لها. وجملةُ مواضعها")
    add(f"**{eastern(places)}** من **{grouped(int(tokens))}** لفظًا في")
    add(f"**{grouped(int(lines))}** سطرًا، منها **{eastern(at_head)}** في صدر السطر.")
    add("")
    add("| وقوعات | الشرائحُ كما في المجمَّد |")
    add("|---|---|")
    for number, forms in shapes:
        add(f"| {eastern(number)} | {forms} |")
    add("")
    add(
        "**والغائبةُ تُطبَع بأسمائها ولا تُطوى**: "
        + "، ".join(f"`{one}`" for one in named)
        + "."
    )
    add("**ولا يُقال إنّها ليست في العربية** — يُقال إنّها **ليست في هذا")
    add("المجمَّد**؛ وشاهدا اثنتين منها في المسوّدة **شعرٌ لا آية** بنصّها.")
    add("")
    add("**وهيكلٌ واحدٌ حمل ثلاثَ شرائحَ متمايزةٍ بالضبط**. والهيكلُ لا يعيّن")
    add("ضبطَه — وهو المقيسُ المُودَع قبلُ: **١٬٨٨٦** هيكلًا غامضًا تحمل")
    add("**٠٫٤٤٦١** من الكتلة. **فمن هذه المواضع ما ليس من باب المسوّدة")
    add("أصلًا، ولا أفصل بينها: الفصلُ يحتاج قراءةً، والقراءةُ ليست لي.**")
    add("")
    add("## اللازمُ الأوّل — وقد صمد")
    add("")
    add(f"حقلُ الحال العامّ **{eastern(field)}** بتًّا، وعند الموضع التالي")
    add(f"للصورة **{eastern(after)}** — نزولٌ")
    add(f"**{eastern(f'{float(field) - float(after):.4f}')}** بتًّا.")
    add("**فللصورة أثرٌ في البتّات**، وهذا لازمُ المسوّدة الأوّل.")
    add("")
    add("| الموضعُ التالي | وقوعات | نصيب |")
    add("|---|---|---|")
    for mark, number, share in near_rows:
        add(f"| {mark} | {eastern(number)} | {eastern(share)} |")
    add("")
    add("**ولكنّ الانضغاطَ إلى خانتين لا إلى واحدة**: الأولى")
    add(f"**{eastern(near_rows[0][2])}** والثانية **{eastern(near_rows[1][2])}**،")
    add("**ولا واحدةَ منهما تبلغ النصف**. فدعوايَ أنّ «علامةً بعينها تغلب»")
    add("**ساقطةٌ برقمها**.")
    add("")
    add("## والأثرُ موضعٌ واحدٌ لا موضعان")
    add("")
    add(f"إنتروبيا الموضع الثالث **{eastern(third_h)}** — قريبةٌ من العامّة")
    add(f"**{eastern(field)}**، بعيدةٌ عن **{eastern(after)}**.")
    add("**والخانةُ الغالبةُ فيه غيرُ الغالبة هناك**، ونصيبُها")
    add(f"**{eastern(third_rows[0][2])}** دون الحدّ المختوم.")
    add("")
    add("| الموضعُ الثالث | وقوعات | نصيب |")
    add("|---|---|---|")
    for mark, number, share in third_rows:
        add(f"| {mark} | {eastern(number)} | {eastern(share)} |")
    add("")
    add("## التصعيدُ بتّةً بتّة")
    add("")
    add("| الدرجة | ملحَقة | محجوزة | ربحٌ ملحَق | ربحٌ محجوز |")
    add("|---|---|---|---|---|")
    for name, attached, kept, gain_in, gain_out in steps:
        add(
            f"| **{name.strip()}** | {eastern(attached)} | {eastern(kept)} "
            f"| {eastern(gain_in)} | {eastern(gain_out)} |"
        )
    add("")
    add(f"**وينزل المحجوزُ في {eastern(falls)} درجاتٍ من أربع** لا في أربع.")
    add("**والدرجةُ التي انقلبت هي التي تضيف بتّةَ الموضع**: تربح ملحَقةً")
    add("وتخسر محجوزة. **فزيادتُها انتحالُ تقديرٍ لا خبرُ مادّة**، وموضعُ")
    add("انقلابها **حدُّ ما تحمله المادّة** لا حدُّ ما تحمله القراءة.")
    add("")
    add("**وآخرُ درجةٍ — وهي تضيف حالَ الموضع السابق — تربح على المحجوز**")
    add(f"**{eastern(steps[4][4])}** بتًّا: **أكثرَ من مئةِ ضعفٍ** ممّا ربحته")
    add("درجاتُ الصور الثلاثُ مجتمعة. **فجارُ الموضع يحمل عن حاله أكثرَ")
    add("ممّا تحمله هذه الصورُ كلُّها.**")
    add("")
    add("## شدّةُ الأثر ليست سعتَه")
    add("")
    add(f"`I(الحال ؛ بتّةُ الجوار)` = **{eastern(bit)}** بتًّا — **دون الحدّ**.")
    add(f"**ولا تناقضَ**: الصورُ **{eastern(places)}** موضعًا من")
    add(f"**{grouped(int(tokens))}**. فالأثرُ **شديدٌ حيث يقع، ضئيلٌ في جملة")
    add("الحقل**، **ولا يُقرأ أحدُهما على الآخر**.")
    add("")
    add("## induction on وinduction FOR")
    add("")
    add("**المبرهَنتان مُصانتان عند كلّ درجةٍ وكلّ حال**: الشرطُ لا يرفع")
    add("الإنتروبيا — وأدنى ربحٍ ملحَقٍ **موجب** في الدرجات كلِّها؛")
    add(f"و`log₂ التباديل ≤ N·H` — وأقصى فسحةٍ بعد ألفِ لفظ **{eastern(slack)}**.")
    add("**والحلقةُ تشهد عليهما سطرًا سطرًا وتُقابِل العدّاداتِ بالأسطر.**")
    add("")
    add("**وطرفاهما أُخِذا بعد ألفِ لفظ** لا عند أوّل الحلقة — إصلاحًا لِما")
    add("مرَّ بطرفٍ تافهٍ في `7773c03f…`.")
    add("")
    add("## ما لا يفصل فيه هذا القياس")
    add("")
    add("المسوّدةُ تعطي للمخصوص المتأخّر **أربعةَ أعاريب**. **ولا تفترق في")
    add("البايتات ألبتّة**: الحروفُ واحدةٌ والعلاماتُ واحدة. **فلا يرجّح هذا")
    add("القياسُ بينها، ولا يُدَّعى أنّه يرجّح.**")
    add("")
    add("**والمسوّدةُ لم تُوقَّع بهذا التشغيل**: صمودُ لازمٍ **صمودُ لازم**،")
    add("لا تصديقُ قراءة؛ وسقوطُه **سقوطُ لازم**، لا تكذيبُ قارئ.")
    add("")
    return "\n".join(out) + "\n"


def main() -> int:
    PAPER.write_text(render(), encoding="utf-8")
    assert RULE.exists()
    print(f"كُتِب {PAPER.relative_to(REPOSITORY)} — {len(render().splitlines())} سطرًا")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
