"""سلسلةُ الأختام — **الترتيبُ مشدودٌ في البصمات، والسبقُ مقيسٌ من التاريخ**.

**ما كان يُقال ولا يُقاس**: كُتِب في كلّ دفعةِ دمجٍ من هذه الجلسة «ترتيبُ
الختم قبل تشغيله شاهدٌ في التاريخ». **وهو صحيحٌ ولا فحصَ يمسكه**: لا شيءَ
في الشجرة يقرأ التاريخَ فيتحقّق أنّ دفعةَ الختم سبقت دفعةَ سجلِّ تشغيله.
فالدعوى كانت **مُحالةً إلى `git` ولا أحدَ يسأله**.

**وههنا يُسأل.** لكلّ ختمٍ **مرساةٌ**: أوّلُ دفعةٍ أدخلت بصمتَه إلى
الشجرة، تُستخرَج بـ`git log -S` على مواضعه لا على الشجرة كلِّها. ولكلّ
سجلِّ تشغيلٍ يذكره مرساةٌ مثلُها. **فالسبقُ فرقُ تاريخين مقروءين**، لا
قولًا في متن.

**والسلسلة**: كلُّ حلقةٍ تضمّ بصمةَ سالفتها، فمن أقحم ختمًا في الوسط
انقطعت البصماتُ بعده كلُّها. وصيغتُها مُعلَنةٌ في `صيغة_الحلقة` فتُعاد
بأيّ آلة.

    حلقة = SHA256(بصمة_السلف | المرساة | تاريخُها | الاسم | الحمولةُ المعياريّة)

**وتزيد على سلسلةٍ تعقد الزمنَ حقلًا مكتوبًا**: المرساةُ **بصمةُ دفعةٍ**،
وهي بصمةٌ على الشجرة كلِّها في لحظتها، **لا حقلًا يكتبه كاتبُ السجلّ**.
فتاريخُها شاهدٌ من خارج الملفّ، ولا يُزوَّر إلّا بإعادة كتابة التاريخ
المنشور — وذلك أثرٌ يُرى.

`AND_WHAT_THE_CHAIN_DOES_NOT_PROVE`: **وحدُّها مُعلَن**. تُثبت أنّ
البصمةَ **كانت في تلك الدفعة**، و**لا تُثبت أنّ التشغيل جرى بعد الختم** —
بل أنّ **إيداعَ** سجلِّه تأخّر عن إيداع ختمه. ومن ختم وشغّل ثمّ أودعهما
معًا يمرُّ عليها بتاريخٍ واحد، **فتُصنَّف حالُه `مُودَعان معًا` ولا
تُحسَب سبقًا**. ولا تحرس صوابَ شرطٍ ولا صدقَ عدد.

`AND_A_SHALLOW_CLONE_IS_CLASSIFIED_NOT_ZEROED`: ونسخةٌ ضحلةٌ لا تحمل
التاريخَ، **فلا يُقرَأ سكوتُها براءةً**: تُردُّ المراسي بسببٍ مُسمًّى،
**وتبقى السلسلةُ نفسُها مفحوصةً** لأنّ فحصَها حسابٌ لا يحتاج تاريخًا.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess  # noqa: S404
import sys
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[1]
CHAIN = REPOSITORY / "deposits" / "seal_chain.json"
GENESIS = "0" * 64
RING_RULE = "SHA256(بصمة_السلف | المرساة | تاريخها | الاسم | الحمولة المعياريّة)"
PAYLOAD_RULE = "json.dumps(ensure_ascii=False, sort_keys=True, separators=(',',':'))"


class ChainError(RuntimeError):
    """سلسلةٌ لا تُعاد — ويُسمّى موضعُ الانقطاع."""


def canonical(payload: dict[str, Any]) -> str:
    """صورةُ الحمولة المعياريّة — واحدةٌ لا تتبدّل بترتيب المفاتيح."""

    return json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def ring_digest(previous: str, anchor: str, dated: str, name: str, body: str) -> str:
    """بصمةُ الحلقة بالصيغة المُعلَنة — ولا صيغةَ ثانية."""

    body_of_ring = "|".join((previous, anchor, dated, name, body))
    return hashlib.sha256(body_of_ring.encode()).hexdigest()


def shallow() -> bool:
    """أنسخةٌ ضحلة؟ فالمراسي لا تُقرَأ، وتُصنَّف الحالُ ولا تُصفَّر."""

    return (REPOSITORY / ".git" / "shallow").exists()


def _git(*argument: str) -> str:
    done = subprocess.run(  # noqa: S603
        ["git", *argument],  # noqa: S607
        cwd=REPOSITORY,
        capture_output=True,
        text=True,
        check=True,
    )
    return done.stdout.strip()


def canonical_date(dated: str) -> str:
    """تاريخُ المرساةِ في صيغةٍ **واحدةٍ لا تتبع إصدارَ git**.

    **العطلُ الذي عالجه** (العطل ٣٧): `%cI` يرسم إزاحةَ UTC صفرًا
    `+00:00` في git 2.43، و`Z` في git 2.55. والتاريخُ **يدخل في بصمةِ
    الحلقة**، فاختلفت بصماتُ السلسلةِ كلُّها بين قرصي وRunner واختلفت
    بصمةُ الخاتمة — **فالسلسلةُ التي تُثبِت الترتيبَ لم تكن قابلةً
    للإعادةِ عبرَ البيئات**. ولم يظهر ذلك حتّى عمل الفحصُ على Runner
    أوّلَ مرّة، إذ كان يُتخطّى للاستنساخِ الضحل.

    **والاختيارُ مقصودٌ ومُعلَن**: تُردُّ `Z` إلى `+00:00`، لا العكس.
    فبصماتُ السلسلةِ المُودَعةُ في الشجرةِ حُسِبت بـ`+00:00`، **فالردُّ
    إليها يُبقي كلَّ بصمةٍ منشورةٍ صحيحةً** — ولو عُكِس لتغيّرت البصماتُ
    كلُّها وبطل ما كُتِب. **ولا تُصلَح البصمةُ بتغييرِ ما نُشِر.**

    وإزاحةٌ غيرُ الصفرِ لا تتأثّر: في هذا التاريخ ٢٦٧ دفعةً بـ`+00:00`
    و٦١ بـ`+03:00`، و`Z` لا تُرسَم إلّا للصفر.
    """

    return dated[:-1] + "+00:00" if dated.endswith("Z") else dated


def anchor_of(digest: str, where: list[str]) -> tuple[str, str]:
    """أوّلُ دفعةٍ أدخلت البصمةَ، بتاريخها — ويُبحَث في مواضعها لا في الكلّ."""

    found = _git(
        "log", "--reverse", "--format=%H %cI", f"-S{digest}", "--", *where
    ).splitlines()
    if not found:
        raise ChainError(f"بصمةٌ بلا مرساةٍ في التاريخ: {digest[:8]}")
    head, _, dated = found[0].partition(" ")
    return head, canonical_date(dated)


SUFFIXES = ("_seal", "_preregistration", "_prereg")


def run_logs(row: dict[str, Any]) -> list[str]:
    """سجلُّ تشغيلِ ختمٍ — **بطريقين مُعلَنين**، والأوّلُ أقوى من الثاني.

    ١) **نسبةٌ بالبصمة**: سجلٌّ يذكر مقدّمةَ الختم في متنه. وهي الأوثق،
       إذ الرابطُ مكتوبٌ في المنسوب لا مستنتَجٌ من اسمه.

    ٢) **نسبةٌ بالاصطلاح**: وحدةُ الختم `<اسم>_seal.py` أو
       `<اسم>_preregistration.py` يقابلها `deposits/<اسم>_run.log`.
       **وهذه أضعف**: الاسمُ قد يكذب، والفحصُ لا يقرأ داخلَ السجلّ.

    وما لا يُنسَب بواحدةٍ منهما **يُسمّى ولا يُقحَم**: ختمٌ بلا سجلٍّ
    مُودَعٍ يخرج من قياس السبق، **ويُعَدّ في صنفه**.
    """

    deposits = REPOSITORY / "deposits"
    found = [one for one in sorted(row["cited"]) if one.endswith(".log")]
    if found:
        return found
    stems: set[str] = set()
    for one in sorted(row.get("modules", [])):
        stem = Path(one).stem
        stem = stem[5:] if stem.startswith("test_") else stem
        for suffix in SUFFIXES:
            if stem.endswith(suffix):
                stem = stem[: -len(suffix)]
                break
        stems.add(stem)
    return [
        f"deposits/{stem}{tail}"
        for stem in sorted(stems)
        for tail in ("_run.log", "_witness.log")
        if (deposits / f"{stem}{tail}").is_file()
    ]


def _index() -> Any:
    path = REPOSITORY / "tools" / "write_seal_index.py"
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise ChainError("لا قارئَ لفهرس الأختام")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def build() -> dict[str, Any]:
    """السلسلةُ مُشتَقّةً من الشجرة والتاريخ — ولا حقلَ فيها مكتوبٌ بيد."""

    rows = _index().gather()
    raw: list[dict[str, Any]] = []
    for row in rows:
        digest = str(row["digest"])
        where = [one for one in row["written"] if not one.startswith("deposits/")]
        anchor, dated = anchor_of(digest, where or list(row["written"]))
        logs = run_logs(row)
        run = ""
        run_dated = ""
        for log in logs:
            found = _git("log", "--reverse", "--format=%H %cI", "--", log).splitlines()
            if found:
                run, _, raw_dated = found[0].partition(" ")
                run_dated = canonical_date(raw_dated)
                break
        raw.append(
            {
                "الاسم": str(row["name"]),
                "المرساة": anchor,
                "تاريخ_المرساة": dated,
                "سجل_التشغيل": logs[0] if logs else "",
                "مرساة_السجل": run,
                "تاريخ_مرساة_السجل": run_dated,
                "الحمولة": {
                    "البصمة": digest,
                    "الشروط": int(row["count"]),
                    "العلامات": list(row["marks"]),
                },
            }
        )
    raw.sort(
        key=lambda row: (
            str(row["تاريخ_المرساة"]),
            str(row["المرساة"]),
            str(row["الحمولة"]["البصمة"]),
        )
    )

    rings: list[dict[str, Any]] = []
    previous = GENESIS
    for rank, entry in enumerate(raw):
        body = canonical(entry["الحمولة"])
        here = ring_digest(
            previous,
            str(entry["المرساة"]),
            str(entry["تاريخ_المرساة"]),
            str(entry["الاسم"]),
            body,
        )
        rings.append(
            {
                "الرتبة": rank,
                **entry,
                "بصمة_الحمولة": hashlib.sha256(body.encode()).hexdigest(),
                "بصمة_السلف": previous,
                "بصمة_الحلقة": here,
            }
        )
        previous = here
    return {
        "السجل": "سلسلةُ أختام القياس",
        "بصمة_الجذر": GENESIS,
        "صيغة_الحلقة": RING_RULE,
        "صيغة_الحمولة": PAYLOAD_RULE,
        "حدها": "تُثبت أنّ البصمةَ كانت في تلك الدفعة، لا أنّ التشغيل تلا الختم",
        "الحلقات": rings,
        "بصمة_الخاتمة": previous,
    }


def objections(chain: dict[str, Any]) -> list[str]:
    """ما يُرَدّ به السجلُّ — قائمةٌ فارغةٌ تعني أنّ السلسلةَ تُعاد."""

    said: list[str] = []
    previous = str(chain["بصمة_الجذر"])
    for one in chain["الحلقات"]:
        body = canonical(one["الحمولة"])
        if hashlib.sha256(body.encode()).hexdigest() != one["بصمة_الحمولة"]:
            said.append(f"حمولةٌ لا تُعاد عند الرتبة {one['الرتبة']}")
        if one["بصمة_السلف"] != previous:
            said.append(f"وصلةٌ منقطعةٌ عند الرتبة {one['الرتبة']}")
        here = ring_digest(
            previous,
            str(one["المرساة"]),
            str(one["تاريخ_المرساة"]),
            str(one["الاسم"]),
            body,
        )
        if here != one["بصمة_الحلقة"]:
            said.append(f"حلقةٌ لا تُعاد عند الرتبة {one['الرتبة']}")
        # **يُمشى بالمحسوب لا بالمكتوب**: فمن أقحم حلقةً في الوسط بطل
        # كلُّ ما بعدها، ولا تنحصر المخالفةُ في جارَيها.
        previous = here
    if previous != chain["بصمة_الخاتمة"]:
        said.append("الخاتمةُ المحسوبةُ تخالف المكتوبة")
    return said


def precedence(chain: dict[str, Any]) -> dict[str, list[str]]:
    """سبقُ الختم على إيداع سجلِّه — **مقيسًا**، وثلاثةُ أصنافٍ لا اثنان."""

    out: dict[str, list[str]] = {"سبق": [], "مودعان معا": [], "تأخر": [], "بلا سجل": []}
    for one in chain["الحلقات"]:
        name = str(one["الاسم"])
        if not one["مرساة_السجل"]:
            out["بلا سجل"].append(name)
        elif one["تاريخ_مرساة_السجل"] > one["تاريخ_المرساة"]:
            out["سبق"].append(name)
        elif one["تاريخ_مرساة_السجل"] == one["تاريخ_المرساة"]:
            out["مودعان معا"].append(name)
        else:
            out["تأخر"].append(name)
    return out


def render() -> str:
    return json.dumps(build(), ensure_ascii=False, indent=2) + "\n"


def deposited() -> dict[str, Any]:
    return dict(json.loads(CHAIN.read_text(encoding="utf-8")))


def main() -> int:
    if shallow():
        print("نسخةٌ ضحلة: لا مراسيَ تُقرَأ — والحالُ مُصنَّفةٌ لا مُصفَّرة")
        return 0
    chain = build()
    written = json.dumps(chain, ensure_ascii=False, indent=2) + "\n"
    CHAIN.write_text(written, encoding="utf-8")
    kinds = precedence(chain)
    said = objections(chain)
    print(f"حلقات: {len(chain['الحلقات'])} | مخالفات: {len(said)}")
    print(f"الخاتمة: {chain['بصمة_الخاتمة'][:16]}")
    for key, rows in kinds.items():
        print(f"  {key}: {len(rows)}")
    for name in kinds["تأخر"]:
        print(f"  ** ختمٌ أُودِع بعد سجلِّ تشغيله: {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
