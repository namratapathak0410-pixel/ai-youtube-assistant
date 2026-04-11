import faiss
import numpy as np
from src.embeddings.transformer import get_embedding

class FAISSStore:
    def __init__(self, dim=128):
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []

    def add(self, chunks):
        vectors = []
        for chunk in chunks:
            vec = get_embedding(chunk.page_content)
            vectors.append(vec)
            self.texts.append(chunk.page_content)

        self.index.add(np.array(vectors))

    def search(self, query, k=3):
        q_vec = get_embedding(query)
        D, I = self.index.search(np.array([q_vec]), k)
        return [self.texts[i] for i in I[0]]