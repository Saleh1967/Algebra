"""النقلُ مُبصَّمٌ: تفريعٌ يتباعد **بإعلان** لا بصمت.

**الاعتراضُ الذي يُجاب ههنا** مكتوبٌ في `src/alghanem/TRANSFER_NOTICE.md`
بخطّ صاحبه قبل النقل: «ونسخُها كلَّها يصنع **تفريعًا يتباعد عن أصله بصمت**،
ثمّ يُستشهَد به بعد جلساتٍ كأنّه الأصل. وكتابةُ `__init__.py` مختصرٍ هنا تصنع
الشيءَ نفسَه بصورةٍ أهدأ».

وهو اعتراضٌ **صحيحٌ في خطره**، والنقلُ وقع بأمرٍ صريح. فالذي يُبطِل الخطرَ
ليس نقضَ الاعتراض بل **آلةٌ تمنع الصمت**: كلُّ ملفٍّ منقولٍ مُبصَّمٌ في
`PORT_MANIFEST.json` بالتزامِ مصدره، وتحريرُ سطرٍ فيه يُسقِط فحصًا باسمه.

`A_FORK_THAT_ANNOUNCES_ITSELF_IS_NOT_THE_FORK_THAT_WAS_FEARED`: فالمخوفُ
تباعدٌ **لا يُعلَن**؛ ومتى صار كلُّ تباعدٍ يُسقِط فحصًا، صار التباعدُ قرارًا
يُتَّخَذ لا حادثةً تقع. والفرقُ بينهما هو الفرقُ بين تفريعٍ ونسخةٍ مُهمَلة.

`SEVEN_AND_THIRTY_COPIED_AND_TWO_WRITTEN_AND_NO_THIRD_CASE`: وسبعةٌ وثلاثون
ملفًّا منقولةٌ **بايتًا ببايت**، وملفّا تهيئةٍ **كُتِبا ههنا** لأنّ نظيرَيهما
يستوردان ما لم يُنقَل. ولا ثالثَ: ملفٌّ في الشجرة ليس في أحد الجدولين يُرَدّ
باسمه، فلا يدخل النقلَ شيءٌ بلا إعلانِ أصله.

`THE_SOURCE_COMMIT_IS_NAMED_SO_THE_DIFFERENCE_IS_COMPUTABLE`: والتزامُ
المصدر مكتوبٌ كاملًا (`22a42b5…`). فمن أراد الفرقَ بين النسختين يومًا **يحسبه
ولا يُقدِّره**: نسخةٌ من ذلك الالتزام، وبصمةٌ ببصمة.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
PORT = REPOSITORY / "src" / "alghanem"
MANIFEST = json.loads((PORT / "PORT_MANIFEST.json").read_text(encoding="utf-8"))


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _modules() -> list[str]:
    return sorted(str(path.relative_to(PORT)) for path in PORT.rglob("*.py"))


def test_every_file_is_either_copied_or_written_here() -> None:
    """جدولان لا غير، ولا ملفَّ خارجَهما — فلا يدخل النقلَ شيءٌ بلا أصلٍ مُعلَن."""

    copied = set(MANIFEST["copied"])
    written = set(MANIFEST["written_here_not_copied"])
    found = set(_modules())

    assert not (copied & written)
    assert found == copied | written, sorted(found ^ (copied | written))
    assert len(copied) == 37
    assert written == {"__init__.py", "arabic/__init__.py"}


def test_no_copied_file_has_drifted_from_its_recorded_digest() -> None:
    """بصمةٌ ببصمة؛ وتحريرُ سطرٍ في منقولٍ يُسقِط هذا الفحصَ باسم ملفّه."""

    drifted = [
        name
        for name, digest in sorted(MANIFEST["copied"].items())
        if _digest(PORT / name) != digest
    ]
    assert not drifted, drifted


def test_the_source_commit_is_named_in_full() -> None:
    """أربعون خانةً ستّةَ عشريّة؛ فالفرقُ يُحسَب ولا يُقدَّر."""

    commit = MANIFEST["source_commit"]
    assert len(commit) == 40
    assert set(commit) <= set("0123456789abcdef")
    assert MANIFEST["source_repository"].endswith("/Alghanem")
    assert MANIFEST["why"].strip()


def test_the_notice_still_carries_the_objection_it_raised() -> None:
    """الاعتراضُ يبقى منصوصًا؛ فالإجابةُ عنه لا تكون بمحوه.

    وهو الموضعُ الذي يُفرِّق بين جوابٍ ومحو: لو حُذِفت الجملةُ لصار السجلُّ
    يقول إنّ أحدًا لم يعترض.
    """

    notice = (PORT / "TRANSFER_NOTICE.md").read_text(encoding="utf-8")
    assert "تفريعًا يتباعد عن أصله بصمت" in notice
    assert "PORT_MANIFEST.json" in notice  # والجوابُ مذكورٌ إلى جانبه


def test_the_two_written_files_are_the_ones_that_could_not_be_copied() -> None:
    """ملفّا التهيئة كُتِبا لأنّ نظيرَيهما يستوردان ما لم يُنقَل، لا لتحسينٍ."""

    for name in MANIFEST["written_here_not_copied"]:
        source = (PORT / name).read_text(encoding="utf-8")
        assert len(source.splitlines()) < 30
        assert "__all__" in source
        # ولا استيرادَ من هذه الشجرة فيهما، وإلّا جرّا ما لم يُنقَل
        assert "from ." not in source
        assert "import alghanem" not in source
