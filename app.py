
import time
import streamlit as st
from google import genai
from google.genai import types

# Page configuration
st.set_page_config(
    page_title="Snap & Study",
    page_icon="📚",
    layout="centered"
)

st.title("📸 Snap & Study")
st.write(
    "Upload a picture of a question or your notes, "
    "and let AI explain it in simple language!"
)

# Get Gemini API key
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error(
        "Gemini API key not found. Please configure "
        "GEMINI_API_KEY in Streamlit Secrets."
    )
    st.stop()

# Store conversation history
if "chat" not in st.session_state:
    st.session_state.chat = []

# Upload an image
uploaded_image = st.file_uploader(
    "Upload your question or notes",
    type=["png", "jpg", "jpeg"]
)

# Enter a question
question = st.text_input(
    "What would you like to understand?"
)

# AI tutor instructions
SYSTEM_PROMPT = """
You are a friendly AI study tutor.
Explain concepts step by step using simple language.
Use examples when helpful.
Explain important terms and formulas for beginners.
Help students understand rather than memorize answers.
If an image is unclear, say so instead of guessing.
Format answers with headings and numbered steps when useful.
"""

# Generate explanation
if st.button("Explain", type="primary"):
    if not uploaded_image and not question.strip():
        st.warning("Please upload an image or enter a question.")

    else:
        contents = []

        if uploaded_image:
            image_part = types.Part.from_bytes(
                data=uploaded_image.getvalue(),
                mime_type=uploaded_image.type
            )
            contents.append(image_part)

        if question.strip():
            contents.append(
                types.Part.from_text(text=question.strip())
            )
        elif uploaded_image:
            contents.append(
                types.Part.from_text(
                    text=(
                        "Explain the content of this image "
                        "step by step in simple language."
                    )
                )
            )

        # Try the primary model, then the fallback model.
        # These model IDs are documented by Google, but access
        # depends on your API project.
        models_to_try = [
            "gemini-3.8-flash",
            "gemini-3.5-flash-lite",
            "gemini-3.6-flash-lite"
        ]

        answer = None
        last_error = None

        with st.spinner("Your AI tutor is thinking..."):
            for model_name in models_to_try:
                # Retry temporary errors twice for each model.
                for attempt in range(2):
                    try:
                        response = client.models.generate_content(
                            model=model_name,
                            contents=contents,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_PROMPT
                            )
                        )

                        if response.text:
                            answer = response.text
                            break

                        last_error = "The model returned an empty response."
                        break

                    except Exception as error:
                        last_error = error
                        error_text = str(error).upper()

                        # Retry only temporary capacity or rate-limit errors.
                        is_temporary = (
                            "503" in error_text
                            or "UNAVAILABLE" in error_text
                            or "429" in error_text
                            or "RESOURCE_EXHAUSTED" in error_text
                            or "500" in error_text
                            or "INTERNAL" in error_text
                        )

                        if not is_temporary:
                            break

                        if attempt == 0:
                            time.sleep(2)

                if answer:
                    break

                # Try the next model only for temporary failures.
                if last_error:
                    error_text = str(last_error).upper()
                    is_temporary = any(
                        code in error_text
                        for code in [
                            "503",
                            "UNAVAILABLE",
                            "429",
                            "RESOURCE_EXHAUSTED",
                            "500",
                            "INTERNAL"
                        ]
                    )
                    if not is_temporary:
                        break

        if answer:
            st.session_state.chat.append({
                "question": question.strip() or "Explain this image",
                "answer": answer
            })
        else:
            error_text = str(last_error).upper() if last_error else ""

            if "403" in error_text or "PERMISSION_DENIED" in error_text:
                st.error(
                    "Google denied access to the API project. "
                    "Check your API key and project permissions."
                )
            elif "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                st.error(
                    "The API usage limit may have been reached. "
                    "Wait a while and check your Gemini API quotas."
                )
            elif (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "500" in error_text
                or "INTERNAL" in error_text
            ):
                st.error(
                    "Gemini is temporarily busy. Both model attempts "
                    "failed. Please wait a minute and try again."
                )
            else:
                st.error(
                    "The AI request failed. Check your API settings "
                    "and Streamlit app logs for details."
                )

# Display previous explanations
if st.session_state.chat:
    st.subheader("📖 Your Study Session")

    for item in reversed(st.session_state.chat):
        st.markdown(f"**Your question:** {item['question']}")
        st.markdown("**AI Tutor's Explanation:**")
        st.write(item["answer"])
        st.divider()

# Clear conversation
if st.button("Clear Study Session"):
    st.session_state.chat = []
    st.rerun()