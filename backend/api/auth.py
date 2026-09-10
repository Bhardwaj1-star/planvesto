from fastapi import HTTPException
from data.supabase import get_supabase


def authenticate_user(authorization: str | None) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization token required")
    token = authorization.removeprefix("Bearer ").strip()
    try:
        result = get_supabase().auth.get_user(token)
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid authorization token") from exc
    user = getattr(result, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authorization token")
    return user.id


def verify_planning_unit_ownership(planning_unit_id: str, user_id: str) -> None:
    result = (
        get_supabase()
        .table("planning_units")
        .select("planning_unit_id")
        .eq("planning_unit_id", planning_unit_id)
        .eq("user_id", user_id)
        .maybe_single()
        .execute()
    )
    if not result or not result.data:
        raise HTTPException(
            status_code=403,
            detail="Planning unit does not belong to authenticated user",
        )
