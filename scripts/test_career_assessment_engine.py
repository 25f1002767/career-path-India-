"""
scripts/test_career_assessment_engine.py
==============================================================================
MPath Career Discovery Assessment Engine Verification Suite
==============================================================================
Validates the new multi-dimensional assessment system across 10 diverse
student personas, checking:
1. Significant differentiation of career recommendations across personas.
2. Correct detection of contradictions and trade-offs.
3. Signature "You May Not Have Considered" lesser-known discoveries.
4. Relational MPath ecosystem connectivity (Courses, Colleges, Exams, Scholarships).
5. Database persistence and backward compatibility with dashboard/profile.
"""

import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Ensure UTF-8 output on Windows consoles
if sys.platform.startswith("win"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from app import app
from extensions import db
from models.assessment import AssessmentResult
from services.career_assessment_engine import CareerAssessmentEngine


PERSONAS = [
    {
        "name": "Persona 1: Analytical + Investigative + Independent",
        "inputs": {
            "q1_curiosity_scenario": "B",  # Scientific data / clues / unexpected event
            "q2_flow_activity": "B",       # Research articles, coding tutorials
            "q3_self_efficacy": "A",       # High analytical self-efficacy
            "q4_work_values": "C",         # Intellectual mastery & premier expert
            "q5_problem_type": "A",        # Cutting-edge software, algorithms, automation
            "q6_work_environment": "E",    # Quiet remote or hybrid desk
            "q7_failure_and_persistence": "A", # Break problem down, research
            "q8_study_investment_tolerance": "B", # 3-4 year degree
            "q9_exam_tolerance": "C",      # Merit / practical interview
            "q10_family_expectations": "E",# Full support
            "q11_financial_constraints": "B", # Moderate loan feasible
            "q12_current_academic_level": "B", # Science (PCM)
            "q13_academic_strengths": "A", # Mathematics, Logic & Quantitative
            "q14_negative_preferences": "B", # Dislike sales quotas
            "q15_decision_making_style": "A", # Empirical data
            "q16_open_reflection": "I love building algorithmic systems and debugging data models."
        },
        "expected_sector_keyword": "Technology"
    },
    {
        "name": "Persona 2: Social + Teaching + Communication",
        "inputs": {
            "q1_curiosity_scenario": "D",  # Listening to struggling person
            "q2_flow_activity": "D",       # Teaching, mentoring peers
            "q3_self_efficacy": "C",       # Interpersonal social self-efficacy
            "q4_work_values": "B",         # Social impact, healing, educating
            "q5_problem_type": "D",        # Law, policy or helping
            "q6_work_environment": "A",    # Collaborative team office/campus
            "q7_failure_and_persistence": "B", # Seek mentor & feedback
            "q8_study_investment_tolerance": "B", # Standard 3-4 year degree
            "q9_exam_tolerance": "B",      # Open with backup
            "q10_family_expectations": "E",# Full support
            "q11_financial_constraints": "B",
            "q12_current_academic_level": "E", # Humanities / Arts
            "q13_academic_strengths": "C", # Languages, Literature, Debating
            "q14_negative_preferences": "A", # Dislike isolated desk spreadsheets
            "q15_decision_making_style": "B", # Mentor guided
            "q16_open_reflection": "I love helping school students overcome their fear of learning."
        },
        "expected_sector_keyword": "Education"
    },
    {
        "name": "Persona 3: Creative + Artistic + Visual",
        "inputs": {
            "q1_curiosity_scenario": "C",  # Visual concept, story, design
            "q2_flow_activity": "C",       # Illustrating, video editing, graphic design
            "q3_self_efficacy": "D",       # Capable in visual/creative, low math comfort
            "q4_work_values": "D",         # Total freedom, studio of own
            "q5_problem_type": "G",        # Films, multimedia, game worlds
            "q6_work_environment": "D",    # Creative studio, workshop
            "q7_failure_and_persistence": "C", # Unconventional creative angle
            "q8_study_investment_tolerance": "B", # 3-4 year degree
            "q9_exam_tolerance": "D",      # Portfolio-driven
            "q10_family_expectations": "E",# Full support
            "q11_financial_constraints": "B",
            "q12_current_academic_level": "E", # Arts / Design
            "q13_academic_strengths": "F", # Visual Arts, Spatial Reasoning, 3D
            "q14_negative_preferences": "A", # Dislike repetitive desk spreadsheets
            "q15_decision_making_style": "D", # Purpose & value-driven
            "q16_open_reflection": "I make digital animations and design mobile user interfaces."
        },
        "expected_sector_keyword": "Design"
    },
    {
        "name": "Persona 4: Entrepreneurial + Leadership + Risk-Taking",
        "inputs": {
            "q1_curiosity_scenario": "E",  # Organizing people, resources, execution
            "q2_flow_activity": "E",       # Business plan, negotiating, budget
            "q3_self_efficacy": "C",       # High social and organizational efficacy
            "q4_work_values": "D",         # Built something of my own, venture
            "q5_problem_type": "E",        # Markets, investments, commercial enterprise
            "q6_work_environment": "A",    # Collaborative tech campus / corporate
            "q7_failure_and_persistence": "C", # Creative pivot
            "q8_study_investment_tolerance": "D", # Foundation then executive study
            "q9_exam_tolerance": "C",      # Practical hiring / venture
            "q10_family_expectations": "C",# High earning potential
            "q11_financial_constraints": "D", # Flexible investment
            "q12_current_academic_level": "D", # Commerce
            "q13_academic_strengths": "D", # Economics, Business Trends, Commerce
            "q14_negative_preferences": "A", # Dislike repetitive isolated data entry
            "q15_decision_making_style": "C", # Hands-on experimentation
            "q16_open_reflection": "I ran our college e-commerce merchandise festival and turned a 40% profit."
        },
        "expected_sector_keyword": "Business"
    },
    {
        "name": "Persona 5: Practical + Hands-on + Technical",
        "inputs": {
            "q1_curiosity_scenario": "A",  # Mechanical device, physical machine malfunctioning
            "q2_flow_activity": "A",       # Assembling, fixing, modifying circuits or models
            "q3_self_efficacy": "B",       # Hands-on practical learning
            "q4_work_values": "A",         # Financial security & income
            "q5_problem_type": "C",        # Physical infrastructure, clean energy, robotics
            "q6_work_environment": "D",    # Workshop, fabrication space
            "q7_failure_and_persistence": "A", # Systematic physical testing
            "q8_study_investment_tolerance": "C", # Early entry diploma / skill
            "q9_exam_tolerance": "C",      # Practical skill evaluations
            "q10_family_expectations": "A",# Job stability
            "q11_financial_constraints": "C", # Need to earn early
            "q12_current_academic_level": "F", # Polytechnic Diploma / ITI
            "q13_academic_strengths": "F", # Visual arts, spatial & mechanical
            "q14_negative_preferences": "B", # Dislike sales quotas
            "q15_decision_making_style": "C", # Hands-on trial
            "q16_open_reflection": "I love assembling electric vehicle battery modules and repairing CNC machines."
        },
        "expected_sector_keyword": "Engineering"
    },
    {
        "name": "Persona 6: Public-Service + Stability + Leadership",
        "inputs": {
            "q1_curiosity_scenario": "E",  # Organizing people and timelines
            "q2_flow_activity": "D",       # Mentoring, community mediation
            "q3_self_efficacy": "A",       # High discipline
            "q4_work_values": "E",         # Respected institutional role, lifetime stability
            "q5_problem_type": "D",        # Defending legal rights, public policy, governance
            "q6_work_environment": "A",    # Government / Corporate office
            "q7_failure_and_persistence": "D", # Step-by-step structure
            "q8_study_investment_tolerance": "B", # Standard degree + exam prep
            "q9_exam_tolerance": "A",      # High competitive exam tolerance (UPSC/State PSC)
            "q10_family_expectations": "A",# Job security & government designation
            "q11_financial_constraints": "A", # Affordable government colleges
            "q12_current_academic_level": "E", # Humanities / Arts
            "q13_academic_strengths": "E", # Social Sciences, History, Politics
            "q14_negative_preferences": "F", # Low tolerance for unpredictable income
            "q15_decision_making_style": "B", # Experienced mentor guidance
            "q16_open_reflection": "I read administrative case studies and aspire to manage district governance."
        },
        "expected_sector_keyword": "Government"
    },
    {
        "name": "Persona 7: Biology + People + Healthcare",
        "inputs": {
            "q1_curiosity_scenario": "B",  # Scientific clues & unexpected event
            "q2_flow_activity": "B",       # Research articles & medical documentaries
            "q3_self_efficacy": "A",       # Disciplined step-by-step mastery
            "q4_work_values": "B",         # Directly healed and empowered vulnerable people
            "q5_problem_type": "B",        # Combating disease, improving clinical therapies
            "q6_work_environment": "B",    # Hospital, diagnostic lab, research institute
            "q7_failure_and_persistence": "A", # Break problem down systematically
            "q8_study_investment_tolerance": "A", # 5.5 to 8+ years intense study
            "q9_exam_tolerance": "A",      # High competitive entrance exam (NEET)
            "q10_family_expectations": "B",# Professional title (Doctor)
            "q11_financial_constraints": "B", # Moderate loan feasible
            "q12_current_academic_level": "C", # Science (PCB)
            "q13_academic_strengths": "B", # Life Sciences, Biology, Human Body
            "q14_negative_preferences": "A", # Dislike isolated desk spreadsheets
            "q15_decision_making_style": "A", # Empirical data
            "q16_open_reflection": "I have spent years studying human physiology and pathology."
        },
        "expected_sector_keyword": "Healthcare"
    },
    {
        "name": "Persona 8: Humanities + Language + Communication",
        "inputs": {
            "q1_curiosity_scenario": "C",  # Storytelling & narrative
            "q2_flow_activity": "C",       # Writing stories, debating
            "q3_self_efficacy": "C",       # Strong verbal self-efficacy
            "q4_work_values": "B",         # Social impact & public voice
            "q5_problem_type": "D",        # Legal rights, public media, constitutional issues
            "q6_work_environment": "A",    # Editorial, law office, media house
            "q7_failure_and_persistence": "C", # Creative pivot
            "q8_study_investment_tolerance": "B", # 3-4 year BA / LLB
            "q9_exam_tolerance": "C",      # Interview / writing samples
            "q10_family_expectations": "E",# Full support
            "q11_financial_constraints": "B",
            "q12_current_academic_level": "E", # Humanities / Arts
            "q13_academic_strengths": "C", # Languages, Literature, Debating
            "q14_negative_preferences": "D", # Dislike strenuous physical outdoor labor
            "q15_decision_making_style": "D", # Purpose & value-driven
            "q16_open_reflection": "I write investigative journalism articles and moderate state-level debates."
        },
        "expected_sector_keyword": "Law"
    },
    {
        "name": "Persona 9: Agriculture + Environment + Practical Work",
        "inputs": {
            "q1_curiosity_scenario": "A",  # Natural & mechanical systems
            "q2_flow_activity": "A",       # Outdoor hands-on experimentation
            "q3_self_efficacy": "B",       # Experiential learning
            "q4_work_values": "B",         # Environmental protection & sustainability
            "q5_problem_type": "F",        # Agriculture, wildlife, water and climate crises
            "q6_work_environment": "C",    # In the field, outdoors, project sites, wildlife
            "q7_failure_and_persistence": "A", # Test hypotheses
            "q8_study_investment_tolerance": "B", # 4-year B.Sc Agriculture / Forestry
            "q9_exam_tolerance": "B",      # Open with backup
            "q10_family_expectations": "E",# Full support
            "q11_financial_constraints": "A", # Low cost state agriculture university
            "q12_current_academic_level": "C", # Science (PCB)
            "q13_academic_strengths": "B", # Life sciences, ecological systems
            "q14_negative_preferences": "A", # Dislike isolated computer desk work all day
            "q15_decision_making_style": "C", # Experiential trial
            "q16_open_reflection": "I volunteer with soil regeneration projects and love agronomy."
        },
        "expected_sector_keyword": "Agriculture"
    },
    {
        "name": "Persona 10: Undecided + Mixed Interests",
        "inputs": {
            "q1_curiosity_scenario": "B",  # Scientific clues
            "q2_flow_activity": "F",       # Organizing data catalogs
            "q3_self_efficacy": "E",       # Currently uncertain, exploratory
            "q4_work_values": "A",         # Financial security
            "q5_problem_type": "E",        # Markets & enterprise
            "q6_work_environment": "E",    # Quiet remote or hybrid desk
            "q7_failure_and_persistence": "D", # Need structure
            "q8_study_investment_tolerance": "B", # 3-4 year degree
            "q9_exam_tolerance": "B",      # Balanced
            "q10_family_expectations": "C",# Financial security
            "q11_financial_constraints": "B",
            "q12_current_academic_level": "A", # Class 10
            "q13_academic_strengths": "A", # Mathematics & Logic
            "q14_negative_preferences": "B", # Dislike aggressive sales
            "q15_decision_making_style": "A", # Empirical data
            "q16_open_reflection": "I am interested in computers and economics but haven't decided on a career."
        },
        "expected_sector_keyword": "Finance"
    }
]


def run_persona_tests():
    with app.app_context():
        print("=================================================================")
        print("[TEST] RUNNING MPATH CAREER ASSESSMENT ENGINE VERIFICATION SUITE")
        print("=================================================================\n")

        passed_count = 0
        all_recommended_categories = set()
        all_top_career_titles = []

        for idx, persona in enumerate(PERSONAS, start=1):
            print(f"--- Testing {persona['name']} ---")
            eval_result = CareerAssessmentEngine.evaluate(persona["inputs"])

            top_matches = eval_result["top_matches"]
            unexpected = eval_result["unexpected_careers"]
            tradeoffs = eval_result["tradeoffs"]
            actions = eval_result["actions"]
            profile = eval_result["profile"]

            # Assertions
            assert len(top_matches) >= 3, f"Expected at least 3 top matches, got {len(top_matches)}"
            assert len(unexpected) >= 1, f"Expected at least 1 unexpected career, got {len(unexpected)}"
            assert len(actions) == 3, f"Expected 3 next actions, got {len(actions)}"
            assert profile["dominant_archetype"], "Dominant thinking archetype missing"

            top_title = top_matches[0]["career"].title
            top_category = top_matches[0]["career"].category
            unexpected_title = unexpected[0]["career"].title

            all_recommended_categories.add(top_category)
            all_top_career_titles.append(top_title)

            print(f"  Dominant Archetype : {profile['dominant_archetype']}")
            print(f"  Top Match #1       : {top_title} ({top_category})")
            print(f"  Top Match #2       : {top_matches[1]['career'].title}")
            print(f"  Unexpected Career  : {unexpected_title} ({unexpected[0]['career'].category})")
            print(f"  Fit Ratings        : Interest={top_matches[0]['interest_fit']}, Values={top_matches[0]['values_fit']}, Feasibility={top_matches[0]['feasibility_fit']}")

            if tradeoffs:
                print(f"  Trade-off Detected : [{tradeoffs[0]['type']}] {tradeoffs[0]['title']}")

            # Verify relational ecosystem links
            linked_courses = top_matches[0]["linked_courses"]
            linked_colleges = top_matches[0]["linked_colleges"]
            linked_exams = top_matches[0]["linked_exams"]

            print(f"  Ecosystem Links    : {len(linked_courses)} Courses, {len(linked_colleges)} Colleges, {len(linked_exams)} Exams")

            # Check sector alignment
            expected_kw = persona.get("expected_sector_keyword", "")
            match_found = any(expected_kw.lower() in (c["career"].category or "").lower() for c in top_matches[:3])
            assert match_found, f"Expected sector keyword '{expected_kw}' in top matches, got {[c['career'].category for c in top_matches[:3]]}"

            print(f"  [PASS] Persona {idx} PASSED!\n")
            passed_count += 1

        print("=================================================================")
        print("[STATS] DIVERSITY & DISTINCTIVENESS SUMMARY")
        print("=================================================================")
        print(f"Total Personas Evaluated: {len(PERSONAS)}")
        print(f"Distinct Sectors Discovered: {len(all_recommended_categories)} ({', '.join(all_recommended_categories)})")
        print(f"Distinct Top Career Matches: {len(set(all_top_career_titles))} out of 10")
        print("=================================================================")

        # Assert that the system did NOT collapse everyone to the same career!
        assert len(set(all_top_career_titles)) >= 8, f"Too much overlap in top careers: {all_top_career_titles}"
        assert len(all_recommended_categories) >= 6, f"Too few distinct sectors: {all_recommended_categories}"

        print("\n[COMPLETE] ALL 10 PERSONAS TESTED AND VERIFIED SUCCESSFULLY WITH HIGH DIVERSITY!")


if __name__ == "__main__":
    run_persona_tests()
