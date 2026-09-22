"""يُشغِّل لعبةَ الصقر والحمامة: مصفوفةٌ، وتوازنٌ مُشتَقّ، ومسارٌ يلتقي به."""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from hawk_dove.game import (  # noqa: E402
    A_PURE_HAWK_POPULATION_IS_STABLE_ONLY_WHEN_FIGHTING_IS_CHEAP_NOTE,
    AN_ESS_IS_NOT_AN_OPTIMUM_NOTE,
    THE_EQUILIBRIUM_IS_DERIVED_NOT_ASSERTED_NOTE,
    THIS_MODEL_CLAIMS_NOTHING_ABOUT_ARABIC_NOTE,
    WHAT_A_LINGUISTIC_READING_WOULD_NEED,
    HawkDoveGame,
    Strategy,
)

_CASES: tuple[tuple[int, int], ...] = ((2, 10), (50, 100), (9, 10), (10, 2))


def main() -> None:
    game = HawkDoveGame(value=Fraction(2), cost=Fraction(10))
    print(f"مصفوفةُ العوائد عند V={game.value} و C={game.cost}:")
    print("            صقر     حمامة")
    for own in Strategy:
        row = "  ".join(f"{str(game.payoff(own, other)):>6}" for other in Strategy)
        label = "صقر  " if own is Strategy.HAWK else "حمامة"
        print(f"  {label}  {row}")
    print()

    print("V | C | نسبةُ الصقور | الجنس | متوسّطُ العائد | مجتمعُ الحمائم | الفرق")
    print("-" * 78)
    for value, cost in _CASES:
        current = HawkDoveGame(value=Fraction(value), cost=Fraction(cost))
        equilibrium = current.equilibrium()
        print(
            f"{value:>2} | {cost:>3} | {str(equilibrium.hawk_share):>6} "
            f"({float(equilibrium.hawk_share):.3f}) | {equilibrium.kind.name:<9} | "
            f"{str(equilibrium.mean_payoff):>7} | "
            f"{str(equilibrium.all_dove_payoff):>6} | "
            f"{str(equilibrium.optimality_gap):>6}"
        )
    print()

    target = float(game.equilibrium().hawk_share)
    for start in (0.02, 0.90):
        path = game.simulate(start, 600, 0.5)
        marks = ", ".join(f"{path[index]:.4f}" for index in (0, 5, 20, 100, 599))
        print(f"من {start:.2f}: {marks}  ← التوازن {target:.4f}")
    print()

    print(THE_EQUILIBRIUM_IS_DERIVED_NOT_ASSERTED_NOTE)
    print(AN_ESS_IS_NOT_AN_OPTIMUM_NOTE)
    print(A_PURE_HAWK_POPULATION_IS_STABLE_ONLY_WHEN_FIGHTING_IS_CHEAP_NOTE)
    print(THIS_MODEL_CLAIMS_NOTHING_ABOUT_ARABIC_NOTE)
    print()
    print("ما يلزم قبل قراءتها نموذجًا لظاهرةٍ لغويّة:")
    for requirement in WHAT_A_LINGUISTIC_READING_WOULD_NEED:
        print(f"  • {requirement}")


if __name__ == "__main__":
    main()
