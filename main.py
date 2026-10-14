from fastapi import FastAPI
from fastapi.responses import JSONResponse
from validation import Request
from routers import requests
from exceptions import AppError, RequestNotFound

app = FastAPI()

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
	return JSONResponse(
		status_code = exc.status_code,
		content = {"detail": exc.message}
	)

app.include_router(requests.router)

@app.get("/")
def home():
	return {"message": "Welcome to the Student System!"}