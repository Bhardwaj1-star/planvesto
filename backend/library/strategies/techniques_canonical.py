"""Canonical Technique Registry.

Technique definitions are reusable strategic methods. They are not strategies
and do not contain investor-specific execution logic.
"""

from models.strategy import TechniqueDefinition


CANONICAL_TECHNIQUES: list[TechniqueDefinition] = [
    TechniqueDefinition(technique_id="tech-bucketing", name="Bucketing", description="Separate resources by time or purpose horizon.", purpose="Match liquidity and risk to when money is needed."),
    TechniqueDefinition(technique_id="tech-laddering", name="Laddering", description="Stagger maturities across time periods.", purpose="Create predictable liquidity while reducing reinvestment concentration."),
    TechniqueDefinition(technique_id="tech-glide-path", name="Glide Path", description="Systematically change the strategic mix as a goal approaches.", purpose="Reduce exposure to adverse late-horizon outcomes."),
    TechniqueDefinition(technique_id="tech-cashflow-matching", name="Cash-flow Matching", description="Match expected resources and cash flows to expected goal outflows.", purpose="Improve funding certainty for known future obligations."),
    TechniqueDefinition(technique_id="tech-barbell", name="Barbell / Dumbbell", description="Combine highly defensive and growth-oriented resource buckets.", purpose="Balance resilience and growth without treating every resource identically."),
    TechniqueDefinition(technique_id="tech-asset-earmarking", name="Asset Earmarking", description="Explicitly reserve resources for one defined goal.", purpose="Prevent the same asset from being fully counted toward multiple goals."),
    TechniqueDefinition(technique_id="tech-goal-segmentation", name="Goal Segmentation", description="Separate competing objectives by priority, horizon, and funding need.", purpose="Make resource allocation across multiple goals explicit."),
    TechniqueDefinition(technique_id="tech-contribution-escalation", name="Contribution Escalation", description="Increase future funding contributions according to a defined rule.", purpose="Use rising surplus or income to close a funding gap."),
    TechniqueDefinition(technique_id="tech-tax-efficient-sequencing", name="Tax-Efficient Sequencing", description="Sequence withdrawals or funding sources with tax consequences in mind.", purpose="Improve after-tax goal funding efficiency."),
    TechniqueDefinition(technique_id="tech-tax-loss-harvesting", name="Tax-Loss Harvesting", description="Realise eligible losses to offset gains while maintaining the intended strategic exposure.", purpose="Manage tax drag without changing the strategic objective."),
]


def get_canonical_techniques() -> list[TechniqueDefinition]:
    return list(CANONICAL_TECHNIQUES)


def get_canonical_technique(technique_id: str) -> TechniqueDefinition | None:
    return next((t for t in CANONICAL_TECHNIQUES if t.active and t.technique_id == technique_id), None)


def validate_technique_registry(techniques: list[TechniqueDefinition] | None = None) -> None:
    catalog = techniques if techniques is not None else CANONICAL_TECHNIQUES
    ids = [t.technique_id for t in catalog]
    if len(ids) != len(set(ids)):
        raise ValueError("Canonical Technique Registry contains duplicate technique_id values")
    for technique in catalog:
        if not technique.technique_id.strip():
            raise ValueError("Canonical Technique Registry contains an empty technique_id")
        if not technique.name.strip():
            raise ValueError(f"Technique {technique.technique_id} has an empty name")


validate_technique_registry()
