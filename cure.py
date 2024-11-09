import tensorflow as tf
import numpy as np
import streamlit as st
import google.generativeai as genai
import os
import time  # Import time for simulating delay
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# CSS Styling with Custom UI Elements
css_code = """
:root {
  /* Colors */
  --body-color: #e4f7ee;  /* Set the background color here */
  --sidebar-color: #fff;
  --primary-color: #008080;
  --primary-color-light: #f6f5ff;
  --toggle-color: #ddd;
  --text-color: #707070;
}

/* Hide Streamlit's deploy button and menu */
header, footer, .css-1lsmgbg.e1fqkh3o3, .css-9s5bis.edgvbvh10 {
  display: none !important;
}

/* Body Background */
body {
  background-color: var(--body-color);  /* Apply background color here */
  color: var(--text-color);
  background-image: url("/home/tridip/Desktop/Plant_disease_backend_copy/bg/pine-leaf.png");
}
.stButton button {
  background-color: #008080 !important;  /* Force the color for Streamlit's button */
  border: 2px solid #008080 !important;  /* Force the border color */
}
/* Predict button hover effect */
.stButton button:hover {
  background-color: teal !important;  /* Change background color on hover */
  color: white !important;  /* Ensure font color remains white on hover */
  box-shadow: 0px 4px 8px rgba(1, 179, 179, 0.48);
}

/* Upload Container */
.uploaded-div {
    font-size: 1.5rem;
  padding: 2rem 0.5rem;
  text-align: center;
  width: 100%;
  max-width: 20rem;
  margin: 2rem auto;
}

/* Buttons */
button, .browse-btn, .predict-btn {
  padding: 10px 20px;
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  background-color: var(--primary-color);
  border: 2px solid teal;
  border-radius: 12px;
  transition: 0.3s;
  text-align: center;
  cursor: pointer;
}

/* Update color for predict button specifically */
.predict-btn {
  background-color: #008080;  /* Change to desired color */
  border: 2px solid #008080;  /* Match the border to the button color */
}

.browse-btn:hover, .predict-btn:hover {
  background-color: teal;
  box-shadow: 0px 4px 8px rgba(1, 179, 179, 0.48);
}

/* Prediction Result */
.result-text {
  font-size: 22px;
  color: teal;
  font-weight: 600;
  margin: 1rem auto;
  text-align: center;
}
/* Buttons */
button, .browse-btn, .predict-btn {
  padding: 10px 20px;
  font-size: 16px;
  font-weight: 600;
  color: #fff;  /* Set the default font color to white */
  background-color: var(--primary-color);
  border: 2px solid teal;
  border-radius: 12px;
  transition: 0.3s;
  text-align: center;
  cursor: pointer;
}
/* Image Preview */
.preview {
  width: 100%;
  max-width: 400px;
  margin: 1rem auto;
  border: 1px dashed black;
  border-radius: 12px;
}

.preview img {
  width: 100%;
  height: auto;
  border-radius: 12px;
}
"""

# Apply the CSS styles to Streamlit
st.markdown(f"<style>{css_code}</style>", unsafe_allow_html=True)

# Configure the Gemini API with your API key
genai.configure(api_key=os.environ["GEMINI_KEY"])
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Function to load the model and make predictions
def model_prediction(test_image):
    model = tf.keras.models.load_model('keras_model/trained_model (1).keras')
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])  # Convert single image to batch
    prediction = model.predict(input_arr)
    result_index = np.argmax(prediction)
    return result_index

# Class labels
class_name = [
    'Apple__Apple_scab', 'Apple_Black_rot', 'Apple_Cedar_apple_rust', 'Apple__healthy',
    'Blueberry__healthy', 'Cherry(including_sour)Powdery_mildew', 'Cherry(including_sour)_healthy', 
    'Corn_(maize)Cercospora_leaf_spot_Gray_leaf_spot', 'Corn(maize)Common_rust', 
    'Corn_(maize)Northern_Leaf_Blight', 'Corn(maize)healthy', 'Grape__Black_rot', 
    'Grape__Esca(Black_Measles)', 'Grape__Leaf_blight(Isariopsis_Leaf_Spot)', 'Grape___healthy', 
    'Orange__Haunglongbing(Citrus_greening)', 'Peach__Bacterial_spot', 'Peach__healthy', 
    'Pepper,bell_Bacterial_spot', 'Pepper,_bell_healthy', 'Potato_Early_blight', 'Potato__Late_blight', 
    'Potato__healthy', 'Raspberry_healthy', 'Soybean_healthy', 'Squash__Powdery_mildew', 
    'Strawberry__Leaf_scorch', 'Strawberry_healthy', 'Tomato_Bacterial_spot', 'Tomato__Early_blight', 
    'Tomato__Late_blight', 'Tomato_Leaf_Mold', 'Tomato__Septoria_leaf_spot', 
    'Tomato__Spider_mites_Two-spotted_spider_mite', 'Tomato_Target_Spot', 'Tomato__Tomato_Yellow_Leaf_Curl_Virus', 
    'Tomato__Tomato_mosaic_virus', 'Tomato__healthy'
]

# Disease Detection UI
import streamlit as st

st.markdown('<h1 style="text-align:center;">🌱 Plant Disease Recognition</h1>', unsafe_allow_html=True)

st.markdown('<div class="uploaded-div">Upload an Image of the Plant</div>', unsafe_allow_html=True)
test_image = st.file_uploader("Choose an Image")

# Add loading bar while the image is being uploaded
if test_image is not None:
    # Simulate a file upload with a loading bar
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.02)  # Simulating a loading time
        progress.progress(i + 1)
    
    st.image(test_image, width=400)

if st.button("Predict"):
    if test_image is not None:
        result_index = model_prediction(test_image)
        predicted_disease = class_name[result_index]
        st.success(f"Model predicts this image is of a plant with: {predicted_disease}")
        
        # Fetch the cure and precautions
        prompt = f"What is the cure and precaution for {predicted_disease}?"
        response = model.generate_content(prompt)
        st.markdown(f'<div class="result-text">Cure and Precaution for {predicted_disease}:</div>', unsafe_allow_html=True)
        # Ensure the response contains candidates
        if response and hasattr(response, 'candidates') and len(response.candidates) > 0:
            # Access the text content
            output_text = response.candidates[0].content.parts[0].text
            st.markdown(output_text)
        else:
         print("No response available.")
        
    else:
        st.error("Please upload an image to predict the disease.")