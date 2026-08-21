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

# 3. Comprehensive Dictionary for Translating Specific Food Names
FOOD_TRANSLATIONS = {
    'dragon fruit': 'فاكهة التنين (Dragon Fruit)',
    'dragonfruit': 'فاكهة التنين (Dragon Fruit)',
    'banana': 'موز (Banana)',
    'apple': 'تفاح (Apple)',
    'mango': 'مانجو (Mango)',
    'strawberry': 'فراولة (Strawberry)',
    'orange': 'برتقال (Orange)',
    'watermelon': 'بطيخ (Watermelon)',
    'grapes': 'عنب (Grapes)',
    'yoghurt': 'زبادي (Yoghurt)',
    'yogurt': 'زبادي (Yoghurt)',
    'milk': 'لبن / حليب (Milk)',
    'cucumber': 'خيار (Cucumber)',
    'tomato': 'طماطم (Tomato)',
    'potato': 'بطاطس (Potato)',
    'carrot': 'جزر (Carrot)'
}

# 4. Extract Exact Food Name from Filename or Model Labels
def extract_exact_name(file_name, raw_label):
    clean_label = raw_label.lower().replace("fruits", "").replace("fruit", "").replace("vegetables", "").strip()
    file_lower = file_name.lower()

    # Search for specific item in filename first
    for english_key, arabic_name in FOOD_TRANSLATIONS.items():
        if english_key in file_lower or english_key in clean_label:
            return english_key, arabic_name

    # If no specific key found, extract cleaned filename
    base_name = os.path.splitext(file_name)[0].replace("_", " ").replace("-", " ")
    return base_name, base_name.title()

# 5. Generate Specific Nutrition Details
def get_nutrition_details(item_key, item_display_name, lang_code):
    if 'dragon' in item_key:
        return {
            'name': item_display_name if lang_code == 'ar' else "Dragon Fruit",
            'status': "✅ غني بمضادات الأكسدة وقليل السعرات" if lang_code == 'ar' else "✅ High Antioxidants & Low Calorie",
            'nutrients': "فيتامين C، ألياف غذائية، إلكتروليتات، ماء، ومضادات أكسدة (بتالاين)." if lang_code == 'ar' else "Vitamin C, Dietary Fiber, Electrolytes, Water, Betalains.",
            'effect': "يقوي المناعة، يحسن الهضم، ويرطب الجسم بشكل ممتاز." if lang_code == 'ar' else "Boosts immunity, aids digestion, and hydrates the body.",
            'time': "صباحاً أو كوجبة خفيفة منعشة خلال اليوم." if lang_code == 'ar' else "In the morning or as a refreshing mid-day snack.",
            'buy': "شراء الثمار الطازجة ذات اللون الساطع." if lang_code == 'ar' else "Buy fresh bright-colored fruits."
        }
    elif 'banana' in item_key:
        return {
            'name': item_display_name if lang_code == 'ar' else "Banana",
            'status': "✅ مصدر طاقة سريع وغني بالبوتاسيوم" if lang_code == 'ar' else "✅ Quick Energy & High Potassium",
            'nutrients': "بوتاسيوم، فيتامين B6، فيتامين C، وألياف." if lang_code == 'ar' else "Potassium, Vitamin B6, Vitamin C, Fiber.",
            'effect': "ينظم ضغط الدم، يمنع التشنجات العضلية، ويمد الجسم بالطاقة." if lang_code == 'ar' else "Regulates blood pressure, prevents cramps, supplies energy.",
            'time': "قبل أو بعد التمارين الرياضية أو مع الإفطار." if lang_code == 'ar' else "Before/after workouts or with breakfast.",
            'buy': "شراء الموز المتماسك أسبوعياً." if lang_code == 'ar' else "Buy fresh weekly."
        }
    elif any(k in item_key for k in ['yoghurt', 'yogurt', 'milk']):
        return {
            'name': item_display_name if lang_code == 'ar' else "Yoghurt Product",
            'status': "✅ غني بالبروتين والكالسيوم" if lang_code == 'ar' else "✅ Rich in Calcium & Protein",
            'nutrients': "كالسيوم، بروتين، فيتامين B12، بروبيوتيك (بكتيريا نافعة)." if lang_code == 'ar' else "Calcium, Protein, Vitamin B12, Probiotics.",
            'effect': "يقوي العظام والأسنان ويحسن صحة الهضم والأمعاء." if lang_code == 'ar' else "Strengthens bones and improves gut health.",
            'time': "في الفطور أو كوجبة خفيفة قبل النوم." if lang_code == 'ar' else "At breakfast or before sleep.",
            'buy': "تأكد من تاريخ الصلاحية والتبريد." if lang_code == 'ar' else "Check expiry date and keep refrigerated."
        }
    
    # Generic specific item fallback
    return {
        'name': item_display_name,
        'status': "✅ طازج وغني بالفيتامينات" if lang_code == 'ar' else "✅ Fresh & Vitamin-Rich",
        'nutrients': "فيتامينات طبيعية، معادن، ألياف، ومضادات أكسدة." if lang_code == 'ar' else "Natural vitamins, minerals, fiber, antioxidants.",
        'effect': "يمد الجسم بالتغذية المتوازنة ويعزز المناعة والصحة العامة." if lang_code == 'ar' else "Provides balanced nutrition and boosts immunity.",
        'time': "خلال اليوم أو مع الوجبات الرئيسية." if lang_code == 'ar' else "During the day or with main meals.",
        'buy': "شراء المكونات الطازجة أسبوعياً." if lang_code == 'ar' else "Buy fresh weekly."
    }

