import json
from pathlib import Path

from services.knowledge.loader import KnowledgeLoader


class CareerService:

    def __init__(self):

        self.loader = KnowledgeLoader()

        # Correct folder path
        self.base_path = (
            Path(__file__).resolve().parents[2]
            / "knowledge"
            / "careers"
        )

    # ======================================
    # Normalize Career Data
    # ======================================

    def normalize(self, career):

        # Description
        if "description" not in career:

            career["description"] = career.get(
                "overview",
                ""
            )

        # Average Salary
        if "average_salary" not in career:

            salary = career.get("salary", {})

            career["average_salary"] = {

                "fresher": salary.get(
                    "entry",
                    "Not Available"
                ),

                "experienced": salary.get(
                    "mid",
                    "Not Available"
                ),

                "international": salary.get(
                    "senior",
                    "Not Available"
                )

            }

        # Education
        if "education" not in career:

            career["education"] = {

                "minimum": career.get(
                    "education_required",
                    "Not Available"
                )

            }

        # Skills
        if "skills" not in career:

            career["skills"] = {

                "technical": career.get(
                    "required_skills",
                    []
                )

            }

        # Slug
        if "slug" not in career:

            career["slug"] = (

                career["title"]

                .lower()

                .replace(" ", "-")

            )

        return career

    # ======================================
    # Get All Careers
    # ======================================

    def get_all(self):

        careers = []

        if not self.base_path.exists():

            print("Career folder not found:", self.base_path)

            return []

        for file in self.base_path.rglob("*.json"):

            # Skip template and schema files
            if "template" in file.name.lower():
                continue

            if "schema" in file.name.lower():
                continue

            try:

                with open(
                    file,
                    "r",
                    encoding="utf-8"
                ) as f:

                    data = json.load(f)

                # Single career object
                if isinstance(data, dict):

                    careers.append(
                        self.normalize(data)
                    )

                # Multiple career objects
                elif isinstance(data, list):

                    for item in data:

                        if isinstance(item, dict):

                            careers.append(
                                self.normalize(item)
                            )

            except Exception as e:

                print("ERROR:", file)

                print(e)

        return careers

    # ======================================
    # Search Careers
    # ======================================

    def search(
        self,
        keyword=None,
        category=None
    ):

        careers = self.get_all()

        results = []

        for career in careers:

            text = (

                career.get("title", "")

                + " "

                + career.get("description", "")

            ).lower()

            if keyword:

                if keyword.lower() not in text:
                    continue

            if category:

                if career.get("category", "").lower() != category.lower():
                    continue

            results.append(career)

        return results

    # ======================================
    # Get Career by Slug
    # ======================================

    def get_by_slug(self, slug):

        for career in self.get_all():

            if career.get("slug") == slug:

                return career

        return None

    # ======================================
    # Categories
    # ======================================

    def categories(self):

        return sorted(

            list(

                {

                    c.get("category", "Other")

                    for c in self.get_all()

                }

            )

        )


career_service = CareerService()