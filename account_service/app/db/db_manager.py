# app/db_manager.py
from sqlalchemy.orm import Session
from db.db import engine, SessionLocal
from models.account import (
    Account,
    CurrentAccount,
    SavingsAccount,
    CashAccount,
    Base,
    Currency,
)
from db.config import DevelopmentConfig


class DatabaseManager:
    def __init__(self, config=DevelopmentConfig):
        self.engine = engine
        self.config = config

    def drop_tables(self):
        """Drop all tables from the database."""
        Base.metadata.drop_all(bind=self.engine)
        print("All tables dropped.")

    def create_tables(self):
        """Create all tables from the defined models."""
        Base.metadata.create_all(bind=self.engine)
        print("All tables created.")

    def seed_data(self):
        """Populate the database with initial seed data."""
        session = SessionLocal()
        try:
            # Add default users or other seed data
            account_current = CurrentAccount(
                name="current 1", user_id=1, balance=100.00, currency=Currency.EURO
            )
            account_savings = SavingsAccount(
                name="savings 1",
                user_id=1,
                balance=100.00,
                interest_rate=3.00,
                currency=Currency.EURO,
            )
            account_cash = CashAccount(
                name="cash 1", user_id=1, balance=100.00, currency=Currency.EURO
            )
            session.add_all([account_current, account_savings, account_cash])
            session.commit()
            print("Database seeded with default data.")

        except Exception as e:
            session.rollback()
            print(f"Error seeding data: {e}")
        finally:
            session.close()

    def reset_database(self):
        """Drop tables, create them from scratch, and populate with seed data."""
        self.drop_tables()
        self.create_tables()
        self.seed_data()
