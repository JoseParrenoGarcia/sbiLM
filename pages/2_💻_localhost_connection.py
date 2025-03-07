import streamlit as st

from utils.prompt_engineering_localhost import generate_feedback

# ---------------------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="Hugging face connection",
    layout="wide",
)

# ---------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# MAIN PANEL
# ---------------------------------------------------------------------
st.title("SBI Feedback Generator")

st.markdown("""
### Instructions:
1. Select the type of feedback.
2. Fill in the text bock.
3. Click 'Generate Feedback' to receive an AI-generated response.
""")

# Feedback Type Selection
feedback_type = st.radio("Type of Feedback", ["Recognition", "Growth", "Correction"], horizontal=True)

# Single Text Input Field
st.write("""
💡 **Tip:** When writing your feedback, consider the following structure:
- **Situation:** Describe the situation where the event occurred.
- **Behavior:** What specific behavior did you observe?
- **Impact:** What impact did the behavior have on the team, project, or goals?
- **Next Steps:** What actions should be taken next?
""")
feedback_text = st.text_area("Enter your feedback description:", placeholder="Example: During the team meeting, an issue with the data pipeline was raised. Alex quickly analyzed the logs and identified the root cause. This prevented a major delay in the project timeline. We should document this process to improve troubleshooting in the future.")

# Generate Feedback Button
if st.button("Generate Feedback"):
    response = generate_feedback(feedback_text, feedback_type)
    st.markdown(f"### AI Feedback:\n{response}")


