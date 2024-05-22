from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Este documento se inicia con pipenv run users

# Entidad user


class User(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    age: int


users_list = [
    User(id=1, name='Juan', surname='Castro', email='juan@gmail.com', age=20),
    User(id=2, name='Camila', surname='Sevilla',
         email='camila008@gmail.com', age=24)
]


def search_user(id: int):
    users = list(filter(lambda user: user.id == id, users_list))
    if users:
        return users[0]
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.get("/users")
async def users():
    return users_list


@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)


@app.get("/userquery/")
async def user_query(id: int):
    return search_user(id)


@app.post("/user/")
async def user(user: User):
    userResult = list(
        filter(lambda userList: userList.id == user.id, users_list))
    if userResult:
        raise HTTPException(status_code=404, detail="User already exist")
    else:
        users_list.append(user)
        raise HTTPException(status_code=200, detail="User added succesfully!")


@app.put("/user/")
async def inser_user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if found:
        raise HTTPException(
            status_code=200, detail="User updated succesfully!")
    else:
        raise HTTPException(status_code=404, detail="Error user not found")


@app.delete("/user/{id}")
async def delete_user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if found:
        raise HTTPException(
            status_code=200, detail="User deleted succesfully!")
    else:
        raise HTTPException(status_code=404, detail="Error user not found")
