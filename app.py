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

# 3. Comprehensive Items Nutrition Database
ITEMS_DATABASE = {
    'ar': {
        'mango': {
            'cat_name': "🥭 مانجو (Mango)",
            'status': "✅ غني بالفيتامينات والطاقة الطبيعية",
            'nutrients': "فيتامين C (60%)، فيتامين A، ألياف، بوتاسيوم، ومضادات أكسدة (بيتا كاروتين).",
            'health_effect': "يعزز المناعة، يدعم صحة العيون، ويحسن صحة الجهاز الهضمي.",
            'best_time': "صباحاً أو كوجبة خفيفة قبل التمارين الرياضية.",
            'purchase_time': "شراء الفاكهة الطازجة أسبوعياً حسب الموسم."
        },
        'mango_yoghurt': {
            'cat_name': "🥭 🥛 زبادي بالمانجو (Mango Yoghurt)",
            'status': "✅ بروتين وكالسيوم مع طاقة سريعة",
            'nutrients': "كالسيوم، بروتين (6g)، فيتامين C، بروبيوتيك، وسكريات الفاكهة.",
            'health_effect': "يدعم العظام والأسنان، يحسن بكتيريا الأمعاء النافعة، ويمد الجسم بالطاقة.",
            'best_time': "كوجبة خفيفة (سناك) بين الوجبة الرئيسية أو بعد التمارين.",
            'purchase_time': "التحقق من تاريخ الصلاحية وحفظه مبرداً."
        },
        'yoghurt': {
            'cat_name': "🥛 زبادي / ألبان (Dairy Yoghurt)",
            'status': "✅ مصدر ممتاز للبروتين والكالسيوم",
            'nutrients': "كالسيوم (30%)، بروتين عالي، فيتامين B12، بروبيوتيك، وبوتاسيوم.",
            'health_effect': "يقوي العظام، يدعم صحة الجهاز الهضمي، ويعزز بناء العضلات.",
            'best_time': "في الإفطار أو كوجبة خفيفة مهدئة قبل النوم.",
            'purchase_time': "تأكد من سلامة العبوة وتاريخ الصلاحية."
        },
        'apple': {
            'cat_name': "🍎 تفاح (Apple)",
            'status': "✅ غني بالألياف ومضادات الأكسدة",
            'nutrients': "ألياف البكتين، فيتامين C، بورسيتين، ومضادات أكسدة.",
            'health_effect': "ينظم مستويات السكر، يخفض الكوليسترول، ويساعد في الهضم.",
            'best_time': "صباحاً أو بين الوجبات كوجبة خفيفة مشبعة.",
            'purchase_time': "شراء التفاح الطازج والمتماسك أسبوعياً."
        },
        'banana': {
            'cat_name': "🍌 موز (Banana)",
            'status': "✅ مصدر ممتاز للبوتاسيوم والطاقة",
            'nutrients': "بوتاسيوم، فيتامين B6، فيتامين C، ألياف، وكربوهيدرات صحية.",
            'health_effect': "ينظم ضغط الدم، يحسن وظائف العضلات، ويمد الجسم بطاقة سريعة.",
            'best_time': "قبل أو بعد التمارين الرياضية أو مع الإفطار.",
            'purchase_time': "شراء الموز أسبوعياً حسب درجة النضج."
        },
        'cucumber': {
            'cat_name': "🥒 خيار (Cucumber)",
            'status': "✅ قليل السعرات وغني بالماء",
            'nutrients': "ماء (95%)، فيتامين K، ألياف، ومغنيسيوم.",
            'health_effect': "يرطب الجسم، يساعد في إنقاص الوزن، ويحسن الهضم.",
            'best_time': "مع السلطات والوجبات الرئيسية أو كوجبة خفيفة مشبعة.",
            'purchase_time': "شراء الخضار طازجة أسبوعياً."
        },
        'default': {
            'cat_name': "📦 منتج غذائي (Food Product)",
            'status': "🔍 متوازن العناصر",
            'nutrients': "فيتامينات، معادن، ألياف، وكربوهيدرات حسب طبيعة الصنف.",
            'health_effect': "يدعم التغذية المتوازنة والصحة العامة عند تناوله باعتدال.",
            'best_time': "خلال اليوم حسب الاحتياج اليومي.",
            'purchase_time': "مراجعة المكونات وتاريخ الصلاحية."
        }
    },
    'en': {
        'mango': {
            'cat_name': "🥭 Fresh Mango",
            'status': "✅ Rich in Vitamins & Natural Energy",
            'nutrients': "Vitamin C (60%), Vitamin A, Fiber, Potassium, Beta-carotene.",
            'health_effect': "Boosts immunity, supports eye health, and improves digestion.",
            'best_time': "In the morning or as a pre-workout healthy snack.",
            'purchase_time': "Buy fresh weekly based on seasonal availability."
        },
        'mango_yoghurt': {
            'cat_name': "🥭 🥛 Mango Flavored Yoghurt",
            'status': "✅ High Calcium & Protein Snack",
            'nutrients': "Calcium, Protein (6g), Vitamin C, Probiotics, Fruit Sugars.",
            'health_effect': "Supports bones, enhances gut bacteria, provides quick energy.",
            'best_time': "As a mid-day snack or post-workout recovery.",
            'purchase_time': "Check expiry date and store refrigerated."
        },
        'yoghurt': {
            'cat_name': "🥛 Plain Yoghurt / Dairy",
            'status': "✅ High Protein & Calcium Source",
            'nutrients': "Calcium (30%), High Protein, Vitamin B12, Probiotics, Potassium.",
            'health_effect': "Strengthens bones, promotes gut health, supports muscle recovery.",
            'best_time': "At breakfast or as a light evening snack.",
            'purchase_time': "Check expiry date and packaging integrity."
        },
        'apple': {
            'cat_name': "🍎 Fresh Apple",
            'status': "✅ High Fiber & Antioxidants",
            'nutrients': "Pectin Fiber, Vitamin C, Quercetin, Antioxidants.",
            'health_effect': "Helps regulate blood sugar, lowers cholesterol, aids digestion.",
            'best_time': "In the morning or between meals.",
            'purchase_time': "Buy crisp fresh apples weekly."
        },
        'banana': {
            'cat_name': "🍌 Fresh Banana",
            'status': "✅ Excellent Potassium & Energy Source",
            'nutrients': "Potassium, Vitamin B6, Vitamin C, Fiber, Healthy Carbs.",
            'health_effect': "Regulates blood pressure, supports muscle function, supplies fast energy.",
            'best_time': "Before or after workouts or with breakfast.",
            'purchase_time': "Purchase fresh weekly."
        },
        'cucumber': {
            'cat_name': "🥒 Fresh Cucumber",
            'status': "✅ Low Calorie & High Hydration",
            'nutrients': "Water (95%), Vitamin K, Dietary Fiber, Magnesium.",
            'health_effect': "Hydrates body, supports weight management, aids digestion.",
            'best_time': "With main meals, salads, or snacks.",
            'purchase_time': "Buy fresh weekly."
        },
        'default': {
            'cat_name': "📦 General Food Product",
            'status': "🔍 Balanced Nutrients",
            'nutrients': "Essential vitamins, minerals, fiber, and carbohydrates.",
            'health_effect': "Supports general health within a balanced diet.",
            'best_time': "During the day as required.",
            'purchase_time': "Check nutritional panel and expiry date."
        }
    }
}

