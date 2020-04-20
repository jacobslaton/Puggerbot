import compiler as cplr
from compiler import Token

##############
## Compiler ##
##############
intField = ("level",)
strField = ("name", "school", "materials", "tags", "src", "class", "desc")
timeField = ("cast", "duration")
distField = ("range",)
voidField = ("verbal", "somatic", "html")
tUnits = ("day", "days", "hour", "hours", "minute", "minutes",
          "round", "action", "bonus", "reaction")
dUnits = ("mile", "miles", "feet")
timSpc = ("indefinite", "instantaneous", "special")
dstSpc = ("self", "sight", "special", "touch")
tkndefs = [cplr.ignoreSpace,
           lambda src: cplr.isKeyword(src, intField, "intf"),
           lambda src: cplr.isKeyword(src, strField, "strf"),
           lambda src: cplr.isKeyword(src, timeField, "timef"),
           lambda src: cplr.isKeyword(src, distField, "distf"),
           lambda src: cplr.isKeyword(src, voidField, "voidf"),
           lambda src: cplr.isKeyword(src, tUnits, "tUnit"),
           lambda src: cplr.isKeyword(src, dUnits, "dUnit"),
           lambda src: cplr.isKeyword(src, ("special",), "special"),
           lambda src: cplr.isKeyword(src, timSpc, "timSpc"),
           lambda src: cplr.isKeyword(src, dstSpc, "dstSpc"),
           cplr.isInteger,
           cplr.isString,
           cplr.isParen]
def encapSym1(stack, symbol):
    return stack[:-1]+[cplr.Node(symbol, stack[-1])]
def appSym1(stack, symbol):
    children = cplr.data(stack[-2])
    if type(children) == list:
        children.append(stack[-1])
    else:
        children = [cplr.data(stack[-2]), stack[-1]]
    return stack[:-2]+[cplr.Node(symbol, children)]
grammar = [
[Token("L"), ((Token("S"),),
              lambda stack: encapSym1(stack, "L")),
             ((Token("L"), Token("S"),),
              lambda stack: appSym1(stack, "L"))],
[Token("S"), ((Token("paren", "("), Token("P"), Token("paren", ")")),
              lambda stack: cplr.parens(stack, "S"))],
[Token("P"), ((Token("F"),),
              lambda stack: encapSym1(stack, "P")),
             ((Token("P"), Token("F")),
              lambda stack: appSym1(stack, "P"))],
[Token("T"), ((Token("int"), Token("tUnit")),
               lambda stack: cplr.castSym2(stack, "T")),
              ((Token("timSpc"),),
               lambda stack: cplr.castSym1(stack, "T"))],
[Token("D"), ((Token("int"), Token("dUnit")),
               lambda stack: cplr.castSym2(stack, "D")),
              ((Token("dstSpc"),),
               lambda stack: cplr.castSym1(stack, "D"))],
[Token("F"), ((Token("intf", "level"), Token("int")),
              lambda stack: cplr.opUnaryL(stack, "level", "F")),
             ((Token("strf", "name"), Token("str")),
              lambda stack: cplr.opUnaryL(stack, "name", "F")),
             ((Token("strf", "school"), Token("str")),
              lambda stack: cplr.opUnaryL(stack, "school", "F")),
             ((Token("strf", "materials"), Token("str")),
              lambda stack: cplr.opUnaryL(stack, "materials", "F")),
             ((Token("strf", "tags"), Token("str")),
              lambda stack: cplr.opUnaryL(stack, "tags", "F")),
             ((Token("strf", "src"), Token("str")),
              lambda stack: cplr.opUnaryL(stack, "src", "F")),
             ((Token("strf", "class"), Token("str")),
              lambda stack: cplr.opUnaryL(stack, "class", "F")),
             ((Token("strf", "desc"), Token("str")),
              lambda stack: cplr.opUnaryL(stack, "desc", "F")),
             ((Token("timef", "cast"), Token("T")),
              lambda stack: cplr.opUnaryL(stack, "cast", "F")),
             ((Token("timef", "duration"), Token("T")),
              lambda stack: cplr.opUnaryL(stack, "duration", "F")),
             ((Token("timef", "duration"), Token("special")),
              lambda stack: cplr.opUnaryL(stack, "duration", "F")),
             ((Token("distf", "range"), Token("D")),
              lambda stack: cplr.opUnaryL(stack, "range", "F")),
             ((Token("distf", "range"), Token("special")),
              lambda stack: cplr.opUnaryL(stack, "range", "F")),
             ((Token("voidf", "verbal"),),
              lambda stack: cplr.castSym1(stack, "F")),
             ((Token("voidf", "somatic"),),
              lambda stack: cplr.castSym1(stack, "F")),
             ((Token("voidf", "html"),),
              lambda stack: cplr.castSym1(stack, "F"))],
]
spEntry = cplr.Compiler(grammar, tkndefs)
#################
## Interpreter ##
#################
getSchoolIndex = None
def fieldSchool(node, params, op):
    if not getSchoolIndex:
        raise cplr.InterpError("Function getSchoolIndex is not set.")
    params.append(getSchoolIndex(node.children[1]))
    src = " "+kwdToField(node.children[0])+" "+op+" ?"
    return src, params
