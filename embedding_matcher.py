import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

class EmbeddingMatcher:
    def __init__(self, patterns, model=None, emb_file='rating_embeddings.npy', label_file='rating_labels.npy', nlp=None,
                 price_emb_file='price_embeddings.npy', price_label_file='price_labels.npy'):
        self.patterns = patterns
        self.model = model or SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.pattern_embeddings = np.load(emb_file)
        self.pattern_ratings = np.load(label_file)
        self.nlp = nlp  # Puede ser None, pero si se pasa, se usará para lematizar
        self.threshold = 0.3
        # Para price_range
        self.price_embeddings = np.load(price_emb_file)
        self.price_labels = np.load(price_label_file)
        print('[EmbeddingMatcher] Embeddings shape:', self.pattern_embeddings.shape)
        print('[EmbeddingMatcher] Ratings shape:', self.pattern_ratings.shape)
        print('[EmbeddingMatcher] Ratings:', self.pattern_ratings)
        print('[EmbeddingMatcher] Price embeddings shape:', self.price_embeddings.shape)
        print('[EmbeddingMatcher] Price labels:', self.price_labels)

    def infer_min_rating(self, query):
        # Lematizar si hay nlp (spacy)
        if self.nlp is not None:
            query_proc = ' '.join([t.lemma_ for t in self.nlp(query)])
        else:
            query_proc = query
        query_emb = self.model.encode([query_proc], normalize_embeddings=True)
        # Similitud coseno con faiss si está disponible
        if 'faiss' in globals():
            index = faiss.IndexFlatIP(self.pattern_embeddings.shape[1])
            faiss.normalize_L2(self.pattern_embeddings)
            faiss.normalize_L2(query_emb)
            index.add(self.pattern_embeddings)
            D, I = index.search(query_emb, 1)
            best_idx = I[0][0]
            score = D[0][0]
        else:
            scores = np.dot(self.pattern_embeddings, query_emb[0])
            best_idx = np.argmax(scores)
            score = scores[best_idx]
        print(f'[EmbeddingMatcher] Best match: rating={self.pattern_ratings[best_idx]}, score={score}')
        if score > self.threshold:
            return int(self.pattern_ratings[best_idx])
        return 3

    def infer_price_range(self, query):
        # Lematizar si hay nlp (spacy)
        if self.nlp is not None:
            query_proc = ' '.join([t.lemma_ for t in self.nlp(query)])
        else:
            query_proc = query
        query_emb = self.model.encode([query_proc], normalize_embeddings=True)
        # Similitud coseno con faiss si está disponible
        if 'faiss' in globals():
            index = faiss.IndexFlatIP(self.price_embeddings.shape[1])
            faiss.normalize_L2(self.price_embeddings)
            faiss.normalize_L2(query_emb)
            index.add(self.price_embeddings)
            D, I = index.search(query_emb, 1)
            best_idx = I[0][0]
            score = D[0][0]
        else:
            scores = np.dot(self.price_embeddings, query_emb[0])
            best_idx = np.argmax(scores)
            score = scores[best_idx]
        print(f'[EmbeddingMatcher] Best match: price={self.price_labels[best_idx]}, score={score}')
        if score > self.threshold:
            return self.price_labels[best_idx]
        return '$$'