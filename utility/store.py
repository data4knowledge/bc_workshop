from utility.neo4j_connection import Neo4jConnection

class Store():

  def __init__(self):
    self.nodes = {}
    self.relationships = {}
    self.node_id = 0

  def node(self, cls, data):
    klass = self.class_as_str(cls)
    if not klass in self.nodes:
      self.nodes[klass] = []
    if not '_id' in data or data['_id'] == None:
      data['_id'] = self.get_node_id()
    self.nodes[klass].append(data)
    return data['_id']
  
  def get_node_id(self):
    self.node_id += 1
    return self.node_id
  
  def relationship(self, from_id, to_id, relationship):
    if not relationship in self.relationships:
      self.relationships[relationship] = []
    data = { 'from': from_id, 'to': to_id }
    self.relationships[relationship].append(data)

  def link(self, from_id, to_id, relationship):
    if from_id == None or to_id == None:
      return 
    else:
      self.relationship(str(from_id), str(to_id), relationship)

  def class_as_str(self, cls):
    if isinstance(cls, str):
      return cls
    else:
      return cls.__name__

  def push(self, clear=False):
    print("A")
    db = Neo4jConnection()
    if clear:
      db.clear()
    print("B")
    tx = db.transaction()
    for key, rows in self.nodes.items():
      query = """
        UNWIND $data AS row
        CREATE (n:%s) SET n += row
      """ % (key)
      tx.run(query, data=rows)
    print("C")
    for key, rows in self.relationships.items():
      query = """
        UNWIND $data AS row
        MATCH (n {_id: row.from}), (m {_id: row.to})
        CREATE (n)-[:%s]->(m)
      """ % (key)
      tx.run(query, data=rows)
    print("D")
    db.commit(tx)
    print("E")

  def __str__(self):
    result = ""
    for key, rows in self.nodes.items():
      for row in rows:
        result += "%s: %s\n" % (key, row)
    for key, rows in self.relationships.items():
      for row in rows:
        result += "%s: %s\n" % (key, row)
    return result