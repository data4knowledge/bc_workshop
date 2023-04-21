import json

def save_json(data, filename):
  with open(filename, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

def read_json(filename):
  with open(filename) as f:
    return json.load(f)

nodes = {}
nodes_ref = {}
file_path = "NN_BC_sandbox.json"
bc = read_json(file_path)
for item in bc["nodes"]:
  id = item['id']
  data = item['properties'] if 'properties' in item else {}
  #nodes[id] = { 'name': item['labels'][0], 'data': data }
  nodes[id] = data
  nodes [id]['type'] = item['labels'][0]
  nodes_ref[id] = False
for item in bc["rels"]:
  start = item['start']
  end = item['end']
  rel = item['label']
  #nodes[start['id']]['data'][rel.lower()] = nodes[end['id']]
  if not rel.lower() in nodes[start['id']]:
    nodes[start['id']][rel.lower()] = []
  nodes[start['id']][rel.lower()].append(nodes[end['id']])
  nodes_ref[end['id']] = True
for k,v in nodes_ref.items():
  if v == False:
    print(nodes[k])