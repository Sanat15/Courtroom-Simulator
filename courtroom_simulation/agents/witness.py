from .base_agent import BaseAgent

class Witness(BaseAgent):
    def __init__(self, name, relationship_to_case, knowledge, potential_bias, llm):
        role = f"Witness: {name}"
        persona = f"You are {name}, a witness in a criminal murder trial. Your role is to answer questions truthfully based on your knowledge. You are {relationship_to_case}. Your knowledge includes: {knowledge}. Be mindful of your potential bias: {potential_bias}."
        super().__init__(role, persona, llm)
        self.name = name
        self.knowledge = knowledge # Store specific facts the witness knows
        
    def respond_to_question(self, question, questioning_lawyer):
        # Format the witness's specific knowledge for the prompt input
        # self.knowledge is a dictionary like {"fact1": "detail1", "fact2": "detail2"}
        knowledge_context = "\nKey Facts I Know:\n"
        if self.knowledge: # Check if the knowledge dictionary is not empty
            knowledge_context += "\n".join([f"- {k}: {v}" for k, v in self.knowledge.items()])
        else:
            knowledge_context += "- No specific facts provided."


        # Construct the input string that goes into the {input} placeholder of the BaseAgent prompt
        # This provides the LLM with the context it needs to answer as this specific witness
        current_situation = f"""You are on the witness stand being questioned by {questioning_lawyer}.
Based on your role, persona, and the following key facts you know, respond truthfully and concisely to the question. Only use information you, as this witness, would realistically know based on the provided facts.
{knowledge_context}

Question: {question}

Your Response as {self.name}:"""

        # Call the generate_response method inherited from BaseAgent,
        # passing the detailed current_situation as the 'input'
        response = self.generate_response(current_situation)
        return response