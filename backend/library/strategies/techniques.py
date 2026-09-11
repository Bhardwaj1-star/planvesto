from models.strategy import TechniqueDefinition

TECHNIQUE_CATALOG: list[TechniqueDefinition] = [
    TechniqueDefinition("tech-bucketing", "Bucketing", "Separate resources by time or purpose horizon.", purpose="Match liquidity and risk to when money is needed."),
    TechniqueDefinition("tech-laddering", "Laddering", "Stagger maturities across time periods.", purpose="Create predictable liquidity while reducing reinvestment concentration."),
    TechniqueDefinition("tech-glide-path", "Glide Path", "Systematically change the strategic mix as a goal approaches.", purpose="Reduce exposure to adverse late-horizon outcomes."),
    TechniqueDefinition("tech-cashflow-matching", "Cash-flow Matching", "Match expected resources and cash flows to expected goal outflows.", purpose="Improve funding certainty for known future obligations."),
    TechniqueDefinition("tech-barbell", "Barbell / Dumbbell", "Combine highly defensive and growth-oriented resource buckets.", purpose="Balance resilience and growth without treating every resource identically."),
    TechniqueDefinition("tech-asset-earmarking", "Asset Earmarking", "Explicitly reserve resources for one defined goal.", purpose="Prevent the same asset from being fully counted toward multiple goals."),
    TechniqueDefinition("tech-goal-segmentation", "Goal Segmentation", "Separate competing objectives by priority, horizon, and funding need.", purpose="Make resource allocation across multiple goals explicit."),
    TechniqueDefinition("tech-contribution-escalation", "Contribution Escalation", "Increase future funding contributions according to a defined rule.", purpose="Use rising surplus or income to close a funding gap."),
    TechniqueDefinition("tech-tax-efficient-sequencing", "Tax-Efficient Sequencing", "Sequence withdrawals or funding sources with tax consequences in mind.", purpose="Improve after-tax goal funding efficiency."),
    TechniqueDefinition("tech-tax-loss-harvesting", "Tax-Loss Harvesting", "Realise eligible losses to offset gains while maintaining the intended strategic exposure.", purpose="Manage tax drag without changing the strategic objective."),
]


def get_all_techniques() -> list[TechniqueDefinition]:
    return list(TECHNIQUE_CATALOG)


def get_technique_by_id(technique_id: str) -> TechniqueDefinition | None:
    return next((t for t in TECHNIQUE_CATALOG if t.active and t.technique_id == technique_id), None)
