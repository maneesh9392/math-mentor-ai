import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def run_explainer_agent(parsed_problem: dict, solver_output: dict):

    problem = parsed_problem["problem_text"]
    answer = solver_output["result"]

    prompt = f"""
You are a math tutor helping a student solve a JEE-style problem.

Problem:
{problem}

Final Answer:
{answer}

Explain the solution step-by-step clearly for a high school student.
Do not change the final answer.
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

        return response.choices[0].message.content

    except Exception:
        return f"""
Step-by-step solution:

Problem: {problem}

Final Answer: {answer}
"""