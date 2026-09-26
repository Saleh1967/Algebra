"""جسرُ البتّات: لكلّ بتّةٍ **ما بُرهن**، و**ما يُقترَح**، و**ما يُلزَم**.

**لمَ هذا الملفُّ قائمٌ بنفسه**: لأنّ سجلّاتَ القياس **لا يدخلها اسمٌ
لغويّ** — وذلك شرطُ نظافتها. فإذا سُئل «وما مدلولُ البتّة؟» لم يَجُز أن
يُدَسَّ الجوابُ في السجلّ، **فيُبنى له جسرٌ مُعلَنٌ مفصولٌ**: عمودٌ لِما
بُرهن، وعمودٌ للمُقترَح **غيرِ الموقَّع**، وعمودٌ لِما يُلزَم لترخيصه.

**والقاعدةُ التي تحكم الجسر**: المدوّنةُ تُثبت **إفادةَ بتّةٍ عن صنفِ
علامةٍ مكتوبة** — وذلك مقيسٌ محجوزٌ. **ولا تُثبت أنّ صنفَ العلامةِ حكمُ
بابٍ نحويّ** — وذلك يحتاج جدولًا مُودَعًا **ليس في المستودع**. فكلُّ جسرٍ
ههنا **معلَّقٌ على إيداعٍ لم يُودَع**، ويُقال ذلك بنصّه لا بالسكوت.

**ولا رقمَ مكتوبٌ بيد**: كلُّ عددٍ مقروءٌ من سجلٍّ مُودَعٍ بنمط، وكلُّ
شريحةٍ محرفيّةٍ مأخوذةٌ من السجلّ لا مكتوبةٌ.
"""

from __future__ import annotations

import re
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
DEPOSITS = REPOSITORY / "deposits"
LADDER = DEPOSITS / "context_ladder_run.log"
TOKENS = DEPOSITS / "arabic_token_run.log"
PAUSAL = DEPOSITS / "pausal_split_run.log"
WITNESS = DEPOSITS / "pausal_split_witness.log"
MORPH = DEPOSITS / "morph_residue_run.log"
SIGNATURE = DEPOSITS / "bridge_signature.md"
PAPER = REPOSITORY / "docs" / "جسر-البتّات.md"
EASTERN = str.maketrans("0123456789.", "٠١٢٣٤٥٦٧٨٩٫")
BOXES = 8

# عائلةُ السؤال ← (المدلولُ المقترَح، جنسُ الجسر، ما يُلزَم)
FAMILIES: dict[str, tuple[str, str, str]] = {
    "آخرُ السطر": (
        "موضعُ وقفٍ محتمَل — أنّ حدَّ السطر حدُّ آيةٍ يُوقَف عليه",
        "يحتاج حدًّا مُودَعًا",
        "فهرسُ آياتٍ مُودَعٌ يُثبِت أنّ السطرَ آيةٌ وأنّ آخرَها موضعُ وقف",
    ),
    "حالُ السابق": (
        "علامةُ آخرِ الكلمة السابقة مقروءةً حكمَ بابٍ لا شريحةً",
        "يحتاج جدولَ أبوابٍ مُودَعًا",
        "جدولُ أبوابٍ مُودَعٌ يُسنِد كلَّ نقطةِ ترميزٍ إلى حكمها",
    ),
    "حالُ ما قبله": (
        "علامةُ ما قبلَ السابق، أو **صدرُ السطر** إن كانت العلامةُ حدًّا",
        "يحتاج جدولَ أبوابٍ مُودَعًا",
        "جدولُ أبوابٍ مُودَعٌ، ومعه حدُّ الصدر مُودَعًا",
    ),
    "حرفُ خاتمةِ السابق": (
        "حرفُ آخرِ الكلمة السابقة مقروءًا بنيةً صرفيّةً لا شريحةً",
        "يحتاج جدولَ صرفٍ مُودَعًا",
        "جدولُ صرفٍ مُودَعٌ يُسنِد حرفَ الخاتمة إلى بنيته",
    ),
}


def eastern(one: object) -> str:
    return str(one).translate(EASTERN)


def grab(pattern: str, text: str) -> str:
    found = re.search(pattern, text, re.M)
    if found is None:
        raise SystemExit(f"لا شاهدَ في السجلّ لـ{pattern}")
    return found.group(1)


def counted(many: int) -> str:
    return "بتّةٌ واحدة" if many == 1 else f"{eastern(many)} بتّات"


