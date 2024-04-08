import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config

MONGO_URI = config("MONGO_URI")  # read environment variable
MONGO_URI = "mongodb+srv://Itachi:Helloworld14@cluster0.tleddj0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

database = client.students

student_collection = database.get_collection("students_collection")


def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "age": student["age"],
        "address": student["address"],
    }


async def retrieve_students(country, age):
    students = []
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}

    filtered_students = student_collection.find(query)

    async for student in filtered_students:
        students.append(student_helper(student))
    return students


# Create a new student
async def add_student(student_data: dict) -> dict:
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)


# Retrieve a student with a matching ID
async def retrieve_student(id: str) -> dict:
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        return student_helper(student)


# Update a student with a matching ID
async def update_studentt(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        updated_student = await student_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_student:
            return True
        return False


# Delete a student with param: ID
async def del_student(id: str):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True
