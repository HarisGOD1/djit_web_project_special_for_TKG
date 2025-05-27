from google import genai
from .get_git_diff import get_git_diff, clean_diff


def generate_response(text):
    client = genai.Client(api_key="AIzaSyAk0B9uYa6jw6R1xsJ7jw6HNOcxGJ4h_8k")

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents="Make a comment for the commit. Give me the answer as a plain text." + '\n' + text,
    )
    return response.text

def get_response(username,reponame):
    diff_raw = get_git_diff(username,reponame)
    diff_cleaned = clean_diff(diff_raw)
    return generate_response(diff_cleaned)
