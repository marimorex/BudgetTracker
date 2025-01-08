import uvicorn
import time
from helpers.logger import logger


def main():
    logger.info("Starting Transaction Microservice")

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