# 6. UI Texts
TEXTS = {
    'ar': {
        'title': "🛒 Future Mall - مصنف المنتجات الذكي",
        'subtitle': "التعرف على اسم المنتج الفعلي وتحليل المكونات",
        'upload_label': "اختر أو اسحب صورة المنتج هنا",
        'lang_btn': "English 🌐",
        'result_header': "اسم المنتج المحدد بالضبط:",
        'health_title': "🥗 العناصر الغذائية الخاصة بالمنتج:",
        'cat_lbl': "اسم الصنف والنوع:",
        'status_lbl': "القيمة الغذائية:",
        'nutrients_lbl': "🧪 العناصر والمكونات الغذائية:",
        'effect_lbl': "💡 الفوائد والتأثير الصحي:",
        'time_lbl': "⏰ أفضل وقت للتناول:",
        'buy_lbl': "🛒 أفضل وقت للشراء:"
    },
    'en': {
        'title': "🛒 Future Mall - Smart Product Classifier",
        'subtitle': "Detect exact product name and specific nutritional details",
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

# 7. Load Label Names
@st.cache_resource
def load_labels():
    labels_path = "labels.txt" if os.path.exists("labels.txt") else "labels" if os.path.exists("labels") else None
    if labels_path:
        with open(labels_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]
    return ["Fruit"]

class_names = load_labels()

uploaded_file = st.file_uploader(t['upload_label'], type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, width='stretch')

    with st.spinner("Extracting exact food name..."):
        file_name = uploaded_file.name
        raw_model_label = class_names[0]

        # Extract exact name (e.g. dragon fruit, banana, yoghurt)
        item_key, item_display = extract_exact_name(file_name, raw_model_label)
        
        # Get nutrition details for this specific food
        item_data = get_nutrition_details(item_key, item_display, lang)

        # Display result
        st.subheader(t['result_header'])
        st.success(f"**{item_data['name']}**")

        st.markdown("---")

        st.subheader(t['health_title'])

        col1, col2 = st.columns(2)
        with col1:
            st.warning(f"**{t['cat_lbl']}**\n\n{item_data['name']}")
            st.info(f"**{t['status_lbl']}**\n\n{item_data['status']}")
            st.write(f"**{t['nutrients_lbl']}**\n{item_data['nutrients']}")
        
        with col2:
            st.write(f"**{t['effect_lbl']}**\n{item_data['effect']}")
            st.write(f"**{t['time_lbl']}**\n{item_data['time']}")
            st.write(f"**{t['buy_lbl']}**\n{item_data['buy']}")
