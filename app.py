import os
import streamlit as st
import numpy as np
from PIL import Image, ImageOps
from teachablemachine import TeachableMachine

# 1. إعداد الصفحة
st.set_page_config(page_title="Future Mall - Classifier", layout="centered")

# 2. إدارة اللغة في الجلسة
if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'

def toggle_language():
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'

# 3. نصوص الواجهة باللغتين
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

# 4. زر تغيير اللغة
st.button(t['lang_btn'], on_click=toggle_language)

# 5. العناوين
st.title(t['title'])
st.caption(t['subtitle'])

# 6. تحميل النموذج
@st.cache_resource
def load_model():
    if os.path.exists("keras_model.h5") and os.path.exists("labels.txt"):
        return TeachableMachine(model_path="keras_model.h5", labels_file="labels.txt")
    return None

model = load_model()

if model is None:
    st.error(t['model_error'])
else:
    # 7. رفع الصورة ومعالجتها (مُحدثة بدون أخطاء Deprecation)
    uploaded_file = st.file_uploader(t['upload_label'], type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        
        # عرض الصورة باستخدام المعيار الحديث بدلاً من use_container_width
        st.image(image, width='stretch')

        # حفظ الصورة مؤقتاً للتنبؤ
        temp_path = "temp_image.jpg"
        image.save(temp_path)

        with st.spinner("..." if st.session_state.lang == 'en' else "جاري التحليل..."):
            result = model.classify_image(temp_path)

        # إزالة الملف المؤقت
        if os.path.exists(temp_path):
            os.remove(temp_path)

        # 8. عرض النتائج
        st.subheader(t['result_header'])
        class_name = result.get('highest_class_id', 'Unknown')
        confidence = result.get('highest_class_confidence', 0.0) * 100

        st.success(f"**{class_name}**")
        st.write(f"{t['confidence']} **{confidence:.2f}%**")
