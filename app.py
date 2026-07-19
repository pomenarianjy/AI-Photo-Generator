import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image
from openai import OpenAI

# Page configurations
st.set_page_config(page_title="Multiverse Photo Styler 🌌", layout="centered")
st.title("Multiverse Photo Styler 🌌")

# Securely pull API keys from Streamlit's secrets manager
DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY", "")
HUGGINGFACE_API_KEY = st.secrets.get("HUGGINGFACE_API_KEY", "")

# Visual style instructions passed to the image generator
STYLE_PROMPTS = {
    "ghibli": "Studio Ghibli aesthetic, Hayao Miyazaki drawing style, lush background landscape illustration, anime character profile",
    "disney": "Disney 3D animation style, cinematic fairy tale princess aesthetic, royal wardrobe clothing, enchanted castle backdrop",
    "onepiece": "One Piece manga profile sketch style, Eiichiro Oda layout artwork, dynamic sea pirate backdrop, anime aesthetic",
    "naruto": "Naruto ninja manga illustration style, Masashi Kishimoto art look, Hidden Leaf Village background structural elements",
    "chow": "1990s Hong Kong comedy movie grading, retro vintage color profiles, Stephen Chow movie style cinematic action shot",
    "starwars": "Sci-fi universe space portrait cinematic, wearing galactic outfit accessories or alien creature features, dramatic space setting",
    "jurassic": "Prehistoric scene composition, fantasy elements merging human features cleanly into dinosaur characteristics, Jurassic Park jungle background",
    "kpop": "Vibrant high-fashion Kpop performance stage layout, glowing arena lighting setups, iconic music star look",
    "sports": "Professional dynamic sports stadium hero backdrop, high action dramatic tracking lighting look, athletic uniform gear",
    "harrypotter": "Hogwarts grand magic atmosphere background, wizards robes clothing styling layout, holding a magic wand"
}

# 1. Image Input Selection
st.subheader("1. Select Your Input Photo")
source_option = st.radio("Choose source:", ("Use Lemuel Lee Sample Image", "Upload My Own Photo"))

img_to_process = None

if source_option == "Use Lemuel Lee Sample Image":
    # Using the standard image URL from the Caproasia article
    sample_url = "https://www.caproasia.com/wp-content/uploads/2023/06/BNP-Paribas-Appoints-Lemuel-Lee-as-Head-of-Wealth-Management-Hong-Kong.jpg"
    try:
        response = requests.get(sample_url, timeout=10)
        img_to_process = Image.open(BytesIO(response.content))
        st.image(img_to_process, caption="Staging Sample: Lemuel Lee", width=250)
    except Exception:
        st.error("Could not load the online sample photo automatically. Please use the upload option below!")
else:
    uploaded_file = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img_to_process = Image.open(uploaded_file)
        st.image(img_to_process, caption="Uploaded Photo", width=250)

# 2. Target Style Picker
st.subheader("2. Pick Your Target Universe")
selected_style = st.selectbox(
    "Choose a style transformation:",
    options=list(STYLE_PROMPTS.keys()),
    format_func=lambda x: {
        "ghibli": "Ghibli Manga Style",
        "disney": "Disney Princess Style",
        "onepiece": "One Piece Anime Style",
        "naruto": "Naruto Anime Style",
        "chow": "Stephen Chow Movie Style",
        "starwars": "Star Wars Character Style",
        "jurassic": "Jurassic Park Dinosaur Mashup",
        "kpop": "Kpop Star Style",
        "sports": "Sports Icon Style",
        "harrypotter": "Harry Potter Wizard Style"
    }.get(x, x.capitalize())
)

# 3. Execution Trigger
if st.button("Transform Universe Style 🚀", disabled=(img_to_process is None)):
    if not DEEPSEEK_API_KEY or not HUGGINGFACE_API_KEY:
        st.error("🔑 Keys Missing: Please navigate to your Streamlit App dashboard settings and add DEEPSEEK_API_KEY and HUGGINGFACE_API_KEY to Advanced Secrets.")
    else:
        with st.spinner("Opening a rift in the space-time continuum..."):
            try:
                # Convert the input image into standard binary formats for raw payload transport
                buffered = BytesIO()
                img_to_process.convert("RGB").save(buffered, format="JPEG")
                img_bytes = buffered.getvalue()

                # Step A: Query Hugging Face free pipeline endpoint for image manipulation
                hf_url = "https://api-inference.huggingface.co/models/timbrooks/instruct-pix2pix"
                hf_headers = {
                    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
                    "Content-Type": "application/octet-stream"
                }
                hf_params = {"prompt": STYLE_PROMPTS[selected_style]}
                
                hf_res = requests.post(hf_url, headers=hf_headers, data=img_bytes, params=hf_params, timeout=45)
                
                if hf_res.status_code != 200:
                    raise Exception(f"The visual conversion engine returned an error code: {hf_res.status_code}. It might be waking up or busy.")
                
                output_image = Image.open(BytesIO(hf_res.content))

                # Step B: Query DeepSeek text API to compose the hilarious matching context
                client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com/v1")
                story_prompt = f"""
                Write a funny, catchy, and perfectly appropriate 3-sentence backstory snippet introducing an unexpected new character who just materialized inside the '{selected_style}' universe. 
                Keep it completely family-friendly (absolutely no violence, erotica, or rude context). Make it witty and entertaining!
                """
                
                completion = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "user", content: story_prompt}],
                    max_tokens=150
                )
                story_text = completion.choices[0].message.content

                # UI Results Layout
                st.success("Dimension Jump Successful!")
                col1, col2 = st.columns(2)
                with col1:
                    st.image(output_image, caption="AI Style Transformation", use_container_width=True)
                with col2:
                    st.info("📜 Universe Story Log")
                    st.write(story_text)

            except Exception as e:
                st.error(f"💥 Portal Failure: {str(e)}")
