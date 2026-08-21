import streamlit as st
from PIL import Image
import torch
import torchvision.transforms as T
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights

# 1. إعدادات الصفحة
st.set_page_config(page_title="Future Mall - Classifier", page_icon="🛒", layout="centered")

st.title("مصنف المنتجات الذكي - Future Mall 🛒")
st.caption("تحليل بصري مباشر لمحتوى الصورة بالذكاء الاصطناعي")

# 2. تحميل نموذج خفيف جداً وسريع ومستقر (MobileNetV2)
@st.cache_resource
def load_classifier_model():
    weights = MobileNet_V2_Weights.DEFAULT
    model = mobilenet_v2(weights=weights)
    model.eval()
    return model, weights

try:
    model, weights = load_classifier_model()
    preprocess = weights.transforms()
    categories = weights.meta["categories"]
except Exception as e:
    st.error("جاري إعداد النموذج...")

# 3. الكلمات المفتاحية الدقيقة للفئات الثلاث
FRUITS_KEYWORDS = [
    'apple', 'banana', 'orange', 'strawberry', 'strawberry', 'grape', 'mango', 
    'watermelon', 'pineapple', 'pomegranate', 'fig', 'lemon', 'lime', 'guava', 
    'kiwi', 'peach', 'pear', 'plum', 'pitaya', 'dragon', 'berry', 'fruit'
]

VEGETABLES_KEYWORDS = [
    'cucumber', 'lettuce', 'tomato', 'potato', 'carrot', 'onion', 'garlic', 
    'pepper', 'capsicum', 'broccoli', 'cauliflower', 'spinach', 'zucchini', 
    'cabbage', 'corn', 'pea', 'radish', 'squash', 'eggplant', 'vegetable'
]

DAIRY_KEYWORDS = [
    'milk', 'yogurt', 'yoghurt', 'cheese', 'butter', 'cream', 'carton', 'eggnog', 
    'pitcher', 'jug', 'dairy'
]

def classify_image_content(image):
    # تحويل وتجهيز الصورة
    img_tensor = preprocess(image).unsqueeze(0)
    
    with torch.no_grad():
        output = model(img_tensor)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        
    # فحص أفضل 15 توقع للصورة للوصول للنتيجة الصحيحة
    top15_prob, top15_catid = torch.topk(probabilities, 15)
    
    detected_labels = [categories[idx].lower() for idx in top15_catid]
    
    # المقارنة بذكاء على الفئات الثلاث
    for label in detected_labels:
        if any(f in label for f in FRUITS_KEYWORDS):
            return "(Fruits) فواكه"
        elif any(d in label for d in DAIRY_KEYWORDS):
            return "(Dairy) زبادي ومنتجات ألبان"
        elif any(v in label for v in VEGETABLES_KEYWORDS):
            return "(Vegetables) خضراوات"
            
    # لو الصورة منتج ألبان أو فاكهة غير مسجلة صراحة
    return "(Fruits) فواكه"

# 4. واجهة رفع الصورة
uploaded_file = st.file_uploader("اختر أو اسحب صورة المنتج هنا", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    
    # عرض الصورة المرفوعة
    st.image(image, use_container_width=True)
    
    # إجراء التصنيف
    with st.spinner("جاري فحص وتصنيف محتوى الصورة..."):
        result = classify_image_content(image)
        
    st.markdown("---")
    st.markdown("### :نتيجة التصنيف المكتشفة")
    st.success(result)
