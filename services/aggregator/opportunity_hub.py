from services.apis.jobs_api import JobsAPI
from services.apis.course_api import CourseAPI
from services.apis.government_api import GovernmentAPI


class OpportunityHub:

    def __init__(self):

        self.jobs = JobsAPI()

        self.courses = CourseAPI()

        self.gov = GovernmentAPI()

    def discover(

        self,

        profile

    ):

        result = {}

        result["jobs"] = self.jobs.search_jobs(

            profile.career_goal

        )

        result["courses"] = self.courses.search(

            profile.career_goal

        )

        result["government"] = self.gov.latest()

        return result