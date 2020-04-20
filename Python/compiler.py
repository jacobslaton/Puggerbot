import copy

#########################
## Classes and Utility ##
#########################
class Token:
    def __init__(self, label:str, value=None):
        self.label = label
        self.value = value
    def __repr__(self):
        return "Token("+repr(self.label)+", "+repr(self.value)+")"
    def __str__(self):
        if self.value:
            return str(self.value)
        return str(self.label)
    def __eq__(self, other):
        if type(other) != Token:
            return False
        return self.label == other.label and self.value == other.value
    def __hash__(self):
        return hash((self.label, self.value))
class Node:
    def __init__(self, label:str, children:list):
        self.label = label
        self.children = children
    def __repr__(self):
        return "Node("+repr(self.label)+", "+repr(self.children)+")"
class LexError(Exception): pass
class ParseError(Exception): pass
class InterpError(Exception): pass
def data(obj):
    if type(obj) == Token:
        return obj.value
    if type(obj) == Node:
        return obj.children
    return None
###############
## Constants ##
###############
rootSymbol = "S'"
sentinel = Token("$")
dotToken = Token(".")
epsToken = Token("eps")
###########################
## Finite State Automata ##
###########################
def endParse(stack):
    return [Node(rootSymbol, data(stack[0]))]
def genNFA(grammar):
    if grammar[0] != [Token(rootSymbol), ((grammar[0][0],), endParse)]:
        grammar.insert(0, [Token(rootSymbol), ((grammar[0][0],), endParse)])
    ## Find Items
    states = []
    for rl in grammar:
        for rhs in rl[1:]:
            terms = rhs[0]
            for dot in range(len(terms)+1):
                state = [rl[0]]+[list(terms[:dot])+[dotToken]+list(terms[dot:])]
                states.append(state)
    ## Find Edges
    edges = []
    ## Find Next-Move Edges
    # For all states that cannot reduce
    for src in [ss for ss in states if ss[1][-1] != dotToken]:
        move = src[1][src[1].index(dotToken)+1]
        mvAlpha = src[1][:src[1].index(dotToken)]+[move]
        for dest in states:
            destAlpha = dest[1][:dest[1].index(dotToken)]
            if mvAlpha == destAlpha:
                edge = [states.index(src), move, states.index(dest)]
                if not edge in edges:
                    edges.append(edge)
    ## Find Same-Alpha Edges
    for src in [ss for ss in states if ss[1][-1] != dotToken]:
        srcAlpha = src[1][:src[1].index(dotToken)]
        for dest in [ss for ss in states if ss != src]:
            destAlpha = dest[1][:dest[1].index(dotToken)]
            if srcAlpha == destAlpha:
                edge = [states.index(src), epsToken, states.index(dest)]
                if not edge in edges:
                    edges.append(edge)
    ## Find Different-State Edges
    for src in [ss for ss in states if ss[1][-1] != dotToken]:
        move = src[1][src[1].index(dotToken)+1]
        # For all states that have no alpha
        for dest in [ss for ss in states if ss[1][0] == dotToken]:
            if dest[0] == move:
                edge = [states.index(src), epsToken, states.index(dest)]
                if not edge in edges:
                    edges.append(edge)
    states = [[ii] for ii in states]
    ## Organize Reductions
    reducs = {}
    for index in range(len(states)):
        rStates = [item for item in states[index] if item[1][-1] == dotToken]
        if rStates:
            reducs[index] = []
            for state in rStates:
                for rl in grammar:
                    for rhs in rl[1:]:
                        terms, func = rhs
                        if tuple(state[1][:-1]) == terms:
                            reducs[index].append(rhs)
    return (states, edges, reducs)
def epsStar(fsa, state, checked=set()):
    checked.update([state])
    move = set([state])
    for ii in [edge for edge in fsa[1] if edge[0] == state]:
        if ii[1] == epsToken:
            move.update([ii[2]])
    for ii in move-checked:
        temp = epsStar(fsa, ii, checked)
        move.update(temp)
    return move
