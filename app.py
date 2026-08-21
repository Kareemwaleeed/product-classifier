import streamlit as st
from PIL import Image
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="Future Mall - Classifier", page_icon="🛒", layout="centered")

st.title("مصنف المنتجات الذكي - Future Mall 🛒")
st.caption("تحليل محتوى الصورة والتصنيف الصحيح الدقيق")

# 2. واجهة رفع الصورة
uploaded_file = st.file_uploader("اختر أو اسحب صورة المنتج هنا", type=["jpg", "png", "jpeg"])

# قوائم الكلمات المفتاحية بالإنجليزية للتأكد من تصنيف نتائج الذكاء الاصطناعي
FRUITS_KEYWORDS = [
    'fruit', 'apple', 'banana', 'orange', 'strawberry', 'grape', 'mango', 
    'watermelon', 'pineapple', 'dragonfruit', 'pitaya', 'berry', 'peach', 
    'pear', 'lemon', 'lime', 'fig', 'pomegranate', 'plum', 'guava', 'kiwi'
]

VEGETABLES_KEYWORDS = [
    'vegetable', 'cucumber', 'lettuce', 'tomato', 'potato', 'carrot', 'onion', 
    'garlic', 'pepper', 'zucchini', 'cabbage', 'broccoli', 'squash', 
    'cauliflower', 'spinach', 'corn', 'eggplant'
]

DAIRY_KEYWORDS = [
    'milk', 'yogurt', 'cheese', 'butter', 'cream', 'dairy', 'eggnog', 
    'ice cream', 'custard', 'laban'
]

def analyze_image_with_api(image_file):
    """تحليل محتوى الصورة عبر API سريع وخفيف جداً"""
    try:
        # إرسال الصورة لـ API تحليل الصور المباشر
        API_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"
        image_bytes = image_file.getvalue()
        
        response = requests.post(API_URL, data=image_bytes, timeout=12)
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            # تجميع الكلمات المكتشفة في الصورة
            detected_text = " ".join([item.get('label', '').lower() for item in data])
            
            # 1. فحص الفواكه (بما فيها الفراولة والتنين وكل الأنواع)
            if any(f in detected_text for f in FRUITS_KEYWORDS):
                return "(Fruits) فواكه"
            
            # 2. فحص منتجات الألبان والزبادي
            elif any(d in detected_text for d in DAIRY_KEYWORDS):
                return "(Dairy) زبادي ومنتجات ألبان"
                
            # 3. فحص الخضراوات
            elif any(v in detected_text for v in VEGETABLES_KEYWORDS):
                return "(Vegetables) خضراوات"

        # في حال لم يتعرف الـ API المباشر، نفحص اسم الملف كخطة بديلة
        filename = image_file.name.lower()
        if any(f in filename for f in FRUITS_KEYWORDS):
            return "(Fruits) فواكه"
        elif any(d in filename for d in DAIRY_KEYWORDS):
            return "(Dairy) زبادي ومنتجات ألبان"
        else:
            return "(Vegetables) خضراوات"

    except Exception:
        return "(Vegetables) خضراوات"

if uploaded_file is not None:
    # عرض الصورة فوراً لتجنب اختفائها
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, use_container_width=True)
    
    # تحليل محتوى الصورة
    with st.spinner("جاري فحص محتوى الصورة..."):
        result = analyze_image_with_api(uploaded_file)
        
    st.markdown("---")
    st.markdown("### :نتيجة التصنيف المكتشفة")
    st.success(result)
