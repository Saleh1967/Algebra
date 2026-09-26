"""تُعاد كلُّ تشغيلةٍ من المدوّنة، ويُقابَل مخرَجُها بالسجلّ المودَع **بتّاً ببتّ**.

**ما يقيسه**: أنّ الأرقامَ المودَعةَ **تُشتَقّ من المدوّنة** لا تُنقَل من
ذاكرةٍ ولا تُحرَّر بيد. والمقابلةُ ببصمة `sha256` على البايتات كلِّها،
لا بسطرٍ يُقرَأ ولا بعينٍ تُجيل.

**ولماذا**: لأنّ سجلًّا مودَعًا قد يصير **أثرًا لا شاهدًا** — يُقرَأ رقمُه
ولا يُعاد حسابُه، فيبقى صادقًا في الشجرة وقد كذب عليه المولّد. فالإعادةُ
**هي** الشاهد.

**وحدُّ ما ههنا مُعلَن**: المدوّنةُ **ليست في الشجرة**، فيُمرَّر مسارُها
ويُقابَل ختمُها. ومن لا مدوّنةَ عنده لا يُشغِّل هذا، **ويقرأ السجلَّ
المودَع مؤرَّخًا بيومه** لا حالًا راهنة. أمّا بصماتُ السجلّات المودَعة
فتُعاد في كلّ بوّابةٍ بلا مدوّنة — وذلك ما يحرسه `test_rerun_audit`.

**والاستدعاءُ مُودَعٌ مع الحكم**: خمسُ تشغيلاتٍ تطلب وسائطَ غيرَ `--text`،
ومن استدعاها بغيرها قرأ **عطلَ استدعاءٍ عطلَ رقمٍ**. فتُكتَب وسائطُها ههنا
كي لا يُعاد ذلك الخطأ.
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
DEPOSITS = REPOSITORY / "deposits"
EXAMPLES = REPOSITORY / "examples" / "rasm"
LOG = DEPOSITS / "rerun_audit.log"
CORPUS_SEAL = "37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a"
CORPUS_LINES = 6_236

# السجلُّ ← (المولّد، وسائطُه الزائدةُ على `--text`)
# و`None` مكانَ `--text` تعني: لا يحتاج المدوّنةَ ألبتّة
RUNS: dict[str, tuple[str, tuple[str, ...], bool]] = {
    "arabic_token": ("run_state_cycle.py", ("--arabic-only",), True),
    "basmala_lifted": ("run_basmala_lifted.py", (), True),
    "context_ladder": ("run_context_ladder.py", (), True),
    "discovered_ascent": ("run_discovered_ascent.py", (), True),
    "greedy_algebra": ("run_greedy_algebra.py", (), True),
    "greedy_licence": ("run_greedy_licence.py", (), True),
    "hasr_audit": (
        "run_hasr_audit.py",
        ("--rule", "deposits/hasr_rule_note.md"),
        False,
    ),
    "huffman_ascent": ("run_huffman_ascent.py", (), True),
    "lifted_bit": ("run_lifted_bit.py", (), True),
    "lumping_barrier": ("run_lumping_barrier.py", (), False),
    "marking_contrast": ("run_marking_contrast.py", (), True),
    "markov_ladder": ("run_markov_ladder.py", (), True),
    "measured_ranking": ("run_measured_ranking.py", (), True),
    "morph_residue": ("run_morph_residue.py", (), True),
    "number_ladder": (
        "run_number_ladder.py",
        ("--rule", "deposits/number_rule_note.md"),
        False,
    ),
    "pausal_split": ("run_pausal_split.py", (), True),
    "praise_blame": (
        "run_praise_blame.py",
        ("--rule", "deposits/praise_blame_rule.md"),
        True,
    ),
    "separation_rule": ("run_separation_rule.py", (), True),
    "state_cycle": ("run_state_cycle.py", (), True),
    "stirling_greedy": (
        "run_stirling_greedy.py",
        (
            "--hasr",
            "deposits/hasr_rule_note.md",
            "--numbers",
            "deposits/number_rule_note.md",
        ),
        False,
    ),
    "temporary_marking": ("run_temporary_marking.py", (), True),
    "transfer_arrow": ("run_transfer_arrow.py", (), True),
    "verse_ending": ("run_verse_ending.py", (), True),
    "word_escalation": ("run_word_escalation.py", (), True),
}

# سجلٌّ مودَعٌ **مختصَرٌ** من كاملٍ مودَعٍ إلى جانبه؛ فيُقابَل المُعادُ
# بالكامل، ويُفحَص أنّ المختصَرَ شريحةُ أسطرٍ منه بلا سطرٍ مفقود
ABRIDGED: dict[str, str] = {"temporary_marking": "temporary_marking_full.log"}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def measure(name: str, corpus: Path) -> dict[str, str]:
    """تُشغَّل واحدةٌ ويُقابَل مخرَجُها — ويُذكَر الحكمُ بلا تلطيف."""

    script, extra, needs_text = RUNS[name]
    order = [sys.executable, str(EXAMPLES / script)]
    if needs_text:
        order += ["--text", str(corpus)]
    order += list(extra)
    done = subprocess.run(order, capture_output=True, cwd=REPOSITORY, check=False)
    if done.returncode != 0:
        tail = done.stderr.decode("utf-8", "replace").strip().splitlines()
        raise SystemExit(f"{name}: رجع {done.returncode} :: {tail[-1] if tail else ''}")
    fresh = done.stdout
    against = DEPOSITS / ABRIDGED.get(name, f"{name}_run.log")
    kept = against.read_bytes()
    row = {
        "name": name,
        "against": against.name,
        "bytes": str(len(kept)),
        "deposited": digest(kept),
        "rederived": digest(fresh),
    }
    row["verdict"] = "مطابق" if row["deposited"] == row["rederived"] else "خالف"
    if name in ABRIDGED:
        brief = (DEPOSITS / f"{name}_run.log").read_text(encoding="utf-8").splitlines()
        whole = set(fresh.decode("utf-8").splitlines())
        row["missing"] = str(sum(1 for one in brief if one not in whole))
        row["brief_lines"] = str(len(brief))
    return row


def render(rows: list[dict[str, str]], corpus_digest: str, lines: int) -> str:
    out: list[str] = []
    add = out.append
    add(f"— المدوّنة: {corpus_digest} | أسطرٌ {lines}")
    add("— حدُّ المقابلة: sha256 على البايتات كلِّها — لا سطرًا ولا عينًا")
    add(f"— المُقابَل: {len(rows)} سجلًّا")
    add("")
    add("  السجلّ | البايتات | بصمةُ المودَع | بصمةُ المُعاد | الحكم")
    for row in rows:
        add(
            f"  {row['name']} | {row['bytes']} | {row['deposited'][:16]} | "
            f"{row['rederived'][:16]} | {row['verdict']}"
        )
    add("")
    matched = [one for one in rows if one["verdict"] == "مطابق"]
    add(f"— مطابقٌ بتّاً ببتّ: {len(matched)}")
    add(f"— مخالف: {len(rows) - len(matched)}")
    add(f"— بايتاتٌ قُوبِلت: {sum(int(one['bytes']) for one in matched)}")
    add("")
    add("— المختصَرُ من كاملٍ مودَعٍ إلى جانبه:")
    for row in rows:
        if "missing" in row:
            add(
                f"    {row['name']}_run.log: {row['brief_lines']} سطرًا، "
                f"قُوبِل بـ{row['against']} — أسطرٌ مفقودةٌ منه {row['missing']}"
            )
    add("")
    add("— الاستدعاءُ كما يجب، ومن خالفه قرأ عطلَ استدعاءٍ عطلَ رقم:")
    for name in sorted(RUNS):
        script, extra, needs_text = RUNS[name]
        args = ("--text <المدوّنة> " if needs_text else "") + " ".join(extra)
        add(f"    {name}: {script} {args}".rstrip())
    return "\n".join(out) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()
    raw = given.text.read_bytes()
    seal = digest(raw)
    if seal != CORPUS_SEAL:
        raise SystemExit(f"مدوّنةٌ غيرُ المختومة: {seal}")
    lines = len(raw.decode("utf-8").splitlines())
    if lines != CORPUS_LINES:
        raise SystemExit(f"أسطرٌ غيرُ المختومة: {lines}")
    rows = [measure(name, given.text) for name in sorted(RUNS)]
    LOG.write_text(render(rows, seal, lines), encoding="utf-8")
    fell = [one["name"] for one in rows if one["verdict"] != "مطابق"]
    print(f"كُتِب {LOG.relative_to(REPOSITORY)} — {len(rows)} سجلًّا")
    print(f"مخالفٌ: {fell if fell else 'لا شيء'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
