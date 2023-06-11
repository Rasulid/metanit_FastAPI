from fastapi import FastAPI
from .api.crud.base_crud import router as base_crud
from .api.auth.auth import router as auth_router

app = FastAPI()
app.include_router(base_crud)
app.include_router(auth_router)

@app.get("/api")
async def root():
    return {"root": "root"}


