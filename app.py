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
        'subtitle': "تحليل الصور، نسبة الثقة، والتحليل الصحي المفصل",
        'upload_label': "اختر أو اسحب صورة المنتج هنا",
        'lang_btn': "English 🌐",
        'model_error': "لم يتم العثور على ملفات النموذج (model.onnx أو labels.txt)",
        'result_header': "نتيجة التصنيف:",
        'confidence': "نسبة الثقة:"
    },
    'en': {
        'title': "🛒 Future Mall - Smart Product Classifier",
        'subtitle': "Image analysis, confidence score, and detailed health breakdown",
        'upload_label': "Choose or drag & drop a product image here",
        'lang_btn': "العربية 🌐",
        'model_error': "Model files not found (model.onnx or labels.txt)",
        'result_header': "Classification Result:",
        'confidence': "Confidence Score:"
    }
}

t = TEXTS[st.session_state.lang]

st.button(t['lang_btn'], on_click=toggle_language)
st.title(t['title'])
st.caption(t['subtitle'])

# 4. تحميل نموذج ONNX والـ Labels
@st.cache_resource
def load_onnx_model():
    if os.path.exists("model.onnx") and os.path.exists("labels.txt"):
        session = ort.InferenceSession("model.onnx")
        with open("labels.txt", "r", encoding="utf-8") as f:
            class_names = [line.strip() for line in f.readlines()]
        return session, class_names
    return None, None

session, class_names = load_onnx_model()

if session is None or class_names is None:
    st.error(t['model_error'])
else:
    uploaded_file = st.file_uploader(t['upload_label'], type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, width='stretch')

        # 5. معالجة الصورة بنفس معايير Teachable Machine
        size = (224, 224)
        image_resized = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image_resized, dtype=np.float32)

        # التطبيع (Normalization)
        normalized_image = (image_array / 127.5) - 1.0
        input_data = np.expand_dims(normalized_image, axis=0)

        # 6. التشغيل عبر onnxruntime
        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name

        with st.spinner("جاري التحليل..." if st.session_state.lang == 'ar' else "Analyzing..."):
            prediction = session.run([output_name], {input_name: input_data})[0]
            
            # حساب Softmax لضمان تحويل المخرجات لنسب مئوية صحيحة
            exp_preds = np.exp(prediction[0] - np.max(prediction[0]))
            probabilities = exp_preds / np.sum(exp_preds)
            
            index = np.argmax(probabilities)
            class_name = class_names[index]
            confidence_score = float(probabilities[index]) * 100

        # 7. عرض النتائج
        st.subheader(t['result_header'])
        st.success(f"**{class_name}**")
        st.write(f"{t['confidence']} **{confidence_score:.2f}%**")
