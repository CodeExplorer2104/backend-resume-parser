from sentence_transformers import SentenceTransformer
import numpy as np

# Load once (important for performance)
model = SentenceTransformer('all-MiniLM-L6-v2')


def get_embedding(text):
    embedding = model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True  # VERY IMPORTANT
    )
    return embedding


def get_embeddings_batch(texts):
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    return embeddings