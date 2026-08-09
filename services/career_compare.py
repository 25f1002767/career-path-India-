from models.career import Career


def compare_careers(career1, career2):

    return {

        "career1": career1,

        "career2": career2,

        "salary_equal":
            career1.average_salary == career2.average_salary,

        "future_equal":
            career1.future_scope == career2.future_scope,

        "education_equal":
            career1.education_required ==
            career2.education_required,

        "skills1":
            career1.skills_required.split(","),

        "skills2":
            career2.skills_required.split(",")

    }