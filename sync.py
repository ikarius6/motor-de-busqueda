import numpy as np
from sentence_transformers import SentenceTransformer
import spacy
import json
from categories import categories
from patterns import rating_patterns, price_patterns

# Simulación de categorías y metadatos
nlp = spacy.load('es_core_news_sm')
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Procesar y lematizar descripciones
lemmatized = [' '.join([t.lemma_ for t in nlp(text)]) for text in categories]

# Calcular embeddings de categorías
embeddings = model.encode(lemmatized, normalize_embeddings=True)

# Guardar embeddings y metadatos de categorías
np.save('category_embeddings.npy', embeddings)
with open('category_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(categories, f, ensure_ascii=False, indent=2)

# Precalcular embeddings de patrones de rating (lematizados)
rating_texts = []
rating_labels = []
for rating, keywords in rating_patterns.items():
    for word in keywords:
        lemma = ' '.join([t.lemma_ for t in nlp(word)])
        rating_texts.append(lemma)
        rating_labels.append(rating)
rating_embeddings = model.encode(rating_texts, normalize_embeddings=True)
np.save('rating_embeddings.npy', rating_embeddings)
np.save('rating_labels.npy', np.array(rating_labels))

# Precalcular embeddings de patrones de price_range (lematizados)
price_texts = []
price_labels = []
for price, keywords in price_patterns.items():
    for word in keywords:
        lemma = ' '.join([t.lemma_ for t in nlp(word)])
        price_texts.append(lemma)
        price_labels.append(price)
price_embeddings = model.encode(price_texts, normalize_embeddings=True)
np.save('price_embeddings.npy', price_embeddings)
np.save('price_labels.npy', np.array(price_labels))

print('Embeddings y metadatos guardados.')
