import jwt
from utilities.jwt_utility import SECRET_KEY, ALGORITHM
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Callable

security = HTTPBearer()

# Function to verify the JWT


def verify_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("can_access") is not True:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )
        payload["token"] = token
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
        )

# Dependency to get the token and verify it


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    return verify_jwt(token.credentials)
