from models.user import User


def build_student_context(user_id):

    context = {}

    user = User.query.get(user_id)

    if not user:

        return context

    # -----------------------------
    # User Name
    # -----------------------------

    if hasattr(user, "username"):

        context["name"] = user.username

    elif hasattr(user, "full_name"):

        context["name"] = user.full_name

    elif hasattr(user, "name"):

        context["name"] = user.name

    else:

        context["name"] = "Student"

    # -----------------------------
    # Email
    # -----------------------------

    if hasattr(user, "email"):

        context["email"] = user.email

    return context