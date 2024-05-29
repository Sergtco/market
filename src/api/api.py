from fastapi import APIRouter, FastAPI, Request, Depends, Response
from sqlalchemy.orm import Session
from database.database import get_db
from database import crud, schemas
from .front import KEY
import jwt


Router = APIRouter()


@Router.post("/api/buy_stock")
async def buy_stock(request: Request, db: Session = Depends(get_db)):
    try:
        decoded = jwt.decode(request.cookies["token"], KEY, algorithms=["HS256"])
        stock = await request.json()
        stock = stock["name"]
        user = schemas.User.model_validate(crud.find_user(db, decoded["login"]))
        if user is not None:
            if user.money <= 0:
                return Response(status_code=400)
            pass
        else:
            return
    except Exception as e:
        print(e)
        return
    crud.buy_stock(db, user.id, stock)
    return Response()


@Router.post("/api/sell_stock")
async def sell_stock(request: Request, db: Session = Depends(get_db)):
    try:
        decoded = jwt.decode(request.cookies["token"], KEY, algorithms=["HS256"])
        stock = await request.json()
        stock = stock["name"]
        userMod = crud.find_user(db, decoded["login"])
        user = schemas.User.model_validate(userMod)
        if user is not None:
            if userMod is not None and userMod.count_stocks()[stock] > 0:
                pass
        else:
            return Response(status_code=400)
    except Exception as e:
        print(e)
        return
    crud.sell_stock(db, user.id, stock)
    return Response()
