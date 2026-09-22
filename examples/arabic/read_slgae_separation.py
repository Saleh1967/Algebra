"""يُشغِّل صفاتِ SLGAE المولودة على خانات المخرج المُجمَّدة، ويعرض التعارضين."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from alghanem.arabic.slgae_deposit import (  # noqa: E402
    BORN_BLOCKS,
    BORN_SIFA_SPLITS,
    SLGAE_ATTRIBUTION,
    SLGAE_NAMED_RESIDUALS,
    UNREDERIVED_SECTIONS,
    derive_class_readings,
    derive_division_conflict,
    derive_inventory_conflict,
    features_of,
    separation_reading,
)

_DASH: str = "—"


def main() -> None:
    reading = separation_reading()
    print(SLGAE_ATTRIBUTION)
    print(f"بصمةُ الوثيقة = {reading.document_digest}")
    print()

    inventory = derive_inventory_conflict()
    division = derive_division_conflict()
    print(
        f"المفردة: مولودةٌ {inventory.born_letters}، ومُجمَّدةٌ "
        f"{inventory.frozen_letters}؛ وفي المُجمَّد وحدَه: "
        f"{' '.join(inventory.only_in_frozen)}"
    )
    print(
        f"القسمة: كتلٌ مولودةٌ {division.born_blocks}، ومخارجُ مُجمَّدةٌ "
        f"{division.frozen_makharij}، وفئاتُ المواصفة "
        f"{division.specification_categories} — ثلاثةٌ لا تُدمَج"
    )
    print()

    print("الكتلُ المولودة وصفاتُها:")
    for block, chars in BORN_BLOCKS:
        split = next((s for s in BORN_SIFA_SPLITS if s.block == block), None)
        sides = f"{split.side_a} | {split.side_b}" if split else "لا صفةَ مولودة"
        print(f"  {block:<10} {chars:<14} ← {sides}")
    print()

    print("الخانة | حروفُها | الحال | انفرد | تعادل | خارج المفردة")
    print("-" * 74)
    for row in derive_class_readings():
        tied = " / ".join("".join(group) for group in row.tied_groups) or _DASH
        print(
            f"{row.makhraj_rank:>2} | {' '.join(row.letters)} | "
            f"{row.outcome.name:<9} | "
            f"{' '.join(row.separated_letters) or _DASH} | {tied} | "
            f"{''.join(row.letters_outside_born) or _DASH}"
        )
    print()
    print(
        f"المعلَّقُ قبلُ {reading.letters_unresolved_before} = "
        f"محسومٌ {reading.resolved_letters} + متعادلٌ {reading.tied_letters} + "
        f"موقوفٌ {reading.undecided_letters}"
    )
    print()
    print("صفاتُ حرفَين للمقابلة:")
    for letter in ("ط", "ص"):
        print(f"  {letter}: {features_of(letter)}")
    print()
    print(
        f"أبوابُ الوثيقة المُودَعةُ نصًّا وغيرُ المُعادةِ الاشتقاق: {len(UNREDERIVED_SECTIONS)}"
    )
    print()
    for note in SLGAE_NAMED_RESIDUALS:
        print(note)


if __name__ == "__main__":
    main()
