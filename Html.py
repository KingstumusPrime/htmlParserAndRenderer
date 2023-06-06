html = """
<html>
 <div>
  <p id="hello" class="WORLD">Hello world</p>
  <p></p>
 </div>
</html>"""
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Node:

  def __init__(self, children, tageName=None, Atributes=None, text=""):
    # nodes children
    self.children = children
    # the type of the node
    self.nodeData = {"tag_name": tageName, "atributes": Atributes}
    self.text = text


def text(data):
  return Node([], text=data)


class Parser:

  def __init__(self, text):
    self.text = text
    self.pos = 0

  def eat(self, charecter):
    if (self.text[self.pos] == charecter):
      self.pos += 1
      return True
    else:
      print("ERROR: Expected " + charecter + " recived: " +
            self.text[self.pos])
      return False

  def eatText(self):
    res = ""
    if self.pos > len(self.text) - 1: return
    while self.text[self.pos].upper() in alphabet:
      res += self.text[self.pos]
      self.pos += 1
      if self.pos > len(self.text) - 1:
        break
    return res

  def eatSpace(self):
    if self.pos > len(self.text) - 1: return
    while self.text[self.pos] == " " or self.text[self.pos] == "\n":
      if self.pos > len(self.text) - 1:
        break
      self.pos += 1

  def nextChar(self):
    return self.text[self.pos]

  def parseNode(self):
    node = None
    if (self.nextChar() == "<"):
      node = self.parseTag()
    else:
      node = self.parseText()
    return node

  def parseText(self):
    res = ""
    while self.pos != len(self.text) and self.text[self.pos] != "<":
      res += self.text[self.pos]
      self.pos += 1
    print("PARSED TEXT WITH A VALUE OF: " + res)
    return text(res)

  def parseNodes(self):
    nodes = []
    while not self.startsWith("</") and self.pos < len(self.text):
      nodes.append(self.parseNode())
    return nodes

  def startsWith(self, value):
    return self.text.startswith(value, self.pos)

  def parseTag(self):
    self.eatSpace()
    if (self.eat("<")):
      tagName = self.eatText()
      print("STARTED PARSING TAG WITH A NAME OF: " + tagName)
      atributes = self.parseAtributes()
      self.eat(">")
      self.eatSpace()

      children = self.parseNodes()

      self.eat("<")
      self.eat("/")
      if (self.eatText() != tagName):
        print("ERROR INVALID TAG")
      print("FINISHED PARSING TAG WITH A NAME OF: " + tagName)
      self.eat(">")
      self.eatSpace()
      return Node(children, tagName, atributes)

  def parseAtributeValue(self):
    if self.eat('"'):
      value = self.eatText()
      while self.nextChar() != '"':
        self.eatSpace()
        value += " " + self.eatText()
        
      if (self.eat('"')):
        return value
      print("ERROR EXPECTED CLOSING QOUTE")
      return "ERROR EXPECTED CLOSING QOUTE"
    print("ERROR OPENING CLOSING QOUTE")
    return "ERROR EXPECTED OPENING QOUTE"

  def parseAtribute(self):
    name = self.eatText()
    self.eatSpace()
    if self.eat("="):
      self.eatSpace()
      value = self.parseAtributeValue()
      print("PARSED: " + name + " WITH A VALUE OF: " + value)
      return name, value

  def parseAtributes(self):
    atributes = {}
    while self.nextChar() != ">":
      self.eatSpace()
      (name, value) = self.parseAtribute()
      atributes[name] = value
    return atributes


def printChildren(node, layers=0):
  for child in node.children:
    if(child.nodeData["tag_name"] != None):
      str =  child.nodeData["tag_name"]
      if len(child.nodeData["atributes"]):
        for key in child.nodeData["atributes"]: 
          str += " " + key + "=" + child.nodeData["atributes"][key]
      print( "-" * layers + str)
    else:
      print("-" * layers + "text:"+ child.text)
    printChildren(child, layers + 1)


def main():
  parse = Parser(html)
  domTree = parse.parseTag()
  print(domTree.nodeData["tag_name"])
  printChildren(domTree, 1)
  print(domTree.children[0].children[0].children[0].text)

