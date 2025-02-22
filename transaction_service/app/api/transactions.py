from fastapi import FastAPI
from rabbitmq import producer

app = FastAPI()


@app.get("/transactions")
def list_trasactions():
    producer.publish_transaction_created("TEST !!!")
    return "Hello world"
