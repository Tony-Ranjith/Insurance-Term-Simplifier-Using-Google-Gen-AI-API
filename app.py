import streamlit as st
import google.generativeai as genai
from googletrans import Translator

# Configure Gemini
genai.configure(api_key="ADD Your API Key")

# Translator
translator = Translator()

# Page setup
st.set_page_config(page_title="Insurance Term Simplifier", layout="centered")

st.title("🧠 Insurance Term Simplifier")
st.write("Enter an insurance term, and I'll explain it in simple sentences with an example.")

# Input box
term = st.text_input("Enter an Insurance Term", "")

# Initialize session state
for key in ['show_example', 'show_surprise', 'show_celebration']:
    if key not in st.session_state:
        st.session_state[key] = False

# Reset session state when term changes
if "last_term" not in st.session_state:
    st.session_state.last_term = ""

if term and term != st.session_state.last_term:
    st.session_state.last_term = term
    for key in ['show_example', 'show_surprise', 'show_celebration']:
        st.session_state[key] = False

# Fetch functions
def fetch_definition(term):
    prompt = f"You are an Insurance Agent. Explain the insurance term '{term}' in 2-3 simple sentences without any emojis or special characters."
    model = genai.GenerativeModel("gemini-2.0-flash")
    return model.generate_content(prompt).text.strip()

def fetch_example(term):
    prompt = f"Give a real-life example to explain the insurance term '{term}' without any emojis or special characters."
    model = genai.GenerativeModel("gemini-2.0-flash")
    return model.generate_content(prompt).text.strip()

def fetch_funny_fact(term):
    prompt = f"Give a funny or surprising fact related to the insurance term '{term}' or insurance in general, without any emojis or special characters."
    model = genai.GenerativeModel("gemini-2.0-flash")
    return model.generate_content(prompt).text.strip()

# Translation helper
def translate_text(text, dest_lang):
    if dest_lang != "en":
        return translator.translate(text, dest=dest_lang).text
    return text

# Language options
lang_codes = {
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "Kannada": "kn",
    "Bengali": "bn"
}

# Language selection dropdown
st.markdown("#### 🌐 Want to view content in your language?")
selected_lang = st.selectbox("Choose your preferred language", list(lang_codes.keys()), index=0)
lang_code = lang_codes[selected_lang]

# Main logic
if term:
    st.markdown("### ✅ Explanation...")
    with st.spinner("Thinking... 🤔"):
        definition = fetch_definition(term)

    st.markdown(f"""
    <div style="background-color:#f9f9f9; border: 1px solid #ddd; padding: 20px; border-radius: 8px; font-size: 16px; color: #3B3B3B; line-height: 1.6;">
        {definition}
    </div>
    """, unsafe_allow_html=True)

    # Translated version of definition
    if lang_code != "en":
        translated_definition = translate_text(definition, lang_code)
        st.markdown(f"""
        <div style="margin-top:10px; background-color:#e8f5e9; border: 1px solid #c8e6c9; padding: 18px; border-radius: 8px; font-size: 15px; color: #1B5E20;">
            {translated_definition}
        </div>
        """, unsafe_allow_html=True)

    # Show Real-World Example
    if st.session_state.show_example:
        st.markdown("### Real-World Example ")
        with st.spinner("Thinking... 🤔"):
            example = fetch_example(term)
        st.markdown(f"""
        <div style="background-color:#fdf5e6; border: 1px solid #f3e5ab; padding: 18px; border-radius: 8px; font-size: 14px; color: #3E2723;">
            {example}
        </div>
        """, unsafe_allow_html=True)

        if lang_code != "en":
            translated_example = translate_text(example, lang_code)
            st.markdown(f"""
            <div style="margin-top:10px; background-color:#fff8e1; border: 1px solid #ffe082; padding: 18px; border-radius: 8px; font-size: 14px; color: #4E342E;">
                {translated_example}
            </div>
            """, unsafe_allow_html=True)

    # Show Surprise Fact
    if st.session_state.show_surprise:
        st.markdown("### 🎉 Surprise Fact")
        with st.spinner("Fetching Surprise Fact... 🤔"):
            funny_fact = fetch_funny_fact(term)
        st.markdown(f"""
        <div style="background-color:#fff3e0; border: 1px solid #ffe0b2; padding: 18px; border-radius: 8px; font-size: 14px; color: #4E342E;">
            {funny_fact}
        </div>
        """, unsafe_allow_html=True)

        if lang_code != "en":
            translated_fact = translate_text(funny_fact, lang_code)
            st.markdown(f"""
            <div style="margin-top:10px; background-color:#fce4ec; border: 1px solid #f8bbd0; padding: 18px; border-radius: 8px; font-size: 14px; color: #880e4f;">
                {translated_fact}
            </div>
            """, unsafe_allow_html=True)

    if st.session_state.show_celebration:
        st.balloons()

    # Action buttons
    st.markdown("---")
    st.markdown("### 🔘 Take Action")
    btn1, btn2, btn3 = st.columns(3)

    with btn1:
        if st.button("Show Real-World Example"):
            st.session_state.show_example = True

    with btn2:
        if st.button("Give Me a Surprise!"):
            st.session_state.show_surprise = True

    with btn3:
        if st.button("Celebrate!"):
            st.session_state.show_celebration = True

# Optional static content
with st.expander("💡 What is Insurance?"):
    st.write("Insurance is a contract between an individual and an insurance company that provides financial protection against unforeseen circumstances. The insurer agrees to compensate the insured for specific losses, damages, or liabilities.")
    
# Footer
st.markdown("---")
st.caption("🚀 Powered by AI Studio + Streamlit")
