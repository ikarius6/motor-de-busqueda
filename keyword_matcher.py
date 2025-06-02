class KeywordMatcher:
    def __init__(self, rating_patterns, price_patterns=None):
        self.rating_patterns = rating_patterns
        self.price_patterns = price_patterns

    def infer_min_rating(self, query):
        q = query.lower()
        for rating, keywords in self.rating_patterns.items():
            for word in keywords:
                if word in q:
                    return rating
        return 3

    def infer_price_range(self, query):
        q = query.lower()
        for price, keywords in self.price_patterns.items():
            for word in keywords:
                if word in q:
                    return price
        return '$$'