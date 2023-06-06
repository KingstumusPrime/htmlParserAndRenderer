from tkinter import *  
from layout import * 



def SolidColor(color, rect):
  c = (color["R"], color["G"], color["B"])
  canvas.create_rectangle(rect.x, rect.y, rect.x + rect.width,rect.y + rect.height, fill="#%02x%02x%02x" % c, width=0)

def buildDisplayList(root):
  list = []
  renderLayoutBox(list, root)
  return list

def renderLayoutBox(list, box):
  renderBackground(list, box)
  renderBorders(list, box)
  #TODO render text

  for child in box.children:
    renderLayoutBox(list, child)

def renderBorders(list, box):
  c = getColor(box, "border-color")
  # if no border color bail
  d = box.dimensions
  if  c == None or (d.border.right == 0 and d.border.left == 0 and d.border. top == 0 and d.border.bottom == 0):
    return
  borderBox = d.borderBox()
  print(d.border.left)
 # left border
  list.append(SolidColor(c, Rect(borderBox.x, borderBox.y, d.border.left, borderBox.height)))
  # right border
  list.append(SolidColor(c, Rect(borderBox.x + borderBox.width - d.border.right, borderBox.y, d.border.left, borderBox.height)))
  # top border
  print(d.border.top)
  list.append(SolidColor(c, Rect(borderBox.x,  borderBox.y, borderBox.width, d.border.top)))
    # bottom border
  list.append(SolidColor(c, Rect(borderBox.x, borderBox.y + borderBox.height - d.border.bottom, borderBox.width, d.border.bottom)))
  
    

def renderBackground(list, box):
  c = getColor(box, "background")
  print(c)
  if c == None:
    return
  list.append(SolidColor(c, box.dimensions.borderBox()))

def getColor(box, name):
  if(box.type.type != "anonymous" and box.type.node.value(name) != None):
    if type(box.type.node.value(name).value) is dict:
      return box.type.node.value(name).value
    else:
      return None
  return None
              
screen = Tk()
screen.title = "htmlExample"
screen.geometry("500x500")

canvas = Canvas(width=800, height=600,  highlightthickness=0, bd=0)


layoutTree = genLayTree()
print(layoutTree)
displayList = buildDisplayList(layoutTree)
print(displayList)
canvas.pack()

screen.mainloop()

