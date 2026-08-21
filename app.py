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

# 3. Dynamic Nutrition Database Generator
def get_nutrition_details(product_name, lang_code):
    p_lower = product_name.lower()
    
    # Nutritional logic based on detected item
    if any(k in p_lower for k in ['yoghurt', 'yogurt', 'laban', 'milk', 'زبادي', 'لبن', 'ألبان']):
        if any(k in p_lower for k in ['mango', 'fruit', 'strawberry', 'apple', 'مانجو', 'فواكه', 'فراولة']):
            return {
                'cat': "🥛🥭 زبادي بنكهة الفواكه (Fruit Yoghurt)" if lang_code == 'ar' else "🥛🥭 Fruit Flavored Yoghurt",
                'status': "✅ بروتين وكالسيوم مع طاقة طبيعية" if lang_code == 'ar' else "✅ High Protein & Calcium Energy Snack",
                'nutrients': "بروتين، كالسيوم، فيتامين C، بروبيوتيك (بكتيريا نافعة)، وسكريات طبيعية." if lang_code == 'ar' else "Protein, Calcium, Vitamin C, Probiotics, Natural Fruit Sugars.",
                'effect': "يقوي العظام والأسنان، يحسن صحة الهضم والأمعاء، ويمد الجسم بالطاقة." if lang_code == 'ar' else "Supports bones and teeth, improves gut health, provides quick energy.",
                'time': "كوجبة خفيفة (سناك) بين الوجبات أو بعد التمارين الرياضية." if lang_code == 'ar' else "As a mid-day snack or post-workout.",
                'buy': "تأكد من تاريخ الصلاحية وحفظ المنتج مبرداً." if lang_code == 'ar' else "Check expiration date and keep refrigerated."
            }
        return {
            'cat': "🥛 زبادي / منتجات ألبان (Dairy Product)" if lang_code == 'ar' else "🥛 Dairy Yoghurt Product",
            'status': "✅ غني بالبروتين والكالسيوم" if lang_code == 'ar' else "✅ Rich in Calcium & Protein",
            'nutrients': "كالسيوم، بروتين عالي، فيتامين B12، بروبيوتيك، وبوتاسيوم." if lang_code == 'ar' else "Calcium, High Protein, Vitamin B12, Probiotics, Potassium.",
            'effect': "يعزز بناء العضلات، يقوي العظام، ويحسن عمل الجهاز الهضمي." if lang_code == 'ar' else "Strengthens bones, promotes gut bacteria, supports muscle recovery.",
            'time': "في الإفطار أو كوجبة خفيفة مهدئة قبل النوم." if lang_code == 'ar' else "At breakfast or as a light evening snack.",
            'buy': "فحص سلامة العبوة وتاريخ الصلاحية." if lang_code == 'ar' else "Check packaging seal and expiry date."
        }
    
    elif any(k in p_lower for k in ['fruit', 'apple', 'banana', 'mango', 'orange', 'strawberry', 'grape', 'فاكهة', 'فواكه', 'تفاح', 'موز', 'مانجو', 'برتقال']):
        return {
            'cat': f"🍎 فاكهة طازجة ({product_name.title()})" if lang_code == 'ar' else f"🍎 Fresh Fruit ({product_name.title()})",
            'status': "✅ غني بالفيتامينات والألياف الطبيعية" if lang_code == 'ar' else "✅ Rich in Vitamins & Natural Fiber",
            'nutrients': "فيتامين C، ألياف غذائية، مضادات أكسدة، وسكريات الفواكه الطبيعية." if lang_code == 'ar' else "Vitamin C, Dietary Fiber, Antioxidants, Natural Fructose.",
            'effect': "يعزز مناعة الجسم، يمد الجسم بالطاقة، ويحسن صحة البشرة والهضم." if lang_code == 'ar' else "Boosts immunity, improves skin health, and aids digestion.",
            'time': "صباحاً أو بين الوجبات الرئيسية كوجبة صحية خفيفة." if lang_code == 'ar' else "In the morning or between main meals.",
            'buy': "شراء الفواكه الطازجة أسبوعياً حسب الموسم." if lang_code == 'ar' else "Buy fresh weekly based on season."
        }
        
    elif any(k in p_lower for k in ['vegetable', 'cucumber', 'tomato', 'potato', 'carrot', 'خضار', 'خضروات', 'خيار', 'طماطم', 'جزر']):
        return {
            'cat': f"🥦 خضروات طازجة ({product_name.title()})" if lang_code == 'ar' else f"🥦 Fresh Vegetables ({product_name.title()})",
            'status': "✅ قليل السعرات وغني بالمعادن والألياف" if lang_code == 'ar' else "✅ Low Calorie & Fiber-Rich",
            'nutrients': "فيتامين A، فيتامين K، حمض الفوليك، معادن أساسية، وألياف." if lang_code == 'ar' else "Vitamin A, Vitamin K, Folic Acid, Minerals, Fiber.",
            'effect': "ينظم مستويات السكر، يحمي القلب، ويساعد في تنظيم الوزن." if lang_code == 'ar' else "Regulates blood sugar, supports heart health, assists weight control.",
            'time': "مع الوجبات الرئيسية (الغداء والعشاء) أو كأطباق سلطة." if lang_code == 'ar' else "With main meals or fresh salads.",
            'buy': "اختيار الخضروات الطازجة أسبوعياً." if lang_code == 'ar' else "Buy fresh vegetables weekly."
        }
        
    else:
        return {
            'cat': f"📦 {product_name.title()}",
            'status': "🔍 منتج غذائي متوازن" if lang_code == 'ar' else "🔍 Balanced Food Item",
            'nutrients': "فيتامينات، معادن، ألياف، وكربوهيدرات حسب نوع المنتج." if lang_code == 'ar' else "Vitamins, minerals, fiber, and carbohydrates.",
            'effect': "يمد الجسم برعاية غذائية متوازنة عند تناوله باعتدال." if lang_code == 'ar' else "Provides balanced nutrition when consumed moderately.",
            'time': "خلال اليوم حسب الاحتياج اليومي." if lang_code == 'ar' else "During the day as needed.",
            'buy': "مراجعة المكونات وتاريخ الصلاحية المدون." if lang_code == 'ar' else "Check nutritional label and expiry date."
        }

