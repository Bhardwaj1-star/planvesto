from rules.canonical import CANONICAL_RULES, RuleRole, RuleScope, get_rule, get_rules, validate_rule_registry


def test_canonical_rule_registry_is_valid():
    validate_rule_registry()
    assert CANONICAL_RULES


def test_canonical_rule_lookup_and_filters():
    rule = get_rule("goal-positive-horizon")
    assert rule.scope == RuleScope.GOAL
    assert rule.role == RuleRole.HARD_CONSTRAINT

    strategy_rules = get_rules(scope=RuleScope.STRATEGY)
    assert strategy_rules
    assert all(rule.scope == RuleScope.STRATEGY for rule in strategy_rules)


def test_canonical_rule_ids_are_unique():
    assert len(CANONICAL_RULES) == len(set(CANONICAL_RULES))
