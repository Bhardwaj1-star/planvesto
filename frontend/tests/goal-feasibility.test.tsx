import assert from "node:assert/strict";
import test from "node:test";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import GoalFeasibility from "../components/goals/GoalFeasibility";
import { withReturnTo } from "../lib/workflow-navigation";

test("unknown feasibility presents the backend reason and Financial State action", () => {
  const markup = renderToStaticMarkup(createElement(GoalFeasibility, {
    goal: {
      feasibility_status: "unknown",
      feasibility_reason: "Current financial surplus is unavailable.",
      required_monthly_contribution: 0,
      workflow_readiness: {
        status: "blocked",
        process_route: "/investor/goal-planner",
        blockers: [{
          key: "financial_state",
          reason: "Current financial surplus is unavailable.",
          missing_data: [{ label: "Income frequency", route: "/investor/onboarding/income" }],
          next_action: {
            label: "Complete Financial State",
            route: "/investor/financial-state",
          },
        }],
        next_action: {
          label: "Complete Financial State",
          route: "/investor/financial-state",
        },
        return_to: "/investor/goal-planner",
      },
    },
  }));

  assert.match(markup, />Unknown</);
  assert.match(markup, /Current financial surplus is unavailable\./);
  assert.match(markup, /Missing data/);
  assert.match(markup, /Income frequency/);
  assert.match(markup, /href="\/investor\/financial-state\?returnTo=%2Finvestor%2Fgoal-planner"/);
  assert.match(markup, /href="\/investor\/onboarding\/income\?returnTo=%2Finvestor%2Ffinancial-state%3FreturnTo%3D%252Finvestor%252Fgoal-planner"/);
  assert.match(markup, /Complete Financial State/);
});

test("feasible goals do not show a prerequisite action", () => {
  const markup = renderToStaticMarkup(createElement(GoalFeasibility, {
    goal: {
      feasibility_status: "feasible",
      feasibility_reason: "The required monthly contribution fits within the current investable surplus.",
      required_monthly_contribution: 0,
      workflow_readiness: {
        status: "ready",
        process_route: "/investor/goal-planner",
        blockers: [],
        next_action: null,
        return_to: "/investor/goal-planner",
      },
    },
  }));

  assert.match(markup, />Feasible</);
  assert.doesNotMatch(markup, /Complete Financial State/);
});

test("return target is encoded while retaining the existing destination route", () => {
  assert.equal(
    withReturnTo("/investor/financial-state", "/investor/goal-planner?goalId=goal-1"),
    "/investor/financial-state?returnTo=%2Finvestor%2Fgoal-planner%3FgoalId%3Dgoal-1",
  );
});