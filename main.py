from Tkinter import *
import ttk
from SPARQLWrapper import SPARQLWrapper, JSON
from PIL import ImageTk, Image
import queryGenerator
import math
import os

path = "lib/lfw/"
## testresultset = "https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/Individuals/FaceNetTest01ResultSet"
testresultset = "https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/Individuals/dlibtest00ResultSet"
## testresultset = "https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/Individuals/facenettest01ResultSet"

startingNode = "https://w3id.org/lio/v1#Image"
blazegraphURL = "http://localhost:9999/blazegraph/namespace/kb/sparql"
queryState = "All"
treeWidth = 300

N = 16 # number  of images
NumCols = 4
NumRowsView = 2


offset = 0
NumRows = int(math.ceil(float(N)/NumCols))
imageWidgets = []
imageRef = []

leftDead = True
rightDead = True
prevSelect = []

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button", fg="red")
   button.pack()

# def donothing():
#     win = Toplevel()
#     win.wm_title("Window")
#
#     l = Label(win, text="Input")
#     l.grid(row=0, column=0)
#
#     b = Button(win, text="Okay", command=win.destroy)
#     b.grid(row=1, column=0)

def updateOffsetButtons(actualRecieved, totalNumberOfResults):
    global leftDead
    global rightDead

    leftDead = offset == 0
    if leftDead:
        leftLabel.config(image=leftDeadImg)
    else:
        leftLabel.config(image=leftImg)

    start = offset*N + 1
    finish = start + actualRecieved - 1
    b.config(text = str(start) + " to " + str(finish))

    rightDead = finish >= totalNumberOfResults
    if rightDead:
        rightLabel.config(image=rightDeadImg)
    else:
        rightLabel.config(image=rightImg)

def left_button(event):
    if not leftDead:
        global offset
        offset = offset - 1
        image_updater(prevSelect)


def right_button(event):
    if not rightDead:
        global offset
        offset = offset + 1
        image_updater(prevSelect)

def rollWheel(event):
    if(event.x > treeWidth):
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

def image_updater(treeSelection):
    sparql = SPARQLWrapper(blazegraphURL)
    query = queryGenerator.generateQuery(N, N*offset, testresultset, tree.selection(), queryState)
    print(query)

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    count=0
    for result in results["results"]["bindings"]:
        imageIRI = result["Image"]["value"]
        correct = result["Correct"]["value"]
        total = result["Total"]["value"]
        imageName = result["Name"]["value"]

        imageNum = imageIRI.split("/")[10]
        filename = path + imageName.replace(" ", "_") + "/" + imageName.replace(" ", "_") + "_" + imageNum.zfill(4) + ".jpg"

        displayImage(count, filename, correct == total)
        count = count + 1

    # update buttons
    query = queryGenerator.generateCountQuery(testresultset, tree.selection(), queryState)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    updateOffsetButtons(count, int(results["results"]["bindings"][0]["count"]["value"]))

    # make the rest of the labels invisible
    for i in range(count, N):
        imageWidgets[i].grid_forget()
    root.update()

def tree_select(event):
    global prevSelect
    global offset

    prevSelect = tree.selection()
    offset = 0

    print("selected items:")
    for item in tree.selection():
        item_text = tree.item(item,"text")
        print(item_text)

    image_updater(tree.selection())




root = Tk()
# root.geometry("1016x508")

f1 = Frame(root)
optionButtonFrame = Frame(f1)

f1.grid(column=0, row=0, sticky="ns")
f1.grid_propagate(False)

f2_0 = Frame(root)
f2_0.grid(column=1, row=0, sticky="news")
f2_0.grid_rowconfigure(0, weight=1)
f2_0.grid_columnconfigure(0, weight=1)
f2_0.grid_propagate(False) # Set grid_propagate to False to allow resizing later

f3 = Frame(root)
f3.grid(column=1, row=1, sticky="s")

