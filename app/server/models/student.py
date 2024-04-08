from pydantic import BaseModel, Field
from typing import List, Optional


class Address(BaseModel):
    city: str = Field(...)
    country: str = Field(...)


class StudentSchema(BaseModel):
    name: str = Field(...)
    age: int = Field(...)
    address: Address

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "age": "23",
                "address": {"city": "Pune", "country": "India"},
            }
        }


class NotFoundModel(BaseModel):
    message: str


class GetStudents(StudentSchema):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[Address] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "age": "23",
                "address": {"city": "Pune", "country": "India"},
            }
        }


class FetchBaseStudent(BaseModel):
    name: str = Field(...)
    age: str = Field(...)


class FetchStudentsModel(BaseModel):
    data: List[FetchBaseStudent]


class UpdateStudentModel(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[Address] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "age": "23",
                "address": {"city": "Pune", "country": "India"},
            }
        }
