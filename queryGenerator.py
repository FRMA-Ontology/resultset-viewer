from SPARQLWrapper import SPARQLWrapper, JSON
from anytree import Node, RenderTree, PreOrderIter
import query

rootNode = Node("https://w3id.org/lio/v1#Image", label="image")
nodes = {"https://w3id.org/lio/v1#Image" : rootNode}


def getModifer(modiferIRI):
    return query.querymapper[modiferIRI]

def generateCountQuery(resultset, modiferIRIs, queryState):
    buildableQuery = query.baseCountQuery
    for modiferIRI in modiferIRIs:
        buildableQuery = buildableQuery + "\n" + getModifer(modiferIRI)

    if(queryState == "Correct"):
        buildableQuery = buildableQuery + "\n" + query.correctQuery

    if(queryState == "Incorrect"):
        buildableQuery = buildableQuery + "\n" + query.incorrectQuery

    return buildableQuery + "\n" + "bind( <" + resultset + "> as ?ResultSet)}"

def generateQuery(limit, offset, resultset, modiferIRIs, queryState):
    buildableQuery = query.baseQuery
    for modiferIRI in modiferIRIs:
        buildableQuery = buildableQuery + "\n" + getModifer(modiferIRI)

    if(queryState == "Correct"):
        buildableQuery = buildableQuery + "\n" + query.correctQuery

    if(queryState == "Incorrect"):
        buildableQuery = buildableQuery + "\n" + query.incorrectQuery

    return buildableQuery + "\n" + "bind( <" + resultset + "> as ?ResultSet)} ORDER BY ?name limit " + str(limit) + " offset " + str(offset)

def generateTree(blazegraphURL, tree):
   sparql = SPARQLWrapper(blazegraphURL)
   sparql.setQuery(query.treeClassQuery)

   sparql.setReturnFormat(JSON)
   results = sparql.query().convert()

   # Add in all top level nodes and capture the rest of the dependencies
   for result in results["results"]["bindings"]:
       classIRI = result["class"]["value"]
       className = result["name"]["value"]

       if classIRI not in nodes.keys():
           nodes[classIRI] = Node(classIRI, label=className)

       if len(result) > 2: # We have a super class
           superIRI = result["super"]["value"]
           superName = result["super_name"]["value"]

           if superIRI not in nodes.keys():
               nodes[superIRI] = Node(superIRI, label=superName)

           nodes[classIRI].parent = nodes[superIRI]

   for node in nodes.values():
       if node.is_root and node != rootNode:
           node.parent = rootNode

   # print tree to console
   for pre, fill, node in RenderTree(rootNode):
       print("%s%s" % (pre, vars(node).get("label")))

   for node in PreOrderIter(rootNode):
       if node.is_root:
           tree.insert('', 'end', node.name, text = vars(node).get("label"))
       else:
           tree.insert(node.parent.name, 'end', node.name, text = vars(node).get("label"))

   return 0
