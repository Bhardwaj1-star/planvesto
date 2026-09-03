type Goal = {
  id: string;
  name: string;
  targetAmount: number;
  currentFunding: number;
  targetDate?: string | null;
  priority: string;
};

type CriticalGoalsProps = {
  goals: Goal[];
};

function money(value: number) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value);
}

export default function CriticalGoals({
  goals,
}: CriticalGoalsProps) {
  return (
    <div className="critical-goals">
      {goals.length === 0 ? (
        <div className="dashboard-empty-state">
          <h3>No critical goals yet</h3>
          <p>
            Your important financial goals will appear here.
          </p>
        </div>
      ) : (
        goals.map((goal) => (
          <div
            key={goal.id}
            className="goal-item"
          >
            <div>
              <span className="goal-priority">
                {goal.priority}
              </span>

              <h3>{goal.name}</h3>

              {goal.targetDate && (
                <p>
                  Target:{" "}
                  {new Date(
                    goal.targetDate
                  ).toLocaleDateString("en-IN")}
                </p>
              )}
            </div>

            <div className="goal-amount">
              <strong>
                {money(goal.targetAmount)}
              </strong>

              <span>
                Funded: {money(goal.currentFunding)}
              </span>
            </div>
          </div>
        ))
      )}
    </div>
  );
}