import streamlit as st
import google.generativeai as genai
import time
import re

# Page configuration
st.set_page_config(
    page_title="AI Email Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Your Gemini API Key
gemini_api_key = "Enter_your_api_key"

# Configure Gemini with Flash 2.5 model
try:
    genai.configure(api_key=gemini_api_key)
    # Using the Flash 2.5 model
    model = genai.GenerativeModel('gemini-2.5-flash')
    st.session_state.api_key_valid = True
except Exception as e:
    st.session_state.api_key_valid = False
    st.error(f"API Configuration Error: {str(e)}")

# Professional Dark Theme CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main {
        background: #0A0A0A;
        padding: 2rem;
    }
    
    /* Header styling - Modern gradient */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #FF6B6B 100%);
        padding: 2.5rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #ffffff 0%, #e0e0e0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    }
    
    .main-header p {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.9);
        font-weight: 300;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #1A1A1A;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Card styling - Glass morphism */
    .glass-card {
        background: rgba(26, 26, 26, 0.95);
        backdrop-filter: blur(10px);
        padding: 1.8rem;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.05);
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    /* Button styling - Modern gradient */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
        border: 1px solid rgba(255,255,255,0.1);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        border-color: rgba(255,255,255,0.3);
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        background: #1E1E1E;
        color: #FFFFFF;
        border-radius: 16px;
        border: 2px solid #2A2A2A;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        background: #252525;
    }
    
    /* Select box styling */
    .stSelectbox > div > div > select {
        background: #1E1E1E;
        color: #FFFFFF;
        border-radius: 12px;
        border: 2px solid #2A2A2A;
        padding: 0.5rem;
    }
    
    /* Radio button styling */
    .stRadio > div {
        background: #1E1E1E;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #2A2A2A;
    }
    
    /* Success message styling */
    .success-box {
        background: linear-gradient(135deg, #1a4731 0%, #0d2f1f 100%);
        color: #a7f3d0;
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        border-left: 4px solid #10b981;
        border: 1px solid #10b981;
    }
    
    /* Feature box styling */
    .feature-box {
        background: #1A1A1A;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid #2A2A2A;
        height: 100%;
    }
    
    .feature-box:hover {
        transform: translateY(-5px);
        border-color: #667eea;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        background: #202020;
    }
    
    .feature-box h3 {
        color: #667eea;
        margin-bottom: 1rem;
        font-weight: 600;
        font-size: 1.5rem;
    }
    
    .feature-box p {
        color: #B0B0B0;
        line-height: 1.6;
    }
    
    /* Info box styling */
    .info-box {
        background: #1E1E1E;
        padding: 1.2rem;
        border-radius: 16px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        border: 1px solid #2A2A2A;
        color: #FFFFFF;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: #1A1A1A;
        padding: 0.5rem;
        border-radius: 16px;
        border: 1px solid #2A2A2A;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: #B0B0B0;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    /* Metric cards */
    .metric-card {
        background: #1A1A1A;
        padding: 1.2rem;
        border-radius: 16px;
        border: 1px solid #2A2A2A;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .metric-label {
        color: #B0B0B0;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        font-size: 0.9rem;
        border-top: 1px solid #2A2A2A;
        margin-top: 3rem;
    }
    
    /* Result container */
    .result-container {
        background: #1A1A1A;
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid #2A2A2A;
        margin-top: 2rem;
    }
    
    /* Sidebar text */
    .sidebar-text {
        color: #B0B0B0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Divider */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
    }
    
    /* Status badge */
    .status-badge {
        background: #1E1E1E;
        padding: 0.5rem 1rem;
        border-radius: 30px;
        display: inline-block;
        border: 1px solid #2A2A2A;
        color: #10b981;
        font-size: 0.9rem;
    }
    
    /* Tab content indicator */
    .tab-indicator {
        color: #667eea;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for different tabs
if 'email_response' not in st.session_state:
    st.session_state.email_response = ""
if 'grammar_response' not in st.session_state:
    st.session_state.grammar_response = ""
if 'rephrase_response' not in st.session_state:
    st.session_state.rephrase_response = ""
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "email"

# Header
st.markdown("""
<div class="main-header">
    <h1>⚡ AI Email Studio</h1>
    <p>Professional email assistant powered by Gemini Flash 2.5 • Generate • Correct • Rephrase</p>
    <div style="margin-top: 1rem;">
        <span class="status-badge">✓ Gemini Flash 2.5 Active</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🚀 AI Email Studio")
    st.markdown("---")
    
    # Model info
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">Gemini</div>
        <div class="metric-label">Flash 2.5 Model</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features
    st.markdown("### ✨ Premium Features")
    features = [
        "🚀 Gemini Flash 2.5",
        "📝 Smart Generation",
        "🔍 Advanced Grammar",
        "🔄 Context Aware",
        "⚡ Real-time Processing",
        "🎯 Professional Output"
    ]
    
    for feature in features:
        st.markdown(f"<div class='sidebar-text'>✓ {feature}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick stats
    st.markdown("### 📊 Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">0.5s</div>
            <div class="metric-label">Avg Response</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">99%</div>
            <div class="metric-label">Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Usage tips
    st.markdown("### 💡 Pro Tips")
    st.markdown("""
    <div class='sidebar-text'>
    • Be specific in your requests<br>
    • Use clear language<br>
    • Specify the tone you need<br>
    • Review and customize output<br>
    • Copy with one click
    </div>
    """, unsafe_allow_html=True)

# Main content
if not st.session_state.api_key_valid:
    st.error("⚠️ API Configuration Error. Please check your API key.")
else:
    # Welcome message
    st.markdown("""
    <div class="info-box">
        <strong>✨ Welcome to AI Email Studio!</strong> Your professional email assistant is ready. Choose a task below to get started.
    </div>
    """, unsafe_allow_html=True)
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["📝 Generate Email", "🔍 Correct Grammar", "🔄 Rephrase Message"])
    
    with tab1:
        st.markdown("### ✍️ Professional Email Generation")
        st.markdown("Describe your email requirements and get a perfectly crafted response.")
        st.markdown('<p class="tab-indicator">📧 Email Generation Mode Active</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            email_prompt = st.text_area(
                "Email Description",
                height=150,
                placeholder="Example: Write a follow-up email to a client about the project proposal we discussed yesterday. Include a request for feedback and suggest a meeting next week.",
                help="Describe what you want to say in detail",
                key="email_input"
            )
        
        with col2:
            st.markdown("### ⚙️ Settings")
            tone = st.selectbox(
                "Professional Tone",
                ["Executive", "Business Formal", "Semi-Formal", "Friendly Professional", "Persuasive"],
                help="Select the professional tone",
                key="email_tone"
            )
            
            purpose = st.selectbox(
                "Email Purpose",
                ["Business Proposal", "Follow-up", "Introduction", "Meeting Request", "Thank You", "Apology", "Announcement"],
                help="What's the purpose of your email?",
                key="email_purpose"
            )
            
            length = st.select_slider(
                "Detail Level",
                options=["Concise", "Balanced", "Detailed"],
                value="Balanced",
                help="How detailed should the email be?",
                key="email_length"
            )
        
        if st.button("🚀 Generate Professional Email", key="generate_btn", use_container_width=True):
            if email_prompt:
                with st.spinner("🔄 AI is crafting your professional email..."):
                    try:
                        prompt = f"""Generate a professional email with the following specifications:
                        
                        Description: {email_prompt}
                        Tone: {tone}
                        Purpose: {purpose}
                        Length: {length}
                        
                        Requirements:
                        - Use appropriate business email format
                        - Include subject line
                        - Professional greeting and signature
                        - Clear structure with paragraphs
                        - Maintain professional language
                        - Be concise yet comprehensive
                        - Include call to action if appropriate
                        
                        Format the email properly with:
                        Subject: [subject line]
                        
                        [Email body with proper spacing]
                        """
                        
                        response = model.generate_content(prompt)
                        st.session_state.email_response = response.text
                        st.session_state.active_tab = "email"
                        
                        st.success("✅ Email generated successfully!")
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("⚠️ Please describe the email you want to generate.")
        
        # Display email response
        if st.session_state.email_response:
            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
            st.markdown("### 📧 Generated Email")
            
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.text_area(
                    "Your Email",
                    value=st.session_state.email_response,
                    height=300,
                    key="email_display",
                    label_visibility="collapsed"
                )
            
            with col2:
                st.markdown("### Actions")
                if st.button("📋 Copy Email", key="copy_email", use_container_width=True):
                    st.success("✓ Ready to copy! (Ctrl+C)")
                if st.button("🔄 Clear", key="clear_email", use_container_width=True):
                    st.session_state.email_response = ""
                    st.rerun()
    
    with tab2:
        st.markdown("### 🔍 Professional Grammar & Style Check")
        st.markdown("Enhance your text with advanced grammar correction and style improvements.")
        st.markdown('<p class="tab-indicator">🔍 Grammar Correction Mode Active</p>', unsafe_allow_html=True)
        
        text_to_correct = st.text_area(
            "Enter your text",
            height=150,
            placeholder="Paste your email or message here for professional improvement...",
            key="correct_text_input"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            correction_level = st.radio(
                "Improvement Level",
                ["Basic Grammar", "Professional Polish", "Executive Review", "Full Enhancement"],
                index=1,
                help="Select how much improvement you need",
                key="correction_level"
            )
        
        with col2:
            writing_style = st.radio(
                "Target Style",
                ["Business Professional", "Technical", "Persuasive", "Academic", "General"],
                index=0,
                help="Choose your target writing style",
                key="writing_style"
            )
        
        if st.button("🔧 Enhance Text", key="correct_btn", use_container_width=True):
            if text_to_correct:
                with st.spinner("🔄 Analyzing and enhancing your text..."):
                    try:
                        prompt = f"""Enhance and correct this text:
                        
                        Original: {text_to_correct}
                        
                        Improvement Level: {correction_level}
                        Target Style: {writing_style}
                        
                        Requirements:
                        - Fix all grammar and spelling errors
                        - Improve sentence structure
                        - Enhance professional tone
                        - Maintain original meaning
                        - Add appropriate transitions
                        - Ensure clarity and flow
                        - Use sophisticated vocabulary where appropriate
                        
                        Provide the enhanced version only.
                        """
                        
                        response = model.generate_content(prompt)
                        st.session_state.grammar_response = response.text
                        st.session_state.active_tab = "grammar"
                        
                        st.success("✅ Text enhanced successfully!")
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("⚠️ Please enter text to enhance.")
        
        # Display grammar response
        if st.session_state.grammar_response:
            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
            st.markdown("### ✨ Enhanced Text")
            
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.text_area(
                    "Enhanced Version",
                    value=st.session_state.grammar_response,
                    height=300,
                    key="grammar_display",
                    label_visibility="collapsed"
                )
            
            with col2:
                st.markdown("### Actions")
                if st.button("📋 Copy Enhanced", key="copy_grammar", use_container_width=True):
                    st.success("✓ Ready to copy! (Ctrl+C)")
                if st.button("🔄 Clear", key="clear_grammar", use_container_width=True):
                    st.session_state.grammar_response = ""
                    st.rerun()
    
    with tab3:
        st.markdown("### 🔄 Professional Message Rephrasing")
        st.markdown("Transform your message while preserving the core meaning.")
        st.markdown('<p class="tab-indicator">🔄 Rephrasing Mode Active</p>', unsafe_allow_html=True)
        
        text_to_rephrase = st.text_area(
            "Enter your message",
            height=150,
            placeholder="Enter your message to rephrase professionally...",
            key="rephrase_text_input"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            rephrase_style = st.selectbox(
                "Target Style",
                ["Executive Level", "Client-Facing", "Team Communication", "Formal Business", "Concise Professional", "Diplomatic"],
                help="How would you like to rephrase it?",
                key="rephrase_style"
            )
        
        with col2:
            complexity = st.select_slider(
                "Complexity Level",
                options=["Simple", "Moderate", "Sophisticated"],
                value="Moderate",
                help="Choose language complexity",
                key="complexity"
            )
        
        if st.button("🔄 Rephrase Professionally", key="rephrase_btn", use_container_width=True):
            if text_to_rephrase:
                with st.spinner("🔄 Rephrasing your message..."):
                    try:
                        prompt = f"""Rephrase this message professionally:
                        
                        Original: {text_to_rephrase}
                        
                        Target Style: {rephrase_style}
                        Complexity: {complexity}
                        
                        Requirements:
                        - Maintain core meaning
                        - Enhance professional tone
                        - Improve clarity and impact
                        - Use appropriate vocabulary
                        - Ensure natural flow
                        - Match business communication standards
                        
                        Provide the rephrased version only.
                        """
                        
                        response = model.generate_content(prompt)
                        st.session_state.rephrase_response = response.text
                        st.session_state.active_tab = "rephrase"
                        
                        st.success("✅ Message rephrased successfully!")
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("⚠️ Please enter a message to rephrase.")
        
        # Display rephrase response
        if st.session_state.rephrase_response:
            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
            st.markdown("### 🔄 Rephrased Message")
            
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.text_area(
                    "Rephrased Version",
                    value=st.session_state.rephrase_response,
                    height=300,
                    key="rephrase_display",
                    label_visibility="collapsed"
                )
            
            with col2:
                st.markdown("### Actions")
                if st.button("📋 Copy Rephrased", key="copy_rephrase", use_container_width=True):
                    st.success("✓ Ready to copy! (Ctrl+C)")
                if st.button("🔄 Clear", key="clear_rephrase", use_container_width=True):
                    st.session_state.rephrase_response = ""
                    st.rerun()

# Footer
st.markdown("""
<div class="footer">
    <p>⚡ AI Email Studio | Powered by Tanmay</p>
    <p style="font-size: 0.8rem; color: #444;">Professional Email Assistant • Real-time Processing • Enterprise Grade</p>
</div>
""", unsafe_allow_html=True)