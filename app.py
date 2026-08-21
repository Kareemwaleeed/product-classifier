import streamlit as st
import numpy as np
from PIL import Image, ImageOps
import urllib.request

st.set_page_config(page_title="Future Mall - Classifier", page_icon="🛍️", layout="centered")

if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'

def toggle_language():
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'

st.button("🌐 English / العربية", on_click=toggle_language)

TEXTS = {
    'ar': {
        'title': "🛍️ مصنف المنتجات الذكي - Future Mall",
        'subtitle': "ارفع صورة أو ضع رابط صورة من الإنترنت لمعرفة تصنيفها والتحليل الصحي.",
        'upload_label': "1. اسحب واكتُب/ارفع صورة هنا...",
        'url_label': "2. أو ضع رابط الصورة المباشر من الإنترنت هنا:",
        'uploaded_img': "الصورة المحددة",
        'prediction': "المنتج المحدد",
        'confidence': "نسبة الثقة",
        'health_title': "📊 التقييم والتحليل الصحي",
        'healthy': "🟢 منتج صحي مفيد",
        'unhealthy': "🔴 منتج غير صحي (يُفضل الاعتدال أو التجنب)",
        'fruits_desc': "الفواكه والخضروات غنية بالألياف، الفيتامينات، ومضادات الأكسدة. ممتازة للصحة العامة.",
        'dairy_desc': "منتجات الألبان غنية بالكالسيوم والبروتين الممتاز لبناء العظام والأنسجة.",
        'junk_desc': "يحتوي على نسبة عالية من السكريات أو الدهون. الاستهلاك المفرط يؤدي لمشاكل صحية.",
        'general_desc': "تأكد دائماً من قراءة بطاقة المكونات والقيمة الغذائية قبل الاستهلاك.",
        'error': "حدث خطأ أثناء معالجة الصورة، يرجى التأكد من الصورة أو الرابط."
    },
    'en': {
        'title': "🛍️ Smart Product Classifier - Future Mall",
        'subtitle': "Upload an image or paste a web image link to classify and assess health.",
        'upload_label': "1. Choose or drag a product image here...",
        'url_label': "2. Or paste a direct image URL from the internet:",
        'uploaded_img': "Selected Image",
        'prediction': "Predicted Category",
        'confidence': "Confidence Level",
        'health_title': "📊 Health & Nutritional Assessment",
        'healthy': "🟢 Healthy Product",
        'unhealthy': "🔴 Unhealthy Product (Consume in moderation)",
        'fruits_desc': "Rich in natural fibers, vitamins, and antioxidants.",
        'dairy_desc': "Great source of calcium and high-quality protein.",
        'junk_desc': "Contains high levels of sugars or trans fats.",
        'general_desc': "Always check the nutrition facts panel on the package.",
        'error': "An error occurred while processing the image or link."
    }
}

t = TEXTS[st.session_state.lang]

st.title(t['title'])
st.write(t['subtitle'])

# تحميل أسماء التصنيفات
with open("labels.txt", "r", encoding="utf-8") as f:
    class_names = [line.strip() for line in f.readlines()]

# خيار رفع ملف أو أدخال رابط من الإنترنت مباشرة
uploaded_file = st.file_uploader(t['upload_label'], type=["jpg", "jpeg", "png", "webp", "bmp", "tiff", "jfif"])
image_url = st.text_input(t['url_label'], placeholder="https://example.com/image.jpg")

image = None

# قراءة الصورة من الملف أو الرابط
if uploaded_file is not None:
    image = Image.open(uploaded_file)
elif image_url:
    try:
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            image = Image.open(response)
    except Exception:
        st.error(t['error'])

# بدء المعالجة والتنبؤ
if image is not None:
    try:
        # التحويل التلقائي لصيغة RGB لضمان قراءة webp وpng المقصوصة
        image_rgb = image.convert("RGB")
        st.image(image_rgb, caption=t['uploaded_img'], use_container_width=True)
        
        # تجهيز أبعاد الصورة للنموذج (224x224)
        size = (224, 224)
        image_resized = ImageOps.fit(image_rgb, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image_resized)
        normalized = (image_array.astype(np.float32) / 127.5) - 1.0
        data = np.expand_dims(normalized, axis=0)

        # استدعاء الكيراس بطريقة آمنة
        import tensorflow as tf
        model = tf.keras.models.load_model("keras_model.h5", compile=False)
        prediction = model.predict(data, verbose=0)
        
        index = np.argmax(prediction)
        predicted_class = class_names[index]
        confidence = prediction[0][index] * 100

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
