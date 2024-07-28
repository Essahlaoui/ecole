from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# CORS middleware
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
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
    student_ids: List[int]

# In-memory storage
students = []
teachers = []
courses = []
classes = []

# CRUD operations for Students
@app.get("/students/", response_model=List[Student])
def get_students():
    return students

@app.post("/students/", response_model=Student)
def add_student(student: Student):
    students.append(student)
    return student

@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, updated_student: Student):
    for index, student in enumerate(students):
        if student.id == student_id:
            students[index] = updated_student
            return updated_student
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for index, student in enumerate(students):
        if student.id == student_id:
            del students[index]
            return {"message": "Student deleted"}
    raise HTTPException(status_code=404, detail="Student not found")

# CRUD operations for Teachers
@app.get("/teachers/", response_model=List[Teacher])
def get_teachers():
    return teachers

@app.post("/teachers/", response_model=Teacher)
def add_teacher(teacher: Teacher):
    teachers.append(teacher)
    return teacher

@app.put("/teachers/{teacher_id}", response_model=Teacher)
def update_teacher(teacher_id: int, updated_teacher: Teacher):
    for index, teacher in enumerate(teachers):
        if teacher.id == teacher_id:
            teachers[index] = updated_teacher
            return updated_teacher
    raise HTTPException(status_code=404, detail="Teacher not found")

@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int):
    for index, teacher in enumerate(teachers):
        if teacher.id == teacher_id:
            del teachers[index]
            return {"message": "Teacher deleted"}
    raise HTTPException(status_code=404, detail="Teacher not found")

# CRUD operations for Courses
@app.get("/courses/", response_model=List[Course])
def get_courses():
    return courses

@app.post("/courses/", response_model=Course)
def add_course(course: Course):
    courses.append(course)
    return course

@app.put("/courses/{course_id}", response_model=Course)
def update_course(course_id: int, updated_course: Course):
    for index, course in enumerate(courses):
        if course.id == course_id:
            courses[index] = updated_course
            return updated_course
    raise HTTPException(status_code=404, detail="Course not found")

@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    for index, course in enumerate(courses):
        if course.id == course_id:
            del courses[index]
            return {"message": "Course deleted"}
    raise HTTPException(status_code=404, detail="Course not found")

# CRUD operations for Classes
@app.get("/classes/", response_model=List[Class])
def get_classes():
    return classes

@app.post("/classes/", response_model=Class)
def add_class(class_: Class):
    classes.append(class_)
    return class_

@app.put("/classes/{class_id}", response_model=Class)
def update_class(class_id: int, updated_class: Class):
    for index, class_ in enumerate(classes):
        if class_.id == class_id:
            classes[index] = updated_class
            return updated_class
    raise HTTPException(status_code=404, detail="Class not found")

@app.delete("/classes/{class_id}")
def delete_class(class_id: int):
    for index, class_ in enumerate(classes):
        if class_.id == class_id:
            del classes[index]
            return {"message": "Class deleted"}
    raise HTTPException(status_code=404, detail="Class not found")