def reduceFSA(fsa):
    states, edges, reducs = [], [], {}
    ## Symbols
    symbols = set()
    for edge in fsa[1]:
        symbols.update([edge[1]])
    symbols -= set([epsToken])
    symbols = tuple(sorted(list(symbols), key=lambda xx: xx.label))
    ## Conversion
    states.append(epsStar(fsa, 0, set()))
    index = 0
    while index < len(states):
        ss = states[index]
        for ii in symbols:
            # Find all states that can be reached by making the current move
            move = set()
            for jj in [edge for edge in fsa[1] if edge[0] in ss]:
                if jj[1] == ii:
                    move.update([jj[2]])
            dest = set()
            for jj in move:
                dest.update(epsStar(fsa, jj, set()))
            # Make sure there is only one starting state
            dest -= set([0])
            # If the current move would go to a state that does not exist, then
            # add that state
            if dest and not dest in states:
                states.append(dest)
            # If the current move goes to a state, then add it to edges
            if dest:
                edges.append([index, ii, states.index(dest)])
        # If the current state contains reduction states, then update reducs
        for key, item in fsa[2].items():
            if key in ss:
                if index in reducs and not item[0] in reducs[index]:
                    reducs[index].append(item[0])
                elif not index in reducs:
                    reducs[index] = copy.deepcopy(item)
        index += 1
    for key, val in reducs.items():
        reducs[key] = sorted(val, key=lambda xx: len(xx[0]))
    ## Translate States
    for ii in range(len(states)):
        indices = states[ii]
        states[ii] = []
        for jj in indices:
            states[ii] += fsa[0][jj]
    ## Return
    return (states, edges, reducs)
######################
## Lexer and Parser ##
######################
def lex(tokdefs, src):
    tokens = []
    badLexeme = ""
    while src != "":
        prevSrc = src
        for func in tokdefs:
            src, token = func(src)
            if token != None:
                tokens.append(token)
        if prevSrc == src:
            badLexeme += src[0]
            src = src[1:]
        elif badLexeme != "":
            raise LexError("Invalid lexeme: \""+badLexeme+"\"")
    return tokens
def parse(dfa, tokens):
    states, edges, reducs = dfa
    tokens += [sentinel]
    stack = [tokens.pop(0)]
    while tokens:
        lookahead = tokens.pop(0)
        simplified = False
        while not simplified:
            simplified = True
            state = 0
            for token in stack:
                shift = [edge for edge in edges if edge[0] == state]
                moves = [edge[1] for edge in shift]
                mvGeneric = [mv.label for mv in moves if mv.value == None]
                if token in moves or token.label in mvGeneric:
                    shiftToken = token
                    if not shiftToken in moves:
                        shiftToken = Token(token.label, None)
                    for edge in shift:
                        if shiftToken == edge[1]:
                            state = edge[2]
                else:
                    errstr = "Cannot shift in state #"+str(state)+" given "
                    errstr += repr(token)+"."
                    raise ParseError(errstr)
            shift = [edge[1] for edge in edges if edge[0] == state]
            shiftTypes = [edge.label for edge in shift if edge.value == None]
            if not lookahead in shift and not lookahead.label in shiftTypes:
                if not state in reducs:
                    raise ParseError("Cannot reduce in state #"+str(state)+".")
                reduc = None
                for rd in reducs[state]:
                    if len(rd[0]) <= len(stack):
                        match = True
                        for ii in range(-len(rd[0]), 0):
                            if rd[0][ii] != stack[ii]:
                                if rd[0][ii].value == None:
                                    if rd[0][ii].label != stack[ii].label:
                                        match = False
                        if match:
                            reduc = rd
                if not reduc:
                    errstr = "Could not resolve reduction in state #{}."
                    raise ParseError(errstr.format(str(state)))
                stack = reduc[1](stack)
                if stack[0].label != rootSymbol:
                    simplified = False
        stack.append(lookahead)
    return stack[0]
