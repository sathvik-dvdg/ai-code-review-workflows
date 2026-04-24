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
        prompt = f"""You are a senior Staff-level Software Engineer, Security Auditor, and GitHub Code Reviewer with experience in large-scale production systems.

Your task is to perform a deep, critical review of a GitHub repository or pull request. Do NOT give surface-level feedback. Focus on real-world risks, failure points, and production-readiness.

## INPUT
I will provide:
- GitHub repo link or code snippets
- (Optional) problem statement or expected behavior
- (Optional) tech stack details

## YOUR REVIEW MUST COVER:

### 1. ARCHITECTURE & DATA FLOW
- Explain how the system works end-to-end
- Identify hidden coupling, tight dependencies, or bad abstractions
- Highlight scalability bottlenecks and design flaws
- Detect unnecessary complexity or overengineering

### 2. CRITICAL BUG DETECTION
- Identify logical errors (edge cases, incorrect assumptions)
- Find silent failures (code that “works” but produces wrong results)
- Detect async issues, race conditions, or state inconsistencies
- Highlight areas where errors are swallowed or ignored

### 3. SECURITY ANALYSIS (STRICT)
- Detect vulnerabilities:
  - Injection (SQL, NoSQL, command, etc.)
  - Authentication/authorization flaws
  - Sensitive data exposure
  - Insecure API handling
- Identify unsafe libraries or patterns
- Flag improper validation and sanitization
- Check token/session handling and secrets management

### 4. BACKEND RELIABILITY
- API contract issues
- Improper error handling and status codes
- Data validation gaps
- Database consistency issues
- Risk of corrupted or fake data storage

### 5. FRONTEND REVIEW (if applicable)
- Incorrect API usage
- State management issues
- UI logic bugs that break real workflows
- Security issues (XSS, unsafe rendering)

### 6. WORKFLOW & DEV PROCESS
- GitHub workflow issues:
  - Missing CI/CD checks
  - No testing strategy
  - Poor commit structure
- Code maintainability problems
- Missing documentation or unclear logic

### 7. TESTING GAPS
- What is NOT tested but should be
- Critical edge cases missing
- Suggest exact test cases

---

## OUTPUT FORMAT (STRICT)

### 🔴 Critical Issues (Must Fix Immediately)
- [Issue]
- Why it is dangerous
- Real-world failure scenario
- Exact fix (code-level suggestion)

### 🟠 Major Issues
- [Issue + explanation + fix]

### 🟡 Minor Issues / Improvements
- [Refactoring, cleanup, performance]

### 🔐 Security Risks Summary
- List all vulnerabilities with severity

### 🧠 Architectural Weaknesses
- High-level design problems

### 🧪 Missing Tests
- List specific test cases to add

### ⚙️ Refactoring Suggestions
- Practical improvements with reasoning

---

## RULES
- Be brutally honest. Do NOT sugarcoat.
- Do NOT assume code is correct—challenge every assumption.
- Prioritize real production risks over style issues.
- If something looks fine, explain WHY it is safe.
- Avoid generic advice—be specific and actionable.

---

Now analyze the provided code/repository.

Diff:
{diff_content}
"""

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        output = response.text if response and response.text else "AI could not generate a response."

with open("review.txt", "w") as f:
    f.write(output)