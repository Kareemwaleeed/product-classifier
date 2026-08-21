import streamlit as st
from PIL import Image
import torch
import torchvision.transforms as T
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights

# 1. إعدادات الصفحة
st.set_page_config(page_title="Future Mall - Classifier", page_icon="🛒", layout="centered")

st.title("مصنف المنتجات الذكي - Future Mall 🛒")
st.caption("تحليل بصري لمحتوى الصورة + عرض الفوائد والمعلومات الغذائية")

# 2. تحميل نموذج الذكاء الاصطناعي
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

# 3. قوائم الكلمات المفتاحية
FRUITS_KEYWORDS = [
    'apple', 'banana', 'orange', 'strawberry', 'grape', 'mango', 
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
    img_tensor = preprocess(image).unsqueeze(0)
    
    with torch.no_grad():
        output = model(img_tensor)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        
    top15_prob, top15_catid = torch.topk(probabilities, 15)
    detected_labels = [categories[idx].lower() for idx in top15_catid]
    
    for label in detected_labels:
        if any(f in label for f in FRUITS_KEYWORDS):
            return "فواكه"
        elif any(d in label for d in DAIRY_KEYWORDS):
            return "ألبان"
        elif any(v in label for v in VEGETABLES_KEYWORDS):
            return "خضراوات"
            
    return "فواكه"

# 4. دالة عرض الفوائد والمعلومات الإضافية
def display_category_info(category_type):
    st.markdown("---")
    st.subheader(f"📊 معلومات وفوائد قسم: {category_type}")
    
    if category_type == "فواكه":
        st.success("🍎 **قسم الفواكه (Fruits Category)**")
        st.markdown("""
        * **الفوائد الصحية:** غنية بـ فيتامين C، الألياف الطبيعية، ومضادات الأكسدة التي تعزز المناعة وتحمي البشرة.
        * **القيمة الغذائية:** تمد الجسم بالسكريات الطبيعية (الفروكتوز) للحصول على الطاقة السريعة ونسبة عالية من الماء للترطيب.
        * **أمثلة شائعة:** فراولة، فاكهة التنين، موز، تفاح، برتقال، مانجو، بطيخ.
        * **نصيحة الحفظ:** يفضل حفظ الفواكه الحساسة (مثل الفراولة) في الثلاجة وعدم غسلها إلا قبل الأكل مباشرة.
        """)
        
    elif category_type == "خضراوات":
        st.info("🥦 **قسم الخضراوات (Vegetables Category)**")
        st.markdown("""
        * **الفوائد الصحية:** ممتازة لتحسين الهضم، خفض الكوليسترول، ودعم صحة القلب بفضل الألياف والمعادن.
        * **القيمة الغذائية:** سعرات حرارية منخفضة جداً، غنية بـ فيتامين A، فيتامين K، الحديد، والمغنيسيوم.
        * **أمثلة شائعة:** خيار، خس، طماطم، بروكلي، جزر، فلفل، كوسة.
        * **نصيحة الحفظ:** تحفظ الخضراوات الورقية في أكياس مخرمة داخل درج الثلاجة للحفاظ على نضارتها.
        """)
        
    elif category_type == "ألبان":
        st.warning("🥛 **قسم الزبادي والألبان (Dairy Category)**")
        st.markdown("""
        * **الفوائد الصحية:** تقوية العظام والأسنان، ودعم صحة الجهاز الهضمي والمعدة (خصوصاً الزبادي لاحتوائه على البروبيوتيك).
        * **القيمة الغذائية:** مصدر أساسي للكالسيوم، البروتين عالي الجودة، فيتامين B12، وفيتامين D.
        * **أمثلة شائعة:** حليب، زبادي، أجبان بأنواعها، زبدة، قشطة.
        * **نصيحة الحفظ:** تحفظ دائماً مبردة في درجة حرارة بين 1 إلى 4 درجات مئوية للتأكد من سلامتها.
        """)

# 5. واجهة رفع الصورة
uploaded_file = st.file_uploader("اختر أو اسحب صورة المنتج هنا", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    
    st.image(image, use_container_width=True)
    
    with st.spinner("جاري تحليل محتوى الصورة واستخراج المعلومات..."):
        category = classify_image_content(image)
        
    st.markdown("### :نتيجة التصنيف المكتشفة")
    st.success(f"المنتج ينتمي إلى: **({category})**")
    
    # عرض الفوائد والمعلومات
    display_category_info(category)
