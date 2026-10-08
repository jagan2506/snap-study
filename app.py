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
    "and let AI help you understand it!"
)

# Get Gemini API key from Streamlit secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error(
        "Gemini API key not found. Please add it to "
        ".streamlit/secrets.toml"
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

# Generate explanation
if st.button("Explain", type="primary"):
    if not uploaded_image and not question.strip():
        st.warning("Please upload an image or enter a question.")

    else:
        with st.spinner("Your AI tutor is thinking..."):
            try:
                contents = []

                if uploaded_image:
                    image_part = types.Part.from_bytes(
                        data=uploaded_image.getvalue(),
                        mime_type=uploaded_image.type
                    )
                    contents.append(image_part)

                if question.strip():
                    contents.append(
                        types.Part.from_text(text=question)
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

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=(
                            "You are a friendly AI study tutor. "
                            "Explain concepts step by step using "
                            "simple language and examples. "
                            "Help students learn rather than just "
                            "memorize answers. If an image is unclear, "
                            "say so instead of guessing."
                        )
                    )
                )

                st.session_state.chat.append({
                    "question": question.strip()
                    or "Explain this image",
                    "answer": response.text
                    or "Sorry, I couldn't generate an answer."
                })

            except Exception as error:
                st.error(f"Something went wrong: {error}")

# Display previous explanations
if st.session_state.chat:
    st.subheader("📖 Your Study Session")

    for item in reversed(st.session_state.chat):
        st.markdown(f"**Your question:** {item['question']}")
        st.markdown("**AI Tutor's Explanation:**")
        st.write(item["answer"])
        st.divider()

# Clear the conversation
if st.button("Clear Study Session"):
    st.session_state.chat = []
    st.rerun()