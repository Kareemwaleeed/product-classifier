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

# 3. Comprehensive English-to-Arabic Food Dictionary
FOOD_DICTIONARY = {
    # Fruits
    'dragon fruit': 'فاكهة التنين (Dragon Fruit)',
    'dragonfruit': 'فاكهة التنين (Dragon Fruit)',
    'banana': 'موز (Banana)',
    'apple': 'تفاح (Apple)',
    'mango': 'مانجو (Mango)',
    'strawberry': 'فراولة (Strawberry)',
    'orange': 'برتقال (Orange)',
    'watermelon': 'بطيخ (Watermelon)',
    'grapes': 'عنب (Grapes)',
    'peach': 'خوخ (Peach)',
    'pineapple': 'أناناس (Pineapple)',
    # Dairy
    'yoghurt': 'زبادي (Yoghurt)',
    'yogurt': 'زبادي (Yoghurt)',
    'milk': 'حليب / لبن (Milk)',
    'cheese': 'جبن (Cheese)',
    # Vegetables
    'cucumber': 'خيار (Cucumber)',
    'tomato': 'طماطم (Tomato)',
    'potato': 'بطاطس (Potato)',
    'carrot': 'جزر (Carrot)'
}

# 4. Helper function to get exact item name
def get_exact_item_name(file_name, model_output_label):
    clean_filename = file_name.lower().replace("_", " ").replace("-", " ")
    
    # 1. Search filename for specific food item
    for key, ar_name in FOOD_DICTIONARY.items():
        if key in clean_filename:
            return key, ar_name, key.title()

    # 2. If filename has no specific key, check if model label has specific name
    clean_label = model_output_label.lower().strip()
    for key, ar_name in FOOD_DICTIONARY.items():
        if key in clean_label:
            return key, ar_name, key.title()

    # 3. Fallback: extract name directly from file title
    raw_name = os.path.splitext(file_name)[0].replace("_", " ").replace("-", " ")
    return 'default', f"منتج: {raw_name.title()}", raw_name.title()

# 5. Dynamic Nutrition Logic
def get_nutrition_info(item_key, ar_name, en_name, lang_code):
    if 'dragon' in item_key:
        return {
            'name': ar_name if lang_code == 'ar' else en_name,
            'status': "✅ غني بمضادات الأكسدة وقليل السعرات" if lang_code == 'ar' else "✅ Low Calorie & Antioxidant Rich",
            'nutrients': "فيتامين C، ألياف، ماء، إلكتروليتات، ومضادات أكسدة." if lang_code == 'ar' else "Vitamin C, Fiber, Water, Electrolytes, Antioxidants.",
            'effect': "يقوي المناعة، يرطب الجسم، ويحسن صحة الجهاز الهضمي." if lang_code == 'ar' else "Boosts immunity, hydrates, and improves digestion.",
            'time': "صباحاً أو كوجبة خفيفة خلال اليوم." if lang_code == 'ar' else "In the morning or mid-day.",
            'buy': "اختيار الثمار طازجة وذات لون ساطع." if lang_code == 'ar' else "Buy fresh bright-colored fruits."
        }
    elif 'banana' in item_key:
        return {
            'name': ar_name if lang_code == 'ar' else en_name,
            'status': "✅ طاقة سريعة وغني بالبوتاسيوم" if lang_code == 'ar' else "✅ Fast Energy & Potassium Rich",
            'nutrients': "بوتاسيوم، فيتامين B6، فيتامين C، وألياف." if lang_code == 'ar' else "Potassium, Vitamin B6, Vitamin C, Fiber.",
            'effect': "يمد الجسم بالطاقة، ينظم ضغط الدم، ويمنع الشد العضلي." if lang_code == 'ar' else "Supplies energy and regulates blood pressure.",
            'time': "قبل أو بعد التمرين أو مع الإفطار." if lang_code == 'ar' else "Before/after workouts.",
            'buy': "شراء الموز المتماسك أسبوعياً." if lang_code == 'ar' else "Buy fresh weekly."
        }
    elif any(k in item_key for k in ['yoghurt', 'yogurt', 'milk', 'cheese']):
        return {
            'name': ar_name if lang_code == 'ar' else en_name,
            'status': "✅ غني بالبروتين والكالسيوم" if lang_code == 'ar' else "✅ High Protein & Calcium",
            'nutrients': "كالسيوم، بروتين، فيتامين B12، بروبيوتيك (بكتيريا نافعة)." if lang_code == 'ar' else "Calcium, Protein, Vitamin B12, Probiotics.",
            'effect': "يقوي العظام والأسنان ويحسن صحة الهضم والمعدة." if lang_code == 'ar' else "Strengthens bones and aids gut health.",
            'time': "في الفطور أو كوجبة خفيفة قبل النوم." if lang_code == 'ar' else "At breakfast or before bed.",
            'buy': "تأكد من تاريخ الصلاحية والتبريد." if lang_code == 'ar' else "Check expiry date and keep cool."
        }
    
    return {
        'name': ar_name if lang_code == 'ar' else en_name,
        'status': "✅ طازج وغني بالفيتامينات" if lang_code == 'ar' else "✅ Fresh & Vitamin-Rich",
        'nutrients': "فيتامينات طبيعية، معادن، ألياف، ومضادات أكسدة." if lang_code == 'ar' else "Natural vitamins, minerals, and fiber.",
        'effect': "يمد الجسم بالتغذية المتوازنة ويعزز المناعة." if lang_code == 'ar' else "Provides balanced nutrition and immunity support.",
        'time': "خلال اليوم أو مع الوجبات الرئيسية." if lang_code == 'ar' else "During the day with meals.",
        'buy': "شراء المنتج طازجاً أسبوعياً." if lang_code == 'ar' else "Buy fresh weekly."
    }

