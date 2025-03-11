from Html import *
from Css import *
from style import *

fontWidth = 6
fontHeight = 14
class LayoutBox:

  def __init__(self, dimensions, type, children):
    self.dimensions = dimensions
    # type of boxType should be an enum with each type of box
    self.type = type
    self.children = children

  def getStyleNode(self):
    return self.type.node if self.type.node != None else None

  def getInlineContainer(self):
    # if we are and inline or anonymous box we can append inline children so return ourselvs
    if self.type.type == "inline" or self.type.type == "anonymous":
      return self
    # we are block
    else:
      if len(self.children) == 0 or self.children[-1].type.type != "anonymous":
        self.children.append(
          LayoutBox(dimensionsDefualt(), boxType("anonymous", None), []))
      return self.children[-1]

  def layout(self, containingBlock):
    if self.type.node != None and self.type.node.node.text != "":
      self.layoutText(containingBlock)
    elif self.type.type == "block":
      self.layout_block(containingBlock)
    elif self.type.type == "inline":
      #todo add inline layouts
      print("inline layouts are expiermental")
      self.layoutInline(containingBlock)
    elif self.type.type == "anonymous":
      #todo add inline anonymous
      print("limted support for inline anoumas")
      self.layoutAnonymous(containingBlock)

  def calculateBlockWidth(self, containingBlock):
    style = self.getStyleNode()

    # width has a value of auto if none is given
    width = "auto" if style.value("width") == None else style.value("width")
    if style.image != None:
      width = style.image.width
    # a zerod value
    zero = Value(0, "px")

    # set margin padding and border
    marginLeft = style.lookup("margin-left", "margin", zero)
    marginRight = style.lookup("margin-right", "margin", zero)

    paddingLeft = style.lookup("padding-left", "padding", zero)
    paddingRight = style.lookup("padding-right", "padding", zero)

    borderLeft = style.lookup("border-left", "border", zero)
    borderRight = style.lookup("border-right", "border", zero)

    # total width
    total = sum([
      marginLeft.toPx(),
      marginRight.toPx(),
      paddingLeft.toPx(),
      paddingRight.toPx(),
      borderLeft.toPx(),
      borderRight.toPx(),
      width.toPx() if width != "auto" else 0.0
    ])
    # if width is not auto and the total is wider than the container treat auto margins like 0
    if width != "auto" and total > containingBlock.content.width:
      if marginLeft == "auto":
        marginLeft = zero
      if marginRight == "auto":
        marginRight = zero

    # keep track of the underflow can be negitive

    underflow = containingBlock.content.width - total

    autoMap = (width == "auto", marginLeft == "auto", marginRight == "auto")
    # none are auto so change right margin to difference can be negitive
    if autoMap == (False, False, False):
      marginRight = Value(marginRight.toPx() + underflow, "px")
    if autoMap == (False, False, True): marginRight = Value(underflow, 'px')
    if autoMap == (False, True, False): marginLeft = Value(underflow, 'px')

    # if width is auto any values become 0
    if autoMap[0] == True:
      if marginLeft == "auto": marginLeft = zero
      if marginRight == "auto": marginRight = zero

      if underflow >= 0:
        # expand to fill container
        width = Value(underflow, "px")
      else:
        # width cannot be negitive so ajust the right margin
        width = zero
        marginRight = Value(marginRight.toPx() + underflow, "px")
    if autoMap == (False, True, True):
      marginRight = Value(underflow / 2, "px")
      marginLeft = Value(underflow / 2, "px")
    self.dimensions.content.width = width.toPx()

    self.dimensions.padding.left = paddingLeft.toPx()
    self.dimensions.padding.right = paddingRight.toPx()

    self.dimensions.border.left = borderLeft.toPx()
    self.dimensions.border.right = borderRight.toPx()

    self.dimensions.margin.left = marginLeft.toPx()
    self.dimensions.margin.right = marginRight.toPx()

  def calculateBlockPosition(self, containingBlock):
    style = self.getStyleNode()

    # save a value with zero
    zero = Value(0.0, "px")

    # if margin top or bottom is auto then use the value of zero
    self.dimensions.margin.top = style.lookup("margin-top", "margin",
                                              zero).toPx()
    self.dimensions.margin.bottom = style.lookup("margin-bottom", "margin",
                                                 zero).toPx()

    self.dimensions.border.top = style.lookup("border-top-width", "border",
                                              zero).toPx()
    self.dimensions.border.bottom = style.lookup("border-bottom-width",
                                                 "border", zero).toPx()

    self.dimensions.padding.top = style.lookup("padding-top", "padding",
                                               zero).toPx()
    self.dimensions.padding.bottom = style.lookup("padding-bottom", "padding",
                                                  zero).toPx()

    # set the x pos
    self.dimensions.content.x = containingBlock.content.x + self.dimensions.margin.left + self.dimensions.border.left + self.dimensions.padding.left
    # position the box below all pervious boxes in the container cause its block
    self.dimensions.content.y = containingBlock.content.height + containingBlock.content.y + self.dimensions.margin.top + self.dimensions.border.top + self.dimensions.padding.top

  def layoutBlockChildren(self):
    for child in self.children:
      child.layout(self.dimensions)

      # update the height so each child is laid out below each other
      self.dimensions.content.height += child.dimensions.marginBox().height

  def calculateBlockHeight(self):
    # if the heigth is an explict lenght use that otherwise use exact length
    # otherwise just use keep the value set by layout block children
    if self.getStyleNode().image != None:
      self.dimensions.content.height = self.getStyleNode().image.height
    elif self.getStyleNode().value("height") != None:
      self.dimensions.content.height = self.getStyleNode().value(
        "height").toPx()

  def layout_block(self, containingBlock):
    # child width can be based on parent width so lay the parent out first
    self.calculateBlockWidth(containingBlock)

    # determine the position of the box
    self.calculateBlockPosition(containingBlock)

    # recursively lay out children
    self.layoutBlockChildren()

    # since parent height is based on children this must be called after the children have been layed out
    self.calculateBlockHeight()

  def calculateInlineWidth(self, containingBlock):
    style = self.getStyleNode()

    # a zerod value
    zero = Value(0, "px")

    # set margin padding and border
    marginLeft = style.lookup("margin-left", "margin", zero).toPx()
    marginRight = style.lookup("margin-right", "margin", zero).toPx()

    paddingLeft = style.lookup("padding-left", "padding", zero).toPx()
    paddingRight = style.lookup("padding-right", "padding", zero).toPx()

    borderLeft = style.lookup("border-left", "border", zero).toPx()
    borderRight = style.lookup("border-right", "border", zero).toPx()

    self.dimensions.border.right = borderRight
    self.dimensions.border.left = borderLeft

    self.dimensions.padding.left = paddingLeft
    self.dimensions.padding.right = paddingRight

    self.dimensions.margin.right = marginRight
    self.dimensions.margin.left = marginLeft

    if style.image != None:
      self.dimensions.content.width = style.image.width

  def calculateInlineHeight(self):

    # height is just the fontsize (i think... no one really knows)
    self.dimensions.content.height = fontHeight; 


  def layoutInlineChildren(self):
    for child in self.children:
      child.layout(self.dimensions)

      # update the width other elements can properly lay themselves out
      self.dimensions.content.width += child.dimensions.marginBox().width

  def calculateInlinePos(self, containingBlock):
    style = self.getStyleNode()
    # a zerod value
    zero = Value(0, "px")
    self.dimensions.padding.top = style.lookup("padding-top", "padding", zero ).toPx()
    self.dimensions.padding.bottom = style.lookup("padding-bottom", "padding", zero ).toPx()

    self.dimensions.margin.top = style.lookup("margin-top", "margin", zero ).toPx()
    self.dimensions.margin.bottom = style.lookup("margin-bottom", "margin", zero ).toPx()

    self.dimensions.border.top = style.lookup("border-top", "border", zero ).toPx()
    self.dimensions.border.bottom = style.lookup("border-bottom", "border", zero ).toPx()

    # set the x pos
    self.dimensions.content.x = containingBlock.content.x + containingBlock.content.width + self.dimensions.margin.left + self.dimensions.border.left + self.dimensions.padding.left
    # position the box below all pervious boxes in the container cause its block
    self.dimensions.content.y = containingBlock.content.y

  def layoutInline(self, containingBlock):
    self.calculateInlineWidth(containingBlock)
    self.calculateInlinePos(containingBlock)
    self.calculateInlineHeight()
    # calculate children first
    self.layoutInlineChildren()

  def calculateAnonymousPos(self, containingBlock):
    # blank boxes have no margins or padding so just use default values
    # set the x pos
    self.dimensions.content.x = containingBlock.content.x
    # position the box below all pervious boxes in the container cause its block
    self.dimensions.content.y = containingBlock.content.height + containingBlock.content.y

    
  def layoutAnonymousChildren(self):
    for child in self.children:
      child.layout(self.dimensions)

      # update the width other elements can properly lay themselves out
      self.dimensions.content.width += child.dimensions.marginBox().width
      self.dimensions.content.height = child.dimensions.content.height

  def layoutAnonymous(self, containingBlock):
    self.calculateAnonymousPos(containingBlock)
    self.layoutAnonymousChildren()

  def layoutText(self, containingBlock):
    # width is character width * char count
    self.dimensions.content.width = len(self.type.node.node.text) * fontWidth
    # width and height are just the font size
    self.dimensions.content.height = fontHeight
    # x and y are just defaults
    self.dimensions.content.x = containingBlock.content.x + containingBlock.content.width
    # position the box below all pervious boxes in the container cause its block
    self.dimensions.content.y = containingBlock.content.y

