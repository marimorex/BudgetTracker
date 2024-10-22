from unittest.mock import patch

import pytest
from fastapi import HTTPException


"""
Savings Account Patch TESTS
"""


def test_patch_existent_account_savings(client):
    """Test updating certain attributes of an existing savings account  via PATCH request to /accounts/savings"""

    # Define the data for the savings account to be created
    savings_account_data_update = {"balance": "123.45"}

    # Perform the PATCH request. Account 2 is a SAVINGS Account
    response = client.patch("/accounts/savings/2", json=savings_account_data_update)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["balance"] == savings_account_data_update["balance"]


def test_patch_non_existent_account_savings(client):
    """Test updating certain attributes of an existing savings account  via PATCH request to /accounts/savings"""

    # Define the data for the savings account to be created
    savings_account_data_update = {"balance": "123.45"}

    # Perform the PATCH request
    response = client.patch("/accounts/savings/333", json=savings_account_data_update)

    assert response.status_code == 404

    assert response.json() == {"detail": "Account not found"}


def test_patch_mismatch_account_type_account_savings(client):
    """Test updating certain attributes of an existing savings account  via PATCH request to /accounts/savings"""

    # Define the data for the savings account to be created
    savings_account_data_update = {"balance": "123.45"}

    # Perform the PATCH request, Account 1 is CURRENT
    response = client.patch("/accounts/savings/1", json=savings_account_data_update)

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Account type mismatch: expected SAVINGS, got CURRENT"
    }


"""
CURRENT Account Patch TESTS
"""


def test_patch_existent_account_current(client):
    """Test updating certain attributes of an existing current account  via PATCH request to /accounts/current"""

    # Define the data for the savings account to be created
    current_account_data_update = {"balance": "123.45"}

    # Perform the PATCH request. Account 1 is a current Account
    response = client.patch("/accounts/current/1", json=current_account_data_update)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["balance"] == current_account_data_update["balance"]


def test_patch_non_existent_account_current(client):
    """Test updating certain attributes of an existing current account  via PATCH request to /accounts/current"""

    # Define the data for the savings account to be created
    current_account_data_update = {"balance": "123.45"}

    # Perform the PATCH request
    response = client.patch("/accounts/current/333", json=current_account_data_update)

    assert response.status_code == 404

    assert response.json() == {"detail": "Account not found"}


def test_patch_mismatch_account_type_account_current(client):
    """Test updating certain attributes of an existing current account  via PATCH request to /accounts/current"""

    # Define the data for the savings account to be created
    current_account_data_update = {"balance": "123.45"}

    # Perform the PATCH request, Account 2 is SAVINGS
    response = client.patch("/accounts/current/2", json=current_account_data_update)

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Account type mismatch: expected CURRENT, got SAVINGS"
    }


"""
CASH Account Patch TESTS
"""


def test_patch_existent_account_cash(client):
    """Test updating certain attributes of an existing cash account  via PATCH request to /accounts/cash"""

    # Define the data for the savings account to be created
    cash_account_data_update = {"balance": "123.45"}

    # Perform the PATCH request. Account 3 is a CASH Account
    response = client.patch("/accounts/cash/3", json=cash_account_data_update)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["balance"] == cash_account_data_update["balance"]


def test_patch_non_existent_account_cash(client):
    """Test updating certain attributes of an existing cash account  via PATCH request to /accounts/cash"""

    # Define the data for the savings account to be created
    cash_account_data_update = {"balance": "123.45"}

    # Perform the PATCH request
    response = client.patch("/accounts/cash/333", json=cash_account_data_update)

    assert response.status_code == 404

    assert response.json() == {"detail": "Account not found"}


def test_patch_mismatch_account_type_account_cash(client):
    """Test updating certain attributes of an existing current account  via PATCH request to /accounts/cash"""

    # Define the data for the savings account to be created
    cash_account_data_update = {"balance": "123.45"}

    # Perform the PATCH request, Account 1 is CURRENT
    response = client.patch("/accounts/cash/1", json=cash_account_data_update)

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Account type mismatch: expected CASH, got CURRENT"
    }
