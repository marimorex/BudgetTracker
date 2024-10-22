from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.api.accounts import get_account_by_id
from app.models.account import DBAccount

"""
Integration tests
"""


def test_client_get_acount_by_id_1(client):
    """Call get_account_by_id using the client, retrieving account with id 1"""
    response = client.get("/accounts/1")
    assert response.status_code == 200
    assert response.json() == {
        "account_id": 1,
        "user_id": 1,
        "name": "current 1",
        "balance": "100.00",
        "currency": "EURO",
        "account_type": "CURRENT",
    }


def test_client_list_accounts(client):
    """Call list_accounts using the client, retrieving all acounts registered"""
    response = client.get("/accounts")
    assert response.status_code == 200
    assert response.json() == [
        {
            "account_id": 1,
            "user_id": 1,
            "name": "current 1",
            "balance": "100.00",
            "currency": "EURO",
            "account_type": "CURRENT",
        },
        {
            "account_id": 2,
            "user_id": 1,
            "name": "savings 1",
            "balance": "100.00",
            "currency": "EURO",
            "account_type": "SAVINGS",
            "interest_rate": 3,
        },
        {
            "account_id": 3,
            "user_id": 1,
            "name": "cash 1",
            "balance": "100.00",
            "currency": "EURO",
            "account_type": "CASH",
        },
    ]


def test_client_list_accounts_by_user_id_1(client):
    """Call list_accounts_by_user_id using the client, retrieving account with id 1"""
    response = client.get("/accounts/user/1")
    assert response.status_code == 200
    assert response.json() == [
        {
            "account_id": 1,
            "user_id": 1,
            "name": "current 1",
            "balance": "100.00",
            "currency": "EURO",
            "account_type": "CURRENT",
        },
        {
            "account_id": 2,
            "user_id": 1,
            "name": "savings 1",
            "balance": "100.00",
            "currency": "EURO",
            "account_type": "SAVINGS",
            "interest_rate": 3,
        },
        {
            "account_id": 3,
            "user_id": 1,
            "name": "cash 1",
            "balance": "100.00",
            "currency": "EURO",
            "account_type": "CASH",
        },
    ]
