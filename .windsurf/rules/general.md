---
trigger: manual
---

Estamos creando un search engine basado en inteligencia articial

Estamos trabajando con:
Python 3.10.5
spaCy 3.8.5
SentenceTransformers 4.1.0
FAISS 1.11.0
Numpy 2.2.4
Flask 3.1.1

Estamos trabajando en español, por lo que necesitamos modelos de embedding que soporten español

La estructura de la base de datos está en directory_dump.sql

Para conectar a la base de datos usamos el .env
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=

La estructura base:
search_engine.py # clase principal del search engine
main.py # archivo para probar el código
app.py # para levantar el flask
sync.py # para sincronizar los embeddings

almacenamos los embedings en:
category_embeddings.npy

El objetivo del search engine es reconocer los intents del usuario sobre su busqueda.

Ejemplo: "plomeros buenos y baratos en querétaro"

Resultado:
{
category: "plomero", // categoria plomero de la db
min_rating: 5, // 5 de 5 estrellas
price_range: '$', //$ económico, $$ normal, $$$ caro
location: {
addres: "querétaro",
lat: 20.5478615,
lng: -100.4200734
}
}

Para obtener la latitud y longitud podemos usar api.mapbox.com, tenemos el apikey en el .env