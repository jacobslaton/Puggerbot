import compiler as cplr
from compiler import Token as Tkn

##############
## Compiler ##
##############
ops = ("and", "or", "is", "==", "not", "!", "!=", "in", "contains",
       "<", ">", "<=", ">=")
intField = ("level",)
strField = ("name", "school")
timeField = ("cast", "duration")
distField = ("range",)
voidField = ("verbal", "somatic")
grpField = ("materials", "tags", "src", "class", "desc")
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
           lambda src: cplr.isKeyword(src, grpField, "grpf"),
           lambda src: cplr.isKeyword(src, tUnits, "tUnit"),
           lambda src: cplr.isKeyword(src, dUnits, "dUnit"),
           lambda src: cplr.isKeyword(src, ("special",), "special"),
           lambda src: cplr.isKeyword(src, timSpc, "timSpc"),
           lambda src: cplr.isKeyword(src, dstSpc, "dstSpc"),
           lambda src: cplr.isOperator(src, ops),
           cplr.isInteger,
           cplr.isString,
           cplr.isParen]
grammar = [
[Tkn("EXPR"), ((Tkn("EXPR"), Tkn("op", "or"), Tkn("TERM")),
               lambda stack: cplr.opBinary(stack, "or", "EXPR")),
              ((Tkn("TERM"),),
               lambda stack: cplr.castSym1(stack, "EXPR"))],
[Tkn("TERM"), ((Tkn("TERM"), Tkn("op", "and"), Tkn("FCTR")),
               lambda stack: cplr.opBinary(stack, "and", "TERM")),
              ((Tkn("FCTR"),),
               lambda stack: cplr.castSym1(stack, "TERM"))],
[Tkn("FCTR"), ((Tkn("paren", "("), Tkn("EXPR"), Tkn("paren", ")")),
               lambda stack: cplr.parens(stack, "FCTR")),
              ((Tkn("op", "not"), Tkn("FCTR")),
               lambda stack: cplr.opUnaryL(stack, "!", "FCTR")),
              ((Tkn("op", "!"), Tkn("FCTR")),
               lambda stack: cplr.opUnaryL(stack, "!", "FCTR")),
              ((Tkn("INTF"),),
               lambda stack: cplr.castSym1(stack, "FCTR")),
              ((Tkn("STRF"),),
               lambda stack: cplr.castSym1(stack, "FCTR")),
              ((Tkn("TIMF"),),
               lambda stack: cplr.castSym1(stack, "FCTR")),
              ((Tkn("DSTF"),),
               lambda stack: cplr.castSym1(stack, "FCTR")),
              ((Tkn("voidf"),),
               lambda stack: cplr.castSym1(stack, "FCTR")),
              ((Tkn("GRPF"),),
               lambda stack: cplr.castSym1(stack, "FCTR"))],
[Tkn("TIMP"), ((Tkn("int"), Tkn("tUnit")),
               lambda stack: cplr.castSym2(stack, "TIMP")),
              ((Tkn("timSpc"),),
               lambda stack: cplr.castSym1(stack, "TIMP"))],
[Tkn("DSTP"), ((Tkn("int"), Tkn("dUnit")),
               lambda stack: cplr.castSym2(stack, "DSTP")),
              ((Tkn("dstSpc"),),
               lambda stack: cplr.castSym1(stack, "DSTP"))],
[Tkn("INTF"), ((Tkn("intf"), Tkn("op", "is"), Tkn("int")),
               lambda stack: cplr.opBinary(stack, "==", "INTF")),
              ((Tkn("intf"), Tkn("op", "=="), Tkn("int")),
               lambda stack: cplr.opBinary(stack, "==", "INTF")),
              ((Tkn("intf"), Tkn("op", "!="), Tkn("int")),
               lambda stack: cplr.opBinary(stack, "!=", "INTF")),
              ((Tkn("intf"), Tkn("op", "<"), Tkn("int")),
               lambda stack: cplr.opBinary(stack, "<", "INTF")),
              ((Tkn("intf"), Tkn("op", ">"), Tkn("int")),
               lambda stack: cplr.opBinary(stack, ">", "INTF")),
              ((Tkn("intf"), Tkn("op", "<="), Tkn("int")),
               lambda stack: cplr.opBinary(stack, "<=", "INTF")),
              ((Tkn("intf"), Tkn("op", ">="), Tkn("int")),
               lambda stack: cplr.opBinary(stack, ">=", "INTF"))],
[Tkn("STRF"), ((Tkn("strf"), Tkn("op", "is"), Tkn("str")),
               lambda stack: cplr.opBinary(stack, "==", "STRF")),
              ((Tkn("strf"), Tkn("op", "=="), Tkn("str")),
               lambda stack: cplr.opBinary(stack, "==", "STRF")),
              ((Tkn("strf"), Tkn("op", "!="), Tkn("str")),
               lambda stack: cplr.opBinary(stack, "!=", "STRF"))],
[Tkn("TIMF"), ((Tkn("timef"), Tkn("op", "is"), Tkn("TIMP")),
               lambda stack: cplr.opBinary(stack, "==", "TIMF")),
              ((Tkn("timef"), Tkn("op", "=="), Tkn("TIMP")),
               lambda stack: cplr.opBinary(stack, "==", "TIMF")),
              ((Tkn("timef"), Tkn("op", "!="), Tkn("TIMP")),
               lambda stack: cplr.opBinary(stack, "!=", "TIMF"))],
[Tkn("DSTF"), ((Tkn("distf"), Tkn("op", "is"), Tkn("DSTP")),
               lambda stack: cplr.opBinary(stack, "==", "DSTF")),
              ((Tkn("distf"), Tkn("op", "=="), Tkn("DSTP")),
               lambda stack: cplr.opBinary(stack, "==", "DSTF")),
              ((Tkn("distf"), Tkn("op", "!="), Tkn("DSTP")),
               lambda stack: cplr.opBinary(stack, "!=", "DSTF"))],
[Tkn("GRPF"), ((Tkn("str"), Tkn("op", "in"), Tkn("grpf")),
               lambda stack: cplr.opBinary(stack, "in", "GRPF")),
              ((Tkn("grpf"), Tkn("op", "contains"), Tkn("str")),
               lambda stack: cplr.opBinary(stack, "contains", "GRPF"))]
]
spells = cplr.Compiler(grammar, tkndefs)
print("Built spells compiler.")
#################
## Interpreter ##
#################
getSchoolIndex = None
def isKwd(kwd):
    return kwd in intField+strField+voidField+grpField
