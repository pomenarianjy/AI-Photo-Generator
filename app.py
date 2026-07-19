import streamlit as st
import requests
import os
import time
from io import BytesIO
from PIL import Image
from openai import OpenAI

# Page setup
st.set_page_config(page_title="AI Universe Transformation Showcase 🌌", layout="wide")

st.title("AI Universe Style Transformation Showcase 🌌")
st.write("Browse the multiverse styles below. Upload your photo and select a dimension to run the transformation engine!")

# Securely pull API keys from Streamlit secrets manager
DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY", "")
HUGGINGFACE_API_KEY = st.secrets.get("HUGGINGFACE_API_KEY", "")

# Catalog map containing your 22 targeted styles in specific order
STYLE_MAP = {
    "Ghibli Style": "Studio Ghibli aesthetic, Hayao Miyazaki drawing style, lush background landscape illustration, anime character profile",
    "Pixar Style": "Pixar 3D animation style, big expressive eyes, smooth clay lighting shader, cinematic Disney cartoon profile",
    "Anime Style": "Modern clean anime character illustration, sharp vector linework, high contrast lighting, aesthetic Japanese cell shading",
    "Pixel Art": "Retro 16-bit pixel art portrait, classic retro video game character icon, pixelated shading texture, blocky retro color scheme",
    "Jurassic Park": "Prehistoric jungle wilderness theme, cinematic adventure film style, deep emerald tropical foliage background, amber lighting hue",
    "Star Wars Engineer": "Sci-fi space opera portrait, cinematic sci-fi lighting glow, detailed technical gear and mechanical uniform, galaxy background",
    "Star Wars Jedi": "Jedi Knight cinematic portrait, flowing robes, glowing plasma lightsaber illumination, mystical force aura, ancient temple backdrop",
    "Lord of the Rings": "High fantasy epic aesthetic, cinematic middle-earth background, ambient glowing ethereal light, detailed elven or heroic armor portrait",
    "Harry Potter": "Hogwarts wizarding world aesthetic, textured school house robes, cinematic magical candlelight ambiance, mysterious stone castle corridor backdrop",
    "Pirates of the Caribbean": "Swashbuckling high-seas adventure theme, weathered cinematic pirate look, dark ocean fog backdrop, dramatic coastal torchlight",
    "James Bond": "Classic suave secret agent aesthetic, sharp tuxedo formal wear, cinematic high-contrast spy film lighting, luxurious urban backdrop",
    "Iron Man": "High-tech armored suit aesthetic, glowing blue arc reactor chest illumination, sleek metallic reflection finish, holographic interface hud elements",
    "Bat man": "Dark gritty vigilante aesthetic, cinematic moody shadow lighting, iconic cowl silhouette, gothic dark city atmosphere",
    "One Piece": "Vibrant custom anime character design, grand line pirate emblem styling, highly detailed colored manga illustration",
    "Naruto": "Masashi Kishimoto anime layout, Hidden Leaf ninja portrait style, dynamic chakra energy aura effect, sharp manga linework",
    "Rurouni Kenshin": "Classic Meiji era samurai aesthetic, cross-shaped cheek scar detail, flowing crimson standard kimono robes, traditional Japanese ink wash background texture",
    "沉香如屑 九重天帝君": "Xianxia celestial style, Immortal Samsara heavenly emperor look, pure white and silver silk robes, ethereal glowing white hair, sacred ancient palace fog backdrop",
    "蒼蘭訣 月尊": "Dark fantasy xianxia aesthetic, Love Between Fairy and Devil Moon Supreme styling, commanding dark obsidian silk robes with gold trim, dramatic blue or green primordial fire accents",
    "三生三世枕上書 東華帝君": "Eternal Love of Dream xianxia aesthetic, Donghua Dijun look, signature flowing purple royal robes, long silver hair, majestic and serene heavenly palace backdrop",
    "香蜜沉沉燼如霜 潤玉": "Ashes of Love xianxia style, Runyu Night Immortal portrait, elegant pristine white and light blue silk robes, gentle ethereal aura, starry night sky backdrop",
    "夜华 三生三世十里桃花": "Three Lives Three Worlds Ten Miles of Peach Blossoms aesthetic, Ye Hua character style, commanding pure black silk robes, long sleek dark hair, mystical peach blossom orchard backdrop"
}

# Helper to load gallery preview images safely
def load_local_image(filename):
    if os.path.exists(filename):
        return Image.open(filename)
    base_dir = "."
    try:
        files = os.listdir(base_dir)
        for f in files:
            if f.lower() == filename.lower():
                return Image.open(os.path.join(base_dir, f))
    except Exception:
        pass
    return None

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
    st.subheader("Universe Samples Exhibit Gallery")
    st.caption("Here is what each dimension looks like using our sample models:")
    
    styles_list = list(STYLE_MAP.keys())
    
    for i in range(0, len(styles_list), 2):
        row_col1, row_col2 = st.columns(2)
        for col, idx in [(row_col1, i), (row_col2, i+1)]:
            if idx < len(styles_list):
                s = styles_list[idx]
                with col:
                    st.markdown(f"**🪐 {s}**")
                    st.caption(STYLE_MAP[s]) # Restored style description
                    fname = f"{s.lower().replace(' ', '_')}.jpg"
                    img = load_local_image(fname)
                    if img: st.image(img, use_container_width=True)
                    else: st.info(f"Upload '{fname}'")

with right_view:
    st.subheader("Live Transformation Control Room")
    uploaded_file = st.file_uploader("Upload portrait (4MB limit)", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        st.image(uploaded_file, width=150)

    selected_style = st.selectbox("Target Dimension:", list(STYLE_MAP.keys()))
    st.info(f"Configuration: {STYLE_MAP[selected_style]}")
    
    if st.button("Transform"):
        st.write("Transformation engine triggered...")

st.write("---")
logo = load_local_image("logo.jpg")
if logo:
    _, c, _ = st.columns([2, 1, 2])
    with c: st.image(logo, use_container_width=True)
