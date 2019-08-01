import os
import rdflib
from rdflib.namespace import RDF, Namespace, OWL, XSD, RDFS
from constants import *
import requests

# Constants
hasFeature = rdflib.term.URIRef("https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/MachineLearningModelOntology/hasFeature")
hasConstituent = rdflib.term.URIRef("http://www.omg.org/spec/EDMC-FIBO/FND/Arrangements/Arrangements/hasConstituent")
hasTag = rdflib.term.URIRef("http://www.omg.org/spec/LCC/Languages/LanguageRepresentation/hasTag")
ResultClass = rdflib.term.URIRef("https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/MachineLearningModelOntology/Result")
next = rdflib.term.URIRef("http://purl.org/ontology/olo/core#next")

def text2IRI(value):
    value = value.lower().replace(' ', '-')
    uriReservedCharacters = [":", "/", "?", "#", "[", "]", "@", "!", "$", "&", "'", "(", ")", "*", "+", ",", ";", "=", "%"]

    final = ""
    for c in value:
        if c in uriReservedCharacters:
            final = final + "%" + str(hex(ord(c)).replace('0x', ''))
        else:
            final = final + str(c)

    return final


def str2bool(v):
    return v.strip().lower() in ("true", "t", "1")


def clearTripleStore(url):
    headers = {'Content-Type': 'application/xml',}
    response = requests.delete(url, headers=headers)
    print(response)
    print(response.content)
    return (response.status_code == 201) or (response.status_code == 200)

def loadOnts(namespace):
    propertiesPath = "RWStore.properties"
    filepath = os.path.abspath("lib" + os.path.sep + "ontologies")

    data = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
        <properties>
            <entry key="quiet">false</entry>
            <entry key="verbose">0</entry>
            <entry key="closure">false</entry>
            <entry key="durableQueues">true</entry>
            <entry key="namespace">{0}</entry>
            <entry key="propertyFile">{1}</entry>
            <entry key="fileOrDirs">{2}</entry>
        </properties>""".format(namespace, propertiesPath, filepath)



    headers = {'Content-Type': 'application/xml',}
    response = requests.post(blazegraphBase + "/dataloader", headers=headers, data=data)

    files = os.listdir(filepath)
    for file in files:
        if file.endswith(".fail") or file.endswith(".good"):
            os.rename(filepath + os.path.sep + file, filepath + os.path.sep + file[:-5])

    print(response)
    print(response.content)

    return (response.status_code == 201) or (response.status_code == 200)

def loadTurtle(filepath, namespace):
    propertiesPath = "RWStore.properties"
    format = "ttl"

    # RDF Format (Default is rdf/xml)
    # Default Graph URI (Optional - Required for quads mode namespace)
    # Suppress all stdout messages (Optional)
    # Show additional messages detailing the load performance. (Optional)
    # Compute the RDF(S)+ closure. (Optional)
    # Files will be renamed to either .good or .fail as they are processed.
    # The namespace of the KB instance. Defaults to kb.
    # The configuration file for the database instance. It must be readable by the web application.
    # Zero or more files or directories containing the data to be loaded. This should be a comma delimited list. The files must be readable by the web application.
    data = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
        <properties>
            <entry key="format">{0}</entry>
            <entry key="quiet">false</entry>
            <entry key="verbose">0</entry>
            <entry key="closure">false</entry>
            <entry key="durableQueues">true</entry>
            <entry key="namespace">{1}</entry>
            <entry key="propertyFile">{2}</entry>
            <entry key="fileOrDirs">{3}</entry>
        </properties>""".format(format, namespace, propertiesPath, filepath)

    print(data)

    headers = {'Content-Type': 'application/xml',}
    response = requests.post(blazegraphBase + "/dataloader", headers=headers, data=data)
    print(response)
    print(response.content)
    return (response.status_code == 201) or (response.status_code == 200)


def loadResultSet(testName, algorithmName, filepath):
    iri = text2IRI(testName)

    # Create resultset
    graph = rdflib.Graph()
    resultset_IRI = rdflib.term.URIRef("https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/Individuals/" + iri)
    graph.add((resultset_IRI, RDF.type, rdflib.term.URIRef("https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/MachineLearningModelOntology/ResultSet")))
    graph.add((resultset_IRI, RDFS.label, rdflib.term.Literal(algorithmName, datatype=XSD.string)))

    with open(filepath) as fp:
        for cnt, line in enumerate(fp):
            lsplit = line.split("\t")

            if len(lsplit) != 5:
                return "Error bad result file"

            result_IRI = rdflib.term.URIRef("https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/Individuals/{0}/Result{1}".format(iri, cnt))
            image1_IRI = rdflib.term.URIRef("https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/Individuals/Image/{0}/{1}/Image".format(lsplit[0].replace("_", ""), lsplit[1]))
            image2_IRI = rdflib.term.URIRef("https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/Individuals/Image/{0}/{1}/Image".format(lsplit[2].replace("_", ""), lsplit[3]))

            if str2bool(lsplit[4]):
                if lsplit[0] == lsplit[2]:
                    tag = rdflib.term.Literal("Match", datatype=XSD.string)
                else:
                    tag = rdflib.term.Literal("Not a Match", datatype=XSD.string)
            else:
                if lsplit[0] == lsplit[2]:
                    tag = rdflib.term.Literal("Not a Match", datatype=XSD.string)
                else:
                    tag = rdflib.term.Literal("Match", datatype=XSD.string)

            graph.add((result_IRI, RDF.type, ResultClass))
            graph.add((result_IRI, hasTag, tag))
            graph.add((result_IRI, hasFeature, image1_IRI))
            graph.add((result_IRI, hasFeature, image2_IRI))
            graph.add((image1_IRI, next, image2_IRI))
            graph.add((resultset_IRI, hasConstituent, result_IRI))


    # Load triples to blazegraph
    outFilePath = "temp" + os.path.sep + filepath.split(os.path.sep)[-1] + ".ttl"
    graph.serialize(destination=outFilePath, format='turtle')
    loadTurtle(os.path.abspath(outFilePath), namespace)

    # clean up
    files = os.listdir("temp" + os.path.sep)
    for file in files:
        if file.endswith(".fail") or file.endswith(".good") or file.endswith(".ttl"):
            os.remove(os.path.join("temp" + os.path.sep, file))

    return None
