"""
Multi-Agent Chatbot System
Contains all agent classes for the Part 3 chatbot implementation.
"""

from .obnoxious_agent import Obnoxious_Agent
from .relevant_documents_agent import Relevant_Documents_Agent
from .query_agent import Query_Agent
from .answering_agent import Answering_Agent
from .head_agent import Head_Agent

__all__ = [
    'Obnoxious_Agent',
    'Relevant_Documents_Agent',
    'Query_Agent',
    'Answering_Agent',
    'Head_Agent',
]
