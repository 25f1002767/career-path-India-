import os
import sys

# Ensure application root in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app
from extensions import db
from services.sources.statutory_ingest import StatutoryOpportunityIngestor
from models.opportunity_source import OpportunitySource
from models.exam import GovernmentExam
from models.exam_cycle import ExamCycle

with app.app_context():
    print("Beginning authoritative statutory opportunity sync...")
    results = StatutoryOpportunityIngestor.ingest_master_catalog()
    print("Ingestion results:", results)

    # Let's verify stats
    src_count = OpportunitySource.query.count()
    exam_count = GovernmentExam.query.count()
    cycle_count = ExamCycle.query.count()
    print(f"Total Sources in DB: {src_count}")
    print(f"Total Exams/Opportunities in DB: {exam_count}")
    print(f"Total Exam Cycles in DB: {cycle_count}")
