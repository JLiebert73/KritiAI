import streamlit as st

# Master 5x5 Architecture Matrix Grid Definitions (25 Nodes)
MASTER_GRID_NODES = [
    # Row 1: Earth Observation Foundations (The "Eye")
    {"id": 1, "row": "Row 1: Earth Observation Foundations (The 'Eye')", "name": "Prithvi-EO-2.0 (NASA/IBM)", "desc": "Multimodal Vision Transformer foundational model for temporal satellite cubes."},
    {"id": 2, "row": "Row 1: Earth Observation Foundations (The 'Eye')", "name": "AlphaEarth Temporal Embeddings", "desc": "DeepMind temporal embeddings capturing seasonal crop phenology."},
    {"id": 3, "row": "Row 1: Earth Observation Foundations (The 'Eye')", "name": "6-Band HLS 30m Raster Cubes", "desc": "Harmonized Landsat-Sentinel multi-temporal surface reflectance rasters."},
    {"id": 4, "row": "Row 1: Earth Observation Foundations (The 'Eye')", "name": "Sentinel-1 SAR (Microwave / Radar)", "desc": "Cloud-penetrating synthetic aperture radar required during monsoon flood intervals."},
    {"id": 5, "row": "Row 1: Earth Observation Foundations (The 'Eye')", "name": "Multi-Temporal NDVI / NDWI Curves", "desc": "Continuous vegetation vigor and water indices tracking parcel dynamics."},

    # Row 2: Krishi-DSS DPI Integration (The "Map")
    {"id": 6, "row": "Row 2: Krishi-DSS DPI Integration (The 'Map')", "name": "KrishiMapper API (Scheme 16/17/29)", "desc": "National Digital Public Infrastructure API protocols for farm boundaries."},
    {"id": 7, "row": "Row 2: Krishi-DSS DPI Integration (The 'Map')", "name": "Krishi-DSS Ground Truth & Spectral Library", "desc": "Verified regional spectral profiles and active cultivation training baselines."},
    {"id": 8, "row": "Row 2: Krishi-DSS DPI Integration (The 'Map')", "name": "Krishi-DSS Flood Inundation Module", "desc": "Automated waterlogging and submergence polygon extraction engine."},
    {"id": 9, "row": "Row 2: Krishi-DSS DPI Integration (The 'Map')", "name": "National One Soil Unified Information System", "desc": "Centralized geospatial soil health and parcel classification repository."},
    {"id": 10, "row": "Row 2: Krishi-DSS DPI Integration (The 'Map')", "name": "Digital Cadastral Boundary Vectors", "desc": "Exact 5-vertex and irregular GeoJSON farmland polygon bounds."},

    # Row 3: Weather & Physical Environment (The "Ground")
    {"id": 11, "row": "Row 3: Weather & Physical Environment (The 'Ground')", "name": "WeatherNext 2 Atmospheric Grids", "desc": "High-resolution atmospheric models for localized weather forecasting."},
    {"id": 12, "row": "Row 3: Weather & Physical Environment (The 'Ground')", "name": "AWS Rainfall Crawler", "desc": "Automatic Weather Station real-time daily precipitation tracking."},
    {"id": 13, "row": "Row 3: Weather & Physical Environment (The 'Ground')", "name": "Soil NPK & Organic Carbon Attributes", "desc": "Spatial nitrogen, phosphorus, potassium, and organic carbon deficiency grids."},
    {"id": 14, "row": "Row 3: Weather & Physical Environment (The 'Ground')", "name": "Soil Moisture & Evapotranspiration Index", "desc": "Sub-surface moisture retention and crop water stress metrics."},
    {"id": 15, "row": "Row 3: Weather & Physical Environment (The 'Ground')", "name": "Digital Elevation Model (DEM)", "desc": "High-precision topographic slope and hydrological flow drainage vectors."},

    # Row 4: Document & Multimodal Intelligence (The "Context")
    {"id": 16, "row": "Row 4: Document & Multimodal Intelligence (The 'Context')", "name": "Gemini 2.5 Flash / VLM", "desc": "Visual Language Model for processing handwritten physical claim forms."},
    {"id": 17, "row": "Row 4: Document & Multimodal Intelligence (The 'Context')", "name": "Layout-Aware Document Parser", "desc": "Structured field extraction from heterogeneous municipal application PDFs."},
    {"id": 18, "row": "Row 4: Document & Multimodal Intelligence (The 'Context')", "name": "Qdrant Vector Semantic Search", "desc": "High-speed semantic retrieval over state agricultural regulations and schemes."},
    {"id": 19, "row": "Row 4: Document & Multimodal Intelligence (The 'Context')", "name": "Aadhaar / eKYC Privacy Masking", "desc": "Zero-knowledge encryption and PII sanitization for farmer identity records."},
    {"id": 20, "row": "Row 4: Document & Multimodal Intelligence (The 'Context')", "name": "Local Dialect Voice-to-Text", "desc": "Multilingual speech recognition for rural citizen grievance reporting."},

    # Row 5: Administrative State-Mutation (The "Action")
    {"id": 21, "row": "Row 5: Administrative State-Mutation (The 'Action')", "name": "PM-KISAN Triage Webhook", "desc": "Encrypted JSON payload dispatch locking unverified claim manifests."},
    {"id": 22, "row": "Row 5: Administrative State-Mutation (The 'Action')", "name": "Village Nodal Officer (VNO) Mobile App", "desc": "Field audit assignment routing direct to local agricultural extension officers."},
    {"id": 23, "row": "Row 5: Administrative State-Mutation (The 'Action')", "name": "PMFBY Indemnity Payout Calculator", "desc": "Statutory disaster loss compensation engine using threshold yield formulas."},
    {"id": 24, "row": "Row 5: Administrative State-Mutation (The 'Action')", "name": "e-Urvarak / iFMS Supply Plan Exporter", "desc": "Automated fertilizer allocation schedule formatted for national portals."},
    {"id": 25, "row": "Row 5: Administrative State-Mutation (The 'Action')", "name": "Automated SMS Citizen Notification", "desc": "Instant regional language SMS alerts informing farmers of audit status."}
]

# Workflow Lighting Configurations
WORKFLOW_LIGHTING = {
    "PM-KISAN": {
        "title": "PM-KISAN Cadastral Audit & Triage Pipeline",
        "active_ids": [1, 3, 6, 7, 10, 21, 22, 25],
        "neon_color": "#ff6b6b",
        "desc": "Illuminates Earth Observation foundational vision models, KrishiMapper boundary APIs, and automated VNO field audit dispatch hooks."
    },
    "PMFBY": {
        "title": "PMFBY-Inundate: Paddy Flood Loss Verification Pipeline",
        "active_ids": [2, 4, 8, 12, 16, 17, 23],
        "neon_color": "#4dabf7",
        "desc": "Illuminates AlphaEarth embeddings, cloud-penetrating Sentinel-1 SAR microwave radar, Krishi-DSS flood masks, AWS rainfall crawlers, Gemini VLM document parsers, and the statutory Indemnity calculator."
    },
    "URVARAK": {
        "title": "Urvarak-Sparsity: Fertilizer Micro-Allocation & Supply Planner",
        "active_ids": [1, 3, 9, 13, 24],
        "neon_color": "#51cf66",
        "desc": "Illuminates multi-temporal HLS cubes, Prithvi crop classification, National One Soil NPK deficiency grids, and the iFMS national supply plan exporter."
    },
    "ALL": {
        "title": "Full Cross-Modal Regional Intelligence Engine (25 Nodes)",
        "active_ids": list(range(1, 26)),
        "neon_color": "#845ef7",
        "desc": "All 25 nodes fully illuminated, demonstrating how KritiAI unifies Earth Observation, Digital Public Infrastructure, Atmospheric modeling, Multimodal VLMs, and Administrative action."
    }
}

def render_5x5_architecture_matrix(active_workflow="ALL", compact=False):
    """
    Renders the 5x5 Master Grid using 100% Streamlit native containers and columns.
    Guarantees zero stray HTML tags or markdown parsing bugs.
    """
    config = WORKFLOW_LIGHTING.get(active_workflow, WORKFLOW_LIGHTING["ALL"])
    active_ids = set(config["active_ids"])
    neon_color = config["neon_color"]
    
    # Render clean status header box using native Streamlit container
    with st.container(border=True):
        col_s1, col_s2 = st.columns([3, 1])
        with col_s1:
            st.markdown(f"**Active Illumination Mode:** `{config['title']}`")
            st.caption(config['desc'])
        with col_s2:
            st.metric(label="Illuminated Nodes", value=f"{len(active_ids)} / 25 Nodes")
            
    # Render grid row by row using native columns to eliminate all HTML string leaks
    current_row_label = ""
    nodes_in_current_row = []
    
    for node in MASTER_GRID_NODES:
        if node["row"] != current_row_label:
            if nodes_in_current_row:
                _render_row_nodes(nodes_in_current_row, active_ids, neon_color)
                nodes_in_current_row = []
            current_row_label = node["row"]
            st.markdown(f"<h4 style='color: #8daeff; margin-top: 18px; margin-bottom: 8px; border-left: 3px solid #4c6ef5; padding-left: 10px; font-size: 1.0rem;'>{current_row_label}</h4>", unsafe_allow_html=True)
        nodes_in_current_row.append(node)
        
    if nodes_in_current_row:
        _render_row_nodes(nodes_in_current_row, active_ids, neon_color)

def _render_row_nodes(nodes, active_ids, neon_color):
    cols = st.columns(len(nodes))
    for idx, node in enumerate(nodes):
        with cols[idx]:
            is_active = node["id"] in active_ids
            with st.container(border=True):
                if is_active:
                    st.markdown(f"<span style='color: {neon_color}; font-weight: 700; font-size: 0.78rem;'>NODE #{node['id']:02d} | ACTIVE</span>", unsafe_allow_html=True)
                    st.markdown(f"**{node['name']}**")
                    st.caption(node['desc'])
                else:
                    st.markdown(f"<span style='color: #6c757d; font-weight: 600; font-size: 0.78rem;'>NODE #{node['id']:02d} | STANDBY</span>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color: #888888; font-weight: 500;'>{node['name']}</span>", unsafe_allow_html=True)
                    st.caption(f"<span style='color: #666666;'>{node['desc']}</span>", unsafe_allow_html=True)
