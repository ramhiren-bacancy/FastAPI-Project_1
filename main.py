from fastapi import  FastAPI
# from sqlalchemy.orm import Session
from app.routes import todo, user
from database import engine,Base
from contextlib import asynccontextmanager

# Base.metadata.create_all(bind=engine) # ! Sync DATABASE

# ! Async DATABASE
@asynccontextmanager
async def lifespan(_app: FastAPI):
    # StartUp
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()

app = FastAPI(lifespan=lifespan,swagger_ui_parameters={"persistAuthorization": True})


app.include_router(todo.router, prefix="/api/todos", tags=["Todos"])
app.include_router(user.router, prefix="/api/users",tags=["Users"])

@app.get("/")
def welcome():
    return {"massage" : "Welcome To Home"}
    


# Note :
# 1. Run the app using `uv run uvicorn main:app --reload`
# 2. migrate the database using `alembic revision --autogenerate -m "Initial Migration"` and then `alembic upgrade head`
# 3. Run the Celery worker using `celery -A app.core.celery_app.celery_app worker --loglevel=info`
#                       OR `celery -A app.core.celery_app.celery_app worker --pool=solo -l info -E` 
#       in a separate terminal

# 4. Run Flower using  `celery -A app.core.celery_app.celery_app flower --port=5555` in a separate terminal to monitor Celery tasks