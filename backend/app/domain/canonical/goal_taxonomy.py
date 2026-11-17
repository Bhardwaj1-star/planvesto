"""
Chapter 03 — Canonical Identity, Categories & Goal Taxonomy
Canonical Goal Catalogue (§2)

Non-negotiable invariants:
1. Exactly ten canonical goal types and IDs.
2. Stable identity: canonical IDs are distinct from display names, custom labels and contextual details.
3. Child Education is contextual detail under goal_education, not a separate canonical type or alias.
4. An investor-provided custom name describes a goal instance while canonical type remains goal_others.
5. Goal priority is a separate decision input, not part of canonical identity.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class CanonicalGoalId(str, Enum):
    RETIREMENT = "goal_retirement"
    MARRIAGE = "goal_marriage"
    VEHICLE = "goal_vehicle"
    DREAM_HOME = "goal_dream_home"
    EDUCATION = "goal_education"
    VACATION = "goal_vacation"
    DEBT_FREEDOM = "goal_debt_freedom"
    WEALTH_CREATION = "goal_wealth_creation"
    FIRE_PASSIVE_INCOME = "goal_fire_passive_income"
    OTHERS = "goal_others"


@dataclass(frozen=True)
class GoalTaxonomyDefinition:
    id: CanonicalGoalId
    display_name: str
    definition: str
    contextual_guidance: str


CANONICAL_GOAL_DEFINITIONS: Dict[CanonicalGoalId, GoalTaxonomyDefinition] = {
    CanonicalGoalId.RETIREMENT: GoalTaxonomyDefinition(
        id=CanonicalGoalId.RETIREMENT,
        display_name="Retirement",
        definition="Plan for financial needs and living expenses after retirement.",
        contextual_guidance="Expected retirement timing, post-retirement expenses and income needs.",
    ),
    CanonicalGoalId.MARRIAGE: GoalTaxonomyDefinition(
        id=CanonicalGoalId.MARRIAGE,
        display_name="Marriage",
        definition="Plan for expenses associated with a marriage or wedding.",
        contextual_guidance="Who the goal is for, event date and cost details.",
    ),
    CanonicalGoalId.VEHICLE: GoalTaxonomyDefinition(
        id=CanonicalGoalId.VEHICLE,
        display_name="Vehicle",
        definition="Build funding for purchasing a vehicle.",
        contextual_guidance="Vehicle type, new/used preference and purchase details.",
    ),
    CanonicalGoalId.DREAM_HOME: GoalTaxonomyDefinition(
        id=CanonicalGoalId.DREAM_HOME,
        display_name="Dream Home",
        definition="Build funding to acquire a home or residential property.",
        contextual_guidance="Location, property details and purchase-related context.",
    ),
    CanonicalGoalId.EDUCATION: GoalTaxonomyDefinition(
        id=CanonicalGoalId.EDUCATION,
        display_name="Education",
        definition="Plan for education-related expenses for the investor or a designated beneficiary.",
        contextual_guidance="Beneficiary and education-related details. Child Education remains contextual detail, not a separate canonical type or alias.",
    ),
    CanonicalGoalId.VACATION: GoalTaxonomyDefinition(
        id=CanonicalGoalId.VACATION,
        display_name="Vacation",
        definition="Plan for costs associated with a holiday or leisure trip.",
        contextual_guidance="Trip type, destination and frequency.",
    ),
    CanonicalGoalId.DEBT_FREEDOM: GoalTaxonomyDefinition(
        id=CanonicalGoalId.DEBT_FREEDOM,
        display_name="Debt Freedom",
        definition="Plan to repay outstanding liabilities and achieve debt freedom.",
        contextual_guidance="Reference to the liability selected for repayment.",
    ),
    CanonicalGoalId.WEALTH_CREATION: GoalTaxonomyDefinition(
        id=CanonicalGoalId.WEALTH_CREATION,
        display_name="Wealth Creation",
        definition="Build long-term wealth through accumulation of assets or an investment corpus.",
        contextual_guidance="Target corpus, time horizon and funding details.",
    ),
    CanonicalGoalId.FIRE_PASSIVE_INCOME: GoalTaxonomyDefinition(
        id=CanonicalGoalId.FIRE_PASSIVE_INCOME,
        display_name="FIRE / Passive Income / Financial Freedom",
        definition="Build sufficient assets or income to achieve financial independence and reduce or remove dependence on employment.",
        contextual_guidance="Target financial-independence age, desired income and work-dependence preference.",
    ),
    CanonicalGoalId.OTHERS: GoalTaxonomyDefinition(
        id=CanonicalGoalId.OTHERS,
        display_name="Others",
        definition="Represent a personal financial goal that does not fit any other approved goal type.",
        contextual_guidance="Investor-provided custom name and description while the canonical type remains goal_others.",
    ),
}


def get_canonical_goal_definition(goal_id: CanonicalGoalId | str) -> Optional[GoalTaxonomyDefinition]:
    """Retrieve canonical definition for a given canonical goal ID."""
    if isinstance(goal_id, str):
        try:
            goal_id = CanonicalGoalId(goal_id)
        except ValueError:
            return None
    return CANONICAL_GOAL_DEFINITIONS.get(goal_id)


def is_valid_canonical_goal_id(goal_id: str) -> bool:
    """Check if the provided string is an approved Chapter 03 canonical goal ID."""
    return any(goal_id == g.value for g in CanonicalGoalId)
