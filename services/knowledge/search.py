import json

from services.knowledge.loader import KnowledgeLoader


class KnowledgeSearch:

    def __init__(self):

        self.loader = KnowledgeLoader()

    # ==========================================
    # Search Everywhere
    # ==========================================

    def search(self, keyword):

        keyword = keyword.lower()

        results = []

        collections = [

            self.loader.careers(),

            self.loader.colleges(),

            self.loader.scholarships(),

            self.loader.exams(),

            self.loader.internships(),

            self.loader.courses(),

            self.loader.skills(),

            self.loader.roadmaps()

        ]

        for collection in collections:

            for item in collection:

                text = json.dumps(item).lower()

                if keyword in text:

                    results.append(item)

        return results

    # ==========================================
    # Search Careers Only
    # ==========================================

    def careers(self, keyword):

        keyword = keyword.lower()

        results = []

        for career in self.loader.careers():

            text = json.dumps(career).lower()

            if keyword in text:

                results.append(career)

        return results

    # ==========================================
    # Search Scholarships
    # ==========================================

    def scholarships(self, keyword):

        keyword = keyword.lower()

        results = []

        for item in self.loader.scholarships():

            text = json.dumps(item).lower()

            if keyword in text:

                results.append(item)

        return results

    # ==========================================
    # Search Colleges
    # ==========================================

    def colleges(self, keyword):

        keyword = keyword.lower()

        results = []

        for item in self.loader.colleges():

            text = json.dumps(item).lower()

            if keyword in text:

                results.append(item)

        return results


knowledge_search = KnowledgeSearch()