import argparse
import json
from utility.store import Store

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

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    prog='Neo4J Simple JSON Loader',
    description='Will load a JSON file into Neo4j creating nodes as per the JSON structure',
    epilog='Note: Multiple files can be loaded, you can clear the DB with the first load'
  )
  parser.add_argument('filename') 
  parser.add_argument("-s", "--start", type=int, nargs='?', default=1, help = "The starting node identifier")
  parser.add_argument('-c', "--clear", dest='clear', action=argparse.BooleanOptionalAction, help = "Clear the database")
  args = parser.parse_args()
  filename = args.filename
  clear = args.clear
  start = args.start
  store = Store(start)
  print (f"Processing {filename} with start node = {start} and DB clear = {clear} ...")
  data = read_json(f'source_data/{filename}')
  process_node(data, "root")
  print ("... Done")
  #print(store)
  try:
    store.push(clear=clear)
  except Exception as e:
    print("Exception")
    print(e)
