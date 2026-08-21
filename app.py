import streamlit as st
import numpy as np
from PIL import Image, ImageOps
import keras

st.set_page_config(page_title="Future Mall - Classifier", page_icon="🛍️", layout="centered")

if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'

def toggle_language():
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'

st.button("🌐 English / العربية", on_click=toggle_language)

TEXTS = {
    'ar': {
        'title': "🛍️ مصنف المنتجات الذكي - Future Mall",
        'subtitle': "ارفع صورة أي منتج لمعرفة تصنيفه، نسبة الثقة، والتحليل الصحي المفصل.",
        'upload_label': "اختر أو اسحب صورة المنتج هنا...",
        'uploaded_img': "الصورة المرفوعة",
        'prediction': "المنتج المحدد",
        'confidence': "نسبة الثقة",
        'health_title': "📊 التقييم والتحليل الصحي",
        'healthy': "🟢 منتج صحي مفيد",
        'unhealthy': "🔴 منتج غير صحي (يُفضل الاعتدال أو التجنب)",
        'fruits_desc': "الفواكه غنية بالألياف، الفيتامينات، ومضادات الأكسدة الطبيعية. ممتازة للصحة العامة وتعزيز المناعة.",
        'dairy_desc': "منتجات الألبان غنية بالكالسيوم والبروتين الممتاز لبناء العظام والأنسجة. يفضل اختيار الأنواع قليلة الدسم وغير المضافة بالسكر.",
        'junk_desc': "يحتوي على نسبة عالية من السكريات، الدهون المتحولة، أو الملح. الاستهلاك المفرط يؤدي للسمنة ومشاكل الصحة.",
        'general_desc': "تأكد دائماً من قراءة بطاقة المكونات والقيمة الغذائية المدونة على العبوة قبل الاستهلاك.",
        'error': "حدث خطأ أثناء قراءة الصورة، يرجى المحاولة بصورة أخرى."
    },
    'en': {
        'title': "🛍️ Smart Product Classifier - Future Mall",
        'subtitle': "Upload any product image to get its class, confidence score, and detailed health assessment.",
        'upload_label': "Choose or drag a product image here...",
        'uploaded_img': "Uploaded Image",
        'prediction': "Predicted Category",
        'confidence': "Confidence Level",
        'health_title': "📊 Health & Nutritional Assessment",
        'healthy': "🟢 Healthy Product",
        'unhealthy': "🔴 Unhealthy Product (Consume in moderation)",
        'fruits_desc': "Rich in natural fibers, vitamins, and antioxidants. Excellent for boosting immune health and digestion.",
        'dairy_desc': "Great source of calcium and high-quality protein for bone health. Opt for low-fat and unsweetened versions.",
        'junk_desc': "Contains high levels of sugars, trans fats, or sodium. Overconsumption may lead to obesity and health risks.",
        'general_desc': "Always check the nutrition facts panel and ingredient list on the package before consuming.",
        'error': "An error occurred while processing the image. Please try another one."
    }
}

t = TEXTS[st.session_state.lang]

st.title(t['title'])
st.write(t['subtitle'])

@st.cache_resource
def load_my_model():
    return keras.models.load_model("keras_model.h5", compile=False)

model = load_my_model()

with open("labels.txt", "r", encoding="utf-8") as f:
    class_names = [line.strip() for line in f.readlines()]

uploaded_file = st.file_uploader(
    t['upload_label'], 
    type=["jpg", "jpeg", "png", "webp", "bmp", "tiff"]
)

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption=t['uploaded_img'], use_container_width=True)
        
        size = (224, 224)
        image_resized = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image_resized)
        normalized = (image_array.astype(np.float32) / 127.5) - 1.0
        data = np.expand_dims(normalized, axis=0)

        prediction = model.predict(data, verbose=0)
        index = np.argmax(prediction)
        predicted_class = class_names[index]
        confidence = prediction[0][index] * 100

        st.markdown("---")
        st.success(f"**{t['prediction']}:** {predicted_class}")
        st.info(f"**{t['confidence']}:** {confidence:.2f}%")

        st.markdown(f"### {t['health_title']}")
        category_lower = predicted_class.lower()

        if "fruit" in category_lower or "vegetable" in category_lower:
            st.success(t['healthy'])
            st.write(t['fruits_desc'])
        elif "dairy" in category_lower or "milk" in category_lower:
            st.success(t['healthy'])
            st.write(t['dairy_desc'])
        else:
            st.warning(t['unhealthy'])
            st.write(t['junk_desc'])

        st.caption(f"💡 {t['general_desc']}")

    except Exception as e:
        st.error(t['error'])
