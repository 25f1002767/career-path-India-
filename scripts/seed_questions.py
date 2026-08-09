import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

from app import app
from extensions import db
from models.question import AssessmentQuestion

questions = [

{
"question":"Which activity excites you the most?",
"option1":"Build software",
"option2":"Treat patients",
"option3":"Manage people",
"option4":"Design graphics",
"value1":"Technology",
"value2":"Medical",
"value3":"Government",
"value4":"Creative"
},

{
"question":"Which subject do you enjoy the most?",
"option1":"Computer Science",
"option2":"Biology",
"option3":"Political Science",
"option4":"Business Studies",
"value1":"Technology",
"value2":"Medical",
"value3":"Government",
"value4":"Business"
},

{
"question":"How do you solve problems?",
"option1":"Using technology",
"option2":"Helping people",
"option3":"Following rules",
"option4":"Creating something new",
"value1":"Technology",
"value2":"Medical",
"value3":"Government",
"value4":"Creative"
}

]

with app.app_context():

    AssessmentQuestion.query.delete()

    for q in questions:

        db.session.add(
            AssessmentQuestion(**q)
        )

    db.session.commit()

    print("Questions Imported Successfully")