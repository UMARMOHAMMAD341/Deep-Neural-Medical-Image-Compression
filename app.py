import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
from db import save_result, get_results

# Page config
st.set_page_config(page_title="Lung Cancer Detection", layout="centered")

# Title
st.title("🫁 Lung Cancer Detection System")
st.write("Upload a CT scan image to detect lung cancer.")

# Load model safely
@st.cache_resource
def load_model():
    try:
        model = tf.keras.models.load_model("model.h5")
        return model
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        return None

model = load_model()

# Upload image
file = st.file_uploader("Upload CT Scan Image", type=["jpg", "png", "jpeg"])

if file is not None:
    image = Image.open(file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("🔍 Predict"):
        if model is None:
            st.error("Model not loaded. Check model.h5 file.")
        else:
            try:
                # Preprocessing
                img = image.resize((224, 224))
                img = np.array(img) / 255.0
                img = np.expand_dims(img, axis=0)

                # Prediction
                prediction = model.predict(img)[0][0]

                # Result
                if prediction > 0.5:
                    result = "⚠️ Malignant (Cancer Detected)"
                    confidence = prediction
                else:
                    result = "✅ Benign (No Cancer)"
                    confidence = 1 - prediction

                # Display result
                st.subheader("🧾 Result")
                st.success(result)
                st.write(f"Confidence: {confidence:.2f}")

                # Save to database
                save_result(file.name, result, confidence)
                st.info("💾 Result saved to database")

            except Exception as e:
                st.error(f"❌ Prediction Error: {e}")

# -------------------------------
# 📊 SHOW HISTORY FROM DATABASE
# -------------------------------

st.markdown("---")
st.subheader("📊 Previous Predictions")

if st.button("📂 Show History"):
    data = get_results()

    if not data:
        st.warning("No records found in database")
    else:
        for row in data:
            st.markdown("------")
            st.write(f"🆔 ID: {row[0]}")
            st.write(f"📁 File Name: {row[1]}")
            st.write(f"📊 Result: {row[2]}")
            st.write(f"🎯 Confidence: {row[3]:.2f}")
            st.write(f"⏰ Time: {row[4]}")