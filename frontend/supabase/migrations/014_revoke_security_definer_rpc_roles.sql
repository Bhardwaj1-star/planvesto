-- Explicitly revoke EXECUTE from exposed roles. Existing explicit grants are not removed by REVOKE ... FROM PUBLIC alone.
revoke execute on function public.handle_new_user() from anon, authenticated;
revoke execute on function public.rls_auto_enable() from anon, authenticated;
