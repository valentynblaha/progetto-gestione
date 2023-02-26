"""Flask app for testing"""
from flask import Flask, request, render_template, jsonify, send_from_directory
from ysa.indexing import VideoSearcher

app = Flask(__name__, template_folder='server/templates', static_folder='server/static')
searcher = VideoSearcher('indexdir')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search():
    args = request.args
    query = args.get('q', '', type=str)
    results = [result.fields() for result in searcher.search(searcher.parse_query(query))]
    return jsonify(results)


@app.route('/data/<path:path>')
def custom_static(path):
    return send_from_directory('data', path)