class boxType:

  def __init__(self, type, node=None):
    self.type = type
    self.node = node


class Dimensions:

  def __init__(self, rect, padd, bord, marg):
    # cosition of the content area relitve to the document orgin (type rect)
    self.content = rect

    #surounding edges see box model class of edge sizes
    self.padding = padd
    self.border = bord
    self.margin = marg

  # area covered by content plus padding
  def paddingBox(self):
    return self.content.expandedBy(self.padding)

  # area covered by content plus padding and border
  def borderBox(self):
    return self.paddingBox().expandedBy(self.border)

  # area covered by content plus padding border and margin
  def marginBox(self):
    return self.borderBox().expandedBy(self.margin)


# return a dimension of  all zeros
def dimensionsDefualt():
  return Dimensions(Rect(0, 0, 0, 0), edgesizeDefualt(), edgesizeDefualt(),
                    edgesizeDefualt())


class Rect():

  def __init__(self, x, y, width, heigth):
    self.x = x
    self.y = y
    self.width = width
    self.height = heigth

  # takes in an edge size and adds it to a rect used to add margins, border, and padding
  def expandedBy(self, edge):
    return Rect(self.x - edge.left, self.y - edge.top,
                self.width + edge.left + edge.right,
                self.height + edge.top + edge.bottom)


