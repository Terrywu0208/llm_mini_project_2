"""
Query Agent - Retrieves relevant documents from Pinecone vector store.
"""

import re
from openai import OpenAI
from pinecone import Pinecone


class Query_Agent:
    def __init__(self, pinecone_index, openai_client, embeddings, embedding_dimensions=None) -> None:
        """
        Initialize the Query_Agent.
        
        Args:
            pinecone_index: Pinecone index instance
            openai_client: OpenAI client instance
            embeddings: Embedding model name (e.g., "text-embedding-3-small")
            embedding_dimensions: Optional embedding dimensions
        """
        self.pinecone_index = pinecone_index
        self.client = openai_client
        self.embeddings = embeddings
        self.embedding_dimensions = embedding_dimensions  # 與 Pinecone index 維度一致，例如 512
        self.prompt = None
        

    def query_vector_store(self, query, k=5):
        """
        Query the Pinecone vector store.
        
        Args:
            query: User's query string
            k: Number of top results to return
            
        Returns:
            List of document results with id, score, and metadata
        """
        # If query is empty, just return empty result
        if not query or not self.embeddings:
            return []

        # Generate embedding for the query using OpenAI API
        kwargs = {"input": query, "model": self.embeddings}
        if self.embedding_dimensions is not None:
            kwargs["dimensions"] = self.embedding_dimensions
        embedding_response = self.client.embeddings.create(**kwargs)
        query_embedding = embedding_response.data[0].embedding

        # Query Pinecone
        pinecone_response = self.pinecone_index.query(
            vector=query_embedding,
            top_k=k,
            include_metadata=True
        )

        results = []
        for match in pinecone_response.matches:
            results.append({
                'id': match.id,
                'score': match.score,
                'metadata': match.metadata
            })

        return results

    def set_prompt(self, prompt):
        """
        Set the prompt for the Query_Agent.
        
        Args:
            prompt: New prompt string
        """
        self.prompt = prompt

    def extract_action(self, response, query = None):
        """
        Extract the action from the response.
        
        Args:
            response: Response to parse
            query: Optional query string
            
        Returns:
            Extracted action string or None
        """
        if not response:
            return None

        # Try to extract action based on expected response format
        # If response is a dict or has 'action' key
        if isinstance(response, dict):
            action = response.get('action', None)
            if action:
                return action

        # If response is a string, try to parse action inline, e.g. "Action: Search"
        action = None
        # Common pattern: "Action: <something>"
        match = re.search(r'Action\s*:\s*([^\n]+)', str(response), re.IGNORECASE)
        if match:
            action = match.group(1).strip()
            return action

        # Alternative: try to find commands in brackets: e.g. "[SEARCH]", or lowercased (search)
        match = re.search(r'[\[\(]([a-zA-Z_ ]+)[\]\)]', str(response))
        if match:
            action = match.group(1).strip()
            return action

        # If all else fails, just return the raw response (or None)
        return None
