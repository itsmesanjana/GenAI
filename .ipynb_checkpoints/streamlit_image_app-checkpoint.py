import google.generativeai as genai 
from dotenv import load_dotenv 
import os
from PIL import Image
import streamlit as st

load_dotenv()

api_key=os.getenv('GEMINI_API_KEY')
# print(api_key)

genai.configure(api_key=api_key)

st.header("Image analytics")

uploaded_file=st.file_uploader('Upload an Image',type=['png','jpg','jpeg'])

if uploaded_file is not None:
    st.image(Image.open(uploaded_file))

prompt=st.text_input('Enter the prompt')
if st.button("GET RESPONSE"):
    img=Image.open(uploaded_file)
    model=genai.GenerativeModel('gemini-2.0-flash')
    response=model.generate_content([prompt,img])
    st.markdown(response.text)