def kwdToField(kwd):
    if kwd in ("name", "school", "cast", "range", "duration", "tags", "src",
               "desc"):
        return "sp_"+kwd
    if kwd == "level":
        return "sp_lvl"
    if kwd == "verbal":
        return "sp_comp_v"
    if kwd == "somatic":
        return "sp_comp_s"
    if kwd == "materials":
        return "sp_comp_m"
    if kwd == "class":
        return "sp_classes"
    return "ERROR"
def fieldSchool(node, params, op):
    if not getSchoolIndex:
        raise cplr.InterpError("Function getSchoolIndex is not set.")
    params.append(getSchoolIndex(node.children[1]))
    src = " "+kwdToField(node.children[0])+" "+op+" ?"
    return src, params
def fieldCast(node, params, op):
    if type(node.children[1]) != list:
        errstr = "Casting time cannot be measured using \""+node.children[1]
        errstr += "\" as units."
        raise cplr.InterpError(errstr)
    src = kwdToField(node.children[0])+" "+op+" ?"
    time = node.children[1][0]
    if node.children[1][1] in ("minute", "minutes"):
        src = " "+src
        params.append(time)
    elif node.children[1][1] in ("hour", "hours"):
        src = " "+src
        params.append(time*60)
    elif node.children[1][1] in ("day", "days"):
        src = " "+src
        params.append(time*1440)
    elif node.children[1][1] in ("action", "bonus", "reaction"):
        src = " ("+src+" and instr(sp_tags, ?))"
        params += [time, "#"+node.children[1][1]]
    else:
        errstr = "Casting time cannot be measured using \""+node.children[1][1]
        errstr += "\" as units."
        raise cplr.InterpError(errstr)
    return src, params
