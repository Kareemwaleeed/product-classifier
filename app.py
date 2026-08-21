import os
import streamlit as st
import numpy as np
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Future Mall - Classifier", layout="centered")

# 2. Language Management
if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'

def toggle_language():
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'

# 3. Categories Health Database
CATEGORIES_INFO = {
    'ar': {
        'Dairy': {
            'cat_name': "🥛 زبادي ومنتجات ألبان (Dairy)",
            'status': "✅ مفيد ومغذي",
            'nutrients': "كالسيوم، بروتين، فيتامين B12، بروبيوتيك.",
            'health_effect': "يعزز صحة العظام والأسنان ويحسن الهضم.",
            'best_time': "في الفطور أو كوجبة خفيفة قبل النوم.",
            'purchase_time': "تأكد من تاريخ الصلاحية والتبريد."
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
            'cat_name': "🥦 خضروات طازجة (Vegetables)",
            'status': "✅ غني بالألياف وقليل السعرات",
            'nutrients': "فيتامينات A, K، ألياف ومعادن.",
            'health_effect': "ينظم السكر في الدم ويساعد في الهضم والرشاقة.",
            'best_time': "مع الوجبات الرئيسية.",
            'purchase_time': "شراء طازج أسبوعياً."
        }
    },
    'en': {
        'Dairy': {
            'cat_name': "🥛 Dairy / Yoghurt Products",
            'status': "✅ Rich in Calcium & Protein",
            'nutrients': "Calcium, Protein, Vitamin B12, Probiotics.",
            'health_effect': "Strengthens bones & supports digestive health.",
            'best_time': "At breakfast or as a light evening snack.",
            'purchase_time': "Check expiry date and keep refrigerated."
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
        }
    }
}

# 4. UI Texts
TEXTS = {
    'ar': {
        'title': "🛒 Future Mall - مصنف المنتجات الذكي",
        'subtitle': "تحليل المنتجات والتصنيف الصحي الدقيق",
        'upload_label': "اختر أو اسحب صورة المنتج هنا",
        'lang_btn': "English 🌐",
        'result_header': "نتيجة التصنيف المكتشفة:",
        'health_title': "🥗 التحليل الصحي والتصنيف:",
        'cat_lbl': "القسم الرئيسي:",
        'status_lbl': "الحالة الصحية:",
        'nutrients_lbl': "🧪 المكونات والمغديات:",
        'effect_lbl': "💡 الفوائد والتأثير الصحي:",
        'time_lbl': "⏰ أفضل وقت للتناول:",
        'buy_lbl': "🛒 أفضل وقت للشراء:"
    },
    'en': {
        'title': "🛒 Future Mall - Smart Product Classifier",
        'subtitle': "Accurate product classification & health breakdown",
        'upload_label': "Choose or drag & drop image here",
        'lang_btn': "العربية 🌐",
        'result_header': "Detected Classification:",
        'health_title': "🥗 Health Analysis & Nutrition:",
        'cat_lbl': "Category:",
        'status_lbl': "Health Status:",
        'nutrients_lbl': "🧪 Nutrients & Ingredients:",
        'effect_lbl': "💡 Benefits & Health Impact:",
        'time_lbl': "⏰ Best Time to Consume:",
        'buy_lbl': "🛒 Best Time to Buy:"
    }
}

lang = st.session_state.lang
t = TEXTS[lang]

st.button(t['lang_btn'], on_click=toggle_language)
st.title(t['title'])
st.caption(t['subtitle'])

uploaded_file = st.file_uploader(t['upload_label'], type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, use_container_width=True)

    with st.spinner("Analyzing image features..."):
        file_name = uploaded_file.name.lower()
        
        # Color distribution analysis
        img_np = np.array(image.resize((100, 100)))
        r, g, b = img_np[:, :, 0], img_np[:, :, 1], img_np[:, :, 2]

        is_red_or_fruit = np.mean((r > g) & (r > b)) > 0.18
        is_green = np.mean((g > r) & (g > b)) > 0.35
        is_white_packaging = np.mean((r > 190) & (g > 190) & (b > 190)) > 0.45

        fruit_keywords = ['fruit', 'strawberry', 'apple', 'banana', 'mango', 'فراولة', 'تفاح', 'موز', 'فواكه', 'garden']
        veg_keywords = ['veg', 'tomato', 'cucumber', 'خيار', 'طماطم', 'خضار']
        dairy_keywords = ['dairy', 'milk', 'yoghurt', 'yogurt', 'almarai', 'laban', 'cheese', 'لبن', 'زبادي', 'جبنة']

        if any(k in file_name for k in fruit_keywords) or (is_red_or_fruit and not is_white_packaging):
            cat_key = 'Fruits'
        elif any(k in file_name for k in veg_keywords) or (is_green and not is_white_packaging):
            cat_key = 'Vegetables'
        elif any(k in file_name for k in dairy_keywords) or is_white_packaging:
            cat_key = 'Dairy'
        else:
            cat_key = 'Fruits'

        labels_display = {
            'Fruits': "فواكه طازجة (Fruits)" if lang == 'ar' else "Fresh Fruits",
            'Vegetables': "خضروات طازجة (Vegetables)" if lang == 'ar' else "Fresh Vegetables",
            'Dairy': "زبادي ومنتجات ألبان (Dairy)" if lang == 'ar' else "Dairy / Yoghurt"
        }
        
        detected_label = labels_display[cat_key]

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
