"""
conftest.py
---

Fixtures for pytest.
"""
from datetime import date

import pytest
import sqlalchemy
from sqlalchemy.orm import Session, sessionmaker
from starlette.testclient import TestClient

from app.api.accounts import app, get_session
from app.models.account import (
    Base,
    DBAccount,
    DBCurrentAccount,
    DBSavingsAccount,
    DBCashAccount,
    Base,
    Currency,
)

test_db = sqlalchemy.create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={"check_same_thread": False},
    echo=True,
)

test_sessionmaker = sessionmaker(bind=test_db)


def setup_test_db():
    """Create tables and test data in test db."""
    Base.metadata.create_all(bind=test_db)
    session = Session(test_db)

    account_current = DBCurrentAccount(
        name="current 1", user_id=1, balance=100.00, currency=Currency.EURO
    )
    account_savings = DBSavingsAccount(
        name="savings 1",
        user_id=1,
        balance=100.00,
        interest_rate=3.00,
        currency=Currency.EURO,
    )
    account_cash = DBCashAccount(
        name="cash 1", user_id=1, balance=100.00, currency=Currency.EURO
    )
    session.add_all([account_current, account_savings, account_cash])
    session.commit()
    print("Database seeded with default data.")


def get_test_session():
    """Create a db session for a single test.
    After the test: close the session and drop all tables."""
    setup_test_db()
    session = test_sessionmaker()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_db)


@pytest.fixture()
def client():
    """Create a TestClient that uses the test database."""

    # See: https://fastapi.tiangolo.com/advanced/testing-database/
    app.dependency_overrides[get_session] = get_test_session
    yield TestClient(app)
    del app.dependency_overrides[get_session]
