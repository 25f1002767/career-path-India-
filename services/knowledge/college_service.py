import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class CollegeService:
    def __init__(self):
        # Resolve project root dynamically
        self.project_root = Path(__file__).resolve().parents[2]
        self.file_path = self.project_root / "knowledge" / "colleges" / "top_india_colleges.json"

    def get_all(self):
        """
        Retrieves colleges from SQLite database if available,
        otherwise falls back to verified JSON dataset.
        """
        try:
            from models.college import College
            from extensions import db
            # If in app context, prefer database records
            colleges = College.query.all()
            if colleges:
                return [
                    {
                        "id": c.id,
                        "name": c.name,
                        "short_name": c.short_name,
                        "city": c.city,
                        "state": c.state,
                        "institution_type": c.institution_type or c.display_type,
                        "government_private": c.government_private or "Government",
                        "course": c.course or "Degree Programs",
                        "fees": c.fees or "As per institutional regulation",
                        "placement": c.placement or "Information not available",
                        "nirf_rank": c.nirf_rank,
                        "official_website": c.display_website,
                        "description": c.description or "Accredited higher education institution in India."
                    }
                    for c in colleges
                ]
        except Exception as e:
            logger.debug("Database not available for CollegeService, falling back to JSON: %s", e)

        if not self.file_path.exists():
            logger.warning("College JSON dataset not found at %s", self.file_path)
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception as e:
            logger.error("Error loading colleges JSON: %s", e)
            return []

    def search(self, keyword=""):
        colleges = self.get_all()
        if not keyword:
            return colleges

        keyword = keyword.lower()
        results = []
        for c in colleges:
            text = " ".join([
                c.get("name") or "",
                c.get("course") or "",
                c.get("city") or "",
                c.get("state") or "",
                c.get("description") or "",
                c.get("institution_type") or ""
            ]).lower()
            if keyword in text:
                results.append(c)
        return results

    def recommend_for_career(self, career_title):
        colleges = self.get_all()
        career_title = career_title.lower()
        results = []
        for c in colleges:
            course = (c.get("course") or "").lower()
            desc = (c.get("description") or "").lower()
            if career_title in course or career_title in desc:
                results.append(c)
        return results[:20]

    def by_state(self, state):
        if not state:
            return self.get_all()
        return [
            c for c in self.get_all()
            if (c.get("state") or "").lower() == state.lower()
        ]

    def by_course(self, course):
        if not course:
            return self.get_all()
        return [
            c for c in self.get_all()
            if course.lower() in (c.get("course") or "").lower()
        ]

college_service = CollegeService()