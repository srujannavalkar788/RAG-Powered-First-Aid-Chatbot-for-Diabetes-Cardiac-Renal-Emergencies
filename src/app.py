# src/app.py
import streamlit as st
from Data_preprocessing import KnowledgeBase
from retriever import HybridRetriever
from generator import ResponseGenerator
import time
import base64
import os

# Custom CSS for better styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Background image function
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
            background-color: rgba(255, 255, 255, 0.9);
            background-blend-mode: multiply;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def load_knowledge_base():
    """
    Load the CSV knowledge base with error handling
    """
    csv_path = os.path.join('data', 'Assignment Data Base.xlsx')
    
    # Verify file exists
    if not os.path.exists(csv_path):
        st.error(f"Critical Error: Medical database not found at {os.path.abspath(csv_path)}")
        st.stop()
        
    try:
        kb = KnowledgeBase(csv_path)
        kb.create_embeddings()
        return kb
    except Exception as e:
        st.error(f"Failed to load knowledge base: {str(e)}")
        st.stop()

def main():
    kb = load_knowledge_base()
    # Load custom CSS and background
    local_css("src/styles.css")
    add_bg_from_local("assets/medical_bg.png")
    
    # Initialize session state
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
    
    # App header
    st.image("assets/logo.png", width=150)
    st.title("MediAssist First-Aid Chatbot")
    st.markdown("""
    <div class="disclaimer-box">
        ⚠️ <strong>Important Disclaimer:</strong> This information is for educational purposes only and is 
        <strong>not</strong> a substitute for professional medical advice, diagnosis, or treatment.
    </div>
    """, unsafe_allow_html=True)
    
    # Emergency notice
    with st.expander("🚨 In case of emergency"):
        st.warning("""
        If you or someone else is experiencing any of the following, call emergency services immediately:
        - Loss of consciousness
        - Severe difficulty breathing
        - Chest pain or pressure
        - Severe bleeding
        - Signs of stroke (FAST: Face drooping, Arm weakness, Speech difficulty, Time to call)
        """)
    
    # Domain selection
    st.sidebar.title("Navigation")
    selected_domain = st.sidebar.radio(
        "Select medical domain:",
        ("General", "Diabetes", "Cardiac", "Renal"),
        index=0
    )
    
    # Quick access buttons
    st.sidebar.markdown("### Common Emergencies")
    if st.sidebar.button("Hypoglycemia (Low Sugar)"):
        st.session_state.conversation.append(("user", "I'm experiencing hypoglycemia symptoms"))
    if st.sidebar.button("Chest Pain"):
        st.session_state.conversation.append(("user", "I have chest pain radiating to my left arm"))
    if st.sidebar.button("Acute Kidney Injury"):
        st.session_state.conversation.append(("user", "I have symptoms of acute kidney injury"))
    
    # Chat interface
    st.markdown("<h2 style='color: #e63946;'>Describe Your Symptoms</h2>", 
    unsafe_allow_html=True)
    
    # Display conversation history
    for role, message in st.session_state.conversation:
        if role == "user":
            st.markdown(f"""
            <div class="user-message">
                <strong>You:</strong> {message}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bot-message">
                <strong>MediAssist:</strong> {message}
            </div>
            """, unsafe_allow_html=True)
    
    # User input
    query = st.text_area(
        "Enter your symptoms or medical concern:",
        key="input",
        placeholder="e.g., 'I'm feeling dizzy and my blood sugar is 60 mg/dL'",
        height=100
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        submit_btn = st.button("Submit", type="primary")
    with col2:
        clear_btn = st.button("Clear Conversation")
    
    if clear_btn:
        st.session_state.conversation = []
        st.experimental_rerun()
    
    if submit_btn and query:
        st.session_state.conversation.append(("user", query))
        
        with st.spinner("Analyzing your symptoms and retrieving medical guidance..."):
            # Initialize components if not already done
            if 'kb' not in st.session_state:
                st.session_state.kb = KnowledgeBase('data/Assignment Data Base.xlsx')
                st.session_state.kb.create_embeddings()
            
            if 'retriever' not in st.session_state:
                st.session_state.retriever = HybridRetriever(st.session_state.kb)
            
            if 'generator' not in st.session_state:
                st.session_state.generator = ResponseGenerator()
            
            # Process query
            start_time = time.time()
            retrieved_info = st.session_state.retriever.hybrid_search(query)
            response = st.session_state.generator.generate_response(query, retrieved_info)
            latency = time.time() - start_time
            
            # Add to conversation
            st.session_state.conversation.append(("bot", response))
            
            # Rerun to show updated conversation
            st.rerun()

if __name__ == "__main__":
    main()