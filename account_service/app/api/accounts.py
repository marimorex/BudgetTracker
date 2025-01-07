import uuid
from fastapi import FastAPI, Depends, HTTPException, status, Request
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
from helpers.logger import logger, request_id_context

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
    Middleware to add unique request ID for Logs
"""


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())  # Generate a unique request ID
    request_id_context.set(request_id)  # Set it in the context variable

    request.state.request_id = request_id  # Store it in request state

    logger.info(f" Incoming request: {request.method} {request.url}")

    response = await call_next(request)  # the respective function is called and awaited
    response.headers[
        "X-Request-ID"
    ] = request_id  # Include the request ID in the response headers
    logger.info(f" Response status: {response.status_code}")

    # Clear the request_id after the response is sent
    request_id_context.set(None)
    return response


def get_request_id(request: Request) -> str:
    return request.state.request_id


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
    # todo add pagination
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
        logger.error(f"Acoount with id: {account_id} not found")
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
        logger.error(f"Error creating the account")
        raise HTTPException(status_code=500, detail=f"Error creating the account")
    return new_account


@app.post("/accounts/current", response_model=CurrentAccount)
def create_account_current(
    account: CurrentAccountCreate, db: Annotated[Session, Depends(get_session)]
) -> DBAccount:
    account_dao = CurrentAccountDAO(db_session=db)
    new_account = account_dao.create_current_account(account)
    if new_account is None:
        logger.error(f"Error creating the account")
        raise HTTPException(status_code=500, detail=f"Error creating the account")
    return new_account


@app.post("/accounts/cash", response_model=CashAccount)
def create_account_cash(
    account: CashAccountCreate, db: Annotated[Session, Depends(get_session)]
) -> DBAccount:
    account_dao = CashAccountDAO(db_session=db)
    new_account = account_dao.create_cash_account(account)
    if new_account is None:
        logger.error(f"Error creating the account")
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
        logger.error(f"{e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error", exc_info=True)
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
        logger.error("Unexpected error", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )

    if not updated_account:
        logger.error(f"Account not found")
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
        logger.error("Unexpected error", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )
    if not updated_account:
        logger.error(f"Account not found")
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
        logger.error(f"No accounts for the user id {user_id}")
        raise HTTPException(
            status_code=404, detail=f"No accounts for the user id {user_id}"
        )
    return accounts