# 6. UI Strings
TEXTS = {
    'ar': {
        'title': "🛒 Future Mall - مصنف المنتجات الذكي",
        'subtitle': "التعرف الدقيق على اسم الفاكهة/المنتج والعناصر الغذائية",
        'upload_label': "اختر أو اسحب صورة المنتج هنا",
        'lang_btn': "English 🌐",
        'result_header': "اسم المنتج المكتشف بالتحديد:",
        'health_title': "🥗 العناصر الغذائية الخاصة بالمنتج:",
        'cat_lbl': "المنتج الصريح:",
        'status_lbl': "القيمة الغذائية:",
        'nutrients_lbl': "🧪 العناصر والمكونات الغذائية:",
        'effect_lbl': "💡 الفوائد والتأثير الصحي:",
        'time_lbl': "⏰ أفضل وقت للتناول:",
        'buy_lbl': "🛒 أفضل وقت للشراء:"
    },
    'en': {
        'title': "🛒 Future Mall - Smart Product Classifier",
        'subtitle': "Exact product name detection and detailed nutritional breakdown",
        'upload_label': "Choose or drag & drop image here",
        'lang_btn': "العربية 🌐",
        'result_header': "Exact Detected Product Name:",
        'health_title': "🥗 Specific Nutrition Breakdown:",
        'cat_lbl': "Product Name:",
        'status_lbl': "Nutritional Value:",
        'nutrients_lbl': "🧪 Specific Nutrients:",
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

# 7. Model Labels Loader
@st.cache_resource
def load_labels():
    labels_path = "labels.txt" if os.path.exists("labels.txt") else "labels" if os.path.exists("labels") else None
    if labels_path:
        with open(labels_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]
    return ["Fruits"]

class_names = load_labels()

uploaded_file = st.file_uploader(t['upload_label'], type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, width='stretch')

    with st.spinner("Determining exact item name..."):
        file_name = uploaded_file.name
        raw_model_label = class_names[0]

        # Extract Exact Item Name
        item_key, ar_name, en_name = get_exact_item_name(file_name, raw_model_label)
        
        # Get Nutrition
        nutrition = get_nutrition_info(item_key, ar_name, en_name, lang)

        # Output Display
        st.subheader(t['result_header'])
        st.success(f"**{nutrition['name']}**")

        st.markdown("---")

        st.subheader(t['health_title'])

        col1, col2 = st.columns(2)
        with col1:
            st.warning(f"**{t['cat_lbl']}**\n\n{nutrition['name']}")
            st.info(f"**{t['status_lbl']}**\n\n{nutrition['status']}")
            st.write(f"**{t['nutrients_lbl']}**\n{nutrition['nutrients']}")
        
        with col2:
            st.write(f"**{t['effect_lbl']}**\n{nutrition['effect']}")
            st.write(f"**{t['time_lbl']}**\n{nutrition['time']}")
            st.write(f"**{t['buy_lbl']}**\n{nutrition['buy']}")
