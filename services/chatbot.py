from models.career import Career


def get_response(message):

    text = message.lower()

    careers = Career.query.all()

    # Search by career title
    for career in careers:

        if career.title.lower() in text:

            return f"""
Career: {career.title}

Category: {career.category}

Education:
{career.education_required}

Skills:
{career.skills_required}

Average Salary:
{career.average_salary}

Future Scope:
{career.future_scope}
"""

    # Search by category
    categories = [
        "technology",
        "medical",
        "business",
        "government",
        "creative"
    ]

    for category in categories:

        if category in text:

            result = Career.query.filter_by(
                category=category.capitalize()
            ).all()

            if result:

                reply = f"Top careers in {category.title()}:\n\n"

                for c in result:

                    reply += f"• {c.title}\n"

                return reply

    return "Sorry, I couldn't understand your question. Try asking about careers, skills, salary, education or categories."