def fieldRange(node, params, op):
    src = kwdToField(node.children[0])+" "+op+" ?"
    dist = node.children[1][0]
    if type(node.children[1]) != list:
        src = " instr(sp_tags, ?)"
        if node.children[1] == "special":
            node.children[1] = "range_special"
        params.append("#"+node.children[1])
    elif node.children[1][1] in ("mile", "miles"):
        src = " "+src
        params.append(dist*5280)
    elif node.children[1][1] in ("feet"):
        src = " "+src
        params.append(dist)
    else:
        errstr = "Casting time cannot be measured using \""+node.children[1][1]
        errstr += "\" as units."
        raise cplr.InterpError(errstr)
    return src, params
def fieldDur(node, params, op):
    src = kwdToField(node.children[0])+" "+op+" ?"
    time = node.children[1][0]
    if type(node.children[1]) != list:
        src = " instr(sp_tags, ?)"
        if node.children[1] == "special":
            node.children[1] = "dur_special"
        params.append(node.children[1])
    elif node.children[1][1] in ("minute", "minutes"):
        src = " "+src
        params.append(time)
    elif node.children[1][1] in ("hour", "hours"):
        src = " "+src
        params.append(time*60)
    elif node.children[1][1] in ("day", "days"):
        src = " "+src
        params.append(time*1440)
    elif node.children[1][1] in "round":
        src = " ("+src+" and instr(sp_tags, ?))"
        params += [time, "#"+node.children[1][1]]
    else:
        errstr = "Casting time cannot be measured using \""+node.children[1][1]
        errstr += "\" as units."
        raise cplr.InterpError(errstr)
    return src, params
def opComp(node, params, op):
    if node.children[0] == "school":
        return fieldSchool(node, params, op)
    if node.children[0] == "cast":
        return fieldCast(node, params, op)
    if node.children[0] == "range":
        return fieldRange(node, params, op)
    if node.children[0] == "duration":
        return fieldDur(node, params, op)
    params.append(node.children[1])
    src = " "
    if node.children[0] in intField:
        src += kwdToField(node.children[0])+" "+op+" ?"
    else:
        src += "lower("+kwdToField(node.children[0])+") "+op+" lower(?)"
    return src, params
def opConj(node, params, op):
    if type(node.children[0]) == cplr.Node:
        node.children[0], params = interpret(node.children[0], params)
    elif node.children[0] in voidField:
        node.children[0] = " "+kwdToField(node.children[0])
    if type(node.children[1]) == cplr.Node:
        node.children[1], params = interpret(node.children[1], params)
    elif node.children[1] in voidField:
        node.children[1] = " "+kwdToField(node.children[1])
    if op == "or":
        return " ("+node.children[0][1:]+" "+op+node.children[1]+")", params
    return node.children[0]+" "+op+node.children[1], params
def opCont(node, params):
    if node.children[0] == "tags":
        node.children[1] = "#"+node.children[1]
    params.append(node.children[1])
    return " instr(lower("+kwdToField(node.children[0])+"), lower(?))", params
def opIn(node, params):
    if node.children[1] == "tags":
        node.children[0] = "#"+node.children[0]
    params.append(node.children[0])
    return " instr(lower("+kwdToField(node.children[1])+"), lower(?))", params
def opNot(node, params):
    node = node.children
    node, params = interpret(node, params)
    return " not"+node, params
def interpret(tree, params=[]):
    if tree == cplr.sentinel:
        tree = "select * from spells"
    elif type(tree) != cplr.Node:
        tree = kwdToField(tree)
    elif tree.label == "S\'":
        tree, params = interpret(tree.children, params)
        tree = "select * from spells where"+tree
    elif tree.label in ("==", "!=", "<", ">", "<=", ">="):
        tree, params = opComp(tree, params, tree.label)
    elif tree.label in ("and", "or"):
        tree, params = opConj(tree, params, tree.label)
    elif tree.label == "contains":
        tree, params = opCont(tree, params)
    elif tree.label == "in":
        tree, params = opIn(tree, params)
    elif tree.label == "!":
        tree, params = opNot(tree, params)
    return tree, params


