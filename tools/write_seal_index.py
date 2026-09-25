"""فهرسُ الأختام — **يُشتَقّ من الشجرة** لا يُنسَخ باليد.

لا يُنقَل رقمٌ إلى هذا الفهرس: كلُّ بصمةٍ فيه **تُعاد حسابًا** من شاهدها
وشروطها بـ`seal(…)`، ولا تُكتَب إلّا إن طابقت ثابتًا مكتوبًا في الشجرة.
فالفهرسُ **شهادةُ اتّساقٍ** لا جدولَ نقل.

وما ليس في الفهرس ليس في الشجرة: يحرس ذلك فحصٌ يوجب أن يكون كلُّ ثابتٍ
سداسيٍّ عشريٍّ من أربعٍ وستّين خانةً في `tests/` **مُشتقًّا ومُفهرَسًا**،
أو مُعلَنًا في جدول المستثنيات بسببه.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[1]
TESTS = REPOSITORY / "tests"
INDEX = REPOSITORY / "docs" / "فهرس-الأختام.md"
HEX = re.compile(r"\b[0-9a-f]{64}\b")
SKIPPED = {".git", "__pycache__", ".mypy_cache", ".ruff_cache", ".pytest_cache"}
EASTERN = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


def eastern(one: object) -> str:
    return str(one).translate(EASTERN)


def celled(one: str) -> str:
    """خليّةُ جدولٍ لا يكسرها عمودٌ في نصّها."""

    return one.replace("|", "\\|")


def counted(number: int, one: str, two: str, few: str, many: str) -> str:
    """مطابقةُ المعدود للعدد — واحدٌ ومثنًّى وجمعُ قلّةٍ وتمييزٌ منصوب."""

    if number == 1:
        return one
    if number == 2:
        return two
    if 3 <= number <= 10:
        return f"{eastern(number)} {few}"
    return f"{eastern(number)} {many}"


def _modules() -> list[tuple[Path, Any]]:
    sys.path[:0] = [
        str(REPOSITORY / "src"),
        str(TESTS / "algebra"),
        str(TESTS / "arabic"),
    ]
    found: list[tuple[Path, Any]] = []
    for path in sorted(TESTS.rglob("*.py")):
        if path.name == "__init__.py":
            continue
        spec = importlib.util.spec_from_file_location(path.stem, path)
        if spec is None or spec.loader is None:
            raise SystemExit(f"لا قارئَ لـ{path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[path.stem] = module
        spec.loader.exec_module(module)
        found.append((path, module))
    return found


def _written() -> dict[str, set[str]]:
    """كلُّ بصمةٍ مكتوبةٍ في الشجرة، ومواضعُها."""

    where: dict[str, set[str]] = {}
    for path in sorted(REPOSITORY.rglob("*")):
        if not path.is_file() or any(one in SKIPPED for one in path.parts):
            continue
        if path.suffix not in {".py", ".md", ".log", ".txt", ".sh", ".toml"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for digest in HEX.findall(text):
            where.setdefault(digest, set()).add(str(path.relative_to(REPOSITORY)))
    return where


def _cited(digest: str) -> set[str]:
    """أين يُذكَر الختمُ بمقدّمته القصيرة — الآلةُ والسجلُّ والوثيقةُ والحكم."""

    short = digest[:8]
    seen: set[str] = set()
    for path in sorted(REPOSITORY.rglob("*")):
        if not path.is_file() or any(one in SKIPPED for one in path.parts):
            continue
        if path.suffix not in {".py", ".md", ".log"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if short in text:
            seen.add(str(path.relative_to(REPOSITORY)))
    return seen


def gather() -> list[dict[str, Any]]:
    """كلُّ شاهدٍ وشروطُه، ببصمةٍ **مُعادةِ الحساب** لا منقولة."""

    from algebra.signified import Oracle, Prediction, seal

    written = _written()
    by_digest: dict[str, dict[str, Any]] = {}
    for path, module in _modules():
        values = list(vars(module).items())
        oracles = [(one, two) for one, two in values if isinstance(two, Oracle)]
        bundles = [
            (one, two)
            for one, two in values
            if isinstance(two, tuple)
            and two
            and all(isinstance(item, Prediction) for item in two)
        ]
        for _, oracle in oracles:
            for _, predictions in bundles:
                digest = seal(oracle, predictions)
                if digest not in written:
                    continue
                by_digest.setdefault(
                    digest,
                    {
                        "digest": digest,
                        "name": oracle.name,
                        "source": oracle.source,
                        "count": len(predictions),
                        "marks": [one.identifier for one in predictions],
                        "written": sorted(written[digest]),
                    },
                )
                home = str(path.relative_to(REPOSITORY))
                by_digest[digest].setdefault("modules", set()).add(home)
    rows = sorted(by_digest.values(), key=lambda one: str(one["name"]))
    for row in rows:
        row["cited"] = sorted(_cited(str(row["digest"])))
    return rows


def render() -> str:
    rows = gather()
    lines: list[str] = []
    add = lines.append
    add("# فهرسُ الأختام — ما سُجِّل قبل النظر")
    add("")
    add("**لا رقمَ منقولٌ ههنا**: كلُّ بصمةٍ في هذا الفهرس **أُعيد حسابُها**")
    add("من شاهدها وشروطها، ولم تُكتَب إلّا بعد أن طابقت ثابتًا في الشجرة.")
    add("ويُولَّد الملفُّ بـ`tools/write_seal_index.py`، ويحرس فحصٌ أنّ")
    add("المكتوبَ **مطابقٌ** لما يولّده، وأنّ **لا ختمَ في الشجرة خارجَه**.")
    add("")
    add(
        f"**الجملة**: {eastern(len(rows))} ختمًا، و"
        f"{eastern(sum(int(one['count']) for one in rows))} شرطًا مكتوبًا قبل النظر."
    )
    add("")
    add("| الختم | الشاهد | شروط | يُذكَر في |")
    add("|---|---|---|---|")
    for row in rows:
        digest = str(row["digest"])
        cited = [one for one in row["cited"] if not one.endswith("فهرس-الأختام.md")]
        add(
            f"| `{digest[:8]}…` | {celled(str(row['name']))} "
            f"| {eastern(row['count'])} "
            f"| {counted(len(cited), 'موضعٌ واحد', 'موضعان', 'مواضعَ', 'موضعًا')} |"
        )
    add("")
    add("## تفصيلُ كلّ ختم")
    add("")
    for row in rows:
        digest = str(row["digest"])
        add(f"### `{digest[:8]}…` — {row['name']}")
        add("")
        add(f"- **المصدر**: {row['source']}")
        add(
            f"- **الشروط** ({eastern(row['count'])}): "
            + "، ".join(str(one) for one in row["marks"])
        )
        cited = [one for one in row["cited"] if not one.endswith("فهرس-الأختام.md")]
        add("- **المواضع**:")
        for one in cited:
            add(f"  - `{one}`")
        add("")
    return "\n".join(lines) + "\n"


def main() -> int:
    text = render()
    INDEX.write_text(text, encoding="utf-8")
    print(f"كُتِب {INDEX.relative_to(REPOSITORY)} — {len(text.splitlines())} سطرًا")
    return 0


if __name__ == "__main__":
    sys.exit(main())
