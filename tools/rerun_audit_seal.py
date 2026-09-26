"""تجميدُ المقابلة: أنّ كلَّ سجلٍّ مودَعٍ **أُعيد من المدوّنة فطابق بتّاً ببتّ**.

`A_RECORD_THAT_FREEZES_A_REPRODUCTION_NOT_A_RESULT`: وسائرُ ما جُمِّد في
هذه الشجرة **نتائجُ**؛ وهذا يُجمِّد **أنّ النتائجَ تُعاد**. فسجلٌّ لا يُعاد
حسابُه يصير أثرًا يُقرَأ رقمُه ولا يُسأل عنه، **والإعادةُ هي الشاهد**.

`THE_CORPUS_IS_NOT_IN_THE_TREE_AND_THAT_IS_SAID`: فعمودُ «المُعاد» في
`rerun_audit.log` **لا يُعاد في البوّابة** — يحتاج المدوّنةَ، وليست ههنا.
فهو **مؤرَّخٌ بيومه**، وجنسُ خلوّه `UNREACHABLE`: فحصُه مُعيَّنٌ ولا تُملَك
مادّتُه. وأمّا عمودُ «المودَع» فيُعاد في **كلّ** بوّابةٍ من الملفّات نفسِها،
وذلك ما يحرسه `verify_against_logs`.

`AND_COVERAGE_IS_AN_INVARIANT_NOT_A_HABIT`: ولا يدخل الشجرةَ سجلُّ تشغيلٍ
لا صفَّ له ههنا — فزيادةُ سجلٍّ بلا تجميدِ بصمته **تردُّ البوّابة**، ولا
تُترَك لتذكُّرٍ.

**ولا بصمةَ كُتِبت بيد**: الصفوفُ مولَّدةٌ من السجلّ المودَع، والسجلُّ
مولَّدٌ من إعادة التشغيل.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Final

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[1]
DEPOSITS: Final[Path] = REPOSITORY / "deposits"
AUDIT_LOG: Final[str] = "rerun_audit.log"

_FIELD_SEPARATOR: Final[str] = "\x1f"
_RECORD_SEPARATOR: Final[str] = "\x1e"
_HEX: Final[str] = "0123456789abcdef"


class RerunAuditError(ValueError):
    """رُدَّ سجلٌّ لا يحمل شكلَ المقابلة، أو فيه مخالفٌ لم يُسمَّ."""


@dataclass(frozen=True, slots=True)
class SealedRerun:
    """مقابلةٌ مُقفَلة: ما أُعيد، وبأيّ مدوّنة، وكم طابق."""

    corpus: str
    corpus_lines: int
    compared: int
    matched: int
    rows: tuple[tuple[str, int, str], ...]
    abridged: tuple[tuple[str, int, int], ...]

    def __post_init__(self) -> None:
        for one in (self.corpus, *(two for _, _, two in self.rows)):
            if len(one) != 64 or set(one) - set(_HEX):
                raise RerunAuditError(f"بصمةٌ ليست sha256: {one}")
        if self.corpus_lines <= 0:
            raise RerunAuditError("مدوّنةٌ بلا أسطر.")
        if self.compared != len(self.rows):
            raise RerunAuditError(f"عُدَّ {self.compared} وفي السجلّ {len(self.rows)} صفًّا.")
        if self.matched != self.compared:
            raise RerunAuditError(
                "سجلٌّ يُجمِّد مقابلةً فيها مخالفٌ — والمخالفُ يُسمّى ولا يُجمَّد."
            )
        names = [one for one, _, _ in self.rows]
        if len(set(names)) != len(names):
            raise RerunAuditError("اسمٌ مكرَّرٌ في الصفوف.")
        if names != sorted(names):
            raise RerunAuditError("الصفوفُ غيرُ مرتّبةٍ — والترتيبُ شرطُ الإعادة.")
        if any(two <= 0 for _, two, _ in self.rows):
            raise RerunAuditError("سجلٌّ بلا بايتات.")
        for name, lines, missing in self.abridged:
            if missing != 0:
                raise RerunAuditError(
                    f"{name}: {missing} سطرًا من المختصَر لا شاهدَ له في الكامل."
                )
            if lines <= 0:
                raise RerunAuditError(f"{name}: مختصَرٌ بلا أسطر.")


FROZEN_RERUN: Final[SealedRerun] = SealedRerun(
    corpus="37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a",
    corpus_lines=6236,
    compared=25,
    matched=25,
    rows=(
        (
            "arabic_token_run.log",
            2702,
            "1bac65d2d938c814ba1c1a69621b949cfac56103ce33a8ad27f537bc1488b02e",
        ),
        (
            "basmala_lifted_run.log",
            1725,
            "921e166a764f1e96a497fa8d8b178a007c09dc9b792ee47ceb46eccc9127cd13",
        ),
        (
            "context_ladder_run.log",
            3880,
            "56056bcc070c8451cd36f4a1827abe5b1cc247ad580d41f8533869b8cbb4885a",
        ),
        (
            "discovered_ascent_run.log",
            4999,
            "bb3499767e47606f87a74040495711b9bbdb94e99bedef86acc6411da56d8fea",
        ),
        (
            "greedy_algebra_run.log",
            2857,
            "c938f1e2986fe766463365bfc6f6a83ee6b80a1681df662db40fe760293a3dd6",
        ),
        (
            "greedy_licence_run.log",
            5664,
            "55df1aa8c8aa6755ffb18db0de51712352174a8ab5cf5a14350c3f40145bcad9",
        ),
        (
            "hasr_audit_run.log",
            3272,
            "f4db4ad597766a58ac25875ce2ce91d447fbf4c7b891772c09b614431c1ed485",
        ),
        (
            "huffman_ascent_run.log",
            8316,
            "4ec84d6a0beecd3c6132c66f168b505f2601e1c971f5beb07aae4d8dcda28642",
        ),
        (
            "lifted_bit_run.log",
            2489,
            "7c5d86bdff465f991c414c019b7b68e6208473ab601dcac91f34d46f88976085",
        ),
        (
            "lumping_barrier_run.log",
            4122,
            "573f9509bb8444ed71fbfed92d148af400625565205a83766803aa8f5f5310bb",
        ),
        (
            "marking_contrast_run.log",
            2661,
            "12743a6449217b35f6b0f8c2f389b2fd3a74889e0dd0e80031d35c6e171e7eb4",
        ),
        (
            "markov_ladder_run.log",
            1986,
            "aba88b38afc14c18d9fd159e536b5047bc4a71db3d0d0404256fa5969d5bf029",
        ),
        (
            "measured_ranking_run.log",
            3951,
            "6de8bba98f9289e481f21bf490456113b524a039a5c9ad38d5b4ea348ef79377",
        ),
        (
            "morph_residue_run.log",
            3194,
            "4f48cb31994928d2469b7e118e3ac957a3b8dc9001ff1ab0bb3e46d603880a0a",
        ),
        (
            "number_ladder_run.log",
            2590,
            "65b893d06ffb7899cd00bb5c81a5a155e4c599dd31b765fbe96056cb4b1c9c67",
        ),
        (
            "pausal_split_run.log",
            7655,
            "4fa8588f04ea03395217cbcb8f190cb9e1a4e683c78394dc47eb10594e558cf1",
        ),
        (
            "praise_blame_run.log",
            3507,
            "0eb078b3aa2a05b69f13f4d1eb2683c5285fc302861217f11ffda42ece6145eb",
        ),
        (
            "separation_rule_run.log",
            1380,
            "60ff64c698c62531be68a839fd066a5dd3c286e8048b9bbbdaed9513c4c41846",
        ),
        (
            "state_cycle_run.log",
            2767,
            "7677e2b30259d7868759dc0f1cb0138c07d50e237f45609f6696f953b6ef77e0",
        ),
        (
            "stirling_greedy_run.log",
            4060,
            "d46c801c6406633ea2ac3167b07c0d0fcf3b488ee5098de87ee80612a5d4735c",
        ),
        (
            "table_consequence_run.log",
            3725,
            "3e26d748a52e2eb4157b9db21136013cf1d75337260de1dde1e4a1c94c1960a4",
        ),
        (
            "temporary_marking_full.log",
            40195,
            "17a9d1554ceaca94406056fc3d5f9631314497587189fa802ca6adcd4d3c912d",
        ),
        (
            "transfer_arrow_run.log",
            2316,
            "6d26453065961266c4649550e88ba6a998e6f42bd2c879c78f8c3dcdafe6fe92",
        ),
        (
            "verse_ending_run.log",
            8168,
            "37e2558e1b5fcb570f01abb27feaa6bd2d81a5334378ee33a05865c5131f26e8",
        ),
        (
            "word_escalation_run.log",
            2682,
            "9190c2d4e4a206d5ea66facac2d02b4842a68cde6c6e3ac7e14a98cfad7389dd",
        ),
    ),
    abridged=(("temporary_marking_run.log", 56, 0),),
)


def record_bytes(record: SealedRerun = FROZEN_RERUN) -> bytes:
    """تسلسلٌ قانونيٌّ للحقول؛ وترتيبُها ترتيبُ تعريفها."""

    rows = [
        f"{one.name}{_FIELD_SEPARATOR}{getattr(record, one.name)}"
        for one in fields(record)
    ]
    return _RECORD_SEPARATOR.join(rows).encode("utf-8")


def rederive_record_digest(record: SealedRerun = FROZEN_RERUN) -> str:
    """بصمةُ السجلّ مُشتَقّةً من حقوله؛ وتبديلُ حقلٍ يُغيّرها."""

    return hashlib.sha256(record_bytes(record)).hexdigest()


RECORD_DIGEST: Final[str] = rederive_record_digest()
"""ختمُ سجلّ المقابلة؛ وبه يُستشهَد بدل النثر."""


def verify_against_logs(record: SealedRerun = FROZEN_RERUN) -> list[str]:
    """تُعاد بصمةُ كلّ ملفٍّ مودَعٍ **الآن** وتُقابَل بالمُجمَّد؛ وما خالف يُسمّى."""

    complaints: list[str] = []
    for name, size, seal in record.rows:
        path = DEPOSITS / name
        if not path.is_file():
            complaints.append(f"سجلٌّ مودَعٌ غائب: {name}")
            continue
        raw = path.read_bytes()
        if len(raw) != size:
            complaints.append(f"{name}: بايتاتُه {len(raw)} والمُجمَّدُ {size}")
        found = hashlib.sha256(raw).hexdigest()
        if found != seal:
            complaints.append(f"{name}: بصمتُه {found[:16]} والمُجمَّدُ {seal[:16]}")
    covered = {one for one, _, _ in record.rows} | {
        one for one, _, _ in record.abridged
    }
    astray = sorted(
        one.name for one in DEPOSITS.glob("*_run.log") if one.name not in covered
    )
    if astray:
        complaints.append(f"سجلُّ تشغيلٍ بلا صفٍّ مُجمَّد: {astray}")
    audit = DEPOSITS / AUDIT_LOG
    if not audit.is_file():
        complaints.append(f"سجلُّ المقابلة غائب: {AUDIT_LOG}")
        return complaints
    text = audit.read_text(encoding="utf-8")
    for row in (
        f"— المدوّنة: {record.corpus} | أسطرٌ {record.corpus_lines}",
        f"— المُقابَل: {record.compared} سجلًّا",
        f"— مطابقٌ بتّاً ببتّ: {record.matched}",
        "— مخالف: 0",
    ):
        if row not in text:
            complaints.append(f"لا شاهدَ في سجلّ المقابلة لـ«{row}»")
    return complaints
