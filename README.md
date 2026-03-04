# 🧠 Reliable Multimodal Math Mentor

An end-to-end AI system that solves JEE-style math problems using:

* RAG (Retrieval Augmented Generation)
* Multi-agent reasoning
* Multimodal input (text, image, audio)
* Human-in-the-loop (HITL)
* Persistent memory & self-learning

---
The current version of the Multimodal Math Mentor is designed to reliably solve foundational to moderate-level JEE-style mathematics problems, particularly in areas such as algebra, basic calculus, probability, and introductory linear algebra concepts. Because the system uses a combination of a structured parser, symbolic computation through SymPy, a retrieval-augmented knowledge base (RAG), and multiple specialized agents such as parser, solver, verifier, and explainer, it performs well on problems that can be expressed as clear equations or standard mathematical rules. For example, it can accurately solve single-variable algebraic equations such as 2x + 5 = 15, simple polynomial equations, and basic derivatives such as d/dx(x^n). The RAG component allows the system to retrieve relevant mathematical formulas and concepts from a curated knowledge base, which helps the explainer agent generate understandable step-by-step explanations for students. In addition, the inclusion of multimodal input through text, image OCR, and audio transcription, along with a verifier agent for correctness checks and a memory layer for storing past problems and feedback, makes the system reliable for educational scenarios involving straightforward analytical problems and concept-based questions.

However, the current implementation has limitations when dealing with more complex or multi-step mathematical problems such as advanced calculus, including product rule, chain rule, and integrals, systems of equations, optimization problems, or word-based mathematical reasoning that requires deeper planning. These limitations mainly arise because the solver agent currently uses rule-based parsing and a limited set of SymPy operations rather than a full reasoning planner. Despite this, the architecture of the system already supports significant expansion. With a few targeted modifications, such as integrating an LLM-based reasoning planner, expanding the set of symbolic math tools including integration, multi-variable solving, and matrix operations, and improving the mathematical expression parser, the system could scale to solve much more difficult problems including JEE Main medium-to-hard questions and complex multi-step analytical problems. Because the project already includes modular agents, RAG retrieval, tool-based solving, and memory-driven learning, it provides a strong foundation that can be extended into a more advanced AI tutoring system capable of handling higher-level mathematics and more sophisticated reasoning tasks.

---

## 🚀 Features

### ✅ Multimodal Input

* Text problems
* Image OCR extraction
* Audio speech-to-text

### ✅ Intelligent Agents

* Parser Agent
* Intent Router
* Solver Agent (SymPy powered)
* Verifier / Critic Agent
* Explainer / Tutor Agent
* Guardrail Agent

### ✅ RAG Pipeline

* Curated math knowledge base
* FAISS vector retrieval
* Source-backed reasoning

### ✅ Human-in-the-Loop (HITL)

Triggered when:

* OCR/ASR confidence low
* Parser detects ambiguity
* Verifier uncertain
* User requests review

### ✅ Memory & Self-Learning

System stores:

* Past problems
* Solutions
* Feedback signals

And retrieves similar problems at runtime.

---

## 🏗️ Architecture

# System Architecture

A[User Input] --> B[Multimodal Parser]
B --> C[Parser Agent]
C --> D[Guardrail Agent]
D --> E[Memory Lookup]
E --> F[RAG Retriever]
F --> G[Intent Router]
G --> H[Solver Agent]
H --> I[Verifier Agent]
I --> J[Explainer Agent]
J --> K[Confidence + HITL]
K --> L[User Feedback]
L --> M[Memory Store]


---

## ⚙️ Setup

```bash
git clone <repo>
cd math-mentor-ai
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

## 🌐 Deployed App

https://math-mentor-ai-3flwqrwsfwzrevw5k5nktv.streamlit.app/

---

## 📊 Evaluation Coverage

* ✅ Multimodal parsing
* ✅ RAG pipeline
* ✅ Multi-agent system
* ✅ HITL integration
* ✅ Memory & learning
* ✅ Deployment ready

---