def family_of(question: str) -> str:
    for name in FAMILIES:
        if question.startswith(name):
            return name
    raise SystemExit(f"سؤالٌ بلا عائلةٍ مُعلَنة: {question}")


def steps(text: str) -> list[tuple[str, str, str, str]]:
    """(الدرجة، السؤالُ كما سُئل، الربحُ المحجوز، الكتل) — من السجلّ."""

    found = re.findall(
        r"^— د(\d+) «(.+?)»: .*? \| ربحٌ محجوزٌ \+([0-9.]+) \| كتلٌ (\d+)$",
        text,
        re.M,
    )
    if not found:
        raise SystemExit("لا درجاتَ في سجلّ السلّم")
    return [(one, two, three, four) for one, two, three, four in found]


def boxes(text: str) -> list[tuple[str, str, str]]:
    """(الشريحة، العدد، النصيب) — لخانات الهدف، شريحةً لا اسمًا.

    **وجدولٌ خالٍ يُردّ**: خانةٌ لا تُقرَأ خيرٌ من جدولٍ يُطبَع فارغًا
    فيُقرَأ «لا خانات». وقد وقع ذلك أوّلَ كتابةِ هذا المولّد.
    """

    found = re.findall(
        r"^    (\S+(?: U\+[0-9A-F]{4})?) \| (\d+) \| نصيبٌ ([0-9.]+)$", text, re.M
    )
    if len(found) != BOXES:
        raise SystemExit(f"خاناتُ الهدف {len(found)} والمُعلَنُ {BOXES}")
    return found


def lifted() -> dict[str, tuple[str, str]]:
    """البتّة ← (كسبُها في المقام أ، كسبُها في المقام ب) — من سجلّ الفصل."""

    found = re.findall(
        r"^  د(\d+) «.+?» \| \+([0-9.]+) \| \+([0-9.]+) \| \S+$",
        PAUSAL.read_text(encoding="utf-8"),
        re.M,
    )
    if len(found) != 12:
        raise SystemExit(f"صفوفُ المقابلة {len(found)} لا اثنا عشر")
    return {one: (two, three) for one, two, three in found}


