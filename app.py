from flask import Flask, request, jsonify
from search_engine import SearchEngine

app = Flask(__name__)
search_engine = SearchEngine()

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Missing query parameter q'}), 400
    results = search_engine.search(query)
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
