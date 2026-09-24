"""استقبالُ المدوّنات عن جارتها: بصمةٌ تُطابَق قبل النقل، ولا بايتةَ تُودَع ههنا.

**العطلُ الذي تعالجه هذه الأداة**: فحوصٌ تتخطّى لغياب متنٍ، ومتنٌ موجودٌ في
الشجرة المجاورة (`Saleh1967/Alghanem`). فكان الوصلُ بينهما **يدًا في كلّ
جلسة**: تُنسَخ فيعمل، وتُنسى فيتخطّى. وهذا العملُ اليدويُّ هو نفسُه العيبُ
الذي نُسمّيه في القياس — مجالٌ لم يُعدَّد — إذ لا يُعرَف من الشجرة أيُّ
بايتاتٍ دخلتها ولا من أين.

`THE_INTAKE_IS_A_DECLARED_TABLE_NOT_A_COPY_COMMAND`: فالمستقبَلاتُ **مسرودةٌ
ههنا** باسمها ومصدرها ومقصدها وطولها وبصمتها. وما ليس في الجدول لا يُستقبَل،
وما في الجدول لا يُنقَل حتّى يُطابق الطولَ والبصمةَ معًا. فنسخةٌ أخرى من
الملفّ نفسِه اسمًا **تُرَدّ**، وهذا هو الفرقُ بين استقبالٍ ونسخ.

`THE_BYTES_ARE_NEVER_DEPOSITED_IN_THE_CODE_TREE`: والمقصدُ مستثنًى في
`.gitignore` بقرارٍ مُعلَن: شجرةُ الشفرة لا تحمل مدوّنة. فالاستقبالُ **يُعاد
في كلّ جلسة** ولا يُثبَّت، والمصدرُ يبقى حيث هو.

`A_DESTINATION_THAT_ALREADY_HOLDS_OTHER_BYTES_IS_NOT_OVERWRITTEN_SILENTLY`:
ومقصدٌ فيه ملفٌّ مخالفُ البصمة يُوقِف الاستقبالَ ويُسمّي الخلاف، ولا يُكتَب
فوقه إلّا بـ`--replace` مُعلَنة. وملفٌّ موافقُ البصمة يُترَك كما هو ويُقال
إنّه كان حاضرًا.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Final

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[1]

SOURCE_ROOT_VARIABLE: Final[str] = "ALGEBRA_INTAKE_SOURCE_ROOT"
"""متغيّرُ البيئة الذي يُصرَّح فيه بجذر الشجرة المصدر؛ ولا يُخمَّن موضعُها."""


class IntakeError(ValueError):
    """رُدَّ استقبالٌ لغياب مصدرٍ أو لمخالفة بصمةٍ أو طول."""


@dataclass(frozen=True, slots=True)
class Intake:
    """مستقبَلٌ مُعلَن: من أين، وإلى أين، وبأيّ طولٍ وبصمة."""

    name: str
    source_relative: str
    destination_relative: str
    byte_length: int
    sha256_hex: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise IntakeError("مستقبَلٌ بلا اسمٍ لا يُسرَد.")
        if self.byte_length <= 0:
            raise IntakeError(f"«{self.name}»: طولٌ غيرُ موجبٍ ليس طولًا.")
        if len(self.sha256_hex) != 64 or set(self.sha256_hex) - set("0123456789abcdef"):
            raise IntakeError(f"«{self.name}»: البصمةُ أربعٌ وستّون خانةً ستّةَ عشريّة.")

    def destination(self, into: Path | None = None) -> Path:
        """المقصدُ داخل شجرةٍ مُسمّاة؛ وجذرُ هذا المستودع افتراضُه."""

        return (REPOSITORY if into is None else into) / self.destination_relative


INTAKES: Final[tuple[Intake, ...]] = (
    Intake(
        name="جدولُ الجذور (مقاييس)",
        source_relative="maqayis_by_root_csv_999.csv",
        destination_relative="maqayis_by_root_csv_999.csv",
        byte_length=5_539_405,
        sha256_hex="2c6000bd47797e183294b89da77df4ddfd27921ea595c6071ba52299c382ccb0",
    ),
    Intake(
        name="المصحف (الرسمُ المُجمَّد)",
        source_relative="corpora/quran-simple-enhanced.txt",
        destination_relative="corpora/quran-simple-enhanced.txt",
        byte_length=1_319_901,
        sha256_hex="37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a",
    ),
)
"""الجدولُ المُعلَن. والثاني **لم يُودَع في الشجرة المصدر بعد**، فاستقبالُه
يُرَدّ بغياب المصدر لا بمخالفة بصمة — وذلك فرقٌ يُقرَأ في المخرَج."""


def digest_of(path: Path) -> str:
    """بصمةُ ملفٍّ موجود؛ وتُحسَب من بايتاته لا من اسمه."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_root(declared: Path | str | None = None) -> Path:
    """جذرُ الشجرة المصدر: المُصرَّحُ، وإلّا متغيّرُ البيئة — ولا ثالثَ يُخمَّن."""

    if declared is not None:
        return Path(declared)
    from_environment = os.environ.get(SOURCE_ROOT_VARIABLE)
    if from_environment:
        return Path(from_environment)
    raise IntakeError(
        "جذرُ الشجرة المصدر يُصرَّح به بـ`--source-root` أو في "
        f"`{SOURCE_ROOT_VARIABLE}`؛ ولا يُخمَّن موضعُ مدوّنة."
    )


