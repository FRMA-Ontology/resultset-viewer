from Tkinter import *
import ttk
from SPARQLWrapper import SPARQLWrapper, JSON
from PIL import ImageTk, Image
import queryGenerator
import math
import os

path = "lib/lfw/"
testresultset = "https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/Individuals/dlibTest01ResultSet"
startingNode = "https://w3id.org/lio/v1#Image"

N = 20 # number  of images
NumCols = 4
NumRowsView = 2

NumRows = int(math.ceil(float(N)/NumCols))
imageWidgets = []
imageRef = []

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()


def rollWheel(event):
        canvas.yview_scroll(-1*event.delta, "units")

def displayImage(index, imagePath, correct):
    # Change Image
    imageRef[index] = ImageTk.PhotoImage(Image.open(imagePath))
    imageWidgets[index].config(image=imageRef[index])

    # set Correct color
    if correct:
        imageWidgets[index].config(bg="green")
    else:
        imageWidgets[index].config(bg="red")

    # make iamge visable
    imageWidgets[index].grid(row = index / NumCols, column = index % NumCols, sticky='news')

def tree_select(event):
    print("selected items:")
    for item in tree.selection():
        item_text = tree.item(item,"text")
        print(item_text)

    blazegraphURL = "http://localhost:9999/blazegraph/namespace/kb/sparql"
    query = queryGenerator.generateQuery(N, testresultset, tree.selection())
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

        displayImage(count, filename, classification == imageName)
        count = count + 1

    print("Found image number: " + str(count))

    # make the rest of the labels invisible
    for i in range(count, N):
        imageWidgets[i].grid_forget()


root = Tk()
# root.geometry("1016x508")

f1 = Frame(root)
f1.grid_propagate(False)

f2_0 = Frame(root)

f1.grid(column=0, row=0, sticky="ns")
f2_0.grid(column=1, row=0, sticky="news")
f2_0.grid_rowconfigure(0, weight=1)
f2_0.grid_columnconfigure(0, weight=1)

# Set grid_propagate to False to allow resizing later
f2_0.grid_propagate(False)


# Add a canvas in that frame
canvas = Canvas(f2_0)
canvas.grid(row=0, column=0, sticky="news")

# Link a scrollbar to the canvas
vsb = Scrollbar(f2_0, orient="vertical", command=canvas.yview)
vsb.grid(row=0, column=1, sticky='ns')
canvas.configure(yscrollcommand=vsb.set)

# Need to update this to support, Windows and X11
# see https://stackoverflow.com/questions/17355902/python-tkinter-binding-mousewheel-to-scrollbar
canvas.bind_all("<MouseWheel>", rollWheel)


# Create a frame to contain the buttons
f2 = Frame(canvas)
canvas.create_window((0, 0), window=f2, anchor='nw')

root.rowconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)


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


# these will be place holders
for j in range(NumRows):
    for i in range(NumCols):
        imageRef.append(ImageTk.PhotoImage(Image.open(path + "Aaron_Eckhart/Aaron_Eckhart_0001.jpg")))
        imageWidgets.append(Label(f2, compound = CENTER, image = imageRef[-1], bg = "green"))
        # imageRef.insert(0, ImageTk.PhotoImage(Image.open(path + "Aaron_Eckhart/Aaron_Eckhart_0001.jpg")))
        # imageWidgets.insert(0, Label(f2, compound = CENTER, image = imageRef[0], bg = "green"))
        imageWidgets[-1].grid(row=j, column=i, sticky='news')

# Update buttons frames idle tasks to let tkinter calculate buttons sizes
f2.update_idletasks()

# Resize the canvas frame to show exactly crollbar
columns_width = sum([imageWidgets[i].winfo_width() for i in range(NumCols)])
rows_height = sum([imageWidgets[i].winfo_height() for i in range(NumRowsView)])
f2_0.config(width=columns_width + vsb.winfo_width(),
                    height=rows_height)

# Set the canvas scrolling region
canvas.config(scrollregion=canvas.bbox("all"))

tree.focus(startingNode)
tree.selection_set(startingNode)

root.mainloop()
