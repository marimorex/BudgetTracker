from fastapi import FastAPI

app = FastAPI()

# Endpoint to list all accounts
@app.get("/accounts/",)
def list_accounts():
    return "hello world"