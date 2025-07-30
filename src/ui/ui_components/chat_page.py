"""
Chat page component for AI assistant functionality.
"""

import streamlit as st
import time

def show_chat_page(video_data):
    """Display the professional AI chat interface."""
    st.markdown("""
    <div class="page-header">
        <h2>💬 AI Study Assistant</h2>
        <p class="page-subtitle">Ask questions about the video content and get instant answers</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize chat if needed
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Set video context for AI
    if not st.session_state.get('video_context'):
        _set_video_context(video_data)
    
    # Professional quick actions
    st.markdown("""
    <div class="section-header">
        <h3>🚀 Quick Actions</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Summarize key points", use_container_width=True):
            add_quick_question("Can you summarize the key points from this video?")
    
    with col2:
        if st.button("❓ Explain concepts", use_container_width=True):
            add_quick_question("Can you explain the main concepts covered in this video?")
    
    with col3:
        if st.button("🎯 Create quiz questions", use_container_width=True):
            add_quick_question("Can you create some quiz questions based on this video content?")
    
    st.markdown("---")
    
    # Professional chat interface
    st.markdown("""
    <div class="section-header">
        <h3>💬 Chat History</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat container with professional styling
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_history:
            _show_welcome_message()
        else:
            _display_chat_history()
    
    # Professional chat input
    st.markdown("### ✏️ Ask a Question")
    user_input = st.chat_input("Type your question about the video content...")
    
    if user_input:
        handle_chat_message(user_input)


def _set_video_context(video_data):
    """Set the video context for AI responses."""
    context = {
        'title': video_data.get('title', 'Unknown Video'),
        'summary': video_data.get('summary', ''),
        'concepts': video_data.get('concepts', []),
        'notes': video_data.get('notes', ''),
        'clips_count': len(video_data.get('clips', [])),
        'duration': video_data.get('duration', 0)
    }
    st.session_state.video_context = context


def _show_welcome_message():
    """Display welcome message for first-time chat users."""
    st.markdown("""
    <div class="welcome-message">
        <div class="welcome-icon">🤖</div>
        <div class="welcome-text">
            <h4>Welcome to your AI Study Assistant!</h4>
            <p>I'm here to help you understand the video content better. You can ask me questions about:</p>
            <ul style="text-align: left; color: var(--text-secondary); max-width: 500px;">
                <li>Key concepts and explanations</li>
                <li>Detailed summaries of specific topics</li>
                <li>Quiz questions for self-assessment</li>
                <li>Clarification on complex ideas</li>
                <li>Study tips and recommendations</li>
            </ul>
            <p>Try using the quick actions above or type your own question below!</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _display_chat_history():
    """Display the chat history with professional styling."""
    for i, message in enumerate(st.session_state.chat_history):
        role = message.get('role', 'user')
        content = message.get('content', '')
        timestamp = message.get('timestamp', '')
        
        if role == 'user':
            st.markdown(f"""
            <div class="user-message">
                <div class="message-content">{content}</div>
                <div class="message-meta">{timestamp}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="ai-message">
                <div class="message-content">{content}</div>
                <div class="message-meta">AI Assistant • {timestamp}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Add separator between message pairs
        if role == 'assistant' and i < len(st.session_state.chat_history) - 1:
            st.markdown('<div class="chat-separator"></div>', unsafe_allow_html=True)


def add_quick_question(question):
    """Add a quick question to chat."""
    handle_chat_message(question)


def handle_chat_message(user_input):
    """Handle chat message and get AI response."""
    # Add user message to history
    timestamp = time.strftime("%H:%M", time.localtime())
    st.session_state.chat_history.append({
        'role': 'user',
        'content': user_input,
        'timestamp': timestamp
    })
    
    with st.spinner("AI is thinking..."):
        # Get AI response (this would integrate with your AI service)
        ai_response = _get_ai_response(user_input)
        
        # Add AI response to history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': ai_response,
            'timestamp': timestamp
        })
    
    st.rerun()


def _get_ai_response(user_input):
    """Get AI response based on user input and video context."""
    # This is a placeholder - integrate with your actual AI service
    context = st.session_state.get('video_context', {})
    
    # Simple response generation based on context
    if any(keyword in user_input.lower() for keyword in ['summary', 'summarize', 'key points']):
        summary = context.get('summary', 'No summary available.')
        return f"Here's a summary of the video:\n\n{summary}"
    
    elif any(keyword in user_input.lower() for keyword in ['concept', 'explain', 'what is']):
        concepts = context.get('concepts', [])
        if concepts:
            concept_list = '\n'.join([f"• {concept}" for concept in concepts[:5]])
            return f"The main concepts covered in this video include:\n\n{concept_list}"
        else:
            return "I couldn't identify specific concepts from this video. Could you be more specific about what you'd like me to explain?"
    
    elif any(keyword in user_input.lower() for keyword in ['quiz', 'question', 'test']):
        return """Here are some quiz questions based on the video content:

1. What are the main topics discussed in this video?
2. How do the key concepts relate to each other?
3. What practical applications can you think of for this content?
4. What questions do you still have after watching this video?

Feel free to ask me to elaborate on any of these questions!"""
    
    else:
        # Generic helpful response
        title = context.get('title', 'this video')
        clips_count = context.get('clips_count', 0)
        
        return f"""I'm here to help you understand "{title}" better! 

This video has been analyzed and I found {clips_count} key segments. You can ask me about:
• Specific concepts or topics
• Summaries of different sections
• Explanations of complex ideas
• Study questions and quizzes

What would you like to know more about?"""
