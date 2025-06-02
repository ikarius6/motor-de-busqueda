class ExtractLocation:
    def __init__(self, nlp, matcher):
        self.nlp = nlp
        self.matcher = matcher
        # Patrones mejorados para ubicaciones mexicanas para spacy
        patterns = [
            # Colonias: "en la colonia del valle" -> captura "del valle"
            [{"LOWER": {"IN": ["en", "de", "por", "cerca"]}},
            {"LOWER": {"IN": ["el", "la", "los", "las"]}, "OP": "?"},
            {"LOWER": "colonia"},
            {"IS_ALPHA": True},  # Primera palabra obligatoria
            {"IS_ALPHA": True, "OP": "*"}],  # Palabras adicionales opcionales
            
            # Calles con nombres compuestos: "calle paseo de paris"
            [{"LOWER": {"IN": ["en", "de", "por", "cerca"]}},
            {"LOWER": {"IN": ["el", "la", "los", "las"]}, "OP": "?"},
            {"LOWER": "calle"},
            {"IS_ALPHA": True},
            {"LOWER": {"IN": ["de", "del", "y"]}, "OP": "?"},
            {"IS_ALPHA": True, "OP": "*"}],
            
            # Avenidas: "avenida constituyentes del sur"
            [{"LOWER": {"IN": ["en", "de", "por", "cerca"]}},
            {"LOWER": {"IN": ["el", "la", "los", "las"]}, "OP": "?"},
            {"LOWER": {"IN": ["avenida", "av", "av."]}},
            {"IS_ALPHA": True},
            {"LOWER": {"IN": ["de", "del", "y"]}, "OP": "?"},
            {"IS_ALPHA": True, "OP": "*"}],
            
            # Sin preposición inicial: "colonia del valle"
            [{"LOWER": {"IN": ["colonia", "calle", "avenida", "av", "av."]}},
            {"IS_ALPHA": True},
            {"LOWER": {"IN": ["de", "del", "y"]}, "OP": "?"},
            {"IS_ALPHA": True, "OP": "*"}],
            
            # Zonas: "zona centro histórico"
            [{"LOWER": {"IN": ["en", "de", "por", "cerca"]}},
            {"LOWER": {"IN": ["el", "la", "los", "las"]}, "OP": "?"},
            {"LOWER": {"IN": ["zona", "sector", "fraccionamiento", "residencial"]}},
            {"IS_ALPHA": True},
            {"IS_ALPHA": True, "OP": "*"}],
            
            # Entidades NER
            [{"LOWER": {"IN": ["en", "de", "por", "cerca"]}},
            {"LOWER": {"IN": ["el", "la", "los", "las"]}, "OP": "?"},
            {"ENT_TYPE": "LOC"}],
            
            # Patrón general más restrictivo (usar límite de tokens)
            [{"LOWER": {"IN": ["en", "de", "por", "cerca"]}},
            {"LOWER": {"IN": ["el", "la", "los", "las"]}, "OP": "?"},
            {"IS_ALPHA": True, "LENGTH": {">=": 3}},
            {"IS_ALPHA": True, "OP": "{0,3}"}],  # Máximo 3 palabras adicionales
        ]
        # Patrones específicos para cada caso
        colonia_pattern = [
            {"LOWER": {"IN": ["en", "por", "cerca"]}, "OP": "?"},
            {"LOWER": {"IN": ["la", "el"]}, "OP": "?"},
            {"LOWER": "colonia"},
            {"IS_ALPHA": True},
            {"IS_ALPHA": True, "OP": "*"}
        ]
        
        calle_pattern = [
            {"LOWER": {"IN": ["en", "por", "cerca"]}, "OP": "?"},
            {"LOWER": {"IN": ["la", "el"]}, "OP": "?"},
            {"LOWER": "calle"},
            {"IS_ALPHA": True},
            {"LOWER": {"IN": ["de", "del"]}, "OP": "?"},
            {"IS_ALPHA": True, "OP": "*"}
        ]
        
        avenida_pattern = [
            {"LOWER": {"IN": ["en", "por", "cerca"]}, "OP": "?"},
            {"LOWER": {"IN": ["la", "el"]}, "OP": "?"},
            {"LOWER": {"IN": ["avenida", "av"]}},
            {"IS_ALPHA": True},
            {"LOWER": {"IN": ["de", "del"]}, "OP": "?"},
            {"IS_ALPHA": True, "OP": "*"}
        ]
        
        # Agregar cada patrón por separado
        self.matcher.add("COLONIA", [colonia_pattern])
        self.matcher.add("CALLE", [calle_pattern])
        self.matcher.add("AVENIDA", [avenida_pattern])
        self.matcher.add("LOCATION_PATTERN", patterns)

    def extract_location(self, query):
        doc = self.nlp(query)
        
        # Primero buscar entidades nombradas de tipo LOC
        ner_locations = []
        for ent in doc.ents:
            if ent.label_ in ["LOC", "GPE"]:  # GPE = Geopolitical entities
                ner_locations.append(ent.text)
        
        # Buscar con patrones
        pattern_locations = []
        matches = self.matcher(doc)
        
        for match_id, start, end in matches:
            matched_span = doc[start:end]
            # Extraer solo la parte de ubicación (sin preposiciones)
            location = self._extract_location_from_span(matched_span)
            if location:
                pattern_locations.append(location)
        
        # Priorizar NER sobre patrones, y el primer match válido
        all_locations = ner_locations + pattern_locations
        
        # Filtrar y limpiar
        for loc in all_locations:
            cleaned = self._clean_location(loc)
            if self._is_valid_location(cleaned):
                return cleaned
                
        return None

    def _extract_location_from_span(self, span):
        """Extrae solo la parte de ubicación del span completo"""
        tokens = [token.text for token in span]
        
        # Encontrar donde empieza la ubicación real
        location_start = 0
        skip_words = {"en", "de", "por", "cerca", "el", "la", "los", "las"}
        
        # Saltar preposiciones y artículos
        while location_start < len(tokens) and tokens[location_start].lower() in skip_words:
            location_start += 1
        
        # Saltar tipo de vía si está presente
        via_types = {"colonia", "calle", "avenida", "av", "av.", "zona", "sector", "fraccionamiento"}
        if location_start < len(tokens) and tokens[location_start].lower() in via_types:
            location_start += 1
        
        # Extraer el resto como ubicación
        if location_start < len(tokens):
            location_tokens = tokens[location_start:]
            return " ".join(location_tokens)
        
        return None

    def _clean_location(self, location):
        """Limpia y normaliza la ubicación extraída"""
        if not location:
            return None
            
        # Remover espacios extra
        cleaned = " ".join(location.split())
        
        # Capitalización correcta para ubicaciones mexicanas
        words = cleaned.split()
        normalized_words = []
        
        # Palabras que deben ir en minúscula (excepto al inicio)
        lowercase_words = {"de", "del", "la", "el", "los", "las", "y", "e"}
        
        for i, word in enumerate(words):
            if i == 0:  # Primera palabra siempre capitalizada
                normalized_words.append(word.capitalize())
            elif word.lower() in lowercase_words:
                normalized_words.append(word.lower())
            else:
                normalized_words.append(word.capitalize())
        
        return " ".join(normalized_words)

    def _is_valid_location(self, location):
        """Valida si la ubicación extraída es válida"""
        if not location or len(location) < 3:
            return False
            
        # Filtrar palabras comunes que no son ubicaciones
        invalid_words = {
            "excelente", "bueno", "mejor", "cerca", "lejos", 
            "barato", "caro", "rápido", "servicio", "trabajo"
        }
        
        return location.lower() not in invalid_words