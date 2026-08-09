MEMORY = {}


def save(user_id, question):

    if user_id not in MEMORY:

        MEMORY[user_id] = []

    MEMORY[user_id].append(question)


def history(user_id):

    return MEMORY.get(user_id, [])