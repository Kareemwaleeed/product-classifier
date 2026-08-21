import os
import streamlit as st
import numpy as np
from PIL import Image, ImageOps
import tflite_runtime.interpreter as tflite

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
        'model_error': "لم يتم العثور على ملفات النموذج (model.tflite أو labels.txt)",
        'result_header': "نتيجة التصنيف:",
        'confidence': "نسبة الثقة:"
    },
    'en': {
        'title': "🛒 Future Mall - Smart Product Classifier",
        'subtitle': "Image analysis, confidence score, and detailed health breakdown",
        'upload_label': "Choose or drag & drop a product image here",
        'lang_btn': "العربية 🌐",
        'model_error': "Model files not found (model.tflite or labels.txt)",
        'result_header': "Classification Result:",
        'confidence': "Confidence Score:"
    }
}

t = TEXTS[st.session_state.lang]

st.button(t['lang_btn'], on_click=toggle_language)
st.title(t['title'])
st.caption(t['subtitle'])

# 4. تحميل نموذج TFLite
@st.cache_resource
def load_tflite_model():
    labels_file = "labels.txt" if os.path.exists("labels.txt") else "labels" if os.path.exists("labels") else None
    
    if os.path.exists("model.tflite") and labels_file:
        interpreter = tflite.Interpreter(model_path="model.tflite")
        interpreter.allocate_tensors()
        
        with open(labels_file, "r", encoding="utf-8") as f:
            class_names = [line.strip() for line in f.readlines()]
            
        return interpreter, class_names
    return None, None

interpreter, class_names = load_tflite_model()

if interpreter is None or class_names is None:
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
        data = np.expand_dims(normalized_image, axis=0)

        # التنبؤ بـ TFLite
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        with st.spinner("جاري التحليل..." if st.session_state.lang == 'ar' else "Analyzing..."):
            interpreter.set_tensor(input_details[0]['index'], data)
            interpreter.invoke()
            prediction = interpreter.get_tensor(output_details[0]['index'])

            index = int(np.argmax(prediction[0]))
            class_name = class_names[index]
            confidence_score = float(prediction[0][index]) * 100

        # عرض النتيجة
        st.subheader(t['result_header'])
        st.success(f"**{class_name}**")
        st.write(f"{t['confidence']} **{confidence_score:.2f}%**")
