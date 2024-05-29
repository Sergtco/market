from sqlalchemy.orm import Session
from . import models, schemas


def init_database(db: Session):
    ssm = models.Stock(name="SSM", amount=1000, max_amount=1000)
    apm = models.Stock(name="APM", amount=4000, max_amount=4000)
    dws = models.Stock(name="DWS", amount=5000, max_amount=5000)
    sergt = models.User(login="sergtco", password="password", money=500)
    khan = models.User(login="khan", password="password", money=500)
    try:
        db.add_all([ssm, apm, dws, sergt, khan])
        db.commit()
    except Exception as e:
        print(e)


def get_stocks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Stock).offset(skip).limit(limit).all()


def find_user(db: Session, login: str):
    return db.query(models.User).filter(models.User.login == login).first()


def buy_stock(db: Session, user_id: int, name: str):
    db.query(models.Stock).filter(models.Stock.name == name).update(
        {models.Stock.amount: models.Stock.amount - 1}, False
    )
    stock = list(filter(lambda stock: stock.name == name, get_stocks(db)))[0]
    stockSch = schemas.Stock.model_validate(stock)
    if stockSch.amount <= 0:
        db.rollback()
        return
    db.query(models.User).filter(models.User.id == user_id).update(
        {models.User.money: models.User.money - stock.max_amount + stock.amount + 1}
    )
    db.add(
        models.Transaction(
            is_offer=False,
            stock_id=stock.id,
            user_id=user_id,
            amount=1,
            price=stock.max_amount - stock.amount - 1,
        )
    )
    db.commit()


def sell_stock(db: Session, user_id: int, name: str):
    db.query(models.Stock).filter(models.Stock.name == name).update(
        {models.Stock.amount: models.Stock.amount + 1}, False
    )
    stock = list(filter(lambda stock: stock.name == name, get_stocks(db)))[0]
    stockSch = schemas.Stock.model_validate(stock)
    if stockSch.max_amount <= stockSch.amount:
        db.rollback()
        return
    db.query(models.User).filter(models.User.id == user_id).update(
        {models.User.money: models.User.money + stock.max_amount - stock.amount - 1}
    )
    db.add(
        models.Transaction(
            is_offer=True,
            stock_id=stock.id,
            user_id=user_id,
            amount=1,
            price=stock.max_amount - stock.amount - 1,
        )
    )
    db.commit()


def validate_user(db: Session, login: str, password: str):
    return (
        db.query(models.User)
        .filter(models.User.login == login)
        .filter(models.User.password == password)
        .first()
    )
