import streamlit as st
import os
from PIL import Image

# Page setup
st.set_page_config(page_title="AI Universe Transformation Showcase 🌌", layout="wide")

# Lively Intro
st.markdown("""
# 🌌 Welcome to the Multiverse Portal
**Ready to jump through time and space?** 🚀  
Select your dream destination, upload your portrait, and watch as our AI engine warps you into the hero, legend, or traveler you were meant to be. From epic galaxy battles to mystical xianxia realms, your transformation awaits—**where will your journey take you today?**
""")
st.write("---")

# Catalog map
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

# Super-Failsafe Image Loader (Finds .jpg, .png, .jpeg regardless of name case)
def load_local_image(filename):
    name_no_ext = os.path.splitext(filename)[0].lower()
    base_dir = "."
    if os.path.exists(base_dir):
        for f in os.listdir(base_dir):
            f_name, f_ext = os.path.splitext(f)
            if f_name.lower() == name_no_ext and f_ext.lower() in ['.jpg', '.jpeg', '.png']:
                try: return Image.open(os.path.join(base_dir, f))
                except: continue
    return None

# --- MAIN LAYOUT ---
left_view, right_view = st.columns([3, 2], gap="large")

with left_view:
    st.subheader("Original Base Portrait Reference")
    # Aligned with gallery grid (2-column layout)
    col_a, col_b = st.columns(2)
    with col_a:
        original_img = load_local_image("baseline.jpg")
        if original_img:
            st.image(original_img, use_container_width=True, caption="Baseline Portrait")
        else:
            st.info("baseline.jpg missing")
    
    st.write("---")
    st.subheader("🪐 Universe Samples Exhibit Gallery")
    
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
                    else: st.warning(f"Missing image for: {s}")

with right_view:
    st.subheader("⚙️ Live Transformation Control Room")
    uploaded_file = st.file_uploader("Upload portrait (4MB limit)", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, width=150)

    selected_style = st.selectbox("Target Dimension:", list(STYLE_MAP.keys()))
    st.info(f"Configuration: {STYLE_MAP[selected_style]}")
    
    if st.button("🚀 Warp Now!", type="primary"):
        st.write("Transformation engine triggered...")

# Footer Logo
st.write("---")
logo = load_local_image("logo.jpg")
if logo:
    _, c, _ = st.columns([2, 1, 2])
    with c: st.image(logo, use_container_width=True)
