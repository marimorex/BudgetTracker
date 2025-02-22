import asyncio
import uvicorn
from helpers.logger import logger
from rabbitmq.connection import client_manager

# from rabbitmq.consumer import start_consumer


def main():
    logger.info("Starting Transaction Microservice")
    channel = client_manager.get_channel()
    uvicorn.run(
        "api.transactions:app",
        host="0.0.0.0",
        port=81,
        reload=True,
    )


if __name__ == "__main__":
    print("NOTE: If you cannot connect to the default URL at 0.0.0.0")
    print("      Try connecting to http://localhost:81")
    main()
