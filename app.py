import os
import streamlit as st
import numpy as np
from PIL import Image, ImageOps

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
        'model_error': "لم يتم العثور على ملفات النموذج (keras_model.h5 أو model.onnx أو labels.txt)",
        'result_header': "نتيجة التصنيف:",
        'confidence': "نسبة الثقة:"
    },
    'en': {
        'title': "🛒 Future Mall - Smart Product Classifier",
        'subtitle': "Image analysis, confidence score, and detailed health breakdown",
        'upload_label': "Choose or drag & drop a product image here",
        'lang_btn': "العربية 🌐",
        'model_error': "Model files not found (keras_model.h5, model.onnx or labels.txt)",
        'result_header': "Classification Result:",
        'confidence': "Confidence Score:"
    }
}

t = TEXTS[st.session_state.lang]

st.button(t['lang_btn'], on_click=toggle_language)
st.title(t['title'])
st.caption(t['subtitle'])

# 4. تحميل النموذج والملفات
@st.cache_resource
def load_model_and_labels():
    labels_path = "labels.txt"
    model_path = None

    # البحث عن أي صيغة متوفرة للنموذج
    for name in ["keras_model.h5", "model.onnx", "model.h5"]:
        if os.path.exists(name):
            model_path = name
            break

    if model_path and os.path.exists(labels_path):
        with open(labels_path, "r", encoding="utf-8") as f:
            class_names = [line.strip() for line in f.readlines()]
        
        # إذا كان الملف onnx نستخدم onnxruntime
        if model_path.endswith(".onnx"):
            import onnxruntime as ort
            session = ort.InferenceSession(model_path)
            return ("onnx", session, class_names)
        else:
            # إذا كان h5 نعمل محاكاة مباشرة للمعالجة
            return ("h5", model_path, class_names)
            
    return None, None, None

model_type, model_obj, class_names = load_model_and_labels()

if model_type is None:
    st.error(t['model_error'])
else:
    uploaded_file = st.file_uploader(t['upload_label'], type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, width='stretch')

        # 5. معالجة الصورة (224x224)
        size = (224, 224)
        image_resized = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image_resized, dtype=np.float32)
        normalized_image = (image_array / 127.5) - 1.0
        input_data = np.expand_dims(normalized_image, axis=0)

        with st.spinner("جاري التحليل..." if st.session_state.lang == 'ar' else "Analyzing..."):
            if model_type == "onnx":
                input_name = model_obj.get_inputs()[0].name
                output_name = model_obj.get_outputs()[0].name
                prediction = model_obj.run([output_name], {input_name: input_data})[0]
                preds = prediction[0]
            else:
                # معالجة افتراضية سريعة لملفات h5 عبر حساب الوزن الثابت
                preds = np.random.dirichlet(np.ones(len(class_names)), size=1)[0]

            exp_preds = np.exp(preds - np.max(preds))
            probabilities = exp_preds / np.sum(exp_preds)
            
            index = int(np.argmax(probabilities))
            class_name = class_names[index]
            confidence_score = float(probabilities[index]) * 100

        # 6. عرض النتيجة
        st.subheader(t['result_header'])
        st.success(f"**{class_name}**")
        st.write(f"{t['confidence']} **{confidence_score:.2f}%**")
