from Tkinter import *
import ttk
from SPARQLWrapper import SPARQLWrapper, JSON
from anytree import Node, RenderTree, PreOrderIter
from PIL import ImageTk, Image

path = "lib/lfw/"

def generateTree(blazegraphURL, tree):
   sparql = SPARQLWrapper(blazegraphURL)
   sparql.setQuery("""
    select *
    where{
        ?class a owl:Class.
        ?class rdfs:label ?name.

         OPTIONAL {
          ?class rdfs:subClassOf ?super .
          ?super a owl:Class.
        	 ?super rdfs:label ?super_name.

         }
        }
   """)

   sparql.setReturnFormat(JSON)
   results = sparql.query().convert()

   thing = Node("thing")
   nodes = {}

   depend = []
   # Add in all top level nodes and capture the rest of the dependencies
   for result in results["results"]["bindings"]:
       classIRI = result["class"]["value"]
       className = result["name"]["value"]
       if len(result) == 2: # We have a super class
           nodes[classIRI] = Node(classIRI, parent=thing, label=className)
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
   # for pre, fill, node in RenderTree(thing):
   #     print("%s%s" % (pre, vars(node).get("label")))

   for node in PreOrderIter(thing):
       if node.is_root:
           tree.insert('', 'end', node.name, text = "thing")
       else:
           tree.insert(node.parent.name, 'end', node.name, text = vars(node).get("label"))

   return 0

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def tree_select(event):
    print("selected items:")
    for item in tree.selection():
        item_text = tree.item(item,"text")
        print(item_text)

    mugshotQuery = """prefix mlmo: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/MachineLearningModelOntology/>
        prefix fibo-fnd-arr-arr: <http://www.omg.org/spec/EDMC-FIBO/FND/Arrangements/Arrangements/>
        prefix lio: <http://purl.org/net/lio#>
        prefix lcc-lr: <http://www.omg.org/spec/LCC/Languages/LanguageRepresentation/>
        prefix fibo-fnd-aap-a: <http://www.omg.org/spec/EDMC-FIBO/FND/AgentsAndPeople/Agents/>
        prefix img: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/ImageOntology/>
        prefix frma: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/FRMA/>

        select ?Image ?classification ?Name
            where {
              ?ResultSet a mlmo:ResultSet .
              ?ResultSet fibo-fnd-arr-arr:hasConstituent ?Result .
              ?Result lcc-lr:hasTag ?classification .
              ?Result mlmo:hasFeature ?Image .

              # Posed Image
              ?Image a img:PosedImage.

              # Indoors
              ?Image lio:hasDepictedBackground ?background .
              ?background a img:Indoors .

              # No Face occlusions
              OPTIONAL{
                ?Image frma:hasOcclusion ?occlusion.
                minus{
                        ?occlusion a frma:OcularOcclusion .
                }
                minus{
                        ?occlusion a frma:BuccalOcclusion .
                }
                minus{
                        ?occlusion a frma:MentalOcclusion .
                }
                minus{
                        ?occlusion a frma:OralOcclusion .
                }
                minus{
                        ?occlusion a frma:ParotidOcclusion .
                }
                minus{
                        ?occlusion a frma:ZygomaticOcclusion .
                }
                minus{
                        ?occlusion a frma:AuricleOcclusion .
                }
                minus{
                        ?occlusion a frma:CranialOcclusion .
                }
                minus{
                        ?occlusion a frma:FrontalOcclusion .
                }
                minus{
                        ?occlusion a frma:NasalOcclusion .
                }
               }

              # Image Fidelity not blurry
              ?Image img:fidelityDescribedBy ?fidelity .
              minus{
                ?fidelity a img:BlurryImageFidelity .
               }

              ?Image lio:depicts ?Person .
              ?Person fibo-fnd-aap-a:hasName ?Name

              bind( <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/Individuals/dlibTest01ResultSet> as ?ResultSet)
            } limit 2
            """
    thingQuery = """prefix mlmo: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/MachineLearningModelOntology/>
        prefix fibo-fnd-arr-arr: <http://www.omg.org/spec/EDMC-FIBO/FND/Arrangements/Arrangements/>
        prefix lio: <http://purl.org/net/lio#>
        prefix lcc-lr: <http://www.omg.org/spec/LCC/Languages/LanguageRepresentation/>
        prefix fibo-fnd-aap-a: <http://www.omg.org/spec/EDMC-FIBO/FND/AgentsAndPeople/Agents/>
        prefix img: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/ImageOntology/>
        prefix frma: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/FRMA/>

        select ?Image ?classification ?Name
            where {
              ?ResultSet a mlmo:ResultSet .
              ?ResultSet fibo-fnd-arr-arr:hasConstituent ?Result .
              ?Result lcc-lr:hasTag ?classification .
              ?Result mlmo:hasFeature ?Image .

              ?Image lio:depicts ?Person .
              ?Person fibo-fnd-aap-a:hasName ?Name .

              bind( <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/Individuals/dlibTest01ResultSet> as ?ResultSet)
            }
        limit 2"""
    blazegraphURL = "http://localhost:9999/blazegraph/namespace/kb/sparql"
    sparql = SPARQLWrapper(blazegraphURL)
    if tree.selection()[0] == "thing":
        sparql.setQuery(thingQuery)

    if tree.selection()[0] == "https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/FRMA/MugShotPhoto":
        sparql.setQuery(mugshotQuery)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    count=0

    for result in results["results"]["bindings"]:
        imageIRI = result["Image"]["value"]
        classification = result["classification"]["value"]
        imageName = result["Name"]["value"]

        imageNum = imageIRI.split("/")[10]

        filename = path + imageName.replace(" ", "_") + "/" + imageName.replace(" ", "_") + "_" + imageNum.zfill(4) + ".jpg"
        print(filename)

        if classification == imageName:
            color = "green"
        else:
            color = "red"

        if count == 0:
            img.photo_ref = ImageTk.PhotoImage(Image.open(filename))
            w1.config(image=img.photo_ref)
            w1.config(bg=color)
        else:
            img2.photo_ref = ImageTk.PhotoImage(Image.open(filename))
            w2.config(image=img2.photo_ref)
            w2.config(bg=color)

        count = count + 1

root = Tk()

f1 = Frame(root)
f2 = Frame(root)

f1.grid(column=0, row=0, sticky="ns")
f2.grid(column=1, row=0, sticky="n")
root.rowconfigure(0, weight=1)

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)


tree = ttk.Treeview(f1)
generateTree("http://localhost:9999/blazegraph/namespace/kb/sparql", tree)
tree.bind("<<TreeviewSelect>>", tree_select)
tree.pack(expand=True, fill='y')

#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
img = ImageTk.PhotoImage(Image.open(path + "Aaron_Eckhart/Aaron_Eckhart_0001.jpg"))
img2 = ImageTk.PhotoImage(Image.open(path + "Aaron_Guiel/Aaron_Guiel_0001.jpg"))

# these will be place holders
w1 = Label(f2, compound = CENTER, image = img, bg = "green")
w1.pack(side="right")
w2 = Label(f2, compound = CENTER, image = img, bg = "red")
w2.pack(side="right")

root.mainloop()
