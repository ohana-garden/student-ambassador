"""Main entry point for the Student Ambassador API.

This module defines the FastAPI application and routes for creating and
retrieving students, applications and negotiation events as described in
the specification.  It uses an in-memory data store from ``database.py``
for demonstration purposes.  In a production deployment the stores
would be replaced with persistent storage.
"""

from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query

from .models import (
    Student,
    Application,
    Negotiation,
    ScholarshipSource,
    ScholarshipMatch,
)
from .database import students, applications, negotiations, scholarship_sources


app = FastAPI(
    title="Student Ambassador API",
    version="0.1.0",
    description=(
        "This API exposes core resources for the Student Ambassador Platform. "
        "It is designed primarily for internal agent access; external clients "
        "should go through the ambassador agent which orchestrates calls and "
        "applies privacy constraints."
    ),
)


@app.post("/students", response_model=Student, status_code=201)
def create_student(student: Student) -> Student:
    """Create a new student profile.

    If a student with the given ID already exists, a 400 error is raised.
    """
    if student.id in students:
        raise HTTPException(status_code=400, detail="Student already exists")
    students[student.id] = student
    return student


@app.get("/students", response_model=List[Student])
def list_students() -> List[Student]:
    """Retrieve a list of all students.

    Intended for authorised agents only.  No filtering is applied.
    """
    return list(students.values())


@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: str) -> Student:
    """Retrieve a single student by their ID.

    Returns 404 if the student does not exist.
    """
    student = students.get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.get(
    "/students/{student_id}/scholarship-matches",
    response_model=List[ScholarshipMatch],
)
def get_scholarship_matches(student_id: str) -> List[ScholarshipMatch]:
    """Generate scholarship matches for the given student.

    In this demonstration implementation, a naive matching algorithm is used
    that assigns a constant match score to each available scholarship source.
    A real implementation would incorporate rules and heuristics to compare
    student data against scholarship criteria and compute a meaningful score.
    """
    # Ensure the student exists
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")

    matches: List[ScholarshipMatch] = []
    # Simple baseline: every scholarship is a full match with a default reason
    for src in scholarship_sources:
        match = ScholarshipMatch(
            source=src,
            match_score=1.0,
            reasons=["Eligible by default in demo implementation"],
        )
        matches.append(match)
    return matches


@app.post("/applications", response_model=Application, status_code=201)
def create_application(application: Application) -> Application:
    """Submit a new application for a student.

    Validates that the referenced student exists and that the application ID
    has not been used previously.  Returns the created application.
    """
    # Validate student exists
    if application.student_id not in students:
        raise HTTPException(status_code=400, detail="Student does not exist")
    # Prevent duplicate IDs
    if any(app.id == application.id for app in applications):
        raise HTTPException(status_code=400, detail="Application ID already exists")
    applications.append(application)
    return application


@app.get("/applications", response_model=List[Application])
def list_applications(student_id: Optional[str] = Query(None)) -> List[Application]:
    """Retrieve a list of applications.

    If ``student_id`` is provided as a query parameter, the list is filtered
    down to only those applications submitted by that student.  Otherwise
    all applications are returned.
    """
    if student_id:
        return [app for app in applications if app.student_id == student_id]
    return applications


@app.post("/negotiations", response_model=Negotiation, status_code=201)
def create_negotiation(negotiation: Negotiation) -> Negotiation:
    """Record a negotiation (e.g. scholarship appeal or aid negotiation).

    Ensures the associated student exists and that the negotiation ID is unique.
    Returns the created negotiation record.
    """
    # Validate student exists
    if negotiation.student_id not in students:
        raise HTTPException(status_code=400, detail="Student does not exist")
    # Prevent duplicate negotiation IDs
    if any(n.id == negotiation.id for n in negotiations):
        raise HTTPException(status_code=400, detail="Negotiation ID already exists")
    negotiations.append(negotiation)
    return negotiation