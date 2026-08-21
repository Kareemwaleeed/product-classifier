import os
import streamlit as st
import numpy as np
from PIL import Image, ImageOps
import onnxruntime as ort

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
        'subtitle': "تحليل الصور ونسبة الثقة بدقة",
        'upload_label': "اختر أو اسحب صورة المنتج هنا",
        'lang_btn': "English 🌐",
        'model_error': "تأكد من وجود ملف model.onnx وملف labels.txt بالحجم الصحيح",
        'result_header': "نتيجة التصنيف:",
        'confidence': "نسبة الثقة:"
    },
    'en': {
        'title': "🛒 Future Mall - Smart Product Classifier",
        'subtitle': "Accurate image analysis and confidence scores",
        'upload_label': "Choose or drag & drop a product image here",
        'lang_btn': "العربية 🌐",
        'model_error': "Ensure valid model.onnx and labels.txt exist in the repository",
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
def load_onnx_model():
    model_file = "model.onnx"
    labels_file = "labels.txt" if os.path.exists("labels.txt") else "labels" if os.path.exists("labels") else None
    
    if os.path.exists(model_file) and labels_file:
        try:
            session = ort.InferenceSession(model_file)
            with open(labels_file, "r", encoding="utf-8") as f:
                class_names = [line.strip() for line in f.readlines()]
            return session, class_names
        except Exception as e:
            return None, None
    return None, None

session, class_names = load_onnx_model()

if session is None or class_names is None:
    st.error(t['model_error'])
else:
    uploaded_file = st.file_uploader(t['upload_label'], type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, width='stretch')

        # معالجة الصورة لـ Teachable Machine (224x224)
        size = (224, 224)
        image_resized = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image_resized, dtype=np.float32)

        # التطبيع
        normalized_image = (image_array / 127.5) - 1.0
        input_data = np.expand_dims(normalized_image, axis=0)

        # التنبؤ
        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name

        with st.spinner("جاري التحليل..." if st.session_state.lang == 'ar' else "Analyzing..."):
            prediction = session.run([output_name], {input_name: input_data})[0]
            
            # حساب النسب المئوية
            exp_preds = np.exp(prediction[0] - np.max(prediction[0]))
            probabilities = exp_preds / np.sum(exp_preds)
            
            index = int(np.argmax(probabilities))
            class_name = class_names[index]
            confidence_score = float(probabilities[index]) * 100

        # عرض النتيجة
        st.subheader(t['result_header'])
        st.success(f"**{class_name}**")
        st.write(f"{t['confidence']} **{confidence_score:.2f}%**")
