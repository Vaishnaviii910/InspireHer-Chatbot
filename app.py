import os
import json
import glob
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Modern SDKs
from google import genai
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# -------------------------------
# CONFIG
# -------------------------------
load_dotenv()
app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env")

# New Client Setup
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_ID = "gemini-2.5-flash"

# -------------------------------
# DOCUMENTS
# -------------------------------
def load_documents():
    documents = []
    
    # PDF
    if os.path.exists("scheme.pdf"):
        loader = PyPDFLoader("scheme.pdf")
        documents.extend(loader.load())
        print("✅ Loaded PDF")

    # JSON (Improved formatting)
    if os.path.exists("governmentschemes.json"):
        with open("governmentschemes.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            items = data if isinstance(data, list) else [data]
            for item in items:
                content = "\n".join([f"{k}: {v}" for k, v in item.items()])
                documents.append(Document(page_content=content))
        print("✅ Loaded JSON")

    # TXT
    for file in glob.glob("*.txt"):
        loader = TextLoader(file, encoding="utf-8")
        documents.extend(loader.load())
        print(f"✅ Loaded {file}")

    return documents

# -------------------------------
# VECTOR DB SETUP
# -------------------------------
def get_vector_db():
    # Explicitly naming the model ensures the dimension (384) stays consistent
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    persist_dir = "chroma_db"

    if os.path.exists(persist_dir) and len(os.listdir(persist_dir)) > 0:
        print("🔍 Loading existing Vector DB...")
        return Chroma(persist_directory=persist_dir, embedding_function=embeddings)

    print("🏗️ Creating new Vector DB...")
    docs = load_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=70)
    split_docs = splitter.split_documents(docs)

    return Chroma.from_documents(
        documents=split_docs, 
        embedding=embeddings, 
        persist_directory=persist_dir
    )

# Global initialization
vector_db = get_vector_db()
retriever = vector_db.as_retriever(search_kwargs={"k": 3})

# -------------------------------
# AI LOGIC
# -------------------------------
def generate_answer(query, context):
    prompt = f"""
    You are InspireHer AI, an assistant for rural women in India.
    Use the CONTEXT to answer the QUESTION.
    If the answer is not in the context, say you don't know.

    CONTEXT:
    {context}

    QUESTION:
    {query}
    """

    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# -------------------------------
# ROUTES
# -------------------------------
@app.route("/", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        query = data.get("query")
        
        if not query:
            return jsonify({"error": "No query provided"}), 400

        # RAG process
        docs = retriever.invoke(query)
        context = "\n---\n".join([d.page_content for d in docs])
        
        answer = generate_answer(query, context)
        return jsonify({"response": answer})

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)