import streamlit as st
from PIL import Image
import torchvision.transforms as T
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights

# 1. إعدادات الصفحة
st.set_page_config(page_title="Future Mall - Classifier", page_icon="🛒", layout="centered")

st.title("مصنف المنتجات الذكي - Future Mall 🛒")
st.caption("تحليل محتوى الصورة والتصنيف الصحيح الدقيق")

# 2. تحميل نموذج الذكاء الاصطناعي (MobileNetV2 خفيف جداً وسريع)
@st.cache_resource
def load_model():
    weights = MobileNet_V2_Weights.DEFAULT
    model = mobilenet_v2(weights=weights)
    model.eval()
    return model, weights

try:
    model, weights = load_model()
    preprocess = weights.transforms()
    categories = weights.meta["categories"]
except Exception as e:
    st.error("حدث خطأ أثناء تحميل النموذج، تأكد من ملف requirements.txt")

# 3. قوائم الكلمات لتوجيه التصنيف حسب محتوى الصورة
FRUITS = [
    'apple', 'banana', 'orange', 'strawberry', 'grape', 'mango', 'watermelon', 
    'pineapple', 'dragonfruit', 'fruit', 'pitaya', 'berry', 'peach', 'pear', 
    'lemon', 'fig', 'pomegranate', 'plum', 'guava', 'kiwi'
]

VEGETABLES = [
    'cucumber', 'lettuce', 'tomato', 'potato', 'carrot', 'onion', 'garlic', 
    'pepper', 'zucchini', 'cabbage', 'broccoli', 'vegetable', 'squash', 
    'cauliflower', 'spinach', 'corn', 'eggplant'
]

DAIRY = [
    'milk', 'yogurt', 'cheese', 'butter', 'cream', 'dairy', 'eggnog', 
    'ice cream', 'custard', 'eggnog'
]

def predict_category(img):
    # تجهيز الصورة وفحصها بالنموذج
    batch = preprocess(img).unsqueeze(0)
    prediction = model(batch).squeeze(0).softmax(0)
    
    # الحصول على أعلى 5 توقعات للصورة
    top5_prob, top5_catid = prediction.topk(5)
    
    for i in range(5):
        label = categories[top5_catid[i]].lower()
        
        if any(f in label for f in FRUITS):
            return "(Fruits) فواكه"
        elif any(v in label for v in VEGETABLES):
            return "(Vegetables) خضراوات"
        elif any(d in label for d in DAIRY):
            return "(Dairy) زبادي ومنتجات ألبان"
            
    # إذا كانت الصورة خضراوات غير مشهورة
    return "(Vegetables) خضراوات"

# 4. واجهة رفع الصورة
uploaded_file = st.file_uploader("اختر أو اسحب صورة المنتج هنا", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    
    # عرض الصورة فوراً
    st.image(image, use_container_width=True)
    
    # تحليل محتوى الصورة وعرض النتيجة
    with st.spinner("جاري تحليل الصورة بالذكاء الاصطناعي..."):
        result = predict_category(image)
        
    st.markdown("---")
    st.markdown("### :نتيجة التصنيف المكتشفة")
    st.success(result)
