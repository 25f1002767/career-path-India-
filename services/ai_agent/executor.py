from services.ai_agent.tools import *

def execute(plan, user_id):

    result = {}

    for step in plan:

        if step == "career":

            result["career"] = career_tool(user_id)

        elif step == "resume":

            result["resume"] = resume_tool(user_id)

        elif step == "college":

            result["college"] = college_tool()

        elif step == "roadmap":

            result["roadmap"] = roadmap_tool()

        elif step == "scholarship":

            result["scholarship"] = scholarship_tool()

        elif step == "internship":

            result["internship"] = internship_tool()

    return result