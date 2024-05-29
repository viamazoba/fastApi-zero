from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel):
    user_name: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "tesla": {
        "user_name": "tesla",
        "full_name": "Juan Camilo",
        "email": "jc@gmail.co",
        "disabled": False,
        "password": "1234"
    },
    "mongo": {
        "user_name": "mongo",
        "full_name": "Juan Esteban",
        "email": "je@gmail.co",
        "disabled": True,
        "password": "7894"
    }
}


def search_user(user_name: str):
    if user_name in users_db:
        return User(**users_db[user_name])


def search_user_db(user_name: str):
    if user_name in users_db:
        return UserDB(**users_db[user_name])


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Auth credentials invalid", headers={"WWW-Authenticate": "Bearer"})
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Inactive user")
    return user


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail='User not found')

    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail='Invalid password')

    return {
        "access_token": user.user_name,
        "token_type": "bearer"
    }


@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
