from . import models
from passlib.context import CryptContext
from src.entities.user import User
from sqlalchemy.orm import Session
import jwt
from uuid import UUID
from dotenv import load_dotenv
from datetime import timedelta,timezone,datetime
import os
from fastapi.security import OAuth2PasswordRequestForm

load_dotenv()

secret_key = os.getenv('secretkey')
algorithm = os.getenv('algorithm')
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

# fungsi pembantu
# fungsi hashing password
def hash_password(password:str)->str:
    return bcrypt_context.hash(password)

# fungsi membandingkan password dan hashed password
def verify_password(plain_password:str, hash_password:str)-> bool:
    return bcrypt_context.verify(plain_password,hash_password)

# fungsi buat refresh dan access token baru
def create_new_token(username:str, user_id:UUID, role:str)->models.TokenData:
    payload_access_token={
        'username':username,
        'sub':str(user_id),
        'role':role,
        'exp':datetime.now(timezone.utc)+timedelta(hours=1)
    }
    payload_refresh_token={
        'username':username,
        'sub':str(user_id),
        'role':role,
        'exp':datetime.now(timezone.utc)+timedelta(days=1)
    }
    access_token = jwt.encode(payload_access_token,secret_key,algorithm)
    refresh_token = jwt.encode(payload_refresh_token,secret_key,algorithm)
    token = models.TokenData(
        access_token=access_token,
        refresh_token=refresh_token
    )
    return token

# fungsi verify token
def verify_token(token:str)->models.PayloadToken:
    return jwt.decode(token,secret_key,algorithm)

# fungsi utama
# fungsi register user baru
def register_new_user(data:models.RequestRegisterData,db:Session)->None:
    hashed_password = hash_password(data.password)
    user = User(
        username=data.username,
        email=data.email,
        password =hashed_password
    )
    db.add(user)
    db.commit()

# fungsi login user
def login_user(form_data:OAuth2PasswordRequestForm,db:Session)->models.TokenData:
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password,user.password):
        return print('password atau username salah')
    token = create_new_token(user.username,user.id,user.role.value)
    return token

# fungsi refresh token
def get_new_token(refresh_token:str)->models.TokenData:
    payload = verify_token(refresh_token)
    if not payload or payload.exp < datetime.now(timezone.utc):
        return print("refresh token invalid")
    new_token = create_new_token(payload.username,payload.sub,payload.role)
    return new_token