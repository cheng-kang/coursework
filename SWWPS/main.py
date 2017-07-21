from flask import Flask, jsonify
import requests
import json
import urllib
app = Flask(__name__)

@app.route('/')
def index():
  return 'REST API for Semantic Web Word Processing Support'

@app.route('/entity/<entity_name>')
def get_entity(entity_name):
  uri = 'https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch=' + entity_name + '&srprop=&srlimit=3'
  try:
    res = requests.get(uri)
  except requests.ConnectionError:
    return "Connection Error"  
  data = json.loads(res.text)
  if 'suggestion' in data['query']['searchinfo']:
    return 'Suggestion: ' + data['query']['searchinfo']['suggestion'] + '<br>' + get_entity(data['query']['searchinfo']['suggestion'])
  else:
    return 'Search result #1: ' + data['query']['search'][0]['title']
  # return json.dumps(data)

@app.route('/entity/<entity_name>/property_list')
def get_entity_property_list(entity_name):
  f_entity_name = urllib.unquote(entity_name).decode('utf8').replace(" ","_")
  uri = 'http://dbpedia.org/data/' + f_entity_name + '.json'
  try:
    res = requests.get(uri)
  except requests.ConnectionError:
    return "Connection Error"
  # return res.text
  data = json.loads(res.text)
  key = 'http://dbpedia.org/resource/' + f_entity_name
  def get_property_name(url):
    property_name = url.rsplit('/', 1)[-1]
    property_name = property_name.rsplit('#', 1)[-1]
    return property_name
  property_names = list(map(get_property_name, data[key].keys()))

  return '<br>'.join(property_names)