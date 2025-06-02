# patterns.py

rating_patterns = {
    5: [
        "mejor", "excelente", "cinco estrellas", "top", "premium", "profesional", "certificado", "recomendado",
        "increíble", "superior", "destacado", "insuperable", "de lujo", "de primera", "óptimo", "excepcional"
    ],
    4: [
        "bueno", "recomendable", "calidad", "confiable", "serio", "correcto", "cumplidor", "aprobado",
        "satisfactorio", "adecuado", "aceptable", "agradable", "respetable", "decente"
    ],
    3: [
        "barato", "económico", "accesible", "básico", "sencillo", "simple", "modesto", "regular",
        "estándar", "común", "normalito", "normal", "promedio"
    ]
}

price_patterns = {
    '$': [
        "barato", "económico", "accesible", "low cost", "más barato", "asequible", "de oferta", "rebajado",
        "económica", "precio bajo", "precio reducido", "costo bajo", "descuento", "ahorro"
    ],
    '$$$': [
        "caro", "premium", "exclusivo", "de lujo", "alto costo", "alto precio", "costoso", "gama alta",
        "elevado", "lujoso", "de élite", "de prestigio", "selecto", "exquisito"
    ],
    '$$': [
        "normal", "precio medio", "regular", "promedio", "intermedio", "estándar", "ni caro ni barato", "balanceado",
        "precio justo", "razonable", "acorde", "ajustado", "media gama"
    ]
}

