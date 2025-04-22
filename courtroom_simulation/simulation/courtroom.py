import time # To add pauses between turns
from agents.judge import Judge
from agents.lawyer import Lawyer
from agents.witness import Witness

from case_data.mahesh_murder_case import CASE_DETAILS, WITNESS_KNOWLEDGE # Import your case data

class Courtroom:
    def __init__(self, llm):
        self.llm = llm
        self.judge = Judge(llm)
        self.prosecution_lawyer = Lawyer("Prosecution Lawyer", "Prosecution", llm)
        self.defense_lawyer = Lawyer("Defense Lawyer", "Defense", llm)
        self.defendant = "Mukesh" # Represent defendant as a simple string for now
        self.witnesses = self._create_witnesses()
        self.jury = Jury(llm) if False else None # Set to Jury(llm) to include jury
        self.case_details = CASE_DETAILS
        self.current_stage = "opening_statements"
        self.active_speaker = None
        self.transcript = [] # To record the proceedings

    def _create_witnesses(self):
        # Instantiate Witness agents based on your case data
        witnesses = {
            "Store Owner": Witness(
                name="Store Owner",
                relationship_to_case="discovered the body",
                knowledge=WITNESS_KNOWLEDGE["Store Owner"],
                potential_bias="None specific to the suspects, primarily concerned with their business.",
                llm=self.llm
            ),
            "Mahesh's Wife": Witness(
                name="Mahesh's Wife",
                relationship_to_case="the victim's spouse",
                knowledge=WITNESS_KNOWLEDGE["Mahesh's Wife"],
                potential_bias="Blames Mukesh for the murder.",
                llm=self.llm
            ),
            # Add other witnesses here following the same pattern
            "Mahesh's Son 1": Witness("Mahesh's Son 1", "the victim's son", WITNESS_KNOWLEDGE.get("Mahesh's Son 1", {}), "May align with mother's view.", self.llm),
            "Mahesh's Son 2": Witness("Mahesh's Son 2", "the victim's son", WITNESS_KNOWLEDGE.get("Mahesh's Son 2", {}), "May align with mother's view.", self.llm),
            "Mahesh's Daughter": Witness("Mahesh's Daughter", "the victim's daughter", WITNESS_KNOWLEDGE.get("Mahesh's Daughter", {}), "May align with mother's view.", self.llm),
             "Neighbour 1": Witness("Neighbour 1", "the victim's neighbour", WITNESS_KNOWLEDGE.get("Neighbour 1", {}), "May be defensive if suspected.", self.llm),
             "Neighbour 2": Witness("Neighbour 2", "the victim's neighbour", WITNESS_KNOWLEDGE.get("Neighbour 2", {}), "May be defensive if suspected.", self.llm),
             "Office Mate 1": Witness("Office Mate 1", "the victim's office mate", WITNESS_KNOWLEDGE.get("Office Mate 1", {}), "May have knowledge of work relationships.", self.llm),
             "Office Mate 2": Witness("Office Mate 2", "the victim's office mate", WITNESS_KNOWLEDGE.get("Office Mate 2", {}), "May have knowledge of work relationships.", self.llm),
        }
        return witnesses


    # In simulation/courtroom.py, inside the Courtroom class

    def run_simulation(self):
        # Run the simulation phases
        self._opening_statements()
        self._present_evidence_and_testimony()
        self._closing_arguments()
        # Skip jury if not included
        # self._jury_deliberation_and_verdict() # Call only if jury is active

        # --- Judge's Ruling Phase ---
        # Summarize the trial for the Judge to make a ruling
        trial_summary_for_judge = self._generate_trial_summary() # Create a method to summarize the transcript

        ruling_prompt = f"""Based on the following summary of the trial proceedings, deliver a final ruling.
        Consider the arguments, evidence mentioned, and witness testimonies.
        State your verdict clearly as either 'GRANTED' or 'DENIED'.

        Trial Summary:
        {trial_summary_for_judge}

        Your Ruling as the Judge (State GRANTED or DENIED):"""

        # Prompt the Judge agent for a ruling
        # Need to call the LLM via the Judge agent's method
        # Assuming Judge has a method like make_ruling
        # You might need to add a specific method to Judge for this final ruling prompt
        final_ruling_text = self.judge.generate_response(ruling_prompt) # Reuse generate_response or add a new method

        # --- Parse the Judge's Ruling ---
        # Look for "GRANTED" or "DENIED" in the response text
        if "GRANTED" in final_ruling_text.upper():
            return "GRANTED"
        elif "DENIED" in final_ruling_text.upper():
            return "DENIED"
        else:
            # Handle cases where the Judge doesn't output GRANTED or DENIED clearly
            print(f"Warning: Judge did not return a clear GRANTED or DENIED verdict. Response: {final_ruling_text}")
            return "UNKNOWN" # Or handle as an error


    def _generate_trial_summary(self):
        # Create a summary of the transcript for the Judge
        # This is a basic summary; for better results, you might use
        # an LLM to summarize the key arguments and evidence.
        summary = "Trial Proceedings:\n" + "\n".join(self.transcript)
        # You might truncate the transcript or use an LLM to summarize
        return summary

    def _add_transcript(self, speaker, text):
        line = f"[{speaker}] {text}"
        print(line)
        self.transcript.append(line)

    def _opening_statements(self):
        self._add_transcript("Judge", self.judge.give_instructions("We will now begin with opening statements. The court will listen closely to the presentations from both the prosecution and the defense."))
        time.sleep(2)

        self._add_transcript(self.prosecution_lawyer.role,
                             self.prosecution_lawyer.make_opening_statement(self.case_details["prosecution_theory"]))
        time.sleep(5) # Pause to simulate real-time

        self._add_transcript(self.defense_lawyer.role,
                             self.defense_lawyer.make_opening_statement(self.case_details["defense_theory"]))
        time.sleep(5)

    def _present_evidence_and_testimony(self):
        self._add_transcript("Judge", self.judge.give_instructions("The prosecution will now present its evidence and call witnesses."))
        time.sleep(2)

        # --- Prosecution Presents Case ---
        prosecution_witness_order = ["Store Owner", "Mahesh's Wife", "Mahesh's Son 1", "Mahesh's Daughter"] # Example order

        for witness_name in prosecution_witness_order:
            witness = self.witnesses.get(witness_name)
            if not witness:
                print(f"Witness {witness_name} not found.")
                continue

            self._add_transcript("Judge", self.judge.give_instructions(f"The prosecution calls {witness_name} to the stand."))
            time.sleep(3)

            # Direct Examination by Prosecution
            self._add_transcript(self.prosecution_lawyer.role, f"Direct examination of {witness_name}.")
            # You'll need to define a sequence of questions or a strategy for the lawyer agent
            # For simplicity, let's ask a few pre-defined questions or have the LLM generate
            # questions based on the witness's knowledge and prosecution's theory.

            # Basic example: Ask the witness to state what they know
            question1 = f"Please tell the court, in your own words, what you know about the events surrounding Mahesh's death."
            self._add_transcript(self.prosecution_lawyer.role, question1)
            time.sleep(3)
            response1 = witness.respond_to_question(question1, self.prosecution_lawyer.role)
            self._add_transcript(witness.name, response1)
            time.sleep(3)

            # Example of asking about a specific piece of knowledge
            if witness_name == "Store Owner":
                 question2 = f"Can you describe the condition of your store when you found Mr. Mahesh?"
                 self._add_transcript(self.prosecution_lawyer.role, question2)
                 time.sleep(3)
                 response2 = witness.respond_to_question(question2, self.prosecution_lawyer.role)
                 self._add_transcript(witness.name, response2)
                 time.sleep(3)
            elif witness_name == "Mahesh's Wife":
                 question2 = f"What was the relationship like between your husband, Mahesh, and his brother, Mukesh?"
                 self._add_transcript(self.prosecution_lawyer.role, question2)
                 time.sleep(3)
                 response2 = witness.respond_to_question(question2, self.prosecution_lawyer.role)
                 self._add_transcript(witness.name, response2)
                 time.sleep(3)

            # --- Cross-Examination by Defense ---
            self._add_transcript("Judge", self.judge.give_instructions(f"Cross-examination by the defense."))
            time.sleep(2)

            self._add_transcript(self.defense_lawyer.role, f"Cross-examination of {witness_name}.")
            # Defense lawyer asks questions to challenge testimony or introduce doubt
            # Example: Ask about the witness's potential bias or inconsistencies
            cross_question1 = f"You mentioned [something from witness's direct testimony]. Isn't it true that [introduce a fact or suggestion that contradicts or casts doubt]?"
            if witness_name == "Mahesh's Wife":
                 cross_question1 = f"You mentioned you blame Mukesh for the murder. Isn't it true you've had disagreements with Mukesh in the past?"
            elif witness_name == "Store Owner":
                 cross_question1 = f"You stated you found the body around [time]. Is it possible it could have been earlier or later?"


            self._add_transcript(self.defense_lawyer.role, cross_question1)
            time.sleep(3)
            response_cross1 = witness.respond_to_question(cross_question1, self.defense_lawyer.role)
            self._add_transcript(witness.name, response_cross1)
            time.sleep(3)

            # --- Redirect Examination (Optional) ---
            # You could add redirect here if needed

            self._add_transcript("Judge", self.judge.give_instructions(f"{witness_name} is excused."))
            time.sleep(2)

        # --- Defense Presents Case ---
        self._add_transcript("Judge", self.judge.give_instructions("The defense will now present its case."))
        time.sleep(2)

        defense_witness_order = ["Mukesh's Party Friend (New Witness Agent needed!)", "Neighbour 1", "Office Mate 1"] # Example order, you need to create these agents
        # You would repeat the process of calling and examining defense witnesses here
        # This requires creating Witness agents for Mukesh's alibi witness, neighbours, and office mates.
        # For now, let's skip the full implementation to keep the guide focused, but you would
        # follow the same pattern as the prosecution witnesses.

        print("\n[Code for Defense Witnesses and their examination would go here]")
        time.sleep(3)

        # --- Introduction of Evidence ---
        # You can represent evidence by having lawyers refer to it in their questions
        # or statements, or by having a separate mechanism for "admitting" evidence.
        # For this guide, agents can refer to evidence in their dialogue based on the
        # CASE_DETAILS["evidence"] dictionary.

        # Example: Prosecution refers to CCTV footage
        # In a lawyer's questioning or statement:
        # "Your Honor, we would like to present evidence, Exhibit A, the CCTV footage from the store."
        # "As the CCTV footage clearly shows..."

        # Implementing formal evidence handling (marking exhibits, objections) adds complexity.

    def _closing_arguments(self):
        self._add_transcript("Judge", self.judge.give_instructions("We will now proceed to closing arguments."))
        time.sleep(2)

        self._add_transcript(self.prosecution_lawyer.role,
                             self.prosecution_lawyer.make_closing_argument(
                                 self.case_details["prosecution_theory"],
                                 self.case_details["evidence"] # Pass evidence details
                                 ))
        time.sleep(5)

        self._add_transcript(self.defense_lawyer.role,
                             self.defense_lawyer.make_closing_argument(
                                 self.case_details["defense_theory"],
                                 self.case_details["evidence"] # Pass evidence details
                                 ))
        time.sleep(5)

    def _jury_deliberation_and_verdict(self):
        if self.jury:
            self._add_transcript("Judge", self.judge.give_instructions("Members of the jury, you will now retire to consider your verdict."))
            time.sleep(3)
            # In a real simulation, the jury agent would deliberate here
            verdict = self.jury.deliberate_and_reach_verdict()
            self._add_transcript(self.jury.role, f"We the jury find the defendant, Mukesh, {verdict}.")
            time.sleep(3)
        else:
            print("\n[No jury in this simulation.]")


    def _final_judgment(self):
        # In a non-jury trial, the judge delivers the verdict.
        # In a jury trial, the judge accepts the verdict and gives final remarks/sentencing if guilty.
        if not self.jury:
             # Simplified judge's verdict for no jury
             judge_verdict_situation = "Considering all the evidence and arguments presented, what is your verdict for the defendant, Mukesh (Guilty or Not Guilty)? Your Judgment:"
             final_judgment = self.judge.generate_response(judge_verdict_situation)
             self._add_transcript("Judge", final_judgment)
        else:
             # Judge acknowledges jury verdict
             self._add_transcript("Judge", self.judge.give_instructions("The court accepts the jury's verdict."))
             # Add sentencing dialogue if the verdict was guilty - this requires more complex logic.


# Example of how to run the simulation in main.py:
# from simulation.courtroom import Courtroom
# from main import llm # Assuming llm is initialized in main.py

# if __name__ == "__main__":
#     courtroom_sim = Courtroom(llm)
#     courtroom_sim.run_simulation()