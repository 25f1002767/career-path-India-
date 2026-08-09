import json
from pathlib import Path


class ExamService:

    def __init__(self):

        self.file_path = (
            Path(__file__).resolve().parents[2]
            / "knowledge"
            / "exams"
            / "all_india_exams.json"
        )

    # ======================================
    # Get All Exams
    # ======================================

    def get_all(self):

        if not self.file_path.exists():

            print("Exam file not found:", self.file_path)

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

            print("Error loading exams:", e)

            return []

    # ======================================
    # Search Exams
    # ======================================

    def search(self, keyword=""):

        exams = self.get_all()

        if not keyword:

            return exams

        keyword = keyword.lower()

        results = []

        for exam in exams:

            text = " ".join([

                exam.get("name", ""),
                exam.get("category", ""),
                exam.get("eligibility", ""),
                exam.get("description", "")

            ]).lower()

            if keyword in text:

                results.append(exam)

        return results

    # ======================================
    # Recommend Exams by Qualification
    # ======================================

    def recommend(self, qualification=""):

        exams = self.get_all()

        if not qualification:

            return exams

        qualification = qualification.lower()

        results = []

        for exam in exams:

            eligibility = exam.get(
                "eligibility",
                ""
            ).lower()

            if qualification in eligibility:

                results.append(exam)

        # If nothing matches, return all exams

        if not results:

            return exams

        return results

    # ======================================
    # Get Exams by Category
    # ======================================

    def by_category(self, category):

        return [

            e for e in self.get_all()

            if e.get("category", "").lower() == category.lower()

        ]


exam_service = ExamService()