# 🧕 InspireHer Chatbot (Project Drishti)

InspireHer is a RAG-based (Retrieval-Augmented Generation) AI assistant designed to empower rural women in India. It provides guidance on entrepreneurship, government schemes, and financial literacy by retrieving information from curated documents.

## 🚀 Features
- **RAG Architecture:** Uses LangChain and ChromaDB to fetch real-time data from PDFs, JSONs, and text files.
- **AI Brain:** Powered by Google Gemini 1.5 Flash for fast and accurate responses.
- **User-Friendly UI:** Built with Streamlit for a simple, accessible chat experience.
- **Multimodal Data:** Handles structured (JSON) and unstructured (PDF/TXT) information about government schemes.

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Backend:** Flask (Python)
- **LLM:** Google Gemini API
- **Vector Database:** ChromaDB
- **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)
- **Framework:** LangChain

## 📂 Project Structure
```text
├── app.py              # Flask Backend (RAG Engine)
├── ui.py               # Streamlit Frontend
├── chroma_db/          # Vector Database storage (Auto-generated)
├── scheme.pdf          # Document for government schemes
├── governmentschemes.json # Structured data for schemes
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
⚙️ Setup Instructions
1. Clone the repository
Bash
git clone [https://github.com/Vaishnaviii910/InspireHer-Chatbot.git](https://github.com/Vaishnaviii910/InspireHer-Chatbot.git)
cd InspireHer-Chatbot
2. Install Dependencies
Bash
pip install -r requirements.txt
3. Set Environment Variables
Create a .env file in the root directory and add your API key:

Code snippet
GEMINI_API_KEY=your_actual_api_key_here
4. Run the Application (Locally)
Terminal 1 (Backend):

Bash
python app.py
Terminal 2 (Frontend):

Bash
streamlit run ui.py
🌐 Deployment
This project is configured for deployment on Render using a monolithic Procfile to run both the Flask backend and Streamlit frontend concurrently.

🤝 Acknowledgments
Part of the Engineering Management (ME-EM) coursework. Special thanks to the open-source community for LangChain and Streamlit.


---

### Why this README helps you:
1.  **Professionalism:** It shows you understand the standard software development lifecycle.
2.  **Architecture:** By listing the "Tech Stack," you are pre-answering many viva questions about which models and databases you used.
3.  **Clarity:** It clearly explains that this is a **RAG** system, which is the "star" of your project.



**Pro-Tip:** Once you save this file, run these commands to update your GitHub repo:
```bash
git add README.md
git commit -m "Add project documentation"
git push origin main