class edgeSizes:

  def __init__(self, left, right, top, bottom):
    self.left = left
    self.right = right
    self.top = top
    self.bottom = bottom


# return edge sizes of all zeros
def edgesizeDefualt():
  return edgeSizes(0, 0, 0, 0)


def buildLayoutTree(node):
  #create root box dimensions not yet supported
  root = LayoutBox(
    dimensionsDefualt(),
    boxType(node.display(), node) if node.display != "none" else None, [])
  if (root.type.node == None):
    print("NODE: " + node.node.nodeData["tag_name"] +
          "had a display of none (aborting tree)")
    return
  #create children
  for child in node.children:
    # Text is currently an inline element
    if child.node.text != "":
      root.getInlineContainer().children.append(buildLayoutTree(child))
    elif child.display() == "block":
      root.children.append(buildLayoutTree(child))
    elif child.display() == "inline":
      # give the inline some special treatemnt is the case were an block node has an inline child
      # TODO make vice versa (if inline node has block children)
      root.getInlineContainer().children.append(buildLayoutTree(child))
    # nodes with display = none are auto skiped
  return root


def createLayoutTree(root, containingBlock):
  # The layout algorithm expects the container height to start at 0.
  # TODO: Save the initial containing block height, for calculating percent heights.
  containingBlock.content.height = 0.0

  rootBox = buildLayoutTree(root)
  rootBox.layout(containingBlock)
  return rootBox


def genLayTree():
  styleTree = parseStyles()
  initLayout = Dimensions(Rect(0, 0, 800, 600), dimensionsDefualt(),
                          dimensionsDefualt(), dimensionsDefualt())
  layoutTree = createLayoutTree(styleTree, initLayout)
  return layoutTree


def main():
  styleTree = parseStyles()
  print("\n" * 100)
  # viewport size
  initLayout = Dimensions(Rect(0, 0, 800, 600), dimensionsDefualt(),
                          dimensionsDefualt(), dimensionsDefualt())
  layoutTree = createLayoutTree(styleTree, initLayout)
