from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="Auth Service",
    version="1.0.0",
    contact={
        "name": "Anandha Kannan N",
        "email": "anandhakannan0001@gmail.com",
    },
)


app.include_router(router, prefix="/api/v1")
