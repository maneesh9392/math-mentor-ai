from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI()


def run_explainer_agent(parsed_problem: dict, solver_output: dict):
    """
    Uses LLM to generate a student-friendly step-by-step explanation
    """

    problem = parsed_problem["problem_text"]
    answer = solver_output["result"]

    prompt = f"""
You are a math tutor helping a student solve a JEE-style problem.

Problem:
{problem}

Final Answer:
{answer}

Explain the solution step-by-step in a clear way that a high school student can understand.

Rules:
- Be concise
- Show reasoning steps
- Do not change the final answer
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert math tutor."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        explanation = response.choices[0].message.content
        return explanation

    except Exception:
        # fallback explanation
        return f"""
Step-by-step solution:

Problem: {problem}

Final Answer: {answer}

The symbolic solver computed this result.
"""