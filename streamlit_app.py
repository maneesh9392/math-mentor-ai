from app.agents.parser_agent import run_parser_agent
import streamlit as st
from app.utils.ocr_utils import extract_text_from_image
from app.utils.audio_utils import transcribe_audio
from app.utils.confidence import needs_hitl
from app.rag.retriever import retrieve_context
from app.agents.intent_router import route_intent
from app.agents.solver_agent import run_solver_agent
from app.agents.verifier_agent import run_verifier_agent
from app.agents.explainer_agent import run_explainer_agent
from app.memory.memory_store import store_interaction
from app.memory.memory_retriever import retrieve_similar_problem
from app.agents.guardrail_agent import run_guardrail

st.set_page_config(page_title="AI Math Mentor", layout="wide")

st.title("🧠 Multimodal Math Mentor")

mode = st.selectbox(
    "Choose Input Mode",
    ["Text", "Image", "Audio"]
)

extracted_text = ""
confidence_score = 1.0

# ================= TEXT =================
if mode == "Text":
    extracted_text = st.text_area("Enter math problem")

# ================= IMAGE =================
elif mode == "Image":
    image_file = st.file_uploader(
        "Upload image",
        type=["png", "jpg", "jpeg"]
    )

    if image_file:
        with st.spinner("Running OCR..."):
            extracted_text, confidence_score = extract_text_from_image(image_file)

# ================= AUDIO =================
elif mode == "Audio":
    audio_file = st.file_uploader(
        "Upload audio",
        type=["wav", "mp3"]
    )

    if audio_file:
        with st.spinner("Transcribing audio..."):
            extracted_text, confidence_score = transcribe_audio(audio_file)

# ================= PREVIEW =================

if extracted_text:

    st.divider()
    st.subheader("🔍 Extracted Text (Editable)")

    extracted_text = st.text_area(
        "Please verify before solving:",
        value=extracted_text,
        height=150
    )

    st.write(f"Confidence: **{confidence_score:.2f}**")

    # ================= HITL TRIGGER =================

    if needs_hitl(confidence_score):
        st.warning("⚠️ Low confidence detected — Human review recommended.")

    if st.button("✅ Solve Problem"):
        parsed_output = run_parser_agent(extracted_text)
        st.divider()
        st.subheader("🧠 Parser Output")

        st.json(parsed_output)
        if parsed_output["needs_clarification"]:
            st.error(f"⚠️ Clarification needed: {parsed_output['ambiguity_reason']}")
        
            # ================= GUARDRAIL =================
            
        guardrail = run_guardrail(parsed_output["problem_text"])

        if not guardrail["allowed"]:
            st.error(f"🚫 Blocked: {guardrail['reason']}")
            st.stop()

            # ================= MEMORY LOOKUP =================

        similar_memory = retrieve_similar_problem(parsed_output["problem_text"])

        if similar_memory:
            st.info("🧠 Found similar previously solved problem!")

            st.write("Previous answer:")
            st.success(similar_memory["solver_output"]["result"])
                # ================= RAG RETRIEVAL =================

        retrieved_chunks = retrieve_context(parsed_output["problem_text"])
        st.divider()
        st.subheader("📚 Retrieved Context")
        for i, chunk in enumerate(retrieved_chunks, 1):
            st.markdown(f"**Source {i}: {chunk['source']}**")
            st.write(chunk["text"])
        
            # ================= INTENT ROUTER =================
        route = route_intent(parsed_output)

        # ================= SOLVER =================
        solver_output = run_solver_agent(parsed_output, route)

        # ================= VERIFIER =================
        verifier_output = run_verifier_agent(parsed_output, solver_output)
        # ================= FINAL CONFIDENCE =================
        final_confidence = min(
            confidence_score,  # OCR/ASR confidence
            solver_output["confidence"],
            verifier_output["confidence"],
        )

        # ================= EXPLAINER =================
        explanation = run_explainer_agent(parsed_output, solver_output)

        # ================= AGENT TRACE =================
        st.divider()
        st.subheader("🔎 Agent Trace")

        st.write("Route:", route)
        st.write("Solver confidence:", solver_output["confidence"])
        st.write("Verifier:", verifier_output)
            # ================= CONFIDENCE METER =================
        st.divider()
        st.subheader("📊 Confidence Indicator")

        st.progress(float(final_confidence))
        st.write(f"Overall Confidence: **{final_confidence:.2f}**")
            # ================= SMART HITL =================
        hitl_required = (
            needs_hitl(confidence_score)
            or parsed_output["needs_clarification"]
            or not verifier_output["verified"]
            or final_confidence < 0.65
        )

        if hitl_required:
            st.warning("⚠️ Human Review Recommended (HITL Triggered)")
        if st.button("🔍 Request Human Review"):
            st.info("👤 Problem flagged for human review.")

        # ================= FINAL ANSWER =================
        st.divider()
        st.subheader("✅ Final Answer")

        if verifier_output["verified"]:
            st.success(solver_output["result"])
        else:
            st.error("Solution uncertain — HITL recommended.")

        st.subheader("📘 Explanation")
        st.write(explanation)
        st.divider()
        st.subheader("🧾 Feedback")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Correct"):
                st.success("Feedback stored (correct).")

        with col2:
            if st.button("❌ Incorrect"):
                comment = st.text_input("What was wrong?")
                st.warning("Feedback noted for learning.")

            # ================= STORE MEMORY =================
        store_interaction(
            raw_input=extracted_text,
            parsed_problem=parsed_output,
            retrieved_context=retrieved_chunks,
            solver_output=solver_output,
            verifier_output=verifier_output,
            user_feedback=None,
        )

