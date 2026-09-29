from datetime import datetime,timedelta,timezone
from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from jose import JWTError,jwt
from passlib.context import CryptContext
from .config import settings
pwd=CryptContext(schemes=['bcrypt'],deprecated='auto'); bearer=HTTPBearer(auto_error=False)
def hash_password(v:str)->str:return pwd.hash(v)
def verify_password(v:str,h:str)->bool:return pwd.verify(v,h)
def token(subject:str,role:str)->str:return jwt.encode({'sub':subject,'role':role,'exp':datetime.now(timezone.utc)+timedelta(hours=12)},settings.jwt_secret,algorithm='HS256')
def user(credentials:HTTPAuthorizationCredentials|None=Depends(bearer)):
 if not credentials: raise HTTPException(status_code=401,detail='Authentication required')
 try:return jwt.decode(credentials.credentials,settings.jwt_secret,algorithms=['HS256'])
 except JWTError: raise HTTPException(status_code=401,detail='Invalid or expired token')
def allow(*roles):
 def dependency(current=Depends(user)):
  if current['role'] not in roles: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Insufficient role')
  return current
 return dependency
