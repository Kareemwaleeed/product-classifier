import os
import streamlit as st
import numpy as np
from PIL import Image, ImageOps
import tensorflow as tf

# 1. إعداد الصفحة
st.set_page_config(page_title="Future Mall - Classifier", layout="centered")

# 2. إدارة اللغة
if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'

def toggle_language():
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'

# 3. النصوص
TEXTS = {
    'ar': {
        'title': "🛒 Future Mall - مصنف المنتجات الذكي",
        'subtitle': "تحليل الصور، نسبة الثقة، والتحليل الصحي المفصل",
        'upload_label': "اختر أو اسحب صورة المنتج هنا",
        'lang_btn': "English 🌐",
        'model_error': "لم يتم العثور على ملفات النموذج (keras_model.h5 أو labels.txt)",
        'result_header': "نتيجة التصنيف:",
        'confidence': "نسبة الثقة:"
    },
    'en': {
        'title': "🛒 Future Mall - Smart Product Classifier",
        'subtitle': "Image analysis, confidence score, and detailed health breakdown",
        'upload_label': "Choose or drag & drop a product image here",
        'lang_btn': "العربية 🌐",
        'model_error': "Model files not found (keras_model.h5 or labels.txt)",
        'result_header': "Classification Result:",
        'confidence': "Confidence Score:"
    }
}

t = TEXTS[st.session_state.lang]

st.button(t['lang_btn'], on_click=toggle_language)
st.title(t['title'])
st.caption(t['subtitle'])

# 4. تحميل النموذج
@st.cache_resource
def load_teachable_model():
    if os.path.exists("keras_model.h5") and (os.path.exists("labels.txt") or os.path.exists("labels")):
        labels_file = "labels.txt" if os.path.exists("labels.txt") else "labels"
        model = tf.keras.models.load_model("keras_model.h5", compile=False)
        with open(labels_file, "r", encoding="utf-8") as f:
            class_names = [line.strip() for line in f.readlines()]
        return model, class_names
    return None, None

model, class_names = load_teachable_model()

if model is None or class_names is None:
    st.error(t['model_error'])
else:
    uploaded_file = st.file_uploader(t['upload_label'], type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, width='stretch')

        # معالجة الصورة (224x224)
        size = (224, 224)
        image_resized = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image_resized, dtype=np.float32)
        
        # التطبيع
        normalized_image = (image_array / 127.5) - 1.0
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        data[0] = normalized_image

        # التنبؤ
        with st.spinner("جاري التحليل..." if st.session_state.lang == 'ar' else "Analyzing..."):
            prediction = model.predict(data)
            index = int(np.argmax(prediction))
            class_name = class_names[index]
            confidence_score = float(prediction[0][index]) * 100

        # عرض النتيجة
        st.subheader(t['result_header'])
        st.success(f"**{class_name}**")
        st.write(f"{t['confidence']} **{confidence_score:.2f}%**")
