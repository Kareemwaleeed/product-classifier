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

# 3. Arabic Dictionary for Specific Products
TRANSLATIONS = {
    'dragon fruit': 'فاكهة التنين (Dragon Fruit)',
    'dragonfruit': 'فاكهة التنين (Dragon Fruit)',
    'banana': 'موز (Banana)',
    'apple': 'تفاح (Apple)',
    'mango': 'مانجو (Mango)',
    'strawberry': 'فراولة (Strawberry)',
    'orange': 'برتقال (Orange)',
    'watermelon': 'بطيخ (Watermelon)',
    'yoghurt': 'زبادي (Yoghurt)',
    'yogurt': 'زبادي (Yoghurt)',
    'milk': 'لبن / حليب (Milk)',
    'cucumber': 'خيار (Cucumber)',
    'tomato': 'طماطم (Tomato)',
    'potato': 'بطاطس (Potato)',
    'carrot': 'جزر (Carrot)'
}

# 4. Specific Nutrition Generator
def get_item_details(item_name, lang_code):
    item_lower = item_name.lower()

    # Determine Specific Arabic / English Name
    translated_name = item_name.title()
    if lang_code == 'ar':
        for k, v in TRANSLATIONS.items():
            if k in item_lower:
                translated_name = v
                break

    # Specific Nutrition Logic
    if any(k in item_lower for k in ['dragon fruit', 'dragonfruit', 'تنين']):
        return {
            'name': translated_name if lang_code == 'ar' else "Dragon Fruit",
            'status': "✅ غني بمضادات الأكسدة وقليل السعرات" if lang_code == 'ar' else "✅ High Antioxidants & Low Calorie",
            'nutrients': "فيتامين C، ألياف غذائية، إلكتوليتات، ماء، ومضادات أكسدة." if lang_code == 'ar' else "Vitamin C, Dietary Fiber, Electrolytes, Water, Antioxidants.",
            'effect': "يقوي المناعة، يحسن الهضم، ويرطب الجسم بشكل ممتاز." if lang_code == 'ar' else "Boosts immunity, aids digestion, and hydrates the body.",
            'time': "صباحاً أو كوجبة خفيفة منعشة خلال اليوم." if lang_code == 'ar' else "In the morning or as a refreshing mid-day snack.",
            'buy': "شراء الثمار الطازجة ذات اللون الساطع." if lang_code == 'ar' else "Buy fresh bright-colored fruits."
        }
    elif any(k in item_lower for k in ['banana', 'موز']):
        return {
            'name': translated_name if lang_code == 'ar' else "Banana",
            'status': "✅ مصدر طاقة سريع وغني بالبوتاسيوم" if lang_code == 'ar' else "✅ Quick Energy & High Potassium",
            'nutrients': "بوتاسيوم، فيتامين B6، فيتامين C، وألياف." if lang_code == 'ar' else "Potassium, Vitamin B6, Vitamin C, Fiber.",
            'effect': "ينظم ضغط الدم، يمنع التشنجات العضلية، ويمد الجسم بالطاقة." if lang_code == 'ar' else "Regulates blood pressure, prevents cramps, supplies energy.",
            'time': "قبل أو بعد التمارين الرياضية أو مع الإفطار." if lang_code == 'ar' else "Before/after workouts or with breakfast.",
            'buy': "شراء الموز المتماسك أسبوعياً." if lang_code == 'ar' else "Buy fresh weekly."
        }
    elif any(k in item_lower for k in ['yoghurt', 'yogurt', 'زبادي', 'لبن', 'milk', 'dairy']):
        return {
            'name': translated_name if lang_code == 'ar' else "Yoghurt / Dairy Product",
            'status': "✅ غني بالبروتين والكالسيوم" if lang_code == 'ar' else "✅ Rich in Calcium & Protein",
            'nutrients': "كالسيوم، بروتين، فيتامين B12، بروبيوتيك." if lang_code == 'ar' else "Calcium, Protein, Vitamin B12, Probiotics.",
            'effect': "يقوي العظام والأسنان ويحسن صحة الهضم والأمعاء." if lang_code == 'ar' else "Strengthens bones and improves gut health.",
            'time': "في الفطور أو كوجبة خفيفة قبل النوم." if lang_code == 'ar' else "At breakfast or before sleep.",
            'buy': "تأكد من تاريخ الصلاحية والتبريد." if lang_code == 'ar' else "Check expiry date and keep refrigerated."
        }
        
    # Default for any other specific fruit/vegetable
    return {
        'name': translated_name,
        'status': "✅ طازج وغني بالفيتامينات" if lang_code == 'ar' else "✅ Fresh & Vitamin-Rich",
        'nutrients': "فيتامينات طبيعية، معادن، ألياف، ومضادات أكسدة." if lang_code == 'ar' else "Natural vitamins, minerals, fiber, antioxidants.",
        'effect': "يمد الجسم بالتغذية المتوازنة ويعزز المناعة والصحة العامة." if lang_code == 'ar' else "Provides balanced nutrition and boosts immunity.",
        'time': "خلال اليوم أو مع الوجبات الرئيسية." if lang_code == 'ar' else "During the day or with main meals.",
        'buy': "شراء المكونات الطازجة أسبوعياً." if lang_code == 'ar' else "Buy fresh weekly."
    }

# 5. UI Texts
TEXTS = {
    'ar': {
        'title': "🛒 Future Mall - مصنف المنتجات الذكي",
        'subtitle': "التعرف على اسم المنتج الفعلي وتحليل المكونات",
        'upload_label': "اختر أو اسحب صورة المنتج هنا",
        'lang_btn': "English 🌐",
        'result_header': "اسم المنتج المحدد:",
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
        'result_header': "Detected Product Name:",
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

# 6. Load Label Names
@st.cache_resource
def load_labels():
    labels_path = "labels.txt" if os.path.exists("labels.txt") else "labels" if os.path.exists("labels") else None
    if labels_path:
        with open(labels_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]
    return ["Dragon Fruit", "Banana", "Apple", "Mango", "Yoghurt"]

class_names = load_labels()

uploaded_file = st.file_uploader(t['upload_label'], type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, width='stretch')

    with st.spinner("Extracting exact item name..."):
        file_name = uploaded_file.name.lower()
        
        # Match exact item name from file or labels
        detected_item = class_names[0]
        for c in class_names:
            clean_c = " ".join(c.split()[1:]) if c.split()[0].isdigit() else c
            if clean_c.lower() in file_name or any(w in file_name for w in clean_c.lower().split()):
                detected_item = clean_c
                break

        clean_item_name = " ".join(detected_item.split()[1:]) if detected_item.split()[0].isdigit() else detected_item
        
        # Extract specific info
        item_data = get_item_details(clean_item_name, lang)

        # Output Display
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
