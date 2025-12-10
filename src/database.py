"""In-memory storage for the Student Ambassador API.

This module provides simple data stores for students, applications, negotiations,
and scholarships.  In production, these would be backed by a persistent
database; here we use Python dictionaries and lists for demonstration purposes.
"""

from typing import Dict, List

from datetime import date

from .models import Student, Application, Negotiation, ScholarshipSource


# In-memory stores
students: Dict[str, Student] = {}
applications: List[Application] = []
negotiations: List[Negotiation] = []

# Sample scholarship sources (would come from commons in real implementation)
scholarship_sources: List[ScholarshipSource] = [
    # Note: deadlines must be date objects rather than tuples to satisfy the schema
    ScholarshipSource(
        id="gates",
        name="Gates Scholarship",
        amount_range=[5000, 20000],
        criteria="Low income, leadership",
        deadline=date(2025, 12, 31),
    ),
    ScholarshipSource(
        id="coca_cola",
        name="Coca-Cola Scholars",
        amount_range=[1000, 5000],
        criteria="Community service",
        deadline=date(2025, 12, 15),
    ),
]