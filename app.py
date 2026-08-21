import os
import streamlit as st
import numpy as np
from PIL import Image, ImageOps
import tensorflow as tf

# 1. Page Configuration
st.set_page_config(page_title="Future Mall - Classifier", layout="centered")

# 2. Language State Management
if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'

def toggle_language():
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'

# 3. Main 3 Categories Database (Dairy, Fruits, Vegetables)
CATEGORY_DB = {
    'dairy': {
        'ar': {
            'name': "منتجات الألبان والزبادي (Dairy)",
            'status': "✅ غني بالبروتين والكالسيوم",
            'nutrients': "كالسيوم، بروتين، فيتامين B12، وبروبيوتيك (بكتيريا نافعة).",
            'effect': "يقوي العظام والأسنان ويحسن صحة الجهاز الهضمي والمعدة.",
            'time': "في وجبة الإفطار أو كوجبة خفيفة قبل النوم.",
            'buy': "تأكد من تاريخ الصلاحية وحفظ المنتج مبرداً."
        },
        'en': {
            'name': "Dairy & Yoghurt Products",
            'status': "✅ Rich in Calcium & Protein",
            'nutrients': "Calcium, Protein, Vitamin B12, and Probiotics.",
            'effect': "Strengthens bones and improves digestive & gut health.",
            'time': "At breakfast or as a light snack before bed.",
            'buy': "Check expiration date and keep properly refrigerated."
        }
    },
    'fruits': {
        'ar': {
            'name': "فواكه طازجة (Fruits)",
            'status': "✅ غنية بالفيتامينات والألياف الطبيعية",
            'nutrients': "فيتامين C، ألياف غذائية، معادن، ومضادات أكسدة طبيعية.",
            'effect': "تعزز جهاز المناعة، تمد الجسم بالطاقة، وترطب الخلايا.",
            'time': "صباحاً، بين الوجبات الرئيسية، أو قبل/بعد التمرين.",
            'buy': "اختر الثمار الطازجة والزاهية أسبوعياً."
        },
        'en': {
            'name': "Fresh Fruits",
            'status': "✅ Rich in Vitamins & Natural Fiber",
            'nutrients': "Vitamin C, Dietary Fiber, Minerals, and Antioxidants.",
            'effect': "Boosts immunity, provides natural energy, and hydrates.",
            'time': "In the morning, between meals, or around workouts.",
            'buy': "Choose fresh and colorful fruits weekly."
        }
    },
    'vegetables': {
        'ar': {
            'name': "خضروات طازجة (Vegetables)",
            'status': "✅ قليل السعرات وغني بالمعادن",
            'nutrients': "ألياف، حديد، بوتاسيوم، فيتامين A، وفيتامين K.",
            'effect': "يحسن صحة القلب، يساعد في ضبط الوزن، وينظم الهضم.",
            'time': "مع الوجبات الرئيسية أو في السلطات الطازجة.",
            'buy': "شراء الخضروات الطازجة والمتماسكة بشكل دوري."
        },
        'en': {
            'name': "Fresh Vegetables",
            'status': "✅ Low Calorie & Mineral-Rich",
            'nutrients': "Fiber, Iron, Potassium, Vitamin A, and Vitamin K.",
            'effect': "Supports heart health, aids digestion, and helps weight control.",
            'time': "With main lunch/dinner meals or fresh salads.",
            'buy': "Buy crisp and fresh vegetables regularly."
        }
    }
}

# 4. UI Texts
TEXTS = {
    'ar': {
        'title': "🛒 Future Mall - مصنف المنتجات الذكي",
        'subtitle': "تصنيف المنتجات إلى (ألبان - فواكه - خضروات) وعرض القيمة الغذائية",
        'upload': "اختر أو اسحب صورة المنتج هنا",
        'btn': "English 🌐",
        'result_header': "تصنيف المنتج المكتشف:",
        'health_title': "🥗 العناصر القيمة للقسم:"
    },
    'en': {
        'title': "🛒 Future Mall - Smart Product Classifier",
        'subtitle': "Classify products into (Dairy - Fruits - Vegetables)",
        'upload': "Choose or drop product image here",
        'btn': "العربية 🌐",
        'result_header': "Detected Category:",
        'health_title': "🥗 Category Nutrition Breakdown:"
    }
}

lang = st.session_state.lang
t = TEXTS[lang]

# Top Bar Language Switcher
st.button(t['btn'], on_click=toggle_language)
st.title(t['title'])
st.caption(t['subtitle'])

# 5. Load AI Model
@st.cache_resource
def load_ai_model():
    model_path = "keras_model.h5"
    labels_path = "labels.txt" if os.path.exists("labels.txt") else "labels"
    
    if os.path.exists(model_path) and os.path.exists(labels_path):
        model = tf.keras.models.load_model(model_path, compile=False)
        with open(labels_path, "r", encoding="utf-8") as f:
            labels = [line.strip() for line in f.readlines()]
        return model, labels
    return None, None

model, class_names = load_ai_model()

# 6. Upload & Process
uploaded_file = st.file_uploader(t['upload'], type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, width='stretch')

    if model is not None and class_names is not None:
        with st.spinner("جاري تحليل التصنيف..."):
            # Image Preprocessing
            size = (224, 224)
            image_resized = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
            image_array = np.asarray(image_resized)
            normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            data[0] = normalized_image_array

            # Prediction
            prediction = model.predict(data)
            index = np.argmax(prediction)
            raw_label = class_names[index].lower()

            # Map raw model output to the 3 main keys
            category_key = 'fruits'
            if 'dairy' in raw_label or 'milk' in raw_label or 'yog' in raw_label:
                category_key = 'dairy'
            elif 'veg' in raw_label or 'خضار' in raw_label:
                category_key = 'vegetables'
            elif 'fruit' in raw_label or 'فاكه' in raw_label:
                category_key = 'fruits'

            info = CATEGORY_DB[category_key][lang]

            # Display Result
            st.subheader(t['result_header'])
            st.success(f"**{info['name']}**")

            st.markdown("---")

            st.subheader(t['health_title'])

            col1, col2 = st.columns(2)
            with col1:
                st.warning(f"**التصنيف:** {info['name']}" if lang == 'ar' else f"**Category:** {info['name']}")
                st.info(f"**القيمة الغذائية:** {info['status']}" if lang == 'ar' else f"**Value:** {info['status']}")
                st.write(f"**المكونات:** {info['nutrients']}" if lang == 'ar' else f"**Nutrients:** {info['nutrients']}")
            
            with col2:
                st.write(f"**الفوائد:** {info['effect']}" if lang == 'ar' else f"**Benefits:** {info['effect']}")
                st.write(f"**أفضل وقت:** {info['time']}" if lang == 'ar' else f"**Best Time:** {info['time']}")
                st.write(f"**نصيحة الشراء:** {info['buy']}" if lang == 'ar' else f"**Buying Tip:** {info['buy']}")
    else:
        st.error("تأكد من وجود ملفات keras_model.h5 و labels.txt في مجلد المشروع.")
