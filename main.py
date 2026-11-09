from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from routers.users import router as user_router
from routers.predict import router as predict_router

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors()},
    )


@app.get("/")
async def root():
   return {'message': 'Hello World'}


app.include_router(user_router)
app.include_router(predict_router)