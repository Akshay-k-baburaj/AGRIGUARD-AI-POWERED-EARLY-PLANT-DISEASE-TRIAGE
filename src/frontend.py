import streamlit as st

def apply_custom_css():
    """Apply professional, clean CSS styling"""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        /* Global Styles */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        .stApp {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        }
        
        #MainMenu, footer, header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        .block-container {
            padding: 3rem 2rem;
            max-width: 800px;
        }
        
        /* Hero */
        .hero-container {
            text-align: center;
            padding: 3rem 0 2rem;
        }
        
        .app-logo {
            font-size: 4rem;
            margin-bottom: 1.5rem;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        .app-title {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1rem;
        }
        
        .app-description {
            font-size: 1.125rem;
            color: #94a3b8;
            max-width: 600px;
            margin: 0 auto 3rem;
            line-height: 1.7;
        }
        
        /* File Uploader - Clean Style */
        [data-testid="stFileUploader"] {
            background: rgba(30, 41, 59, 0.6) !important;
            backdrop-filter: blur(10px);
            border: 2px dashed #334155 !important;
            border-radius: 1.5rem !important;
            padding: 3rem 2rem !important;
            transition: all 0.3s ease;
        }
        
        [data-testid="stFileUploader"]:hover {
            border-color: #10b981 !important;
            background: rgba(30, 41, 59, 0.8) !important;
        }
        
        [data-testid="stFileUploader"] section {
            border: none !important;
            padding: 0 !important;
        }
        
        [data-testid="stFileUploader"] label {
            font-size: 1.125rem !important;
            color: #e2e8f0 !important;
            font-weight: 600 !important;
            text-align: center !important;
        }
        
        [data-testid="stFileUploader"] button {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
            color: white !important;
            border: none !important;
            padding: 0.875rem 2rem !important;
            border-radius: 0.75rem !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.2s !important;
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4) !important;
        }
        
        [data-testid="stFileUploader"] button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.6) !important;
        }
        
        [data-testid="stFileUploader"] small {
            color: #94a3b8 !important;
            font-size: 0.875rem !important;
        }
        
        /* Image Display */
        [data-testid="stImage"] {
            border-radius: 1.25rem;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            margin: 2rem 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Analyze Button */
        .stButton button {
            width: 100%;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            border: none;
            padding: 1.125rem 2rem;
            border-radius: 1rem;
            font-weight: 700;
            font-size: 1.125rem;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 1.5rem 0;
            box-shadow: 0 8px 24px rgba(16, 185, 129, 0.4);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .stButton button:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 36px rgba(16, 185, 129, 0.6);
        }
        
        /* Badge */
        .verify-badge {
            display: inline-block;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: #10b981;
            padding: 0.625rem 1.25rem;
            border-radius: 2rem;
            font-size: 0.875rem;
            font-weight: 600;
            margin: 1.5rem 0;
        }
        
        /* Results Section */
        .results-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid rgba(16, 185, 129, 0.2);
        }
        
        .results-icon {
            font-size: 2.5rem;
        }
        
        .results-title {
            font-size: 2rem;
            font-weight: 700;
            color: #e2e8f0;
        }
        
        /* Result Cards */
        .result-card {
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 1rem;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .result-label {
            font-size: 0.875rem;
            color: #94a3b8;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }
        
        .result-value {
            font-size: 1.75rem;
            color: #10b981;
            font-weight: 700;
        }
        
        /* Progress Bar */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #10b981 0%, #34d399 100%);
        }
        
        /* Info Box */
        [data-testid="stAlert"] {
            background: rgba(16, 185, 129, 0.1) !important;
            border: 1px solid rgba(16, 185, 129, 0.3) !important;
            border-left: 4px solid #10b981 !important;
            border-radius: 0.75rem !important;
            color: #d1fae5 !important;
        }
        
        /* Spinner */
        .stSpinner > div {
            border-top-color: #10b981 !important;
        }
        
        /* Error Alert */
        .element-container:has([data-baseweb="notification"]) [data-baseweb="notification"] {
            background: rgba(239, 68, 68, 0.1) !important;
            border: 1px solid rgba(239, 68, 68, 0.3) !important;
            border-radius: 1rem !important;
            color: #fca5a5 !important;
        }
        
        /* Divider */
        hr {
            border: none;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            margin: 2rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

def render_hero():
    """Render hero section"""
    st.markdown("""
        <div class="hero-container">
            <div class="app-logo">🌿</div>
            <h1 class="app-title">AgriGuard AI</h1>
            <p class="app-description">
                Advanced plant disease detection powered by deep learning. 
                Upload a leaf image to get instant diagnosis and treatment recommendations.
            </p>
        </div>
    """, unsafe_allow_html=True)

def render_file_uploader():
    """Render file upload section - cleaner without extra wrapper"""
    uploaded_file = st.file_uploader(
        "📸 Drop your plant image here or click to browse",
        type=["jpg", "jpeg", "png"],
        help="Supported formats: JPG, JPEG, PNG • Max size: 200MB"
    )
    return uploaded_file

def render_integrity_badge(file_hash):
    """Render integrity badge"""
    st.markdown(
        f'<div class="verify-badge">✓ Verified • Hash: {file_hash[:16]}</div>',
        unsafe_allow_html=True
    )

def render_results(predicted_class_name, confidence_score, advice):
    """Render results with styled cards"""
    # Results header with custom HTML
    st.markdown("""
        <div class="results-header">
            <div class="results-icon">🎯</div>
            <div class="results-title">Analysis Results</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Detection result card
    st.markdown(f"""
        <div class="result-card">
            <div class="result-label">Detected Condition</div>
            <div class="result-value">{predicted_class_name.replace('_', ' ').title()}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Confidence card
    st.markdown(f"""
        <div class="result-card">
            <div class="result-label">Confidence Level</div>
            <div class="result-value">{confidence_score:.1%}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    st.progress(confidence_score)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recommendation with icon
    st.markdown("### 💊 Treatment Recommendation")
    st.info(advice)

def render_trust_section():
    """Render footer"""
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #64748b; padding: 2rem 0;'>"
        "Powered by AI • Trusted by farmers worldwide 🌍"
        "</p>",
        unsafe_allow_html=True
    )