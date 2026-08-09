import json
from pathlib import Path


class InternshipService:

    def __init__(self):

        self.path = (
            Path(__file__).resolve().parents[2]
            / "knowledge"
            / "internships"
            / "technology_internships.json"
        )

    # ==========================================
    # Load all internships
    # ==========================================

    def get_all(self):

        if not self.path.exists():

            print("Internship file not found:", self.path)

            return []

        with open(self.path, "r", encoding="utf-8") as f:

            return json.load(f)

    # ==========================================
    # Recommend internships by skills
    # ==========================================

    def recommend(self, skills=None):

        internships = self.get_all()

        if not skills:

            return internships

        skills = [s.lower() for s in skills]

        results = []

        for internship in internships:

            title = internship.get("title", "")

            internship_skills = internship.get("skills", [])

            # Convert list to string if needed
            if isinstance(internship_skills, list):

                skills_text = " ".join(internship_skills)

            else:

                skills_text = str(internship_skills)

            text = f"{title} {skills_text}".lower()

            if any(skill in text for skill in skills):

                results.append(internship)

        return results


internship_service = InternshipService()