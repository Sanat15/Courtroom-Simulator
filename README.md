# AI Courtroom Simulation

This project implements a basic courtroom trial simulation using Large Language Model (LLM) agents. The simulation features different legal roles powered by LLMs that interact based on a predefined case narrative.

## Features

* **LLM-Powered Agents:** Agents representing key courtroom roles (Judge, Prosecution Lawyer, Defense Lawyer, Witnesses) powered by a Large Language Model.
* **Defined Roles and Personas:** Each agent has a specific role, responsibilities, and a basic persona to guide their behavior and dialogue.
* **Case Narrative:** The simulation runs based on a predefined criminal case scenario (The State vs. Mukesh).
* **Basic Trial Phases:** Includes fundamental courtroom phases such as opening statements, witness examination, and closing arguments.
* **Dialogue Generation:** Agents generate natural language dialogue and responses using the integrated LLM.
* **Structured Project:** Code is organized into modules for agents, case data, and simulation logic.

## Setup

1.  **Clone or Download the Project:** Get the project files onto your local machine.
2.  **Install Python:** Ensure you have Python 3.7+ installed. Download from [python.org](https://www.python.org/).
3.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv courtroom_env
    ```
4.  **Activate the Virtual Environment:**
    * On macOS and Linux:
        ```bash
        source courtroom_env/bin/activate
        ```
    * On Windows:
        ```bash
        .\courtroom_env\Scripts\activate
        ```
5.  **Install Dependencies:** With the virtual environment activated, install the required libraries.
    ```bash
    pip install langchain langchain-google-genai python-dotenv # Add 'openai' instead of 'langchain-google-genai' if using OpenAI
    ```
6.  **Get Your LLM API Key:** Obtain an API key for a Large Language Model (e.g., Google Gemini from [aistudio.google.com](https://aistudio.google.com/) or OpenAI GPT).
7.  **Configure API Key:** Create a file named `.env` in the root directory of your project (`courtroom_simulation/`). Add your API key in the format:
    ```dotenv
    GOOGLE_API_KEY='YOUR_GOOGLE_GEMINI_API_KEY'
    # Or for OpenAI:
    # OPENAI_API_KEY='YOUR_OPENAI_API_KEY'
    ```
    Replace `'YOUR_GOOGLE_GEMINI_API_KEY'` (or `'YOUR_OPENAI_API_KEY'`) with your actual key.
8.  **Add `.env` to `.gitignore` (If Using Git):** Prevent your API key from being committed to version control. Create or open `.gitignore` in the root directory and add the line `.env`.

## Project Structure

courtroom_simulation/

├── agents/             # Contains code for different agent roles

│   ├── init.py

│   ├── base_agent.py   # Base class for all agents

│   ├── judge.py        # Judge agent

│   ├── lawyer.py       # Prosecution and Defense lawyers

│   ├── witness.py      # Witness agent

│   └── jury.py         # Jury agent (Optional, if implemented)

├── case_data/          # Contains the case narrative and evidence details

│   ├── init.py

│   └── mahesh_murder_case.py # Specific case data

├── simulation/         # Contains the main simulation logic

│   ├── init.py

│   └── courtroom.py    # Courtroom environment and simulation runner

├── main.py             # Entry point to run the simulation

└── .env                # Stores environment variables like API keys


## Running the Simulation

1.  **Activate your virtual environment:** Ensure your `courtroom_env` is activated in your terminal.
2.  **Navigate to the project directory:** Use `cd` to go into the `courtroom_simulation` folder.
3.  **Run the main script:**
    ```bash
    python main.py
    ```
    The simulation will start, and you will see the dialogue and events of the trial printed in your terminal.

## Customization

* **Case Data:** You can modify the case narrative, evidence, suspects, and witness knowledge by editing the `case_data/mahesh_murder_case.py` file. Update the dictionaries (`CASE_DETAILS`, `WITNESS_KNOWLEDGE`) to define a different case.
* **Agent Personas:** Adjust the `persona` strings within the agent class files (`judge.py`, `lawyer.py`, `witness.py`) to fine-tune their behavior and speaking style.
* **LLM Model:** Change the `model` parameter in `main.py` when initializing `ChatGoogleGenerativeAI` (or `ChatOpenAI`) to use a different LLM model if available and compatible.

---
