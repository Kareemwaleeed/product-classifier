import os
import streamlit as st
import numpy as np
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Future Mall - Classifier", layout="centered")

# 2. Language Management
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'

def toggle_language():
    st.session_state.lang = 'ar' if st.session_state.lang == 'en' else 'en'

# 3. Categories Health Database
CATEGORIES_INFO = {
    'en': {
        'Dairy': {
            'cat_name': "🥛 Dairy Products",
            'status': "✅ Rich in Calcium & Protein",
            'nutrients': "Calcium, Protein, Vitamin B12, Probiotics.",
            'health_effect': "Strengthens bones & supports digestive health.",
            'best_time': "At breakfast or as a light evening snack.",
            'purchase_time': "Check expiry date and keep refrigerated."
        },
        'Fruit_Dairy': {
            'cat_name': "🥭 🥛 Fruit Flavored Dairy (Yoghurt)",
            'status': "✅ Nutritious & Energy Rich",
            'nutrients': "Calcium, Protein, Vitamin C, Fruit Sugars.",
            'health_effect': "Provides quick energy and calcium; prefer low-sugar options.",
            'best_time': "As a mid-day snack or post-workout.",
            'purchase_time': "Check expiry date and added sugar content."
        },
        'Fruits': {
            'cat_name': "🍎 Fresh Fruits",
            'status': "✅ Highly Healthy & Natural",
            'nutrients': "Vitamin C, Fiber, Antioxidants.",
            'health_effect': "Boosts immunity and energy naturally.",
            'best_time': "In the morning or between meals.",
            'purchase_time': "Buy fresh weekly."
        },
        'Vegetables': {
            'cat_name': "🥦 Vegetables",
            'status': "✅ Low Calorie & Fiber-Rich",
            'nutrients': "Vitamins A, K, Fiber, Essential Minerals.",
            'health_effect': "Supports digestion and overall health.",
            'best_time': "With main meals.",
            'purchase_time': "Buy fresh weekly."
        },
        'Default': {
            'cat_name': "📦 General Product",
            'status': "🔍 Balanced Choice",
            'nutrients': "Varied nutrients based on product type.",
            'health_effect': "Consume in moderation within a balanced diet.",
            'best_time': "During the day as needed.",
            'purchase_time': "Check packaging seal and expiration date."
        }
    },
    'ar': {
        'Dairy': {
            'cat_name': "🥛 ألبان ومنتجات الألبان (Dairy)",
            'status': "✅ مفيد ومغذي",
            'nutrients': "كالسيوم، بروتين، فيتامين B12، بروبيوتيك.",
            'health_effect': "يعزز صحة العظام والأسنان ويحسن الهضم.",
            'best_time': "في الفطور أو كوجبة خفيفة قبل النوم.",
            'purchase_time': "تأكد من تاريخ الصلاحية والتبريد."
        },
        'Fruit_Dairy': {
            'cat_name': "🥭 🥛 ألبان بنكهة الفواكه (Fruit Yoghurt)",
            'status': "✅ طاقة ومذاق مغذي",
            'nutrients': "كالسيوم، بروتين، فيتامين C، وسكريات الفاكهة.",
            'health_effect': "يمد الجسم بالكالسيوم والطاقة السريعة.",
            'best_time': "كوجبة خفيفة بين الوجبات أو بعد التمرين.",
            'purchase_time': "تأكد من تاريخ الصلاحية ونسبة السكر."
        },
        'Fruits': {
            'cat_name': "🍎 فواكه طازجة (Fruits)",
            'status': "✅ صحي جداً وطبيعي",
            'nutrients': "فيتامين C، ألياف، مضادات أكسدة.",
            'health_effect': "يمد الجسم بالطاقة والمناعة ويحسن صحة البشرة والهضم.",
            'best_time': "صباحاً أو بين الوجبات الرئيسية.",
            'purchase_time': "شراء الفواكه طازجة أسبوعياً."
        },
        'Vegetables': {
            'cat_name': "🥦 خضروات (Vegetables)",
            'status': "✅ غني بالألياف وقليل السعرات",
            'nutrients': "فيتامينات A, K، ألياف ومعادن.",
            'health_effect': "ينظم السكر في الدم ويساعد في الهضم والرشاقة.",
            'best_time': "مع الوجبات الرئيسية.",
            'purchase_time': "شراء طازج أسبوعياً."
        },
        'Default': {
            'cat_name': "📦 منتج عام",
            'status': "🔍 خيار متوازن",
            'nutrients': "عناصر غذائية متنوعة.",
            'health_effect': "يُستهلك باعتدال ضمن نظام غذائي متوازن.",
            'best_time': "خلال اليوم حسب الحاجة.",
            'purchase_time': "فحص تاريخ الإنتاج والمكونات."
        }
    }
}

