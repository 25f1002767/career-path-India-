import json
from pathlib import Path


class ScholarshipService:

    def __init__(self):

        self.file_path = Path(
            "knowledge/scholarships/all_india_scholarships.json"
        )

    def get_all(self):

        if not self.file_path.exists():

            return []

        with open(
            self.file_path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def search(self, keyword=""):

        scholarships = self.get_all()

        if not keyword:

            return scholarships

        keyword = keyword.lower()

        results = []

        for s in scholarships:

            text = (

                s["title"] + " " +

                s["provider"] + " " +

                s["category"] + " " +

                s["description"]

            ).lower()

            if keyword in text:

                results.append(s)

        return results


scholarship_service = ScholarshipService()