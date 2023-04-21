import json
from utility.store import Store

store = Store()

def save_json(data, filename):
  with open(filename, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

def read_json(filename):
  with open(filename) as f:
    return json.load(f)

def process_node(node, parent_key):
  if type(node) == list:
    results = []
    for item in node:
      result = process_node(item, parent_key)
      if result == None:
        pass
      else:
        results += result
    return results
  elif type(node) == dict:
    properties = {}
    links = {}
    for key, value in node.items():
      result = process_node(value, key)
      if result == None:
        properties[key] = value
      elif result == []:
        properties[key] = value
      else:
        links[key] = result
    new_node = store.node(klass(properties, parent_key), properties)
    for rel, end_ids in links.items():
      for end_id in end_ids:
        store.relationship(new_node, end_id, rel)
    return [new_node]
  else:
    return None
  
def klass(properties, parent_key):
  if '_type' in properties:
    return properties['_type']
  else:
    return parent_key
  
data = read_json('source_data/cdisc_lib.json')
process_node(data, "root")
print(store)
try:
  store.push(clear=True)
except Exception as e:
  print("Exception")
  print(e)
