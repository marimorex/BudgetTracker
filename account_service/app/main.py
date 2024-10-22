import uvicorn
from db.db_manager import DatabaseManager
import time


def main():
    time.sleep(3)

    # Check if we are in dev mode
    db_manager = DatabaseManager()
    db_manager.reset_database()

    uvicorn.run(
        "api.accounts:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    print("NOTE: If you cannot connect to the default URL at 0.0.0.0")
    print("      Try connecting to http://localhost:8000")
    main()
