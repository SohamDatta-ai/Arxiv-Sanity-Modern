# Arxiv Sanity Modern

A local research assistant for managing and discovering Arxiv papers, inspired by the original Arxiv Sanity Preserver.

## Overview

Arxiv Sanity Modern addresses the challenge of information overload in scientific research. It indexes papers locally using semantic embeddings, allowing researchers to search by concept rather than keyword and receive personalized recommendations based on their library.

The project is built with a focus on speed, privacy, and simplicity. It uses FastAPI for the backend, HTMX for a responsive frontend, and SQLite for data storage.

## Key Features

*   **Semantic Search**: Utilizes `sentence-transformers` to understand the meaning of queries, retrieving relevant papers even if they do not match exact keywords.
*   **Personalization**: Analyzes saved papers to generate a custom feed of recommended research.
*   **Local Processing**: All embeddings and data storage occur locally on the user's machine.
*   **Performance**: Designed for minimal latency with a lightweight technology stack.

## Installation

### Option 1: Docker (Recommended)

Run the application using Docker Compose:

```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`.

### Option 2: Python (Manual)

1.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Fetch and index the latest papers:
    ```bash
    python scripts/fetch_papers.py
    ```

3.  Start the server:
    ```bash
    python -m app.main
    ```

## Usage

1.  **Search**: Use the search bar to find papers.
2.  **Save**: Click the "save" link on any paper to add it to your library. First-time users can create an account via the "Login or Create" button.
3.  **Recommendations**: Navigate to the "Recommended" tab to view papers similar to those in your library.

## Status

**Work in Progress (WIP)**. This project is currently in active development.

## Author

Soham Datta
