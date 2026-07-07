import streamlit as st
import os
from PIL import Image
import tempfile
import time
from vector_store import index_and_retrieve_context
from kriti_engine import extract_document_info, audit_claim, run_short_audit_firehose

# Minimalist Premium UI
st.set_page_config(page_title="KritiAI - Prototype", layout="wide", initial_sidebar_state="collapsed")

# Handle Login from URL params
if st.query_params.get("login") == "true":
    st.session_state.authenticated = True
    st.query_params.clear()
    st.rerun()

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

current_page = st.query_params.get("page", "dashboard")

# CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap');
    
    .stApp {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom Top Navigation */
    .harvey-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 40px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: -60px;
        margin-bottom: 60px;
    }
    .harvey-logo {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 400;
        letter-spacing: -0.5px;
    }
    .harvey-logo a {
        text-decoration: none;
        color: inherit;
    }
    .harvey-nav-links {
        display: flex;
        gap: 30px;
        font-size: 0.9rem;
        color: #a0a0a0;
    }
    .harvey-nav-links a {
        text-decoration: none;
        color: inherit;
        transition: color 0.2s;
    }
    .harvey-nav-links a:hover {
        color: #ffffff;
    }
    .btn-login {
        border: 1px solid white;
        background: transparent;
        color: white;
        padding: 8px 20px;
        border-radius: 4px;
        font-size: 0.9rem;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
    }
    .btn-login:hover {
        background: rgba(255, 255, 255, 0.1);
    }
    .auth-text {
        font-size: 0.9rem;
        color: #a0a0a0;
    }

    /* Rotating Hero Section */
    .hero-container {
        position: relative;
        height: 250px;
        width: 100%;
        display: flex;
        justify-content: center;
    }
    
    .hero-slide {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        text-align: center;
        opacity: 0;
        animation: fadeRotate 15s infinite;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-size: cover;
        background-position: center;
        box-shadow: inset 0 0 0 2000px rgba(0, 0, 0, 0.65);
    }
    
    .hero-slide:nth-child(1) { animation-delay: 0s; background-image: url('https://images.unsplash.com/photo-1592982537447-6f23f81e3a24?auto=format&fit=crop&q=80&w=2000'); }
    .hero-slide:nth-child(2) { animation-delay: 5s; background-image: url('https://images.unsplash.com/photo-1586771107445-d3af9e1edec2?auto=format&fit=crop&q=80&w=2000'); }
    .hero-slide:nth-child(3) { animation-delay: 10s; background-image: url('https://images.unsplash.com/photo-1560493676-04071c5f467b?auto=format&fit=crop&q=80&w=2000'); }

    @keyframes fadeRotate {
        0%, 25% { opacity: 1; transform: translateY(0px); }
        33%, 92% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0px); }
    }

    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 4.5rem;
        line-height: 1.1;
        font-weight: 400;
        margin-bottom: 20px;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #a0a0a0;
        max-width: 700px;
        margin: 0 auto;
        font-weight: 300;
        line-height: 1.5;
    }

    /* Override Streamlit Elements */
    h1, h2, h3 { font-family: 'Playfair Display', serif; font-weight: 400; text-align: center; }
    
    .stButton { display: flex; justify-content: center; }
    .stButton>button {
        background-color: white !important;
        color: black !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 10px 30px !important;
        font-weight: 500 !important;
        transition: all 0.3s;
    }
    .stButton>button:hover { background-color: #e0e0e0 !important; }
    
    div[data-testid="stFileUploaderDropzone"] {
        min-height: 300px;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px dashed rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        transition: all 0.3s;
    }
    div[data-testid="stFileUploaderDropzone"]:hover {
        background-color: rgba(255, 255, 255, 0.08);
        border: 1px dashed rgba(255, 255, 255, 0.6);
    }
    
    .status-verifiable { color: #48bb78; font-weight: 500; font-size: 1.2rem;}
    .status-discrepancy { color: #f56565; font-weight: 500; font-size: 1.2rem;}
    hr { border-color: rgba(255, 255, 255, 0.1); }
</style>
""", unsafe_allow_html=True)

# ----------------- LOGIN PAGE -----------------
if not st.session_state.authenticated:
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
    _, login_col, _ = st.columns([1, 1, 1])
    with login_col:
        st.markdown("<h1 style='text-align: center; font-size: 3.5rem;'>KritiAI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #a0a0a0;'>Regional Governance Intelligence Engine</p>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🌐 Sign in with Google", use_container_width=True):
            st.session_state.authenticated = True
            st.rerun()
    st.stop()

# ----------------- MAIN NAVBAR -----------------
st.markdown("""
<div class="harvey-nav">
    <div class="harvey-logo"><a href="/?page=dashboard" target="_self">KritiAI</a></div>
    <div class="harvey-nav-links">
        <a href="/?page=search" target="_self">Semantic Search</a>
        <a href="/?page=learn" target="_self">Learn More</a>
        <a href="/?page=onboarding" target="_self">Onboarding</a>
    </div>
    <div class="harvey-nav-buttons">
        <span class="auth-text">Auditor Account</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- ROUTING -----------------
st.markdown("<div style='padding: 0 40px;'>", unsafe_allow_html=True)

if current_page == "dashboard":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-slide">
            <div class="hero-title">Intelligent Agricultural Auditing</div>
            <div class="hero-subtitle">Empowering regional governance with multimodal AI and spatial intelligence to seamlessly automate claim verification and fraud detection.</div>
        </div>
        <div class="hero-slide">
            <div class="hero-title">Aligning Ground Truth</div>
            <div class="hero-subtitle">Cross-referencing physical satellite constraints with bureaucratic records to instantly and mathematically verify disaster claims.</div>
        </div>
        <div class="hero-slide">
            <div class="hero-title">Fraud Detection at Scale</div>
            <div class="hero-subtitle">Transforming messy, handwritten documentation into verifiable spatial intelligence for state-wide agricultural infrastructure.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        st.markdown("### Add a Document")
        st.markdown("<p style='text-align: center; color:#a0a0a0;'>Upload a PMFBY claim for spatial verification.</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Upload PMFBY Form", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Document Scan", use_column_width=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("Run Spatial Audit", key="audit_btn"):
                lat = 26.2500
                lon = 91.2500
                
                with st.spinner("Extracting..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tf:
                        image.save(tf.name)
                        temp_path = tf.name
                    doc_text = extract_document_info(temp_path)
                
                with st.spinner("Querying Earth Engine & Vector Store..."):
                    vector_context = index_and_retrieve_context(lat, lon, "2025-07-15")
                    
                with st.spinner("Running Short Audit (X/News Firehose)..."):
                    firehose_context = run_short_audit_firehose("2025-07-15", "Kamrup")
                    
                with st.spinner("Aligning modalities..."):
                    result = audit_claim(doc_text, vector_context, firehose_context)
                    
                st.markdown("---")
                st.markdown("#### Audit Results")
                
                decision = result.get('audit_decision', 'ERROR')
                if decision == 'VERIFIABLE':
                    st.markdown(f"Status: <span class='status-verifiable'>{decision}</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"Status: <span class='status-discrepancy'>{decision}</span>", unsafe_allow_html=True)
                    
                st.write(f"**Confidence:** {result.get('confidence_score', 0.0) * 100:.1f}%")
                
                with st.expander("Reasoning Trace"):
                    st.info(result.get('reasoning', 'No reasoning output.'))
                with st.expander("Vector Context"):
                    st.text(vector_context)
                with st.expander("Firehose Short Audit (X/News)"):
                    st.text(firehose_context)
                    
                if os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except Exception:
                        pass

elif current_page == "onboarding":
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        st.markdown("## Want to add the power intelligence to your massive workflow? Take the first step.")
        st.markdown("<p style='text-align: center; color:#a0a0a0;'>First stage is, add documents.</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        uploaded_files = st.file_uploader("Upload historical claims and records", accept_multiple_files=True, label_visibility="collapsed")
        
        if uploaded_files:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate parsing percentage
            for i in range(100):
                time.sleep(0.04) # 4 seconds total
                progress_bar.progress(i + 1)
                status_text.text(f"Parsing percentage: {i+1}%. This process may take days on massive enterprise datalakes...")
                
            st.success("Documents successfully parsed!")
            st.markdown("The system is now weaving together a story from the document timeline, and preparing a unified knowledge graph.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Next Step", key="next_step"):
                st.info("Coming soon.")

elif current_page == "search" or current_page == "learn":
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        st.markdown("<br><br><h3 style='color:#a0a0a0;'>Coming Soon</h3>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

