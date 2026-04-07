import streamlit as st
from PIL import Image
import numpy as np
try:
    import tensorflow as tf
except:
    tf = None
from db import save_result, get_results

# ✅ MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="Lung Cancer Detection", layout="centered")

# -------------------------------
# 🔐 LOGIN SYSTEM
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

users = {
    "umar": "1234",
    "admin": "admin"
}

if not st.session_state.logged_in:
    st.title("🔐 Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Invalid credentials ❌")

    st.stop()

# -------------------------------
# MAIN APP
# -------------------------------
st.title("🫁 Lung Cancer Detection System")
st.write(f"👤 Logged in as: {st.session_state.username}")
st.write("Upload a CT scan image to detect lung cancer.")

# Load model
@st.cache_resource
def load_model():
    if tf is None:
        return None
    try:
        return tf.keras.models.load_model("model.h5")
    except:
        return None

model = load_model()

# Upload image
file = st.file_uploader("Upload CT Scan Image", type=["jpg", "png", "jpeg"])

if file is not None:
    image = Image.open(file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("🔍 Predict"):
        if model is None:
            st.warning("⚠️ Model not available in deployed version")
        else:
            try:
                img = image.resize((224, 224))
                img = np.array(img) / 255.0
                img = np.expand_dims(img, axis=0)

                prediction = model.predict(img)[0][0]

                if prediction > 0.5:
                    result = "⚠️ Malignant (Cancer Detected)"
                    confidence = prediction
                else:
                    result = "✅ Benign (No Cancer)"
                    confidence = 1 - prediction

                st.subheader("🧾 Result")
                st.success(result)
                st.write(f"Confidence: {confidence:.2f}")

                save_result(st.session_state.username, file.name, result, confidence)
                st.info("💾 Result saved to database")

            except Exception as e:
                st.error(f"❌ Prediction Error: {e}")

# -------------------------------
# 📊 HISTORY
# -------------------------------
st.markdown("---")
st.subheader("📊 Previous Predictions")

if st.button("📂 Show History"):
    data = get_results(st.session_state.username)

    if not data:
        st.warning("No records found")
    else:
        for row in data:
            st.markdown("------")
            st.write(f"🆔 ID: {row[0]}")
            st.write(f"📁 File Name: {row[1]}")
            st.write(f"📊 Result: {row[2]}")
            st.write(f"🎯 Confidence: {row[3]:.2f}")
            st.write(f"⏰ Time: {row[4]}")
            st.write(f"👤 User: {row[5]}")

# -------------------------------
# 🔓 LOGOUT
# -------------------------------
if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()