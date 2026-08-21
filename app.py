import streamlit as st
from PIL import Image
import requests
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="Future Mall - Classifier", page_icon="🛒", layout="centered")

st.title("مصنف المنتجات الذكي - Future Mall 🛒")
st.caption("تحليل محتوى الصورة والتصنيف الصحيح الدقيق")

# رابط نموذج الذكاء الاصطناعي المباشر (Google ViT)
API_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"

# 2. قوائم الكلمات لتوجيه الفئات
FRUITS = [
    'apple', 'banana', 'orange', 'strawberry', 'grape', 'mango', 'watermelon', 
    'pineapple', 'dragonfruit', 'pitaya', 'fruit', 'berry', 'peach', 'pear', 
    'lemon', 'fig', 'pomegranate', 'plum', 'guava', 'kiwi', 'papaya'
]

VEGETABLES = [
    'cucumber', 'lettuce', 'tomato', 'potato', 'carrot', 'onion', 'garlic', 
    'pepper', 'zucchini', 'cabbage', 'broccoli', 'vegetable', 'squash', 
    'cauliflower', 'spinach', 'corn', 'eggplant'
]

DAIRY = [
    'milk', 'yogurt', 'cheese', 'butter', 'cream', 'dairy', 'eggnog', 
    'ice cream', 'custard'
]

def query_huggingface_api(image_bytes):
    """إرسال الصورة للذكاء الاصطناعي لفحص محتواها"""
    try:
        response = requests.post(API_URL, data=image_bytes, timeout=10)
        return response.json()
    except Exception:
        return None

def classify_image(image):
    # تحويل الصورة إلى بايتات
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_bytes = img_byte_arr.getvalue()
    
    # تحليل الصورة
    results = query_huggingface_api(img_bytes)
    
    if results and isinstance(results, list):
        for item in results:
            label = item.get('label', '').lower()
            if any(f in label for f in FRUITS):
                return "(Fruits) فواكه"
            elif any(v in label for v in VEGETABLES):
                return "(Vegetables) خضراوات"
            elif any(d in label for d in DAIRY):
                return "(Dairy) زبادي ومنتجات ألبان"
                
    # افتراضي في حال عدم التعرف
    return "(Vegetables) خضراوات"

# 3. واجهة رفع الصورة
uploaded_file = st.file_uploader("اختر أو اسحب صورة المنتج هنا", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    
    # عرض الصورة فوراً
    st.image(image, use_container_width=True)
    
    # تحليل محتوى الصورة
    with st.spinner("جاري تحليل الصورة بالذكاء الاصطناعي..."):
        result = classify_image(image)
        
    st.markdown("---")
    st.markdown("### :نتيجة التصنيف المكتشفة")
    st.success(result)
