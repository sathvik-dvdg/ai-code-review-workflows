import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise Exception("Missing API key: GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if not os.path.exists("diff.txt"):
    output = "No diff file found."
else:
    with open("diff.txt", "r") as f:
        diff_content = f.read()

    if not diff_content.strip() or diff_content.strip() == "No diff":
        output = "No code changes detected for review."
    else:
        prompt = f"""
Act as a senior software engineer and security reviewer.

Review the following git diff for:
- Critical bugs
- Security vulnerabilities
- Logic errors
- Missing edge cases

Focus only on real production risks.

Return:
1. Critical Issues
2. Major Issues
3. Security Risks
4. Missing Tests
5. Refactoring Suggestions

Diff:
{diff_content}
"""

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        output = response.text if response and response.text else "AI could not generate a response."

with open("review.txt", "w") as f:
    f.write(output)