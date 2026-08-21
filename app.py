import streamlit as st
import numpy as np
from PIL import Image, ImageOps
import urllib.request
from teachablemachine import TeachableMachine

st.set_page_config(page_title="Future Mall - Classifier", page_icon="🛍️", layout="centered")

if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'

def toggle_language():
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'

st.button("🌐 English / العربية", on_click=toggle_language)

TEXTS = {
    'ar': {
        'title': "🛍️ مصنف المنتجات الذكي - Future Mall",
        'subtitle': "ارفع صورة أي منتج أو ضع رابطها لمعرفة تصنيفه، نسبة الثقة، والتحليل الصحي المفصل.",
        'upload_label': "اختر أو اسحب صورة المنتج هنا...",
        'url_label': "أو ضع رابط الصورة المباشر من الإنترنت:",
        'uploaded_img': "الصورة المرفوعة",
        'prediction': "المنتج المحدد",
        'confidence': "نسبة الثقة",
        'health_title': "📊 التقييم والتحليل الصحي",
        'healthy': "🟢 منتج صحي مفيد",
        'unhealthy': "🔴 منتج غير صحي (يُفضل الاعتدال أو التجنب)",
        'fruits_desc': "الفواكه والخضروات غنية بالألياف، الفيتامينات، ومضادات الأكسدة. ممتازة للصحة العامة.",
        'dairy_desc': "منتجات الألبان غنية بالكالسيوم والبروتين الممتاز لبناء العظام والأنسجة.",
        'junk_desc': "يحتوي على نسبة عالية من السكريات أو الدهون. الاستهلاك المفرط يؤدي لمشاكل صحية.",
        'general_desc': "تأكد دائماً من قراءة بطاقة المكونات والقيمة الغذائية قبل الاستهلاك.",
        'error': "حدث خطأ أثناء قراءة الصورة، يرجى المحاولة بصورة أخرى."
    },
    'en': {
        'title': "🛍️ Smart Product Classifier - Future Mall",
        'subtitle': "Upload any product image or paste its link to get its class, confidence score, and health assessment.",
        'upload_label': "Choose or drag a product image here...",
        'url_label': "Or paste a direct image URL from the internet:",
        'uploaded_img': "Uploaded Image",
        'prediction': "Predicted Category",
        'confidence': "Confidence Level",
        'health_title': "📊 Health & Nutritional Assessment",
        'healthy': "🟢 Healthy Product",
        'unhealthy': "🔴 Unhealthy Product (Consume in moderation)",
        'fruits_desc': "Rich in natural fibers, vitamins, and antioxidants.",
        'dairy_desc': "Great source of calcium and high-quality protein.",
        'junk_desc': "Contains high levels of sugars or trans fats.",
        'general_desc': "Always check the nutrition facts panel on the package.",
        'error': "An error occurred while processing the image."
    }
}

t = TEXTS[st.session_state.lang]

st.title(t['title'])
st.write(t['subtitle'])

@st.cache_resource
def load_model():
    return TeachableMachine(model_path="keras_model.h5", labels_file="labels.txt")

model = load_model()

# رفع ملف أو إدخال رابط صورة من النت
uploaded_file = st.file_uploader(
    t['upload_label'], 
    type=["jpg", "jpeg", "png", "webp", "bmp", "tiff", "jfif"]
)
image_url = st.text_input(t['url_label'], placeholder="https://example.com/image.jpg")

image = None

# قراءة الصورة من الملف أو من الرابط
if uploaded_file is not None:
    image = Image.open(uploaded_file)
elif image_url:
    try:
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            image = Image.open(response)
    except Exception:
        st.error(t['error'])

if image is not None:
    try:
        image_rgb = image.convert("RGB")
        st.image(image_rgb, caption=t['uploaded_img'], use_container_width=True)
        
        # حفظ الصورة مؤقتاً للتنبؤ
        image_rgb.save("temp_input.jpg")
        
        result = model.classify_image("temp_input.jpg")
        predicted_class = result['class_name']
        confidence = result['highest_class_confidence'] * 100

        st.markdown("---")
        st.success(f"**{t['prediction']}:** {predicted_class}")
        st.info(f"**{t['confidence']}:** {confidence:.2f}%")

        st.markdown(f"### {t['health_title']}")
        category_lower = str(predicted_class).lower()

        if "fruit" in category_lower or "vegetable" in category_lower:
            st.success(t['healthy'])
            st.write(t['fruits_desc'])
        elif "dairy" in category_lower or "milk" in category_lower or "yoghurt" in category_lower:
            st.success(t['healthy'])
            st.write(t['dairy_desc'])
        else:
            st.warning(t['unhealthy'])
            st.write(t['junk_desc'])

        st.caption(f"💡 {t['general_desc']}")

    except Exception as e:
        st.error(f"{t['error']} ({e})")
