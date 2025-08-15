from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from uuid import uuid4

app = FastAPI()

# In-memory "database"
users: Dict[str, dict] = {}

# Pydantic model for User
class User(BaseModel):
    name: str
    email: str

@app.post("/users")
def create_user(user: User):
    user_id = str(uuid4())  # generate a unique ID
    users[user_id] = user.dict()
    return {"id": user_id, "message": "User created"}

@app.get("/users")
def list_users():
    return [{"id": user_id, **user} for user_id, user in users.items()]

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    if user_id in users:
        del users[user_id]
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
