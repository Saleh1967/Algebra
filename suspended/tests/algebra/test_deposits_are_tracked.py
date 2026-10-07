"""كلُّ سجلٍّ مُودَعٍ **متعقَّبٌ في المستودع** — وإلّا فليس مُودَعًا.

**ما يحرسه**: أنّ ما تقرأه الأختامُ شاهدًا موجودٌ **في التاريخ** لا في
قرصٍ واحدٍ عابر. فسجلٌّ يُقرَأ في فحصٍ وليس متعقَّبًا **يمرُّ عندي ويسقط
عند غيري**، وذلك أسوأُ من السقوط عند الاثنين.

**ولماذا**: `*.log` كان مُهمَلًا في `.gitignore` (سطرُ Django)، فبقيت
**ثلاثةٌ وثلاثون** سجلًّا خارجَ التعقّب، **ولا التزامَ واحدًا في التاريخ
كلِّه مسَّ `deposits/*.log`** — والأختامُ تشتشهد بها. والعطلُ ٢٥.

**وحدُّه**: يحرس **الوجودَ في التعقّب** لا صوابَ ما في السجلّ؛ فسجلٌّ
متعقَّبٌ بأرقامٍ خاطئةٍ يمرُّ عليه. **يردُّ الغيابَ لا الخطأ.**
"""

from __future__ import annotations

import subprocess
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
DEPOSITS = REPOSITORY / "deposits"


def _tracked() -> set[str]:
    done = subprocess.run(
        ["git", "ls-files", "-z", "--", "deposits"],
        capture_output=True,
        cwd=REPOSITORY,
        check=True,
    )
    rows = done.stdout.decode("utf-8").split("\0")
    return {one.split("/", 1)[1] for one in rows if one.startswith("deposits/")}


def test_every_deposited_file_is_tracked() -> None:
    """ما في `deposits/` على القرص هو ما في التاريخ — بلا فضلةٍ منسيّة."""

    present = {one.name for one in DEPOSITS.iterdir() if one.is_file()}
    astray = sorted(present - _tracked())
    assert astray == [], astray


def test_the_logs_are_tracked_in_particular() -> None:
    """والسجلّاتُ خاصّةً — فهي شواهدُ الأختام، وهي التي غابت."""

    logs = {one.name for one in DEPOSITS.glob("*.log")}
    assert len(logs) > 30, len(logs)
    assert logs <= _tracked(), sorted(logs - _tracked())


def test_the_ignore_file_carries_the_exception_by_name() -> None:
    """الاستثناءُ مكتوبٌ في `.gitignore`، ولا يُترَك لإضافةٍ بالقوّة كلَّ مرّة."""

    rules = (REPOSITORY / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert "*.log" in rules
    assert "!deposits/*.log" in rules
    assert rules.index("*.log") < rules.index("!deposits/*.log")
