from fastapi import FastAPI

from app.server.routes.students import router as StudentRouter

app = FastAPI()

app.include_router(StudentRouter, tags=["Student"], prefix="/students")


@app.get("/", tags=["Root Dir"])
async def default():
    return {"message": "Library Management System"}
