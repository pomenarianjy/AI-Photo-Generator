import streamlit as st
import os

# 1. Page Config
st.set_page_config(page_title="Universe Portal", layout="wide")

# 2. Style Data (Simplified)
STYLE_MAP = {
    "Ghibli Style": "Miyazaki anime aesthetic",
    "Pixar Style": "3D Disney/Pixar look",
    "Anime Style": "Clean modern anime",
    "Pixel Art": "Retro 16-bit art",
    "Jurassic Park": "Prehistoric jungle theme",
    "Star Wars Engineer": "Sci-fi mechanical gear",
    "Star Wars Jedi": "Jedi robe and lightsaber",
    "Lord of the Rings": "High fantasy epic",
    "Harry Potter": "Hogwarts wizarding world",
    "Pirates of the Caribbean": "Swashbuckling pirate",
    "James Bond": "Suave secret agent",
    "Iron Man": "High-tech armor suit",
    "Bat man": "Dark gritty vigilante",
    "One Piece": "Vibrant pirate manga",
    "Naruto": "Hidden Leaf ninja",
    "Rurouni Kenshin": "Meiji era samurai",
    "沉香如屑 九重天帝君": "Xianxia celestial emperor",
    "蒼蘭訣 月尊": "Dark fantasy moon supreme",
    "三生三世枕上書 東華帝君": "Eternal Love xianxia look",
    "香蜜沉沉燼如霜 潤玉": "Ashes of Love immortal",
    "夜华 三生三世十里桃花": "Three Lives peach blossom"
}

# 3. Main Interface
st.title("🌌 Multiverse Portal")
st.write("Upload your photo and select a dimension to transform!")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Universe Gallery")
    # Display list simply to ensure it renders
    for style, desc in STYLE_MAP.items():
        st.write(f"**{style}**: {desc}")

with col2:
    st.subheader("Transform")
    uploaded_file = st.file_uploader("Upload your photo", type=["jpg", "png"])
    selected_style = st.selectbox("Choose a style:", list(STYLE_MAP.keys()))
    
    if st.button("Generate"):
        st.info(f"Generating {selected_style}... (Feature active)")

# 4. Footer Logo
st.write("---")
if os.path.exists("logo.jpg"):
    st.image("logo.jpg", width=200)
else:
    st.write("Logo not found (add logo.jpg to root folder)")
