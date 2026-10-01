from library.strategies.techniques import TECHNIQUE_CATALOG, get_technique_by_id
from library.strategies.techniques_canonical import (
    CANONICAL_TECHNIQUES,
    get_canonical_technique,
    get_canonical_techniques,
    validate_technique_registry,
)


def test_canonical_technique_registry_has_unique_ids():
    ids = [t.technique_id for t in CANONICAL_TECHNIQUES]
    assert ids
    assert len(ids) == len(set(ids))
    validate_technique_registry()


def test_technique_catalog_is_canonical_source_of_truth():
    assert TECHNIQUE_CATALOG is CANONICAL_TECHNIQUES
    assert get_canonical_techniques() == CANONICAL_TECHNIQUES


def test_canonical_technique_lookup():
    technique = get_canonical_technique("tech-bucketing")
    assert technique is not None
    assert technique.name == "Bucketing"
    assert get_technique_by_id("tech-bucketing") == technique
