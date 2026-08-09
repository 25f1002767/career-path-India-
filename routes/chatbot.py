from flask import Blueprint, render_template, request, session

from services.ai.copilot import career_copilot
from flask import Blueprint, request, jsonify
from services.chatbot_service import ask_ai

chatbot = Blueprint("chatbot", __name__, url_prefix="/chatbot")


@chatbot.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    prompt = data.get("message", "")

    answer = ask_ai(prompt)

    return jsonify({
        "answer": answer
    })

chatbot = Blueprint(
    "chatbot",
    __name__,
    url_prefix="/chatbot"
)


@chatbot.route("/", methods=["GET", "POST"])
def home():

    guidance = None

    if request.method == "POST":

        question = request.form.get("question")

        if question:

            # Logged-in user
            if "user_id" in session:

                guidance = career_copilot(
                    session["user_id"],
                    question
                )

            # Guest user
            else:

                guidance = career_copilot(
                    None,
                    question
                )

    return render_template(
        "chatbot/index.html",
        guidance=guidance
    )