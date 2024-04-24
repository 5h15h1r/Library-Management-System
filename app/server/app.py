from fastapi import FastAPI
from server.middleware.rate_limiter import RateLimiterMiddleware
from app.server.routes.students import router as StudentRouter

app = FastAPI()

app.middleware("http")(
    RateLimiterMiddleware(redis_url="redis://localhost", window_size=4, max_requests=4)
)
app.include_router(StudentRouter, tags=["Student"], prefix="/students")


@app.get("/", tags=["Root Dir"])
async def default():
    return {"message": "Library Management System"}
