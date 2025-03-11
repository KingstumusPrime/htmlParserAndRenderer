from keyWords import colorMap
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "1234567890"
css = """
p, div {
  color:red;
  width: 200px;
}

.error, #failParse, #dogs {
  color: #0EFA00;
  display: block;
}

html { display: block; padding: 12px;}
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
"""

units = ["px"]


class styleRule():

  def __init__(self, selectors, atributes, specificity):
    self.selectors = selectors
    self.atributes = atributes
    self.specificity = specificity


class Selector:

  def __init__(self, name=None, sClass=None, id=None):
    self.name = name
    self.sClass = sClass
    self.id = id


class Atribute:

  def __init__(self, name, value):
    self.name = name
    self.value = value


class Value:

  def __init__(self, value, unit=None):
    self.value = value
    self.unit = unit

  def toPx(self):
    if self.unit == "px":
      return int(self.value)
    else:
      return 0.0


class cssParser:

  def __init__(self, text):
    self.text = text
    self.pos = 0

  def nextChar(self):
    if (self.pos >= len(self.text)):
      return -1
    return self.text[self.pos]

  def eat(self, charecter, muted=False):
    if (self.text[self.pos] == charecter):
      self.pos += 1
      return True
    elif not muted:
      print("ERROR: Expected " + charecter + " recived: " +
            self.text[self.pos])
      return False

  def eatText(self):
    res = ""
    if self.pos > len(self.text) - 1: return
    while self.text[self.pos].upper() in alphabet + "*-":
      res += self.text[self.pos]
      self.pos += 1
      if self.pos > len(self.text) - 1:
        break
    return res

  def startsWith(self, value):
    return self.text.startswith(value, self.pos)

  def eatSpace(self):
    if self.pos >= len(self.text): return
    while self.text[self.pos] == " " or self.text[self.pos] == "\n":
      self.pos += 1
      if self.pos > len(self.text) - 1:
        break

  def eatPrefix(self):
    prefixs = "#."
    for i in prefixs:
      if (self.eat(i, True)):
        return i
    return ""

  def parseSelector(self):
    prefix = self.eatPrefix()
    name = self.eatText()
    print("FOUND SELETOR WITH A NAME OF: " + prefix + name)
    if (prefix == "."):
      return Selector(sClass=name)
    elif prefix == "#":
      return Selector(id=name)
    else:
      return Selector(name=name)

  def parseSelectors(self):
    selects = []
    while (self.nextChar() != "{"):
      self.eatSpace()
      selects.append(self.parseSelector())
      self.eatSpace()
      if (self.nextChar() == ","):
        self.eat(",")
        self.eatSpace()
    return selects

  def getSpecity(self, selectors):
    # replace a with zero becuse style tags are not supported
    a = 0
    b = 0
    c = 0
    d = 0
    for selct in selectors:
      if selct.sClass:
        c += 1
      if selct.id:
        b += 1
      if selct.name:
        d += 1
    return (a, b, c, d)

  def parseAtribute(self):
    self.eatSpace()
    atr = self.eatText()
    self.eatSpace()
    self.eat(":")
    self.eatSpace()
    val, unit = self.parseValue()
    self.eat(";")
    if (type(val) != dict):
      print("PARSED A " + atr + " WITH A VALUE OF " + val)
    return Atribute(atr, Value(val, unit))

  def parseNum(self):
    res = ""
    if self.pos > len(self.text) - 1: return
    while self.text[self.pos] in numbers:
      res += self.text[self.pos]
      self.pos += 1
      if self.pos > len(self.text) - 1:
        break
    return res

  def parseUnit(self):
    for u in units:
      if self.startsWith(u):
        print("FOUND UNIT OF: " + u)
        self.pos += len(u)
        return u

  def parseLength(self):
    val = self.parseNum()
    unit = self.parseUnit()
    return (val, unit)

  def parseValue(self):
    if (self.nextChar() in numbers):
      return self.parseLength()
    elif self.nextChar() == "#":
      return (self.parseColor(), None)
    else:
      # if a keyword check if it is really a color name
      word = self.eatText()
      if word.lower() in colorMap:
        word = colorMap[word.lower()]
      return (word, None)

  def parseColor(self):
    self.eat("#")
    res = {
      "R": self.parseHexPair(),
      "G": self.parseHexPair(),
      "B": self.parseHexPair()
    }
    print("R: " + str(res["R"]) + " G: " + str(res["G"]) + " B: " +
          str(res["B"]))
    return res

  def parseHexPair(self):
    val = self.text[self.pos] + self.text[self.pos + 1]
    self.pos += 2
    return int(val, 16)

  def parseAtributes(self):
    attrs = []
    while (self.nextChar() != "}"):
      attrs.append(self.parseAtribute())
      self.eatSpace()
    return attrs

  def parseRule(self):
    selct = self.parseSelectors()
    self.eat("{")
    attrs = self.parseAtributes()
    self.eat("}")
    return styleRule(selct, attrs, self.getSpecity(selct))

  def parseStylesheet(self):
    sheet = []
    while self.pos < len(self.text):
      sheet.append(self.parseRule())
      self.eatSpace()
    return sheet


def printValue(val):
  if type(val.value) == dict:
    return "rgb(" + str(val.value["R"]) + ", " + str(
      val.value["G"]) + ", " + str(val.value["B"]) + ")"
  if val.unit:
    return str(val.value) + val.unit
  return val.value


def printRule(rule):
  print("PARSING RULE")
  for selct in rule.selectors:
    if selct.sClass:
      print("CLASS: " + selct.sClass)
    if selct.id:
      print("id: " + selct.id)
    if selct.name:
      print(selct.name)
  print(rule.specificity)
  for i, attr in enumerate(rule.atributes):
    print(attr.name + ":" + printValue(attr.value))


def main():
  parser = cssParser(css)
  sheet = parser.parseStylesheet()
  print("===NAVIGATING TREE===")
  for rule in sheet:
    printRule(rule)
