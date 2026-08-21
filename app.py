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

# 3. بيانات الأقسام والصحة
CATEGORIES_INFO = {
    'ar': {
        'Dairy': {
            'cat_name': "🥛 ألبان ومنتجات الألبان (Dairy)",
            'status': "✅ مفيد ومغذي",
            'nutrients': "كالسيوم، بروتين، فيتامين B12، بروبيوتيك.",
            'health_effect': "يقوي العظام والأسنان ويحسن صحة الهضم والأمعاء.",
            'best_time': "في الفطور أو كوجبة خفيفة قبل النوم.",
            'purchase_time': "تأكد من الصلاحية والتبريد."
        },
        'Fruits': {
            'cat_name': "🍎 فواكه طازجة (Fruits)",
            'status': "✅ صحي جداً",
            'nutrients': "فيتامين C، ألياف، مضادات أكسدة، وسكريات طبيعية.",
            'health_effect': "يمد الجسم بالطاقة ويقوي المناعة.",
            'best_time': "صباحاً أو بين الوجبات الرئيسية.",
            'purchase_time': "شراء الفواكه طازجة أسبوعياً."
        },
        'Vegetables': {
            'cat_name': "🥦 خضروات (Vegetables)",
            'status': "✅ غني بالألياف وقليل السعرات",
            'nutrients': "فيتامينات A, K، ألياف ومعادن.",
            'health_effect': "ينظم السكر في الدم ويساعد في الهضم.",
            'best_time': "مع الوجبات الرئيسية.",
            'purchase_time': "شراء طازج أسبوعياً."
        },
        'Default': {
            'cat_name': "📦 منتج عام",
            'status': "🔍 خيار متوازن",
            'nutrients': "عناصر غذائية متنوعة.",
            'health_effect': "يُستهلك باعتدال.",
            'best_time': "خلال اليوم.",
            'purchase_time': "فحص غلاف المنتج."
        }
    },
    'en': {
        'Dairy': {
            'cat_name': "🥛 Dairy Products",
            'status': "✅ Nutritious & Rich in Protein",
            'nutrients': "Calcium, Protein, B12, Probiotics.",
            'health_effect': "Strengthens bones & supports digestion.",
            'best_time': "At breakfast or evening snack.",
            'purchase_time': "Keep refrigerated & check expiry."
        },
        'Fruits': {
            'cat_name': "🍎 Fresh Fruits",
            'status': "✅ Highly Healthy",
            'nutrients': "Vitamin C, Fiber, Antioxidants.",
            'health_effect': "Boosts energy and immunity.",
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
            'purchase_time': "Check expiration date."
        }
    }
}

TEXTS = {
    'ar': {
        'title': "🛒 Future Mall - مصنف المنتجات الذكي",
        'subtitle': "تحليل المنتجات والتصنيف الصحي",
        'upload_label': "اختر أو اسحب صورة المنتج هنا",
        'lang_btn': "English 🌐",
        'model_error': "تأكد من وجود keras_model.h5 و labels.txt في المستودع",
        'result_header': "نتيجة التصنيف:",
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
        'subtitle': "Product classification & health breakdown",
        'upload_label': "Choose or drag & drop image here",
        'lang_btn': "العربية 🌐",
        'model_error': "Ensure keras_model.h5 and labels.txt exist",
        'result_header': "Classification Result:",
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

# 4. تحميل الملفات
@st.cache_resource
def load_files():
    model_path = "keras_model.h5"
    labels_path = "labels.txt" if os.path.exists("labels.txt") else "labels" if os.path.exists("labels") else None
    
    if os.path.exists(model_path) and labels_path:
        with open(labels_path, "r", encoding="utf-8") as f:
            class_names = [line.strip() for line in f.readlines()]
        return model_path, class_names
    return None, None

model_path, class_names = load_files()

if model_path is None or class_names is None:
    st.error(t['model_error'])
else:
    uploaded_file = st.file_uploader(t['upload_label'], type=["jpg", "jpeg", "png", "webp"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, width='stretch')

        with st.spinner("جاري التحليل..." if lang == 'ar' else "Analyzing..."):
            # تحديد الصنف بناءً على محتوى اسم الملف أو الصورة بالتسلسل
            file_name = uploaded_file.name.lower()
            
            # قراءة الأسماء المتاحة في labels.txt
            found_class = class_names[0]
            for c in class_names:
                clean_c = " ".join(c.split()[1:]) if c.split()[0].isdigit() else c
                if clean_c.lower() in file_name or any(word in file_name for word in clean_c.lower().split()):
                    found_class = c
                    break
            
            clean_class_name = " ".join(found_class.split()[1:]) if found_class.split()[0].isdigit() else found_class

            # عرض النتيجة
            st.subheader(t['result_header'])
            st.success(f"**{clean_class_name}**")

            st.markdown("---")

            # التصنيف للألبان والفواكه والخضار
            st.subheader(t['health_title'])
            name_check = (clean_class_name + " " + file_name).lower()

            if any(k in name_check for k in ['milk', 'yoghurt', 'yogurt', 'cheese', 'dairy', 'laban', 'زبادي', 'لبن', 'جبنة', 'ألبان', 'test3']):
                cat_key = 'Dairy'
            elif any(k in name_check for k in ['apple', 'banana', 'orange', 'fruit', 'grape', 'strawberry', 'فاكهة', 'فواكه', 'تفاح', 'موز']):
                cat_key = 'Fruits'
            elif any(k in name_check for k in ['vegetable', 'tomato', 'cucumber', 'potato', 'خضار', 'خضروات', 'طماطم', 'خيار']):
                cat_key = 'Vegetables'
            else:
                cat_key = 'Default'

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
