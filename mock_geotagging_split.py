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

def render_back_button():
    if st.button("🏠 Back to KritiAI Core Brain", use_container_width=True):
        st.query_params["page"] = "hub"
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)

def render_doc_intel_page():
    render_back_button()
    
def render_id_graph_page():
    render_back_button()
    
def render_vector_space_page():
    render_back_button()
    
def render_land_cover_page():
    render_back_button()
    
def render_geotagging_map_page():
    render_back_button()
    
