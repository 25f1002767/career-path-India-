import re
from typing import Dict, Any, List, Tuple
from models.career import Career
from models.course import Course
from models.college import College
from models.exam import GovernmentExam
from models.scholarship import Scholarship
from models.internship import Internship


class GroundingVerifier:
    """
    Validates mentioned entities against authentic MPath databases,
    cleans decorative artifacts, and generates verified navigation actions.
    """

    @classmethod
    def clean_text(cls, text: str) -> str:
        """
        Removes decorative stars, repeated sparkles, and excessive formatting artifacts.
        """
        if not text:
            return ""

        # Remove repeated stars or sparkles
        cleaned = re.sub(r'[\u2b50\u2605\U0001f31f\u2728]{2,}', '', text)
        # Remove single leading stars in headings
        cleaned = re.sub(r'^[\u2b50\u2605\U0001f31f\u2728]\s*', '', cleaned, flags=re.MULTILINE)
        # Normalize double blank lines
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        return cleaned.strip()

    @classmethod
    def verify_and_enrich(cls, text: str, tool_results: List[Dict[str, Any]] = None) -> Tuple[str, Dict[str, Any]]:
        """
        Scans text and tool results for genuine MPath entities and produces
        verified structured action cards and sources.
        """
        cleaned_text = cls.clean_text(text)
        tool_results = tool_results or []

        matched_careers = []
        matched_courses = []
        matched_colleges = []
        matched_exams = []
        matched_scholarships = []
        matched_internships = []
        actions = []
        sources = set()

        # 1. Process tool results first (they are already verified database records)
        for item in tool_results:
            if not isinstance(item, dict):
                continue

            # Career
            if "slug" in item and "category" in item and "title" in item:
                if not any(c["id"] == item["id"] for c in matched_careers):
                    matched_careers.append(item)
                    actions.append({
                        "label": f"Explore {item['title']}",
                        "url": f"/careers/{item['slug']}",
                        "type": "career",
                        "variant": "primary"
                    })
                    sources.add("MPath Verified National Career Repository (NCS Aligned)")

            # Course
            elif "degree_level" in item and "name" in item:
                if not any(co["id"] == item["id"] for co in matched_courses):
                    matched_courses.append(item)
                    actions.append({
                        "label": f"Explore {item['name']}",
                        "url": f"/courses/{item['id']}",
                        "type": "course",
                        "variant": "outline-primary"
                    })
                    sources.add("MPath Higher Education Course Directory")

            # College
            elif "nirf_rank" in item or "city" in item:
                if not any(col["id"] == item["id"] for col in matched_colleges):
                    matched_colleges.append(item)
                    actions.append({
                        "label": f"View {item['name']}",
                        "url": f"/colleges/{item['id']}",
                        "type": "college",
                        "variant": "outline-secondary"
                    })
                    sources.add("MPath Verified Accredited College Registry")

            # Exam
            elif "exam_type" in item and "name" in item:
                if not any(ex["id"] == item["id"] for ex in matched_exams):
                    matched_exams.append(item)
                    actions.append({
                        "label": f"Exam Details: {item.get('short_name') or item['name']}",
                        "url": f"/exams/{item['id']}",
                        "type": "exam",
                        "variant": "outline-warning"
                    })
                    sources.add("MPath Government & Entrance Exam Registry")

            # Scholarship
            elif "provider" in item and "title" in item:
                if not any(sc["id"] == item["id"] for sc in matched_scholarships):
                    matched_scholarships.append(item)
                    actions.append({
                        "label": f"Scholarship: {item['title'][:25]}...",
                        "url": item.get("url") or f"/scholarships/{item['id']}",
                        "type": "scholarship",
                        "variant": "outline-success"
                    })
                    sources.add("MPath National & State Scholarship Portal")

            # Internship
            elif "company" in item and "title" in item:
                if not any(ins["id"] == item["id"] for ins in matched_internships):
                    matched_internships.append(item)
                    actions.append({
                        "label": f"Internship: {item['title']}",
                        "url": "/internships/",
                        "type": "internship",
                        "variant": "outline-info"
                    })
                    sources.add("MPath Verified Student Internship Registry")

        # 2. Text-based entity extraction fallback (check against top careers in DB)
        if len(matched_careers) < 3:
            # Check for popular careers mentioned in text
            words_in_text = set(re.findall(r'\b[A-Z][a-zA-Z\s]{3,25}\b', cleaned_text))
            for word in words_in_text:
                w_str = word.strip()
                if len(w_str) > 4:
                    c_match = Career.query.filter(Career.title.ilike(f"{w_str}")).first()
                    if c_match and not any(c["id"] == c_match.id for c in matched_careers):
                        matched_careers.append({
                            "id": c_match.id,
                            "title": c_match.title,
                            "slug": c_match.slug,
                            "category": c_match.category,
                            "average_salary": c_match.average_salary,
                            "url": f"/careers/{c_match.slug}"
                        })
                        actions.append({
                            "label": f"Explore {c_match.title}",
                            "url": f"/careers/{c_match.slug}",
                            "type": "career",
                            "variant": "primary"
                        })
                        sources.add("MPath Verified National Career Repository")

        # Add general actions if relevant
        if any(c in cleaned_text.lower() for c in ["roadmap", "steps", "plan"]) and matched_careers:
            top_career = matched_careers[0]
            actions.append({
                "label": f"Generate Full Roadmap",
                "url": f"/roadmap/{top_career['id']}",
                "type": "roadmap",
                "variant": "success"
            })

        if any(c in cleaned_text.lower() for c in ["compare", "vs", "versus"]):
            actions.append({
                "label": "Open Career Comparison Tool",
                "url": "/careers/compare",
                "type": "tool",
                "variant": "outline-primary"
            })

        metadata = {
            "careers": matched_careers[:4],
            "courses": matched_courses[:3],
            "colleges": matched_colleges[:3],
            "exams": matched_exams[:3],
            "scholarships": matched_scholarships[:3],
            "internships": matched_internships[:3],
            "actions": actions[:6],
            "sources": list(sources) or ["MPath Career Intelligence Knowledgebase 2026"]
        }

        return cleaned_text, metadata
