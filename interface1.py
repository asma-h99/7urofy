import streamlit as st
from code_f import generate
import base64

# إعداد الصفحة
st.set_page_config(
    page_title="حروفي - شات بوت للأطفال",
    page_icon="🤖",
)

# إضافة CSS لتغيير لون النص في title و markdown فقط
st.markdown(
    """
    <style>
    h1 {
        color: #54701e; 
    }
    .stMarkdown {
        color: #54701e;  
    }
    .user-message {
        color: #1a3e5c; 
        font-weight: bold;
    }
    .bot-message {
        color: #54701e; 
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# استخدام HTML داخل st.markdown لتغيير st.title()
st.markdown("<h1 style='color: #54701e;'></h1>", unsafe_allow_html=True)
st.markdown(" **🌟 هيــــا بنا نتعلم الحروف العربية معاً, يمكننا أن نحقق تقدمًا كبيرًا في إتقان هذه اللغة الجميلة**")

# تهيئة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# دالة لتحويل الصورة إلى base64
def background_image_to_base64(image_path):
    with open(image_path, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    return encoded

# تحديد مسار الصورة للخلفية
image_path = "img.png"  

# إضافة الخلفية باستخدام CSS
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{background_image_to_base64(image_path)}");
        background-size: 75%; 
        background-position: center 95%;
        background-repeat: no-repeat;
        background-attachment: fixed;  
        direction: rtl;  
        text-align: right; 
        background-color: #ffffff;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# دالة لتوليد الردود
def generate_response(prompt):
    description, image_url,audio_path = generate(prompt)
    
    # Return response in the expected format
    return description, image_url,audio_path

# إدخال المستخدم
user_input = st.text_input("", "", placeholder="اكتب الحرف الذي تريد تعلمه هنا...")

if st.button("إرسال") and user_input:
    # توليد الرد
    try:
        response, image_url, audio_path = generate_response(user_input)
        
        # Ensure response, image_url, and audio_path are set properly
        if response is not None and image_url is not None and audio_path is not None:
            # حفظ سجل المحادثة
            st.session_state["messages"].append({"user": user_input, "bot": response, "image_url": image_url, "audio_path": audio_path})

            # عرض سجل المحادثة
            for msg in st.session_state["messages"]:
                st.markdown(f'<div class="user-message">🧑‍🎓 أنت: {msg["user"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="bot-message">🤖 حروفي: <pre>{msg["bot"]}</pre></div>', unsafe_allow_html=True)
                
                # عرض الصورة إذا كانت موجودة
                if "image_url" in msg and msg["image_url"]:
                    st.image(msg["image_url"], caption="🎨 الصورة المولدة", use_container_width=True)
                
                # تشغيل الصوت إذا كان موجودًا
                if "audio_path" in msg and msg["audio_path"]:
                    st.audio(msg["audio_path"])  # Play the audio file

        else:
            st.error("حدث خطأ أثناء توليد الرد!")
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
