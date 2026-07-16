import streamlit as st
import pydeck as pdk
import pandas as pd
from architecture_matrix import render_5x5_architecture_matrix

def render_urvarak_sparsity_page():
    """
    Renders Mock UI 2: Urvarak-Sparsity (Fertilizer Micro-Allocation Planner)
    Solves: Replacing subjective, manual estimates of village fertilizer demand with real-time, soil-and-crop-specific supply modeling.
    """
    st.markdown("""
    <div class="glass-wrapper" style="margin-bottom: 24px;">
        <div class="glass-card" style="border-left: 4px solid #51cf66; background: linear-gradient(135deg, rgba(81, 207, 102, 0.15) 0%, rgba(15, 17, 26, 0.96) 100%);">
            <div style="font-size: 1.5rem; font-weight: 700; color: #ffffff;">Urvarak-Sparsity: Fertilizer Micro-Allocation Planner</div>
            <div style="color: #adb5bd; font-size: 0.98rem; margin-top: 6px;">Replacing subjective manual estimates of village fertilizer demand with real-time, soil-and-crop-specific supply modeling integrated with the national e-Urvarak / iFMS portal.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ----------------- TOP VIEW: CHOROPLETH & HOTSPOT MAP -----------------
    st.markdown("### Step 1: Block-Level Crop Footprint & Soil Nutrient Deficiency Hotspots")
    st.markdown("<p style='color: #a0a0a0; font-size: 0.92rem; margin-bottom: 16px;'>Choropleth rendering of crop classification footprints (`Node 1 & 3: Prithvi HLS cubes isolating high-nutrient demanding crops`) cross-referenced against National One Soil NPK deficiency grids (`Node 9 & 13`).</p>", unsafe_allow_html=True)

    # Kamrup Blocks Polygon Data
    blocks_data = [
        {"name": "Rangia Agricultural Block", "crop": "Winter Rice & Wheat (High N Demand)", "npk_status": "Severe Nitrogen Deficiency (-34%)", "color": [250, 82, 82, 160], "polygon": [[91.68, 26.24], [91.75, 26.26], [91.78, 26.21], [91.70, 26.19], [91.68, 26.24]]},
        {"name": "Palashbari Block", "crop": "Mustard & Pulses (Phosphorus Sensitive)", "npk_status": "Moderate Phosphorus Deficiency (-18%)", "color": [255, 168, 76, 160], "polygon": [[91.70, 26.19], [91.78, 26.21], [91.82, 26.16], [91.74, 26.13], [91.70, 26.19]]},
        {"name": "Hajo Alluvial Block", "crop": "Early Boro Paddy", "npk_status": "Balanced NPK Grid", "color": [81, 207, 102, 160], "polygon": [[91.60, 26.22], [91.68, 26.24], [91.70, 26.19], [91.62, 26.17], [91.60, 26.22]]},
        {"name": "Boko River Basin Block", "crop": "Jute & Kharif Vegetables", "npk_status": "Potassium Deficiency (-22%)", "color": [255, 212, 59, 160], "polygon": [[91.52, 26.18], [91.60, 26.22], [91.62, 26.17], [91.55, 26.13], [91.52, 26.18]]}
    ]

    block_layer = pdk.Layer(
        "PolygonLayer",
        data=blocks_data,
        get_polygon="polygon",
        get_fill_color="color",
        get_line_color=[255, 255, 255, 255],
        get_line_width=3,
        pickable=True
    )

    view_state = pdk.ViewState(latitude=26.20, longitude=91.68, zoom=10.8, pitch=35)
    st.pydeck_chart(pdk.Deck(
        layers=[block_layer],
        initial_view_state=view_state,
        tooltip={"text": "Block: {name}\nCrop Profile: {crop}\nSoil Nutrient Status: {npk_status}"}
    ))

    st.markdown("<br>", unsafe_allow_html=True)

    # ----------------- INTERACTIVE SLIDERS & DATA TABLE -----------------
    st.markdown("### Step 2: Interactive Allocation Planner & Correction Sliders")
    st.markdown("<p style='color: #a0a0a0; font-size: 0.92rem; margin-bottom: 16px;'>Dynamically adjust regional supply parameters to test monsoon scenarios and compute mathematically optimized village quotas.</p>", unsafe_allow_html=True)

    slider_col1, slider_col2, slider_col3 = st.columns(3)
    with slider_col1:
        n_scale = st.slider("Scale Nitrogen Target (%)", min_value=-30, max_value=50, value=10, step=5, help="Adjust Urea allocation based on anticipated vegetative demands.")
    with slider_col2:
        monsoon_shift = st.slider("Anticipated Monsoon Shift (Weeks)", min_value=-2, max_value=4, value=0, step=1, help="Advance or delay supply delivery schedules.")
    with slider_col3:
        buffer_margin = st.slider("Urea Bag Buffer Margin (%)", min_value=0, max_value=25, value=10, step=5, help="Emergency contingency stock held at district warehouse.")

    # Compute dynamic allocation based on sliders
    scale_factor = 1.0 + (n_scale / 100.0)
    buf_factor = 1.0 + (buffer_margin / 100.0)

    villages = [
        {"village": "Rangia Cadastral Cluster", "block": "Rangia", "crop_area_ha": 1420.5, "npk_status": "Severe N (-34%)", "base_urea": 284, "base_dap": 142, "base_mop": 71},
        {"village": "Palashbari South Cluster", "block": "Palashbari", "crop_area_ha": 980.2, "npk_status": "Moderate P (-18%)", "base_urea": 176, "base_dap": 118, "base_mop": 49},
        {"village": "Hajo Central Village", "block": "Hajo", "crop_area_ha": 1150.0, "npk_status": "Balanced NPK", "base_urea": 207, "base_dap": 104, "base_mop": 58},
        {"village": "Boko Alluvial Basin", "block": "Boko", "crop_area_ha": 860.8, "npk_status": "Severe K (-22%)", "base_urea": 155, "base_dap": 78, "base_mop": 65},
        {"village": "Kamalpur North Grid", "block": "Kamalpur", "crop_area_ha": 1310.4, "npk_status": "Moderate N (-15%)", "base_urea": 249, "base_dap": 125, "base_mop": 62}
    ]

    table_rows = []
    for v in villages:
        opt_urea = int(v["base_urea"] * scale_factor * buf_factor)
        table_rows.append({
            "Village / Cluster Name": v["village"],
            "Block": v["block"],
            "Computed Acreage (Ha)": f"{v['crop_area_ha']:,.1f}",
            "Soil NPK Deficiency (`Node 13`)": v["npk_status"],
            "Optimized Urea Allocation (MT)": f"{opt_urea:,} MT",
            "Optimized DAP Allocation (MT)": f"{int(v['base_dap'] * buf_factor):,} MT",
            "Optimized MOP Allocation (MT)": f"{int(v['base_mop'] * buf_factor):,} MT"
        })

    df_table = pd.DataFrame(table_rows)
    st.dataframe(df_table, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ----------------- ACTION BUTTON: EXPORT iFMS CSV -----------------
    st.markdown("### Step 3: Export National Supply Schedule (`Node 24`)")
    st.markdown("<p style='color: #a0a0a0; font-size: 0.92rem; margin-bottom: 16px;'>Format the spatial optimization output to match the exact schema of the national Integrated Fertilizer Management System (`e-Urvarak / iFMS`) portal.</p>", unsafe_allow_html=True)

    csv_data = df_table.to_csv(index=False).encode("utf-8")
    
    export_col1, export_col2 = st.columns([1.5, 2.5])
    with export_col1:
        st.download_button(
            label="Export iFMS CSV (National Portal Template)",
            data=csv_data,
            file_name="urvarak_ifms_supply_schedule_kamrup.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )
    with export_col2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.03); padding: 12px 16px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); font-size: 0.88rem; color: #adb5bd;">
            <b>Automated Portal Integration:</b> CSV payload formatted according to Department of Fertilizers Scheme Code 24 data exchange contract. Ready for automated SFTP ingest into state fertilizer dispatch depots.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 35px 0;'>", unsafe_allow_html=True)
    st.markdown("### Architecture Matrix Illumination for Urvarak-Sparsity Workflow")
    render_5x5_architecture_matrix("URVARAK", compact=True)
