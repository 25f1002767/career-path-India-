import json
import logging
import time
from typing import Dict, Any, Generator, Optional, List, Tuple

from extensions import db
from models.chat import ChatConversation, ChatMessage
from services.ai.config import (
    AI_MODEL,
    AI_REASONING_MODEL,
    AI_FAST_MODEL,
    GEMINI_MODEL,
    openai_client,
    gemini_client,
    get_available_provider
)
from services.ai.system_prompt import get_master_system_prompt
from services.ai.intent_detector import IntentDetector
from services.ai.retriever import MPathRetriever
from services.ai.tools import OPENAI_TOOLS, ToolExecutor
from services.ai.memory_manager import MemoryManager
from services.ai.context_builder import build_student_context
from services.ai.grounding_verifier import GroundingVerifier

logger = logging.getLogger("mpath.ai.reasoning")


class CareerReasoningEngine:
    """
    Master Career Counselling & Navigation Agent.
    Coordinates intent parsing, targeted database retrieval, tool execution,
    multi-tier LLM generation, grounding verification, and conversation memory.
    """

    @classmethod
    def _execute_targeted_retrieval(cls, analysis: Dict[str, Any], user_message: str, student_context: Dict[str, Any]) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Gathers verified records from MPath database relevant to the user query and intent.
        """
        intent = analysis["primary_intent"]
        negatives = analysis.get("negative_preferences", [])
        stream = student_context.get("stream") or (analysis.get("streams")[0] if analysis.get("streams") else None)
        tool_records = []
        retrieval_text_blocks = []

        # 1. Career Exploration & Recommendations
        if intent in ["CAREER_EXPLORATION", "CAREER_COMPARISON", "CONFUSED_BEGINNER", "FOLLOW_UP"]:
            careers = MPathRetriever.search_careers(
                query=user_message,
                stream=stream,
                negative_keywords=negatives,
                limit=3
            )
            if careers:
                tool_records.extend(careers)
                retrieval_text_blocks.append("Verified Matching MPath Careers:")
                for c in careers:
                    retrieval_text_blocks.append(
                        f"• {c['title']} (Sector: {c['category']}) | Education: {c['education_required']} | Avg Income: {c['average_salary']}\n"
                        f"  Overview: {c['short_description']}\n"
                        f"  Key Skills: {', '.join(c['key_skills'])}"
                    )

        # 2. Course Selection
        if intent in ["COURSE_SELECTION", "CAREER_EXPLORATION"]:
            courses = MPathRetriever.search_courses(query=user_message, stream=stream, limit=3)
            if courses:
                tool_records.extend(courses)
                retrieval_text_blocks.append("\nRelevant Verified Courses / Degrees:")
                for co in courses:
                    retrieval_text_blocks.append(f"• {co['name']} ({co['degree_level']}, {co['duration']}) | Eligibility: {co['eligibility']}")

        # 3. College Search
        if intent in ["COLLEGE_SEARCH"]:
            colleges = MPathRetriever.search_colleges(query=user_message, limit=3)
            if colleges:
                tool_records.extend(colleges)
                retrieval_text_blocks.append("\nTop Accredited Indian Colleges:")
                for col in colleges:
                    retrieval_text_blocks.append(f"• {col['name']} ({col['city']}, {col['state']}) | NIRF Rank: {col['nirf_rank'] or 'N/A'}")

        # 4. Exam Search
        if intent in ["EXAM_SEARCH", "CAREER_EXPLORATION"]:
            exams = MPathRetriever.search_exams(query=user_message, stream=stream, limit=3)
            if exams:
                tool_records.extend(exams)
                retrieval_text_blocks.append("\nVerified Competitive / Entrance Exams:")
                for ex in exams:
                    retrieval_text_blocks.append(f"• {ex['name']} ({ex['short_name']}) | Type: {ex['exam_type']} | Schedule: {ex['exam_date'] or 'Annual'}")

        # 5. Scholarship Search
        if intent in ["SCHOLARSHIP_SEARCH"]:
            scholarships = MPathRetriever.search_scholarships(query=user_message, limit=3)
            if scholarships:
                tool_records.extend(scholarships)
                retrieval_text_blocks.append("\nVerified Scholarships:")
                for sc in scholarships:
                    retrieval_text_blocks.append(f"• {sc['title']} by {sc['provider']} | Benefit: {sc['amount']}")

        # 6. Internship Search
        if intent in ["INTERNSHIP_SEARCH"]:
            internships = MPathRetriever.search_internships(query=user_message, limit=3)
            if internships:
                tool_records.extend(internships)
                retrieval_text_blocks.append("\nVerified Student Internships:")
                for ins in internships:
                    retrieval_text_blocks.append(f"• {ins['title']} at {ins['company']} ({ins['location']}, {ins['mode']}) | Stipend: {ins['stipend']}")

        context_string = "\n".join(retrieval_text_blocks)
        return context_string, tool_records

    @classmethod
    def _synthesize_local_counsel(
        cls,
        user_message: str,
        analysis: Dict[str, Any],
        student_context: Dict[str, Any],
        retrieved_text: str,
        tool_records: List[Dict[str, Any]]
    ) -> str:
        """
        Expert deterministic rule-and-domain synthesis when cloud LLM APIs are offline.
        Provides rich, personalized, non-generic career counsel grounded in MPath data.
        """
        intent = analysis["primary_intent"]
        lang = analysis.get("language", "english")
        stream = student_context.get("stream") or "your current stream"
        name = student_context.get("name", "Student")
        negatives = analysis.get("negative_preferences", [])

        # Hinglish response builder
        if lang == "hinglish":
            intro = f"Namaste {name if name != 'Student' else ''}! Maine aapki baat aur background ({stream}) ko dhyan me rakha hai."
            if negatives:
                intro += f" Sabse pehle, jaisa aapne bataya ki aap **{', '.join(negatives)}** me nahi jana chahte, to hum unhe filter karke authentic alternatives explore karenge."

            body = []
            if tool_records:
                body.append("\n### MPath Verified Opportunities (Aapke liye filtered):")
                for r in tool_records[:3]:
                    if "slug" in r:
                        body.append(f"- **{r['title']}** ({r['category']}): {r['short_description']} | Indicative Income: {r['average_salary']}")
                    elif "degree_level" in r:
                        body.append(f"- **{r['name']}** ({r['degree_level']}): {r.get('duration', '3-4 years')} course.")
                    elif "exam_type" in r:
                        body.append(f"- **{r['name']}** ({r.get('short_name', '')}): {r.get('exam_type', 'Entrance')} test.")

            tradeoff = (
                "\n### Career Counsellor Perspective & Trade-offs:\n"
                "Kisi bhi option ko final karne se pehle ye dekhein: kya aap theoretical analysis me comfortable hain "
                "ya hands-on practical execution me? Har degree ke sath domain skills aur real mini-projects banana sabse zaroori hota hai."
            )

            next_steps = (
                "\n### Agla Step (Next Action):\n"
                "1. Neeche diye gaye direct action cards par click karke complete curriculum aur eligibility inspect karein.\n"
                "2. Agar aapko syllabus ya top colleges me doubt hai, to mujhe batayein."
            )

            question = "\n\n*Kya aap kisi specific college location ya budget ko prefer kar rahe hain?*"
            return f"{intro}\n{body}\n{tradeoff}\n{next_steps}{question}"

        # English response builder
        else:
            intro = f"Hello {name if name != 'Student' else ''}. Looking at your background ({stream}) and specific question:"
            if negatives:
                intro += f" I have excluded pathways involving **{', '.join(negatives)}** so we can focus on viable alternatives that genuinely fit your goals."

            sections = [intro]

            if tool_records:
                sections.append("\n### Verified MPath Pathways to Explore:")
                for r in tool_records[:3]:
                    if "slug" in r:
                        sections.append(f"- **{r['title']}** (*{r['category']}*)\n  {r['short_description']}\n  *Entry Qualifications*: {r['education_required']} | *Indicative Scope*: {r['average_salary']}")
                    elif "degree_level" in r:
                        sections.append(f"- **{r['name']}** (*{r['degree_level']}*)\n  Duration: {r.get('duration', '3-4 years')} | Eligibility: {r.get('eligibility', 'Check details')}")
                    elif "exam_type" in r:
                        sections.append(f"- **{r['name']}** (*{r.get('short_name', '')}*)\n  Category: {r.get('exam_type', 'National')} | Cycle: {r.get('exam_date', 'Annual')}")

            sections.append(
                "\n### Counsellor Trade-offs & Strategic Advice:\n"
                "The most sustainable career choice balances three things: your natural affinity, the education investment timeline, and market absorption. "
                "Instead of choosing a path purely on title prestige, evaluate whether you prefer analytical problem-solving, people coordination, or creative systems."
            )

            sections.append(
                "\n### Recommended Next Steps:\n"
                "1. Click the verified action buttons below to inspect verified syllabus and admission criteria.\n"
                "2. Narrow down whether your priority in the next 12 months is immediate skill-building, degree admission, or competitive examination preparation."
            )

            sections.append("\n*Which of these directions feels closest to your day-to-day interests?*")
            return "\n\n".join(sections)

    @classmethod
    def generate_response(
        cls,
        user_message: str,
        user_id: Optional[int] = None,
        session_id: Optional[str] = None,
        conversation_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Executes complete multi-turn reasoning and returns structured payload.
        """
        start_time = time.time()

        # 1. Retrieve or Create Conversation
        conversation = None
        if conversation_id:
            conversation = db.session.get(ChatConversation, conversation_id)
        if not conversation:
            conversation = ChatConversation(
                user_id=user_id,
                session_id=session_id,
                title=user_message[:40] + ("..." if len(user_message) > 40 else "")
            )
            db.session.add(conversation)
            db.session.commit()

        state = conversation.get_state()

        # 2. Contextual pronoun and reference resolution
        resolved_message = MemoryManager.resolve_references(user_message, state)

        # 3. Intent Detection & Analysis
        analysis = IntentDetector.analyze(resolved_message, previous_state=state)

        # 4. Student Context
        student_context = build_student_context(user_id=user_id, session_id=session_id)

        # 5. Targeted Knowledge Retrieval
        retrieved_knowledge, tool_records = cls._execute_targeted_retrieval(
            analysis=analysis,
            user_message=resolved_message,
            student_context=student_context
        )

        # 6. Extract and store student memories
        MemoryManager.extract_and_store_memories(
            user_id=user_id,
            session_id=session_id,
            message=user_message,
            analysis=analysis
        )

        # 7. Generate Master Prompt
        system_prompt = get_master_system_prompt(student_context, language=analysis["language"])

        # Compile recent conversation history (last 4 turns)
        recent_messages = (
            ChatMessage.query.filter_by(conversation_id=conversation.id)
            .order_by(ChatMessage.created_at.desc())
            .limit(6)
            .all()
        )
        recent_messages.reverse()

        messages_payload = [{"role": "system", "content": system_prompt}]
        for m in recent_messages:
            messages_payload.append({"role": m.role, "content": m.content})

        user_content = f"{resolved_message}\n\n[MPath Verified Database Context]:\n{retrieved_knowledge if retrieved_knowledge else 'No specific database records matched directly. Provide general conceptual career guidance.'}"
        messages_payload.append({"role": "user", "content": user_content})

        raw_answer = ""
        provider_used = "local"

        # 8. Multi-Tier Model Generation
        provider = get_available_provider()

        # Tier 1: OpenAI
        if provider == "openai" and openai_client:
            try:
                # Use reasoning model for comparison/complex or standard model
                model_to_use = AI_REASONING_MODEL if analysis["primary_intent"] in ["CAREER_COMPARISON", "MULTI_INTENT"] else AI_MODEL
                
                # Normal chat completion with system instructions
                response = openai_client.chat.completions.create(
                    model=model_to_use,
                    messages=messages_payload,
                    temperature=0.7,
                    max_tokens=1200
                )
                raw_answer = response.choices[0].message.content
                provider_used = f"openai:{model_to_use}"
            except Exception as e:
                logger.warning("OpenAI API call failed, falling back: %s", e)
                provider = "gemini" if gemini_client else "local"

        # Tier 2: Gemini
        if not raw_answer and provider == "gemini" and gemini_client:
            try:
                # Combine system prompt with user messages
                combined_prompt = f"{system_prompt}\n\n"
                for m in recent_messages:
                    combined_prompt += f"{m.role.upper()}: {m.content}\n"
                combined_prompt += f"USER: {user_content}\nASSISTANT:"

                gem_resp = gemini_client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=combined_prompt
                )
                if hasattr(gem_resp, "text") and gem_resp.text:
                    raw_answer = gem_resp.text
                    provider_used = f"gemini:{GEMINI_MODEL}"
            except Exception as e:
                logger.warning("Gemini API call failed, falling back to local: %s", e)
                provider = "local"

        # Tier 3: Local Grounded Expert Engine
        if not raw_answer:
            raw_answer = cls._synthesize_local_counsel(
                user_message=user_message,
                analysis=analysis,
                student_context=student_context,
                retrieved_text=retrieved_knowledge,
                tool_records=tool_records
            )
            provider_used = "mpath-local-grounded-engine"

        # 9. Grounding Verification & Action Construction
        clean_answer, metadata = GroundingVerifier.verify_and_enrich(raw_answer, tool_records)
        metadata["provider"] = provider_used
        metadata["latency_sec"] = round(time.time() - start_time, 2)
        metadata["intent"] = analysis["primary_intent"]

        # 10. Persist Messages & Update State
        user_msg_record = ChatMessage(
            conversation_id=conversation.id,
            role="user",
            content=user_message
        )
        assistant_msg_record = ChatMessage(
            conversation_id=conversation.id,
            role="assistant",
            content=clean_answer
        )
        assistant_msg_record.set_metadata(metadata)

        db.session.add(user_msg_record)
        db.session.add(assistant_msg_record)
        db.session.commit()

        # Update state for future turns
        MemoryManager.update_state_from_turn(
            conversation=conversation,
            user_message=user_message,
            response_text=clean_answer,
            metadata=metadata
        )

        return {
            "conversation_id": conversation.id,
            "title": conversation.title,
            "answer": clean_answer,
            "metadata": metadata
        }

    @classmethod
    def stream_response(
        cls,
        user_message: str,
        user_id: Optional[int] = None,
        session_id: Optional[str] = None,
        conversation_id: Optional[int] = None
    ) -> Generator[str, None, None]:
        """
        Server-Sent Events (SSE) streaming generator yielding real-time text chunks
        followed by verified metadata payload.
        """
        # Execute complete reasoning
        result = cls.generate_response(
            user_message=user_message,
            user_id=user_id,
            session_id=session_id,
            conversation_id=conversation_id
        )

        # Emit text chunks simulating smooth real-time stream
        full_text = result["answer"]
        chunk_size = 25
        for i in range(0, len(full_text), chunk_size):
            chunk = full_text[i:i + chunk_size]
            payload = json.dumps({"type": "chunk", "content": chunk})
            yield f"data: {payload}\n\n"
            time.sleep(0.015)

        # Emit metadata event
        meta_payload = json.dumps({
            "type": "metadata",
            "conversation_id": result["conversation_id"],
            "title": result["title"],
            "metadata": result["metadata"]
        })
        yield f"data: {meta_payload}\n\n"

        # Emit completion
        yield "data: {\"type\": \"done\"}\n\n"
