# Multi-Agent Chatbot - Streamlit App

This is a Streamlit web application for the Multi-Agent Chatbot system from Mini Project Part 3. The chatbot uses multiple specialized agents to handle user queries, filter inappropriate content, and retrieve relevant documents.

## Features

- **Interactive Chat Interface**: Modern web-based chat interface
- **Multi-Agent System**: 
  - Obnoxious Agent: Filters inappropriate content
  - Relevant Documents Agent: Checks if retrieved documents are relevant
  - Query Agent: Retrieves documents from Pinecone vector store
  - Chat Agent: Generates responses using retrieved documents
- **Real-time Agent Path Display**: See which agent is handling each query
- **Conversation History**: Maintains context across multiple turns
- **Error Handling**: Graceful error messages and recovery

## Installation

1. **Clone or navigate to the project directory**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys**:
   
   Create or edit `.streamlit/secrets.toml` file:
   ```toml
   OPENAI_API_KEY = "your-openai-api-key-here"
   PINECONE_API_KEY = "your-pinecone-api-key-here"
   PINECONE_INDEX_NAME = "mp2-part3-index"
   ```
   
   **Important**: Replace the placeholder values with your actual API keys.

## Usage

1. **Start the Streamlit app**:
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Initialize the chatbot**:
   - Click the "🚀 Initialize Chatbot" button in the sidebar
   - Wait for the initialization to complete

3. **Start chatting**:
   - Type your message in the chat input at the bottom
   - The chatbot will process your query and respond
   - The sidebar shows which agent is currently handling your query

4. **Clear conversation**:
   - Click "🗑️ Clear Conversation" in the sidebar to start a new conversation

## Project Structure

```
mini_pj_2/
├── streamlit_app.py          # Main Streamlit application
├── agents/                   # Agent classes
│   ├── __init__.py
│   ├── obnoxious_agent.py
│   ├── relevant_documents_agent.py
│   ├── query_agent.py
│   ├── answering_agent.py
│   └── head_agent.py
├── .streamlit/
│   └── secrets.toml          # API keys configuration (not in git)
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Agent System Architecture

The chatbot uses a hierarchical agent system:

1. **Head Agent**: Controller that manages all sub-agents
2. **Obnoxious Agent**: First line of defense - filters inappropriate queries
3. **Query Agent**: Retrieves relevant documents from Pinecone
4. **Relevant Documents Agent**: Validates if retrieved documents are relevant
5. **Answering Agent**: Generates final response using relevant documents

### Query Flow

```
User Query
    ↓
Obnoxious Agent Check
    ↓ (if not obnoxious)
Query Agent (Retrieve Documents)
    ↓
Relevant Documents Agent (Validate)
    ↓ (if relevant)
Answering Agent (Generate Response)
    ↓
Response to User
```

## Configuration

### API Keys

The application requires:
- **OpenAI API Key**: For GPT-4.1-nano model and embeddings
- **Pinecone API Key**: For vector store access
- **Pinecone Index Name**: Name of your Pinecone index (default: "mp2-part3-index")

### Model Settings

- All agents use `gpt-4.1-nano` model
- Embedding model: `text-embedding-3-small` (512 dimensions)
- Max tokens for responses: 250
- Temperature: 0.2 (for Answering Agent)

## Troubleshooting

### "API keys not found" Error

- Make sure `.streamlit/secrets.toml` exists
- Verify that all three keys are set in the secrets file
- Restart the Streamlit app after updating secrets

### "Error initializing Head_Agent"

- Check that your API keys are valid
- Verify that your Pinecone index exists and is accessible
- Check your internet connection

### Chatbot not responding

- Check the sidebar for error messages
- Try reinitializing the chatbot
- Clear the conversation and try again

## Notes

- The chatbot is designed to answer questions about machine learning and AI topics
- Queries outside the knowledge base will be refused
- Inappropriate queries will be filtered by the Obnoxious Agent
- Conversation history is maintained during the session but not persisted

## License

This project is part of a mini project assignment.
