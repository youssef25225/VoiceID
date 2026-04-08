import faiss
import numpy as np

try:
    from core.features import EMBEDDING_DIM as _DIM
except ImportError:
    _DIM = 512


class VoiceModel:
    dim = _DIM

    def __init__(self):
        self.index       = faiss.IndexFlatIP(self.dim)
        self.labels      = []
        self.id_to_label = {}
        self.counter     = 0

    @property
    def n_speakers(self):
        return len(set(self.labels))

    @property
    def n_vectors(self):
        return self.index.ntotal

    def _add(self, name: str, embedding: np.ndarray):
        vec = np.array([embedding], dtype="float32")
        faiss.normalize_L2(vec)
        self.index.add(vec)
        self.id_to_label[self.counter] = name
        self.labels.append(name)
        self.counter += 1

    def enroll(self, name: str, embedding: np.ndarray):
        self._add(name, embedding)

    def rebuild(self, enrolled: dict):
        self.index       = faiss.IndexFlatIP(self.dim)
        self.labels      = []
        self.id_to_label = {}
        self.counter     = 0
        for name, embeddings in enrolled.items():
            for emb in embeddings:
                self._add(name, emb)

    def predict(self, embedding: np.ndarray, k: int = 3, threshold: float = 0.75):
        if self.index.ntotal == 0:
            return "Unknown", 0.0, {}

        k     = min(k, self.index.ntotal)
        query = np.array([embedding], dtype="float32")
        faiss.normalize_L2(query)

        D, I = self.index.search(query, k)

        votes: dict[str, float] = {}
        for i, idx in enumerate(I[0]):
            if idx == -1:
                continue
            name  = self.id_to_label[idx]
            score = float(D[0][i])
            votes[name] = votes.get(name, 0.0) + score

        best       = max(votes, key=votes.__getitem__)
        best_score = float(D[0][0])

        if best_score < threshold:
            return "Unknown", best_score, votes

        return best, best_score, votes