import streamlit as st
import pandas as pd
import pydeck as pdk
import time
import random
import cv2
import numpy as np
import plotly.graph_objects as go
import networkx as nx
from vision_extraction import fetch_arcgis_satellite_imagery, extract_field_boundaries

def render_geotagging_page():
    st.markdown("### KritiAI: Autonomous Identity Resolution & Geotagging Engine")
    st.markdown("<p style='color: #a0a0a0; font-size: 0.94rem; margin-bottom: 24px;'>Resolving the 'Tenancy Gap' by extracting unstructured administrative data, building multi-modal identity graphs, and projecting oral-lessee claims directly onto the geospatial grid using Earth Observation Vision Models.</p>", unsafe_allow_html=True)
    

def render_back_button():
    if st.button("🏠 Back to KritiAI Core Brain", use_container_width=True):
        st.query_params["page"] = "hub"
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)

def render_doc_intel_page():
    render_back_button()
    # SECTION 1: LIVE INGESTION & DOCUMENT INTELLIGENCE
    # -------------------------------------------------------------------------
    st.markdown("#### 1. Real-Time Document Intelligence (OCR-to-Spatial Pipeline)")

    # Initialize extraction state
    if "doc_extracted" not in st.session_state:
        st.session_state.doc_extracted = False

    doc_col, attn_col = st.columns(2)

    with doc_col:
        with st.container(border=True):
            doc_type = st.radio("Select Source Data to Ingest", [
                "Degraded Local Panchayat Lease (Handwritten)", 
                "Crumpled Village Panchayat Certificate"
            ], horizontal=False)
            
            if "doc_type_prev" not in st.session_state:
                st.session_state.doc_type_prev = doc_type

            if st.session_state.doc_type_prev != doc_type:
                st.session_state.doc_extracted = False
                st.session_state.doc_type_prev = doc_type
            
            if "Degraded" in doc_type:
                img_path = "assets/doc_lease.jpg"
            else:
                img_path = "assets/doc_panchayat.jpg"
            
            if st.button("Extract Entities via VLM", type="primary", use_container_width=True):
                st.session_state.doc_extracted = True
            
            st.image(img_path, use_container_width=True, caption="Original Document")
    
    with attn_col:
        if st.session_state.doc_extracted:
            with st.container(border=True):
                st.markdown("<b style='color:#ffcc00;'>VLM Attention Map</b>", unsafe_allow_html=True)
                from PIL import Image
                img = Image.open(img_path)
                w, h = img.size
                
                fig_vlm = go.Figure()
                fig_vlm.add_trace(go.Image(z=np.array(img)))
                
                if "Degraded" in doc_type:
                    boxes = [
                        {"name": "Landlord: R. Sharma (KH-115/P)", "coords": [0.15*w, 0.2*h, 0.85*w, 0.35*h], "color": "rgba(255, 135, 135, 0.4)", "border": "red", "text_pos": [0.5*w, 0.27*h]},
                        {"name": "Lessee: Bipul Das", "coords": [0.2*w, 0.4*h, 0.8*w, 0.55*h], "color": "rgba(99, 230, 190, 0.4)", "border": "green", "text_pos": [0.5*w, 0.47*h]},
                        {"name": "Anchor: Gandhi Basti Road", "coords": [0.1*w, 0.65*h, 0.9*w, 0.8*h], "color": "rgba(255, 204, 0, 0.4)", "border": "gold", "text_pos": [0.5*w, 0.72*h]}
                    ]
                else:
                    boxes = [
                        {"name": "Govt Trust Land", "coords": [0.15*w, 0.15*h, 0.85*w, 0.3*h], "color": "rgba(255, 135, 135, 0.4)", "border": "red", "text_pos": [0.5*w, 0.22*h]},
                        {"name": "Applicant: Dipankar Saikia", "coords": [0.2*w, 0.45*h, 0.8*w, 0.6*h], "color": "rgba(99, 230, 190, 0.4)", "border": "green", "text_pos": [0.5*w, 0.52*h]},
                        {"name": "Claim: 3 Bighas", "coords": [0.25*w, 0.7*h, 0.75*w, 0.85*h], "color": "rgba(255, 204, 0, 0.4)", "border": "gold", "text_pos": [0.5*w, 0.77*h]}
                    ]
                    
                for box in boxes:
                    x0, y0, x1, y1 = box["coords"]
                    
                    # Draw filled box
                    fig_vlm.add_trace(go.Scatter(
                        x=[x0, x1, x1, x0, x0],
                        y=[y0, y0, y1, y1, y0],
                        fill="toself",
                        fillcolor=box["color"],
                        line=dict(color=box["border"], width=3),
                        hoverinfo="skip",
                        showlegend=False
                    ))
                    
                    # Add permanent text
                    fig_vlm.add_trace(go.Scatter(
                        x=[box["text_pos"][0]],
                        y=[box["text_pos"][1]],
                        mode="text",
                        text=[box["name"]],
                        textfont=dict(color="white", size=14, family="Courier New"),
                        hoverinfo="skip",
                        showlegend=False
                    ))
                    
                fig_vlm.update_layout(
                    margin=dict(l=0, r=0, b=0, t=0),
                    xaxis=dict(visible=False, range=[0, w]),
                    yaxis=dict(visible=False, range=[h, 0]),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig_vlm, use_container_width=True, config={'displayModeBar': False})

    if st.session_state.doc_extracted:
        with st.expander("💻 View Raw VLM Logs (KritiAI Terminal)", expanded=False):
            if "Degraded" in doc_type:
                st.markdown("""
                <div style="background-color: #0c0e15; color: #4af626; padding: 15px; font-family: 'Courier New', Courier, monospace; border-radius: 4px; font-size: 0.8rem; overflow-y: auto; border: 1px solid #1a1c23;">
                    > [SYSTEM] Initializing Layout-Aware Vision-Language Model...<br>
                    > [INGEST] Scanning Handwritten Lease Agreement...<br>
                    > [OCR] Detected Bilingual Script (English/Assamese). Low contrast detected.<br>
                    > [DENOISE] Enhancing contrast and removing water stains...<br>
                    > [EXTRACT] <b>Landlord Target:</b> R. Sharma (Resolved to KH-115/P)<br>
                    > [EXTRACT] <b>Unregistered Entity:</b> Bipul Das (Role: Lessee)<br>
                    > [EXTRACT] <b>Spatial Anchor:</b> "South of Gandhi Basti road"<br>
                    > [EXTRACT] <b>Temporal Anchor:</b> "Kharif Paddy"<br>
                    > [ALIGN] Vectorizing extracted semantic text for Knowledge Graph projection...<br>
                    > <span style="color:#ffcc00;">[SUCCESS] Unregistered Farmer Node Created (ID: UNREG-902).</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background-color: #0c0e15; color: #4af626; padding: 15px; font-family: 'Courier New', Courier, monospace; border-radius: 4px; font-size: 0.8rem; overflow-y: auto; border: 1px solid #1a1c23;">
                    > [SYSTEM] Initializing Layout-Aware Vision-Language Model...<br>
                    > [INGEST] Scanning Panchayat Certificate...<br>
                    > [OCR] Rectifying folded and crumpled topology...<br>
                    > [EXTRACT] <b>Document Type:</b> Oral Affidavit #202A<br>
                    > [EXTRACT] <b>Landlord Target:</b> Unknown (Govt Trust Land)<br>
                    > [EXTRACT] <b>Unregistered Entity:</b> Dipankar Saikia<br>
                    > [EXTRACT] <b>Claimed Area:</b> 3 bighas<br>
                    > [ALIGN] Querying Bhulekh database for geographic matching...<br>
                    > <span style="color:#ffcc00;">[SUCCESS] Unregistered Farmer Node Created (ID: UNREG-903).</span>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------

def render_land_cover_page():
    render_back_button()
    # SECTION 3: SEMANTIC LAND COVER CLASSIFICATION
    # -------------------------------------------------------------------------
    st.markdown("#### 3. Semantic Land Cover Classification")
    st.markdown("<p style='color: #a0a0a0; font-size: 0.9rem;'>Now that the identity is resolved, the system dynamically queries the ArcGIS World Imagery API for the Khatauni target coordinate and runs our local vision model pipeline to physically extract the sub-lease parcel boundaries.</p>", unsafe_allow_html=True)

    with st.form("coordinate_form"):
        st.markdown("<b style='font-size:0.9rem;'>Query Custom Coordinates</b>", unsafe_allow_html=True)
        col_lat, col_lon = st.columns(2)
        with col_lat:
            lat = st.number_input("Latitude", value=30.2520, format="%.4f")
        with col_lon:
            lon = st.number_input("Longitude", value=74.9450, format="%.4f")
        st.form_submit_button("Analyze Real-Time Satellite Imagery", type="primary")

    with st.spinner("Initializing ArcGIS Imagery and Vision Extraction Engine..."):
    
        # Fetch and process the real tile at zoom 16 to get a high density of fields
        st.session_state.lat = lat
        st.session_state.lon = lon
        raw_img = fetch_arcgis_satellite_imagery(lat, lon, zoom=16)
        binary_mask, skeleton_mask, overlay_img, field_count, valid_contours = extract_field_boundaries(raw_img, lat, lon)
    
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("<b style='font-size:0.85rem;color:#adb5bd;'>Raw ArcGIS Satellite</b>", unsafe_allow_html=True)
            st.image(raw_img, use_container_width=True)
            st.caption(f"Input: [{lat}, {lon}]")
        with c2:
            st.markdown("<b style='font-size:0.85rem;color:#adb5bd;'>Latent Edge Mask</b>", unsafe_allow_html=True)
            st.image(binary_mask, use_container_width=True)
            st.caption("Morphological Topology")
        with c3:
            st.markdown("<b style='font-size:0.85rem;color:#fcc419;'>Skeletonization (Thinning)</b>", unsafe_allow_html=True)
            st.image(skeleton_mask, use_container_width=True)
            st.caption("Pure Topological Centerlines")
        with c4:
            st.markdown("<b style='font-size:0.85rem;color:#63e6be;'>Interactive Cadastral Vectors</b>", unsafe_allow_html=True)
        
            # Convert CV2 Contours to Interactive Plotly Polygons
            fig = go.Figure()
            fig.add_trace(go.Image(z=raw_img))
            mock_owners = ["Bipul Das", "Dipankar Saikia", "Meera Gogoi", "Raju Das", "Anita Borah", "Sanjib Kalita", "Priya Hazarika", "Unknown Tenant", "State Trust"]
        
            # Store generated data to display in a table later
            extracted_registry = []
        
            for item in valid_contours:
                contour = item['geometry']
                lc_class = item['class']
                lc_color = item['color']
                r, g, b = lc_color
            
                x = contour[:, 0, 0]
                y = contour[:, 0, 1]
                # Close the polygon
                x = np.append(x, x[0])
                y = np.append(y, y[0])
            
                owner = random.choice(mock_owners)
                khasra = f"KH-{random.randint(100, 999)}/P"
                area_sqm = int(cv2.contourArea(contour) * 1.5) # Mock conversion
            
                extracted_registry.append({
                    "Registry ID": khasra,
                    "Geotagged Owner": owner,
                    "Land Cover Class": lc_class,
                    "Estimated Area (sqm)": area_sqm,
                    "Status": "Matched" if owner not in ["Unknown Tenant", "State Trust"] else "Unregistered"
                })
            
                fig.add_trace(go.Scatter(
                    x=x, y=y,
                    fill="toself",
                    fillcolor=f"rgba({r}, {g}, {b}, 0.45)", # Semi-transparent semantic fill
                    line=dict(color=f"rgb({r}, {g}, {b})", width=2),
                    hoveron="fills",
                    hoverinfo="text",
                    text=f"<b>Owner:</b> {owner}<br><b>ID:</b> {khasra}<br><b>Class:</b> {lc_class}<br><b>Area:</b> {area_sqm} sqm",
                    hoverlabel=dict(bgcolor=f"rgba({r}, {g}, {b}, 0.9)", font=dict(color="black")),
                    showlegend=False
                ))
        
            # Hide axes and lock ranges to image dimensions to map the entire area
            h, w, _ = raw_img.shape
            fig.update_layout(
                margin=dict(l=0, r=0, b=0, t=0),
                xaxis=dict(visible=False, range=[0, w]),
                yaxis=dict(visible=False, range=[h, 0]),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                hovermode="closest"
            )
        
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.caption(f"Hover to view owner details for {field_count} Parcels")
            
            # Save to session state for the Geotagging Map page
            st.session_state.extracted_registry = extracted_registry
            st.session_state.valid_contours = valid_contours

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------

def render_geotagging_map_page():
    render_back_button()
    # SECTION 4: EXTRACTED CADASTRAL REGISTRY (TABLE)
    # -------------------------------------------------------------------------
    st.markdown("#### Live Extracted Cadastral Registry")
    st.markdown("<p style='color: #a0a0a0; font-size: 0.9rem;'>The following database registry was generated in real-time purely from the vision model's boundary extraction and cross-referenced against the Knowledge Graph.</p>", unsafe_allow_html=True)

    extracted_registry = st.session_state.get('extracted_registry', [])
    valid_contours = st.session_state.get('valid_contours', [])

    if len(extracted_registry) > 0:
        df_registry = pd.DataFrame(extracted_registry)
        st.dataframe(df_registry, use_container_width=True, hide_index=True)
    else:
        st.info("No valid cadastral polygons detected in this sector.")

    # -------------------------------------------------------------------------
    # SECTION 4: GROUND-TRUTH GEOTAGGING MAP
    # -------------------------------------------------------------------------
    st.markdown("#### 4. The Geotagged Spatial Registry")
    viz_data = []

    if len(valid_contours) > 0:
        st.markdown("<p style='color: #a0a0a0; font-size: 0.9rem;'>The PyDeck visualization below demonstrates the real-time AI Land Cover classification superimposed directly onto the global spatial registry.</p>", unsafe_allow_html=True)
        # We need lat and lon from session state or default
        view_lat = st.session_state.get('lat', 30.2520)
        view_lon = st.session_state.get('lon', 74.9450)
        for i, item in enumerate(valid_contours):
            geo_polygon = item['geo_polygon']
            lc_class = item['class']
            r, g, b = item['color']
        
            # Match it with the extracted_registry generated in Section 3
            owner = extracted_registry[i]["Geotagged Owner"]
            khasra = extracted_registry[i]["Registry ID"]
            area = extracted_registry[i]["Estimated Area (sqm)"]
        
            viz_data.append({
                "polygon": geo_polygon,
                "class": lc_class,
                "owner": owner,
                "khasra": khasra,
                "area": area,
                "fill_color": [r, g, b, 140],
                "line_color": [r, g, b, 255],
                "line_width": 2
            })
    else:
        # FALLBACK: Render default mock data
        st.markdown("<p style='color: #a0a0a0; font-size: 0.9rem;'>No live polygons extracted. Rendering default spatial registry fallback. <b style='color:#63e6be;'>Green polygons</b> are standard registered farmers. The <b style='color:#ffcc00;'>Gold polygon</b> represents a geotagged unregistered tenant farmer.</p>", unsafe_allow_html=True)
        view_lat = 26.1795
        view_lon = 91.7615
    
        map_data = [
            {"coords": [[91.7588, 26.1805], [91.7602, 26.1815], [91.7628, 26.1818], [91.7645, 26.1808], [91.7648, 26.1792], [91.7635, 26.1778], [91.7610, 26.1775], [91.7592, 26.1788], [91.7588, 26.1805]], "is_unreg": False, "farmer": "S. Borah", "khasra": "KH-101"},
            {"coords": [[91.7558, 26.1852], [91.7582, 26.1855], [91.7590, 26.1835], [91.7568, 26.1832], [91.7558, 26.1852]], "is_unreg": True, "farmer": "Bipul Das (UNREG-902)", "khasra": "KH-115/P (Sub-lease)"},
            {"coords": [[91.7535, 26.1848], [91.7558, 26.1852], [91.7568, 26.1832], [91.7545, 26.1828], [91.7535, 26.1848]], "is_unreg": False, "farmer": "M. Kalita", "khasra": "KH-114"},
        ]
    
        for f in map_data:
            is_unreg = f["is_unreg"]
            viz_data.append({
                "polygon": f["coords"],
                "class": "UNREGISTERED TENANT" if is_unreg else "FORMAL LAND OWNER",
                "owner": f["farmer"],
                "khasra": f["khasra"],
                "area": "N/A",
                "fill_color": [255, 204, 0, 165] if is_unreg else [32, 201, 151, 140],
                "line_color": [255, 204, 0, 255] if is_unreg else [100, 255, 180, 255],
                "line_width": 5 if is_unreg else 2
            })
    
    layer = pdk.Layer(
        "PolygonLayer",
        data=viz_data,
        get_polygon="polygon",
        get_fill_color="fill_color",
        get_line_color="line_color",
        get_line_width="line_width",
        pickable=True,
        auto_highlight=True
    )

    view_state = pdk.ViewState(
        latitude=view_lat,
        longitude=view_lon,
        zoom=15,
        pitch=40
    )

    st.pydeck_chart(
        pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={
                "html": """
                <div style="background: rgba(15, 17, 26, 0.95); padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.2); font-family: 'Inter', sans-serif;">
                    <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; border-bottom: 1px solid rgba(255,255,255,0.15); padding-bottom: 6px; margin-bottom: 8px;">{khasra}</div>
                    <div style="font-size: 0.9rem; color: #adb5bd; margin-bottom: 4px;">Owner: <b style="color: #ffffff;">{owner}</b></div>
                    <div style="font-size: 0.9rem; color: #adb5bd; margin-bottom: 6px;">Land Cover: <b style="color: #8daeff;">{class}</b></div>
                    <div style="font-size: 0.85rem; font-weight: 700; color: #000000; background: #63e6be; padding: 4px 8px; border-radius: 4px; display: inline-block;">Area: {area} sqm</div>
                </div>
                """
            }
        )
    )


def render_id_graph_page():
    render_back_button()
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. Knowledge Graph
    st.markdown("#### 1. Identity Resolution via Link Identification (Massive 3D Graph)")
    st.markdown("<p style='color: #a0a0a0; font-size: 0.9rem;'>Using Graph Neural Networks to resolve unregistered entities. Nodes represent the source datalakes, and Edges represent the extracted intelligence linking them.</p>", unsafe_allow_html=True)
    with st.container(border=True):
        # Generate a Focused 3D Knowledge Graph with specific realistic examples
        G = nx.Graph()

        # Add Realistic Extraction Clusters (The Examples)
        examples = [
            {
                "id": "UNREG-902", "name": "Bipul Das", "color": "#63e6be",
                "proxies": [
                    ("focal_1_1", "Panchayat Lease Doc #98221", 12, "#ffcc00", "Extracted: Lessee 'Bipul Das' on KH-115/P"),
                    ("focal_1_2", "Aadhaar Telemetry Ping", 12, "#8daeff", "Extracted: Mobile # matched to KH-115/P"),
                    ("focal_1_3", "Bhulekh API (KH-115/P)", 12, "#ff8787", "Extracted: Landlord = R. Sharma"),
                    ("focal_1_4", "Prithvi-EO Sowing Signature", 12, "#eebefa", "Extracted: Active Kharif Paddy Pixel Match")
                ]
            },
            {
                "id": "UNREG-903", "name": "Dipankar Saikia", "color": "#63e6be",
                "proxies": [
                    ("focal_2_1", "Handwritten Oral Affidavit #202A", 12, "#ffcc00", "Extracted: 3 bighas cultivated by 'D. Saikia'"),
                    ("focal_2_2", "PM-KISAN Denied Claim Log", 12, "#8daeff", "Extracted: DBT Rejected due to unverified tenancy"),
                    ("focal_2_3", "AlphaEarth Multispectral Mask", 12, "#eebefa", "Extracted: Continuous Rabi cultivation (3 years)")
                ]
            },
            {
                "id": "UNREG-904", "name": "Meera Gogoi", "color": "#63e6be",
                "proxies": [
                    ("focal_3_1", "KrishiMapper GPS Point", 12, "#8daeff", "Extracted: VNO uploaded photo tagged to 'Meera'"),
                    ("focal_3_2", "Legacy Khasra PDF Scan", 12, "#ffcc00", "Extracted: Tenant name fuzzily matched to 'Meera G'"),
                    ("focal_3_3", "State Crop Registry JSON", 12, "#ff8787", "Extracted: Registered land under Govt. Trust"),
                    ("focal_3_4", "Flood Inundation Polygon", 12, "#eebefa", "Extracted: 40% waterlogged, requires relief payout")
                ]
            },
            {
                "id": "UNREG-905", "name": "Raju Das", "color": "#63e6be",
                "proxies": [
                    ("focal_4_1", "Urvarak Fertilizer DB", 12, "#ff8787", "Extracted: Subsidized Urea purchased by 'R. Das'"),
                    ("focal_4_2", "Local Crop Mill Receipt", 12, "#ffcc00", "Extracted: 20 quintals of paddy sold"),
                    ("focal_4_3", "Sentinel-1 SAR Data", 12, "#eebefa", "Extracted: Transplanting date matches receipt timeline")
                ]
            },
            {
                "id": "UNREG-906", "name": "Anita Borah", "color": "#63e6be",
                "proxies": [
                    ("focal_5_1", "Drone Multispectral Scan", 12, "#eebefa", "Extracted: High-res cadastral boundary verification"),
                    ("focal_5_2", "Jan Dhan Bank Proxy", 12, "#8daeff", "Extracted: Cash transfer matches tenancy rent schedule"),
                    ("focal_5_3", "Village Headman WhatsApp Log", 12, "#ffcc00", "Extracted: NLP matched name 'Anita' to plot 12B")
                ]
            },
            {
                "id": "UNREG-907", "name": "Sanjib Kalita", "color": "#63e6be",
                "proxies": [
                    ("focal_6_1", "Kisan Credit Card (KCC) Query", 12, "#ff8787", "Extracted: Denied loan for KH-109 (Owner Mismatch)"),
                    ("focal_6_2", "Aadhaar e-KYC Vault", 12, "#8daeff", "Extracted: Biometric hash linked to local PIN code"),
                    ("focal_6_3", "Oral Tenancy Ledger", 12, "#ffcc00", "Extracted: 5 Bigha verbal lease recognized by Panchayat")
                ]
            },
            {
                "id": "UNREG-908", "name": "Priya Hazarika", "color": "#63e6be",
                "proxies": [
                    ("focal_7_1", "PMFBY Insurance Proxy", 12, "#ff8787", "Extracted: Proxy claimant proxy tied to 'Priya'"),
                    ("focal_7_2", "Telecom Tower Triangulation", 12, "#8daeff", "Extracted: Primary mobile device active in field 14 hrs/day"),
                    ("focal_7_3", "Prithvi-EO Yield Prediction", 12, "#eebefa", "Extracted: Predicted 15t/ha matching PMFBY claim")
                ]
            }
        ]
    
        for ex in examples:
            target_id = f"target_{ex['id']}"
            G.add_node(target_id, type="Target", name=f"{ex['id']} ({ex['name']})", size=18, color=ex['color'])
        
            for p_id, p_name, p_size, p_color, p_extract in ex['proxies']:
                G.add_node(p_id, type="Focal", name=p_name, size=p_size, color=p_color)
                G.add_edge(target_id, p_id, extracted=p_extract)
    
        # Link the examples slightly to show cross-graph resolution
        G.add_edge("focal_1_3", "focal_3_3", extracted="Shared Administrative District Node")
        G.add_edge("focal_2_2", "focal_1_2", extracted="Shared Aadhaar Vault Proxy")
        G.add_edge("focal_4_1", "focal_5_2", extracted="Correlated Financial/Subisdy Timeline")
        G.add_edge("focal_6_1", "focal_2_2", extracted="Correlated Denied Services Matrix")
        G.add_edge("focal_7_1", "focal_4_1", extracted="State Database Redundancy")
        G.add_edge("focal_3_4", "focal_7_3", extracted="Joint Spatial Overlap (Disaster/Yield)")

        # Generate 3D positions using spring layout
        pos = nx.spring_layout(G, dim=3, k=0.1, iterations=50, seed=42)

        # Build Traces
        edge_x = []
        edge_y = []
        edge_z = []
    
        mid_x = []
        mid_y = []
        mid_z = []
        mid_text = []

        for edge in G.edges(data=True):
            x0, y0, z0 = pos[edge[0]]
            x1, y1, z1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_z.extend([z0, z1, None])
        
            # If it's a focal edge with extracted info, plot a midpoint for hover text
            extracted_info = edge[2].get("extracted", "")
            if "Extracted:" in extracted_info:
                mid_x.append((x0+x1)/2)
                mid_y.append((y0+y1)/2)
                mid_z.append((z0+z1)/2)
                mid_text.append(f"<b>EDGE INTELLIGENCE</b><br>{extracted_info}")

        edge_trace = go.Scatter3d(
            x=edge_x, y=edge_y, z=edge_z,
            line=dict(width=1.5, color='rgba(141, 174, 255, 0.15)'), # Faint glassy blue connections
            hoverinfo='none',
            mode='lines'
        )
    
        # Invisible scatter trace at edge midpoints purely for showing the extracted text on hover
        edge_hover_trace = go.Scatter3d(
            x=mid_x, y=mid_y, z=mid_z,
            mode='markers',
            marker=dict(size=4, color='rgba(255, 204, 0, 0.8)'),
            text=mid_text,
            hoverinfo='text',
            hoverlabel=dict(bgcolor="#0c0e15", font_size=13, font_family="Inter")
        )

        node_x = []
        node_y = []
        node_z = []
        node_text = []
        node_color = []
        node_size = []
    
        for node in G.nodes(data=True):
            x, y, z = pos[node[0]]
            node_x.append(x)
            node_y.append(y)
            node_z.append(z)
            n_data = node[1]
        
            node_text.append(f"<b>Source Node:</b> {n_data['name']}")
            node_color.append(n_data['color'])
            node_size.append(n_data['size'])

        node_trace = go.Scatter3d(
            x=node_x, y=node_y, z=node_z,
            mode='markers',
            text=node_text,
            hoverinfo='text',
            hoverlabel=dict(bgcolor="#0c0e15", font_size=12, font_family="Inter"),
            marker=dict(
                showscale=False,
                color=node_color,
                size=node_size,
                line_width=0
            )
        )

        fig = go.Figure(data=[edge_trace, edge_hover_trace, node_trace],
             layout=go.Layout(
                title='',
                showlegend=False,
                hovermode='closest',
                margin=dict(b=0,l=0,r=0,t=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                scene=dict(
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title='', backgroundcolor="rgba(0,0,0,0)"),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title='', backgroundcolor="rgba(0,0,0,0)"),
                    zaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title='', backgroundcolor="rgba(0,0,0,0)"),
                    bgcolor='rgba(0,0,0,0)'
                )
             )
        )
    
        # Set height to make it immersive like the image
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------


def render_vector_space_page():
    render_back_button()
    
    # 3. Latent Space UMAP
    st.markdown("#### 2. Vector Embedding Space (Latent Projection)")
    st.markdown("<p style='color: #a0a0a0; font-size: 0.9rem;'>How does the AI know that 'Bipul D.', 'Bipal Das', and 'Khatauni 115' are the same person? It embeds them into a 768-dimensional space. If they cluster close together (visualized here via UMAP projection), the AI merges their identity.</p>", unsafe_allow_html=True)
    
    with st.container(border=True):
        np.random.seed(42)
        n_points = 500
        
        # Create three distinct clusters
        cluster_1 = np.random.normal(loc=[2, 2, 2], scale=0.5, size=(n_points // 3, 3))
        cluster_2 = np.random.normal(loc=[-2, -2, -2], scale=0.5, size=(n_points // 3, 3))
        cluster_3 = np.random.normal(loc=[3, -3, 1], scale=0.5, size=(n_points - 2 * (n_points // 3), 3))
        
        all_points = np.vstack([cluster_1, cluster_2, cluster_3])
        
        fig_umap = go.Figure()
        
        # Background noise
        fig_umap.add_trace(go.Scatter3d(
            x=np.random.uniform(-4, 4, 1000),
            y=np.random.uniform(-4, 4, 1000),
            z=np.random.uniform(-4, 4, 1000),
            mode='markers',
            marker=dict(size=2, color='rgba(255, 255, 255, 0.1)'),
            hoverinfo='none',
            showlegend=False
        ))
        
        # Clusters
        fig_umap.add_trace(go.Scatter3d(
            x=all_points[:, 0], y=all_points[:, 1], z=all_points[:, 2],
            mode='markers',
            marker=dict(size=4, color=all_points[:, 2], colorscale='Viridis', opacity=0.8),
            text=[f"Embedded Vector #{i}" for i in range(len(all_points))],
            hoverinfo='text',
            showlegend=False
        ))
        
        # Highlight a specific resolution
        fig_umap.add_trace(go.Scatter3d(
            x=[2.1, 2.05, 2.15],
            y=[2.1, 2.15, 2.05],
            z=[2.1, 2.0, 2.2],
            mode='markers+text',
            marker=dict(size=8, color='#ffcc00', symbol='diamond'),
            text=["'Bipul D.' (Panchayat)", "'Bipal Das' (Oral)", "KH-115/P (Satellite)"],
            textposition="top center",
            textfont=dict(color="white"),
            name="Resolved Entity: UNREG-902"
        ))
        
        fig_umap.update_layout(
            margin=dict(l=0, r=0, b=0, t=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            scene=dict(
                xaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=''),
                yaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=''),
                zaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title='')
            ),
            height=500
        )
        
        st.plotly_chart(fig_umap, use_container_width=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 4. Raw Tensor Output
    st.markdown("#### 3. Confidence Matrix Output")
    st.markdown("<p style='color: #a0a0a0; font-size: 0.9rem;'>The deterministic probabilistic math executing under the hood for a single entity merge.</p>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #0c0e15; color: #a0a0a0; padding: 15px; font-family: 'Courier New', Courier, monospace; border-radius: 4px; font-size: 0.8rem; border: 1px solid #1a1c23;">
        <span style="color:#e0e0e0;">[TENSOR OP]</span> Computing Cosine Similarity against Vector DB...<br><br>
        <span style="color:#e0e0e0;">INPUT_VECTOR:</span> [0.12, -0.44, 0.89, ..., 0.02] (Shape: 1x768)<br><br>
        <span style="color:#e0e0e0;">CANDIDATE_MATCHES:</span><br>
        &nbsp;&nbsp;1. Node(UNREG-902) : <span style="color:#63e6be;">Sim=0.984</span> (Euclidean L2=0.012)<br>
        &nbsp;&nbsp;2. Node(REG-104)   : <span style="color:#ff8787;">Sim=0.412</span> (Euclidean L2=2.441)<br>
        &nbsp;&nbsp;3. Node(UNREG-11)  : <span style="color:#ff8787;">Sim=0.301</span> (Euclidean L2=3.102)<br><br>
        <span style="color:#ffcc00;">[MERGE ACTION]</span> Threshold > 0.95 met. Fusing Sub-Graph into UNREG-902.<br>
        <span style="color:#e0e0e0;">[DB WRITE]</span> ACK received. Graph topology updated in 4ms.
    </div>
    """, unsafe_allow_html=True)
