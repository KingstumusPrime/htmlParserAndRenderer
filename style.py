from Html import *
from Css import *
from tkinter import *
from PIL import ImageTk, Image

css = """html { display: block; padding: 12px;}
* {
  margin: 20px;
}

.bun { 
  display: inline; 
  background: #DAB399; 
  padding-top: 60px;
  padding-bottom: 60px;
  padding-left: 50px;
}
.lettuce { 
  display: inline; 
  background: #00FF00; 
  padding-top: 60px;
  padding-bottom: 60px;
  padding-left: 22px;
}

.meat { 
  display: inline; 
  background: #7F390A; 
  padding-top: 60px;
  padding-bottom: 60px;
  padding-left: 55px;
}

.cheese { 
  display: inline; 
  background: #E1EA23; 
  padding-top: 60px;
  padding-bottom: 60px;
  padding-left: 20px;
}

#block {
  display: block;
  background: #FF0000;
  margin-bottom: 200px;
}

img {
  width: 150px;
  height: 150px;
}

"""

html = """
<html>
  <div id="block">
    <div class="bun">HELLO WORLD</div>
    <div class="lettuce"></div>
    <div class="cheese"></div>
    <div class="meat"></div>
    <div class="bun"></div>
    Hello world
  </div>
  <div id="block">
    <div class="bun"></div>
    <div class="lettuce"></div>
    <div class="cheese"></div>
    <div class="meat"></div>
    <div class="bun"></div>
  </div>
  <img src="./htmlPic.jpg"></img>
</html>"""


class styledNode:

  def __init__(self, node, specifiedValues, children, image=None):
    # in c++ node is a pointer!
    self.node = node

    # hashmap (dict) of the name value pairs applied to element comes in form of {str: value(the class)}
    self.specifiedValues = specifiedValues

    # similar to the html tree children are generated recurivly to fill the array
    self.children = children

    self.image = image

  def value(self, name):
    return self.specifiedValues[name] if name in self.specifiedValues else None

  def display(self):
    if self.value("display") == None: return "inline"
    if self.value("display").value == "block":
      return "block"
    elif self.value("display").value == "none":
      return "none"
    else:
      return "inline"

  # try values in order returning each one if it exsists otherwise return 3rd
  def lookup(self, first, second, third):
    if self.value(first) != None:
      return self.value(first)
    else:
      return self.value(second) if self.value(second) != None else third
  def getImage(self):
    print(self.node.isImage())
    if self.node.isImage():
      self.image = loadImage(self.node.nodeData["atributes"]["src"], {"w": self.value("width"), "h": self.value("height")})


class ImageOb:
  def __init__(self, src, baseWidth, baseHeight, obj) -> None:
    self.src = src
    self.width = baseWidth
    self.height = baseHeight
    self.obj = obj

def loadImage(src, externalDimensions):
  imageRef = Image.open(src)
  im = ImageTk.PhotoImage(imageRef)
  width, height = imageRef.size
  # ratio of width to height
  if externalDimensions["w"] != None and externalDimensions["h"] == None:
    height = externalDimensions["w"].toPx() * height/width
    width = externalDimensions["w"].toPx() 
  elif externalDimensions["w"] == None and externalDimensions["h"] != None:
    height = externalDimensions["h"].toPx()  * width/height
    width = externalDimensions["h"].toPx() 
  elif externalDimensions["w"] != None and externalDimensions["h"] != None:
    height = externalDimensions["h"].toPx() 
    width = externalDimensions["w"].toPx() 
  print("LOADING IMAGE: " + src)
  imageRef = imageRef.resize((int(width), int(height)), Image.Resampling.BILINEAR)
  im = ImageTk.PhotoImage(imageRef)
  return ImageOb(src, width, height, im)


def getNodeData(nodeData):
  # loop through atributes checking or classes and ids return in the formate of (name, c, i)
  c = []
  i = ""
  for attr in nodeData["atributes"]:
    if (attr == "class"):
      c = nodeData["atributes"][attr].split(" ")
    if (attr == "id"):
      i = nodeData["atributes"][attr]
  return (nodeData["tag_name"], c, i)


def matchSelector(nodeData, selector):
  data = getNodeData(nodeData)
  if data[0] == selector.name or selector.name == "*":
    return True
  if selector.sClass in data[1]:
    return True

  if data[2] == selector.id:
    return True

  return False


def matchRule(nodeData, rule):
  for selct in rule.selectors:
    if (matchSelector(nodeData, selct)):
      return rule
  return None


def matchRules(nodeData, stylesheet):
  return [rule for rule in stylesheet if matchRule(nodeData, rule)]


def specifiedValues(nodeData, styleSheet):
  data = {}
  printAbleData = {}
  rules = matchRules(nodeData, styleSheet)
  for rule in rules:
    for attr in rule.atributes:
      data[attr.name] = attr.value
      printAbleData[attr.name] = printValue(attr.value)
  print("TAG WITH A NAME OF: " + nodeData["tag_name"] + " MATCHED WITH: ")
  print(printAbleData)
  return data


# takes in a dom tree (see html.py) and a css tree (see css.py) and smashes they together
def styleTree(root, styleSheet):
  node = styledNode(
    root,
    specifiedValues(root.nodeData, styleSheet) if root.text == "" else {},
    [styleTree(child, styleSheet) for child in root.children])
  node.getImage()
  return node


def parseStyles():
  parse = Parser(html)
  domTree = parse.parseTag()
  parser = cssParser(css)
  sheet = parser.parseStylesheet()
  sheet = sorted(sheet, key=lambda r: r.specificity, reverse=True)
  return styleTree(domTree, sheet)


def main():
  #Make dom tree
  parse = Parser(html)
  domTree = parse.parseTag()
  print(domTree.nodeData["tag_name"])
  printChildren(domTree, 1)
  print(domTree.children[0].children[0].children[0].text)

  # Make syle tree
  print("\n\n===PARSING STYLES===\n\n")
  parser = cssParser(css)
  sheet = parser.parseStylesheet()
  print("===NAVIGATING TREE===")
  # sort our sheet
  sheet = sorted(sheet, key=lambda r: r.specificity, reverse=True)
  for rule in sheet:
    printRule(rule)

  print("DONE" + "\n" * 75)
  print(styleTree(domTree, sheet).children[0].specifiedValues)
