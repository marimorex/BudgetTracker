from app.models.account import (
    DBAccount,
    DBSavingsAccount,
    DBCurrentAccount,
    DBCashAccount,
)
from typing import Union, Optional
from app.schemas.account_schema import (
    Account,
    SavingsAccount,
    CurrentAccount,
    CashAccount,
    SavingsAccountCreate,
    CashAccountCreate,
    CurrentAccountCreate,
    AccountCreate,
    AccountUpdate,
    SavingsAccountUpdate,
)
from app.models.enums import AccountType
from sqlalchemy.orm import with_polymorphic, Session

from app.db.db import SessionLocal
from sqlalchemy import select
from .exceptions import AccountTypeMismatchError, AccountNotFoundError


class AccountDAO:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_accounts(self) -> Optional[list[DBAccount]]:
        return self.db_session.execute(select(DBAccount)).scalars().all()

    def get_account_by_id(self, account_id: int) -> Optional[DBAccount]:
        return self.db_session.get(DBAccount, account_id)

    def get_all_accounts_by_user_id(self, user_id: int) -> list[DBAccount]:
        return (
            self.db_session.execute(
                select(DBAccount).where(DBAccount.user_id == user_id)
            )
            .scalars()
            .all()
        )

    def create_account(
        self, account_data, account_type: type[DBAccount]
    ) -> Optional[DBAccount]:
        """
        Each specific DAO inherits from AccountDAO and can override or add type-specific methods.
        """
        new_account = account_type(**account_data.model_dump())
        self.db_session.add(new_account)
        try:
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            print(f"Error creating account: {e}")
            return None
        self.db_session.refresh(new_account)
        return new_account

    def update_account(
        self,
        account_id: int,
        account_data: type[AccountCreate],
        account_type: AccountType,
    ) -> Optional[DBAccount]:
        """
        Each specific DAO inherits from AccountDAO and can override or add type-specific methods.
        In this case, account_data, can be of type SavingsAccountCreate, CashAccountCreate, CurrentAccountCreate,
        """
        account = self.get_account_by_id(account_id)
        if not account:
            return None

        if account.account_type != account_type.name:
            raise AccountTypeMismatchError(
                f"Account type mismatch: expected {account_type.name}, got {account.account_type.name}"
            )

        for key, value in account_data.model_dump(exclude_unset=True).items():
            setattr(account, key, value)

        self.db_session.commit()
        self.db_session.refresh(account)
        return account


class SavingsAccountDAO(AccountDAO):
    def create_savings_account(
        self, account_data: SavingsAccountCreate
    ) -> Optional[DBAccount]:
        return self.create_account(account_data, DBSavingsAccount)

    def update_savings_account(
        self, account_id: int, account_data: SavingsAccountUpdate
    ) -> Optional[DBAccount]:
        return self.update_account(account_id, account_data, AccountType.SAVINGS)


class CurrentAccountDAO(AccountDAO):
    def create_current_account(
        self, account_data: CurrentAccountCreate
    ) -> Optional[DBAccount]:
        return self.create_account(account_data, DBCurrentAccount)

    def update_current_account(
        self, account_id: int, account_data: AccountUpdate
    ) -> Optional[DBAccount]:
        return self.update_account(account_id, account_data, AccountType.CURRENT)


class CashAccountDAO(AccountDAO):
    def create_cash_account(
        self, account_data: CashAccountCreate
    ) -> Optional[DBCashAccount]:
        return self.create_account(account_data, DBCashAccount)

    def update_cash_account(
        self, account_id: int, account_data: AccountUpdate
    ) -> Optional[DBAccount]:
        return self.update_account(account_id, account_data, AccountType.CASH)
