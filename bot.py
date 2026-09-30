import os
from dotenv import load_dotenv
import anthropic
import chromadb
from sentence_transformers import SentenceTransformer

# Load the API key from the .env file
load_dotenv()

# ---------- STEP 1: READ the document ----------
from pypdf import PdfReader

reader = PdfReader("document.pdf")
text = ""
for page in reader.pages:
    text += (page.extract_text() or "") + "\n"
print(f"Read {len(reader.pages)} pages, {len(text)} characters.")

# ---------- STEP 2: CUT it into pieces ----------
def split_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size - overlap
    return chunks

chunks = split_text(text)
print(f"Document split into {len(chunks)} pieces.")

# ---------- STEP 3: INDEX the pieces ----------
print("Loading the embedding model (first time takes a minute)...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

db = chromadb.Client()
collection = db.create_collection("docs")

embeddings = embedder.encode(chunks).tolist()
collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=[f"chunk{i}" for i in range(len(chunks))],
)

# ---------- STEP 4 + 5: FIND relevant pieces, ASK Claude ----------
claude = anthropic.Anthropic(
    default_headers={"anthropic-workspace-id": os.getenv("ANTHROPIC_WORKSPACE_ID")}
)

def ask(question):
    # Find the 3 pieces closest in meaning to the question
    q_embedding = embedder.encode([question]).tolist()
    results = collection.query(query_embeddings=q_embedding, n_results=3)
    context = "\n\n".join(results["documents"][0])

    # Build the message for Claude
    prompt = f"""Answer the question using ONLY the context below.
If the answer is not in the context, say "I couldn't find that in the document."

Context:
{context}

Question: {question}"""

    response = claude.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text

# ---------- Chat loop ----------
print("\nBot is ready!")
while True:
    question = input("\nAsk a question (or type 'quit'): ")
    if question.lower() == "quit":
        break
    print("\n" + ask(question))