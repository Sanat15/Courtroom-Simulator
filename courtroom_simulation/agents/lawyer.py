from .base_agent import BaseAgent

class Lawyer(BaseAgent):
    def __init__(self, role, side, llm):
        # Role will be "Prosecution Lawyer" or "Defense Lawyer"
        # Side will be "Prosecution" or "Defense"
        persona = f"You are the {role} representing the {side} in a criminal murder trial. Your goal is to argue your case effectively, question witnesses strategically, and persuade the jury (if applicable). You must adhere to courtroom etiquette."
        super().__init__(role, persona, llm)
        self.side = side

    def make_opening_statement(self, case_summary):
        current_situation = f"It is your turn to make the opening statement for the {self.side}. Summarize your case and what you intend to prove.\nCase Summary: {case_summary}\n\nYour Opening Statement as the {self.role}:"
        response = self.generate_response(current_situation)
        return response

    def question_witness(self, witness_name, question):
        current_situation = f"You are questioning witness {witness_name}. Ask your question.\nYour Question as the {self.role}:"
        response = self.generate_response(current_situation)
        return response

    def make_closing_argument(self, case_summary, key_evidence):
        current_situation = f"It is your turn to make the closing argument for the {self.side}. Summarize the evidence and arguments, and urge for a verdict.\nCase Summary: {case_summary}\nKey Evidence Presented: {key_evidence}\n\nYour Closing Argument as the {self.role}:"
        response = self.generate_response(current_situation)
        return response

    def raise_objection(self, objection_type, reason):
        # This will likely just be a signal to the simulation loop
        # The Judge agent will handle the ruling
        print(f"{self.role} raises an objection: {objection_type}. Reason: {reason}")
        return f"Objection, {objection_type}, Your Honor. {reason}"