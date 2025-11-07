from fastapi import FastAPI
from .routes import router

app = FastAPI(
    title="REST API microservie for creating notes",
    description="A simple microservice for note creatin",
)


app.include_router(router)
