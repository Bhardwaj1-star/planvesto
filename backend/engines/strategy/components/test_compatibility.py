from .compatibility import are_compatible, incompatible_pairs


def test_funding_and_accumulation_are_compatible():
    assert are_compatible(("component-funding", "component-accumulation"))


def test_credit_and_preservation_are_incompatible():
    assert not are_compatible(("component-credit", "component-preservation"))


def test_unknown_component_is_rejected():
    assert not are_compatible(("component-funding", "component-does-not-exist"))


def test_incompatible_pairs_are_reported():
    assert incompatible_pairs(("component-credit", "component-preservation")) == [
        ("component-credit", "component-preservation")
    ]
