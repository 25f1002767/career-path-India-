import fitz


def extract_resume_text(filepath):

    document = fitz.open(filepath)

    text = ""

    for page in document:

        text += page.get_text()

    return text