import os
import streamlit as st
import numpy as np
from PIL import Image, ImageOps
from keras_models_lite import TeachableMachineModel

# 1. إعداد الصفحة
st.set_page_config(page_title="Future Mall - Classifier", layout="centered")

# 2. إدارة اللغة
if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'

def toggle_language():
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'

# 3. النصوص باللغتين
TEXTS = {
    'ar': {
        'title': "🛒 Future Mall - مصنف المنتجات الذكي",
        'subtitle': "تحليل الصور ونسبة الثقة بدقة",
        'upload_label': "اختر أو اسحب صورة المنتج هنا",
        'lang_btn': "English 🌐",
        'model_error': "تأكد من وجود ملفات keras_model.h5 و labels.txt في المستودع",
        'result_header': "نتيجة التصنيف:",
        'confidence': "نسبة الثقة:"
    },
    'en': {
        'title': "🛒 Future Mall - Smart Product Classifier",
        'subtitle': "Accurate image analysis and confidence scores",
        'upload_label': "Choose or drag & drop a product image here",
        'lang_btn': "العربية 🌐",
        'model_error': "Ensure keras_model.h5 and labels.txt are in the repository",
        'result_header': "Classification Result:",
        'confidence': "Confidence Score:"
    }
}

t = TEXTS[st.session_state.lang]

# 4. الواجهة والزرار
st.button(t['lang_btn'], on_click=toggle_language)
st.title(t['title'])
st.caption(t['subtitle'])

# 5. تحميل النموذج والملفات
@st.cache_resource
def load_model():
    model_path = "keras_model.h5"
    labels_path = "labels.txt" if os.path.exists("labels.txt") else "labels" if os.path.exists("labels") else None
    
    if os.path.exists(model_path) and labels_path:
        model = TeachableMachineModel(model_path=model_path, labels_file=labels_path)
        return model
    return None

tm_model = load_model()

if tm_model is None:
    st.error(t['model_error'])
else:
    # 6. رفع الصورة والتصنيف
    uploaded_file = st.file_uploader(t['upload_label'], type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, width='stretch')

        # حفظ وقتي للتنبؤ
        temp_file = "temp_predict.jpg"
        image.save(temp_file)

        with st.spinner("جاري التحليل..." if st.session_state.lang == 'ar' else "Analyzing..."):
            predictions = tm_model.predict(temp_file)
            
            # الحصول على الفئة الأكثر ترجيحاً
            highest_class = predictions['class_name']
            confidence = predictions['confidence'] * 100

        if os.path.exists(temp_file):
            os.remove(temp_file)

        # 7. عرض النتائج
        st.subheader(t['result_header'])
        st.success(f"**{highest_class}**")
        st.write(f"{t['confidence']} **{confidence:.2f}%**")