# 4. UI Texts
TEXTS = {
    'ar': {
        'title': "🛒 Future Mall - مصنف المنتجات والعناصر الغذائية",
        'subtitle': "التحليلي الذكي لاسم المنتج ومكوناته الغذائية",
        'upload_label': "اختر أو اسحب صورة المنتج هنا",
        'lang_btn': "English 🌐",
        'result_header': "اسم المنتج المكتشف:",
        'health_title': "🥗 التحليل الغذائي والصحي:",
        'cat_lbl': "المنتج والتصنيف:",
        'status_lbl': "القيمة الغذائية:",
        'nutrients_lbl': "🧪 العناصر الغذائية والمكونات:",
        'effect_lbl': "💡 الفوائد والتأثير الصحي:",
        'time_lbl': "⏰ أفضل وقت للتناول:",
        'buy_lbl': "🛒 أفضل وقت للشراء:"
    },
    'en': {
        'title': "🛒 Future Mall - Product & Nutrition Classifier",
        'subtitle': "Smart analysis for detected products and nutritional details",
        'upload_label': "Choose or drag & drop image here",
        'lang_btn': "العربية 🌐",
        'result_header': "Detected Product Name:",
        'health_title': "🥗 Health & Nutrition Breakdown:",
        'cat_lbl': "Product & Category:",
        'status_lbl': "Nutritional Value:",
        'nutrients_lbl': "🧪 Nutrients & Ingredients:",
        'effect_lbl': "💡 Health Impact & Benefits:",
        'time_lbl': "⏰ Best Time to Consume:",
        'buy_lbl': "🛒 Best Time to Buy:"
    }
}

lang = st.session_state.lang
t = TEXTS[lang]

st.button(t['lang_btn'], on_click=toggle_language)
st.title(t['title'])
st.caption(t['subtitle'])

# 5. Load Class Names
@st.cache_resource
def load_labels():
    labels_path = "labels.txt" if os.path.exists("labels.txt") else "labels" if os.path.exists("labels") else None
    if labels_path:
        with open(labels_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]
    return ["Mango Yoghurt", "Apple", "Banana", "Cucumber"]

class_names = load_labels()

uploaded_file = st.file_uploader(t['upload_label'], type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, width='stretch')

    with st.spinner("Extracting product name and nutrition data..."):
        file_name = uploaded_file.name.lower()
        
        # Read exact product name from labels or filename
        detected_product = class_names[0]
        for class_item in class_names:
            clean_item = " ".join(class_item.split()[1:]) if class_item.split()[0].isdigit() else class_item
            if clean_item.lower() in file_name or any(w in file_name for w in clean_item.lower().split()):
                detected_product = clean_item
                break

        # Remove line numbers if present
        clean_product_name = " ".join(detected_product.split()[1:]) if detected_product.split()[0].isdigit() else detected_product
        
        # Fetch nutritional analysis dynamically
        nutrition_info = get_nutrition_details(clean_product_name, lang)

        # Output Display
        st.subheader(t['result_header'])
        st.success(f"**{clean_product_name}**")

        st.markdown("---")

        st.subheader(t['health_title'])

        col1, col2 = st.columns(2)
        with col1:
            st.warning(f"**{t['cat_lbl']}**\n\n{nutrition_info['cat']}")
            st.info(f"**{t['status_lbl']}**\n\n{nutrition_info['status']}")
            st.write(f"**{t['nutrients_lbl']}**\n{nutrition_info['nutrients']}")
        
        with col2:
            st.write(f"**{t['effect_lbl']}**\n{nutrition_info['effect']}")
            st.write(f"**{t['time_lbl']}**\n{nutrition_info['time']}")
            st.write(f"**{t['buy_lbl']}**\n{nutrition_info['buy']}")
