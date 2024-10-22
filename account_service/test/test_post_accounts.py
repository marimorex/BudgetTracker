from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.api.accounts import get_account_by_id
from app.models.account import DBAccount

"""
Integration tests
"""


def test_create_account_savings(client):
    """Test creating a new savings account via POST request to /accounts/savings"""

    # Define the data for the savings account to be created
    savings_account_data = {
        "user_id": 1,
        "name": "My Savings",
        "balance": "500.00",
        "currency": "EURO",
        "account_type": "SAVINGS",
        "interest_rate": 2.5,
    }

    # Perform the POST request
    response = client.post("/accounts/savings", json=savings_account_data)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["user_id"] == savings_account_data["user_id"]
    assert response_data["name"] == savings_account_data["name"]
    assert response_data["balance"] == savings_account_data["balance"]
    assert response_data["currency"] == savings_account_data["currency"]
    assert response_data["account_type"] == "SAVINGS"
    assert response_data["interest_rate"] == savings_account_data["interest_rate"]
    assert "account_id" in response_data


def test_create_account_current(client):
    """Test creating a new Current account via POST request to /accounts/current"""

    # Define the data for the savings account to be created
    current_account_data = {
        "user_id": 1,
        "name": "My Current",
        "balance": "500.00",
        "currency": "EURO",
        "account_type": "CURRENT",
    }

    # Perform the POST request
    response = client.post("/accounts/current", json=current_account_data)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["user_id"] == current_account_data["user_id"]
    assert response_data["name"] == current_account_data["name"]
    assert response_data["balance"] == current_account_data["balance"]
    assert response_data["currency"] == "EURO"
    assert response_data["account_type"] == "CURRENT"
    assert "account_id" in response_data


def test_create_account_cash(client):
    """Test creating a new Current account via POST request to /accounts/cash"""

    # Define the data for the savings account to be created
    cash_account_data = {
        "user_id": 1,
        "name": "My Current",
        "balance": "500.00",
        "currency": "EURO",
        "account_type": "CASH",
    }

    # Perform the POST request
    response = client.post("/accounts/cash", json=cash_account_data)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["user_id"] == cash_account_data["user_id"]
    assert response_data["name"] == cash_account_data["name"]
    assert response_data["balance"] == cash_account_data["balance"]
    assert response_data["currency"] == "EURO"
    assert response_data["account_type"] == "CASH"
    assert "account_id" in response_data
