"""Canonical Technique Registry.

Technique definitions are reusable strategic methods. They are not strategies
and do not contain investor-specific execution logic.
"""

from models.strategy import TechniqueDefinition

CANONICAL_TECHNIQUES: list[TechniqueDefinition] = undefined;


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