def parseVerbose(dfa, tokens):
    states, edges, reducs = dfa
    tokens += [sentinel]
    stack = [tokens.pop(0)]
    while tokens:
        lookahead = tokens.pop(0)
        print("-"*80)
        print("Stack     :",)
        for ii in stack:
            if type(ii) is Node:
                printTree(ii)
            else:
                print(ii)
        print("Lookahead :", lookahead)
        print("Tokens    :", "".join([str(ii) for ii in tokens]))
        print()
        simplified = False
        while not simplified:
            simplified = True
            state = 0
            for token in stack:
                shift = [edge for edge in edges if edge[0] == state]
                moves = [edge[1] for edge in shift]
                print("Can we shift?")
                print("Is ", token, " in", moves, "?")
                mvGeneric = [mv.label for mv in moves if mv.value == None]
                if token in moves or token.label in mvGeneric:
                    print(end="Yes!\nMove along edge: ")
                    print("{:2} - {:^3} > ".format(state, str(token)), end="")
                    shiftToken = token
                    if not shiftToken in moves:
                        shiftToken = Token(token.label, None)
                    for edge in shift:
                        if shiftToken == edge[1]:
                            state = edge[2]
                    print("{:2}".format(state))
                else:
                    errstr = "Cannot shift in state #"+str(state)+" given "
                    errstr += repr(token)+"."
                    raise ParseError(errstr)
                print()
            shift = [edge[1] for edge in edges if edge[0] == state]
            print("Should we reduce?")
            print("Can we shift given the next token?")
            print("Is", lookahead, "in", shift, "?")
            shiftTypes = [edge.label for edge in shift if edge.value == None]
            if not lookahead in shift and not lookahead.label in shiftTypes:
                print("No!")
                print("Is there a legal reduce move?")
                print("We are in state #"+str(state)+".")
                if not state in reducs:
                    print(tokens)
                    raise ParseError("Cannot reduce in state #"+str(state)+".")
                print("Possible reduce moves:")
                for ii in reducs[state]:
                    print(ii)
                reduc = None
                for rd in reducs[state]:
                    if len(rd[0]) <= len(stack):
                        match = True
                        for ii in range(-len(rd[0]), 0):
                            if rd[0][ii] != stack[ii]:
                                if rd[0][ii].value == None:
                                    if rd[0][ii].label != stack[ii].label:
                                        match = False
                        if match:
                            reduc = rd
                if not reduc:
                    errstr = "Could not resolve reduction in state #{}."
                    raise ParseError(errstr.format(str(state)))
                print("Reduce!")
                for ii in stack:
                    if type(ii) is Node:
                        printTree(ii)
                    else:
                        print(ii)
                print("reduces to")
                stack = reduc[1](stack)
                for ii in stack:
                    if type(ii) is Node:
                        printTree(ii)
                    else:
                        print(ii)
                print()
                if stack[0].label != rootSymbol:
                    simplified = False
            else:
                print("Yes! Do not reduce.")
        print("-"*80)
        print()
        stack.append(lookahead)
    return stack[0]
#############################
## Default Lexer Functions ##
#############################
def isKeyword(src, kwords, tag="kword"):
    lexeme = ""
    while src != "" and src[0].isalnum():
        lexeme += src[0]
        src = src[1:]
    if lexeme in kwords:
        return src, Token(tag, lexeme)
    return lexeme+src, None
def isOperator(src, ops):
    lexeme = ""
    opChars = set()
    for ii in ops:
        opChars.update(ii)
    goodLexeme = ""
    while src != "" and src[0] in opChars:
        lexeme += src[0]
        src = src[1:]
        if lexeme in ops:
            goodLexeme = lexeme
    if lexeme in ops:
        return src, Token("op", lexeme)
    if goodLexeme in ops:
        return lexeme[len(goodLexeme):]+src, Token("op", goodLexeme)
    return lexeme+src, None
def isInteger(src):
    lexeme = ""
    while src != "" and src[0].isnumeric():
        lexeme += src[0]
        src = src[1:]
    if lexeme != "":
        return src, Token("int", lexeme)
    return src, None
def isString(src):
    if src == "" or src != "" and src[0] != "\"":
        return src, None
    lexeme = ""
    src = src[1:]
    while src != "" and (src[0] != "\"" or src[0] == "\"" and lexeme != "" and lexeme[-1] == "\\"):
        lexeme += src[0]
        src = src[1:]
    if src == "":
        raise LexError("Odd number of double quotes.")
    return src[1:], Token("str", lexeme)
def isParen(src):
    lexeme = ""
    if src != "" and src[0] == "(":
        src = src[1:]
        return src, Token("paren", "(")
    elif src != "" and src[0] == ")":
        src = src[1:]
        return src, Token("paren", ")")
    return src, None
def isWhitespace(src):
    lexeme = ""
    while src != "" and src[0].isspace():
        lexeme += src[0]
        src = src[1:]
    if lexeme != "":
        return src, Token("space", lexeme)
    return src, None
def ignoreSpace(src):
    while src != "" and src[0].isspace():
        src = src[1:]
    return src, None
##############################
## Default Parser Functions ##
##############################
def opUnaryL(stack, op, symbol, implicit=None):
    child = None
    if implicit:
        child = Node(op, [implicit, data(stack[-1])])
    else:
        child = Node(op, data(stack[-1]))
    return stack[:-2]+[Node(symbol, child)]
def opUnaryR(stack, op, symbol, implicit=None):
    child = None
    if implicit:
        child = Node(op, [data(stack[-2]), implicit])
    else:
        child = Node(op, data(stack[-2]))
    return stack[:-2]+[Node(symbol, child)]
