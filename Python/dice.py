import compiler as cplr
from compiler import Token
import random

##############
## Compiler ##
##############
ops = ("+", "-", "*", "/", "^", "d", "kh", "kl", "dh", "dl", "!", "!!")
tkndefs = [cplr.ignoreSpace,
           lambda src: cplr.isOperator(src, ops),
           cplr.isInteger,
           cplr.isParen]
grammar = [
[Token("E"), ((Token("E"), Token("op", "+"), Token("T")),
              lambda stack: cplr.opBinary(stack, "+", "E")),
             ((Token("E"), Token("op", "-"), Token("T")),
              lambda stack: cplr.opBinary(stack, "-", "E")),
             ((Token("T"),),
              lambda stack: cplr.castSym1(stack, "E"))],
[Token("T"), ((Token("T"), Token("op", "*"), Token("F")),
              lambda stack: cplr.opBinary(stack, "*", "T")),
             ((Token("T"), Token("op", "/"), Token("F")),
              lambda stack: cplr.opBinary(stack, "/", "T")),
             ((Token("T"), Token("op", "^"), Token("F")),
              lambda stack: cplr.opBinary(stack, "^", "T")),
             ((Token("F"),),
              lambda stack: cplr.castSym1(stack, "T"))],
[Token("F"), ((Token("paren", "("), Token("E"), Token("paren", ")")),
              lambda stack: cplr.parens(stack, "F")),
             ((Token("int"),),
              lambda stack: cplr.castSym1(stack, "F")),
             ((Token("D"),),
              lambda stack: cplr.castSym1(stack, "F"))],
[Token("D"), ((Token("op", "d"), Token("F")),
              lambda stack: cplr.opUnaryL(stack, "d", "D", "1")),
             ((Token("F"), Token("op", "d"), Token("F")),
              lambda stack: cplr.opBinary(stack, "d", "D")),
             ((Token("paren", "("), Token("D"), Token("paren", ")")),
              lambda stack: cplr.parens(stack, "D")),
             ((Token("K"),),
              lambda stack: cplr.castSym1(stack, "D"))],
[Token("K"), ((Token("D"), Token("op", "kh")),
              lambda stack: cplr.opUnaryR(stack, "kh", "K", "1")),
             ((Token("D"), Token("op", "kh"), Token("F")),
              lambda stack: cplr.opBinary(stack, "kh", "K")),
             ((Token("D"), Token("op", "kl")),
              lambda stack: cplr.opUnaryR(stack, "kl", "K", "1")),
             ((Token("D"), Token("op", "kl"), Token("F")),
              lambda stack: cplr.opBinary(stack, "kl", "K")),
             ((Token("D"), Token("op", "dh")),
              lambda stack: cplr.opUnaryR(stack, "dh", "K", "1")),
             ((Token("D"), Token("op", "dh"), Token("F")),
              lambda stack: cplr.opBinary(stack, "dh", "K")),
             ((Token("D"), Token("op", "dl")),
              lambda stack: cplr.opUnaryR(stack, "dl", "K", "1")),
             ((Token("D"), Token("op", "dl"), Token("F")),
              lambda stack: cplr.opBinary(stack, "dl", "K")),
             ((Token("D"), Token("op", "!")),
              lambda stack: cplr.opUnaryR(stack, "!", "K", "1")),
             ((Token("D"), Token("op", "!"), Token("F")),
              lambda stack: cplr.opBinary(stack, "!", "K")),
             ((Token("D"), Token("op", "!!")),
              lambda stack: cplr.opUnaryR(stack, "!!", "K", "1")),
             ((Token("D"), Token("op", "!!"), Token("F")),
              lambda stack: cplr.opBinary(stack, "!!", "K"))]
]
dice = cplr.Compiler(grammar, tkndefs)
print("Built dice compiler.")
#################
## Interpreter ##
#################
def opAdd(node, msg):
    msgs = []
    total = 0
    for ii in node.children:
        if type(ii) == cplr.Node:
            submsg, num = interpret(ii)
            total += num
            msgs.append(submsg)
        else:
            total += int(ii)
            msgs.append(ii)
    msg += "+".join(msgs)
    return msg, total
