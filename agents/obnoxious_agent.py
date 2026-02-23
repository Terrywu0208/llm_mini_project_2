"""
Obnoxious Agent - Checks if user queries are rude, offensive, or inappropriate.
"""

from openai import OpenAI


class Obnoxious_Agent:
    def __init__(self, client) -> None:
        """
        Initialize the Obnoxious_Agent.
        
        Args:
            client: OpenAI client instance
        """
        self.client = client
        self.prompt = (
            "You are an obnoxious filter. Your job is to check if a user's query is rude, offensive, or inappropriate, "
            "or if it violates any social conduct expected in a classroom or professional environment. "
            "If the message is obnoxious, respond with 'OBNOXIOUS'. Otherwise, respond only with 'NOT OBNOXIOUS' and nothing else."
        )

    def set_prompt(self, prompt):
        """
        Set the prompt for the Obnoxious_Agent.
        
        Args:
            prompt: New prompt string
        """
        self.prompt = prompt

    def extract_action(self, response) -> bool:
        """
        Extract the action from the response.
        
        Args:
            response: Response string from the model
            
        Returns:
            True if obnoxious, False otherwise
        """
        response_str = response.strip().upper()
        # Expecting only 'OBNOXIOUS' or 'NOT OBNOXIOUS'
        if response_str == 'OBNOXIOUS':
            return True
        elif response_str == 'NOT OBNOXIOUS':
            return False
        else:
            # fallback, treat unknown as not obnoxious
            return False

    def check_query(self, query):
        """
        Check if the query is obnoxious or not.
        
        Args:
            query: User's query string
            
        Returns:
            True if obnoxious, False otherwise
        """
        # Use OpenAI API to check if query is obnoxious
        response = self.client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {
                    "role": "system",
                    "content": self.prompt
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            max_tokens=10,
            temperature=0
        )
        reply = response.choices[0].message.content
        if reply is None:
            return False
        return self.extract_action(reply)
