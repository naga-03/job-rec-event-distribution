from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.config import JWT_SECRET, JWT_ALGORITHM

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    print("AUTH HEADER RECEIVED")
    print("TOKEN:", credentials.credentials)

    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        # Map "sub" to "user_id" for consistency
        if "sub" in payload and "user_id" not in payload:
            payload["user_id"] = payload["sub"]
        
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

def require_recruiter(user=Depends(get_current_user)):
    if user.get("user_type") != "recruiter":
        raise HTTPException(status_code=403, detail="Recruiter access required")
    return user

def require_job_seeker(user=Depends(get_current_user)):
    if user.get("user_type") != "job_seeker":
        raise HTTPException(status_code=403, detail="Job seeker access required")
    return user