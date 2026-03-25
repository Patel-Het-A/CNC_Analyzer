import streamlit as st
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pipeline.pipeline import CNCPipeline

load_dotenv()

st.set_page_config(page_title="CNC AI Analyzer", layout="wide")

st.markdown("<h1 style='text-align:center;'>🔧 CNC AI Analyzer</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.subheader("📥 Enter G-code")

    gcode_input = st.text_area(
        "",
        height=250,
        placeholder="Paste your G-code here..."
    )

    run_btn = st.button("🚀 Run Analysis", use_container_width=True)

if run_btn:

    if not gcode_input.strip():
        st.warning("Please enter G-code")
        st.stop()

    gcode = gcode_input.strip().split("\n")

    api_key = os.getenv("GROQ_API_KEY")
    pipeline = CNCPipeline(api_key=api_key)

    result = pipeline.run(gcode)

    st.divider()

    with st.expander("📊 Metrics", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Original")
            st.json(result["metrics"]["original"])

        with col2:
            st.markdown("### Optimized")
            st.json(result["metrics"]["optimized"])

        st.success(f"Improvement: {result['metrics']['improvemnt']}%")

    with st.expander("⚠️ Issues", expanded=False):
        if result["issues"]:
            for issue in result["issues"]:
                st.error(str(issue))
        else:
            st.success("No issues found")

    with st.expander("📈 Toolpath Visualization", expanded=False):

        fig = plt.figure(figsize=(10, 5))

        ax1 = fig.add_subplot(121, projection='3d')
        ax1.set_title("Original")

        for seg in result["toolpath"]:
            x = [seg.start.x, seg.end.x]
            y = [seg.start.y, seg.end.y]
            z = [seg.start.z, seg.end.z]
            ax1.plot(x, y, z, 'r' if seg.move_type == "G00" else 'b')

        ax2 = fig.add_subplot(122, projection='3d')
        ax2.set_title("Optimized")

        for seg in result["optimized_toolpath"]:
            x = [seg.start.x, seg.end.x]
            y = [seg.start.y, seg.end.y]
            z = [seg.start.z, seg.end.z]
            ax2.plot(x, y, z, 'r' if seg.move_type == "G00" else 'g')

        st.pyplot(fig)

    with st.expander("🤖 AI Explanation & Suggestions", expanded=False):

        if result["ai"]:
            st.markdown("### 🧠 Explanation")

            explanation_lines = result["ai"]["explanation"].split("\n")
            for line in explanation_lines:
                if line.strip():
                    st.code(line)

            st.markdown("### 💡 Suggestions")

            if not result["issues"]:
                st.success("No critical issues found")
            else:
                suggestion_lines = result["ai"]["suggestion"].split("\n")
                for line in suggestion_lines:
                    if line.strip():
                        st.code(line)

        else:
            st.warning("AI not enabled")