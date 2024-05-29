from pydantic import BaseModel, ConfigDict


class StockBase(BaseModel):
    name: str
    amount: int
    max_amount: int


class StockCreate(StockBase):
    pass


class Stock(StockBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TransactionBase(BaseModel):
    is_offer: bool
    user_id: int
    stock_id: int
    amount: int
    price: float


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    money: float
    transactions: list[Transaction] = []

    model_config = ConfigDict(from_attributes=True)
