import json
from pathlib import Path


class CollegeService:

    def __init__(self):

        self.file_path = (
            Path(__file__).resolve().parents[2]
            / "knowledge"
            / "colleges"
            / "top_india_colleges.json"
        )

    # ======================================
    # Get All Colleges
    # ======================================

    def get_all(self):

        if not self.file_path.exists():

            print("College file not found:", self.file_path)

            return []

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

                if isinstance(data, list):

                    return data

                return []

        except Exception as e:

            print("Error loading colleges:", e)

            return []

    # ======================================
    # Search Colleges
    # ======================================

    def search(self, keyword=""):

        colleges = self.get_all()

        if not keyword:

            return colleges

        keyword = keyword.lower()

        results = []

        for c in colleges:

            text = " ".join([

                c.get("name", ""),
                c.get("course", ""),
                c.get("city", ""),
                c.get("state", ""),
                c.get("description", "")

            ]).lower()

            if keyword in text:

                results.append(c)

        return results

    # ======================================
    # Recommend Colleges for Career
    # ======================================

    def recommend_for_career(self, career_title):

        colleges = self.get_all()

        career_title = career_title.lower()

        results = []

        for c in colleges:

            course = c.get("course", "").lower()

            desc = c.get("description", "").lower()

            if career_title in course or career_title in desc:

                results.append(c)

        return results[:20]

    # ======================================
    # Get Colleges by State
    # ======================================

    def by_state(self, state):

        return [

            c for c in self.get_all()

            if c.get("state", "").lower() == state.lower()

        ]

    # ======================================
    # Get Colleges by Course
    # ======================================

    def by_course(self, course):

        return [

            c for c in self.get_all()

            if course.lower() in c.get("course", "").lower()

        ]


college_service = CollegeService()