def opBinary(stack, op, symbol):
    child = Node(op, [data(stack[-3]), data(stack[-1])])
    return stack[:-3]+[Node(symbol, child)]
def castSym1(stack, symbol):
    return stack[:-1]+[Node(symbol, data(stack[-1]))]
def castSym2(stack, symbol):
    return stack[:-2]+[Node(symbol, [data(stack[-2]), data(stack[-1])])]
def parens(stack, symbol):
    return stack[:-3]+[Node(symbol, data(stack[-2]))]
##############
## Compiler ##
##############
class Compiler:
    def __init__(self, grammar:tuple, tkndefs:tuple):
        self.fsa = reduceFSA(genNFA(grammar))
        self.tkndefs = tkndefs
    def compile(self, src):
        tokens = lex(self.tkndefs, src)
        return parse(self.fsa, lex(self.tkndefs, src))
    def compileVerbose(self, src):
        return parseVerbose(self.fsa, lex(self.tkndefs, src))
###########
## Print ##
###########
def printGrammar(grammar):
    lhs = "{:"+str(max([len(str(rl[0])) for rl in grammar]))+"} ::="
    for rl in grammar:
        print(lhs.format(str(rl[0])), end=" ")
        exprs = ["".join([str(tok) for tok in rhs[0]]) for rhs in rl[1:]]
        print("|".join(exprs))
    print()
def printFSA(fsa):
    states, edges, reducs = fsa
    lhs = "{:"
    lengths = [max([len(str(item[0])) for item in grp]) for grp in states]
    lhs += str(max(lengths))
    lhs += "} ::="
    ## Print States
    indent = " "*(4+(len(states)-1)//10)
    count = 0
    for grp in states:
        print(("{:"+str(1+(len(states)-1)//10)+"}:  ").format(count), end="")
        print(lhs.format(str(grp[0][0])), end=" ")
        print("".join([str(token) for token in grp[0][1:][0]]))
        for item in grp[1:]:
            print(indent, end="")
            print(lhs.format(str(item[0])), end=" ")
            print("".join([str(token) for token in item[1:][0]]))
        if count in reducs:
            for rule in reducs[count]:
                print(indent+str(rule[1]), end=" ")
                print("".join([str(tkn) for tkn in rule[0]+(dotToken,)]))
        count += 1
    print()
    ## Print Edges
    for edge in edges:
        print("{:2} - {:^3} > {:2}".format(edge[0], str(edge[1]), edge[2]))
def printTree(tree, indent=0):
    if tree == sentinel:
        return
    if indent == 0:
        print(indent*4*" "+"Root: "+str(tree.label))
    else:
        print(indent*4*" "+"Branch: "+str(tree.label))
    if type(tree) == Node and type(tree.children) == Node:
        printTree(tree.children, indent+1)
    else:
        if type(tree.children) == str:
            print((indent+1)*4*" "+tree.children)
        else:
            for ii in tree.children:
                if type(ii) == Node:
                    printTree(ii, indent+1)
                else:
                    print((indent+1)*4*" "+str(ii))
def printCompiler(cplr):
    ## FSA
    printFSA(cplr.fsa)
    print()
    ## Symbols
    symbols = set()
    for edge in cplr.fsa[1]:
        symbols.update([edge[1]])
    symbols -= set([epsToken])
    symbols = tuple(sorted(list(symbols), key=lambda xx: xx.label))
    ## Table
    nCol = len(symbols)
    wCol = 7
    hBrdr, vBrdr, xBrdr = "-", "|", "+"
    hBold, vBold, xBold = "=", "#", "X"
    print(" "*5+xBold+(hBold*wCol+xBold)*nCol)
    print(end=" "*5+vBold)
    for ii in symbols:
        print(end=(" {:>"+str(wCol-2)+"} "+vBold).format(str(ii)))
    print()
    print(xBold+hBold*4+(xBold+hBold*wCol)*nCol+xBold)
    for ii in range(len(cplr.fsa[0])):
        print(end=(vBold+" {:>2} "+vBold).format(ii))
        for jj in symbols:
            move = []
            for kk in [edge for edge in cplr.fsa[1] if edge[0] == ii]:
                if kk[1] == jj:
                    move.append(str(kk[2]))
            print(end=(" {:>"+str(wCol-2)+"} "+vBrdr).format(",".join(move)))
        print()
        print(xBold+hBold*4+xBold+(hBrdr*wCol+xBrdr)*nCol)


