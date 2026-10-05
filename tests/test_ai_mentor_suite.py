import sys
import os
import unittest
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import app
from services.ai.intent_detector import IntentDetector
from services.ai.retriever import MPathRetriever
from services.ai.reasoning_engine import CareerReasoningEngine
from services.ai.memory_manager import MemoryManager
from models.chat import ChatConversation, ChatMessage


class TestAIMentorSuite(unittest.TestCase):
    """
    Evaluation Suite testing the 20 Golden Questions and Multi-turn Reasoning
    for MPath Master Intelligent Career Counselling Agent.
    """

    @classmethod
    def setUpClass(cls):
        cls.app = app.app
        cls.ctx = cls.app.app_context()
        cls.ctx.push()

    @classmethod
    def tearDownClass(cls):
        cls.ctx.pop()

    def test_01_confused_beginner(self):
        msg = "I don't know what career I want."
        res = CareerReasoningEngine.generate_response(user_message=msg, session_id="eval_01")
        self.assertTrue(len(res["answer"]) > 50)
        self.assertNotIn("\u2b50\u2b50\u2b50", res["answer"])
        self.assertIn(res["metadata"]["intent"], ["CONFUSED_BEGINNER", "CAREER_EXPLORATION"])

    def test_02_pcm_no_engineering(self):
        msg = "I am PCM but don't want engineering."
        res = CareerReasoningEngine.generate_response(user_message=msg, session_id="eval_02")
        self.assertTrue(len(res["answer"]) > 50)
        # Should not push pure engineering as top recommendation
        self.assertNotIn("\u2b50\u2b50\u2b50", res["answer"])
        for act in res["metadata"]["actions"]:
            self.assertTrue(act["url"].startswith("/") and not act["url"].startswith("//"))

    def test_03_maths_no_coding(self):
        msg = "I like maths but hate coding."
        res = CareerReasoningEngine.generate_response(user_message=msg, session_id="eval_03")
        self.assertTrue(len(res["answer"]) > 50)

    def test_04_coding_no_btech(self):
        msg = "I like coding but don't want B.Tech."
        res = CareerReasoningEngine.generate_response(user_message=msg, session_id="eval_04")
        self.assertTrue(len(res["answer"]) > 50)

    def test_05_govt_job_after_graduation(self):
        msg = "I want a government job after graduation."
        res = CareerReasoningEngine.generate_response(user_message=msg, session_id="eval_05")
        self.assertTrue(len(res["answer"]) > 50)

    def test_06_after_bsc_mathematics(self):
        msg = "What can I do after B.Sc Mathematics?"
        res = CareerReasoningEngine.generate_response(user_message=msg, session_id="eval_06")
        self.assertTrue(len(res["answer"]) > 50)

    def test_07_college_search(self):
        msg = "Which colleges should I consider?"
        res = CareerReasoningEngine.generate_response(user_message=msg, session_id="eval_07")
        self.assertTrue(len(res["answer"]) > 50)

    def test_08_scholarship_eligibility(self):
        msg = "Am I eligible for this scholarship?"
        res = CareerReasoningEngine.generate_response(user_message=msg, session_id="eval_08")
        self.assertTrue(len(res["answer"]) > 50)

    def test_09_exam_discovery(self):
        msg = "What exams can I give?"
        res = CareerReasoningEngine.generate_response(user_message=msg, session_id="eval_09")
        self.assertTrue(len(res["answer"]) > 50)

    def test_10_earn_early_constraint(self):
        msg = "I need a career where I can start earning quickly."
        res = CareerReasoningEngine.generate_response(user_message=msg, session_id="eval_10")
        self.assertTrue(len(res["answer"]) > 50)

    def test_11_family_pressure_balance(self):
        msg = "My parents want government job but I want private sector."
        res = CareerReasoningEngine.generate_response(user_message=msg, session_id="eval_11")
        self.assertTrue(len(res["answer"]) > 50)

    def test_12_biology_without_mbbs(self):
        msg = "I like biology but don't want to become a doctor."
        res = CareerReasoningEngine.generate_response(user_message=msg, session_id="eval_12")
        self.assertTrue(len(res["answer"]) > 50)

    def test_13_environment_careers(self):
        msg = "I want to work in environment."
        res = CareerReasoningEngine.generate_response(user_message=msg, session_id="eval_13")
        self.assertTrue(len(res["answer"]) > 50)

    def test_14_psychologist_pathway(self):
        msg = "I want to become a psychologist."
        res = CareerReasoningEngine.generate_response(user_message=msg, session_id="eval_14")
        self.assertTrue(len(res["answer"]) > 50)

    def test_15_arts_to_tech_transition(self):
        msg = "I am from Arts. Can I work in technology?"
        res = CareerReasoningEngine.generate_response(user_message=msg, session_id="eval_15")
        self.assertTrue(len(res["answer"]) > 50)

    def test_16_ai_resilience(self):
        msg = "Which career will AI not replace?"
        res = CareerReasoningEngine.generate_response(user_message=msg, session_id="eval_16")
        self.assertTrue(len(res["answer"]) > 50)

    def test_17_career_comparison(self):
        msg = "Compare CA, MBA and CFA."
        res = CareerReasoningEngine.generate_response(user_message=msg, session_id="eval_17")
        self.assertTrue(len(res["answer"]) > 50)

    def test_18_six_month_roadmap(self):
        msg = "What should I do in the next six months?"
        res = CareerReasoningEngine.generate_response(user_message=msg, session_id="eval_18")
        self.assertTrue(len(res["answer"]) > 50)

    def test_19_scholarship_retrieval(self):
        msg = "Find me scholarships."
        res = CareerReasoningEngine.generate_response(user_message=msg, session_id="eval_19")
        self.assertTrue(len(res["answer"]) > 50)

    def test_20_college_near_me(self):
        msg = "Find colleges near me."
        res = CareerReasoningEngine.generate_response(user_message=msg, session_id="eval_20")
        self.assertTrue(len(res["answer"]) > 50)

    def test_21_multiturn_conversational_state(self):
        """
        Tests multi-turn context memory:
        Turn 1: "What about BCA?"
        Turn 2: "What about its fees?" ('its' = BCA)
        Turn 3: "What colleges offer it?" ('it' = BCA)
        """
        session_id = f"eval_multi_{int(time.time())}"
        
        # Turn 1
        t1 = CareerReasoningEngine.generate_response(
            user_message="What about BCA?",
            session_id=session_id
        )
        conv_id = t1["conversation_id"]
        self.assertIsNotNone(conv_id)

        # Turn 2
        t2 = CareerReasoningEngine.generate_response(
            user_message="What about its fees?",
            session_id=session_id,
            conversation_id=conv_id
        )
        self.assertTrue(len(t2["answer"]) > 40)

        # Turn 3
        t3 = CareerReasoningEngine.generate_response(
            user_message="What colleges offer it?",
            session_id=session_id,
            conversation_id=conv_id
        )
        self.assertTrue(len(t3["answer"]) > 40)

    def test_22_hinglish_fluency(self):
        msg = "Mujhe engineering nahi karni but maths pasand hai. 12th PCM ke baad kya options hain?"
        analysis = IntentDetector.analyze(msg)
        self.assertEqual(analysis["language"], "hinglish")
        res = CareerReasoningEngine.generate_response(user_message=msg, session_id="eval_hinglish")
        self.assertTrue(len(res["answer"]) > 50)


if __name__ == "__main__":
    unittest.main()
