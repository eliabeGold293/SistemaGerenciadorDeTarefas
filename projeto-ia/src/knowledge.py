# src/knowledge.py
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.db.sqlite.sqlite import SqliteDb

from config import settings


def get_contents_db():
    return SqliteDb(
        db_file='data/sqlite/contents.db'
    )

def get_vector_db():
    vector_db = ChromaDb(
        collection='vertice_documention',
        path='data/chromadb',
        persistent_client=True,
        embedder=GeminiEmbedder(
            api_key=settings.GOOGLE_API_KEY
        ),
    )
    return vector_db

def get_knowledge():
    knowledge = Knowledge(
        vector_db=get_vector_db(),
        contents_db=get_contents_db(),
    )

    knowledge.add_contents(
        [
            {
                'path': 'documents/about.pdf',
            },
            {
                'path': 'documents/portfolio.pdf',
            },
            {
                'path': 'documents/services.pdf',
            }
        ],
        skip_if_exists=True
    )
    return knowledge