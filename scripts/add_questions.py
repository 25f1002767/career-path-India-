import sys
from pathlib import Path

# Add project root to Python path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from app import app
from extensions import db
from models.question import AssessmentQuestion


questions = [

    {
        "question": "What kind of activity gives you the most satisfaction?",
        "category": "Technology",
        "option_a": "Building apps, websites, or solving technical problems",
        "option_b": "Helping people improve their health",
        "option_c": "Managing money, business, or marketing",
        "option_d": "Serving society through administration or public service"
    },

    {
        "question": "Which subject would you choose even if there were no exams?",
        "category": "Technology",
        "option_a": "Computer Science / Mathematics",
        "option_b": "Biology / Psychology",
        "option_c": "Commerce / Economics",
        "option_d": "Political Science / History / Civics"
    },

    {
        "question": "How do your friends usually describe you?",
        "category": "Business",
        "option_a": "Logical and analytical",
        "option_b": "Caring and supportive",
        "option_c": "Confident and persuasive",
        "option_d": "Responsible and disciplined"
    },

    {
        "question": "Which future sounds most exciting to you?",
        "category": "Technology",
        "option_a": "Working in AI, software, cybersecurity, or data science",
        "option_b": "Becoming a doctor, nurse, physiotherapist, or healthcare expert",
        "option_c": "Starting a company or becoming a business leader",
        "option_d": "Becoming an IAS officer, police officer, or government administrator"
    },

    {
        "question": "What type of problems do you enjoy solving?",
        "category": "Technology",
        "option_a": "Technical and logical problems",
        "option_b": "Human and health-related problems",
        "option_c": "Financial and business problems",
        "option_d": "Social and governance problems"
    }

]


with app.app_context():

    # Remove old questions
    AssessmentQuestion.query.delete()

    # Add new questions
    for q in questions:
        db.session.add(
            AssessmentQuestion(**q)
        )

    db.session.commit()

    print("Smart assessment questions added successfully!")