# Document Q&A Bot (RAG)

A beginner project: ask questions about a PDF and get answers based only on its contents. It uses RAG (Retrieval-Augmented Generation) with Claude.

## How it works

1. **Read**: extracts the text from `document.pdf`
2. **Cut**: splits the text into overlapping 500-character pieces
3. **Index**: turns each piece into an embedding (a numeric "meaning fingerprint") and stores it in ChromaDB
4. **Find**: embeds your question and retrieves the 3 most similar pieces
5. **Ask**: sends those pieces plus your question to Claude, with the instruction to answer only from that context

If the answer isn't in the document, the bot says so instead of guessing.

## Tech used

- Python 3.12
- [Anthropic API](https://docs.anthropic.com) (Claude Haiku 4.5)
- ChromaDB (vector store, runs in memory)
- sentence-transformers (`all-MiniLM-L6-v2`, free, runs locally)
- pypdf (PDF text extraction)

## Setup

1. Clone this repository and open the folder in a terminal.
2. (Recommended) Create and activate a clean environment, for example with conda:
```
   conda create -n docbot python=3.12 -y
   conda activate docbot
```
3. Install the tools:
```
   pip install -r requirements.txt
```
4. Create a file named `.env` in the project folder:
```
   ANTHROPIC_API_KEY=your-key-here
   ANTHROPIC_WORKSPACE_ID=your-workspace-id-here
```
   Get a key at [console.anthropic.com](https://console.anthropic.com). The workspace ID line is only needed if your API key is not scoped to a workspace. Never share or commit your `.env` file.
5. Put your PDF in the project folder and name it `document.pdf`.

## Run

```
python bot.py
```

Wait for "Bot is ready!", then type a question. Type `quit` to exit.

## Limitations

- Works only with PDFs that contain selectable text (not scans or photos of paper).
- Text inside images and charts is not read.
- Only the 3 best-matching pieces are sent to Claude, so questions that need information from across the whole document (such as totals or summaries) may be answered poorly.
- The index is rebuilt every time the bot starts.
- Your document's text is sent to Anthropic's API when you ask a question. Don't use confidential files unless your policies allow it.

## Ideas for next steps

- Show which page each answer came from (citations)
- Support several files and a web interface
- Better retrieval (hybrid search, reranking)