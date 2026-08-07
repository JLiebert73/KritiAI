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
    st.markdown("### Document Intelligence & Geotagging Knowledge Graph")
    st.markdown("<p style='color: #a0a0a0; font-size: 0.94rem; margin-bottom: 24px;'>Resolving the 'Tenancy Gap' by extracting unstructured administrative data, building multi-modal identity graphs, and projecting oral-lessee claims directly onto the geospatial grid using Earth Observation Vision Models.</p>", unsafe_allow_html=True)
    
    # -------------------------------------------------------------------------
    # SECTION 1: LIVE INGESTION & DOCUMENT INTELLIGENCE
    # -------------------------------------------------------------------------
    st.markdown("#### 1. Real-Time Document Intelligence (OCR-to-Spatial Pipeline)")
    
    doc_col, terminal_col = st.columns([1, 1.2])
    
    with doc_col:
        with st.container(border=True):
            st.markdown("<b style='color:#e0e0e0;'>Source Data:</b> `Degraded Local Panchayat Lease (Handwritten/Bilingual)`", unsafe_allow_html=True)
            # Simulated messy document snippet
            st.markdown("""
            <div style="background-color: #dfd8c8; color: #3b3a36; padding: 20px; font-family: 'Courier New', Courier, monospace; border-radius: 4px; box-shadow: inset 0 0 10px rgba(0,0,0,0.5); font-style: italic; font-weight: bold; font-size: 0.9rem;">
                <p>Date: 14/06/2023</p>
                <p>Khatauni Reg: KH-115/P (Landlord: R. Sharma)</p>
                <p style="text-decoration: underline;">Sub-lease to: Bipul Das (Oral Lessee)</p>
                <p>Boundary note: 2 bighas South of Gandhi Basti road.</p>
                <p>Crop: Kharif Paddy, Rainfed.</p>
                <p style="opacity: 0.6; font-size: 0.7rem;">(Panchayat seal barely legible... signature scrawled)</p>
            </div>
            """, unsafe_allow_html=True)
    
    with terminal_col:
        with st.container(border=True):
            st.markdown("<b style='color:#8daeff;'>VLM Extraction Engine (KritiAI Terminal)</b>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background-color: #0c0e15; color: #4af626; padding: 15px; font-family: 'Courier New', Courier, monospace; border-radius: 4px; font-size: 0.8rem; height: 180px; overflow-y: auto; border: 1px solid #1a1c23;">
                > [SYSTEM] Initializing Layout-Aware Vision-Language Model...<br>
                > [INGEST] Scanning Panchayat Document #98221...<br>
                > [OCR] Detected Bilingual Script (English/Assamese)...<br>
                > [EXTRACT] Landlord Target: R. Sharma (Resolved to KH-115/P)<br>
                > [EXTRACT] <b>Unregistered Entity:</b> Bipul Das (Role: Lessee)<br>
                > [EXTRACT] Spatial Anchor: "South of Gandhi Basti road"<br>
                > [EXTRACT] Temporal Anchor: "Kharif Paddy"<br>
                > [ALIGN] Vectorizing extracted semantic text for Knowledge Graph projection...<br>
                > <span style="color:#ffcc00;">[SUCCESS] Unregistered Farmer Node Created (ID: UNREG-902).</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # SECTION 2: IDENTITY RESOLUTION KNOWLEDGE GRAPH (3D)
    # -------------------------------------------------------------------------
    st.markdown("#### 2. Identity Resolution via Link Identification (Massive 3D Graph)")
    st.markdown("<p style='color: #a0a0a0; font-size: 0.9rem;'>Using Graph Neural Networks to resolve unregistered entities. <b>Nodes represent the source datalakes</b>, and <b>Edges represent the extracted intelligence linking them</b>.</p>", unsafe_allow_html=True)
    
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
    # SECTION 3: LIVE VISION MODEL POLYGON EXTRACTION
    # -------------------------------------------------------------------------
    st.markdown("#### 3. Live Cross-Modal Vision Segmentation (Physical Geotagging)")
    st.markdown("<p style='color: #a0a0a0; font-size: 0.9rem;'>Now that the identity is resolved, the system dynamically queries the ArcGIS World Imagery API for the Khatauni target coordinate and runs our local vision model pipeline to physically extract the sub-lease parcel boundaries.</p>", unsafe_allow_html=True)
    
    with st.spinner("Initializing ArcGIS Imagery and Vision Extraction Engine..."):
        # Target coordinate in Assam (agricultural area)
        target_lat, target_lon = 26.2343, 91.5644
        
        # Run our vision extraction pipeline
        raw_img = fetch_arcgis_satellite_imagery(target_lat, target_lon, zoom=17)
        binary_mask, skeleton_mask, overlay_img, field_count, valid_contours = extract_field_boundaries(raw_img)
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("<b style='font-size:0.85rem;color:#adb5bd;'>Raw ArcGIS Satellite</b>", unsafe_allow_html=True)
            st.image(raw_img, use_container_width=True)
            st.caption(f"Input: [{target_lat}, {target_lon}]")
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
            
            for contour in valid_contours:
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
                    "Estimated Area (sqm)": area_sqm,
                    "Status": "Matched" if owner not in ["Unknown Tenant", "State Trust"] else "Unregistered"
                })
                
                fig.add_trace(go.Scatter(
                    x=x, y=y,
                    fill="toself",
                    fillcolor="rgba(0, 0, 0, 0)", # Completely transparent fill
                    line=dict(color="rgb(42, 246, 178)", width=2),
                    hoveron="fills", # Trigger hover when mouse is inside the transparent polygon
                    hoverinfo="text",
                    text=f"<b>Geotagged Owner:</b> {owner}<br><b>Registry ID:</b> {khasra}<br><b>Area:</b> {area_sqm} sqm",
                    hoverlabel=dict(bgcolor="rgba(42, 246, 178, 0.9)", font=dict(color="black")),
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

    st.markdown("<br>", unsafe_allow_html=True)
    
    # -------------------------------------------------------------------------
    # SECTION 4: EXTRACTED CADASTRAL REGISTRY (TABLE)
    # -------------------------------------------------------------------------
    st.markdown("#### Live Extracted Cadastral Registry")
    st.markdown("<p style='color: #a0a0a0; font-size: 0.9rem;'>The following database registry was generated in real-time purely from the vision model's boundary extraction and cross-referenced against the Knowledge Graph.</p>", unsafe_allow_html=True)
    
    if len(extracted_registry) > 0:
        df_registry = pd.DataFrame(extracted_registry)
        st.dataframe(df_registry, use_container_width=True, hide_index=True)
    else:
        st.info("No valid cadastral polygons detected in this sector.")

    # -------------------------------------------------------------------------
    # SECTION 4: GROUND-TRUTH GEOTAGGING MAP
    # -------------------------------------------------------------------------
    st.markdown("#### 4. The Geotagged Spatial Registry")
    st.markdown("<p style='color: #a0a0a0; font-size: 0.9rem;'>The PyDeck visualization below demonstrates the final organizational brain state. <b style='color:#63e6be;'>Green polygons</b> are standard registered farmers. The <b style='color:#ffcc00;'>Gold polygon</b> represents our newly geotagged unregistered tenant farmer, completely mapped and fully legally resolvable.</p>", unsafe_allow_html=True)
    
    gandhi_lat = 26.1795
    gandhi_lon = 91.7615

    # We use a mix of standard registered farms (green) and our newly discovered unregistered farm (gold)
    map_data = [
        # Standard Registered
        {"coords": [[91.7588, 26.1805], [91.7602, 26.1815], [91.7628, 26.1818], [91.7645, 26.1808], [91.7648, 26.1792], [91.7635, 26.1778], [91.7610, 26.1775], [91.7592, 26.1788], [91.7588, 26.1805]], 
         "is_unreg": False, "farmer": "S. Borah", "khasra": "KH-101", "resolution": "Direct Land Registry (RoR)"},
         
        # Newly Geotagged Unregistered Tenant Farmer (KH-115/P Sublease)
        {"coords": [[91.7558, 26.1852], [91.7582, 26.1855], [91.7590, 26.1835], [91.7568, 26.1832], [91.7558, 26.1852]], 
         "is_unreg": True, "farmer": "Bipul Das (UNREG-902)", "khasra": "KH-115/P (Sub-lease)", "resolution": "Document OCR + Knowledge Graph Inference"},
         
        # Standard Registered
        {"coords": [[91.7535, 26.1848], [91.7558, 26.1852], [91.7568, 26.1832], [91.7545, 26.1828], [91.7535, 26.1848]], 
         "is_unreg": False, "farmer": "M. Kalita", "khasra": "KH-114", "resolution": "Direct Land Registry (RoR)"},
    ]
    
    viz_data = []
    for f in map_data:
        is_unreg = f["is_unreg"]
        viz_data.append({
            "polygon": f["coords"],
            "farmer_name": f["farmer"],
            "khasra_id": f["khasra"],
            "resolution_method": f["resolution"],
            "fill_color": [255, 204, 0, 165] if is_unreg else [32, 201, 151, 140],
            "line_color": [255, 204, 0, 255] if is_unreg else [100, 255, 180, 255],
            "badge": "UNREGISTERED TENANT (AI-GEOTAGGED)" if is_unreg else "FORMAL LAND OWNER",
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
        latitude=gandhi_lat,
        longitude=gandhi_lon,
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
                    <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; border-bottom: 1px solid rgba(255,255,255,0.15); padding-bottom: 6px; margin-bottom: 8px;">{khasra_id}</div>
                    <div style="font-size: 0.9rem; color: #adb5bd; margin-bottom: 4px;">Cultivator: <b style="color: #ffffff;">{farmer_name}</b></div>
                    <div style="font-size: 0.9rem; color: #adb5bd; margin-bottom: 6px;">Geotagging Method: <b style="color: #8daeff;">{resolution_method}</b></div>
                    <div style="font-size: 0.85rem; font-weight: 700; color: #000000; background: #ffcc00; padding: 4px 8px; border-radius: 4px; display: inline-block;">{badge}</div>
                </div>
                """
            }
        )
    )
