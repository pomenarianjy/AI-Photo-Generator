import streamlit as st
import requests
import os
from io import BytesIO
from PIL import Image
from openai import OpenAI

# Page setup - wide layout is perfect for split views
st.set_page_config(page_title="AI Universe Transformation Showcase 🌌", layout="wide")

st.title("AI Universe Style Transformation Showcase 🌌")
st.write("Browse the multiverse styles below. Select a single dimension in the control panel to run the transformation engine!")

# Securely pull API keys from Streamlit secrets manager
DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY", "")
HUGGINGFACE_API_KEY = st.secrets.get("HUGGINGFACE_API_KEY", "")

# Streamlined core map containing exactly 5 targeted styles
STYLE_MAP = {
    "Ghibli Style": "Studio Ghibli aesthetic, Hayao Miyazaki drawing style, lush background landscape illustration, anime character profile",
    "One Piece": "One Piece manga profile sketch style, Eiichiro Oda layout artwork, dynamic sea pirate backdrop, anime aesthetic",
    "Pixar Style": "Pixar 3D animation style, big expressive eyes, smooth clay lighting shader, cinematic Disney cartoon profile",
    "Anime Style": "Modern clean anime character illustration, sharp vector linework, high contrast lighting, aesthetic Japanese cell shading",
    "Pixel Art": "Retro 16-bit pixel art portrait, classic retro video game character icon, pixelated shading texture, blocky retro color scheme"
}

# Helper to load images safely
def load_local_image(filename):
    if os.path.exists(filename):
        return Image.open(filename)
    return None

original_img = load_local_image("baseline.jpg")

# Live Transformation Engine (Runs only ONE style request at a time)
def run_single_style_generation(style_name, visual_instruction, image_obj):
    try:
        buffered = BytesIO()
        image_obj.convert("RGB").save(buffered, format="JPEG")
        img_bytes = buffered.getvalue()

        url = "https://api-inference.huggingface.co/models/timbrooks/instruct-pix2pix"
        hf_headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/octet-stream"
        }
        
        # Extended timeout for stability during single requests
        hf_res = requests.post(url, headers=hf_headers, data=img_bytes, params={"prompt": visual_instruction}, timeout=30)

        if hf_res.status_code != 200:
            return None, f"Visual engine busy (Status {hf_res.status_code}). Hugging Face is processing other global queues. Please try again in a few seconds."
        
        transformed_art = Image.open(BytesIO(hf_res.content))

        # Build Backstory via DeepSeek
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

# --- MAIN LAYOUT CONTEXT ---
left_view, right_view = st.columns([3, 2], gap="large")

# ==========================================
# LEFT VIEW: STATIC MULTIVERSE EXHIBIT GRID
# ==========================================
with left_view:
    st.subheader("📸 The Reference & Multiverse Preview Gallery")
    
    # Showcase base portrait at the top
    if original_img:
        st.image(original_img, width=200, caption="Your Base Reference Image")
    else:
        st.error("Missing local 'baseline.jpg' file.")
        
    st.write("---")
    st.markdown("### 🖼️ Universe Samples Exhibit")
    st.caption("Here is what each dimension looks like using our sample models:")
    
    styles_list = list(STYLE_MAP.keys())
    
    # Render styles sequentially to balance columns neatly
    for i in range(0, len(styles_list), 2):
        row_col1, row_col2 = st.columns(2)
        
        # Left Slot
        with row_col1:
            s1 = styles_list[i]
            st.markdown(f"**🪐 {s1}**")
            st.caption(STYLE_MAP[s1])
            sample_img_file = f"{s1.lower().replace(' ', '_')}.jpg"
            sample_img = load_local_image(sample_img_file)
            if sample_img:
                st.image(sample_img, use_container_width=True)
            else:
                st.info(f"💡 Upload '{sample_img_file}' to view sample.")
                
        # Right Slot
        if i + 1 < len(styles_list):
            with row_col2:
                s2 = styles_list[i+1]
                st.markdown(f"**🪐 {s2}**")
                st.caption(STYLE_MAP[s2])
                sample_img_file_2 = f"{s2.lower().replace(' ', '_')}.jpg"
                sample_img_2 = load_local_image(sample_img_file_2)
                if sample_img_2:
                    st.image(sample_img_2, use_container_width=True)
                else:
                    st.info(f"💡 Upload '{sample_img_file_2}' to view sample.")
        st.write("")

# ==========================================
# RIGHT VIEW: INTERACTIVE LIVE RUN PANEL
# ==========================================
with right_view:
    st.subheader("⚙️ Live Transformation Control Room")
    st.write("Select a single style dimensions target parameter below to execute your live conversion via the neural engine link.")
    
    # User picks EXACTLY ONE style at a time
    selected_style = st.selectbox("🎯 Target Dimension Universe:", list(STYLE_MAP.keys()))
    
    st.write(f"**Current Style Configuration:**")
    st.info(f"\"{STYLE_MAP[selected_style]}\"")
    
    # Single Action Trigger Button
    if st.button(f"Transform to {selected_style} 🚀", type="primary"):
        if not DEEPSEEK_API_KEY or not HUGGINGFACE_API_KEY:
            st.error("🔑 API Keys Missing: Please check your secrets configurations drawer.")
        elif not original_img:
            st.error("Base portrait missing.")
        else:
            with st.spinner(f"Initializing connection... warping baseline portrait into {selected_style}..."):
                art_out, text_out = run_single_style_generation(selected_style, STYLE_MAP[selected_style], original_img)
                
                if art_out:
                    st.write("---")
                    st.success("🎉 Transformation Complete!")
                    st.image(art_out, use_container_width=True, caption=f"Your Transformed Portrait: {selected_style}")
                    st.markdown(f"### 📜 Multiverse Timeline Identity")
                    st.success(text_out)
                else:
                    st.write("---")
                    st.error(text_out)
