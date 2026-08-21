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

# 3. بيانات الأقسام الصحية
CATEGORIES_INFO = {
    'ar': {
        'Dairy': {
            'cat_name': "🥛 ألبان ومنتجات الألبان (Dairy)",
            'status': "✅ غني بالبروتين والكالسيوم",
            'nutrients': "كالسيوم، بروتين، فيتامين B12، بروبيوتيك، وبوتاسيوم.",
            'health_effect': "يعزز صحة العظام والأسنان، ويحسن الهضم والمناعة.",
            'best_time': "في الفطور، أو كوجبة خفيفة ليلاً.",
            'purchase_time': "تأكد من تاريخ الصلاحية والحفظ مبرداً."
        },
        'Fruits': {
            'cat_name': "🍎 فواكه طازجة (Fruits)",
            'status': "✅ صحي ومفيد جداً",
            'nutrients': "فيتامين C، ألياف، مضادات أكسدة، وسكريات طبيعية.",
            'health_effect': "يمد الجسم بالطاقة المناسبة ويحسن صحة البشرة والهضم.",
            'best_time': "صباحاً أو بين الوجبات الرئيسية.",
            'purchase_time': "شراء الفواكه الطازجة أسبوعياً."
        },
        'Vegetables': {
            'cat_name': "🥦 خضروات (Vegetables)",
            'status': "✅ قليل السعرات وغني بالألياف",
            'nutrients': "فيتامين A، فيتامين K، حمض الفوليك، ومعادن.",
            'health_effect': "ينظم مستويات السكر في الدم ويساعد في إنقاص الوزن.",
            'best_time': "مع الوجبات الرئيسية (الغداء والعشاء).",
            'purchase_time': "تفضل طازجة أسبوعياً."
        },
        'Default': {
            'cat_name': "📦 منتج عام",
            'status': "🔍 خيار متوازن",
            'nutrients': "عناصر غذائية متنوعة حسب طبيعة المنتج.",
            'health_effect': "يُنصح باستهلاكه باعتدال ضمن نظام غذائي متوازن.",
            'best_time': "خلال اليوم حسب الحاجة.",
            'purchase_time': "فحص تاريخ الإنتاج والمكونات."
        }
    },
    'en': {
        'Dairy': {
            'cat_name': "🥛 Dairy Products",
            'status': "✅ Rich in Calcium & Protein",
            'nutrients': "Calcium, Protein, Vitamin B12, Probiotics, Potassium.",
            'health_effect': "Strengthens bones and teeth, improves gut health.",
            'best_time': "At breakfast or as a light evening snack.",
            'purchase_time': "Check expiration date and keep refrigerated."
        },
        'Fruits': {
            'cat_name': "🍎 Fresh Fruits",
            'status': "✅ Highly Nutritious",
            'nutrients': "Vitamin C, Fiber, Antioxidants, Natural Fructose.",
            'health_effect': "Boosts energy and improves overall health.",
            'best_time': "In the morning or between meals.",
            'purchase_time': "Buy fresh weekly."
        },
        'Vegetables': {
            'cat_name': "🥦 Vegetables",
            'status': "✅ Fiber-Rich & Low Calorie",
            'nutrients': "Vitamin A, Vitamin K, Folic Acid, Minerals.",
            'health_effect': "Supports weight management and digestion.",
            'best_time': "With lunch or dinner.",
            'purchase_time': "Purchase fresh weekly."
        },
        'Default': {
            'cat_name': "📦 General Product",
            'status': "🔍 Balanced Choice",
            'nutrients': "Varied nutrients based on the product.",
            'health_effect': "Consume moderately.",
            'best_time': "As needed during the day.",
            'purchase_time': "Check packaging and expiration."
        }
    }
}

# 4. النصوص
TEXTS = {
    'ar': {
        'title': "🛒 Future Mall - مصنف المنتجات الذكي",
        'subtitle': "تصنيف دقيق للألبان والفواكه والخضروات",
        'upload_label': "اختر أو اسحب صورة المنتج هنا",
        'lang_btn': "English 🌐",
        'model_error': "تأكد من وجود ملف model.tflite وملف labels.txt في المستودع",
        'result_header': "نتيجة التصنيف:",
        'confidence': "نسبة الثقة:",
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
        'subtitle': "Accurate product classification with nutritional breakdown",
        'upload_label': "Choose or drag & drop a product image here",
        'lang_btn': "العربية 🌐",
        'model_error': "Ensure model.tflite and labels.txt exist in the repository",
        'result_header': "Classification Result:",
        'confidence': "Confidence Score:",
        'health_title': "🥗 Health Analysis & Category Details:",
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

# 5. تحميل نموذج TFLite
@st.cache_resource
def load_tflite_model():
    model_path = "model.tflite"
    labels_path = "labels.txt" if os.path.exists("labels.txt") else "labels" if os.path.exists("labels") else None

    if os.path.exists(model_path) and labels_path:
        interpreter = tflite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        with open(labels_path, "r", encoding="utf-8") as f:
            class_names = [line.strip() for line in f.readlines()]
        return interpreter, class_names
    return None, None

interpreter, class_names = load_tflite_model()

if interpreter is None or class_names is None:
    st.error(t['model_error'])
else:
    uploaded_file = st.file_uploader(t['upload_label'], type=["jpg", "jpeg", "png", "webp"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, width='stretch')

        # معالجة الصورة
        size = (224, 224)
        image_resized = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image_resized, dtype=np.float32)
        normalized_image = (image_array / 127.5) - 1.0
        input_data = np.expand_dims(normalized_image, axis=0)

        # إجراء التوقع بالـ TFLite
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        output_data = interpreter.get_tensor(output_details[0]['index'])
        probs = output_data[0]

        index = int(np.argmax(probs))
        raw_class_name = class_names[index]
        clean_class_name = " ".join(raw_class_name.split()[1:]) if raw_class_name.split()[0].isdigit() else raw_class_name
        confidence_score = float(probs[index]) * 100

        # عرض النتيجة
        st.subheader(t['result_header'])
        st.success(f"**{clean_class_name}**")
        st.write(f"{t['confidence']} **{confidence_score:.2f}%**")

        st.markdown("---")

        # ربط الصنف بالأقسام الصحيحة
        st.subheader(t['health_title'])
        name_lower = clean_class_name.lower()

        if any(k in name_lower for k in ['milk', 'yoghurt', 'yogurt', 'cheese', 'dairy', 'laban', 'زبادي', 'لبن', 'جبنة', 'ألبان']):
            cat_key = 'Dairy'
        elif any(k in name_lower for k in ['apple', 'banana', 'orange', 'fruit', 'grape', 'strawberry', 'فاكهة', 'فواكه', 'تفاح', 'موز']):
            cat_key = 'Fruits'
        elif any(k in name_lower for k in ['vegetable', 'tomato', 'cucumber', 'potato', 'خضار', 'خضروات', 'طماطم', 'خيار']):
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
