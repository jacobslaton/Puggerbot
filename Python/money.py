import re

def parse(string):
    string = re.sub(r"([0-9]) ([a-z])", r"\1\2", re.sub(r" +", r" ", string))
    args = string.lower().split(" ")
    money = {"pp":0, "gp":0, "ep":0, "sp":0, "cp":0}
    for ii in args:
        if re.fullmatch("[0-9]+(p|(pp)|(platinum))", ii):
            money["pp"] += int(ii[:ii.find("p")])
        elif re.fullmatch("[0-9]+(g|(gp)|(gold))", ii):
            money["gp"] += int(ii[:ii.find("g")])
        elif re.fullmatch("[0-9]+(e|(ep)|(electrum))", ii):
            money["ep"] += int(ii[:ii.find("e")])
        elif re.fullmatch("[0-9]+(s|(sp)|(silver))", ii):
            money["sp"] += int(ii[:ii.find("s")])
        elif re.fullmatch("[0-9]+(c|(cp)|(copper))", ii):
            money["cp"] += int(ii[:ii.find("c")])
    return money;
def split(money, num):
    if num <= 0: return "Attempted to split amongst 0 or fewer parties."
    share = {"pp":0, "gp":0, "ep":0, "sp":0, "cp":0}
    remainder = {"pp":0, "gp":0, "ep":0, "sp":0, "cp":0}
    for ii in share: share[ii] = money[ii]//num
    for ii in remainder: remainder[ii] = money[ii]%num
    string = "Share:"
    for ii in share:
        if share[ii] > 0:
            string += " "+str(share[ii])+ii[0]
    string += "\nChange:"
    noRmdr = True
    for ii in remainder:
        if remainder[ii] > 0:
            noRmdr = False
            string += " "+str(remainder[ii])+ii[0]
    if noRmdr: string += "None"
    return string
def worth(money):
    least = {"pp":0, "gp":0, "ep":0, "sp":0, "cp":0}
    conv = {"pp":1000, "gp":100, "ep":50, "sp":10, "cp":1}
    cp = 0
    for ii in money:
        cp += conv[ii]*money[ii]
    for ii in least:
        least[ii] = cp//conv[ii]
        cp -= least[ii]*conv[ii]
    string = "Total Worth: "
    for ii in least:
        if least[ii] > 0:
            noRmdr = False
            string += str(least[ii])+ii[0]+" "
    return string


