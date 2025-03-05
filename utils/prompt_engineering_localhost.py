import ollama

def generate_feedback(feedback_text, feedback_type="Recognition"):
    """
    Calls DeepSeek-R1 14B locally using Ollama with an optimized prompt.
    """

    prompt = f"""
    You are an expert leadership coach trained in the SBI (Situation-Behavior-Impact) feedback model.
    Your task is to generate {feedback_type} feedback based on the user’s input.

    ## Instructions
    - Use the SBI framework: Situation → Behavior → Impact → Next Steps.
    - Ensure feedback is clear, specific, and actionable.
    - The tone should be radically candid.
    - Format the output as a structured phrase or paragraph.

    ---

    Now, generate structured SBI **{feedback_type}** feedback for the following input:

    "{feedback_text}"
    """

    # Call the local DeepSeek-R1 model using Ollama
    response = ollama.chat(model="deepseek-r1:14b", messages=[{"role": "user", "content": prompt}])

    return response["message"]["content"]
