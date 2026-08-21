import numpy as np
import streamlit as st

# 1. قائمة الكلمات الدلالية والفئات لتجميع أي نوع خضار، فاكهة، أو ألبان
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

def map_prediction_to_main_category(predicted_label: str) -> str:
    """تحويل اسم العنصر المتوقع إلى إحدى الفئات الثلاث الرئيسية"""
    label_clean = predicted_label.lower().strip()
    
    # فحص الفواكه
    if any(fruit in label_clean for fruit in FRUITS_LIST):
        return "فواكه (Fruits)"
    
    # فحص الخضراوات (تشمل الخيار والخس وغيرهما)
    elif any(veg in label_clean for veg in VEGETABLES_LIST):
        return "خضراوات (Vegetables)"
    
    # فحص منتجات الألبان (تشمل اللبن والزبادي)
    elif any(dairy in label_clean for dairy in DAIRY_LIST):
        return "منتجات ألبان (Dairy)"
    
    else:
        return "فئة غير معروفة"

# --- كيفية استخدام الدالة داخل الكود عندك بعد التنبؤ ---

# نفترض أن التنبؤ أخرج اسم العنصر الفرعي (مثل: 'cucumber' أو 'lettuce' أو 'yogurt')
# raw_prediction = model_classes[np.argmax(predictions[0])]

# مثال للتجربة:
raw_prediction = "cucumber"  # استبدل هذا بـ مخرجات النموذج الفعلية

final_result = map_prediction_to_main_category(raw_prediction)

# عرض النتيجة على الواجهة
st.markdown("### نتيجة التصنيف المكتشفة:")
st.success(f"{final_result}")
