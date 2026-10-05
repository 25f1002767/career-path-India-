import uuid
from flask import Blueprint, render_template, request, session, jsonify, Response
from extensions import db
from models.chat import ChatConversation, ChatMessage
from services.ai.reasoning_engine import CareerReasoningEngine
from services.ai.context_builder import build_student_context

chatbot = Blueprint("chatbot", __name__, url_prefix="/chatbot")


def get_or_create_session_id():
    if "chat_session_id" not in session:
        session["chat_session_id"] = str(uuid.uuid4())
    return session["chat_session_id"]


@chatbot.route("/", methods=["GET"])
def home():
    """
    Renders the modern, full-featured MPath AI Career Mentor interface.
    """
    user_id = session.get("user_id")
    sess_id = get_or_create_session_id()

    # Fetch user's conversation threads
    query = ChatConversation.query.filter_by(is_archived=False)
    if user_id:
        query = query.filter((ChatConversation.user_id == user_id) | (ChatConversation.session_id == sess_id))
    else:
        query = query.filter_by(session_id=sess_id)

    conversations = query.order_by(ChatConversation.updated_at.desc()).all()
    student_ctx = build_student_context(user_id=user_id, session_id=sess_id)

    return render_template(
        "chatbot/index.html",
        conversations=conversations,
        student_context=student_ctx
    )


@chatbot.route("/conversations", methods=["GET"])
def list_conversations():
    """
    Returns list of conversations for current user/session.
    """
    user_id = session.get("user_id")
    sess_id = get_or_create_session_id()

    query = ChatConversation.query.filter_by(is_archived=False)
    if user_id:
        query = query.filter((ChatConversation.user_id == user_id) | (ChatConversation.session_id == sess_id))
    else:
        query = query.filter_by(session_id=sess_id)

    convs = query.order_by(ChatConversation.updated_at.desc()).all()
    return jsonify([c.to_dict() for c in convs])


@chatbot.route("/conversations", methods=["POST"])
def create_conversation():
    """
    Explicitly starts a new conversation thread.
    """
    user_id = session.get("user_id")
    sess_id = get_or_create_session_id()
    data = request.get_json(silent=True) or {}
    title = data.get("title", "New Career Exploration").strip() or "New Career Exploration"

    conv = ChatConversation(
        user_id=user_id,
        session_id=sess_id,
        title=title
    )
    db.session.add(conv)
    db.session.commit()
    return jsonify(conv.to_dict()), 201


@chatbot.route("/conversations/<int:conv_id>", methods=["GET"])
def get_conversation(conv_id):
    """
    Retrieves full message history of a specific conversation.
    """
    user_id = session.get("user_id")
    sess_id = get_or_create_session_id()

    conv = ChatConversation.query.get_or_404(conv_id)
    # Check ownership
    if conv.user_id and conv.user_id != user_id and conv.session_id != sess_id:
        return jsonify({"error": "Unauthorized"}), 403

    messages = [m.to_dict() for m in conv.messages]
    return jsonify({
        "conversation": conv.to_dict(),
        "messages": messages
    })


@chatbot.route("/conversations/<int:conv_id>", methods=["PATCH"])
def rename_conversation(conv_id):
    """
    Renames a conversation thread.
    """
    user_id = session.get("user_id")
    sess_id = get_or_create_session_id()

    conv = ChatConversation.query.get_or_404(conv_id)
    if conv.user_id and conv.user_id != user_id and conv.session_id != sess_id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json(silent=True) or {}
    new_title = data.get("title", "").strip()
    if new_title:
        conv.title = new_title[:180]
        db.session.commit()

    return jsonify(conv.to_dict())


@chatbot.route("/conversations/<int:conv_id>", methods=["DELETE"])
def delete_conversation(conv_id):
    """
    Deletes or archives a conversation thread.
    """
    user_id = session.get("user_id")
    sess_id = get_or_create_session_id()

    conv = ChatConversation.query.get_or_404(conv_id)
    if conv.user_id and conv.user_id != user_id and conv.session_id != sess_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(conv)
    db.session.commit()
    return jsonify({"status": "deleted", "id": conv_id})


@chatbot.route("/ask", methods=["POST"])
def ask():
    """
    Non-streaming endpoint returning full response with structured metadata cards.
    """
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    conv_id = data.get("conversation_id")

    if not message:
        return jsonify({"error": "Please provide a career inquiry."}), 400

    user_id = session.get("user_id")
    sess_id = get_or_create_session_id()

    try:
        result = CareerReasoningEngine.generate_response(
            user_message=message,
            user_id=user_id,
            session_id=sess_id,
            conversation_id=conv_id
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "answer": "Your MPath Career Mentor is temporarily unable to formulate a response. Please try asking again.",
            "error": str(e),
            "metadata": {
                "careers": [],
                "courses": [],
                "colleges": [],
                "exams": [],
                "scholarships": [],
                "internships": [],
                "actions": [],
                "sources": []
            }
        }), 500


@chatbot.route("/stream", methods=["GET"])
def stream():
    """
    Server-Sent Events (SSE) streaming endpoint.
    Streams incremental text chunks followed by verified metadata cards.
    """
    message = request.args.get("message", "").strip()
    conv_id = request.args.get("conversation_id", type=int)

    if not message:
        return jsonify({"error": "Missing message parameter"}), 400

    user_id = session.get("user_id")
    sess_id = get_or_create_session_id()

    return Response(
        CareerReasoningEngine.stream_response(
            user_message=message,
            user_id=user_id,
            session_id=sess_id,
            conversation_id=conv_id
        ),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


@chatbot.route("/feedback", methods=["POST"])
def feedback():
    """
    Records student feedback (thumbs up/down) for continuous quality improvement.
    """
    data = request.get_json(silent=True) or {}
    message_id = data.get("message_id")
    sentiment = data.get("sentiment")  # "positive", "negative"

    if message_id and sentiment in ["positive", "negative"]:
        msg = ChatMessage.query.get(message_id)
        if msg:
            meta = msg.get_metadata()
            meta["feedback"] = sentiment
            msg.set_metadata(meta)
            db.session.commit()
            return jsonify({"status": "recorded"})

    return jsonify({"status": "ignored"}), 200