from huggingface_hub import InferenceClient

def run_style_generation(style_name, visual_instruction, image_obj):
    try:
        # 1. Transform Image using the official Hugging Face client library
        # This handles modern server routing and DNS resolution gracefully
        hf_client = InferenceClient(token=HUGGINGFACE_API_KEY)
        
        # Call the pix2pix model directly via the helper client
        transformed_art = hf_client.image_to_image(
            image=image_obj.convert("RGB"),
            prompt=visual_instruction,
            model="timbrooks/instruct-pix2pix"
        )

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
