from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from services.dashboard_service import get_dashboard


router = APIRouter(
    prefix="/api/investor",
    tags=["Investor Dashboard"],
)

security = HTTPBearer()


def get_access_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    return credentials.credentials


@router.get("/dashboard")
def dashboard(
    access_token: str = Depends(get_access_token),
):
    try:
        return get_dashboard(access_token)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )