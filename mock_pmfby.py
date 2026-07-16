import streamlit as st
import pydeck as pdk
import pandas as pd
from architecture_matrix import render_5x5_architecture_matrix

def render_pmfby_inundate_page():
    """
    Renders Mock UI 1: PMFBY-Inundate (Paddy Loss Verification Tool)
    Solves: Validating farmer-reported flood claims without waiting for physical Crop Cutting Experiments (CCEs).
    """
    st.markdown("""
    <div class="glass-wrapper" style="margin-bottom: 24px;">
        <div class="glass-card" style="border-left: 4px solid #4dabf7; background: linear-gradient(135deg, rgba(77, 171, 247, 0.15) 0%, rgba(15, 17, 26, 0.96) 100%);">
            <div style="font-size: 1.5rem; font-weight: 700; color: #ffffff;">PMFBY-Inundate: Automated Paddy Flood Claim Verification</div>
            <div style="color: #adb5bd; font-size: 0.98rem; margin-top: 6px;">Validating farmer-reported flood submergence claims across Assam & Eastern India without waiting for delayed physical Crop Cutting Experiments (CCEs).</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ----------------- TOP BAR: CLAIM SEARCH & FILTER -----------------
    st.markdown("### Step 1: Filter & Search Incoming Disaster Claims")
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([1.5, 1.5, 1.5, 1.2])
    with filter_col1:
        selected_dist = st.selectbox("Select District / Flood Basin:", ["Kamrup District (Pagladiya Basin)", "Dhubri District (Brahmaputra Basin)", "Barpeta District (Manas Basin)", "Cachar District (Barak Basin)"])
    with filter_col2:
        selected_crop = st.selectbox("Insured Crop Type:", ["Winter Paddy / Sali Rice (Kharif)", "Boro Rice (Early Summer)", "Jute (Flood-Prone Alluvial)", "Mustard / Oilseeds"])
    with filter_col3:
        claimed_date = st.selectbox("Disaster / Submergence Event Date:", ["2026-06-25 (Monsoon Flash Flood)", "2026-06-18 (Heavy Basin Inundation)", "2026-07-02 (Breached Embankment)"])
    with filter_col4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Query Claims Database", use_container_width=True, type="primary"):
            st.toast("Retrieved 142 verified claims matching basin criteria.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ----------------- DUAL-MAP VIEW: PRE vs POST DISASTER -----------------
    st.markdown("### Step 2: Dual-Map Satellite & Radar Submergence Verification")
    st.markdown("<p style='color: #a0a0a0; font-size: 0.92rem; margin-bottom: 16px;'>Left: Pre-disaster baseline HLS optical cube showing active vegetation. Right: Cloud-penetrating Sentinel-1 SAR microwave radar isolating exact floodwater boundaries overlaid on the cadastral parcel.</p>", unsafe_allow_html=True)

    map_col1, map_col2 = st.columns(2)
    center_lat, center_lon = 26.2450, 91.6820

    with map_col1:
        st.markdown('<div class="gis-panel-header" style="border-left: 3px solid #63e6be;">Pre-Disaster Baseline (Optical HLS - 15 Days Pre-Flood)</div>', unsafe_allow_html=True)
        
        # Healthy parcel polygon
        parcel_coords = [
            [center_lon, center_lat],
            [center_lon + 0.0032, center_lat + 0.0004],
            [center_lon + 0.0036, center_lat + 0.0028],
            [center_lon + 0.0006, center_lat + 0.0031],
            [center_lon, center_lat]
        ]
        
        pre_layer = pdk.Layer(
            "PolygonLayer",
            data=[{"polygon": parcel_coords, "name": "Survey No: KH-408/A (Pre-Flood)", "ndwi": "-0.34 (Dry Soil / Healthy Paddy)", "ndvi": "0.78 (Peak Vegetative Vigor)"}],
            get_polygon="polygon",
            get_fill_color=[32, 201, 151, 180],
            get_line_color=[255, 255, 255, 255],
            get_line_width=4,
            pickable=True
        )
        
        view_state = pdk.ViewState(latitude=center_lat + 0.0015, longitude=center_lon + 0.0018, zoom=15.2, pitch=38)
        st.pydeck_chart(pdk.Deck(
            layers=[pre_layer],
            initial_view_state=view_state,
            tooltip={"text": "{name}\nNDWI: {ndwi}\nNDVI: {ndvi}"}
        ))

    with map_col2:
        st.markdown('<div class="gis-panel-header" style="border-left: 3px solid #4dabf7;">Post-Disaster Sentinel-1 SAR (Microwave Radar Flood Mask)</div>', unsafe_allow_html=True)
        
        # Flooded water polygon inside the parcel
        flood_coords = [
            [center_lon + 0.0004, center_lat + 0.0003],
            [center_lon + 0.0030, center_lat + 0.0005],
            [center_lon + 0.0034, center_lat + 0.0024],
            [center_lon + 0.0008, center_lat + 0.0026],
            [center_lon + 0.0004, center_lat + 0.0003]
        ]
        
        post_parcel_layer = pdk.Layer(
            "PolygonLayer",
            data=[{"polygon": parcel_coords, "name": "Survey No: KH-408/A (Cadastral Boundary)"}],
            get_polygon="polygon",
            get_fill_color=[100, 110, 130, 40],
            get_line_color=[255, 255, 255, 255],
            get_line_width=3,
            pickable=True
        )
        
        post_flood_layer = pdk.Layer(
            "PolygonLayer",
            data=[{"polygon": flood_coords, "name": "SAR Inundation Mask (Krishi-DSS Flood Module)", "submerged_pct": "78.4% Submerged", "ndwi": "+0.68 (Deep Floodwater)"}],
            get_polygon="polygon",
            get_fill_color=[77, 171, 247, 210],
            get_line_color=[130, 210, 255, 255],
            get_line_width=4,
            pickable=True
        )
        
        st.pydeck_chart(pdk.Deck(
            layers=[post_parcel_layer, post_flood_layer],
            initial_view_state=view_state,
            tooltip={"text": "{name}\nStatus: {submerged_pct}\nNDWI: {ndwi}"}
        ))

    st.markdown("<br>", unsafe_allow_html=True)

    # ----------------- METADATA PANEL & RECOVERY CURVE -----------------
    st.markdown("### Step 3: Multimodal Claim Validation & Statutory Indemnity Calculation")
    meta_col1, meta_col2 = st.columns([1.3, 1.7])

    with meta_col1:
        st.markdown("""
        <div class="glass-card" style="background: rgba(18, 20, 30, 0.94); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 12px; padding: 18px;">
            <div style="font-size: 1.2rem; font-weight: 700; color: #ffffff; border-bottom: 1px solid rgba(255,255,255,0.15); padding-bottom: 10px; margin-bottom: 12px;">Claim ID: PMFBY-ASM-2026-8841</div>
            <div style="font-size: 0.95rem; color: #adb5bd; margin-bottom: 6px;">Farmer Name: <b style="color: #ffffff;">Hemanta Sarma</b> | Policy: <b style="color: #ffffff;">PADDY-KHARIF-26</b></div>
            <div style="font-size: 0.95rem; color: #adb5bd; margin-bottom: 6px;">Survey No: <b style="color: #ffffff;">KH-408/A</b> | Village: <b style="color: #ffffff;">Rangia Alluvial Block</b></div>
            <div style="font-size: 0.95rem; color: #adb5bd; margin-bottom: 14px;">Total Insured Area: <b style="color: #ffffff;">3.20 Hectares</b> | Sum Insured: <b style="color: #ffffff;">INR 1,20,000</b></div>
            
            <div style="background: rgba(77, 171, 247, 0.12); border: 1px solid rgba(77, 171, 247, 0.3); border-radius: 8px; padding: 12px; margin-bottom: 12px;">
                <div style="font-size: 0.85rem; color: #8daeff; font-weight: 600; text-transform: uppercase;">SAR Inundation Submergence Area</div>
                <div style="font-size: 1.75rem; font-weight: 700; color: #4dabf7;">78.4% Submerged</div>
                <div style="font-size: 0.82rem; color: #cccccc;">2.51 Hectares underwater across 5-vertex cadastral bounds.</div>
            </div>
            
            <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 8px; padding: 12px; margin-bottom: 12px;">
                <div style="font-size: 0.85rem; color: #adb5bd; font-weight: 600; text-transform: uppercase;">Waterlogging Duration (AWS Rainfall Crawler)</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #ffd43b;">11 Continuous Days</div>
                <div style="font-size: 0.82rem; color: #cccccc;">Verified via local Automatic Weather Station precipitation logs (`Node 12`).</div>
            </div>

            <div style="background: rgba(81, 207, 102, 0.1); border-left: 3px solid #51cf66; padding: 10px; border-radius: 6px; font-size: 0.88rem; color: #d3f9d8;">
                <b>Gemini 2.5 Flash VLM Parser (`Node 16 & 17`):</b> Physical handwritten claim form ingested. Extracted loss cause matches microwave SAR telemetry with <b>99.4% confidence</b>.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with meta_col2:
        st.markdown("""
        <div class="glass-card" style="background: rgba(18, 20, 30, 0.94); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 12px; padding: 18px; margin-bottom: 16px;">
            <div style="font-size: 1.15rem; font-weight: 700; color: #ffffff; margin-bottom: 12px;">Statutory Indemnity Payout Calculator (`Node 23`)</div>
            <div style="font-size: 0.9rem; color: #adb5bd; margin-bottom: 10px;">Applying the official Government of India Pradhan Mantri Fasal Bima Yojana formula:</div>
            <div style="background: rgba(0,0,0,0.4); padding: 10px 14px; border-radius: 6px; font-family: monospace; font-size: 1.05rem; color: #8daeff; margin-bottom: 12px;">
                Indemnity = [(Threshold Yield - Actual Computed Yield) / Threshold Yield] × Sum Insured
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 12px;">
                <div style="background: rgba(255,255,255,0.04); padding: 10px; border-radius: 6px;">
                    <div style="font-size: 0.78rem; color: #adb5bd;">Threshold Yield</div>
                    <div style="font-size: 1.15rem; font-weight: 700; color: #ffffff;">3,400 kg/Ha</div>
                </div>
                <div style="background: rgba(255,255,255,0.04); padding: 10px; border-radius: 6px;">
                    <div style="font-size: 0.78rem; color: #adb5bd;">SAR Actual Yield</div>
                    <div style="font-size: 1.15rem; font-weight: 700; color: #ff8787;">741 kg/Ha</div>
                </div>
                <div style="background: rgba(255,255,255,0.04); padding: 10px; border-radius: 6px;">
                    <div style="font-size: 0.78rem; color: #adb5bd;">Computed Loss Ratio</div>
                    <div style="font-size: 1.15rem; font-weight: 700; color: #ffd43b;">78.20% Loss</div>
                </div>
            </div>
            <div style="background: rgba(77, 171, 247, 0.18); border: 1px solid #4dabf7; border-radius: 8px; padding: 14px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 0.88rem; color: #adb5bd; text-transform: uppercase; font-weight: 600;">Verified Indemnity Payout</div>
                    <div style="font-size: 0.82rem; color: #cccccc;">Ready for instant Direct Benefit Transfer (DBT) disbursement</div>
                </div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #ffffff;">INR 93,840</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="font-size: 0.95rem; font-weight: 600; color: #ffffff; margin-bottom: 8px;">Multi-Temporal NDVI / NDWI Recovery Curve (`Node 5`)</div>', unsafe_allow_html=True)
        # Chart data
        chart_data = pd.DataFrame({
            "Timeline": ["May 15 (Sowing)", "June 01 (Growth)", "June 15 (Pre-Flood)", "June 25 (Peak Flood)", "July 05 (Receding)", "July 15 (Recovery)"],
            "NDVI (Vegetation Vigor)": [0.25, 0.52, 0.78, 0.12, 0.18, 0.31],
            "NDWI (Water Index)": [-0.42, -0.38, -0.34, 0.68, 0.41, 0.08]
        }).set_index("Timeline")
        st.line_chart(chart_data, color=["#51cf66", "#4dabf7"])

    st.markdown("<br>", unsafe_allow_html=True)

    # ----------------- ACTION BUTTONS -----------------
    st.markdown("### Step 4: Execute Administrative Action")
    act_col1, act_col2 = st.columns(2)
    with act_col1:
        if st.button("Approve Loss Payout (INR 93,840 DBT via PMFBY Gateway)", key="btn_app_pmfby", use_container_width=True, type="primary"):
            st.success("Indemnity Payout INR 93,840 approved and transmitted to the Public Financial Management System (PFMS) for direct account deposit.")
    with act_col2:
        if st.button("Escalate for Physical Crop Cutting Experiment (CCE) Blending", key="btn_esc_cce", use_container_width=True):
            st.info("Claim escalated to District Statistical Officer for manual CCE ground-truth blending.")

    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 35px 0;'>", unsafe_allow_html=True)
    st.markdown("### Architecture Matrix Illumination for PMFBY-Inundate Workflow")
    render_5x5_architecture_matrix("PMFBY", compact=True)
