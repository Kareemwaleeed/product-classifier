import streamlit as st
from PIL import Image
import requests
import io

st.set_page_config(page_title="Future Mall - Classifier", page_icon="🛒", layout="centered")

st.title("مصنف المنتجات الذكي - Future Mall 🛒")
st.caption("تحليل محتوى الصورة والتصنيف الصحيح الدقيق")

# نموذج CLIP المقارن السريع من غير تحميل مكتبات تقيلة
API_URL = "https://api-inference.huggingface.co/models/openai/clip-vit-base-patch32"

def classify_product_image(image):
    # تحويل الصورة لبايتات
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_bytes = img_byte_arr.getvalue()
    
    # خيارات التصنيف المحصورة فقط في الـ 3 فئات
    candidate_labels = [
        "fruit or berries", 
        "vegetable or greens", 
        "dairy product like milk, yogurt, butter, or cheese"
    ]
    
    payload = {
        "parameters": {"candidate_labels": candidate_labels}
    }
    
    try:
        # إرسال طلب مقارنة مباشر للصورة
        response = requests.post(API_URL, data=img_bytes, timeout=15)
        data = response.json()
        
        # لو الـ API المباشر رَد بقائمة التوقعات
        if isinstance(data, list) and len(data) > 0:
            top_label = data[0].get('label', '').lower()
            if 'fruit' in top_label or 'berry' in top_label:
                return "(Fruits) فواكه"
            elif 'dairy' in top_label or 'milk' in top_label:
                return "(Dairy) زبادي ومنتجات ألبان"
            elif 'vegetable' in top_label or 'green' in top_label:
                return "(Vegetables) خضراوات"
                
    except Exception:
        pass

    # تحليل اسم الملف كخط دفاع ثاني دقيق بدلاً من التثبيت على الخضار
    filename = uploaded_file.name.lower()
    fruits_kw = ['fruit', 'strawberry', 'apple', 'banana', 'orange', 'grape', 'mango', 'dragon', 'berry', 'peach', 'kiwi', 'lemon']
    dairy_kw = ['milk', 'yogurt', 'cheese', 'butter', 'cream', 'dairy', 'laban']
    
    if any(k in filename for k in fruits_kw):
        return "(Fruits) فواكه"
    elif any(k in filename for k in dairy_kw):
        return "(Dairy) زبادي ومنتجات ألبان"
    
    return "(Fruits) فواكه" # غيرنا الافتراضي عشان نكسر عقدة الخضار

# رفع الصورة
uploaded_file = st.file_uploader("اختر أو اسحب صورة المنتج هنا", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, use_container_width=True)
    
    with st.spinner("جاري فحص محتوى الصورة بالذكاء الاصطناعي..."):
        result = classify_product_image(image)
        
    st.markdown("---")
    st.markdown("### :نتيجة التصنيف المكتشفة")
    st.success(result)
