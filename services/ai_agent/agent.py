from services.ai_agent.planner import create_plan
from services.ai_agent.executor import execute
from services.ai_agent.memory import save

from services.ai_career_mentor import get_ai_guidance


def run_agent(user_id, question):

    save(user_id, question)

    plan = create_plan(question)

    data = execute(plan, user_id)

    prompt = f"""

Student Question

{question}

Available Information

{data}

Provide the best personalized guidance.

"""

    return get_ai_guidance(prompt)