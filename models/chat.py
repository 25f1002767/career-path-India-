from datetime import datetime
import json
from extensions import db


class ChatConversation(db.Model):
    """
    Represents an ongoing or historical career counselling session.
    """
    __tablename__ = "chat_conversations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)
    session_id = db.Column(db.String(100), nullable=True, index=True)
    title = db.Column(db.String(200), default="Career Exploration Session")
    summary = db.Column(db.Text, nullable=True)
    state_json = db.Column(db.Text, nullable=True)  # JSON: active career, course, exam, constraints
    is_archived = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    messages = db.relationship(
        "ChatMessage",
        backref="conversation",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="ChatMessage.created_at.asc()"
    )

    def get_state(self):
        if not self.state_json:
            return {}
        try:
            return json.loads(self.state_json)
        except Exception:
            return {}

    def set_state(self, state_dict):
        self.state_json = json.dumps(state_dict)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "summary": self.summary or "",
            "created_at": self.created_at.isoformat() if self.created_at else "",
            "updated_at": self.updated_at.isoformat() if self.updated_at else "",
            "message_count": len(self.messages) if self.messages else 0
        }


class ChatMessage(db.Model):
    """
    Individual turn within a career counselling conversation.
    """
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("chat_conversations.id"), nullable=False, index=True)
    role = db.Column(db.String(20), nullable=False)  # "user", "assistant", "system"
    content = db.Column(db.Text, nullable=False)
    metadata_json = db.Column(db.Text, nullable=True)  # Structured cards, actions, sources, intent
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_metadata(self):
        if not self.metadata_json:
            return {}
        try:
            return json.loads(self.metadata_json)
        except Exception:
            return {}

    def set_metadata(self, meta_dict):
        self.metadata_json = json.dumps(meta_dict)

    def to_dict(self):
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "role": self.role,
            "content": self.content,
            "metadata": self.get_metadata(),
            "created_at": self.created_at.isoformat() if self.created_at else ""
        }


class StudentMemory(db.Model):
    """
    Long-term career preferences, constraints, anti-preferences and facts extracted from chats.
    """
    __tablename__ = "student_memories"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)
    session_id = db.Column(db.String(100), nullable=True, index=True)
    category = db.Column(db.String(50), nullable=False, index=True)
    # categories: education, career_interest, career_goal, skill, preference, constraint, negative_preference, decision, location
    key = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Text, nullable=False)
    confidence = db.Column(db.String(20), default="medium")  # low, medium, high
    source = db.Column(db.String(50), default="chat")  # chat, assessment, profile
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "key": self.key,
            "value": self.value,
            "confidence": self.confidence,
            "source": self.source,
            "updated_at": self.updated_at.isoformat() if self.updated_at else ""
        }
