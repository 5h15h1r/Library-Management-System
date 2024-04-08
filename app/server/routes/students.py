from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder


from app.server.database import (
    add_student,
    del_student,
    retrieve_student,
    retrieve_students,
    update_studentt,
)
from app.server.models.student import (
    StudentSchema,
    UpdateStudentModel,
)


router = APIRouter()


@router.post(
    "/",
    response_description="Student data created",
    response_model=None,
    status_code=201,
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": {
                        "id": "string",
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {"example": {"message": "Internal Server Error"}}
            },
        },
    },
)
async def create_students(student: StudentSchema = Body(...)):
    student = jsonable_encoder(student)
    new_student = await add_student(student)
    data = {"id": new_student["id"]}
    return data


@router.get(
    "/",
    response_description="Students retrieved",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "name": "string",
                                "age": 0,
                            }
                        ]
                    }
                }
            },
        },
        404: {
            "description": "No Records Found",
            "content": {"application/json": {"example": {"message": "string"}}},
        },
    },
)
async def list_students(country: str = None, age: int = None):
    students = await retrieve_students(country, age)
    if students:
        return {"data": students}
    raise HTTPException(status_code=404, detail="No records found .")


@router.get(
    "/{id}",
    response_description="Student data retrieved",
    response_model=StudentSchema,
    responses={
        400: {
            "description": "No Records Found",
            "content": {"application/json": {"example": {"message": "string"}}},
        },
    },
)
async def fetch_student(id):
    student = await retrieve_student(id)
    if student:
        return student
    raise HTTPException(status_code=404, detail=f"No student with the id {id} found")


@router.patch(
    "/{id}",
    status_code=204,
    response_description="Student data updated",
    responses={
        204: {
            "description": "No content",
            "content": {"application/json": {"example": {}}},
        },
    },
)
async def update_student(id: str, req: UpdateStudentModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_student = await update_studentt(id, req)
    if updated_student:
        return None

    raise HTTPException(status_code=400, detail=f"No student with the id {id} found")


@router.delete(
    "/{id}",
    response_description="Student data deleted from the database",
    responses={
        200: {
            "content": {"application/json": {"example": {}}},
        },
        404: {
            "description": "No Records Found",
            "content": {"application/json": {"example": {"message": "string"}}},
        },
    },
)
async def delete_student(id: str):
    deleted_student = await del_student(id)
    if deleted_student:
        return "{}"

    raise HTTPException(status_code=404, detail="Student with id {id} doesn't exist")
