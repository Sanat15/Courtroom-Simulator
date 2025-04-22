import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Assuming you are using Google Gemini, adjust if using OpenAI or other
from langchain_google_genai import ChatGoogleGenerativeAI
# Or for OpenAI: from langchain_openai import ChatOpenAI

class BaseAgent:
    def __init__(self, role, persona, llm):
        self.role = role
        self.persona = persona
        self.llm = llm # The initialized LLM model
        self.memory = [] # Simple list to store dialogue history
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", f"You are a {self.role} in a courtroom simulation. {self.persona}"),
            # This is the crucial line - it should ONLY expect '{input}'
            ("human", "{input}")
        ])
        self.chain = {'input': RunnablePassthrough()} | self.prompt_template | self.llm | StrOutputParser()

    def add_to_memory(self, speaker, text):
        self.memory.append(f"{speaker}: {text}")

    def get_memory_context(self):
        # Provide recent conversation history as context
        return "\n".join(self.memory[-10:]) # Adjust number of lines as needed

    def generate_response(self, current_situation):
        # Construct the input for the LLM
        context = self.get_memory_context()
        input_text = f"Current Situation: {current_situation}\n\nConversation History:\n{context}\n\nYour Response as the {self.role}:"

        try:
            response = self.chain.invoke({"input": input_text})
            self.add_to_memory(self.role, response)
            return response
        except Exception as e:
            print(f"Error generating response for {self.role}: {e}")
            return f"({self.role} is unable to respond at this time.)"

    def __str__(self):
        return self.role