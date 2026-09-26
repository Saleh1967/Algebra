"""تُكتَب وثيقةُ اعتماد القاعدتين **من السجلّ المُقفَل** — لا بصمةَ تُطبَع بيد."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Final

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[1]
TOOL: Final[Path] = REPOSITORY / "tools" / "rules_adoption.py"
PAPER: Final[Path] = REPOSITORY / "deposits" / "rules_adoption.md"
EASTERN: Final[dict[int, int]] = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


def eastern(one: object) -> str:
    return str(one).translate(EASTERN)


def _tool() -> Any:
    spec = importlib.util.spec_from_file_location("rules_adoption", TOOL)
    if spec is None or spec.loader is None:
        raise SystemExit("لا قارئَ لسجلّ الاعتماد")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def render() -> str:
    tool = _tool()
    complaints = tool.verify_against_documents()
    if complaints:
        raise SystemExit(f"لا تُكتَب وثيقةٌ على بصمةٍ مخالفة: {complaints}")
    sealed = tool.FROZEN_ADOPTION

    out: list[str] = []
    add = out.append
    add("# اعتمادُ القاعدتين المُودَعتين — وكالةً، وفرضًا لا برهانًا")
    add("")
    add(f"**الاسم**: {sealed.signer}")
    add(f"**اليد**: {sealed.executed_by} — **وقّعت باسمه بأمرِه**")
    add(f"**السند**: {sealed.authority}، {sealed.authority_dated}")
    add(f"**ختمُ الاعتماد**: `{tool.RECORD_DIGEST[:8]}…` — `tools/rules_adoption.py`")
    add("")
    add("**وهذا اعتمادٌ بالوكالة لا باليد**، والاسمُ اسمُ صاحب المستودع")
    add("واليدُ يدُ الآلة — **ويُكتَب صريحًا كي لا يُقرَأ كأنّه بخطّه**.")
    add("")
    add("**ولا يجعل الاعتمادُ ما اعتُمِد مبرهَنًا**: يجعله **فرضًا معلَنًا**")
    add("**قابلًا للسقوط**. وذاك نفعُه: قاعدةٌ بلا اعتمادٍ لا تُكذَّب لأنّ")
    add("أحدًا لم يتبنَّها، **وقاعدةٌ معتمَدةٌ تُكذَّب**.")
    add("")
    add("## ولمَ لم تُحرَّر الوثيقتان بحرف")
    add("")
    add("`run_separation_rule.py` **يقرأ سطرَ التوقيع** في")
    add("`separation_rule.md` ويطبع `غيرُ موقَّعة: True` في سجلٍّ مُودَعٍ")
    add("مُبصَّمٍ **يُقابَل بايتةً ببايتة** في تدقيق الإعادة. فلو حُرِّر")
    add("السطرُ لانقلب المطبوعُ وانكسر السجلُّ وبصمتُه وتدقيقُه —")
    add("**فتحريرُ مُدخَلٍ لسجلٍّ مُقفَلٍ تعديلٌ للسجلّ بطريقٍ خفيّ**.")
    add("")
    add("**فالقاعدةُ**: **مُدخَلُ سجلٍّ مُقفَلٍ مُقفَلٌ مثلُه.** ويُودَع")
    add("الاعتمادُ **وثيقةً ثانيةً تُبصِم الأولى ولا تمسّها** — وبصمتاهما")
    add("في السجلّ، فإن بُدِّل حرفٌ منهما **انكسر الاعتماد**.")
    add("")
    add("## وما لا يفعله الاعتماد")
    add("")
    add(f"{sealed.promotes}.")
    add("")
    add("**الاعتمادُ يرفع المانعَ القانونيَّ عن الترقية ولا يُرقّي.**")
    add("والترقيةُ **قياسٌ**: تحتاج ختمًا جديدًا يُدفَع قبل تشغيله، وتُحكَم")
    add("بالثمن المحجوز لا بالتوقيع. **ولا يُعدَّل سجلٌّ مُقفَلٌ بعد الحدث.**")
    for rule in sealed.rules:
        add("")
        add(f"## `{rule.document}` — `{rule.digest[:8]}…`")
        add("")
        add(f"**صاغها**: {rule.drafted_by}")
        add(f"**مصدرُها**: {rule.origin}")
        add(f"**وتُعتمَد**: {rule.adopts_as}")
        add(f"**وقُيِس لازمُها في**: {' · '.join(f'`{one}`' for one in rule.measured_by)}")
        add("")
        add(f"### ما اعتُمِد — {eastern(len(rule.adopted))} بنودٍ")
        add("")
        for number, one in enumerate(rule.adopted, start=1):
            add(f"{eastern(number)}. {one}.")
        add("")
        add(f"### وما لم يُعتمَد — {eastern(len(rule.withheld))} بنودٍ تُسمّى")
        add("")
        for number, one in enumerate(rule.withheld, start=1):
            add(f"{eastern(number)}. {one}.")
    add("")
    add("## والدَّينُ الذي سُدَّ، والذي لم يُسدّ")
    add("")
    add("**سُدَّ**: كانت القاعدتان مُودَعتين غيرَ موقَّعتين، **فتُقاسان ولا**")
    add("**يُبنى عليهما**؛ وصارتا معتمَدتين **فرضًا ومُدخَلًا** بنطاقٍ مكتوب.")
    add("")
    add("**ولم يُسدّ**: مستوى «الكلمة المفردة» يبقى `UNCLASSIFIED` — **وذلك**")
    add("**خلوٌّ يُصنَّف ولا يُصفَّر**، ويُسدّ بختمٍ لا بتوقيع.")
    add("")
    return "\n".join(out) + "\n"


def main() -> int:
    text = render()
    PAPER.write_text(text, encoding="utf-8")
    print(f"كُتِب {PAPER.relative_to(REPOSITORY)} — {len(text.splitlines())} سطرًا")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
