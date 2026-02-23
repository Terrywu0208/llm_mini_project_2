"""
Head Agent - Controller agent that manages all sub-agents.
"""

from openai import OpenAI
from pinecone import Pinecone
from .obnoxious_agent import Obnoxious_Agent
from .relevant_documents_agent import Relevant_Documents_Agent
from .query_agent import Query_Agent
from .answering_agent import Answering_Agent


class Head_Agent:
    def __init__(self, openai_key, pinecone_key, pinecone_index_name) -> None:
        """
        Initialize the Head_Agent.
        
        Args:
            openai_key: OpenAI API key
            pinecone_key: Pinecone API key
            pinecone_index_name: Name of the Pinecone index
        """
        self.openai_key = openai_key
        self.pinecone_key = pinecone_key
        self.pinecone_index_name = pinecone_index_name
        # Placeholders for sub-agents; to be set up in setup_sub_agents()
        self.obnoxious_agent = None
        self.relevant_documents_agent = None
        self.retriever_agent = None
        self.chat_agent = None

    def setup_sub_agents(self):
        """Setup all sub-agents."""
        client = OpenAI(api_key=self.openai_key)
        pinecone_index = Pinecone(api_key=self.pinecone_key).Index(self.pinecone_index_name)
        
        self.obnoxious_agent = Obnoxious_Agent(client)
        self.relevant_documents_agent = Relevant_Documents_Agent(client)
        self.retriever_agent = Query_Agent(pinecone_index, client, "text-embedding-3-small", embedding_dimensions=512)
        self.chat_agent = Answering_Agent(client)

    def process_query(self, user_input, conversation_history=None):
        """
        Process a user query and return response with agent path.
        
        Args:
            user_input: User's query string
            conversation_history: Optional conversation history as list of dicts with 'role' and 'content'
            
        Returns:
            Tuple of (bot_response, agent_path)
        """
        # Make sure all subagents are set up
        if (self.obnoxious_agent is None or 
            self.relevant_documents_agent is None or 
            self.retriever_agent is None or 
            self.chat_agent is None):
            self.setup_sub_agents()

        if conversation_history is None:
            conversation_history = []

        # Step 1: Check for obnoxious input
        if self.obnoxious_agent.check_query(user_input):
            bot_response = "I can't respond to that."
            agent_path = "Obnoxious_Agent"
        # Step 2 & 3: Retrieve, check relevance, then answer or refuse
        else:
            top_docs = self.retriever_agent.query_vector_store(user_input)
            meta = lambda d: d.get("metadata") or {}
            docs = [{"content": meta(d).get("text", meta(d).get("content", ""))} for d in top_docs]
            context_text = "Context documents (retrieved for the user's question):\n\n" + "\n".join(d["content"] for d in docs)
            conv_relevance = [
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": context_text}
            ]
            if not top_docs or self.relevant_documents_agent.get_relevance(conv_relevance) != "Relevant":
                bot_response = "This question is outside the scope I can help with."
                agent_path = "Relevant_Documents_Agent"
            else:
                bot_response = self.chat_agent.generate_response(user_input, docs, conversation_history)
                agent_path = "Chat_Agent"
        
        return bot_response, agent_path

    def main_loop(self):
        """Run the main loop for the chatbot (command-line interface)."""
        print("Welcome to the Multi-Agent Chatbot! Type 'exit' or 'quit' to stop.\n")

        # Make sure all subagents are set up
        if (self.obnoxious_agent is None or 
            self.relevant_documents_agent is None or 
            self.retriever_agent is None or 
            self.chat_agent is None):
            self.setup_sub_agents()

        conversation = []
        while True:
            user_input = input("User: ")
            if user_input.strip().lower() in ['exit', 'quit']:
                print("Exiting chatbot. Goodbye!")
                break

            bot_response, agent_path = self.process_query(user_input, conversation)
            
            # Record turn
            print(f"Your question: {user_input}")
            print(f"[{agent_path}]")
            print(f"Bot: {bot_response}\n")
            conversation.append({"role": "user", "content": user_input})
            conversation.append({"role": "assistant", "content": bot_response})
