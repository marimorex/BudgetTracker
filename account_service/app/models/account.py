from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, Integer, String, Float, Enum, Numeric
from models.enums import AccountType, Currency
from decimal import Decimal
from db.db import Base


class Account(Base):
    """
    Represents a generic bank account.

    Attributes:
        __tablename__ (str): Name of the database table.
        minimum_balance (int): The minimum balance allowed for all accounts (default is 0).
        account_id (int): The unique identifier of the account.
        user_id (int): The ID of the user owning the account.
        name (str): The name of the account (e.g., personal savings).
        balance (Decimal): The balance in the account, with a setter that validates minimum balance.
        currency (Currency): The currency in which the account operates.
        account_type (AccountType): The type of account (e.g., savings, current, cash).

    Methods:
        balance (property): Gets the current balance of the account.
        balance (setter): Sets the account balance and ensures it meets the minimum balance requirement.

    __mapper_args__:
        polymorphic_on: Specifies the field used for single table inheritance (account_type).
    """

    __tablename__ = "accounts"

    # class attributes
    minimum_balance = 0

    # sqlachemy mappings
    account_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[Currency] = mapped_column(Enum(Currency), nullable=False)
    account_type: Mapped[AccountType] = mapped_column(Enum(AccountType), nullable=False)

    __mapper_args__ = {"polymorphic_on": account_type}

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, balance):
        if balance < Account.minimum_balance:
            raise ValueError("Minimum balance is ${Account.minimum_balance}")
        self._balance = balance


class SavingsAccount(Account):
    """
    Represents a savings account, inheriting from the Account class.

    Attributes:
        interest_rate (float): The interest rate applied to the savings account.

    Methods:
        apply_interest(): Applies the interest to the balance based on the interest rate.

    __mapper_args__:
        polymorphic_identity: Specifies that this class represents a savings account in the inheritance hierarchy.
    """

    __mapper_args__ = {"polymorphic_identity": AccountType.SAVINGS}

    interest_rate: Mapped[float] = mapped_column(Float, nullable=True)

    def apply_interest(self):
        self.balance += self.balance * self.interest_rate


class CurrentAccount(Account):
    """
    Represents a current (or checking) account, inheriting from the Account class.

    __mapper_args__:
        polymorphic_identity: Specifies that this class represents a current account in the inheritance hierarchy.
    """

    __mapper_args__ = {"polymorphic_identity": AccountType.CURRENT}


class CashAccount(Account):
    """
    Represents a cash account, inheriting from the Account class.

    __mapper_args__:
        polymorphic_identity: Specifies that this class represents a cash account in the inheritance hierarchy.
    """

    __mapper_args__ = {"polymorphic_identity": AccountType.CASH}
