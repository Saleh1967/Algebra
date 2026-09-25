"""تُكتَب وثيقةُ العدد والمعدود **من السجلّ المُقفَل** — لا من نثر.

ولا يُكتَب رقمٌ لا يُقابِله حقلٌ في `tools/number_ledger_seal.py`، وكلُّ
حقلٍ منه مفحوصٌ بإعادة اشتقاقه ومقابَلٌ بالإيداع والسجلّ.
"""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[1]
SEAL = REPOSITORY / "tools" / "number_ledger_seal.py"
PAPER = REPOSITORY / "docs" / "العدد-والمعدود-حسابًا.md"
EASTERN = str.maketrans("0123456789.", "٠١٢٣٤٥٦٧٨٩٫")


def eastern(one: object) -> str:
    return str(one).translate(EASTERN)


def _seal() -> Any:
    spec = importlib.util.spec_from_file_location("number_ledger_seal", SEAL)
    if spec is None or spec.loader is None:
        raise SystemExit("لا قارئَ لسجلّ العدد والمعدود")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def render() -> str:
    tool = _seal()
    r = tool.FROZEN_NUMBERS
    complaints = tool.verify_against_logs()
    if complaints:
        raise SystemExit(f"لا تُكتَب وثيقةٌ على سجلٍّ مخالف: {complaints}")
    whole = sum(r.places)
    gains = [float(one) for one in r.step_gains]

    out: list[str] = []
    add = out.append
    add("# العددُ والمعدود — حسابًا لا قياسًا")
    add("")
    add(f"**ختمُ السجلّ**: `{tool.RECORD_DIGEST[:8]}…` — مُشتَقٌّ من حقوله.")
    add("")
    add("**هذا فصلٌ لم تُجرِه هذه الشجرة.** أُجري على **تشجيرٍ إعرابيٍّ ليس**")
    add("**في هذا المستودع**، فلا أملك مدوّنتَه ولا حوافَّه. **ولا أوقّع**")
    add("**تأويلَه**: لا القاعدةَ المنقولة، ولا تعليلَ المخالفات الثلاث، ولا")
    add("أنّ خمسةً وثلاثين موضعًا تكفي حكمًا على العربيّة.")
    add("")
    add("**وما فعلتُه**: أعدتُ **حسابَه على أعداده**، وصعّدتُ **بتّةً بتّة**")
    add("على توزيعه، وأعدتُ اشتقاقَ مجالات ثقته. **وما لا تسمح به أعدادُه**")
    add("**سُمّي دَينًا ولم يُخمَّن.**")
    add("")
    add("## التعدادُ التامّ — induction ON")
    add("")
    add("| الصنف | المواضع | المطابق | H |")
    add("|---|---|---|---|")
    for index, name in enumerate(r.classes):
        here = tool.entropy(
            (r.conforming[index], r.places[index] - r.conforming[index])
        )
        add(
            f"| {name} | {eastern(r.places[index])} | {eastern(r.conforming[index])} "
            f"| {eastern(f'{here:.4f}')} |"
        )
    add("")
    add(f"**المواضعُ {eastern(whole)}، والمطابقُ {eastern(sum(r.conforming))}.**")
    add("**والحيرةُ تنعدم تمامًا في ثلاثة أصنافٍ من أربعة**، ومحصورةٌ كلُّها")
    add("في صنفٍ واحد.")
    add("")
    add("## ما أُعيد اشتقاقُه فطابق")
    add("")
    add("| المقدار | المعروض | المُشتَقُّ ههنا |")
    add("|---|---|---|")
    flat = tool.entropy(tuple(two for _, two in r.outcomes))
    given = math.fsum(
        r.places[index]
        / whole
        * tool.entropy((r.conforming[index], r.places[index] - r.conforming[index]))
        for index in range(4)
    )
    for label, shown, mine in (
        ("H(المعدود) بلا شرط", r.flat, f"{flat:.4f}"),
        ("H(المعدود | صنفِ العدد)", r.given, f"{given:.4f}"),
        ("الكسب", r.gain, f"{flat - given:.4f}"),
        ("نصيبُه من الحيرة", r.share, f"{(flat - given) / flat:.4f}"),
    ):
        add(f"| {label} | {eastern(shown)} | {eastern(mine)} |")
    add("")
    add("**وتوزيعُ مخرج المعدود لم ينشره الأنبوب**، فقراءتُه لي:")
    add("")
    add("| المخرج | المواضع |")
    add("|---|---|")
    for key, count in r.outcomes:
        add(f"| {key} | {eastern(count)} |")
    add("")
    add("**وسندُ هذه القراءة الوحيدُ** أنّها تُعيد `H` المنشورةَ")
    add(f"(**{eastern(r.flat)}**) **بلا بقيّة**. **وهذا سندٌ يُذكَر بحدّه**،")
    add("**ولا يُسمّى نصَّ الأنبوب.**")
    add("")
    add("## التصعيدُ بتّةً بتّة")
    add("")
    add("| الدرجة | السؤال | الربح | كتل |")
    add("|---|---|---|---|")
    add("| د٠ | — بلا سؤال — | — | ١ |")
    for index, step in enumerate(r.steps):
        add(
            f"| د{eastern(index + 1)} | «أمن {step}؟» "
            f"| {eastern(r.step_gains[index])} | {eastern(index + 2)} |"
        )
    add("")
    add(f"**وأوّلُ بتّةٍ وحدَها تشتري {eastern(f'{gains[0] / float(r.gain):.4f}')}**")
    add("**من الكسب كلِّه** — أكثرَ من أربعة أخماسه. **والثانيةُ تبلغ الشرطَ**")
    add("**التامّ**، فلا تربح ثالثةٌ شيئًا.")
    add("")
    add("**وبتّتان تستنفدان أربعةَ أصنافٍ، والسقفُ الخام بتّتان** — **فلا**")
    add("**إسرافَ في التخصيص ههنا**، بخلاف ما وقع في فصلٍ آخرَ حُمِلت فيه")
    add("أربعَ عشرةَ حالةً على ثمانِ بتّات.")
    add("")
    add("## induction FOR — ولم ينجح، وذاك إعلانُ الأنبوب نفسِه")
    add("")
    add("| الذراع | المحجوز | ويلسن ٩٥٪ |")
    add("|---|---|---|")
    for label, hits, tries in r.held_out:
        low, high = tool.wilson(hits, tries)
        add(
            f"| {label} | {eastern(hits)}/{eastern(tries)} = "
            f"{eastern(f'{hits / tries:.4%}')} "
            f"| [{eastern(f'{low:.4%}')} , {eastern(f'{high:.4%}')}] |"
        )
    add("")
    add("**والمجالان متداخلان** — فالعيّنةُ أصغرُ من أن تحمل دعوى تنبّؤ.")
    add("**فالحكمُ ههنا قام على التعداد التامّ (induction ON) لا على**")
    add("**التنبّؤ (induction FOR)**، وهذا حدُّه.")
    add("")
    add("## الدُّيونُ — مُسمّاةٌ بنصّها")
    add("")
    for name, why in r.debts:
        add(f"- **{name}** — {why}.")
    add("")
    add("## ما لا يُدَّعى بهذه الوثيقة")
    add("")
    add("**أنّ الأرقامَ تُعيد حسابَها لا يعني أنّ القياسَ صحيح.** المُعادُ")
    add("**حسابُ الأنبوب على أعداده**، لا **أعدادُه على المصحف**: تلك تحتاج")
    add("تشجيرَه، **وليس مُودَعًا**. فما طابق ههنا **طابق حسابًا**، ولا")
    add("يُقال إنّه طابق قياسًا.")
    add("")
    return "\n".join(out) + "\n"


def main() -> int:
    PAPER.write_text(render(), encoding="utf-8")
    print(f"كُتِب {PAPER.relative_to(REPOSITORY)} — {len(render().splitlines())} سطرًا")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