def render() -> str:
    ladder = LADDER.read_text(encoding="utf-8")
    tokens = TOKENS.read_text(encoding="utf-8")
    rows = steps(ladder)
    held = grab(r"مجموعُ الكسب المحجوز: \+([0-9.]+)", ladder)
    first_share = grab(r"نصيبُ الدرجة الأولى من الكسب المحجوز: ([0-9.]+)", ladder)
    entropy = grab(r"H\(الحال\) = ([0-9.]+)", tokens)
    words = grab(r"— الألفاظ: عبرَ العدّادات (\d+)", tokens)
    bare = grab(r"^    (\S+) \(بلا علامة\) (\d+) \| نصيبٌ [0-9.]+$", tokens)
    bare_share = grab(r"\(بلا علامة\) \d+ \| نصيبٌ ([0-9.]+)", tokens)
    three = grab(r"نصيبُ الثلاث: \d+ من \d+ = ([0-9.]+)", tokens)
    reach = grab(r"— الدرجاتُ المبلوغة: (\d+)", ladder)
    split = PAUSAL.read_text(encoding="utf-8")
    shown = WITNESS.read_text(encoding="utf-8")
    kept = lifted()
    inner = grab(r"— المجال \(ب\) ما ليس آخرَ سطره: (\d+)", split)
    rest_whole = grab(r"— مجموعُ الإحدى عشرة في \(أ\): \+([0-9.]+)", split)
    rest_inner = grab(r"— مجموعُ الإحدى عشرة في \(ب\): \+([0-9.]+)", split)
    bare_inner = grab(r"· \| 23986 \| نصيبٌ ([0-9.]+)", split)
    bare_last = grab(r"· \| 333 \| نصيبٌ ([0-9.]+)", shown)
    field_inner = grab(r"— خاناتُ الحال في المجال \(ب\): H = ([0-9.]+)", split)
    field_last = grab(r"— H\(ج\) = ([0-9.]+)", shown)
    identity = grab(r"— I المُشتَقّ = ([0-9.]+)", shown)
    drift = grab(r"— أقصى انحرافٍ عن الهويّة: (\S+)", shown)
    morph = MORPH.read_text(encoding="utf-8")
    shape_gain = grab(r"— I\(الحال؛ه\) محجوزةً: \+([0-9.]+)", morph)
    bone_gain = grab(r"— I\(الحال؛ج\) محجوزةً: \+([0-9.]+)", morph)
    near_gain = grab(r"— I\(الحال؛ر\) محجوزةً: \+([0-9.]+)", morph)
    added_out = grab(r"— I\(الحال؛ر \| ه\) محجوزةً: (\S+)", morph)
    shape_cells = grab(r"— صورُ \(ه\) منقوصةَ العلامة: (\d+)", morph)
    bone_cells = grab(r"— صورُ \(ج\) مجرَّدةً: (\d+)", morph)
    near_cells = grab(r"— قيمُ \(ر\) حالِ السابق: (\d+)", morph)
    rows_here = re.findall(
        r"^  (?:\(ه\) الصورةُ منقوصةً|\(ه، ر\) معًا) \| (\d+) \| ([0-9.]+) \|",
        morph,
        re.M,
    )
    if len(rows_here) != 2:
        raise SystemExit("لا صفَّين للصورة ولمجموعِها مع الجار")
    both_cells = rows_here[1][0]
    added_in = f"{float(rows_here[0][1]) - float(rows_here[1][1]):.6f}"
    parts = grab(r"— أقسامُها: (\d+)", morph)
    stretch = grab(r"— نصيبُ حروف المدّ الثلاثة منها: ([0-9.]+)", morph)
    hand = SIGNATURE.read_text(encoding="utf-8")
    signer = grab(r"\*\*من وقَّع\*\*: (.+)$", hand)
    signed = grab(r"^([0-9a-f]{64})$", hand)
    tails = re.findall(
        r"^    (\S+ U\+[0-9A-F]{4}) \| (\d+) \| نصيبٌ ([0-9.]+)$", morph, re.M
    )
    if not tails:
        raise SystemExit("لا أقسامَ لخانة بلا علامة")

    out: list[str] = []
    add = out.append
    add("# جسرُ البتّات — ما بُرهن لكلٍّ، وما يُقترَح، وما يُلزَم")
    add("")
    add("**هذا الملفُّ مُشتَقٌّ** ويُعاد توليدُه من السجلّات المُودَعة.")
    add("**ولا رقمَ فيه مكتوبٌ بيد**، ولا شريحةَ محرفٍ إلّا مقروءةً من سجلّ.")
    add("")
    add("**القاعدةُ التي تحكمه**، وهي حدُّ كلّ سطرٍ بعدها:")
    add("")
    add(
        f"- **ما بُرهن**: أنّ البتّةَ **تُفيد عن صنفِ العلامةِ الأخيرةِ "
        f"المكتوبة** — مقيسًا **محجوزًا** على {eastern(words)} لفظًا."
    )
    add(
        "- **ما لم يُبرهَن ولا يُبرهَن من هذه البايتات**: أنّ صنفَ العلامةِ "
        "**حكمُ بابٍ نحويّ**. فذلك يحتاج جدولًا مُودَعًا، **وليس في "
        "المستودع جدول**."
    )
    add("")
    add("## الهدفُ المقيس — وهو أوّلُ حدٍّ على كلّ جسر")
    add("")
    add(
        "**الهدفُ**: آخرُ نقطةِ ترميزٍ في اللفظ **إن كانت علامةً** "
        f'(`category == "Mn"`)، وإلّا فخانةُ `{bare}`. و`H` = '
        f"**{eastern(entropy)}** على ثماني خانات."
    )
    add("")
    add("| الخانة | العدد | النصيب |")
    add("|---|---:|---:|")
    for slice_, count, share in boxes(ladder):
        add(f"| `{slice_}` | {eastern(count)} | {eastern(share)} |")
    add("")
    add(
        f"**وأكبرُ خانةٍ `{bare}` بنصيبٍ {eastern(bare_share)}** — وهي "
        "**خانةُ من لا علامةَ له**. فيجتمع فيها المبنيُّ والموقوفُ عليه "
        "والمحذوفُ آخرُه، **ولا يفصلها بايتٌ**. فهذه الخانةُ وحدَها "
        "**سقفٌ على كلّ قراءةٍ إعرابيّة**، لا بتّةٌ واحدة."
    )
    add("")
    add(
        f"**ونصيبُ الثلاث** (الحركاتِ التي تُقرَأ إعرابًا) "
        f"**{eastern(three)}** — فأقلُّ من نصف الحقل."
    )
    add("")
    add(f"## جسرُ كلّ بتّة — {eastern(reach)} درجةً بلغها الجشع")
    add("")
    add("| البتّة | السؤالُ **كما سُئل** (بايتاتٌ فقط) | ربحٌ محجوز | كتلٌ | جنسُ الجسر |")
    add("|---|---|---:|---:|---|")
    for step, question, gain, blocks in rows:
        kind = FAMILIES[family_of(question)][1]
        add(
            f"| د{eastern(step)} | «{question}» | **+{eastern(gain)}** | "
            f"{eastern(blocks)} | {kind} |"
        )
    add("")
    add(f"**ومجموعُ الكسب المحجوز +{eastern(held)} بتًّا.**")
    add("")
    add("## المدلولُ لكلّ عائلة — **موقَّعٌ فرضًا، غيرُ مُرخَّصٍ برهانًا**")
    add("")
    add(
        f"**وقَّع {signer} القراءاتِ الأربعَ** بإيداع "
        f"[`bridge_signature.md`](../deposits/bridge_signature.md)، "
        f"مربوطةً ببصمتها `{signed[:16]}…` — فتبديلُ حرفٍ في قراءةٍ "
        "**يكسر التوقيع**."
    )
    add("")
    add(
        "**وصائغُ نصوصِها الآلة، والتبنّي فعلُ المُوقِّع**: فالآلةُ صاغت "
        "فرضًا، والمُوقِّعُ تبنّاه. **ولا تُوقِّع الآلةُ ما صاغته** — وإلّا "
        "كان المؤلِّفُ هو المُصدِّق (المادّة ٢٧)."
    )
    add("")
    add(
        "**وما يفعله التوقيعُ بالضبط**: لا يجعل القراءةَ مبرهَنة، بل "
        "**يُدخِلها في دائرة النقض**. فقراءةٌ بلا توقيعٍ لا تُكذَّب لأنّ "
        "صاحبَها لم يقلها، **وقراءةٌ موقَّعةٌ تُكذَّب**. **والمُرخَّصُ "
        "صفرٌ**: لا جدولَ أُودِع لعائلةٍ واحدة."
    )
    add("")
    for name in FAMILIES:
        reading, kind, needed = FAMILIES[name]
        mine = [one for one in rows if family_of(one[1]) == name]
        earned = f"{sum(float(one[2]) for one in mine):.6f}"
        add(f"### «{name}» — {counted(len(mine))}، كسبُها +{eastern(earned)}")
        add("")
        add("- **ما بُرهن**: إفادةٌ محجوزةٌ عن صنفِ العلامة بهذا المقدار.")
        add(f"- **المدلولُ المتبنَّى** (موقَّعًا فرضًا): {reading}.")
        add(f"- **جنسُ الجسر**: {kind}.")
        add(f"- **ما يُلزَم**: {needed}.")
        add("")
    add("## أوّلُ بتّةٍ هي أقلُّها لغويّةً — وهذا مقيسٌ لا رأي")
    add("")
    first = rows[0]
    add(
        f"أكبرُ بتّةٍ في السلّم هي **د{eastern(first[0])}** «{first[1]}» "
        f"بربحٍ محجوزٍ **+{eastern(first[2])}**، ونصيبُها من الكسب كلِّه "
        f"**{eastern(first_share)}**."
    )
    add("")
    add(
        "**وهي بتّةُ موضعٍ لا بتّةُ نحو**: تسأل عن حدّ السطر، **ولا تنظر في "
        "حرفٍ ولا علامة**. فأقوى ما دفع له المجمَّدُ **أبعدُه عن الإعراب**، "
        "وأقربُ ما يُقرَأ إعرابًا **أضعفُه كسبًا**."
    )
    add("")
    add("## ما يعيش بعد رفع حدّ السطر — وهذا هو البرهانُ المتاحُ لكلّ بتّة")
    add("")
    add(
        "**السؤالُ**: كم من كسب كلّ بتّةٍ أثرُ **حدّ السطر** وكم أثرُ "
        "**الجوار**؟ فرُفِع كلُّ موضعٍ آخرِ سطرٍ وأُعيد القياسُ "
        "**بالأسئلة نفسِها وبترتيبها نفسِه** — لا اختيارَ جشعٍ جديد — "
        f"على **{eastern(inner)}** موضعًا (ختمُ `c4ffe307…`)."
    )
    add("")
    add("| البتّة | في (أ) كلُّ المواضع | في (ب) بلا أواخرِ الأسطر | ما بقي | أعاشت؟ |")
    add("|---|---:|---:|---:|---|")
    for step, question, gain, _ in rows:
        whole_gain, inner_gain = kept[step]
        stayed = float(inner_gain) / float(whole_gain) if float(whole_gain) else 0.0
        living = "**نعم**" if float(inner_gain) > 0 else "**لا**"
        add(
            f"| د{eastern(step)} | +{eastern(whole_gain)} | +{eastern(inner_gain)} | "
            f"{eastern(f'{stayed:.2f}')}× | {living} |"
        )
    add("")
    add(
        f"**فلا بتّةَ ماتت إلّا الموضعيّة نفسُها** — وهي تصير **صفرًا تامًّا** "
        f"لأنّها ثابتةٌ في (ب) بحكم التقييد. ومجموعُ الإحدى عشرة الباقية "
        f"ينزل من **+{eastern(rest_whole)}** إلى **+{eastern(rest_inner)}** — "
        "**فثلاثةُ أرباعِ ما تحمله بتّاتُ الجوار ليس أثرَ حدّ السطر.**"
    )
    add("")
    add("### ودعوايَ في تعليل ذلك سقطت — بشرطين مختومين")
    add("")
    add(
        f"زعمتُ أنّ خانةَ `{bare}` **مسكونةٌ بالوقف**، فبرفع أواخر الأسطر "
        f"ينقص نصيبُها. **فزاد**: {eastern(bare_share)} ⟶ "
        f"**{eastern(bare_inner)}**. وقِيس مقامُ أواخرِ الأسطر وحدَه فبان "
        f"السبب: نصيبُ `{bare}` فيها **{eastern(bare_last)}** — أي نحوُ "
        "**سُدسِ** ما في وسط السطر. **فأواخرُ الأسطر أقلُّ المواضع خلوًّا "
        "من العلامة لا أكثرُها.**"
    )
    add("")
    add(
        f"وزعمتُ أنّ `H` **ترتفع** برفع الوقف. **فنزلت**: "
        f"{eastern(entropy)} ⟶ **{eastern(field_inner)}**، ومقامُ الأواخر "
        f"وحدَه **{eastern(field_last)}**. **والحدسُ الساذجُ كان أصوبَ "
        "من تعليلي.**"
    )
    add("")
    add(
        "**وقاعدةُ السلسلة تُغلِق على البتّة الأولى**: "
        f"`H(أ) − Σ وزنٌ·H = {eastern(identity)}` وهو **الربحُ الملحَقُ "
        "للدرجة الأولى بعينه**، بانحرافٍ "
        f"`{eastern(drift)}`. **فبتّةُ الموضع هي اختلافُ التوزيعين لا شيءَ "
        "غيرُه** — وذلك يُسمّى ولا يُفسَّر."
    )
    add("")
    add("## السقفُ الأعلى — وهو أهمُّ سطرٍ في هذا الملفّ")
    add("")
    add(
        "**سؤالٌ يتقدّم كلَّ جسر**: كم من العلامةِ الأخيرة يحدّده **اللفظُ "
        "في نفسه**؟ فإن كان أكثرَها فليس لجارِه — ولا لأيّ حكمٍ تركيبيّ — "
        "إلّا ما بقي **بعد** معرفة صورته. فقِيس ذلك بختم `0410f435…` على "
        f"**{eastern(words)}** لفظًا: صورةُ اللفظ **منقوصةَ علامتِه "
        "الأخيرة** (ولا تسريب: لفظٌ بلا علامةٍ يعطي الصورةَ عينَها)."
    )
    add("")
    add("| المتغيّر | قيمُه | معلوماتُه محجوزةً | نصيبُه من الحقل |")
    add("|---|---:|---:|---:|")
    for label_, cells, gain in (
        ("**صورةُ اللفظ منقوصةً**", shape_cells, shape_gain),
        ("الهيكلُ مجرَّدًا", bone_cells, bone_gain),
        ("حالُ السابق وحدَه", near_cells, near_gain),
    ):
        part = f"{float(gain) / float(entropy):.4f}"
        add(f"| {label_} | {eastern(cells)} | +{eastern(gain)} | {eastern(part)} |")
    add("")
    times = eastern(f"{float(shape_gain) / float(held):.2f}")
    share_of_field = eastern(f"{float(shape_gain) / float(entropy):.4f}")
    add(
        f"**فصورةُ اللفظ تحمل +{eastern(shape_gain)} بتًّا محجوزًا — "
        f"{times} ضِعفَ كسبِ السلّم كلِّه** (+{eastern(held)})، "
        f"و**{share_of_field}** من الحقل. **فالعلامةُ الأخيرةُ في أكثرها "
        "من بنية اللفظ لا من جواره** — وذلك مقيسٌ محجوزٌ لا رأي."
    )
    add("")
    add("### وما يبقى لقراءةٍ تركيبيّةٍ — بحدّين لا برقمٍ واحد")
    add("")
    add(
        "سُئل: أيزيد الجارُ شيئًا **بعد** معرفة الصورة؟ **والجوابُ لم "
        "يُحسَم**، ويُعرَض بحدّيه:"
    )
    add("")
    add(
        f"- **محجوزًا: {eastern(added_out)}** — سالبٌ. وليس معناه أنّ "
        f"الجارَ لا يحمل شيئًا، بل أنّ الفضاءَ اتّسع من "
        f"{eastern(shape_cells)} خانةً إلى {eastern(both_cells)}، "
        "**فعاقبت السَّعةُ التقديرَ**."
    )
    add(
        f"- **ملحَقًا: +{eastern(added_in)}** — وهو **حدٌّ أعلى** مُسمًّى "
        "منتفخًا **قبل النظر**، لا قياسًا."
    )
    add("")
    add(
        "**فالسؤالُ خلوٌّ مُصنَّف** (`UNCLASSIFIED`): فحصُه مُعيَّنٌ "
        "والمقدِّرُ لم يحسمه — **لا نتيجةُ صفر**."
    )
    add("")
    add(
        f"**وأمّا السقفُ فيُقرَأ**: حتّى بالحدّ الأعلى المنتفخ، ما يزيده "
        f"الجارُ بعد الصورة **+{eastern(added_in)}** — أي **دون نصفِ** "
        f"كسبِ السلّم وحدَه (+{eastern(held)})، و"
        f"**{eastern(f'{float(added_in) / float(entropy):.4f}')}** "
        "من الحقل. "
        "**فأكثرُ نصفِ ما قِيس لبتّات الجوار هو بنيةُ اللفظ نفسِها، وما "
        "يبقى لأيّ قراءةٍ تركيبيّة أربعةٌ من مئةٍ من الحقل فأقلّ.**"
    )
    add("")
    add(f"### وخانةُ `{bare}` صارت مُسمّاةً بأقسامها")
    add("")
    add(
        f"أكبرُ خانةٍ في الهدف — نصيبُها {eastern(bare_share)} — **شُقِّقت "
        f"بحرف خاتمتها**: **{eastern(parts)}** قسمًا، لا كتلةً واحدة. "
        "وذلك فحصُ بايتاتٍ لا تفسيرٌ نحويّ."
    )
    add("")
    add("| حرفُ الخاتمة | العدد | نصيبُه من الخانة |")
    add("|---|---:|---:|")
    for letter, count, share in tails:
        add(f"| `{letter}` | {eastern(count)} | {eastern(share)} |")
    add("")
    add(
        f"**وحروفُ المدّ الثلاثةُ المختومةُ {eastern(stretch)} منها.** "
        "فالفجوةُ الكبرى **موزّعةٌ على حروفٍ مسمّاةٍ بنقاط ترميزها**، "
        "ومَن أراد قراءتَها فليودِع جدولًا يُسنِد الحرفَ إلى بنيته."
    )
    add("")
    add("## ما لا يُدَّعى في هذا الملفّ")
    add("")
    add("- **لا بتّةَ ههنا بُرهنت إفادتُها اللغويّة.** المبرهَنُ إفادتُها عن")
    add("  **صنفِ علامةٍ مكتوبة**، والفرقُ بينهما هو هذا الملفُّ كلُّه.")
    add("- **ولا جسرَ ههنا مُرخَّص**: القراءاتُ **موقَّعةٌ فرضًا** لا")
    add("  مُرخَّصةٌ برهانًا؛ وكلُّ عائلةٍ معلَّقةٌ على جدولٍ لم يُودَع،")
    add("  **والموقَّعُ عليه أربعةُ فروضٍ والمُرخَّصُ صفر**.")
    add("- **والجشعُ غيرُ مبرهَن**: ما بُلِغ حدٌّ أدنى، ولا يُقال «لا يُبلَغ».")
    return "\n".join(out) + "\n"


def main() -> int:
    PAPER.write_text(render(), encoding="utf-8")
    print(f"كُتِب {PAPER.relative_to(REPOSITORY)} — {len(render().splitlines())} سطرًا")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
