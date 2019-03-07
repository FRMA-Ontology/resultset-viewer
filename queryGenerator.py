from SPARQLWrapper import SPARQLWrapper, JSON
from anytree import Node, RenderTree, PreOrderIter
import query

rootNode = Node("thing")
nodes = {"thing" : rootNode}


def getModifer(modiferIRI):
    return query.querymapper[modiferIRI]

def generateQuery(limit, resultset, modiferIRIs):
    buildableQuery = query.baseQuery
    for modiferIRI in modiferIRIs:
        buildableQuery = buildableQuery + "\n" + getModifer(modiferIRI)

    return buildableQuery + "\n" + "bind( <" + resultset + "> as ?ResultSet)} limit " + str(limit)

def generateTree(blazegraphURL, tree):
   sparql = SPARQLWrapper(blazegraphURL)
   sparql.setQuery(query.treeClassQuery)

   sparql.setReturnFormat(JSON)
   results = sparql.query().convert()

   depend = []
   # Add in all top level nodes and capture the rest of the dependencies
   for result in results["results"]["bindings"]:
       classIRI = result["class"]["value"]
       className = result["name"]["value"]
       if len(result) == 2: # We have a super class
           nodes[classIRI] = Node(classIRI, parent=rootNode, label=className)
       else:
           superIRI = result["super"]["value"]
           superName = result["super_name"]["value"]
           depend.append((classIRI, className, superIRI))

   # Handle all nodes that have parents
   while(len(depend) > 0):
       for i in range(len(depend)):
           if depend[i][2] in nodes.keys():
               nodes[depend[i][0]] = Node(depend[i][0], parent=nodes[depend[i][2]], label=depend[i][1])
               del depend[i]
               break

   # print tree to console
   for pre, fill, node in RenderTree(rootNode):
       print("%s%s" % (pre, vars(node).get("label")))

   for node in PreOrderIter(rootNode):
       if node.is_root:
           tree.insert('', 'end', node.name, text = "thing")
       else:
           tree.insert(node.parent.name, 'end', node.name, text = vars(node).get("label"))

   return 0
