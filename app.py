import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- Configuration ---
# 1. Streamlit Cloud Secrets වලින් හෝ Local Environment එකෙන් Key එක සෙවීම
GOOGLE_API_KEY = None

try:
    # st.secrets තිබේ නම් සහ එය ක්‍රැෂ් නොවේ නම් පමණක් Key එක ලබා ගනී
    if st.secrets and "GOOGLE_API_KEY" in st.secrets:
        GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except Exception:
    pass

# 2. Secrets වල නැත්නම් කෙලින්ම ඔයාගේ අලුත් API Key එක පාවිච්චි කිරීම (PC එකේදී වැඩ කිරීමට)
if not GOOGLE_API_KEY:
    GOOGLE_API_KEY = "AQ.Ab8RN6IzT2K_13wEJPS8iX1hCyve91IsptxFd2rzJQoQDXMFZQ"

# Gemini API එක Configure කිරීම
genai.configure(api_key=GOOGLE_API_KEY)

# Setup Streamlit Page Configuration
st.set_page_config(
    page_title="SehanAI Studio", 
    page_icon="✨", 
    layout="centered"
)

# --- 🎨 CUSTOM CSS FOR FIXED BEAUTIFUL UI ---
st.markdown("""
    <style>
        /* Main background color */
        .stApp {
            background: linear-gradient(135deg, #0f172a, #1e1b4b);
            color: #f8fafc;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #020617 !important;
            border-right: 1px solid #334155;
        }
        
        /* Title styling */
        h1 {
            color: #38bdf8 !important;
            font-family: 'Inter', sans-serif;
            font-weight: 800;
            text-align: center;
            text-shadow: 0px 4px 12px rgba(56, 189, 248, 0.2);
        }
        
        h3 {
            color: #94a3b8 !important;
            text-align: center;
            font-size: 1.1rem !important;
            margin-bottom: 2rem;
        }

        /* Custom styling for chat input */
        .stChatInputContainer {
            background-color: #1e293b !important;
            border-radius: 12px !important;
            border: 1px solid #334155 !important;
        }
        
        /* Button styling */
        .stButton>button {
            background: linear-gradient(90deg, #0ea5e9, #2563eb);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0px 4px 12px rgba(37, 99, 235, 0.4);
        }
    </style>
""", unsafe_allow_html=True)

# --- AI Models ---
CHAT_MODEL = "gemini-2.5-flash"

# --- SIDEBAR (App Info & Image Uploader) ---
with st.sidebar:
    st.markdown("<h2 style='color: #38bdf8; text-align: center;'>✨ SehanAI Studio</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Your Ultimate Multilingual & Vision AI Companion.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("👨‍💻 Founder & Developer:")
    st.info("**M.K.D.Sehan**")
    
    st.markdown("---")
    
    # 📸 Image Uploader Section
    st.subheader("📸 Upload Image")
    uploaded_file = st.file_uploader(
        "Upload an image to analyze or discuss with AI:", 
        type=["jpg", "jpeg", "png"]
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        st.success("Image uploaded successfully!")
    else:
        st.info("You can upload an image here to ask questions, analyze it, or get editing ideas.")

# --- MAIN PAGE (Chat Interface) ---
st.markdown("<h1>✨ SehanAI Studio</h1>", unsafe_allow_html=True)
st.markdown("<h3>Developed by M.K.D.Sehan</h3>", unsafe_allow_html=True)

# AI System Instructions
system_prompt = (
    "You are SehanAI Studio, a highly advanced and friendly AI assistant developed by M.K.D.Sehan. "
    "You can engage in conversation fluently in both Sinhala and English, always responding in the same language as the user. "
    "You are capable of analyzing and discussing images provided by the user. If an image is provided and the user "
    "asks to change or edit it, give them detailed, creative prompt instructions or explanations on how to achieve it. "
    "Always maintain a smart, polite, and helpful tone."
)

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Previous Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"], use_column_width=True)

# Get User Input
prompt = st.chat_input("Ask SehanAI anything...")

if prompt:
    # Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)
            st.session_state.messages.append({"role": "user", "content": prompt, "image": image})
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})

    # Fetch Response from Gemini Model
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
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")
            if "429" in str(e):
                st.warning("Rate limit exceeded. Please wait 60 seconds before sending another message.")

# --- FOOTER ---
st.markdown("<br><hr><p style='text-align: center; color: #64748b;'>🚀 Powered by Gemini | Developed with ❤️ by <b>M.K.D.Sehan</b></p>", unsafe_allow_html=True)
