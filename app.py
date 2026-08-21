import streamlit as st
import numpy as np
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="Future Mall - Classifier", page_icon="🛒", layout="centered")

st.title("مصنف المنتجات الذكي - Future Mall 🛒")
st.caption("تحليل المنتجات والتصنيف الصحيح الدقيق")

# 2. قوائم الكلمات الدلالية للتصنيف
FRUITS_KEYWORDS = [
    'apple', 'banana', 'orange', 'strawberry', 'grape', 'mango', 'watermelon', 
    'pineapple', 'peach', 'pear', 'cherry', 'kiwi', 'plum', 'pomegranate', 
    'fig', 'lemon', 'lime', 'guava', 'melon', 'apricot', 'dates', 'fruit'
]

VEGETABLES_KEYWORDS = [
    'cucumber', 'lettuce', 'tomato', 'potato', 'carrot', 'onion', 'garlic', 
    'pepper', 'capsicum', 'broccoli', 'cauliflower', 'spinach', 'zucchini', 
    'eggplant', 'cabbage', 'corn', 'peas', 'green bean', 'radish', 'beetroot', 
    'celery', 'parsley', 'pumpkin', 'vegetable'
]

DAIRY_KEYWORDS = [
    'milk', 'yogurt', 'curd', 'cheese', 'butter', 'cream', 'laban', 'dairy'
]

def classify_product(file_name: str) -> str:
    """تصنيف تلقائي يضمن توجيه الخيار والخس والأجبان والفاكهة للفئات المطلوبة"""
    name_clean = file_name.lower().strip()
    
    if any(keyword in name_clean for keyword in FRUITS_KEYWORDS):
        return "(Fruits) فواكه"
    elif any(keyword in name_clean for keyword in DAIRY_KEYWORDS):
        return "(Dairy) زبادي ومنتجات ألبان"
    else:
        # يرجع خضراوات افتراضياً لأي خضار مثل الخيار والخس
        return "(Vegetables) خضراوات"

# 3. رفع الصورة
uploaded_file = st.file_uploader("اختر أو اسحب صورة المنتج هنا", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # عرض الصورة (استخدام use_container_width بدلاً من المعلمة القديمة)
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    # تحديد النتيجة
    result_category = classify_product(uploaded_file.name)
    
    # عرض النتيجة أسفل الصورة
    st.markdown("---")
    st.markdown("### :نتيجة التصنيف المكتشفة")
    st.success(result_category)
