type DashboardCardProps = {
  title: string;
  value?: string;
  description?: string;
  children?: React.ReactNode;
};

export default function DashboardCard({
  title,
  value,
  description,
  children,
}: DashboardCardProps) {
  return (
    <section className="dashboard-card">
      <div className="dashboard-card-header">
        <div>
          <h2>{title}</h2>

          {description && (
            <p>{description}</p>
          )}
        </div>

        {value && (
          <strong>{value}</strong>
        )}
      </div>

      {children}
    </section>
  );
}