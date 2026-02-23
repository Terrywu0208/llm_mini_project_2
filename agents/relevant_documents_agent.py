"""
Relevant Documents Agent - Checks if retrieved documents are relevant to the user's query.
"""

from openai import OpenAI


class Relevant_Documents_Agent:
    def __init__(self, openai_client) -> None:
        """
        Initialize the Relevant_Documents_Agent.
        
        Args:
            openai_client: OpenAI client instance
        """
        self.openai_client = openai_client
        

    def get_relevance(self, conversation) -> str:
        """
        Get if the returned documents are relevant.
        
        Args:
            conversation: List of conversation messages with role and content
            
        Returns:
            "Relevant" or "Irrelevant"
        """
        # We assume conversation includes at least a user turn and some context
        prompt = """
You judge if the CONTEXT DOCUMENTS below are useful for answering the USER's question.
If the context documents contain information that can answer the user's question, reply with exactly: Relevant
If the context is unrelated or cannot answer the question, reply with exactly: Irrelevant
=== USER QUESTION ===
"""
        for msg in conversation:
            prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"
        prompt += "\nYour one-word answer (Relevant or Irrelevant):"

        try:
            completion = self.openai_client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": "You answer with one word only: Relevant (if the context documents help answer the user's question) or Irrelevant (if they do not)."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=15,
                temperature=0,
            )
            response = completion.choices[0].message.content.strip()
            # Clean/standardize: accept "relevant" or "irrelevant" anywhere in response
            r = (response or "").lower()
            if "irrelevant" in r:
                return "Irrelevant"
            if "relevant" in r:
                return "Relevant"
            return "Irrelevant"  # fallback if LLM outputs something unexpected
        except Exception as e:
            return f"Error judging relevance: {e}"
