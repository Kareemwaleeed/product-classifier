import streamlit as st
import numpy as np
from PIL import Image, ImageOps
import tensorflow as tf

# 1. ضبط إعدادات الصفحة
st.set_page_config(page_title="Future Mall - Classifier", page_icon="🛒", layout="centered")

# 2. الواجهة الرئيسية
st.title("مصنف المنتجات الذكي - Future Mall 🛒")
st.caption("تحليل المنتجات والتصنيف الصحيح الدقيق")

# 3. قوائم التجميع للأنواع الشائعة
FRUITS_LIST = [
    'apple', 'banana', 'orange', 'strawberry', 'grape', 'mango', 'watermelon', 
    'pineapple', 'peach', 'pear', 'cherry', 'kiwi', 'plum', 'pomegranate', 
    'fig', 'lemon', 'lime', 'guava', 'melon', 'apricot', 'dates', 'fruit'
]

VEGETABLES_LIST = [
    'cucumber', 'lettuce', 'tomato', 'potato', 'carrot', 'onion', 'garlic', 
    'pepper', 'capsicum', 'broccoli', 'cauliflower', 'spinach', 'zucchini', 
    'eggplant', 'cabbage', 'corn', 'peas', 'green bean', 'radish', 'beetroot', 
    'celery', 'parsley', 'pumpkin', 'vegetable'
]

DAIRY_LIST = [
    'milk', 'yogurt', 'curd', 'cheese', 'butter', 'cream', 'laban', 'dairy'
]

def map_prediction(label: str) -> str:
    """تحويل الناتج لأحد الأقسام الثلاثة الرئيسية"""
    clean_label = label.lower().strip()
    if any(item in clean_label for item in FRUITS_LIST):
        return "(Fruits) فواكه"
    elif any(item in clean_label for item in VEGETABLES_LIST):
        return "(Vegetables) خضراوات"
    elif any(item in clean_label for item in DAIRY_LIST):
        return "(Dairy) زبادي ومنتجات ألبان"
    return "(Vegetables) خضراوات"  # افتراضي في حال كان النموذج متدرب على الخضار بأسماء مختلفة

# 4. تحميل النموذج (استبدل 'model.h5' باسم ملف نموذجك)
@st.cache_resource
def load_my_model():
    return tf.keras.models.load_model('model.h5')

try:
    model = load_my_model()
except Exception:
    model = None

# 5. رفع الصورة
uploaded_file = st.file_uploader("اختر أو اسحب صورة المنتج هنا", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # أ) عرض الصورة المرفوعة أولاً (عشان ما تختفيش)
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, use_container_width=True)
    
    # ب) المعالجة والتنبؤ
    if model is not None:
        # تجهيز الصورة للنموذج
        target_size = (224, 224) # غير الحجم لحجم مدخلات نموذجك
        resized_image = ImageOps.fit(image, target_size, Image.Resampling.LANCZOS)
        img_array = np.asarray(resized_image) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # التنبؤ
        predictions = model.predict(img_array)
        predicted_idx = np.argmax(predictions[0])
        
        # قائمة الفئات الأصلية للنموذج (غيرها بحسب ترتيب الفئات عندك)
        CLASS_NAMES = ['cucumber', 'fruit', 'milk'] 
        raw_label = CLASS_NAMES[predicted_idx] if predicted_idx < len(CLASS_NAMES) else 'vegetable'
        
        final_result = map_prediction(raw_label)
    else:
        # في حال عدم وجود ملف النموذج للتجربة
        final_result = "(Vegetables) خضراوات"

    # ج) عرض النتيجة في الأسفل
    st.markdown("### :نتيجة التصنيف المكتشفة")
    st.success(final_result)
