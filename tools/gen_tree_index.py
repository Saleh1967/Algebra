"""الشجرةُ المرخَّصة: كلُّ ملفٍّ في هذا المستودع مقسومٌ قسمةً تامّةً بالبصمة، مقارنًا بالغانم المثبَّت (ADR ٢).

لا يقرأ هذا المولِّدُ نصًّا: يقرأ من git أسماءَ الملفّات وبصماتِها (`git ls-files -s`، و`git ls-tree` للغانم) فقط.
لكلّ ملفٍّ عددُه = بصمتُه (blob)، وصنفٌ واحدٌ لا غير بترتيبٍ معلَنٍ لا يُبدَّل:

0. `فارغ` — بلا محتوى (بصمةُ الملفّ الفارغ): لا أصلَ له ولا هو نسخةٌ من شيء، فلا يُعدّ زائدة.
1. `مطابق_للغانم` — بصمتُه في الغانم المثبَّت بعينها: زائدةٌ هنا، أصلُها في الغانم (المرجعُ الوحيد).
2. `مكرر_داخلي` — بصمتُه تتكرّر هنا: الأصلُ أوّلُ مسارٍ بالترتيب، والباقي زائدةٌ تشير إليه.
3. `مختلف_عن_الغانم` — اسمُه في الغانم وبصمتُه غيرُها: نسختان افترقتا.
4. `معلق` — تحت `suspended/` (سجلُّه `SUSPENDED_REGISTRY.json`).
5. `بقية` — حيٌّ فريدٌ لا هذا ولا ذاك: بقيّةٌ للتفسير، لا «مرخَّص» (لا ترخيصَ بلا بوّابة).

الأوّلُ أوّلًا: ما وقع في صنفٍ لا يُنظر له فيما بعده. مخرجاه (`TREE_INDEX.md`، `docs/tree/tree.json`) خارج الجرد
باسمهما، وإلّا تغيّرت بصمتُهما بتوليدهما. التشغيل بعد `git add` (الجردُ من الفهرس):
`python3 tools/gen_tree_index.py` يولّد، و`--check` يطابق، و`--refresh-alghanem DIR REV` يجدّد مودَعَ الغانم.
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from collections.abc import Iterable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "TREE_INDEX.md"
DATA = ROOT / "docs" / "tree" / "tree.json"
ALGHANEM = ROOT / "deposits" / "alghanem-tree.json"
OUTPUTS = ("TREE_INDEX.md", "docs/tree/tree.json")
CLASSES = ("فارغ", "مطابق_للغانم", "مكرر_داخلي", "مختلف_عن_الغانم", "معلق", "بقية")
EMPTY = "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"  # بصمةُ الملفّ الفارغ في git

Entry = tuple[str, str]  # (المسار، البصمة)


def classify(here: Iterable[Entry], alghanem: Iterable[Entry]) -> list[dict[str, str]]:
    """القسمةُ التامّة: لكلّ ملفٍّ صنفٌ واحد، وللزائدة أصلُها. دالّةٌ نقيّة بلا قراءة."""

    rows = sorted(here)
    g_blobs = {b for _, b in alghanem}
    g_paths = dict(alghanem)
    first: dict[str, str] = {}
    for p, b in rows:
        first.setdefault(b, p)
    count = Counter(b for _, b in rows)
    out: list[dict[str, str]] = []
    for p, b in rows:
        if b == EMPTY:
            cls, origin = "فارغ", ""
        elif b in g_blobs:
            cls, origin = "مطابق_للغانم", "alghanem"
        elif count[b] > 1 and first[b] != p:
            cls, origin = "مكرر_داخلي", first[b]
        elif p in g_paths:
            cls, origin = "مختلف_عن_الغانم", "alghanem"
        elif p.startswith("suspended/"):
            cls, origin = "معلق", ""
        else:
            cls, origin = "بقية", ""
        out.append({"path": p, "blob": b, "class": cls, "origin": origin})
    return out


def verify(rows: list[dict[str, str]], here: Iterable[Entry]) -> list[str]:
    """شروطُ التمام: كلُّ ملفٍّ مرّةً بصنفٍ معلَن، وكلُّ زائدةٍ داخليّةٍ أصلُها ملفٌّ حاضرٌ ببصمتها نفسِها."""

    errs: list[str] = []
    paths = dict(here)
    seen = Counter(r["path"] for r in rows)
    if set(seen) != set(paths):
        errs.append("FILE_WITHOUT_CLASS")
    if any(n > 1 for n in seen.values()):
        errs.append("FILE_IN_TWO_CLASSES")
    for r in rows:
        if r["class"] not in CLASSES:
            errs.append(f"UNDECLARED_CLASS:{r['path']}")
        if r["class"] == "مكرر_داخلي" and (
            r["origin"] == r["path"] or paths.get(r["origin"]) != r["blob"]
        ):
            errs.append(f"DUPLICATE_WITHOUT_ORIGIN:{r['path']}")
    return errs


def _git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True,
                          text=True).stdout


def inventory() -> list[Entry]:
    """الجردُ من الفهرس، بلا مخرجَي المولِّد."""

    out: list[Entry] = []
    for line in _git("ls-files", "-s", "-z").split("\0"):
        if not line:
            continue
        meta, path = line.split("\t", 1)
        if path not in OUTPUTS:
            out.append((path, meta.split()[1]))
    return out


def summary(rows: list[dict[str, str]], rev: str) -> dict[str, object]:
    by = Counter(r["class"] for r in rows)
    tops: dict[str, Counter[str]] = {c: Counter() for c in CLASSES}
    for r in rows:
        tops[r["class"]][r["path"].split("/", 1)[0]] += 1
    return {
        "alghanem_rev": rev,
        "total": len(rows),
        "classes": {c: by[c] for c in CLASSES},
        "by_top": {c: dict(sorted(tops[c].items(), key=lambda kv: (-kv[1], kv[0])))
                   for c in CLASSES},
        "distinct_blobs": len({r["blob"] for r in rows}),
    }


def render(s: dict[str, object]) -> str:
    cls = s["classes"]
    assert isinstance(cls, dict)
    total = s["total"]
    assert isinstance(total, int)
    by_top = s["by_top"]
    assert isinstance(by_top, dict)
    lines = [
        "# الشجرةُ المرخَّصة — Algebra مقسومًا بالبصمة ومقارنًا بالغانم",
        "",
        "مولَّدٌ بـ`python3 tools/gen_tree_index.py`؛ لا يُحرَّر باليد، و`--check` في CI يطابقه (ADR ٢). "
        f"الغانم مثبَّتٌ بإيداعه `{s['alghanem_rev']}` (`deposits/alghanem-tree.json`). "
        "لا يُقرأ نصّ: أسماءٌ وبصماتٌ من git فقط.",
        "",
        f"**{total} ملفًّا، {s['distinct_blobs']} بصمةً متميّزة؛ القسمةُ تامّة: كلُّ ملفٍّ في صنفٍ واحد.**",
        "",
        "| الصنف | العدد | النسبة |",
        "|---|---|---|",
    ]
    for c in CLASSES:
        n = cls[c]
        lines.append(f"| `{c}` | {n} | {100 * n / total:.1f}% |")
    lines += ["", "## الأصنافُ بالمجلّد الأعلى", ""]
    for c in CLASSES:
        tops = by_top[c]
        if tops:
            cells = "، ".join(f"`{k}` {v}" for k, v in list(tops.items())[:12])
            lines.append(f"- `{c}`: {cells}")
    lines += [
        "",
        "## ما يقوله الرقم — باسمه",
        "",
        "- `فارغ` بلا محتوى: لا يُعدّ نسخةً ولا زائدة، وإلّا تضخّم المكرَّرُ ببصمةٍ واحدة.",
        "- `مطابق_للغانم` زائدةٌ هنا بالبصمة: الأصلُ في الغانم، والنقلُ إليه قد تمّ لهذه الملفّات بعينها.",
        "- `مختلف_عن_الغانم` نسختان افترقتا بالاسم نفسِه: أيُّهما الأصلُ قرارٌ لا يحسمه المولِّد.",
        "- `بقية` ليست «مرخَّصة»: حيّةٌ فريدةٌ لم تدخل من البوّابة ولم تُعلَّق — للتفسير أو للتعليق.",
        "- الجدولُ الكامل لكلّ ملفٍّ (مسارُه، بصمتُه، صنفُه، أصلُه) في `docs/tree/tree.json`.",
        "",
    ]
    return "\n".join(lines)


def build() -> tuple[str, str, list[str]]:
    dep = json.loads(ALGHANEM.read_text(encoding="utf-8"))
    g = [(p, b) for p, b in dep["files"]]
    here = inventory()
    rows = classify(here, g)
    errs = verify(rows, here)
    s = summary(rows, dep["rev"])
    data = json.dumps({**s, "files": rows}, ensure_ascii=False, indent=0, sort_keys=True) + "\n"
    return render(s), data, errs


def refresh_alghanem(repo: str, rev: str) -> None:
    files: list[list[str]] = []
    for line in _git("ls-tree", "-r", "-z", rev, cwd=Path(repo)).split("\0"):
        if line:
            meta, path = line.split("\t", 1)
            kind, blob = meta.split()[1:3]
            if kind == "blob":
                files.append([path, blob])
    full = _git("rev-parse", rev, cwd=Path(repo)).strip()
    ALGHANEM.write_text(json.dumps({"repo": "Saleh1967/Alghanem", "rev": full, "files": files},
                                   ensure_ascii=False, indent=0) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    if argv[:1] == ["--refresh-alghanem"]:
        refresh_alghanem(argv[1], argv[2])
        return 0
    index, data, errs = build()
    if errs:
        sys.stderr.write("\n".join(errs) + "\n")
        return 1
    if argv[:1] == ["--check"]:
        stale = [p for p, want in ((INDEX, index), (DATA, data))
                 if not p.exists() or p.read_text(encoding="utf-8") != want]
        if stale:
            sys.stderr.write("TREE_INDEX_STALE: شغّل tools/gen_tree_index.py\n")
            return 1
        sys.stdout.write("TREE_INDEX.md مطابق\n")
        return 0
    DATA.parent.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(index, encoding="utf-8")
    DATA.write_text(data, encoding="utf-8")
    sys.stdout.write("كُتب TREE_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