def verify(path: Path, intake: Intake) -> None:
    """طابِق الطولَ ثمّ البصمة؛ والموافقةُ في أحدهما لا تُغني عن الآخر."""

    if not path.is_file():
        raise IntakeError(f"«{intake.name}»: لا ملفَّ في {path}.")
    size = path.stat().st_size
    if size != intake.byte_length:
        raise IntakeError(
            f"«{intake.name}»: الطولُ {size} والمُعلَنُ {intake.byte_length}؛ "
            "فهما ملفّان لا ملفّ."
        )
    seen = digest_of(path)
    if seen != intake.sha256_hex:
        raise IntakeError(
            f"«{intake.name}»: البصمةُ {seen[:12]}… والمُعلَنةُ "
            f"{intake.sha256_hex[:12]}…؛ ولا يُبنى على المخالفة."
        )


def receive(
    intake: Intake, root: Path, *, into: Path | None = None, replace: bool = False
) -> str:
    """استقبِل مستقبَلًا واحدًا وأرجِع سطرَ خبره؛ ولا يُكتَب فوق مخالفٍ صامتًا."""

    source = root / intake.source_relative
    verify(source, intake)

    destination = intake.destination(into)
    if destination.is_file():
        if destination.stat().st_size == intake.byte_length and (
            digest_of(destination) == intake.sha256_hex
        ):
            return f"حاضرٌ سلفًا: {intake.name} ({intake.sha256_hex[:8]}…)"
        if not replace:
            raise IntakeError(
                f"«{intake.name}»: في المقصد بايتاتٌ مخالفةٌ للبصمة؛ "
                "ولا يُكتَب فوقها إلّا بـ`--replace` مُعلَنة."
            )
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    verify(destination, intake)
    return (
        f"استُقبِل: {intake.name} ← {intake.destination_relative} "
        f"({intake.byte_length} بايتًا · {intake.sha256_hex[:8]}…)"
    )


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="استقبالُ مدوّنةٍ من الشجرة المجاورة ببصمتها"
    )
    parser.add_argument("--source-root", default=None)
    parser.add_argument("--only", default=None, help="اسمُ مستقبَلٍ واحدٍ من الجدول")
    parser.add_argument("--replace", action="store_true")
    return parser


def run(arguments: argparse.Namespace) -> list[str]:
    """شغِّل الاستقبالَ واطبع سطرًا لكلّ مستقبَل — ناجحًا كان أو مردودًا."""

    root = source_root(arguments.source_root)
    if not root.is_dir():
        raise IntakeError(f"جذرُ الشجرة المصدر ليس مجلَّدًا: {root}")
    wanted = [
        one for one in INTAKES if arguments.only is None or one.name == arguments.only
    ]
    if not wanted:
        raise IntakeError(f"لا مستقبَلَ باسم «{arguments.only}» في الجدول.")
    lines: list[str] = []
    for intake in wanted:
        try:
            lines.append(receive(intake, root, replace=arguments.replace))
        except IntakeError as refused:
            lines.append(f"رُدَّ: {refused}")
    return lines


def main() -> None:
    for line in run(build_argument_parser().parse_args()):
        print(line)


if __name__ == "__main__":
    main()
