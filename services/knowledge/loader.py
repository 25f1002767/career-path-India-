import json
from pathlib import Path


class KnowledgeLoader:

    def __init__(self):
        self.base_path = (
            Path(__file__).resolve().parents[2]
            / "knowledge"
            / "1"
        )

    def load_json(self, relative_path):
        file_path = self.base_path / relative_path

        if not file_path.exists():
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_folder(self, folder):

        folder_path = self.base_path / folder
        results = []

        if not folder_path.exists():
            return results

        for file in folder_path.rglob("*.json"):

            if "template" in file.name.lower():
                continue

            if "schema" in file.name.lower():
                continue

            try:
                with open(file, "r", encoding="utf-8") as f:
                    results.append(json.load(f))

            except Exception as e:
                print("\nERROR FILE:", file)
                print(e)

        return results

    def careers(self):
        return self.load_folder("careers")

    def colleges(self):
        return self.load_folder("colleges")

    def scholarships(self):
        return self.load_folder("scholarships")

    def exams(self):
        return self.load_folder("government_exams")

    def internships(self):
        return self.load_folder("internships")

    def courses(self):
        return self.load_folder("courses")

    def skills(self):
        return self.load_folder("skills")

    def roadmaps(self):
        return self.load_folder("roadmaps")