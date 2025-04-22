from .base_agent import BaseAgent

class Judge(BaseAgent):
    def __init__(self, llm):
        role = "Judge"
        persona = "You are a fair and impartial judge presiding over a criminal murder trial. You must follow courtroom procedure, rule on objections, and guide the trial process. Your language should be formal and authoritative."
        super().__init__(role, persona, llm)

    def rule_on_objection(self, objection_type, objecting_lawyer, opposing_lawyer, context):
        # This method would involve asking the LLM to make a ruling based on context
        # Implementing complex legal reasoning for rulings is advanced.
        # For a basic simulation, you could simplify this.
        current_situation = f"An objection of '{objection_type}' has been raised by {objecting_lawyer} against {opposing_lawyer}.\nContext of the objection: {context}\n\nYour ruling as the Judge (e.g., 'Sustained.' or 'Overruled.'):"
        response = self.generate_response(current_situation)
        return response

    def give_instructions(self, instructions):
         current_situation = f"You need to give instructions to the court or the jury. The instructions are: {instructions}\n\nYour statement as the Judge:"
         response = self.generate_response(current_situation)
         return response