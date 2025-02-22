import asyncio
import uvicorn
from db.db_manager import DatabaseManager
import time
from helpers.logger import logger
from rabbitmq.consumer import start_consumer


async def main():
    logger.info("Starting account microservice")

    # todo implement try catch to connect to db
    # Check if we are in dev mode

    db_manager = DatabaseManager()
    db_manager.reset_database()
    logger.info("connected to DB accounts")

    consumer_task = asyncio.create_task(start_consumer())

    server_task = asyncio.create_task(
        uvicorn.run(
            "api.accounts:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
        )
    )
    await asyncio.gather(consumer_task, server_task)


if __name__ == "__main__":
    print("NOTE: If you cannot connect to the default URL at 0.0.0.0")
    print("      Try connecting to http://localhost:8000")
    asyncio.run(main())
