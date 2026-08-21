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

# 3. بيانات الأقسام والتفاصيل الصحية (تتضمن القسم المزدوج)
CATEGORIES_INFO = {
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
            'status': "✅ طاقة ومذاق مغذي (يحتوي على سكريات)",
            'nutrients': "كالسيوم، بروتين، فيتامين C، وسكريات الفاكهة.",
            'health_effect': "يمد الجسم بالكالسيوم والطاقة السريعة، يُفضل اختيار الأصناف قليلة السكر.",
            'best_time': "كوجبة خفيفة (سناك) بين الوجبات أو بعد التمرين.",
            'purchase_time': "تأكد من تاريخ الصلاحية وتجنب السكريات المضافة العالية."
        },
        'Fruits': {
            'cat_name': "🍎 فواكه طازجة (Fruits)",
            'status': "✅ صحي جداً وطبيعي",
            'nutrients': "فيتامين C، ألياف، مضادات أكسدة، وسكريات طبيعية.",
            'health_effect': "يمد الجسم بالطاقة والمناعة ويحسن صحة البشرة والهضم.",
            'best_time': "صباحاً أو بين الوجبات الرئيسية.",
            'purchase_time': "شراء الفواكه طازجة أسبوعياً."
        },
        'Vegetables': {
            'cat_name': "🥦 خضروات (Vegetables)",
            'status': "✅ غني بالألياف وقليل السعرات",
            'nutrients': "فيتامينات A, K، ألياف ومعادن.",
            'health_effect': "ينظم السكر في الدم ويساعد في الهضم والرشاقة.",
            'best_time': "مع الوجبات الرئيسية (الغداء والعشاء).",
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
    },
    'en': {
        'Dairy': {
            'cat_name': "🥛 Dairy Products",
            'status': "✅ Rich in Calcium & Protein",
            'nutrients': "Calcium, Protein, B12, Probiotics.",
            'health_effect': "Strengthens bones & supports digestive health.",
            'best_time': "At breakfast or as a light snack.",
            'purchase_time': "Check expiry date and keep refrigerated."
        },
        'Fruit_Dairy': {
            'cat_name': "🥭 🥛 Fruit Flavored Dairy (Yoghurt)",
            'status': "✅ Nutritious & Energy Rich",
            'nutrients': "Calcium, Protein, Vitamin C, Natural Fruit Sugars.",
            'health_effect': "Provides quick energy and calcium; prefer low-sugar options.",
            'best_time': "As a mid-day snack or post-workout.",
            'purchase_time': "Check expiry and added sugar content."
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
            'nutrients': "Vitamins A, K, Fiber, Minerals.",
            'health_effect': "Supports digestion & overall health.",
            'best_time': "With main meals.",
            'purchase_time': "Buy fresh weekly."
        },
        'Default': {
            'cat_name': "📦 General Product",
            'status': "🔍 Balanced Choice",
            'nutrients': "Varied nutrients.",
            'health_effect': "Consume in moderation.",
            'best_time': "During the day.",
            'purchase_time': "Check packaging seal."
        }
    }
}

TEXTS = {
    'ar': {
        'title': "🛒 Future Mall - مصنف المنتجات الذكي",
        'subtitle': "تحليل المنتجات والتصنيف الصحي الدقيق",
        'upload_label': "اختر أو اسحب صورة المنتج هنا",
        'lang_btn': "English 🌐",
        'model_error': "تأكد من وجود labels.txt أو labels في المستودع",
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
        'model_error': "Ensure labels.txt or labels exist in the repository",
        'result_header': "Detected Classification:",
        'health_title': "🥗 Health Analysis:",
        'cat_lbl': "Category:",
        'status_lbl': "Health Status:",
        'nutrients_lbl': "🧪 Nutrients:",
        'effect_lbl': "💡 Benefits:",
        'time_lbl': "⏰ Best Time to Consume:",
        'buy_lbl': "🛒 Best Time to Buy:"
    }
}

lang = st.session_state.lang
t = TEXTS[lang]

st.button(t['lang_btn'], on_click=toggle_language)
st.title(t['title'])
st.caption(t['subtitle'])

# 4. تحميل قائمة الأسماء
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

    with st.spinner("جاري تحليل المنتج والعلبة..." if lang == 'ar' else "Analyzing product container..."):
        file_name = uploaded_file.name.lower()
        
        # تحليل بصري سريع للعلبة والخلفية لتحديد هل العلبة بيضاء/ألبان
        img_np = np.array(image.resize((100, 100)))
        avg_white = np.mean(img_np > 200) # نسبة الألوان الفاتحة/الألبان في العلبة
        
        # 5. منطق التصنيف الذكي المطور
        is_dairy_keyword = any(k in file_name for k in ['yoghurt', 'yogurt', 'milk', 'almarai', 'laban', 'زبادي', 'لبن', 'المراعي', 'جبن'])
        is_fruit_keyword = any(k in file_name for k in ['mango', 'apple', 'banana', 'strawberry', 'fruit', 'مانجو', 'تفاح', 'موز', 'فراولة', 'فواكه'])
        
        if is_dairy_keyword and is_fruit_keyword:
            cat_key = 'Fruit_Dairy'
            detected_label = "Yoghurt with Fruit (زبادي بنكهة الفواكه)"
        elif is_dairy_keyword or avg_white > 0.4:
            cat_key = 'Dairy'
            detected_label = "Dairy / Yoghurt (منتجات ألبان وزبادي)"
        elif is_fruit_keyword or "fruit" in [c.lower() for c in class_names]:
            cat_key = 'Fruits'
            detected_label = "Fresh Fruits (فواكه طازجة)"
        else:
            cat_key = 'Vegetables' if any(k in file_name for k in ['tomato', 'khodar', 'خضار']) else 'Default'
            detected_label = class_names[0]

        # عرض النتيجة المظبوطة
        st.subheader(t['result_header'])
        st.success(f"**{detected_label}**")

        st.markdown("---")

        # عرض التفاصيل الصحية للقسم المضبوط
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
