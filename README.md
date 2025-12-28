# Arxiv Sanity Modern 🧠

> **Your personal research assistant. Like Spotify, but for Arxiv papers.**

Finding good papers used to be a nightmare. Now it's a vibe.

## 🌟 Highlights
*   **Semantic Search**: Type "robots" and find "automata". It understands meaning, not just keywords.
*   **Personal Feed**: Save the papers you like. The engine learns your taste and recommends hidden gems.
*   **Blazing Fast**: Built with **FastAPI** & **HTMX**. Loads locally in milliseconds. No tracking, no ads.
*   **Local First**: Your data stays on your machine. Powered by `sentence-transformers`.

## ℹ️ Overview
**The Problem**: Arxiv.org is a firehose. 200+ new AI papers drop daily. It's impossible to keep up using just a chronological list.

**The Solution**: An intelligent interface that acts as a noise filter.

I rebuilt Andrej Karpathy's legendary *Arxiv Sanity Preserver* using modern 2025 tech. It's designed for researchers, students, and curious minds who want to spend their time **reading**, not searching.

## 🚀 Usage
The workflow is simple:
1.  **Search**: Type `transformers` or `computer vision` to filter the noise.
2.  **Curate**: Click **[save]** on papers that look interesting. *(Auto-login included!)*
3.  **Discover**: Go to the **Recommended** tab. It uses vector math to find papers "mathematically similar" to your library.

## ⬇️ Installation
You can get this running in 2 minutes.

### 🐳 The Easy Way (Docker)
```bash
docker-compose up --build
```
Open **[http://localhost:8000](http://localhost:8000)**. That's it.

### 🐍 The Python Way
If you prefer running it raw:
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Fetch Data (Get the latest 100 papers)
python scripts/fetch_papers.py

# 3. Run
python -m app.main
```

## ✍️ Author
Built by **Soham Datta**.
I built this because I was drowning in browser tabs and needed a better way to organize my reading list. It is a personal project I'm sharing with the world.

**⚠️ Status**: Work in Progress (WIP). It works great on my machine, but it's not Enterprise SaaS yet!

## 💭 Contribute
Found a bug? Want to add a feature?
Feel free to open an Issue or submit a PR! I'd love to hear your feedback on how we can make research easier for everyone.
