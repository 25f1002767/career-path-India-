import re
from typing import Dict, Any, List

class IntentDetector:
    """
    Classifies user intent and extracts career entities, constraints, and preferences.
    Handles English, Hindi, and Hinglish.
    """

    INTENTS = {
        "CAREER_EXPLORATION": ["career", "scope", "field", "become", "options", "kya karu", "kya banu", "banoon", "fields", "paths", "direction"],
        "CAREER_COMPARISON": ["compare", "vs", "versus", "difference", "better", "kaun sa accha", "which is better", "dono me se"],
        "COURSE_SELECTION": ["course", "degree", "bca", "btech", "bsc", "ba", "bcom", "diploma", "masters", "ug", "pg", "padhai"],
        "COLLEGE_SEARCH": ["college", "university", "institute", "campus", "colleges near", "top college", "best college", "admission", "fees"],
        "EXAM_SEARCH": ["exam", "entrance", "jee", "neet", "cuet", "upsc", "ssc", "gate", "cat", "nda", "pariksha"],
        "SCHOLARSHIP_SEARCH": ["scholarship", "financial aid", "funding", "fee waiver", "stipend", "fellowship", "chhatravritti"],
        "INTERNSHIP_SEARCH": ["internship", "intern", "trainee", "practical training", "summer intern"],
        "ROADMAP": ["roadmap", "next 6 months", "next year", "plan", "steps", "kaise shuru karu", "step by step", "timeline", "kya karu ab"],
        "ELIGIBILITY": ["eligible", "eligibility", "qualification", "age limit", "percentage", "can i do", "kya mai kar sakta", "criteria"],
        "SKILL_GUIDANCE": ["skill", "learn", "tools", "coding", "technologies", "seekhna", "project"],
        "CONFUSED_BEGINNER": ["don't know", "dont know", "confused", "no idea", "samajh nahi aa raha", "lost", "kuch samajh nahi"],
        "ANXIETY_EMPATHY": ["pressure", "anxious", "scared", "fear", "parents want", "family pressure", "failed", "depression", "tension", "stress", "dar"]
    }

    @staticmethod
    def detect_language(text: str) -> str:
        """
        Detects if user is speaking in Hinglish, Hindi (Devanagari), or English.
        """
        # Devanagari Unicode range: \u0900-\u097F
        if re.search(r'[\u0900-\u097F]', text):
            return "hindi"
        
        hinglish_words = {
            "kya", "hai", "mujhe", "mera", "meri", "karna", "kare", "kaise", "nahi", 
            "hona", "chahiye", "baad", "mein", "aur", "batao", "bataiye", "pasand",
            "accha", "padhai", "sarkari", "naukri", "wale", "karni", "hota", "hote"
        }
        words = set(re.findall(r'\b[a-zA-Z]+\b', text.lower()))
        if len(words.intersection(hinglish_words)) >= 2 or any(w in words for w in ["kya", "mujhe", "karna", "nahi"]):
            return "hinglish"
        return "english"

    @classmethod
    def analyze(cls, message: str, previous_state: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Extracts primary intent, secondary intents, constraints, and detected entities.
        """
        msg_lower = message.lower()
        matched_intents = []

        for intent, keywords in cls.INTENTS.items():
            for kw in keywords:
                if re.search(r'\b' + re.escape(kw) + r'\b', msg_lower):
                    matched_intents.append(intent)
                    break

        # Check for pronoun / follow-up references
        is_follow_up = False
        pronouns = ["it", "its", "this", "these", "that", "there", "usme", "iska", "iski", "isme", "waha"]
        for p in pronouns:
            if re.search(r'\b' + re.escape(p) + r'\b', msg_lower):
                is_follow_up = True
                break

        # Extract negative preferences (anti-preferences)
        negatives = []
        neg_patterns = [
            r"(?:don't want|dont want|no|hate|dislike|not interested in|nahi karni|nahi chahiye|nhi chahiye|nahi banna)\s+([a-zA-Z\s]+)",
            r"without\s+([a-zA-Z\s]+)",
            r"besides\s+([a-zA-Z\s]+)"
        ]
        for pat in neg_patterns:
            matches = re.findall(pat, msg_lower)
            for m in matches:
                item = m.strip().split()[0] if m.strip() else ""
                if item and len(item) > 2 and item not in ["a", "an", "the", "to", "in"]:
                    negatives.append(item)

        # Extract stream mentions
        streams = []
        if any(k in msg_lower for k in ["pcm", "physics chemistry maths", "science with maths"]):
            streams.append("Science (PCM)")
        elif any(k in msg_lower for k in ["pcb", "physics chemistry biology", "medical stream", "biology"]):
            streams.append("Science (PCB)")
        elif any(k in msg_lower for k in ["commerce", "accounts", "economics"]):
            streams.append("Commerce")
        elif any(k in msg_lower for k in ["arts", "humanities", "social science"]):
            streams.append("Arts")

        # Specific constraints
        constraints = {}
        if any(k in msg_lower for k in ["earn early", "quick job", "jaldi kamana", "start earning quickly"]):
            constraints["earn_early"] = True
        if any(k in msg_lower for k in ["stable", "stability", "secure", "suraksha"]):
            constraints["stability"] = True
        if any(k in msg_lower for k in ["govt", "government", "sarkari"]):
            constraints["government_preference"] = True
        if any(k in msg_lower for k in ["private", "corporate", "pvt"]):
            constraints["private_preference"] = True
        if any(k in msg_lower for k in ["near home", "near me", "in mp", "in delhi", "in maharashtra", "locally"]):
            constraints["location_constraint"] = True

        primary_intent = matched_intents[0] if matched_intents else ("FOLLOW_UP" if is_follow_up else "CAREER_EXPLORATION")

        return {
            "primary_intent": primary_intent,
            "all_intents": list(set(matched_intents)),
            "is_follow_up": is_follow_up,
            "language": cls.detect_language(message),
            "negative_preferences": negatives,
            "streams": streams,
            "constraints": constraints,
            "raw_message": message
        }
