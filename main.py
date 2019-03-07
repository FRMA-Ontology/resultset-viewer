from Tkinter import *
import ttk
from SPARQLWrapper import SPARQLWrapper, JSON
from PIL import ImageTk, Image
import queryGenerator

path = "lib/lfw/"
testresultset = "https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/Individuals/dlibTest01ResultSet"


def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def tree_select(event):
    print("selected items:")
    for item in tree.selection():
        item_text = tree.item(item,"text")
        print(item_text)

    limit = 2
    blazegraphURL = "http://localhost:9999/blazegraph/namespace/kb/sparql"
    query = queryGenerator.generateQuery(limit, testresultset, tree.selection())
    print(query)

    sparql = SPARQLWrapper(blazegraphURL)
    sparql.setQuery(query)
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
queryGenerator.generateTree("http://localhost:9999/blazegraph/namespace/kb/sparql", tree)
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
