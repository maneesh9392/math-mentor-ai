# 🧠 Reliable Multimodal Math Mentor

An end-to-end AI system that solves JEE-style math problems using:

* RAG (Retrieval Augmented Generation)
* Multi-agent reasoning
* Multimodal input (text, image, audio)
* Human-in-the-loop (HITL)
* Persistent memory & self-learning

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
