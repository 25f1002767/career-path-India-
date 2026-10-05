import json
import re
from typing import Dict, Any, List, Optional
from extensions import db
from models.chat import ChatConversation, ChatMessage, StudentMemory


class MemoryManager:
    """
    Handles conversational state, pronoun resolution, selective long-term memory,
    and structured conversation summaries.
    """

    PRONOUNS_MAP = {
        "it": "active_subject",
        "its": "active_subject",
        "this": "active_subject",
        "these": "active_subject",
        "that": "active_subject",
        "iska": "active_subject",
        "iski": "active_subject",
        "isme": "active_subject",
        "usme": "active_subject"
    }

    @classmethod
    def resolve_references(cls, message: str, state: Dict[str, Any]) -> str:
        """
        Resolves ambiguous pronouns to their active conversational referents.
        e.g., 'What about its fees?' when active_subject='BCA' ->
        'What about BCA fees?' (for internal semantic understanding).
        """
        active_subject = state.get("active_subject") or state.get("current_career") or state.get("current_course")
        if not active_subject:
            return message

        msg_lower = message.lower()
        # If message is very short or contains references without naming a subject
        needs_context = any(re.search(r'\b' + re.escape(p) + r'\b', msg_lower) for p in cls.PRONOUNS_MAP.keys())
        if needs_context and not any(k in msg_lower for k in [active_subject.lower()]):
            return f"{message} (context: referring to {active_subject})"
        return message

    @classmethod
    def update_state_from_turn(cls, conversation: ChatConversation, user_message: str, response_text: str, metadata: Dict[str, Any] = None):
        """
        Updates the active conversational focus (subject, career, course, exam) in state_json.
        """
        state = conversation.get_state()
        metadata = metadata or {}

        # If careers were discussed, update active career
        if metadata.get("careers"):
            state["current_career"] = metadata["careers"][0].get("title")
            state["active_subject"] = state["current_career"]

        # If courses were discussed
        if metadata.get("courses"):
            state["current_course"] = metadata["courses"][0].get("name")
            if not metadata.get("careers"):
                state["active_subject"] = state["current_course"]

        # If exams were discussed
        if metadata.get("exams"):
            state["current_exam"] = metadata["exams"][0].get("name")

        # Check for stream in user message
        msg_l = user_message.lower()
        if "pcm" in msg_l:
            state["stream"] = "Science (PCM)"
        elif "pcb" in msg_l:
            state["stream"] = "Science (PCB)"
        elif "commerce" in msg_l:
            state["stream"] = "Commerce"
        elif "arts" in msg_l:
            state["stream"] = "Arts"

        conversation.set_state(state)
        db.session.commit()

    @classmethod
    def extract_and_store_memories(cls, user_id: Optional[int], session_id: Optional[str], message: str, analysis: Dict[str, Any]):
        """
        Selectively persists high-value preferences, constraints, and negative preferences.
        """
        # Negative preferences
        negatives = analysis.get("negative_preferences", [])
        for neg in negatives:
            cls._upsert_memory(
                user_id=user_id,
                session_id=session_id,
                category="negative_preference",
                key=f"dislikes_{neg.lower()}",
                value=f"Prefers not to pursue {neg}",
                confidence="high",
                source="chat"
            )

        # Stream
        streams = analysis.get("streams", [])
        for s in streams:
            cls._upsert_memory(
                user_id=user_id,
                session_id=session_id,
                category="education",
                key="academic_stream",
                value=s,
                confidence="high",
                source="chat"
            )

        # Constraints
        constraints = analysis.get("constraints", {})
        if constraints.get("earn_early"):
            cls._upsert_memory(
                user_id=user_id,
                session_id=session_id,
                category="constraint",
                key="earning_timeline",
                value="Prefers to start earning early",
                confidence="high",
                source="chat"
            )
        if constraints.get("stability"):
            cls._upsert_memory(
                user_id=user_id,
                session_id=session_id,
                category="preference",
                key="work_value",
                value="High priority on career stability",
                confidence="high",
                source="chat"
            )
        if constraints.get("government_preference"):
            cls._upsert_memory(
                user_id=user_id,
                session_id=session_id,
                category="preference",
                key="sector_preference",
                value="Government sector",
                confidence="medium",
                source="chat"
            )

    @classmethod
    def _upsert_memory(cls, user_id, session_id, category, key, value, confidence, source):
        try:
            mem = StudentMemory.query.filter_by(
                user_id=user_id,
                session_id=session_id if not user_id else None,
                category=category,
                key=key
            ).first()

            if mem:
                mem.value = value
                mem.confidence = confidence
            else:
                mem = StudentMemory(
                    user_id=user_id,
                    session_id=session_id if not user_id else None,
                    category=category,
                    key=key,
                    value=value,
                    confidence=confidence,
                    source=source
                )
                db.session.add(mem)
            db.session.commit()
        except Exception:
            db.session.rollback()

    @classmethod
    def get_memories_summary(cls, user_id: Optional[int], session_id: Optional[str]) -> List[str]:
        """
        Returns compact list of verified long-term facts about the student.
        """
        mems = StudentMemory.query.filter(
            (StudentMemory.user_id == user_id) if user_id else (StudentMemory.session_id == session_id)
        ).all()

        summary = []
        for m in mems:
            summary.append(f"[{m.category.upper()}]: {m.value} (Confidence: {m.confidence})")
        return summary
