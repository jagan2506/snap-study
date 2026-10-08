# 📸 Snap & Study — Your AI Study Buddy

## About the Project

Studying can sometimes be confusing, especially when a question or concept in your notes is difficult to understand. That's why I created **Snap & Study**, a simple AI-powered study assistant designed to make learning easier.

With Snap & Study, students can upload a picture of a question, textbook page, or handwritten notes and ask for an explanation. The AI tutor helps break down difficult concepts into simpler language, making them easier to understand.

My goal with this project is to make studying more interactive, convenient, and less stressful for students.

## ✨ Features

* **Upload an Image:** Upload a picture of a question, textbook content, or study notes.
* **Ask Questions:** Type a question about what you want to learn.
* **AI-Powered Explanations:** Get clear, step-by-step explanations with the help of Google Gemini.
* **Study Session History:** Review previous questions and explanations during your current session.
* **Simple Interface:** Use the application through an easy-to-understand Streamlit interface.

## 🛠️ Technologies Used

* **Python** — Core programming language
* **Streamlit** — User interface and web application
* **Google Gemini API** — AI-powered explanations and image understanding

## 🚀 Getting Started

Follow these steps to run Snap & Study on your computer.

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd snap-study
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install the Required Packages

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Your Gemini API Key

Create a file named `secrets.toml` inside the `.streamlit` folder.

Add the following line:

```toml
GEMINI_API_KEY = "your-gemini-api-key-here"
```

Replace the placeholder with your API key from [Google AI Studio](https://aistudio.google.com/apikey).

**Important:** Keep your API key private. Never upload your real `secrets.toml` file to GitHub.

### 5. Run the Application

```bash
python -m streamlit run app.py
```

The application will open in your browser, ready to use.

## 💡 How It Works

1. Open Snap & Study.
2. Upload an image of a question or enter a question directly.
3. Click the **Explain** button.
4. Read the AI-generated explanation.
5. Continue exploring your topic by asking more questions.

## 🔒 Security

The Gemini API key is stored in Streamlit's secrets configuration rather than being written directly into the application code. The real secrets file should remain private and must not be committed to the public repository.

## 🎯 What I Learned

Building this project helped me explore how Python, Streamlit, and generative AI can work together to solve a practical problem. It also gave me experience with image uploads, API integration, application development, and creating a simple user-friendly interface.

## 🌟 Future Improvements

Some features I would like to add in the future include:

* A more interactive chat experience with follow-up questions
* The ability to email study-session summaries
* Support for additional file formats
* Options to save and revisit previous study sessions

## 🙌 Acknowledgements

Thanks to the developers of Streamlit and Google Gemini for providing tools that make it easier to build useful AI-powered applications.

---

**Snap & Study — Snap a question, understand the concept, and keep learning! 📚**
