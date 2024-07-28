from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import datetime

uri = "mongodb+srv://fouadessahlaoui:htGw8HaZyfBJBeMh@cluster0.1rgg7rn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Access the database
db = client.school

# Define the collections
students_collection = db.students
teachers_collection = db.teachers
courses_collection = db.courses
classes_collection = db.classes
backups_collection = db.backups

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = FastAPI()

class Student(BaseModel):
    id: int
    name: str
    grade: int

class Teacher(BaseModel):
    id: int
    name: str
    subject: str

class Course(BaseModel):
    id: int
    name: str
    teacher_id: int

class Class(BaseModel):
    id: int
    course_id: int
    student_ids: list[int]

# Helper function to serialize BSON ObjectId
def serialize_id(id):
    return str(id)

# Initialize the database
def initialize_db():
    collections = ["students", "teachers", "courses", "classes", "backups"]
    existing_collections = db.list_collection_names()

    for collection in collections:
        if collection not in existing_collections:
            db.create_collection(collection)
            print(f"Created collection: {collection}")

initialize_db()

# Students
@app.get("/students/")
def read_students():
    students = list(students_collection.find({}))
    for student in students:
        student["_id"] = serialize_id(student["_id"])
    return students

@app.post("/students/")
def create_student(student: Student):
    student_dict = student.dict()
    students_collection.insert_one(student_dict)
    return student_dict

@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    result = students_collection.update_one({"id": student_id}, {"$set": updated_student.dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student.dict()

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    result = students_collection.delete_one({"id": student_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted"}

# Teachers
@app.get("/teachers/")
def read_teachers():
    teachers = list(teachers_collection.find({}))
    for teacher in teachers:
        teacher["_id"] = serialize_id(teacher["_id"])
    return teachers

@app.post("/teachers/")
def create_teacher(teacher: Teacher):
    teacher_dict = teacher.dict()
    teachers_collection.insert_one(teacher_dict)
    return teacher_dict

@app.put("/teachers/{teacher_id}")
def update_teacher(teacher_id: int, updated_teacher: Teacher):
    result = teachers_collection.update_one({"id": teacher_id}, {"$set": updated_teacher.dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return updated_teacher.dict()

@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int):
    result = teachers_collection.delete_one({"id": teacher_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return {"message": "Teacher deleted"}

# Courses
@app.get("/courses/")
def read_courses():
    courses = list(courses_collection.find({}))
    for course in courses:
        course["_id"] = serialize_id(course["_id"])
    return courses

@app.post("/courses/")
def create_course(course: Course):
    course_dict = course.dict()
    courses_collection.insert_one(course_dict)
    return course_dict

@app.put("/courses/{course_id}")
def update_course(course_id: int, updated_course: Course):
    result = courses_collection.update_one({"id": course_id}, {"$set": updated_course.dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Course not found")
    return updated_course.dict()

@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    result = courses_collection.delete_one({"id": course_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"message": "Course deleted"}

# Classes
@app.get("/classes/")
def read_classes():
    classes = list(classes_collection.find({}))
    for class_ in classes:
        class_["_id"] = serialize_id(class_["_id"])
    return classes

@app.post("/classes/")
def create_class(class_: Class):
    class_dict = class_.dict()
    classes_collection.insert_one(class_dict)
    return class_dict

@app.put("/classes/{class_id}")
def update_class(class_id: int, updated_class: Class):
    result = classes_collection.update_one({"id": class_id}, {"$set": updated_class.dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Class not found")
    return updated_class.dict()

@app.delete("/classes/{class_id}")
def delete_class(class_id: int):
    result = classes_collection.delete_one({"id": class_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Class not found")
    return {"message": "Class deleted"}

# Backup
@app.post("/backup/{entity}")
def backup_data(entity: str):
    if entity not in ["students", "teachers", "courses", "classes"]:
        raise HTTPException(status_code=400, detail="Invalid entity")
    
    collection = {
        "students": students_collection,
        "teachers": teachers_collection,
        "courses": courses_collection,
        "classes": classes_collection
    }[entity]

    data = list(collection.find({}))
    backup_document = {
        "entity": entity,
        "timestamp": datetime.datetime.now(),
        "data": data
    }
    backups_collection.insert_one(backup_document)
    return {"message": f"{entity} backed up successfully"}

@app.get("/backups/")
def get_backups():
    backups = list(backups_collection.find({}))
    for backup in backups:
        backup["_id"] = serialize_id(backup["_id"])
    return backups
