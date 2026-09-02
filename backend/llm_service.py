import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

client = genai.Client(api_key=api_key)


async def generate_clinical_explanation(
    test_name: str,
    value: float,
    unit: str,
    status: str,
    reference_min: float,
    reference_max: float,
    routing: str
) -> dict:

    prompt = f"""
You are a clinical laboratory results explanation assistant.

Analyze the following laboratory result:

Test: {test_name}
Value: {value} {unit}
Reference range: {reference_min} - {reference_max} {unit}
Classification: {status}
Recommended routing: {routing}

Provide a concise, clinically relevant explanation for a general user.

Your response MUST contain exactly two sections:

Explanation:
Explain what the result means and why it has been classified as {status}.
Do not diagnose a disease. Do not invent patient-specific information.

Next step:
Suggest an appropriate general next step based on the severity.
For Critical results, emphasize prompt medical attention.
For Warning results, recommend appropriate follow-up or review.
For Normal results, state that the result is within the supplied reference range.

Keep the response concise and understandable.
"""

    response = await client.aio.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    text = response.text.strip()

    explanation = text
    next_step = routing

    if "Next step:" in text:
        parts = text.split("Next step:", 1)
        explanation = parts[0].replace("Explanation:", "").strip()
        next_step = parts[1].strip()

    return {
        "explanation": explanation,
        "next_step": next_step
    }