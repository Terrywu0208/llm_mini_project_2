"""
Answering Agent - Generates responses to user queries using retrieved documents.
"""

from openai import OpenAI


class Answering_Agent:
    def __init__(self, openai_client) -> None:
        """
        Initialize the Answering_Agent.
        
        Args:
            openai_client: OpenAI client instance
        """
        self.openai_client = openai_client

    def generate_response(self, query, docs, conv_history, k=5):
        """
        Generate a response to the user's query.
        
        Args:
            query: User's query string
            docs: List of retrieved documents with 'content' key
            conv_history: Conversation history as list of dicts with 'role' and 'content'
            k: Maximum number of documents to use
            
        Returns:
            Generated response string
        """
        if not docs:
            # If no documents but there's conversation history, emphasize using history
            if conv_history:
                system_prompt = "You are a helpful assistant. Answer the user's question based on the previous conversation history. Use the context from earlier in the conversation to provide a helpful response."
            else:
                system_prompt = "You are a helpful assistant. Answer the user's question to the best of your ability, even though you don't have specific documents to reference."
            doc_snippets = ""
        else:
            system_prompt = "You are a helpful assistant. Answer the user's question using the following context documents and your previous conversation history."
            # Join the retrieved documents up to top k
            doc_snippets = "\n".join(
                [f"Document {i+1}:\n{doc['content']}" for i, doc in enumerate(docs[:k])]
            )

        # Compose prompt for LLM
        prompt = f"""{system_prompt}

=== Context Documents ===
{doc_snippets}
=== Conversation History ===
"""
        if conv_history:
            for msg in conv_history:
                prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"
        prompt += f"User: {query}\nAssistant:"

        # Call OpenAI completion API to generate response
        # Assumes self.openai_client is an OpenAI client with a .chat.completions.create or similar method
        try:
            completion = self.openai_client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *[
                        {"role": msg['role'], "content": msg['content']}
                        for msg in conv_history
                    ],
                    {"role": "user", "content": f"{query}\n\nContext:\n{doc_snippets}"}
                ],
                max_tokens=250,
                temperature=0.2,
            )
            # Depending on API client, this may need adjusting
            response = completion.choices[0].message.content.strip()
            return response
        except Exception as e:
            # If OpenAI fails, fallback to a simple concatenation
            return f"Sorry, I could not process your request because of a system error. ({e})"