def fieldTime(spell, field):
    label = cplr.data(field).label
    time = cplr.data(field).children
    if time in timSpc:
        if time == "special" and not "#dur_special" in spell["tags"]:
            spell["tags"].append("dur_special")
        elif not "#"+time in spell["tags"]:
            spell["tags"].append(time)
        spell["duration"] = 0
        return spell
    spell[label] = int(time[0])
    if time[1] in ("hour", "hours"):
        spell[label] *= 60
    elif time[1] in ("day", "days"):
        spell[label] *= 1440
    elif time[1] in ("round", "action", "bonus", "reaction"):
        if not time[1] in spell["tags"]:
            spell["tags"].append(time[1])
    return spell
def fieldDist(spell, field):
    label = cplr.data(field).label
    dist = cplr.data(field).children
    if dist in dstSpc:
        if dist == "special" and not "#range_special" in spell["tags"]:
            spell["tags"].append("range_special")
        elif not dist in spell["tags"]:
            spell["tags"].append(dist)
        spell["range"] = 0
        return spell
    spell[label] = int(dist[0])
    if dist[1] in ("mile", "miles"):
        spell[label] *= 5280
    return spell
def newSpell(data):
    if not getSchoolIndex:
        raise cplr.InterpError("Function getSchoolIndex is not set.")
    spell = {"level":0, "name":"", "school":-1, "materials":"", "tags":[],
             "src":"", "class":[], "desc":"", "cast":-1, "duration":-1,
             "range":-1, "verbal":0, "somatic":0, "html":0}
    for field in cplr.data(data):
        if cplr.data(field) in voidField:
            spell[cplr.data(field)] = 1
            continue
        label = cplr.data(field).label
        if label in timeField:
            spell = fieldTime(spell, field)
        elif label in distField:
            spell = fieldDist(spell, field)
        elif label is "school":
            spell[label] = getSchoolIndex(cplr.data(field).children)
        elif label in ("tags", "class"):
            spell[label] += cplr.data(field).children.split(", ")
        elif label is "level":
            spell[label] = cplr.data(field).children
        elif label is "desc":
            spell[label] += cplr.data(field).children[1:-1]
        else:
            spell[label] += cplr.data(field).children
    spell["name"] = spell["name"].replace("'", "''")
    spell["materials"] = spell["materials"].replace("'", "''")
    spell["desc"] = spell["desc"].replace("'", "''")
    spell["desc"] = spell["desc"].replace("\\\"", "\"")
    spell["tags"] = "#"+"#".join(spell["tags"])
    spell["class"] = "#"+"#".join(spell["class"])
    return """
insert into spells values
(
    '{name}', {level}, {school}, {html},
    {cast}, {range}, {duration}, {verbal}, {somatic}, '{materials}',
    '{tags}', '{src}', '{class}',
    '{desc}'
);
"""[1:].format(**spell)
def interpret(tree):
    if tree == cplr.sentinel:
        tree = ""
    elif type(tree) == list:
        spells = []
        for spell in tree:
            spells.append(newSpell(spell))
        tree = "".join(spells)
    elif tree.label == "S\'":
        tree = interpret(tree.children)
    elif tree.label == "S" and type(tree.children) == list:
        tree = newSpell(tree)
    return tree
def load(filename):
    src = ""
    with open(filename, "r") as fin:
        for ii in fin:
            src += ii
    return interpret(spEntry.compile(src))


