import os
from dotenv import load_dotenv
from groq import AsyncGroq  # <--- CORRECTED: Import the AsyncGroq client

# Load environment variables from .env file
load_dotenv()

# Configure the AsyncGroq client
try:
    # CORRECTED: Instantiate the AsyncGroq client
    client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY")) 
except Exception as e:
    print(f"CRITICAL ERROR: Failed to initialize Groq client. {e}")
    client = None

# This is the "System Prompt" that defines the AI's persona and rules.
SYSTEM_PROMPT = """
You are Kairos, a world-class Socratic tutor for the Rust programming language.
Your primary goal is to help a user understand a concept by guiding them, NOT by giving them the answer.
You will be given the user's code, the compiler error it produced, and a guiding question.
Your task is to rephrase or elaborate on the guiding question in a helpful, insightful, and encouraging way.

RULES:
1.  **NEVER, EVER provide the corrected code or the direct solution.**
2.  **DO NOT explain the error directly.** Instead, ask questions that lead the user to explain it themselves.
3.  Your response should be in the form of a question or a request for the user to think about a concept.
4.  Use analogies if they help clarify a concept.
5.  Keep your responses concise (2-4 sentences).
6.  Your tone is patient, wise, and encouraging.
"""

async def get_socratic_response(user_code: str, error_output: str, guiding_question: str) -> str | None:
    if not client:
        return "Error: AI Tutor is not configured."

    try:
        # Construct the detailed prompt for the AI
        user_prompt = f"""
        Here is the user's code:
        ```rust
        {user_code}
        ```

        Here is the compiler error it produced:
        ```
        {error_output}
        ```

        My guiding question for the user is: "{guiding_question}"

        Based on all this information, please provide your Socratic response to the user.
        """

        chat_completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            model="llama3-8b-8192", # Using a fast and capable model
            temperature=0.7,
        )
        
        response = chat_completion.choices[0].message.content
        return response.strip()

    except Exception as e:
        print(f"Error getting response from Groq: {e}")
        return "An error occurred while communicating with the AI. Please try again."