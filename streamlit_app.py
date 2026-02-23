"""
Streamlit App for Multi-Agent Chatbot (Part 3)
Provides an interactive web interface for the multi-agent chatbot system.
"""

import streamlit as st
from agents.head_agent import Head_Agent


def initialize_head_agent():
    """Initialize the Head_Agent with API keys from secrets."""
    try:
        # Get API keys from Streamlit secrets
        openai_key = st.secrets.get("OPENAI_API_KEY")
        pinecone_key = st.secrets.get("PINECONE_API_KEY")
        index_name = st.secrets.get("PINECONE_INDEX_NAME", "mp2-part3-index")
        
        if not openai_key or not pinecone_key:
            st.error("⚠️ API keys not found. Please configure them in `.streamlit/secrets.toml`")
            return None
        
        # Initialize Head_Agent
        head_agent = Head_Agent(openai_key, pinecone_key, index_name)
        head_agent.setup_sub_agents()
        
        return head_agent
    except Exception as e:
        st.error(f"❌ Error initializing Head_Agent: {str(e)}")
        return None


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Multi-Agent Chatbot",
        page_icon="🤖",
        layout="wide"
    )
    
    # Initialize session state
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    if "head_agent" not in st.session_state:
        st.session_state.head_agent = None
    
    if "initialized" not in st.session_state:
        st.session_state.initialized = False
    
    if "current_agent" not in st.session_state:
        st.session_state.current_agent = None
    
    # Sidebar
    with st.sidebar:
        st.title("🤖 Multi-Agent Chatbot")
        st.markdown("---")
        
        # Initialize button
        if not st.session_state.initialized:
            if st.button("🚀 Initialize Chatbot", type="primary", use_container_width=True):
                with st.spinner("Initializing agents..."):
                    st.session_state.head_agent = initialize_head_agent()
                    if st.session_state.head_agent:
                        st.session_state.initialized = True
                        st.success("✅ Chatbot initialized successfully!")
                        st.rerun()
        else:
            st.success("✅ Chatbot Ready")
            if st.button("🔄 Reinitialize", use_container_width=True):
                st.session_state.head_agent = None
                st.session_state.initialized = False
                st.session_state.conversation_history = []
                st.rerun()
        
        st.markdown("---")
        
        # Current agent display
        if st.session_state.current_agent:
            st.markdown("### Current Agent")
            agent_colors = {
                "Obnoxious_Agent": "🔴",
                "Relevant_Documents_Agent": "🟡",
                "Chat_Agent": "🟢"
            }
            agent_icon = agent_colors.get(st.session_state.current_agent, "⚪")
            st.markdown(f"{agent_icon} **{st.session_state.current_agent}**")
        
        st.markdown("---")
        
        # Clear conversation button
        if st.session_state.conversation_history:
            if st.button("🗑️ Clear Conversation", use_container_width=True):
                st.session_state.conversation_history = []
                st.session_state.current_agent = None
                st.rerun()
        
        # Info section
        st.markdown("### ℹ️ About")
        st.markdown("""
        This chatbot uses multiple specialized agents:
        - **Obnoxious Agent**: Filters inappropriate content
        - **Relevant Documents Agent**: Checks document relevance
        - **Query Agent**: Retrieves documents from Pinecone
        - **Chat Agent**: Generates responses
        """)
    
    # Main content area
    st.title("💬 Multi-Agent Chatbot")
    st.markdown("Ask questions about machine learning and AI topics!")
    
    # Check if initialized
    if not st.session_state.initialized:
        st.info("👈 Please initialize the chatbot using the button in the sidebar.")
        return
    
    # Display conversation history
    for message in st.session_state.conversation_history:
        role = message["role"]
        content = message["content"]
        
        with st.chat_message(role):
            st.markdown(content)
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Add user message to conversation history
        st.session_state.conversation_history.append({"role": "user", "content": prompt})
        
        # Process query
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    bot_response, agent_path = st.session_state.head_agent.process_query(
                        prompt,
                        st.session_state.conversation_history[:-1]  # Exclude the current user message
                    )
                    
                    st.markdown(bot_response)
                    
                    # Update current agent
                    st.session_state.current_agent = agent_path
                    
                    # Add assistant response to conversation history
                    st.session_state.conversation_history.append({
                        "role": "assistant",
                        "content": bot_response
                    })
                    
                except Exception as e:
                    error_msg = f"❌ Error processing query: {str(e)}"
                    st.error(error_msg)
                    st.session_state.conversation_history.append({
                        "role": "assistant",
                        "content": error_msg
                    })


if __name__ == "__main__":
    main()
