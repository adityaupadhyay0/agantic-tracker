from enum import Enum
from typing import List, Optional
from fastapi import HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

class UserRole(str, Enum):
    INDIVIDUAL = "individual"
    TEAM_LEAD = "team_lead"
    ADMIN = "admin"

class UserContext(BaseModel):
    user_id: str
    role: UserRole
    teams: List[str] = []

# Simplified Auth Mock
API_KEY_NAME = "X-CORTEX-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_current_user(api_key: str = Security(api_key_header)) -> UserContext:
    """
    Mocks user authentication and RBAC.
    In production, this would validate a JWT/SSO session.
    """
    if not api_key:
        # Default to a mock individual for development
        return UserContext(user_id="dev_user", role=UserRole.INDIVIDUAL, teams=["engineering"])

    if api_key == "admin-key":
        return UserContext(user_id="admin", role=UserRole.ADMIN)
    elif api_key == "lead-key":
        return UserContext(user_id="lead", role=UserRole.TEAM_LEAD, teams=["engineering"])

    return UserContext(user_id="dev_user", role=UserRole.INDIVIDUAL, teams=["engineering"])

def check_scope_access(user: UserContext, scope: str, scope_id: Optional[str] = None):
    """
    Enforces RBAC on BCO scope access.
    """
    if user.role == UserRole.ADMIN:
        return True

    if scope == "individual":
        if scope_id != user.user_id:
             raise HTTPException(status_code=403, detail="You can only access your own individual BCOs")

    if scope == "team":
        if user.role == UserRole.INDIVIDUAL:
             raise HTTPException(status_code=403, detail="Individual contributors cannot access team BCOs")
        if user.role == UserRole.TEAM_LEAD and scope_id not in user.teams:
             raise HTTPException(status_code=403, detail="You do not have access to this team's BCOs")

    if scope == "organization":
        if user.role != UserRole.ADMIN:
             raise HTTPException(status_code=403, detail="Only admins can access organization-wide BCOs")

    return True
