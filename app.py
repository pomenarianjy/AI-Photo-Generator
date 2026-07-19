import streamlit as st
import requests
import os
import time
from io import BytesIO
from PIL import Image
from openai import OpenAI

# Page setup - wide layout is perfect for split views
st.set_page_config(page_title="AI Universe Transformation Showcase 🌌", layout="wide")

st.title("AI Universe Style Transformation Showcase 🌌")
st.write("Browse the multiverse styles below. Upload your photo and select a dimension to run the transformation engine!")

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

# Helper to load gallery preview images safely with case-insensitive fallback logic
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

# Live Transformation Engine (Includes automatic retry logic for transient network failures)
def run_single_style_generation(style_name, visual_instruction, image_obj):
    buffered = BytesIO()
    image_obj.convert("RGB").save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()

    url = "https://api-inference.huggingface.co/models/timbrooks/instruct-pix2pix"
    hf_headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/octet-stream"
    }
    
    transformed_art = None
    max_retries = 2
    
    # Retry loop to gracefully handle network drops
    for attempt in range(max_retries):
        try:
            hf_res = requests.post(url, headers=hf_headers, data=img_bytes, params={"prompt": visual_instruction}, timeout=25)
            
            if hf_res.status_code == 200:
                transformed_art = Image.open(BytesIO(hf_res.content))
                break
            elif hf_res.status_code == 503:
                time.sleep(5)
                continue
            else:
                return None, f"Visual engine busy (Status {hf_res.status_code}). Hugging Face community tier capacity exceeded. Please try again in a few moments."
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            if attempt < max_retries - 1:
                time.sleep(3)
                continue
            return None, "Network DNS resolution failed. Streamlit's container network interface is currently disconnected from Hugging Face. Please click 'Reboot App' in your Streamlit Cloud manager dashboard to restore the link."
        except Exception as e:
            return None, f"Portal engine breakdown: {str(e)}"

    if not transformed_art:
        return None, "The image generation engine timed out. The model could be loading from cold storage."

    # Build Backstory via DeepSeek
    try:
        client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com/v1")
        story_prompt = f"Write a funny, catchy, family-safe, 3-sentence backstory introducing an anonymous new character who just landed inside the '{style_name}' universe. Do not use names or identify real people."
        
        completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", content: story_prompt}],
            max_tokens=140
        )
        story_text = completion.choices[0].message.content
        return transformed_art, story_text
    except Exception:
        return transformed_art, f"Welcome to the {style_name} sector of the multiverse. Your transmission code arrived successfully, altering your appearance to blend in perfectly with the local environment."

# --- MAIN LAYOUT CONTEXT ---
left_view, right_view = st.columns([3, 2], gap="large")

# ==========================================
# LEFT VIEW: BASE REFERENCE & EXHIBIT GALLERY
# ==========================================
with left_view:
    st.subheader("Original Base Portrait Reference")
    original_img = load_local_image("baseline.jpg")
    if original_img:
        # Placed in a matching half-width sub-column to exactly mirror the grid items below
        img_col1, img_col2 = st.columns(2)
        with img_col1:
            st.image(original_img, use_container_width=True, caption="Base Image: baseline.jpg")
    else:
        st.info("baseline.jpg not detected in root directory. Live uploaded file will act as context.")

    st.write("---")
    st.subheader("Universe Samples Exhibit Gallery")
    st.caption("Here is what each dimension looks like using our sample models:")
    st.write("---")
    
    styles_list = list(STYLE_MAP.keys())
    
    for i in range(0, len(styles_list), 2):
        row_col1, row_col2 = st.columns(2)
        
        with row_col1:
            s1 = styles_list[i]
            st.markdown(f"**🪐 {s1}**")
            st.caption(STYLE_MAP[s1])
            sample_img_file = f"{s1.lower().replace(' ', '_')}.jpg"
            sample_img = load_local_image(sample_img_file)
            if sample_img:
                st.image(sample_img, use_container_width=True)
            else:
                st.info(f"Upload '{sample_img_file}' to view sample.")
                
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
                    st.info(f"Upload '{sample_img_file_2}' to view sample.")
        st.write("")

# ==========================================
# RIGHT VIEW: INTERACTIVE LIVE RUN PANEL
# ==========================================
with right_view:
    st.subheader("Live Transformation Control Room")
    
    st.markdown("<span style='color: #888888; font-size: 13px; display: block; margin-bottom: -10px;'>Limits: Maximum 4MB size per image • Standard JPEG/PNG format preferred</span>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Step 1: Upload your own portrait image (Optional)", type=["jpg", "jpeg", "png"])
    
    active_img = None
    is_file_compliant = True
    
    if uploaded_file is not None:
        max_bytes = 4 * 1024 * 1024
        if uploaded_file.size > max_bytes:
            st.error(f"File too large: Your file is {uploaded_file.size / (1024*1024):.2f}MB. Please compress the file below 4MB to prevent engine upload drops.")
            is_file_compliant = False
        else:
            try:
                active_img = Image.open(uploaded_file)
                active_img.verify()
                active_img = Image.open(uploaded_file)
            except Exception:
                st.error("Invalid File Structure: The uploaded file appears corrupted or uses an unsupported compression matrix.")
                is_file_compliant = False

        if is_file_compliant and active_img:
            st.success("File verified: Structure and payload size match compliance standards.")
            st.image(active_img, width=150, caption="Uploaded Target Profile")
    else:
        active_img = original_img
        if not active_img:
            st.warning("Ready to process: Please upload a file to customize the input target.")

    selected_style = st.selectbox("Step 2: Target Dimension Universe:", list(STYLE_MAP.keys()))
    
    st.write(f"**Current Style Configuration:**")
    st.info(f"\"{STYLE_MAP[selected_style]}\"")
    
    if st.button(f"Transform to {selected_style}", type="primary", disabled=not is_file_compliant):
        if not DEEPSEEK_API_KEY or not HUGGINGFACE_API_KEY:
            st.error("API Keys Missing: Please check your secrets configurations drawer.")
        elif active_img is None:
            st.error("Missing Target Image: You must upload a clean file or supply baseline.jpg before starting.")
        else:
            with st.spinner(f"Warping portrait into the {selected_style} matrix..."):
                art_out, text_out = run_single_style_generation(selected_style, STYLE_MAP[selected_style], active_img)
                
                if art_out:
                    st.write("---")
                    st.success("Transformation Complete!")
                    st.image(art_out, use_container_width=True, caption=f"Your Transformed Portrait: {selected_style}")
                    st.markdown(f"### Multiverse Timeline Identity")
                    st.info(text_out)
                else:
                    st.write("---")
                    st.error(text_out)

# ==========================================
# FOOTER SIGNATURE SECTION
# ==========================================
st.write("---")
st.markdown(
    '<p style="font-family:\'Brush Script MT\', \'cursive\', sans-serif; color: #FF69B4; font-size: 36px; text-align: center; padding: 25px 0px; margin: 0;">Have a Great Day</p>', 
    unsafe_allow_html=True
)
