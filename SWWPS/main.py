from flask import Flask, jsonify
import requests
import json
import urllib
import re
from fuzzywuzzy import fuzz, process
app = Flask(__name__)

@app.route('/')
def index():
  return 'API for Semantic Web Word Processing Support'

@app.route('/get_entity_name/<keyword>')
def get_entity_name(keyword):
  uri = 'https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch=' + keyword + '&srprop=&srlimit=3'
  try:
    res = requests.get(uri)
  except requests.ConnectionError:
    return "Connection Error"  
  data = json.loads(res.text)
  if 'suggestion' in data['query']['searchinfo']:
    return get_entity_name(data['query']['searchinfo']['suggestion'])
  else:
    return data['query']['search'][0]['title']

@app.route('/get_entity_property_list/<entity_name>')
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

  return json.dumps(property_names)

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

@app.route('/test/<entity_name>')
def get_entity_property_list_test(entity_name):
  refined_entity_name = get_entity_name(entity_name)
  f_entity_name = urllib.unquote(refined_entity_name).decode('utf8').replace(" ","_")
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

  splited = []
  for name in property_names:
    splited.append(camel_case_split(name))

  matches = ''
  splited_entity_name = urllib.unquote(entity_name).decode('utf8').replace(" ","_").rsplit('_of_', 1)
  if len(splited_entity_name) > 1:
    keyword = splited_entity_name[0]
    matches = '<br>"'+keyword+'"<br>'
    for name in splited:
      matches += name + '<br>'
      matches += 'Ratio: '+str(fuzz.ratio(keyword, name))
      matches += '    Partial Ratio: '+str(fuzz.partial_ratio(keyword, name))
      matches += '    token_sort_ratio: '+str(fuzz.token_sort_ratio(keyword, name))
      matches += '    token_set_ratio: '+str(fuzz.token_set_ratio(keyword, name))
      matches += '<br>'
  # matches = process.extract('population', property_names)
  j = []
  if entity_name == 'China':
    keyword = 'population'
    matches = '<br>"'+keyword+'"<br>'
    for name in splited:
      if 'population' in name:
        j.append({
            'label': name,
            'value': name
          })
      matches += name + '<br>'
      matches += 'Ratio: '+str(fuzz.ratio(keyword, name))
      matches += '    Partial Ratio: '+str(fuzz.partial_ratio(keyword, name))
      matches += '    token_sort_ratio: '+str(fuzz.token_sort_ratio(keyword, name))
      matches += '    token_set_ratio: '+str(fuzz.token_set_ratio(keyword, name))
      matches += '<br>'

  return json.dumps(j)
  # return '<br>'.join(property_names) + '<br><br>Matches:<br>' + matches + entity_name + '<br>' + json.dumps(splited)

def camel_case_split(identifier):
  matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
  return ' '.join([m.group(0).lower() for m in matches])










