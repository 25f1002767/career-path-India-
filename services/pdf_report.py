from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()


def generate_report(user, assessment, recommendations, filename):

    doc = SimpleDocTemplate(filename)

    story = []

    story.append(
        Paragraph(
            "<b>CareerPath India AI Report</b>",
            styles["Title"]
        )
    )

    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            f"Student : {user.username}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Email : {user.email}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Recommended Category : {assessment.recommended_category}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            "<b>Top Career Recommendations</b>",
            styles["Heading2"]
        )
    )

    for item in recommendations:

        story.append(

            Paragraph(

                f"{item['career'].title} ({item['score']}%)",

                styles["Normal"]

            )

        )

    doc.build(story)