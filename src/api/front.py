from typing import Annotated
from fastapi import APIRouter, Depends, FastAPI, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from database.database import get_db
from database import crud
from sqlalchemy.orm import Session
from fastapi import Form
import jwt

KEY = "secret"

Router = APIRouter()
templates = Jinja2Templates(directory="static/templates")


@Router.get("/")
async def index(request: Request, db: Session = Depends(get_db)):
    try:
        decoded = jwt.decode(request.cookies["token"], KEY, algorithms=["HS256"])
        user = crud.find_user(db, decoded["login"])
        if user is not None:
            pass
        else:
            return Response(status_code=400)
    except Exception as e:
        print(e)
        return RedirectResponse("/login")
    stocks = crud.get_stocks(db)
    stocks = {stock: (stock.max_amount - stock.amount) for stock in stocks}
    return templates.TemplateResponse(
        request=request, name="index.html", context={"stocks": stocks, "user": user}
    )


@Router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={})


@Router.post("/login")
async def check_login(
    request: Request,
    response: Response,
    login: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: Session = Depends(get_db),
):
    user = crud.validate_user(db, login, password)
    if user is not None:
        form = {"login": user.login}
        token = jwt.encode(form, KEY, algorithm="HS256").decode("utf-8")
        response.set_cookie(key="token", value=token)
        response.status_code = 303
        response.headers["location"] = "/"
        return response
    response.status_code = 303
    response.headers["location"] = "/login"
    return response
