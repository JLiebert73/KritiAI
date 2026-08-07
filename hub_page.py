import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time

def render_hub_page():
    st.markdown("<h1 style='text-align: center; font-family: Playfair Display; color: #ffffff; margin-bottom: 0px;'>KritiAI Core Brain</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #a0a0a0; font-size: 1.1rem; margin-top: 5px; margin-bottom: 40px;'>The Multi-Modal Intelligence Hub</p>", unsafe_allow_html=True)
    
    # 3-Column Layout for the Hub and Spoke
    left_col, center_col, right_col = st.columns([1, 1.5, 1])
    
    # Left Spokes
    with left_col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("📄 Document Intelligence\n(OCR & VLM)", use_container_width=True, key="hub_doc"):
            st.query_params["page"] = "doc_intel"
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🧬 Identity Graph\n(Link Attack)", use_container_width=True, key="hub_id"):
            st.query_params["page"] = "id_graph"
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🌍 Spatial Geotagging\n(Claim Projection)", use_container_width=True, key="hub_geo"):
            st.query_params["page"] = "geotagging"
            st.rerun()
            
    # Center Hub (Rotating Brain)
    with center_col:
        # Generate a spherical/brain-like 3D scatter
        np.random.seed(42)
        n_nodes = 800
        phi = np.random.uniform(0, 2 * np.pi, n_nodes)
        costheta = np.random.uniform(-1, 1, n_nodes)
        u = np.random.uniform(0, 1, n_nodes)
        theta = np.arccos(costheta)
        r = 1.0 * np.cbrt(u)
        
        # Squeeze slightly into an oval shape to resemble a brain
        x = r * np.sin(theta) * np.cos(phi) * 0.8
        y = r * np.sin(theta) * np.sin(phi) * 1.2
        z = r * np.cos(theta) * 0.9
        
        # Color gradient based on depth
        colors = z
        
        fig = go.Figure(data=[go.Scatter3d(
            x=x, y=y, z=z,
            mode='markers',
            marker=dict(
                size=3,
                color=colors,
                colorscale='Agal', # A nice glowing blue/purple scale if available, else Viridis
                opacity=0.8
            ),
            hoverinfo='none'
        )])
        
        # Add rotation animation using layout.scene.camera
        # Streamlit doesn't support live python while loops modifying figures well,
        # but we can set an initial camera angle, or just make it an interactive 3D plot
        # that the user can spin manually, which still looks incredibly cool.
        
        fig.update_layout(
            margin=dict(l=0, r=0, b=0, t=0),
            scene=dict(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                zaxis=dict(visible=False),
                bgcolor='rgba(0,0,0,0)',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=0.5)
                )
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400,
            showlegend=False
        )
        
        # Using a container to center it
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # The Vector Space Button directly below the brain
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        if st.button("🌌 Enter Vector Space", type="primary", use_container_width=True):
            st.query_params["page"] = "vector_space"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # Right Spokes
    with right_col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🛰️ Semantic Land Cover\n(CV Pipeline)", use_container_width=True, key="hub_land"):
            st.query_params["page"] = "land_cover"
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🌊 PMFBY Flood Audit\n(Inundation)", use_container_width=True, key="hub_pmfby"):
            st.query_params["page"] = "pmfby"
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🌾 Urvarak Sparsity\n(Fertilizer Planning)", use_container_width=True, key="hub_urvarak"):
            st.query_params["page"] = "urvarak"
            st.rerun()
