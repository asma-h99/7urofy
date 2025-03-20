import openai
import requests
from PIL import Image
from io import BytesIO
import re
import os
import sys
import time

# ----------------------------------------------
# Setup
# ----------------------------------------------
api_key = "my_key"

client = openai.OpenAI(api_key=api_key)

output_folder = "educational_outputs"
os.makedirs(output_folder, exist_ok=True)

# ----------------------------------------------
# Generate Educational Text
# ----------------------------------------------
def generate_educational_text(letter):
    prompt = f"""
    أنشئ جملة قصيرة مفيدة مكونة من 5 كلمات ذات معنى مترابط و واضح، تحتوي على الحرف ({letter}).  
    اجعل الحرف ({letter}) فقط بخط عريض (bold) داخل كل كلمة يظهر فيها.  
    استخدم تشكيلًا كاملًا للكلمات لضمان نطق صحيح.  
    يجب أن تكون الجملة مترابطة، ذات معنى واضح، وسهلة الفهم لطفل عمره 6 سنوات.  
    استخدم كلمات بسيطة ومألوفة للأطفال لمساعدتهم على تعلم نطق الحرف ({letter}) بسهولة.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "أنت مدرس أطفال تفاعلي تكتب جملًا قصيرة وممتعة مع تشكيل واضح للكلمات وتساعد الطفل على نطق الحرف المختار."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=60
    )

    return response.choices[0].message.content.strip()

# ----------------------------------------------
# Translate to Visual Description [Images]
# ----------------------------------------------

def translate_to_visual_description(text):
    persona_prompt = """
    You are a specialist in generating child-safe cartoon descriptions for educational platforms.
    Rules:
    - Age: 6 years.
    - Style: Bright, colorful, magical, friendly characters.
    - No violence, scary elements, or complex themes.
    - Educational elements encouraged.
    - Simple, clear backgrounds.
    - No text in image.
    """

    full_prompt = f"""
    {persona_prompt}

    Translate this Arabic text into a visual description:
    "{text}"

    Visual Description:
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You create safe, magical cartoons for young children."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.1,
        max_tokens=150
    )

    return response.choices[0].message.content.strip()

# ----------------------------------------------
# Text-to-Speech
# ----------------------------------------------
def text_to_speech(text, output_file):
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="nova",
        input=text
    )

    with open(output_file, "wb") as file:
        file.write(response.content)

# ----------------------------------------------
# Generate Image
# ----------------------------------------------
def generate_image_from_description(prompt, output_path):
    full_prompt = f"{prompt} in a cute anime/cartoon style with no text or writing, simple and child-friendly."

    response = client.images.generate(
        prompt=full_prompt,
        n=1,
        size="512x512"
    )

    image_url = response.data[0].url
    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))
    image.save(output_path)

# ----------------------------------------------
# Main execution
# ----------------------------------------------
def generate (letter):
    text = generate_educational_text(letter)
    visual_description = translate_to_visual_description(text)

    audio_path = os.path.join(output_folder, "output.mp3")
    image_path = os.path.join(output_folder, "generated_image.png")

    text_to_speech(text, audio_path)
    generate_image_from_description(visual_description, image_path)

    print("\n" + "="*40)
    print(":loudspeaker: النص المُولّد:")
    print(f"\n:white_check_mark: {text}")
    print("="*40)

    print("\n:frame_with_picture: الوصف البصري المُولّد:")
    print(f"{visual_description}\n")

    #(f":studio_microphone: تم حفظ الصوت في: {audio_path}")
    print(f":frame_with_picture: تم حفظ الصورة في: {image_path}")

    #Image.open(image_path).show()
    return text,image_path,audio_path