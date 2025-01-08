from fastapi import FastAPI

app = FastAPI()


@app.get("/transactions")
def list_trasactions():
    return "Hello world"