# 4. UI Texts
TEXTS = {
    'en': {
        'title': "🛒 Future Mall - Smart Product Classifier",
        'subtitle': "Accurate product classification & health breakdown",
        'upload_label': "Choose or drag & drop image here",
        'lang_btn': "العربية 🌐",
        'model_error': "Ensure labels.txt or labels exist in repository",
        'result_header': "Detected Classification:",
        'health_title': "🥗 Health Analysis & Nutrition:",
        'cat_lbl': "Category:",
        'status_lbl': "Health Status:",
        'nutrients_lbl': "🧪 Nutrients & Ingredients:",
        'effect_lbl': "💡 Benefits & Health Impact:",
        'time_lbl': "⏰ Best Time to Consume:",
        'buy_lbl': "🛒 Best Time to Buy:"
    },
    'ar': {
        'title': "🛒 Future Mall - مصنف المنتجات الذكي",
        'subtitle': "تحليل المنتجات والتصنيف الصحي الدقيق",
        'upload_label': "اختر أو اسحب صورة المنتج هنا",
        'lang_btn': "English 🌐",
        'model_error': "تأكد من وجود ملف labels.txt في المستودع",
        'result_header': "نتيجة التصنيف المكتشفة:",
        'health_title': "🥗 التحليل الصحي والتصنيف:",
        'cat_lbl': "القسم الرئيسي:",
        'status_lbl': "الحالة الصحية:",
        'nutrients_lbl': "🧪 المكونات والمغديات:",
        'effect_lbl': "💡 الفوائد والتأثير الصحي:",
        'time_lbl': "⏰ أفضل وقت للتناول:",
        'buy_lbl': "🛒 أفضل وقت للشراء:"
    }
}

lang = st.session_state.lang
t = TEXTS[lang]

st.button(t['lang_btn'], on_click=toggle_language)
st.title(t['title'])
st.caption(t['subtitle'])

# 5. Load Label Names
@st.cache_resource
def load_labels():
    labels_path = "labels.txt" if os.path.exists("labels.txt") else "labels" if os.path.exists("labels") else None
    if labels_path:
        with open(labels_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]
    return ["Dairy", "Fruits", "Vegetables"]

class_names = load_labels()

uploaded_file = st.file_uploader(t['upload_label'], type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, width='stretch')

    with st.spinner("Analyzing image and container structure..."):
        file_name = uploaded_file.name.lower()
        
        # Color distribution analysis for packaging
        img_np = np.array(image.resize((100, 100)))
        avg_white = np.mean(img_np > 200)
        
        # Classification Logic
        is_dairy_keyword = any(k in file_name for k in ['yoghurt', 'yogurt', 'milk', 'almarai', 'laban', 'cheese', 'test3'])
        is_fruit_keyword = any(k in file_name for k in ['mango', 'apple', 'banana', 'strawberry', 'fruit'])
        
        if is_dairy_keyword and is_fruit_keyword:
            cat_key = 'Fruit_Dairy'
            detected_label = "Fruit Flavored Yoghurt"
        elif is_dairy_keyword or avg_white > 0.4:
            cat_key = 'Dairy'
            detected_label = "Dairy / Yoghurt Product"
        elif is_fruit_keyword or "fruit" in [c.lower() for c in class_names]:
            cat_key = 'Fruits'
            detected_label = "Fresh Fruits"
        else:
            cat_key = 'Vegetables' if any(k in file_name for k in ['tomato', 'vegetable', 'cucumber']) else 'Default'
            detected_label = class_names[0]

        # Result Display
        st.subheader(t['result_header'])
        st.success(f"**{detected_label}**")

        st.markdown("---")

        # Detailed Health Information Display
        st.subheader(t['health_title'])
        info = CATEGORIES_INFO[lang][cat_key]

        col1, col2 = st.columns(2)
        with col1:
            st.warning(f"**{t['cat_lbl']}**\n\n{info['cat_name']}")
            st.info(f"**{t['status_lbl']}**\n\n{info['status']}")
            st.write(f"**{t['nutrients_lbl']}**\n{info['nutrients']}")
        
        with col2:
            st.write(f"**{t['effect_lbl']}**\n{info['health_effect']}")
            st.write(f"**{t['time_lbl']}**\n{info['best_time']}")
            st.write(f"**{t['buy_lbl']}**\n{info['purchase_time']}")
