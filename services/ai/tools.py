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
            "description": "Find verified student internship opportunities across statutory government programs, premier research labs, and corporate drives.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Role, skills, company, or statutory scheme (e.g., 'TULIP', 'DRDO', 'Python', 'Civil')"},
                    "category": {"type": "string", "description": "Sector or domain (e.g., 'Technology', 'Civil & Architecture', 'Finance')"},
                    "mode": {"type": "string", "description": "Work mode: 'Remote', 'Hybrid', 'Onsite'"},
                    "org_type": {"type": "string", "description": "Provider type: 'Government', 'Corporate', 'Research', 'PSU'"},
                    "state": {"type": "string", "description": "Indian state or territory"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_internship_details",
            "description": "Retrieve complete structured dossier for a specific internship opportunity including eligibility, stipend, duration, and verified application link.",
            "parameters": {
                "type": "object",
                "properties": {
                    "identifier": {"type": "string", "description": "Internship title, slug, or ID"}
                },
                "required": ["identifier"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_internships_for_student",
            "description": "Deterministic discovery and ranking of verified internships matching student's degree, skills, career goal, and work mode preferences.",
            "parameters": {
                "type": "object",
                "properties": {
                    "degree": {"type": "string", "description": "Current or completed degree, e.g. 'B.Tech CSE', 'B.Sc Mathematics', 'BCA'"},
                    "skills": {"type": "string", "description": "Student skills comma-separated, e.g. 'Python, SQL, Statistics'"},
                    "target_career": {"type": "string", "description": "Career interest, e.g. 'Data Scientist', 'Urban Planner'"},
                    "work_mode": {"type": "string", "description": "'Remote', 'Hybrid', 'Onsite', or 'Any'"},
                    "state": {"type": "string", "description": "Student state or preferred location"}
                },
                "required": []
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
    },
    {
        "type": "function",
        "function": {
            "name": "find_opportunities_for_student",
            "description": "Deterministic discovery of verified Indian examinations, government recruitment, entrance tests, apprenticeships, and opportunities matching a student's education level, stream, state, and age with zero hallucination.",
            "parameters": {
                "type": "object",
                "properties": {
                    "education_level": {"type": "string", "description": "e.g. 'Class 12', 'Graduate / UG', 'Postgraduate'"},
                    "stream": {"type": "string", "description": "e.g. 'Mathematics', 'PCM', 'Commerce', 'PCB', 'Arts'"},
                    "state": {"type": "string", "description": "Indian state or domicile, e.g. 'Madhya Pradesh', 'Delhi'"},
                    "age": {"type": "integer", "description": "Student age in years"},
                    "course": {"type": "string", "description": "Specific degree or course, e.g. 'B.Sc Mathematics', 'BCA', 'B.Tech'"},
                    "category": {"type": "string", "description": "Reservation category if applicable (General, OBC, SC, ST, EWS)"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_exam_details",
            "description": "Retrieve comprehensive structured dossier for an Indian competitive exam or recruitment drive including eligibility criteria, latest exam cycle, syllabus, selection stages, pay scale, and verified official portals.",
            "parameters": {
                "type": "object",
                "properties": {
                    "exam_identifier": {"type": "string", "description": "Exam name, short name, or slug (e.g. 'UPSC CSE', 'MPPSC', 'IIT JAM', 'CSIR NET')"}
                },
                "required": ["exam_identifier"]
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

            elif tool_name == "find_opportunities_for_student":
                return MPathRetriever.discover_opportunities_for_student(
                    education_level=args.get("education_level"),
                    stream=args.get("stream"),
                    state=args.get("state"),
                    age=args.get("age"),
                    category=args.get("category"),
                    course=args.get("course"),
                    limit=6
                )

            elif tool_name == "get_exam_details":
                return MPathRetriever.get_exam_details(args.get("exam_identifier", ""))

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
                    category=args.get("category") or args.get("domain"),
                    mode=args.get("mode"),
                    org_type=args.get("org_type"),
                    state=args.get("state"),
                    limit=5
                )

            elif tool_name == "get_internship_details":
                ident = args.get("identifier", "")
                res = MPathRetriever.get_internship_details(ident)
                return res or {"status": "not_found", "message": f"No internship found for '{ident}'"}

            elif tool_name == "find_internships_for_student":
                profile_payload = {
                    "degree": args.get("degree", "B.Tech"),
                    "skills": args.get("skills", ""),
                    "target_career": args.get("target_career", ""),
                    "work_mode": args.get("work_mode", "Any"),
                    "state": args.get("state", "")
                }
                return MPathRetriever.find_internships_for_student(profile_payload, limit=5)

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
