import streamlit as st
import requests

# Streamlit app
st.title("Sentiment Analysis App")
text = st.text_area("Enter text for sentiment analysis:")

if st.button("Predict"):
    if text:
        # Call the Flask API
        response = requests.post(
            'http://127.0.0.1:5000/predict',  # Adjust if deployed elsewhere
            json={'text': text}
        )
        
        if response.status_code == 200:
            result = response.json()
            st.write(result)
        else:
            st.error("Error in prediction")
    else:
        st.warning("Please enter some text for analysis.")
