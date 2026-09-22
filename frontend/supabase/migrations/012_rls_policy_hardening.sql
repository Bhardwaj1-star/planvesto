-- RLS policy hardening: scope exposed public policies to authenticated users
-- and avoid per-row auth.uid() evaluation. Ownership predicates are preserved.
do $$
declare
  p record;
  using_expr text;
  check_expr text;
begin
  for p in
    select schemaname, tablename, policyname, cmd, qual, with_check
    from pg_policies
    where schemaname = 'public'
      and (coalesce(qual, '') like '%auth.uid()%' or coalesce(with_check, '') like '%auth.uid()%')
  loop
    execute format(
      'alter policy %I on %I.%I to authenticated',
      p.policyname, p.schemaname, p.tablename
    );

    using_expr := replace(p.qual, 'auth.uid()', '(select auth.uid())');
    check_expr := replace(p.with_check, 'auth.uid()', '(select auth.uid())');

    if p.cmd = 'SELECT' then
      execute format(
        'alter policy %I on %I.%I using (%s)',
        p.policyname, p.schemaname, p.tablename, using_expr
      );
    elsif p.cmd = 'INSERT' then
      execute format(
        'alter policy %I on %I.%I with check (%s)',
        p.policyname, p.schemaname, p.tablename, check_expr
      );
    elsif p.cmd = 'UPDATE' then
      execute format(
        'alter policy %I on %I.%I using (%s) with check (%s)',
        p.policyname, p.schemaname, p.tablename, using_expr, check_expr
      );
    elsif p.cmd = 'DELETE' then
      execute format(
        'alter policy %I on %I.%I using (%s)',
        p.policyname, p.schemaname, p.tablename, using_expr
      );
    elsif p.cmd = 'ALL' then
      execute format(
        'alter policy %I on %I.%I using (%s) with check (%s)',
        p.policyname, p.schemaname, p.tablename, using_expr, check_expr
      );
    end if;
  end loop;
end $$;