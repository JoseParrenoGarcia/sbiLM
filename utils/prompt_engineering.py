import streamlit as st
import requests
import os

# Load API key from secrets
# API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
# API_URL = "https://api-inference.huggingface.co/models/deepseek-ai/deepseek-llm-7b-chat"

# Try loading from Streamlit secrets first (for Streamlit Cloud deployment)
if "HUGGINGFACE_API_KEY" in st.secrets:
    API_KEY = st.secrets["HUGGINGFACE_API_KEY"]
# Otherwise, try loading from an environment variable (for GitHub Actions or local development)
else:
    API_KEY = os.getenv("HUGGINGFACE_API_KEY")

HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def clean_response(response):
    separator_token = "### RESPONSE START ###"
    separator_end = "### RESPONSE END ###"
    response_clean = response.strip().split(separator_token, 1)[-1].strip()
    if separator_end in response_clean:
        response_clean = response_clean.split(separator_end, 1)[0].strip()

    return response_clean


def query_huggingface(payload):
    """Send request to Hugging Face API and return response."""
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        print(f"API Error: {response.status_code} - {response.text}")
        return {"error": f"API error {response.status_code}: {response.text}"}

    result = response.json()
    print(result[0]["generated_text"])

    # Ensure response contains the expected output
    if isinstance(result, list) and "generated_text" in result[0]:
        return clean_response(result[0]["generated_text"])
    elif isinstance(result, dict) and "error" in result:
        return result["error"]
    else:
        return "Unexpected response format from API."


def generate_feedback(feedback_text, feedback_type):
    """
    Calls the Hugging Face API to generate SBI feedback.
    """
    separator_token = "### RESPONSE START ###"

    prompt = f"""
        The SBI (Situation-Behavior-Impact) feedback model is a structured approach to giving clear and objective feedback.
        - **Situation:** Describe the context in which the behavior occurred.
        - **Behavior:** Explain the specific behavior you observed.
        - **Impact:** Share the effect this behavior had on the team, project, or outcome.
        - **Next Steps:** Suggest how to improve or reinforce this behavior in the future.

        # Below is an examples of recognition using SBI feedback:
        # 
        # **Recognition Example:**
        # **Situation:** During the client presentation, the team faced a difficult question about the data methodology.
        # **Behavior:** Alex confidently explained the statistical approach and provided clear, well-reasoned answers.
        # **Impact:** This increased the client's trust and led to a successful contract extension.
        # **Next Steps:** Continue preparing for potential tough questions in advance.

        # **Growth Example:**
        # **Situation:** During the sprint review, deadlines were missed due to last-minute changes.
        # **Behavior:** The team was not informed in time, causing confusion and delays.
        # **Impact:** This led to extra workload and misalignment in priorities.
        # **Next Steps:** Improve communication of changes as early as possible.
        # 
        # **Correction Example:**
        # **Situation:** In a high-stakes debugging session, Alex interrupted others frequently.
        # **Behavior:** This disrupted the flow of discussion and made it difficult to find a resolution.
        # **Impact:** The debugging process took longer, and team morale was affected.
        # **Next Steps:** Allow others to share their thoughts before interjecting.

        # **Output Format:** Use proper Markdown formatting:
        # - Bold headings (**Situation:**, **Behavior:**, etc.).
        # - Use bullet points or numbers where needed.
        # - Keep spacing clean and readable.

        # **Output example:**
        # - **Situation:** During the team meeting, an issue with the data pipeline was raised.
        # - **Behavior:** You quickly analyzed the logs and identified the root cause.
        # - **Impact:** This prevented a major delay in the project timeline.
        # - **Next Steps:** We should document this process to improve troubleshooting in the future. Would you be happy to take the lead?
        # - Your quick thinking and problem-solving skills saved the team from a potential delay. By analyzing the logs and identifying the root cause of the data pipeline issue, you prevented a major setback in our project timeline. This demonstrates your ability to stay calm under pressure and make quick, informed decisions. Let's make sure to document this process so we can use it as a reference for future troubleshooting. Great job, Alex!

        **Requirements:**  Ensure your feedback is:
        - Radically candid.
        - Refers to the person we want to provide feedback to.
        - Present the SBIN bullet points first.
        - Follow them with a short paragraph which I can use to read out loud.

        Now, generate {feedback_type} feedback based on the following input:

        {feedback_text}

        {separator_token}
        """

    payload = {"inputs": prompt, "parameters": {"max_length": 500}}
    response = query_huggingface(payload)

    return response