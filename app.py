import streamlit as st
from PIL import Image
from transformers import pipeline

# 1. إعدادات الصفحة
st.set_page_config(page_title="Future Mall - Classifier", page_icon="🛒", layout="centered")

st.title("مصنف المنتجات الذكي - Future Mall 🛒")
st.caption("تحليل محتوى الصورة والتصنيف الصحيح الدقيق")

# 2. تحميل موديل الفرز المباشر (خفيف وبيميز بين الـ 3 فئات بدقة عالية جداً)
@st.cache_resource
def load_clip_classifier():
    return pipeline("zero-shot-image-classification", model="openai/clip-vit-base-patch32")

try:
    classifier = load_clip_classifier()
except Exception as e:
    st.error("جاري تحميل الموديل، يرجى الانتظار قليلاً...")
    classifier = None

# الفئات الثلاث المطلوبة فقط باللغة الإنجليزية ليفهمها الذكاء الاصطناعي
LABELS = [
    "a photo of fresh fruits", 
    "a photo of fresh vegetables", 
    "a photo of dairy products like milk, yogurt, or cheese"
]

def classify_image(img):
    if classifier is None:
        return "جاري تحميل النموذج..."
    
    # الموديل بيقرأ الصورة ويقارنها بالتلات خيارات دول حصراً
    results = classifier(img, candidate_labels=LABELS)
    best_match = results[0]['label']
    
    if best_match == "a photo of fresh fruits":
        return "(Fruits) فواكه"
    elif best_match == "a photo of fresh vegetables":
        return "(Vegetables) خضراوات"
    else:
        return "(Dairy) زبادي ومنتجات ألبان"

# 3. واجهة رفع الصورة
uploaded_file = st.file_uploader("اختر أو اسحب صورة المنتج هنا", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    
    # عرض الصورة فوراً
    st.image(image, use_container_width=True)
    
    # تحليل محتوى الصورة
    with st.spinner("جاري فحص الصورة بالذكاء الاصطناعي..."):
        result = classify_image(image)
        
    st.markdown("---")
    st.markdown("### :نتيجة التصنيف المكتشفة")
    st.success(result)
