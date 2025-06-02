import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import spacy
from spacy.matcher import Matcher
import json
import os
from fuzzy_matcher import FuzzyMatcher
from embedding_matcher import EmbeddingMatcher
from keyword_matcher import KeywordMatcher
from collections import Counter
from mapbox_utils import geocode_location
from patterns import rating_patterns, price_patterns
from extract_location import ExtractLocation

class SearchEngine:
    def __init__(self, embedding_file='category_embeddings.npy', metadata_file='category_metadata.json'):
        self.embedding_file = embedding_file
        self.metadata_file = metadata_file
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.nlp = spacy.load('es_core_news_sm')
        self.index = None
        self.categories = None
        self.embeddings = None
        self.keyword_matcher = KeywordMatcher(rating_patterns, price_patterns)
        self.fuzzy_matcher = FuzzyMatcher(rating_patterns, price_patterns)
        self.semantic_matcher = EmbeddingMatcher(
            rating_patterns,
            model=self.model,
            nlp=self.nlp,
            price_emb_file='price_embeddings.npy',
            price_label_file='price_labels.npy'
        )
        self.matcher = Matcher(self.nlp.vocab)
        self.extract_location = ExtractLocation(self.nlp, self.matcher)
        self._load_data()

    def _load_data(self):
        if not (os.path.exists(self.embedding_file) and os.path.exists(self.metadata_file)):
            raise FileNotFoundError('Embeddings o metadata no encontrados. Ejecuta sync.py primero.')
        self.embeddings = np.load(self.embedding_file)
        with open(self.metadata_file, encoding='utf-8') as f:
            self.categories = json.load(f)
        # Normalizar embeddings y crear el índice FAISS
        self.embeddings = self.embeddings.astype('float32')
        self.index = faiss.IndexFlatIP(self.embeddings.shape[1])
        faiss.normalize_L2(self.embeddings)
        self.index.add(self.embeddings)
        

    def _lemmatize(self, text):
        doc = self.nlp(text)
        return ' '.join([t.lemma_ for t in doc])

    def infer_min_rating(self, query):
        keyword_rating = self.keyword_matcher.infer_min_rating(query)
        fuzzy_rating = self.fuzzy_matcher.infer_min_rating(query)
        semantic_rating = self.semantic_matcher.infer_min_rating(query)
        ratings = [keyword_rating, fuzzy_rating, semantic_rating]
        weights = [0.4, 0.3, 0.3]
        avg = round(sum(r * w for r, w in zip(ratings, weights)))
        return min(max(avg, 3), 5)

    def infer_price_range(self, query):
        keyword_price = self.keyword_matcher.infer_price_range(query)
        fuzzy_price = self.fuzzy_matcher.infer_price_range(query)
        semantic_price = self.semantic_matcher.infer_price_range(query)
        prices = [keyword_price, fuzzy_price, semantic_price]
        count = Counter(prices)
        most_common = count.most_common(1)[0][0]
        return most_common

    def infer_location(self, query):
        location = self.extract_location.extract_location(query)
        if location:
            coords = geocode_location(f"{location}, México")
            if coords:
                lat, lng = coords
                return {
                    'address': location,
                    'lat': lat,
                    'lng': lng
                }
        return None

    def search(self, query, top_k=1):
        # Lematizar y vectorizar la consulta
        lemmatized_query = self._lemmatize(query)
        query_embedding = self.model.encode([lemmatized_query], normalize_embeddings=True).astype('float32')
        faiss.normalize_L2(query_embedding)
        D, I = self.index.search(query_embedding, top_k)
        idx = I[0][0]
        category = self.categories[idx]
        min_rating = self.infer_min_rating(query)
        price_range = self.infer_price_range(query)
        location = self.infer_location(query)
        result = {
            'category': category,
            'min_rating': min_rating,
            'price_range': price_range,
            'location': {
                'address': location if location else None
            },
            'score': float(D[0][0])
        }
        return result