def opSub(node, msg):
    msgs = []
    total = 0
    if type(node.children[0]) == cplr.Node:
        submsg, num = interpret(node.children[0])
        total = num
        msgs.append(submsg)
    else:
        total = int(node.children[0])
        msgs.append(node.children[0])
    for ii in node.children[1:]:
        if type(ii) == cplr.Node:
            submsg, num = interpret(ii)
            total -= num
            msgs.append(submsg)
        else:
            total -= int(ii)
            msgs.append(ii)
    msg += "-".join(msgs)
    return msg, total
def opMul(node, msg):
    msgs = []
    total = 1
    for ii in node.children:
        if type(ii) == cplr.Node:
            submsg, num = interpret(ii)
            total *= num
            if "+" in submsg or "-" in submsg:
                msgs.append("("+submsg+")")
            else:
                msgs.append(submsg)
        else:
            total *= int(ii)
            msgs.append(ii)
    msg += "*".join(msgs)
    return msg, total
def opDiv(node, msg):
    msgs = []
    total = 1
    if type(node.children[0]) == cplr.Node:
        submsg, num = interpret(node.children[0])
        total = num
        if "+" in submsg or "-" in submsg:
            msgs.append("("+submsg+")")
        else:
            msgs.append(submsg)
    else:
        total = int(node.children[0])
        msgs.append(node.children[0])
    for ii in node.children[1:]:
        if type(ii) == cplr.Node:
            submsg, num = interpret(ii)
            total /= num
            if "+" in submsg or "-" in submsg:
                msgs.append("("+submsg+")")
            else:
                msgs.append(submsg)
        else:
            total /= int(ii)
            msgs.append(ii)
    msg += "/".join(msgs)
    return msg, total
def opPow(node, msg):
    msgs = []
    total = 0
    if type(node.children[0]) == cplr.Node:
        submsg, num = interpret(node.children[0])
        total = num
        if "+" in submsg or "-" in submsg:
            msgs.append("("+submsg+")")
        else:
            msgs.append(submsg)
    else:
        total = int(node.children[0])
        msgs.append(node.children[0])
    for ii in node.children[1:]:
        if type(ii) == cplr.Node:
            submsg, num = interpret(ii)
            total = total**num
            if "+" in submsg or "-" in submsg:
                msgs.append("("+submsg+")")
            else:
                msgs.append(submsg)
        else:
            total = total**int(ii)
            msgs.append(ii)
    msg += "^".join(msgs)
    return msg, total
def opDice(node, msg):
    # Die Count
    msg += "("
    dieCount = 0
    if type(node.children[0]) == cplr.Node:
        submsg, dieCount = interpret(node.children[0])
        msg += submsg
    else:
        msg += node.children[0]
        dieCount = int(node.children[0])
    msg += "d"
    # Die Size
    dieSize = 0
    if type(node.children[1]) == cplr.Node:
        submsg, dieSize = interpret(node.children[1])
        msg += submsg
    else:
        msg += node.children[1]
        dieSize = int(node.children[1])
    msg += " => "
    # Rolls
    rolls = []
    for ii in range(dieCount):
        rolls.append(random.randint(1, dieSize))
    msg += "+".join([str(ii) for ii in rolls])+" => "+str(sum(rolls))+")"
    return msg, sum(rolls)
def interpret(tree, msg=""):
    if tree.label == "S\'":
        msg, tree = interpret(tree.children, msg)
    elif tree.label == "+":
        msg, tree = opAdd(tree, msg)
    elif tree.label == "-":
        msg, tree = opSub(tree, msg)
    elif tree.label == "*":
        msg, tree = opMul(tree, msg)
    elif tree.label == "/":
        msg, tree = opDiv(tree, msg)
    elif tree.label == "^":
        msg, tree = opPow(tree, msg)
    elif tree.label == "d":
        msg, tree = opDice(tree, msg)
    return msg, tree
def roll(src):
    msg, num = interpret(dice.compile(src))
    if "d" in src:
        return " => ".join([src, msg, str(num)])
    return " => ".join([src, str(num)])


