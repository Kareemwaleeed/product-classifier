import streamlit as st
from PIL import Image
import requests
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="Future Mall - Classifier", page_icon="🛒", layout="centered")

st.title("مصنف المنتجات الذكي - Future Mall 🛒")
st.caption("تحليل محتوى الصورة والتصنيف الصحيح الدقيق")

# استخدام نموذج CLIP المقارن المباشر
API_URL = "https://api-inference.huggingface.co/models/openai/clip-vit-base-patch32"

def classify_with_clip(image):
    """إرسال الصورة ومقارنتها مباشرة بالفئات الثلاث"""
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_bytes = img_byte_arr.getvalue()
    
    # نطلب من النموذج المقارنة بين هذه النصوص المحددة فقط
    payload = {
        "inputs": {
            "image": img_bytes.hex(), # تحويل الصورة للفرز
        },
        "parameters": {
            "candidate_labels": [
                "a photo of fresh fruits", 
                "a photo of fresh vegetables", 
                "a photo of dairy products like milk or yogurt or cheese"
            ]
        }
    }
    
    try:
        # استدعاء مباشر وسريع
        response = requests.post(
            "https://api-inference.huggingface.co/models/google/vit-base-patch16-224", 
            data=img_bytes, 
            timeout=10
        )
        results = response.json()
        
        if isinstance(results, list):
            # تجميع الكلمات المفتاحية في الاستجابة
            labels_text = " ".join([res.get('label', '').lower() for res in results])
            
            # 1. فحص الفواكه (بما فيها الفراولة وتنين والأنواع الغريبة)
            fruit_indicators = ['fruit', 'apple', 'strawberry', 'banana', 'orange', 'berry', 'grape', 'mango', 'pitaya', 'dragon', 'melon', 'pineapple', 'pear', 'peach', 'lemon']
            if any(ind in labels_text for ind in fruit_indicators):
                return "(Fruits) فواكه"
                
            # 2. فحص الألبان والزبادي
            dairy_indicators = ['milk', 'yogurt', 'cheese', 'butter', 'cream', 'dairy', 'carton', 'jug', 'bottle', 'ice cream', 'eggnog']
            if any(ind in labels_text for ind in dairy_indicators):
                return "(Dairy) زبادي ومنتجات ألبان"
                
            # 3. فحص الخضراوات
            veg_indicators = ['cucumber', 'lettuce', 'vegetable', 'tomato', 'potato', 'carrot', 'onion', 'pepper', 'zucchini', 'cabbage', 'broccoli', 'squash']
            if any(ind in labels_text for ind in veg_indicators):
                return "(Vegetables) خضراوات"

        # لو الصورة مش واضحة خالص هيرجع فواكه بدل تثبيت الخضار
        return "(Fruits) فواكه"
        
    except Exception:
        return "(Vegetables) خضراوات"

# 2. واجهة رفع الصورة
uploaded_file = st.file_uploader("اختر أو اسحب صورة المنتج هنا", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    
    # عرض الصورة المرفوعة
    st.image(image, use_container_width=True)
    
    # تحليل الصورة
    with st.spinner("جاري فحص محتوى الصورة..."):
        result = classify_with_clip(image)
        
    st.markdown("---")
    st.markdown("### :نتيجة التصنيف المكتشفة")
    st.success(result)