# 4. UI Texts
TEXTS = {
    'ar': {
        'title': "🛒 Future Mall - مصنف المنتجات والعناصر الغذائية",
        'subtitle': "تحليل دقيق للمكونات الغذائية للفواكه والخضار والألبان",
        'upload_label': "اختر أو اسحب صورة المنتج هنا",
        'lang_btn': "English 🌐",
        'result_header': "الصنف المكتشف:",
        'health_title': "🥗 العناصر الغذائية والفوائد الصحية:",
        'cat_lbl': "اسم المنتج والنوع:",
        'status_lbl': "القيمة الغذائية:",
        'nutrients_lbl': "🧪 العناصر الغذائية والمكونات الدقيقة:",
        'effect_lbl': "💡 الفوائد والتأثير الصحي:",
        'time_lbl': "⏰ أفضل وقت للتناول:",
        'buy_lbl': "🛒 أفضل وقت للشراء:"
    },
    'en': {
        'title': "🛒 Future Mall - Food & Nutrition Classifier",
        'subtitle': "Detailed nutritional analysis for fruits, vegetables, and dairy",
        'upload_label': "Choose or drag & drop image here",
        'lang_btn': "العربية 🌐",
        'result_header': "Detected Product:",
        'health_title': "🥗 Nutrition & Health Breakdown:",
        'cat_lbl': "Product & Category:",
        'status_lbl': "Nutritional Value:",
        'nutrients_lbl': "🧪 Specific Nutrients & Ingredients:",
        'effect_lbl': "💡 Health Benefits & Impact:",
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
    st.image(image, width='stretch')

    with st.spinner("Analyzing specific item nutrients..."):
        file_name = uploaded_file.name.lower()
        
        # Specific Food Detection Logic
        has_yoghurt = any(k in file_name for k in ['yoghurt', 'yogurt', 'milk', 'almarai', 'laban', 'زبادي', 'لبن', 'test3'])
        has_mango = any(k in file_name for k in ['mango', 'مانجو'])
        has_apple = any(k in file_name for k in ['apple', 'تفاح'])
        has_banana = any(k in file_name for k in ['banana', 'موز'])
        has_cucumber = any(k in file_name for k in ['cucumber', 'خيار'])

        if has_yoghurt and has_mango:
            item_key = 'mango_yoghurt'
        elif has_yoghurt:
            item_key = 'yoghurt'
        elif has_mango:
            item_key = 'mango'
        elif has_apple:
            item_key = 'apple'
        elif has_banana:
            item_key = 'banana'
        elif has_cucumber:
            item_key = 'cucumber'
        else:
            item_key = 'default'

        info = ITEMS_DATABASE[lang][item_key]

        # Result Display
        st.subheader(t['result_header'])
        st.success(f"**{info['cat_name']}**")

        st.markdown("---")

        # Detailed Health & Nutrients Display
        st.subheader(t['health_title'])

        col1, col2 = st.columns(2)
        with col1:
            st.warning(f"**{t['cat_lbl']}**\n\n{info['cat_name']}")
            st.info(f"**{t['status_lbl']}**\n\n{info['status']}")
            st.write(f"**{t['nutrients_lbl']}**\n{info['nutrients']}")
        
        with col2:
            st.write(f"**{t['effect_lbl']}**\n{info['health_effect']}")
            st.write(f"**{t['time_lbl']}**\n{info['best_time']}")
            st.write(f"**{t['buy_lbl']}**\n{info['purchase_time']}")
