# Motor de Búsqueda

Este es un motor de búsqueda para un directorio de negocios. Utiliza una combinación de coincidencia por palabras clave, coincidencia difusa y coincidencia semántica para encontrar los mejores resultados para una consulta dada.

## Instalación

```bash
pip install -r requirements.txt
```

Instala el modelo de spacy con español.

```bash
python -m spacy download es_core_news_sm
```

Establece tu clave de API de Mapbox en el archivo `.env`.

## Uso

Ejecuta primero el script de sincronización para crear los archivos de *embeddings* y metadatos.

```bash
python sync.py
```

Luego ejecuta la aplicación.

```bash
python app.py
```

Prueba la API con:

```bash
http GET http://localhost:5001/search?q=excelente%20jardinero,%20barato%20por%20el%20centro
```

## Licencia

MIT

## Autor

Mr.Jack (ikarius6)
