import streamlit as st
from PIL import Image
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="Future Mall - Classifier", page_icon="🛒", layout="centered")

st.title("مصنف المنتجات الذكي - Future Mall 🛒")
st.caption("تحليل بصري مباشر لمحتوى الصورة بالذكاء الاصطناعي")

# 2. إعداد مفتاح API الخاص بـ Google Gemini
# يُفضل وضع المفتاح في Streamlit Secrets أو كتابته مباشرة هنا للتجربة
API_KEY = st.secrets.get("GEMINI_API_KEY", "ضع_مفتاح_GEMINI_هنا")

if API_KEY != "ضع_مفتاح_GEMINI_هنا":
    genai.configure(api_key=API_KEY)

def classify_with_gemini(image):
    try:
        # استخدام نموذج رؤية خفيف وسريع
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = """
        Examine this image carefully and classify it into EXACTLY ONE of these three categories:
        1. Fruits
        2. Vegetables
        3. Dairy

        Rules:
        - If it's any fruit (strawberries, dragon fruit, apples, bananas, etc.), respond with ONLY: Fruits
        - If it's any vegetable (cucumbers, lettuce, tomatoes, etc.), respond with ONLY: Vegetables
        - If it's any dairy product (milk, yogurt, cheese, butter, etc.), respond with ONLY: Dairy

        Respond with ONLY one word from the list above.
        """
        
        response = model.generate_content([prompt, image])
        answer = response.text.strip().lower()
        
        if 'fruit' in answer:
            return "(Fruits) فواكه"
        elif 'vegetable' in answer:
            return "(Vegetables) خضراوات"
        elif 'dairy' in answer:
            return "(Dairy) زبادي ومنتجات ألبان"
        else:
            return "(Vegetables) خضراوات"
            
    except Exception as e:
        return f"حدث خطأ أثناء الاتصال بالخدمة: {str(e)}"

# 3. واجهة رفع الصورة
uploaded_file = st.file_uploader("اختر أو اسحب صورة المنتج هنا", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    
    # عرض الصورة فوراً
    st.image(image, use_container_width=True)
    
    # التحليل البصري الحقيقي
    with st.spinner("جاري فحص وتصنيف محتوى الصورة..."):
        result = classify_with_gemini(image)
        
    st.markdown("---")
    st.markdown("### :نتيجة التصنيف المكتشفة")
    st.success(result)
