from SPARQLWrapper import SPARQLWrapper, JSON
from anytree import Node, RenderTree, PreOrderIter
import query

rootNode = Node("https://w3id.org/lio/v1#Image", label="image")
nodes = {"https://w3id.org/lio/v1#Image" : rootNode}


def getModifer(modiferIRI):
    return query.querymapper[modiferIRI]

def generateCountQuery(resultset, modiferIRIs, queryState):
    buildableQuery = query.prefix + "\n" + query.countImages

    buildableQuery = buildableQuery + "\n{"
    buildableQuery = buildableQuery + "\n" + query.selectTruePositive
    for modiferIRI in modiferIRIs:
        buildableQuery = buildableQuery + "\n" + getModifer(modiferIRI)
    buildableQuery = buildableQuery + "\n" + query.endTruePositive + "\n}"

    buildableQuery = buildableQuery + "\n{"
    buildableQuery = buildableQuery + "\n" + query.selectTrueNegative
    for modiferIRI in modiferIRIs:
        buildableQuery = buildableQuery + "\n" + getModifer(modiferIRI)
    buildableQuery = buildableQuery + "\n" + query.endTrueNegative + "\n}"

    buildableQuery = buildableQuery + "\n{"
    buildableQuery = buildableQuery + "\n" + query.selectTotal + "\n" + query.baseGraph
    for modiferIRI in modiferIRIs:
        buildableQuery = buildableQuery + "\n" + getModifer(modiferIRI)
    buildableQuery = buildableQuery + "\n" + query.endTotal + "\n}"

    if(queryState == "Correct"):
        buildableQuery = buildableQuery + "\n" + query.correctQuery2

    if(queryState == "Incorrect"):
        buildableQuery = buildableQuery + "\n" + query.incorrectQuery2

    return buildableQuery + "\n" + "bind( <" + resultset + "> as ?ResultSet) \n bind( ?trueNegative + ?truePositive as ?Correct) }"
    # buildableQuery = query.prefix + "\n" + query.baseCountQuery
    # for modiferIRI in modiferIRIs:
    #     buildableQuery = buildableQuery + "\n" + getModifer(modiferIRI)
    #
    # if(queryState == "Correct"):
    #     buildableQuery = buildableQuery + "\n" + query.correctQuery
    #
    # if(queryState == "Incorrect"):
    #     buildableQuery = buildableQuery + "\n" + query.incorrectQuery
    #
    # return buildableQuery + "\n" + "bind( <" + resultset + "> as ?ResultSet)}"

# def generateQuery(limit, offset, resultset, modiferIRIs, queryState):
#     buildableQuery = query.baseQuery
#     for modiferIRI in modiferIRIs:
#         buildableQuery = buildableQuery + "\n" + getModifer(modiferIRI)
#
#     if(queryState == "Correct"):
#         buildableQuery = buildableQuery + "\n" + query.correctQuery
#
#     if(queryState == "Incorrect"):
#         buildableQuery = buildableQuery + "\n" + query.incorrectQuery
#
#     return buildableQuery + "\n" + "bind( <" + resultset + "> as ?ResultSet)} ORDER BY ?Image limit " + str(limit) + " offset " + str(offset)

def generateQuery(limit, offset, resultset, modiferIRIs, queryState):
    buildableQuery = query.prefix + "\n" + query.selectCount

    buildableQuery = buildableQuery + "\n{"
    buildableQuery = buildableQuery + "\n" + query.selectTruePositive
    for modiferIRI in modiferIRIs:
        buildableQuery = buildableQuery + "\n" + getModifer(modiferIRI)
    buildableQuery = buildableQuery + "\n" + query.endTruePositive + "\n}"

    buildableQuery = buildableQuery + "\n{"
    buildableQuery = buildableQuery + "\n" + query.selectTrueNegative
    for modiferIRI in modiferIRIs:
        buildableQuery = buildableQuery + "\n" + getModifer(modiferIRI)
    buildableQuery = buildableQuery + "\n" + query.endTrueNegative + "\n}"

    buildableQuery = buildableQuery + "\n{"
    buildableQuery = buildableQuery + "\n" + query.selectTotal + "\n" + query.baseGraph
    for modiferIRI in modiferIRIs:
        buildableQuery = buildableQuery + "\n" + getModifer(modiferIRI)
    buildableQuery = buildableQuery + "\n" + query.endTotal + "\n}"

    if(queryState == "Correct"):
        buildableQuery = buildableQuery + "\n" + query.correctQuery2

    if(queryState == "Incorrect"):
        buildableQuery = buildableQuery + "\n" + query.incorrectQuery2

    return buildableQuery + "\n" + "bind( <" + resultset + "> as ?ResultSet) \n bind( ?trueNegative + ?truePositive as ?Correct) } ORDER BY ?Image limit " + str(limit) + " offset " + str(offset)

def generateAccuracyQuery(resultset, modiferIRIs):
    buildableQuery = ""
    for modiferIRI in modiferIRIs:
        try:
            buildableQuery = buildableQuery + "\n" + getModifer(modiferIRI)
        except KeyError:
            print("Error: " + modiferIRI + " not found!!")
            return "Error"
    buildableQuery = buildableQuery + "\n" + "bind( <" + resultset + "> as ?ResultSet)"
    fullquery = query.prefix + query.baseAccQuery + "{\n" + query.baseCountQuery + "\n" + buildableQuery + "}}\n{" + query.baseNumTruePositive + "\n" + buildableQuery + "}}\n{" + query.baseNumTrueNegative + "\n" + buildableQuery + "}}\n}"

    return fullquery

def generateTree(blazegraphURL, resultset, tree):
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
   # for pre, fill, node in RenderTree(rootNode):
   #     print("%s%s" % (pre, vars(node).get("label")))

   for node in PreOrderIter(rootNode):
       label = vars(node).get("label")
       q = generateAccuracyQuery(resultset, [node.name])
       if(q == "Error"):
           label = label + "(" + q + ")"
       else:
           sparql = SPARQLWrapper(blazegraphURL)
           sparql.setQuery(q)

           sparql.setReturnFormat(JSON)
           results = sparql.query().convert()

           for result in results["results"]["bindings"]:
               total = float(result["count"]["value"])
               correctCount = float(result["numCorrect"]["value"])

           if(total == 0):
               accuracy = "N/A"
           else:
               accuracy = str("%.2f" % ((correctCount/total) * 100))+ "%"
           label = label + "(" + accuracy + ")"
           print(label + ", " + accuracy)

       if node.is_root:
           tree.insert('', 'end', node.name, text = label)
       else:
           tree.insert(node.parent.name, 'end', node.name, text = label)

   return 0

def getResultSets(blazegraphURL):
   sparql = SPARQLWrapper(blazegraphURL)
   sparql.setQuery(query.resultSetQuery)
   sparql.setReturnFormat(JSON)
   results = sparql.query().convert()

   iris = []
   # Add in all top level nodes and capture the rest of the dependencies
   for result in results["results"]["bindings"]:
       iris.append(result["ResultSet"]["value"])

   return iris
