import os
from dotenv import load_dotenv

from simulation.courtroom import Courtroom
# Load environment variables from .env file
load_dotenv()

# Initialize the LLM
# For Google Gemini:
from langchain_google_genai import ChatGoogleGenerativeAI
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key) # Or your chosen Gemini model

if __name__ == "__main__":
    courtroom_sim = Courtroom(llm)
    courtroom_sim.run_simulation()
    