from pydantic import BaseModel, condecimal
from decimal import Decimal
from typing import Optional
from app.models.enums import AccountType, Currency

"""
    Account Schemas
"""


class Account(BaseModel):
    account_id: int
    user_id: int
    name: str
    balance: condecimal(gt=-1)
    currency: Currency
    account_type: AccountType

    # class Config:
    #     orm_mode = True
    #     from_attributes=True


class SavingsAccount(Account):
    interest_rate: float


class CurrentAccount(Account):
    pass  # No extra fields for CurrentAccount


class CashAccount(Account):
    pass  # No extra fields for CashAccount


"""
    Create Account Schemas
    Removing auto-generated no changeable fields (e.g. acount_id)
"""


class AccountCreate(BaseModel):
    user_id: int
    name: str
    balance: condecimal(gt=-1)
    currency: Currency


class SavingsAccountCreate(AccountCreate):
    interest_rate: float
    account_type: AccountType = AccountType.SAVINGS


class CurrentAccountCreate(AccountCreate):
    account_type: AccountType = AccountType.CURRENT


class CashAccountCreate(AccountCreate):
    account_type: AccountType = AccountType.CASH


"""
    Update Account Schemas
"""


class AccountUpdate(BaseModel):
    name: Optional[str] = None
    balance: Optional[condecimal(gt=-1)] = None


class SavingsAccountUpdate(AccountUpdate):
    interest_rate: Optional[float] = None
