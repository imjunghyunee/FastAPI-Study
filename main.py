# main.py

from fastapi import FastAPI
from route import router

app = FastAPI(title="ToDo List Service")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome to the ToDo List Service!"}
