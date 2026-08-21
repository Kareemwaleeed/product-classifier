import streamlit as st
from PIL import Image
from transformers import pipeline

# 1. إعدادات الصفحة
st.set_page_config(page_title="Future Mall - Classifier", page_icon="🛒", layout="centered")

st.title("مصنف المنتجات الذكي - Future Mall 🛒")
st.caption("تحليل محتوى الصورة والتصنيف الصحيح الدقيق")

# 2. تحميل نموذج الذكاء الاصطناعي لفحص الصور محلياً
@st.cache_resource
def load_classifier():
    # نموذج تصنيف صور سريع وخفيف جداً
    return pipeline("image-classification", model="google/vit-base-patch16-224")

classifier = load_classifier()

# 3. قوائم الكلمات لتوجيه الفئات
FRUITS = ['apple', 'banana', 'orange', 'strawberry', 'grape', 'mango', 'watermelon', 'pineapple', 'dragonfruit', 'fruit', 'pitaya', 'berry', 'peach', 'pear', 'lemon']
VEGETABLES = ['cucumber', 'lettuce', 'tomato', 'potato', 'carrot', 'onion', 'garlic', 'pepper', 'zucchini', 'cabbage', 'broccoli', 'vegetable', 'squash']
DAIRY = ['milk', 'yogurt', 'cheese', 'butter', 'cream', 'dairy', 'eggnog', 'ice cream']

def predict_image_category(img):
    # تحليل محتوى الصورة عبر الذكاء الاصطناعي
    results = classifier(img)
    
    # فحص أفضل النتائج المكتشفة داخل الصورة
    for item in results:
        label = item['label'].lower()
        if any(f in label for f in FRUITS):
            return "(Fruits) فواكه"
        elif any(v in label for v in VEGETABLES):
            return "(Vegetables) خضراوات"
        elif any(d in label for d in DAIRY):
            return "(Dairy) زبادي ومنتجات ألبان"
            
    # لو الصورة خضار مشهور أو غير معرف
    return "(Vegetables) خضراوات"

# 4. واجهة رفع الصورة
uploaded_file = st.file_uploader("اختر أو اسحب صورة المنتج هنا", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    
    # عرض الصورة فوراً
    st.image(image, use_container_width=True)
    
    # تحليل الصورة وعرض النتيجة
    with st.spinner("جاري تحليل الصورة..."):
        result = predict_image_category(image)
        
    st.markdown("---")
    st.markdown("### :نتيجة التصنيف المكتشفة")
    st.success(result)
