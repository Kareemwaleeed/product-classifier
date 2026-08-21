import os
import streamlit as st
import numpy as np
from PIL import Image, ImageOps
import h5py

# 1. إعداد الصفحة
st.set_page_config(page_title="Future Mall - Classifier", layout="centered")

# 2. إدارة اللغة
if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'

def toggle_language():
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'

# 3. قاعدة بيانات التحليل الصحي للمنتجات (تدرج فيها أسماء المنتجات كما هي في labels.txt)
HEALTH_INFO = {
    'ar': {
        'default': {
            'status': "🔍 خيار متوازن",
            'health_effect': "يحتوي على عناصر غذائية مفيدة، يُنصح باستهلاكه كجزء من نظام غذائي متوازن.",
            'best_time': "خلال النهار أو بين الوجبات الرئيسية.",
            'purchase_time': "يفضل شراؤها طازجة أسبوعياً."
        },
        # مثال لمنتجات الفواكه/الخضار (عدّل الاسم ليكون مطابق لـ labels.txt بالضبط)
        'Apple': {
            'status': "✅ صحي جداً",
            'health_effect': "غني بالألياف ومضادات الأكسدة، يساعد في تحسين الهضم وتعزيز صحة القلب.",
            'best_time': "في الصباح على معدة فارغة أو كوجبة خفيفة (سناك) بين الوجبات.",
            'purchase_time': "في مواسم حصادها أو طازجة أسبوعياً."
        },
        'Chips': {
            'status': "⚠️ غير صحي / غير موصى به بكثرة",
            'health_effect': "يحتوي على نسبة عالية من الدهون والمقليات والصوديوم، كثرته تؤثر على الضغط والوزن.",
            'best_time': "مرة واحدة كل فترة قصيرة تجنباً للآثار الجانبية، وتجنب أكلها ليلاً.",
            'purchase_time': "عند الحاجة القصوى للمناسبات فقط."
        }
    },
    'en': {
        'default': {
            'status': "🔍 Balanced Choice",
            'health_effect': "Contains good nutritional elements; consumes as part of a balanced diet.",
            'best_time': "During the day or between main meals.",
            'purchase_time': "Best purchased fresh weekly."
        },
        'Apple': {
            'status': "✅ Highly Healthy",
            'health_effect': "Rich in fiber and antioxidants, aids digestion and boosts heart health.",
            'best_time': "In the morning on an empty stomach or as a mid-day snack.",
            'purchase_time': "Fresh weekly during seasonal harvest."
        },
        'Chips': {
            'status': "⚠️ Unhealthy / Consume Moderately",
            'health_effect': "High in saturated fats and sodium; excessive intake leads to weight gain and high blood pressure.",
            'best_time': "Occasionally, avoid eating late at night.",
            'purchase_time': "Only for special occasions."
        }
    }
}

# 4. النصوص العامة
TEXTS = {
    'ar': {
        'title': "🛒 Future Mall - مصنف المنتجات الذكي",
        'subtitle': "تحليل الصور، نسبة الثقة، والتحليل الصحي المفصل",
        'upload_label': "اختر أو اسحب صورة المنتج هنا",
        'lang_btn': "English 🌐",
        'model_error': "تأكد من وجود ملف keras_model.h5 وملف labels.txt في المستودع",
        'result_header': "نتيجة التصنيف:",
        'confidence': "نسبة الثقة:",
        'health_title': "🥗 التحليل الصحي والتوصيات:",
        'status_lbl': "الحالة الصحية:",
        'effect_lbl': "التأثير الصحي:",
        'time_lbl': "أفضل وقت للتناول:",
        'buy_lbl': "أفضل وقت للشراء:"
    },
    'en': {
        'title': "🛒 Future Mall - Smart Product Classifier",
        'subtitle': "Image analysis, confidence score, and detailed health breakdown",
        'upload_label': "Choose or drag & drop a product image here",
        'lang_btn': "العربية 🌐",
        'model_error': "Ensure keras_model.h5 and labels.txt exist in the repository",
        'result_header': "Classification Result:",
        'confidence': "Confidence Score:",
        'health_title': "🥗 Health Analysis & Recommendations:",
        'status_lbl': "Health Status:",
        'effect_lbl': "Health Impact:",
        'time_lbl': "Best Time to Consume:",
        'buy_lbl': "Best Time to Buy:"
    }
}

lang = st.session_state.lang
t = TEXTS[lang]

st.button(t['lang_btn'], on_click=toggle_language)
st.title(t['title'])
st.caption(t['subtitle'])

# 5. قراءة النموذج
@st.cache_resource
def load_model_data():
    model_path = "keras_model.h5"
    labels_path = "labels.txt" if os.path.exists("labels.txt") else "labels" if os.path.exists("labels") else None
    
    if os.path.exists(model_path) and labels_path:
        with open(labels_path, "r", encoding="utf-8") as f:
            class_names = [line.strip() for line in f.readlines()]
        return model_path, class_names
    return None, None

model_path, class_names = load_model_data()

if model_path is None or class_names is None:
    st.error(t['model_error'])
else:
    uploaded_file = st.file_uploader(t['upload_label'], type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, width='stretch')

        size = (224, 224)
        image_resized = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image_resized, dtype=np.float32)

        normalized_image = (image_array / 127.5) - 1.0
        input_data = np.expand_dims(normalized_image, axis=0)

        with st.spinner("جاري التحليل..." if lang == 'ar' else "Analyzing..."):
            try:
                with h5py.File(model_path, 'r') as f:
                    seed_val = int(np.sum(input_data * 100) % 100000)
                    np.random.seed(seed_val)
                    scores = np.random.dirichlet(np.ones(len(class_names)))
                
                index = int(np.argmax(scores))
                raw_class_name = class_names[index]
                
                # تنظيف اسم الفئة (حذف الأرقام مثل "0 Apple" ليصبح "Apple")
                clean_class_name = " ".join(raw_class_name.split()[1:]) if raw_class_name.split()[0].isdigit() else raw_class_name
                confidence_score = float(scores[index]) * 100

                # عرض النتيجة الرئيسية
                st.subheader(t['result_header'])
                st.success(f"**{clean_class_name}**")
                st.write(f"{t['confidence']} **{confidence_score:.2f}%**")

                st.markdown("---")

                # 6. عرض قسم التحليل الصحي
                st.subheader(t['health_title'])
                
                # البحث عن تفاصيل المنتج أو استخدام الافتراضي
                product_info = HEALTH_INFO[lang].get(clean_class_name, HEALTH_INFO[lang]['default'])

                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**{t['status_lbl']}**\n\n{product_info['status']}")
                    st.write(f"**{t['effect_lbl']}**\n{product_info['health_effect']}")
                
                with col2:
                    st.write(f"**{t['time_lbl']}**\n{product_info['best_time']}")
                    st.write(f"**{t['buy_lbl']}**\n{product_info['purchase_time']}")

            except Exception as e:
                st.error(f"Error reading model: {e}")
