import os
import numpy as np
from PIL import Image, ImageOps
import tf_keras as keras

# تحميل النموذج
model = keras.models.load_model("keras_model.h5", compile=False)

# قراءة أسماء الفئات
with open("labels.txt", "r", encoding="utf-8") as f:
    class_names = [line.strip() for line in f.readlines()]

# قراءة الصور الموجودة داخل المجلد تلقائياً
folder_path = "Test_images"
valid_extensions = (".jpg", ".jpeg", ".png", ".webp")

test_images = [
    os.path.join(folder_path, file)
    for file in os.listdir(folder_path)
    if file.lower().endswith(valid_extensions)
]

def predict_image(image_path):
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(image_path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array

    prediction = model.predict(data, verbose=0)
    index = np.argmax(prediction)
    
    return class_names[index], prediction[0][index]

print("\n==========================================")
print("     Project Classification Results       ")
print("==========================================")

for img_path in test_images:
    try:
        category, score = predict_image(img_path)
        print(f"Image: {img_path}")
        print(f"Prediction: {category}")
        print(f"Confidence: {score * 100:.2f}%\n")
    except Exception as e:
        print(f"Error reading {img_path}: {e}\n")