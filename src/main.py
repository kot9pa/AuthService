import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import db_helper
from config import settings
from base import Base

from api_v1.users.models import User
from api_v1.codes.models import Code
from api_v1 import internal_router


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     async with db_helper.engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#     yield

# app = FastAPI(lifespan=lifespan)
# app.include_router(router=internal_router, prefix=f"{settings.api_v1_prefix}")

app = FastAPI()
app.include_router(router=internal_router, prefix=f"{settings.api_v1_prefix}")

@app.get("/", tags=["Service"])
def ping():
    return {"Success": True}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