leftImg = ImageTk.PhotoImage(Image.open("lib/left.jpg"))
leftDeadImg = ImageTk.PhotoImage(Image.open("lib/left_dead.jpg"))
leftLabel = Label(f3, image=leftImg, fg="grey" )
leftLabel.pack(padx=5, pady=10, side=LEFT)
leftLabel.bind("<Button-1>", left_button)

b = Label(f3, text = 'Look Here')
b.pack(padx=5, pady=10, side=LEFT)

rightImg = ImageTk.PhotoImage(Image.open("lib/right.jpg"))
rightDeadImg = ImageTk.PhotoImage(Image.open("lib/right_dead.jpg"))
rightLabel = Label(f3, image=rightImg )
rightLabel.pack(padx=5, pady=10, side=LEFT)
rightLabel.bind("<Button-1>", right_button)


f3.update_idletasks()


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
# filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Select Dataset", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

def allCommand(event):
   global queryState
   queryState = "All"
   print("State was set to all")
   image_updater(prevSelect)
   allLabel.config(image=allImg)
   correctLabel.config(image=correctDeadImg)
   incorrectLabel.config(image=incorrectDeadImg)

def correctCommand(event):
   global queryState
   queryState = "Correct"
   print("State was set to correct")
   image_updater(prevSelect)
   allLabel.config(image=allDeadImg)
   correctLabel.config(image=correctImg)
   incorrectLabel.config(image=incorrectDeadImg)

def incorrectCommand(event):
   global queryState
   queryState = "Incorrect"
   print("State was set to incorrect")
   image_updater(prevSelect)
   allLabel.config(image=allDeadImg)
   correctLabel.config(image=correctDeadImg)
   incorrectLabel.config(image=incorrectImg)


optionButtonFrame.pack()
allImg = ImageTk.PhotoImage(Image.open("lib/all.jpg"))
allDeadImg = ImageTk.PhotoImage(Image.open("lib/all_dead.jpg"))
allLabel = Label(optionButtonFrame, image=allImg, fg="grey" )
allLabel.pack(pady=10, side=LEFT)
allLabel.bind("<Button-1>", allCommand)

correctImg = ImageTk.PhotoImage(Image.open("lib/correct.jpg"))
correctDeadImg = ImageTk.PhotoImage(Image.open("lib/correct_dead.jpg"))
correctLabel = Label(optionButtonFrame, image=correctDeadImg, fg="grey" )
correctLabel.pack(pady=10, side=LEFT)
correctLabel.bind("<Button-1>", correctCommand)

incorrectImg = ImageTk.PhotoImage(Image.open("lib/incorrect.jpg"))
incorrectDeadImg = ImageTk.PhotoImage(Image.open("lib/incorrect_dead.jpg"))
incorrectLabel = Label(optionButtonFrame, image=incorrectDeadImg, fg="grey" )
incorrectLabel.pack(pady=10, side=LEFT)
incorrectLabel.bind("<Button-1>", incorrectCommand)

tree = ttk.Treeview(f1)
queryGenerator.generateTree("http://localhost:9999/blazegraph/namespace/kb/sparql", testresultset, tree)
tree.bind("<<TreeviewSelect>>", tree_select)
tree.pack(expand=True, fill='y')
print("Here")
tree.heading("#0", text="Visual Attributes")
tree.column("#0", minwidth=100, width=treeWidth)


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
f3.update_idletasks()

# Resize the canvas frame to show exactly crollbar
columns_width = sum([imageWidgets[i].winfo_width() for i in range(NumCols)])
rows_height = sum([imageWidgets[i].winfo_height() for i in range(NumRowsView)])
f2_0.config(width=columns_width + vsb.winfo_width(),
                    height=rows_height)

# Set the canvas scrolling region
canvas.config(scrollregion=canvas.bbox("all"))

tree.focus(startingNode)
tree.selection_set(startingNode)

def fix():
    a = root.winfo_geometry().split('+')[0]
    b = a.split('x')
    w = int(b[0])
    h = int(b[1])
    root.geometry('%dx%d' % (w+1,h+1))

root.update()
root.after(0, fix)

root.mainloop()
# root.destroy()
