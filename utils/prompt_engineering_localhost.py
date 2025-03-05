import ollama
import re

from utils.examples_database import EXAMPLES_DB

def clean_response(response):
    """
    Cleans the response from DeepSeek by removing any text before </think> and stripping special tags.
    """
    # Remove everything BEFORE </think>
    response_clean = re.sub(r".*</think>", "", response, flags=re.DOTALL).strip()

    return response_clean



def generate_feedback(feedback_text, feedback_type="Recognition"):
    """
    Calls DeepSeek-R1 14B locally using Ollama with an optimized prompt.
    """
    example = EXAMPLES_DB.get(feedback_type, {"input": "", "output": ""})

    prompt = f"""
    You are an expert leadership coach trained in the SBI (Situation-Behavior-Impact) feedback model.
    Your task is to generate {feedback_type} feedback based on the user’s input.

    ## Instructions
    - Use the SBI framework: Situation → Behavior → Impact → Next Steps.
    - Ensure feedback is clear, specific, and actionable.
    - The tone should be radically candid.
    - Format the output as a structured phrase or paragraph.
    
    ## **Example Feedback**
    **User Input:** "{example['input']}"
    
    **Expected Output:**
    {example['output']}

    ---

    Now, generate structured SBI **{feedback_type}** feedback for the following input:

    "{feedback_text}"
    """

    # Call the local DeepSeek-R1 model using Ollama
    response = ollama.chat(model="deepseek-r1:14b", messages=[{"role": "user", "content": prompt}])
    cleaned_response = clean_response(response["message"]["content"])

    return cleaned_response
