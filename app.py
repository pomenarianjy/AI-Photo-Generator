import streamlit as st
import requests
import os
from io import BytesIO
from PIL import Image
from openai import OpenAI

# Page setups for a beautiful clean look
st.set_page_config(page_title="AI Universe Transformation Showcase 🌌", layout="wide")

# Hide names and keep titles clean
st.title("AI Universe Style Transformation Showcase 🌌")
st.write("See how one classic portrait transforms across 10 distinct fictional dimensions, complete with custom reality-warped backstories.")

# Securely pull API keys from Streamlit secrets manager
DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY", "")
HUGGINGFACE_API_KEY = st.secrets.get("HUGGINGFACE_API_KEY", "")

# Define all 10 specific universe transformations
STYLE_MAP = {
    "Ghibli Style": "Studio Ghibli aesthetic, Hayao Miyazaki drawing style, lush background landscape illustration, anime character profile",
    "Disney Princess": "Disney 3D animation style, cinematic fairy tale princess aesthetic, royal wardrobe clothing, enchanted castle backdrop",
    "One Piece": "One Piece manga profile sketch style, Eiichiro Oda layout artwork, dynamic sea pirate backdrop, anime aesthetic",
    "Naruto": "Naruto ninja manga illustration style, Masashi Kishimoto art look, Hidden Leaf Village background structural elements",
    "Stephen Chow Movie": "1990s Hong Kong comedy movie grading, retro vintage color profiles, Stephen Chow movie style cinematic action shot",
    "Star Wars": "Sci-fi universe space portrait cinematic, wearing galactic outfit accessories or alien creature features, dramatic space setting",
    "Jurassic Park": "Prehistoric scene composition, fantasy elements merging human features cleanly into dinosaur characteristics, Jurassic Park jungle background",
    "Kpop Star": "Vibrant high-fashion Kpop performance stage layout, glowing arena lighting setups, iconic music star look",
    "Sports": "Professional dynamic sports stadium hero backdrop, high action dramatic tracking lighting look, athletic uniform gear",
    "Harry Potter": "Hogwarts grand magic atmosphere background, wizards robes clothing styling layout, holding a magic wand"
}

# Load the local baseline image from your repository folder
def load_local_image():
    if os.path.exists("baseline.jpg"):
        return Image.open("baseline.jpg")
    return None

original_img = load_local_image()

# --- SECTION 1: THE ORIGINAL PORTRAIT ---
st.write("---")
st.subheader("📸 The Original Baseline Portrait")
if original_img:
    st.image(original_img, width=280, caption="Base Reference Image")
else:
    st.error("Missing local image asset. Make sure 'baseline.jpg' is uploaded to the root directory of your GitHub repository.")

# --- SECTION 2: THE 10-STYLE GENERATION SHOWCASE ---
st.write("---")
st.subheader("🌀 The Multiverse Gallery")
st.info("Click the generation engine button below to initialize all 10 alternate-dimension styles side-by-side simultaneously!")

def run_style_generation(style_name, visual_instruction, image_obj):
    try:
        # 1. Transform Image
        buffered = BytesIO()
        image_obj.convert("RGB").save(buffered, format="JPEG")
        img_bytes = buffered.getvalue()

        hf_url = "https://api-inference.huggingface.co/models/timbrooks/instruct-pix2pix"
        hf_headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/octet-stream"
        }
        hf_params = {"prompt": visual_instruction}
        
        hf_res = requests.post(hf_url, headers=hf_headers, data=img_bytes, params=hf_params, timeout=40)
        if hf_res.status_code != 200:
            return None, "Visual engine busy or rate-limited. Please retry in a few moments."
        
        transformed_art = Image.open(BytesIO(hf_res.content))

        # 2. Build Backstory via DeepSeek
        client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com/v1")
        story_prompt = f"Write a funny, catchy, family-safe, 3-sentence backstory introducing an anonymous new character who just landed inside the '{style_name}' universe. Do not use names or identify real people."
        
        completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", content: story_prompt}],
            max_tokens=140
        )
        story_text = completion.choices[0].message.content
        return transformed_art, story_text

    except Exception as e:
        return None, f"Portal error: {str(e)}"

# Master Trigger Button
if st.button("Generate All Styles Matrix 🚀", type="primary"):
    if not DEEPSEEK_API_KEY or not HUGGINGFACE_API_KEY:
        st.error("🔑 API Keys Missing: Make sure you saved DEEPSEEK_API_KEY and HUGGINGFACE_API_KEY inside your Streamlit secrets drawer.")
    elif not original_img:
        st.error("Base image failed to stage.")
    else:
        styles_list = list(STYLE_MAP.keys())
        
        # Split items across 2 columns per row layout
        for i in range(0, len(styles_list), 2):
            col1, col2 = st.columns(2)
            
            # Left Card Item
            with col1:
                st.write(f"### 🪐 {styles_list[i]}")
                with st.spinner(f"Rendering {styles_list[i]}..."):
                    art_out, text_out = run_style_generation(styles_list[i], STYLE_MAP[styles_list[i]], original_img)
                    if art_out:
                        st.image(art_out, use_container_width=True)
                        st.success(text_out)
                    else:
                        st.error(text_out)
            
            # Right Card Item
            if i + 1 < len(styles_list):
                with col2:
                    st.write(f"### 🪐 {styles_list[i+1]}")
                    with st.spinner(f"Rendering {styles_list[i+1]}..."):
                        art_out, text_out = run_style_generation(styles_list[i+1], STYLE_MAP[styles_list[i+1]], original_img)
                        if art_out:
                            st.image(art_out, use_container_width=True)
                            st.success(text_out)
                        else:
                            st.error(text_out)
            st.write("---")
