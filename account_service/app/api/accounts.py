from fastapi import FastAPI, Depends, HTTPException, status
from typing import List, Union, Annotated
from app.daos.account_dao import (
    AccountDAO,
    SavingsAccountDAO,
    CurrentAccountDAO,
    CashAccountDAO,
    DBAccount,
    AccountTypeMismatchError,
)
from app.schemas.account_schema import (
    Account,
    SavingsAccount,
    CurrentAccount,
    CashAccount,
    CashAccountCreate,
    CurrentAccountCreate,
    SavingsAccountCreate,
    AccountUpdate,
    SavingsAccountUpdate,
)
from app.db.db import SessionLocal, Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
    Session DB for Dependency Injection
"""


def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


"""
    General Accounts Endpoints
"""


@app.get(
    "/accounts", response_model=List[Union[SavingsAccount, CurrentAccount, CashAccount]]
)
def list_accounts(db: Annotated[Session, Depends(get_session)]) -> List[DBAccount]:
    account_dao = AccountDAO(db_session=db)
    accounts = account_dao.get_all_accounts()
    return accounts


@app.get(
    "/accounts/{account_id}",
    response_model=Union[SavingsAccount, CurrentAccount, CashAccount],
)
def get_account_by_id(
    account_id: int, db: Annotated[Session, Depends(get_session)]
) -> DBAccount:
    account_dao = AccountDAO(db_session=db)
    account = account_dao.get_account_by_id(account_id)
    if account is None:
        raise HTTPException(
            status_code=404, detail=f"Acoount with id: {account_id} not found"
        )
    return account


"""
    Post Accounts Endpoints
"""


@app.post("/accounts/savings", response_model=SavingsAccount)
def create_account_savings(
    account: SavingsAccountCreate, db: Annotated[Session, Depends(get_session)]
) -> DBAccount:
    account_dao = SavingsAccountDAO(db_session=db)
    new_account = account_dao.create_savings_account(account)
    if new_account is None:
        raise HTTPException(status_code=500, detail=f"Error creating the account")
    return new_account


@app.post("/accounts/current", response_model=CurrentAccount)
def create_account_current(
    account: CurrentAccountCreate, db: Annotated[Session, Depends(get_session)]
) -> DBAccount:
    account_dao = CurrentAccountDAO(db_session=db)
    new_account = account_dao.create_current_account(account)
    if new_account is None:
        raise HTTPException(status_code=500, detail=f"Error creating the account")
    return new_account


@app.post("/accounts/cash", response_model=CashAccount)
def create_account_cash(
    account: CashAccountCreate, db: Annotated[Session, Depends(get_session)]
) -> DBAccount:
    account_dao = CashAccountDAO(db_session=db)
    new_account = account_dao.create_cash_account(account)
    if new_account is None:
        raise HTTPException(status_code=500, detail=f"Error creating the account")
    return new_account


"""
    Patch Accounts Endpoints
"""


@app.patch("/accounts/savings/{account_id}", response_model=SavingsAccount)
def update_account_savings(
    account_id: int,
    account_update: SavingsAccountUpdate,
    db: Annotated[Session, Depends(get_session)],
) -> DBAccount:
    """
    Update a savings account by its ID.
    """
    account_dao = SavingsAccountDAO(db_session=db)
    try:
        updated_account = account_dao.update_savings_account(account_id, account_update)
    except AccountTypeMismatchError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )

    if not updated_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )

    return updated_account


@app.patch("/accounts/current/{account_id}", response_model=CurrentAccount)
def update_account_current(
    account_id: int,
    account_update: AccountUpdate,
    db: Annotated[Session, Depends(get_session)],
) -> DBAccount:
    """
    Update a savings account by its ID.
    """
    account_dao = CurrentAccountDAO(db_session=db)
    try:
        updated_account = account_dao.update_current_account(account_id, account_update)
    except AccountTypeMismatchError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )

    if not updated_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    return updated_account


@app.patch("/accounts/cash/{account_id}", response_model=CashAccount)
def update_account_cash(
    account_id: int,
    account_update: AccountUpdate,
    db: Annotated[Session, Depends(get_session)],
) -> DBAccount:
    """
    Update a savings account by its ID.
    """
    account_dao = CashAccountDAO(db_session=db)
    try:
        updated_account = account_dao.update_cash_account(account_id, account_update)
    except AccountTypeMismatchError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )
    if not updated_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    return updated_account


"""
    Accounts per User Endpoints
"""


@app.get(
    "/accounts/user/{user_id}",
    response_model=List[Union[SavingsAccount, CurrentAccount, CashAccount]],
)
def list_accounts_by_user_id(
    user_id: int, db: Annotated[Session, Depends(get_session)]
) -> List[DBAccount]:
    account_dao = AccountDAO(db_session=db)
    accounts = account_dao.get_all_accounts_by_user_id(user_id)
    if accounts is None:
        raise HTTPException(status_code=404, detail=f"No accounts for the user id {id}")
    return accounts
