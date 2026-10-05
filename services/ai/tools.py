from typing import Dict, Any, List, Optional
import json
from services.ai.retriever import MPathRetriever
from models.user import User
from models.assessment import AssessmentResult
from models.career import Career
from models.college import College
from models.course import Course
from models.exam import GovernmentExam
from models.scholarship import Scholarship
from models.chat import StudentMemory
from extensions import db


# OpenAI Tool Definitions
OPENAI_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_careers",
            "description": "Search verified careers in MPath database with optional stream and negative keyword filters (e.g., exclude engineering, exclude coding).",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Keywords or career domain (e.g., 'mathematics data', 'healthcare', 'finance')"},
                    "stream": {"type": "string", "description": "Student stream if applicable, e.g. 'Science (PCM)', 'Commerce', 'Arts'"},
                    "negative_keywords": {"type": "array", "items": {"type": "string"}, "description": "Terms to strictly exclude, e.g. ['engineering', 'coding']"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_career_details",
            "description": "Retrieve comprehensive details for a specific career including skills, degrees, top colleges, exams, and roadmap.",
            "parameters": {
                "type": "object",
                "properties": {
                    "career_identifier": {"type": "string", "description": "Career title, slug, or ID"}
                },
                "required": ["career_identifier"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_courses",
            "description": "Search Indian degree programs and courses relevant to a domain or stream.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Degree name or subject, e.g. 'BCA', 'B.Sc Mathematics', 'Data Analytics'"},
                    "stream": {"type": "string", "description": "Class 12 stream"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_colleges",
            "description": "Find top accredited Indian colleges for a particular course, state, or NIRF ranking.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "College name or keyword"},
                    "state": {"type": "string", "description": "Indian state or union territory, e.g. 'Madhya Pradesh', 'Delhi'"},
                    "course_name": {"type": "string", "description": "Course name, e.g. 'BCA', 'B.Sc Statistics'"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_exams",
            "description": "Search verified entrance and competitive government exams in India.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Exam name or category, e.g. 'UPSC', 'SSC', 'CUET', 'Banking'"},
                    "stream": {"type": "string", "description": "Academic stream"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_scholarships",
            "description": "Find verified government and private scholarships matching student criteria.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Scholarship name or category"},
                    "state": {"type": "string", "description": "State of domicile"},
                    "education_level": {"type": "string", "description": "e.g. 'Class 12', 'Undergraduate'"},
                    "income_limit": {"type": "number", "description": "Annual family income limit in INR"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_internships",
            "description": "Find student internship and trainee opportunities across tech, business, and non-profit sectors.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Role or keywords, e.g. 'Data Analyst Intern', 'Content Writer'"},
                    "domain": {"type": "string", "description": "Sector or industry domain"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compare_careers",
            "description": "Perform an in-depth side-by-side comparison of 2 or 3 careers regarding duration, difficulty, income, stability, and growth.",
            "parameters": {
                "type": "object",
                "properties": {
                    "career_titles": {"type": "array", "items": {"type": "string"}, "description": "Names of careers to compare"}
                },
                "required": ["career_titles"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_student_preference",
            "description": "Record a persistent student preference, constraint, or anti-preference (e.g. location limit, dislike of coding).",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "enum": ["negative_preference", "location", "preference", "constraint", "goal"]},
                    "key": {"type": "string", "description": "Identifier key, e.g. 'dislike_sales', 'location_limit'"},
                    "value": {"type": "string", "description": "Specific value or explanation"},
                    "confidence": {"type": "string", "enum": ["low", "medium", "high"]}
                },
                "required": ["category", "key", "value"]
            }
        }
    }
]


class ToolExecutor:
    """
    Executes tool calls against authentic MPath databases.
    """

    @classmethod
    def execute(cls, tool_name: str, args: Dict[str, Any], user_id: Optional[int] = None, session_id: Optional[str] = None) -> Any:
        try:
            if tool_name == "search_careers":
                return MPathRetriever.search_careers(
                    query=args.get("query", ""),
                    stream=args.get("stream"),
                    negative_keywords=args.get("negative_keywords"),
                    limit=5
                )

            elif tool_name == "get_career_details":
                ident = args.get("career_identifier", "")
                details = MPathRetriever.get_career_details(ident)
                if not details:
                    # Try searching for closest match
                    sim = MPathRetriever.search_careers(query=ident, limit=1)
                    if sim:
                        details = MPathRetriever.get_career_details(sim[0]["slug"])
                return details or {"status": "not_found", "message": f"No career dossier found for '{ident}'"}

            elif tool_name == "search_courses":
                return MPathRetriever.search_courses(
                    query=args.get("query", ""),
                    stream=args.get("stream"),
                    limit=5
                )

            elif tool_name == "search_colleges":
                return MPathRetriever.search_colleges(
                    query=args.get("query", ""),
                    state=args.get("state"),
                    course_name=args.get("course_name"),
                    limit=5
                )

            elif tool_name == "search_exams":
                return MPathRetriever.search_exams(
                    query=args.get("query", ""),
                    stream=args.get("stream"),
                    limit=5
                )

            elif tool_name == "search_scholarships":
                return MPathRetriever.search_scholarships(
                    query=args.get("query", ""),
                    state=args.get("state"),
                    education_level=args.get("education_level"),
                    income_limit=args.get("income_limit"),
                    limit=5
                )

            elif tool_name == "search_internships":
                return MPathRetriever.search_internships(
                    query=args.get("query", ""),
                    domain=args.get("domain"),
                    limit=5
                )

            elif tool_name == "compare_careers":
                titles = args.get("career_titles", [])
                comparison = []
                for title in titles[:3]:
                    c = Career.query.filter(Career.title.ilike(f"%{title}%")).first()
                    if c:
                        comparison.append({
                            "title": c.title,
                            "category": c.category,
                            "education": c.education_required or c.minimum_qualification,
                            "salary": c.average_salary or "Competitive",
                            "work_modes": c.work_modes,
                            "future_scope": c.future_scope,
                            "url": f"/careers/{c.slug}"
                        })
                return comparison

            elif tool_name == "save_student_preference":
                cat = args.get("category", "preference")
                key = args.get("key", "general")
                val = str(args.get("value", ""))
                conf = args.get("confidence", "medium")

                existing = StudentMemory.query.filter_by(
                    user_id=user_id,
                    session_id=session_id if not user_id else None,
                    category=cat,
                    key=key
                ).first()

                if existing:
                    existing.value = val
                    existing.confidence = conf
                else:
                    mem = StudentMemory(
                        user_id=user_id,
                        session_id=session_id if not user_id else None,
                        category=cat,
                        key=key,
                        value=val,
                        confidence=conf,
                        source="chat"
                    )
                    db.session.add(mem)
                db.session.commit()
                return {"status": "success", "recorded": f"{key} = {val}"}

            else:
                return {"error": f"Unknown tool: {tool_name}"}

        except Exception as e:
            return {"error": f"Tool execution error: {str(e)}"}
