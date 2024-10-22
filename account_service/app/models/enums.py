from enum import Enum


class Currency(str, Enum):
    """
    A class representing the types of Currencies.
    """

    EURO = "EURO"
    DOLAR = "DOLAR"
    CRIPTO = "CRIPTO"


class AccountType(str, Enum):
    """
    A class representing the types of Accounts.
    """

    CURRENT = "CURRENT"
    CASH = "CASH"
    SAVINGS = "SAVINGS"
