import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- Configuration ---
# 1. Insert your Gemini API Key here
GOOGLE_API_KEY = "AQ.Ab8RN6LRenzHgO-xVwaxIzcCRz9JlaFQOHp8i_9bZaGXsr_v_g"

# Configure the API Key
if GOOGLE_API_KEY and GOOGLE_API_KEY != "AQ.Ab8RN6LRenzHgO-xVwaxIzcCRz9JlaFQOHp8i_9bZaGXsr_v_g":
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    st.error("Please enter your Google API Key inside the 'app.py' file.")
    st.stop()

# 2. Setup Streamlit Page Configuration
st.set_page_config(
    page_title="SehanAI Studio", 
    page_icon="✨", 
    layout="centered"
)

# --- AI Models ---
CHAT_MODEL = "gemini-2.5-flash"

# --- SIDEBAR (App Info & Image Uploader) ---
with st.sidebar:
    st.title("✨ SehanAI Studio")
    st.markdown("Your Ultimate Multilingual & Vision AI Companion.")
    st.subheader("👨‍💻 Founder & Developer:")
    st.info("**M.K.D.Sehan**")
    
    st.markdown("---")
    
    # 📸 Image Uploader Section
    st.subheader("📸 Upload Image")
    uploaded_file = st.file_uploader(
        "Upload an image to analyze or discuss with AI:", 
        type=["jpg", "jpeg", "png"]
    )
    
    # Display Image Preview if uploaded
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        st.success("Image uploaded successfully!")
    else:
        st.info("You can upload an image here to ask questions, analyze it, or get editing ideas.")

# --- MAIN PAGE (Chat Interface) ---
st.title("✨ SehanAI Studio")
st.subheader("Developed by M.K.D.Sehan")
st.write("Welcome! Ask anything in **English** or **Sinhala**. You can also upload images via sidebar.")

# 3. AI System Instructions
system_prompt = (
    "You are SehanAI Studio, a highly advanced and friendly AI assistant developed by M.K.D.Sehan. "
    "You can engage in conversation fluently in both Sinhala and English, always responding in the same language as the user. "
    "You are capable of analyzing and discussing images provided by the user. If an image is provided and the user "
    "asks to change or edit it, give them detailed, creative prompt instructions or explanations on how to achieve it. "
    "Always maintain a smart, polite, and helpful tone."
)

# 4. Initialize Chat History (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display Previous Chat History on Screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"], use_column_width=True)

# 6. Get User Input (Prompt)
prompt = st.chat_input("Ask SehanAI anything...")

# If user sends a message
if prompt:
    # 6.1. Display User Message on Screen
    with st.chat_message("user"):
        st.markdown(prompt)
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)
            st.session_state.messages.append({
                "role": "user", 
                "content": prompt, 
                "image": image
            })
        else:
            st.session_state.messages.append({
                "role": "user", 
                "content": prompt
            })

    # 7. Fetch Response from Gemini Model
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            model = genai.GenerativeModel(
                model_name=CHAT_MODEL,
                system_instruction=system_prompt
            )
            
            if uploaded_file is not None:
                response = model.generate_content([prompt, image])
            else:
                response = model.generate_content(prompt)
            
            full_response = response.text
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response
            })
            
        except Exception as e:
            st.error(f"Error: {e}")
            if "429" in str(e):
                st.warning("Rate limit exceeded. Please wait 60 seconds before sending another message.")

# --- FOOTER ---
st.markdown("---")
st.caption("🚀 Powered by Gemini | Developed with ❤️ by **M.K.D.Sehan**")
