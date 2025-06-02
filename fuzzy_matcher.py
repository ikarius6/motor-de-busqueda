from fuzzywuzzy import fuzz
import re

class FuzzyMatcher:
    def __init__(self, patterns, price_patterns=None, threshold=80):
        self.patterns = patterns
        self.price_patterns = price_patterns
        self.threshold = threshold

    def infer_min_rating(self, query):
        query_clean = re.sub(r'[^\w\s]', '', query.lower())
        words = query_clean.split()
        
        best_rating = 3
        best_score = 0
        
        for rating, patterns in self.patterns.items():
            for pattern in patterns:
                for word in words:
                    score = fuzz.ratio(pattern, word)
                    if score > self.threshold and score > best_score:
                        best_score = score
                        best_rating = rating
        return best_rating

    def infer_price_range(self, query):
        query_clean = re.sub(r'[^\w\s]', '', query.lower())
        words = query_clean.split()
        best_price = '$$'
        best_score = 0

        for price, patterns in self.price_patterns.items():
            for pattern in patterns:
                for word in words:
                    score = fuzz.ratio(pattern, word)
                    if score > self.threshold and score > best_score:
                        best_score = score
                        best_price = price
        return best_price