import os
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Security
from .auth0 import Auth0, Auth0User
from sqlalchemy.orm import Session

from .database.crud import (
    get_user_by_id,
    create_user,
    get_users,
    get_user,
    create_user_item,
    get_items,
)
from .database.schemas import User, UserCreate, Item, ItemCreate
from .database.db import get_db


auth = Auth0(
    domain=os.environ["AUTH0_DOMAIN"],
    api_audience=os.environ["AUTH0_AUDIENCE"],
    # scopes={"read:test": ""},
    scopes={"openid profile email": ""},
)
app = FastAPI()


@app.post("/secure", dependencies=[Depends(auth.implicit_scheme)])
# def index(user: Auth0User = Security(auth.get_user, scopes=["read:test"])):
def index(user: Auth0User = Security(auth.get_user)):
    return {"message": f"{user}"}


@app.post("/oauth2-redirect")
def signup(user: Auth0User = Security(auth.get_user, scopes=["user:admin"])):
    return {"message": "success"}


@app.post("/users/", response_model=User, dependencies=[Depends(auth.implicit_scheme)])
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    authUser: Auth0User = Security(auth.get_user, scopes=["user:admin"]),
):
    db_user = get_user_by_id(db, id=user.id)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


@app.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=Item)
def create_item_for_user(user_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    return create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = get_items(db, skip=skip, limit=limit)
    return items
