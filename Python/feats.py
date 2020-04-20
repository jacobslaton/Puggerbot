import compiler as cplr
from compiler import Token

##############
## Compiler ##
##############
ops = ("and", "or", "is", "==", "not", "!", "!=", "in", "contains")
sField = ("name",)
gField = ("req", "desc", "type", "src")
tkndefs = [cplr.ignoreSpace,
           lambda src: cplr.isOperator(src, ops),
           lambda src: cplr.isKeyword(src, sField, "sf"),
           lambda src: cplr.isKeyword(src, gField, "gf"),
           cplr.isString,
           cplr.isParen]
grammar = [
[Token("E"), ((Token("E"), Token("op", "or"), Token("T")),
              lambda stack: cplr.opBinary(stack, "or", "E")),
             ((Token("T"),),
              lambda stack: cplr.castSym1(stack, "E"))],
[Token("T"), ((Token("T"), Token("op", "and"), Token("F")),
              lambda stack: cplr.opBinary(stack, "and", "T")),
             ((Token("F"),),
              lambda stack: cplr.castSym1(stack, "T"))],
[Token("F"), ((Token("paren", "("), Token("E"), Token("paren", ")")),
              lambda stack: cplr.parens(stack, "F")),
             ((Token("op", "not"), Token("F")),
              lambda stack: cplr.opUnaryL(stack, "!", "F")),
             ((Token("op", "!"), Token("F")),
              lambda stack: cplr.opUnaryL(stack, "!", "F")),
             ((Token("S"),),
              lambda stack: cplr.castSym1(stack, "F")),
             ((Token("G"),),
              lambda stack: cplr.castSym1(stack, "F"))],
[Token("S"), ((Token("sf"), Token("op", "is"), Token("str")),
              lambda stack: cplr.opBinary(stack, "==", "S")),
             ((Token("sf"), Token("op", "=="), Token("str")),
              lambda stack: cplr.opBinary(stack, "==", "S")),
             ((Token("sf"), Token("op", "!="), Token("str")),
              lambda stack: cplr.opBinary(stack, "!=", "S"))],
[Token("G"), ((Token("str"), Token("op", "in"), Token("gf")),
              lambda stack: cplr.opBinary(stack, "in", "G")),
             ((Token("gf"), Token("op", "contains"), Token("str")),
              lambda stack: cplr.opBinary(stack, "contains", "G"))]
]
feats = cplr.Compiler(grammar, tkndefs)
print("Built feats compiler.")
#################
## Interpreter ##
#################
def isKwd(kwd):
    return kwd in sField or kwd in gField
def kwdToField(kwd):
    if isKwd(kwd):
        return "ft_"+kwd
    return "ERROR"
def opComp(node, params, op):
    params.append(node.children[1])
    src = " lower("+kwdToField(node.children[0])+") "+op+" lower(?)"
    return src, params
def opConj(node, params, op):
    if type(node.children[0]) == cplr.Node:
        node.children[0], params = interpret(node.children[0], params)
    elif isKwd(node.children[0]):
        node.children[0] = " "+kwdToField(node.children[0])
    if type(node.children[1]) == cplr.Node:
        node.children[1], params = interpret(node.children[1], params)
    elif isKwd(node.children[1]):
        node.children[1] = " "+kwdToField(node.children[1])
    return node.children[0]+" "+op+node.children[1], params
def opCont(node, params):
    params.append(node.children[1])
    return " instr(lower("+kwdToField(node.children[0])+"), lower(?))", params
def opIn(node, params):
    params.append(node.children[0])
    return " instr(lower("+kwdToField(node.children[1])+"), lower(?))", params
def opNot(node, params):
    node = node.children
    node, params = interpret(node, params)
    return " not"+node, params
def interpret(tree, params=[]):
    if tree == cplr.sentinel:
        tree = "select * from feats"
    elif type(tree) != cplr.Node:
        tree = kwdToField(tree)
    elif tree.label == "S\'":
        tree, params = interpret(tree.children, params)
        tree = "select * from feats where"+tree
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


