import compiler as cplr
from compiler import Token

##############
## Compiler ##
##############
ops = ("and", "or", "is", "==", "not", "!", "!=", "in", "contains",
       "<", ">", "<=", ">=")
iField = ("age", "speed")
sField = ("name", "subrace", "size")
gField = ("stats", "lang", "feats", "src")
tkndefs = [cplr.ignoreSpace,
           lambda src: cplr.isOperator(src, ops),
           lambda src: cplr.isKeyword(src, iField, "if"),
           lambda src: cplr.isKeyword(src, sField, "sf"),
           lambda src: cplr.isKeyword(src, gField, "gf"),
           cplr.isInteger,
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
             ((Token("I"),),
              lambda stack: cplr.castSym1(stack, "F")),
             ((Token("S"),),
              lambda stack: cplr.castSym1(stack, "F")),
             ((Token("G"),),
              lambda stack: cplr.castSym1(stack, "F"))],
[Token("I"), ((Token("if"), Token("op", "is"), Token("int")),
              lambda stack: cplr.opBinary(stack, "==", "I")),
             ((Token("if"), Token("op", "=="), Token("int")),
              lambda stack: cplr.opBinary(stack, "==", "I")),
             ((Token("if"), Token("op", "!="), Token("int")),
              lambda stack: cplr.opBinary(stack, "!=", "I"))],
[Token("S"), ((Token("sf"), Token("op", "is"), Token("str")),
              lambda stack: cplr.opBinary(stack, "==", "S")),
             ((Token("sf"), Token("op", "=="), Token("str")),
              lambda stack: cplr.opBinary(stack, "==", "S")),
             ((Token("sf"), Token("op", "!="), Token("str")),
              lambda stack: cplr.opBinary(stack, "==", "S"))],
[Token("G"), ((Token("str"), Token("op", "in"), Token("gf")),
              lambda stack: cplr.opBinary(stack, "in", "G")),
             ((Token("gf"), Token("op", "contains"), Token("str")),
              lambda stack: cplr.opBinary(stack, "contains", "G"))]
]
races = cplr.Compiler(grammar, tkndefs)
print("Built races compiler.")
#################
## Interpreter ##
#################
getSizeIndex = None
def isKwd(kwd):
    return kwd in iField or kwd in sField or kwd in gField
def kwdToField(kwd):
    if kwd in ("name", "size", "speed"):
        return "races.rc_"+kwd
    if kwd in ("stats", "lang", "feats", "src"):
        query = " (instr(lower(races.rc_"+kwd+"), lower(?)) or"
        query += " instr(lower(subraces.sr_"+kwd+"), lower(?)))"
        return query
    if kwd == "subrace":
        return "subraces.sr_"+kwd
    if kwd == "age":
        return "races.rc_"+kwd
    return "ERROR"
def opComp(node, params, op):
    if node.children[0] == "size":
        params.append(getSizeIndex(node.children[1]))
    else:
        params.append(node.children[1])
    src = " "
    if node.children[0] == "size" or node.children[0] in iField:
        src += kwdToField(node.children[0])+" "+op+" ?"
    else:
        src += "lower("+kwdToField(node.children[0])+") "+op+" lower(?)"
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
    params.append(node.children[1])
    return kwdToField(node.children[0]), params
def opIn(node, params):
    params.append(node.children[0])
    params.append(node.children[0])
    return kwdToField(node.children[1]), params
def opNot(node, params):
    node = node.children
    node, params = interpret(node, params)
    return " not"+node, params
def interpret(tree, params=[]):
    if tree == cplr.sentinel:
        tree = "select races.rc_name, subraces.sr_sub, "
        tree += "races.rc_stats, subraces.sr_stats, races.rc_age_adult, "
        tree += "races.rc_age_max, races.rc_size, races.rc_speed, "
        tree += "races.rc_height, races.rc_weight, races.rc_lang, "
        tree += "subraces.sr_lang, races.rc_feats, subraces.sr_feats, "
        tree += "races.rc_src, subraces.sr_src from races "
        tree += "left outer join subraces on races.rc_name=subraces.sr_race"
    elif type(tree) != cplr.Node:
        tree = kwdToField(tree)
    elif tree.label == "S\'":
        tree, params = interpret(tree.children, params)
        query = "select races.rc_name, subraces.sr_sub, "
        query += "races.rc_stats, subraces.sr_stats, races.rc_age_adult, "
        query += "races.rc_age_max, races.rc_size, races.rc_speed, "
        query += "races.rc_height, races.rc_weight, races.rc_lang, "
        query += "subraces.sr_lang, races.rc_feats, subraces.sr_feats, "
        query += "races.rc_src, subraces.sr_src from races "
        query += "left outer join subraces on "
        query += "races.rc_name=subraces.sr_race where"+tree
        tree = query
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


