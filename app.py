import streamlit as st
from google import genai
from google.genai import types
import json
from PIL import Image
import io

st.set_page_config(page_title="Image Analyzer", layout="centered")

# --- API Key Modal ---
if "api_key" not in st.session_state:
    st.session_state.api_key = None
if "connected" not in st.session_state:
    st.session_state.connected = False

@st.dialog("Connect to Gemini")
def api_key_dialog():
    st.markdown("Enter your Gemini API key to get started.")
    st.markdown("[Get a free key from Google AI Studio](https://aistudio.google.com/app/apikey)", unsafe_allow_html=True)
    key = st.text_input("API Key", type="password", placeholder="AIza...")
    if st.button("Connect", width='stretch'):
        if key.strip():
            try:
                client = genai.Client(api_key=key.strip())
                client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents="ping"
                )
                st.session_state.api_key = key.strip()
                st.session_state.connected = True
                st.rerun()
            except Exception as e:
                st.error(f"Could not connect: {e}")
        else:
            st.warning("Please enter an API key.")

if not st.session_state.connected:
    api_key_dialog()
    st.stop()

# --- Main App ---
st.title("Visual Analysis Pipeline")
st.caption("Powered by Gemini Vision API")

col1, col2 = st.columns([6, 1])
with col2:
    if st.button("🔌 Disconnect"):
        st.session_state.api_key = None
        st.session_state.connected = False
        st.rerun()

# --- Model Selector ---
model_options = {
    "Gemini 2.5 Flash (Recommended)": "gemini-2.5-flash",
    "Gemini 2.5 Flash-Lite (Higher limits)": "gemini-2.5-flash-lite",
    "Gemini 2.5 Pro (Most capable, lower limits)": "gemini-2.5-pro",
}
selected_label = st.selectbox("Select Model", list(model_options.keys()))
selected_model = model_options[selected_label]

# --- File Upload ---
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("Analyze Image"):
        with st.spinner("Analyzing..."):
            try:
                buffer = io.BytesIO()
                image.save(buffer, format="PNG")
                image_bytes = buffer.getvalue()

                client = genai.Client(api_key=st.session_state.api_key)

                prompt = """Analyze this image and return a JSON object with these fields:
                - description: one sentence summary
                - objects: list of key objects detected
                - scene: type of scene (indoor/outdoor/abstract/etc)
                - colors: dominant colors
                - confidence_notes: anything you're uncertain about

                Return only valid JSON, no markdown backticks."""

                response = client.models.generate_content(
                    model=selected_model,
                    contents=[
                        types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
                        prompt
                    ]
                )

                raw = response.text.strip()
                if raw.startswith("```"):
                    raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()

                result = json.loads(raw)

                st.subheader("Analysis Results")
                st.write(f"**Description:** {result['description']}")
                st.write(f"**Scene:** {result['scene']}")
                st.write(f"**Objects:** {', '.join(result['objects'])}")
                st.write(f"**Colors:** {', '.join(result['colors'])}")
                st.write(f"**Notes:** {result['confidence_notes']}")

                with st.expander("Raw JSON"):
                    st.json(result)

            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    st.error("Rate limit hit on this model. Try switching to a different model from the dropdown above.")
                else:
                    st.error(f"Something went wrong: {e}")
