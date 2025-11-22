def apply_greptile_style():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif !important;
    }

    .stApp {
        background: linear-gradient(135deg, #0A0F1E 0%, #0F1624 100%);
    }

    .main > div {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    h1 {
        font-size: 2.5rem !important;
        margin-bottom: 1rem !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #B4B8BE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    h2 {
        font-size: 1.75rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }

    h3 {
        font-size: 1.25rem !important;
        color: #00D9A3 !important;
    }

    p, label, .stMarkdown {
        color: #B4B8BE !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }

    .stButton > button {
        background: #00D9A3 !important;
        color: #0A0F1E !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(0, 217, 163, 0.2) !important;
    }

    .stButton > button:hover {
        background: #00F5B8 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 217, 163, 0.3) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    div[data-testid="stFileUploader"] {
        background-color: #131B2E !important;
        border: 2px dashed #2A3B52 !important;
        border-radius: 12px !important;
        padding: 2rem !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="stFileUploader"]:hover {
        border-color: #00D9A3 !important;
        background-color: #1A2537 !important;
    }

    .uploadedFile {
        background-color: #1A2537 !important;
        border: 1px solid #2A3B52 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }

    .stAlert {
        background-color: #131B2E !important;
        border-left: 4px solid #00D9A3 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        color: #E8EAED !important;
    }

    div[data-testid="stSuccess"] {
        background-color: rgba(0, 217, 163, 0.1) !important;
        border-left-color: #00D9A3 !important;
    }

    div[data-testid="stWarning"] {
        background-color: rgba(255, 193, 7, 0.1) !important;
        border-left-color: #FFC107 !important;
    }

    div[data-testid="stError"] {
        background-color: rgba(255, 82, 82, 0.1) !important;
        border-left-color: #FF5252 !important;
    }

    div[data-testid="stInfo"] {
        background-color: rgba(33, 150, 243, 0.1) !important;
        border-left-color: #2196F3 !important;
    }

    .stProgress > div > div > div {
        background-color: #00D9A3 !important;
    }

    .stSpinner > div {
        border-top-color: #00D9A3 !important;
    }

    div.stImage {
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4) !important;
        transition: transform 0.3s ease !important;
    }

    div.stImage:hover {
        transform: scale(1.02) !important;
    }

    .stSelectbox > div > div {
        background-color: #131B2E !important;
        border: 1px solid #2A3B52 !important;
        border-radius: 8px !important;
        color: #E8EAED !important;
    }

    .stTextInput > div > div > input {
        background-color: #131B2E !important;
        border: 1px solid #2A3B52 !important;
        border-radius: 8px !important;
        color: #E8EAED !important;
        padding: 0.75rem !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #00D9A3 !important;
        box-shadow: 0 0 0 2px rgba(0, 217, 163, 0.2) !important;
    }

    div[data-testid="stExpander"] {
        background-color: #131B2E !important;
        border: 1px solid #2A3B52 !important;
        border-radius: 12px !important;
        margin-bottom: 1rem !important;
    }

    div[data-testid="stExpander"]:hover {
        border-color: #00D9A3 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: transparent !important;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #131B2E !important;
        border: 1px solid #2A3B52 !important;
        border-radius: 8px !important;
        color: #B4B8BE !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #00D9A3 !important;
        border-color: #00D9A3 !important;
        color: #0A0F1E !important;
    }

    .element-container {
        margin-bottom: 1rem !important;
    }

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F1624 0%, #131B2E 100%) !important;
        border-right: 1px solid #2A3B52 !important;
    }

    div[data-testid="stSidebar"] h1,
    div[data-testid="stSidebar"] h2,
    div[data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }

    .metric-card {
        background: linear-gradient(135deg, #131B2E 0%, #1A2537 100%);
        border: 1px solid #2A3B52;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        border-color: #00D9A3;
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 217, 163, 0.15);
    }

    code {
        background-color: #1A2537 !important;
        color: #00D9A3 !important;
        padding: 0.2rem 0.4rem !important;
        border-radius: 4px !important;
        font-family: 'Courier New', monospace !important;
    }

    pre {
        background-color: #131B2E !important;
        border: 1px solid #2A3B52 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }

    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent 0%, #2A3B52 50%, transparent 100%) !important;
        margin: 2rem 0 !important;
    }

    .stDataFrame {
        border: 1px solid #2A3B52 !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }

    div[data-testid="stMetricValue"] {
        color: #00D9A3 !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #B4B8BE !important;
        font-size: 0.875rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    .stRadio > div {
        background-color: #131B2E !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }

    .stCheckbox {
        color: #E8EAED !important;
    }

    div[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    .stSlider > div > div > div {
        background-color: #2A3B52 !important;
    }

    .stSlider > div > div > div > div {
        background-color: #00D9A3 !important;
    }

    footer {
        visibility: hidden !important;
    }

    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px !important;
    }
    </style>
    """
