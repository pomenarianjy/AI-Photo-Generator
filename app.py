import streamlit as st
import requests
import os
import time
from io import BytesIO
from PIL import Image
from openai import OpenAI

# Page setup and the new lively introduction
st.set_page_config(page_title="AI Universe Transformation Showcase 🌌", layout="wide")

st.markdown("""
# 🌌 Welcome to the Multiverse Portal
**Ready to jump through time and space?** 🚀  
Select your dream destination, upload your portrait, and watch as our AI engine warps you into the hero, legend, or traveler you were meant to be. From epic galaxy battles to mystical xianxia realms, your transformation awaits—**where will your journey take you today?**
""")
st.write("---")

# ... (Keep your STYLE_MAP, load_local_image, and run_single_style_generation functions here as they were) ...

# --- MAIN LAYOUT ---
left_view, right_view = st.columns([3, 2], gap="large")

with left_view:
    st.subheader("Original Base Portrait Reference")
    original_img = load_local_image("baseline.jpg")
    if original_img:
        img_col1, _ = st.columns([1, 2])
        with img_col1:
            st.image(original_img, use_container_width=True, caption="Base Image: baseline.jpg")
    
    st.write("---")
    st.subheader("🪐 Universe Samples Exhibit Gallery")
    st.caption("Browse our curated dimensions below to see what your new reality could look like!")
    
    styles_list = list(STYLE_MAP.keys())
    
    for i in range(0, len(styles_list), 2):
        row_col1, row_col2 = st.columns(2)
        for col, idx in [(row_col1, i), (row_col2, i+1)]:
            if idx < len(styles_list):
                s = styles_list[idx]
                with col:
                    st.markdown(f"**🪐 {s}**")
                    st.caption(STYLE_MAP[s])
                    fname = f"{s.lower().replace(' ', '_')}.jpg"
                    img = load_local_image(fname)
                    if img: st.image(img, use_container_width=True)
                    else: st.info(f"Upload '{fname}' to view sample.")

with right_view:
    st.subheader("⚙️ Live Transformation Control Room")
    uploaded_file = st.file_uploader("Step 1: Upload your own portrait image (Optional)", type=["jpg", "jpeg", "png"])
    
    # ... (Keep your existing file compliance logic here) ...

    selected_style = st.selectbox("Step 2: Target Dimension Universe:", list(STYLE_MAP.keys()))
    st.info(f"Configuration: {STYLE_MAP[selected_style]}")
    
    if st.button("🚀 Warp Now!", type="primary"):
        # ... (Transformation execution code) ...
        pass

st.write("---")
logo = load_local_image("logo.jpg")
if logo:
    _, c, _ = st.columns([2, 1, 2])
    with c: st.image(logo, use_container_width=True)
