import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time

def render_hub_page():
    st.markdown("<h1 style='text-align: center; font-family: Playfair Display; color: #ffffff; margin-bottom: 0px;'>KritiAI Core Brain</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #a0a0a0; font-size: 1.1rem; margin-top: 5px; margin-bottom: 40px;'>The Multi-Modal Intelligence Hub</p>", unsafe_allow_html=True)
    
    # 3x3 Grid Layout to encircle the brain
    # Top Row
    top_l, top_c, top_r = st.columns([1, 1.5, 1])
    with top_c:
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        if st.button("📄 Document Intelligence\n(OCR & VLM)", use_container_width=True, key="hub_doc"):
            st.query_params["page"] = "doc_intel"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # Middle Row
    mid_l, mid_c, mid_r = st.columns([1, 1.5, 1])
    
    with mid_l:
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        if st.button("🧬 Identity Graph\n(Link Attack)", use_container_width=True, key="hub_id"):
            st.query_params["page"] = "id_graph"
            st.rerun()
            
    with mid_c:
        np.random.seed(42)
        n_points = 500
        
        # Create three distinct clusters
        cluster_1 = np.random.normal(loc=[2, 2, 2], scale=0.5, size=(n_points // 3, 3))
        cluster_2 = np.random.normal(loc=[-2, -2, -2], scale=0.5, size=(n_points // 3, 3))
        cluster_3 = np.random.normal(loc=[3, -3, 1], scale=0.5, size=(n_points - 2 * (n_points // 3), 3))
        
        all_points = np.vstack([cluster_1, cluster_2, cluster_3])
        
        fig = go.Figure()
        
        # Orbital Rings (Enclosing the Brain in a Circle)
        theta = np.linspace(0, 2*np.pi, 100)
        radius = 3.5
        x_ring = radius * np.cos(theta)
        y_ring = radius * np.sin(theta)
        z_zeros = np.zeros(100)
        
        # XY Plane Ring
        fig.add_trace(go.Scatter3d(x=x_ring, y=y_ring, z=z_zeros, mode='lines', line=dict(color='rgba(90, 160, 255, 0.4)', width=2), hoverinfo='none', showlegend=False))
        # XZ Plane Ring
        fig.add_trace(go.Scatter3d(x=x_ring, y=z_zeros, z=y_ring, mode='lines', line=dict(color='rgba(90, 160, 255, 0.2)', width=2), hoverinfo='none', showlegend=False))
        # YZ Plane Ring
        fig.add_trace(go.Scatter3d(x=z_zeros, y=x_ring, z=y_ring, mode='lines', line=dict(color='rgba(90, 160, 255, 0.2)', width=2), hoverinfo='none', showlegend=False))

        # Background noise (sparser and colored)
        fig.add_trace(go.Scatter3d(
            x=np.random.uniform(-4, 4, 300),
            y=np.random.uniform(-4, 4, 300),
            z=np.random.uniform(-4, 4, 300),
            mode='markers',
            marker=dict(size=2, color='rgba(90, 160, 255, 0.15)'),
            hoverinfo='none',
            showlegend=False
        ))
        
        # Clusters
        fig.add_trace(go.Scatter3d(
            x=all_points[:, 0], y=all_points[:, 1], z=all_points[:, 2],
            mode='markers',
            marker=dict(size=4, color=all_points[:, 2], colorscale='electric', opacity=0.8),
            text=[f"Embedded Vector #{i}" for i in range(len(all_points))],
            hoverinfo='text',
            showlegend=False
        ))
        
        # Highlight a specific resolution
        fig.add_trace(go.Scatter3d(
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
        
        fig.update_layout(
            margin=dict(l=0, r=0, b=0, t=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            scene=dict(
                xaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=''),
                yaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=''),
                zaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=''),
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=0.5)
                )
            ),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
    with mid_r:
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        if st.button("🛰️ Spatial Geotagging\n(CV Pipeline)", use_container_width=True, key="hub_land"):
            st.query_params["page"] = "land_cover"
            st.rerun()

    # Bottom Row
    bot_l, bot_c, bot_r = st.columns([1, 1.5, 1])
    
    with bot_l:
        if st.button("🌊 PMFBY Flood Audit\n(Inundation)", use_container_width=True, key="hub_pmfby"):
            st.query_params["page"] = "pmfby"
            st.rerun()
            
    with bot_r:
        if st.button("🌾 Urvarak Sparsity\n(Fertilizer Planning)", use_container_width=True, key="hub_urvarak"):
            st.query_params["page"] = "urvarak"
            st.rerun()
