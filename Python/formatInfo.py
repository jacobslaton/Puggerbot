import version

def hdlPlural(value, singular, plural=""):
    if plural == "": plural += singular+"s"
    string = str(value)+" "
    if value == 1: string += singular
    else: string += plural
    return string
def spellEntry(dnddb, spell):
    tags = spell[10]
    school = dnddb.getSchoolString(spell[2])
    entry = "(\n\nname \""+spell[0]+"\"\nlevel "+str(spell[1])
    entry += " school \""+school+"\""
    if "#ritual" in tags:
        tags = tags.replace("#ritual", "")
        entry += "  tags \"ritual\""
    ## Casting Time
    entry += "\n\ncast        "
    if "#action" in tags:
        tags = tags.replace("#action", "")
        if spell[4] <= 1: entry += "1 action"
        else: entry += str(spell[4])+" action"
    elif "#bonus" in tags:
        tags = tags.replace("#bonus", "")
        if spell[4] <= 1: entry += "1 bonus"
        else: entry += str(spell[4])+" bonuses"
    elif "#reaction" in tags:
        tags = tags.replace("#reaction", "")
        if spell[4] <= 1: entry += "1 reaction"
        else: entry += str(spell[4])+" reactions"
    elif spell[4]%1440 == 0:
        entry += str(spell[4]//1440)+" day"
        if spell[4] > 1440: entry += "s"
    elif spell[4]%60 == 0:
        entry += str(spell[4]//60)+" hour"
        if spell[4] > 60: entry += "s"
    else:
        entry += str(spell[4])+" minute"
        if spell[4] > 1: entry += "s"
    ## Range
    entry += "\nrange       "
    if "#self" in tags:
        tags = tags.replace("#self", "")
        entry += "self"
    elif "#sight" in tags:
        tags = tags.replace("#sight", "")
        entry += "sight"
    elif "#range_special" in tags:
        tags = tags.replace("#range_special", "")
        entry += "special"
    elif "#touch" in tags:
        tags = tags.replace("#touch", "")
        entry += "touch"
    elif spell[5]%5280 == 0:
        entry += str(spell[5]//5280)+" mile"
        if spell[6] > 5280: entry += "s"
    else:
        entry += str(spell[5])
        if spell[5] > 1: entry += " feet"
        else: entry += " foot"
    ## Duration
    entry += "\nduration    "
    if "#rounds" in tags:
        tags = tags.replace("#rounds", "")
        if spell[4] <= 1: entry += "1 round"
        else: entry += str(spell[4])+" rounds"
    elif "#indefinite" in tags:
        tags = tags.replace("#indefinite", "")
        entry += "indefinite"
    elif "#instantaneous" in tags:
        tags = tags.replace("#instantaneous", "")
        entry += "instantaneous"
    elif "#dur_special" in tags:
        tags = tags.replace("#dur_special", "")
        entry += "special"
    elif spell[6]%1440 == 0:
        entry += str(spell[6]//1440)+" day"
        if spell[6] > 1440: entry += "s"
    elif spell[6]%60 == 0:
        entry += str(spell[6]//60)+" hour"
        if spell[6] > 60: entry += "s"
    else:
        entry += str(spell[6])+" minute"
        if spell[6] > 1: entry += "s"
    if "#concentration" in tags:
        tags = tags.replace("#concentration", "")
        entry += "  tags \"concentration\""
    entry += "\n"
    ## Components
    if spell[7] == 1: entry += "verbal "
    if spell[8] == 1: entry += "somatic "
    if spell[9] != "": entry += "materials \""+spell[9]+"\""
    entry += "\n\ndesc \"\n"+spell[13].replace("\"", "\\\"")+"\n\"\n\n"
    entry += "class         \""+", ".join(spell[12][1:].split("#"))+"\"\n"
    if tags != "":
        entry += "tags          \""+", ".join(tags[1:].split("#"))+"\"\n"
    entry += "src           \""+spell[11]+"\"\n"
    if spell[3] == 1: entry += "html\n"
    return entry+"\n)"
def spellCard(dnddb, spell):
    lineEnd = "\n"
    if spell[3]: lineEnd = "<br>"+lineEnd
    string = spell[0]+lineEnd
    school = dnddb.getSchoolString(spell[2])
    if spell[1] == 0: string += school.capitalize()+" cantrip"
    else: string += str(spell[1])+dnddb.getSfx(spell[1]-1)+"-level "+school
    if "#ritual" in spell[10]: string += " (ritual)"
    string += lineEnd+"Casting Time: "
    if "#action" in spell[10]: string += "1 action"
    elif "#bonus" in spell[10]: string += "1 bonus action"
    elif "#reaction" in spell[10]: string += "1 reaction"
    elif spell[4]%60 == 0: string += hdlPlural(spell[4]//60, "hour")
    elif spell[4] == 0: string += "ERROR"
    else: string += hdlPlural(spell[4], "minute")
    string += lineEnd+"Range: "
    if "#touch" in spell[10]: string += "Touch"
    elif "#sight" in spell[10]: string += "Sight"
    elif "#self" in spell[10]:
        string += "Self"
        if spell[5] != 0:
            string += " ("
            shape = ""
            if "#radius" in spell[10]: shape += " radius"
            elif "#cone" in spell[10]: shape += " cone"
            elif "#cube" in spell[10]: shape += " cube"
            elif "#cylinder" in spell[10]: shape += " cylinder"
            elif "#hemisphere" in spell[10]: shape += " hemisphere"
            elif "#line" in spell[10]: shape += " line"
            elif "#sphere" in spell[10]: shape += " sphere"
            if spell[5]%5280 == 0:
                if shape != "": string += str(spell[5]//5280)+" mile"
                else: string += hdlPlural(spell[5]//5280, "mile")
            else:
                if shape != "": string += str(spell[5])+" foot"
                else: string += hdlPlural(spell[5], "foot", "feet")
            string += shape+")"
    elif "#range_special" in spell[10]: string += "Special"
    elif spell[5] == 0: string += "Unlimited"
    else:
        if spell[5]%5280 == 0: string += hdlPlural(spell[5]//5280, "mile")
        else: string += hdlPlural(spell[5], "foot", "feet")
    string += lineEnd+"Components: "
    components = []
    if (spell[7] == 1): components.append("V")
    if (spell[8] == 1): components.append("S")
    if (spell[9] != ""): components.append("M ("+spell[9]+")")
    for comp in components[:-1]: string += comp+", "
    if components: string += components[-1]
    else: string += "ERROR"
    string += lineEnd+"Duration: "
    if "#concentration" in spell[10]: string += "Concentration, up to "
    if spell[6] == 0:
        if "#indefinite" in spell[10]: string += "Until dispelled"
        elif "#dur_special" in spell[10]: string += "Special"
        else: string += "Instantaneous"
    elif spell[6]%1440 == 0: string += hdlPlural(spell[6]//1440, "day")
    elif spell[6]%60 == 0: string += hdlPlural(spell[6]//60, "hour")
    elif "#rounds" in spell[10]: string += hdlPlural(spell[6], "round")
    else: string += hdlPlural(spell[6], "minute")
    string += lineEnd+lineEnd+spell[13]+lineEnd+lineEnd+"Source ("+spell[11]+")"
    return string
def spellMinimal(dnddb, spell):
    string = spell[0]+" "*(37-len(spell[0]))
    string += str(spell[1])+dnddb.getSfx(spell[1]-1)+" "
    string += dnddb.getSchoolString(spell[2])[:3]
    if "#ritual" in spell[10]: string += " (R)   "
    else: string += " "*7
    temp = ""
    if spell[7]: temp += "V"
    if spell[8]: temp += "S"
    if spell[9]: temp += "M"
    string += temp+" "*(6-len(temp))
    if "#action" in spell[10]: string += " 1 act   "
    elif "#bonus" in spell[10]: string += " 1 bon   "
    elif "#reaction" in spell[10]: string += " 1 rea   "
    elif spell[4]%60 == 0: string += "%2u hrs   "%(spell[4]//60)
    else: string += "%2u min   "%spell[4]
    if "#touch" in spell[10]: string += " touch   "
    elif "#sight" in spell[10]: string += " sight   "
    elif "#self" in spell[10]: string += "  self   "
    elif "#range_special" in spell[10]: string += "  spc    "
    elif spell[4] == 0: string += " unlim   "
    elif spell[4]%5280 == 0: string += "%3u mi   "%(spell[5]//5280)
    else: string += "%3u ft   "%spell[5]
    if "#indefinite" in spell[10]: string += "   inf"
    elif "#dur_special" in spell[10]: string += "   spc"
    elif spell[6] == 0: string += "  inst"
    elif spell[6]%1440 == 0: string += "%2u dys"%(spell[6]//1440)
    elif spell[6]%60 == 0: string += "%2u hrs"%(spell[6]//60)
    elif "#rounds" in spell[10]: string += "%2u rnd"%spell[6]
    else: string += "%2u min"%spell[6]
    if "#concentration" in spell[10]: string += " (C)   "
    else: string += " "*7
    string += spell[11]
    return string
def fileSpellQuery(dnddb, spells):
    srcs = []
    for ii in spells:
        for jj in ii[11].split(", "):
            if not jj[:jj.rfind(" ")] in [kk[0] for kk in srcs]:
                src = dnddb.query("sources", jj[:jj.rfind(" ")])
                if src != []:
                    srcs.append(src[0])
    file = open("Queries/SpellQuery.html", "w")
    file.write("""<!DOCTYPE html>
<html lang="en">

<head>
<title>D&amp;D Spell Query</title>
<meta charset="utf-8"/>
<meta name="robots" content="noindex,nofollow"/>
<style>
body
{
    color: lime;
    background-color: black;
}
h1, h2
{
    color: lime;
    background-color: #2e2e2e;
    font-family: Papyrus, serif;
    text-align: center;
    border: thin solid lime;
}
a
{
    color: lime;
}
#wrapper
{
    background-color: #5c5c5c;
    font-family: Lucida Console;
    width: 85%;
    margin: auto;
}
#index
{
    background-color: #5c5c5c;
    font-family: Lucida Console;
    margin: auto;
}
#key
{
    width: 50%;
    margin: auto;
}
.spell
{
    width: 75%;
    margin: auto;
    text-align: left;
}
#footer
{
    background-color: #2e2e2e;
    font-size: small;
    font-style: italic;
    border-top: thin solid lime;
}
@media print
{
    body
    {
        background-color: #FFFFFF;
        color: #000000
    }
    h1, h2
    {
        color: #000000;
        background-color: #000000;
        font-family: Papyrus, serif;
        text-align: center;
        border: thin solid #000000;
    }
    a
    {
        display: none;
    }
    .name
    {
        display: inline;
        color: #000000;
    }
    #wrapper
    {
        background-color: #000000;
        font-family: Lucida Console;
        width: 100%;
        margin: 0;
    }
    #index
    {
        background-color: #000000;
        font-family: Lucida Console;
        margin: 0;
    }
    #key
    {
        width: 50%;
        margin: auto;
    }
    .spell
    {
        width: 100%;
        margin: 0;
        text-align: left;
    }
    #footer
    {
        background-color: #000000;
        font-size: small;
        font-style: italic;
        border-top: thin solid #000000;
    }
}
</style>
</head>

<body>
<div id="wrapper">
<h1>D&amp;D Spell Query</h1>

<div>
<table id="index" align="center" border="5">
<tr>
    <th style="width:20%" id="name"  >Name</th>
    <th style="width: 5%" id="level" >Level</th>
    <th style="width: 5%" id="school">School</th>
    <th style="width: 5%" id="comp"  >Comp</th>
    <th style="width:10%" id="cast"  >Cast</th>
    <th style="width:10%" id="range" >Range</th>
    <th style="width:10%" id="dur"   >Dur</th>
    <th style="width: 5%" id="tags"  >Tags</th>
    <th style="width:20%" id="source">Source</th>
</tr>
""")
    for ii in spells:
        file.write("<tr>\n")
        file.write(" "*4+"<th headers=\"name\" align=\"left\">\n"+" "*8+"<a class=\"name\" href=\"#"+ii[0]+"\">"+ii[0]+"</a>\n"+" "*4+"</th>\n")
        file.write(" "*4+"<th headers=\"level\" >"+str(ii[1])+dnddb.getSfx(ii[1]-1)+"</th>\n")
        file.write(" "*4+"<th headers=\"school\">"+str(dnddb.getSchoolString(ii[2])[:3])+"</th>\n")
        file.write(" "*4+"<th headers=\"comp\"  >")
        if ii[7]: file.write("V")
        if ii[8]: file.write("S")
        if ii[9]: file.write("M")
        file.write("</th>\n"+" "*4+"<th headers=\"cast\"  >")
        if "#action" in ii[10]: file.write("1 act")
        elif "#bonus" in ii[10]: file.write("1 bon")
        elif "#reaction" in ii[10]: file.write("1 rea")
        elif ii[4]%60 == 0: file.write(str(ii[4]//60)+" hrs")
        else: file.write(str(ii[4])+" min")
        file.write("</th>\n"+" "*4+"<th headers=\"range\" >")
        if "#touch" in ii[10]: file.write("touch")
        elif "#sight" in ii[10]: file.write("sight")
        elif "#self" in ii[10]: file.write("self")
        elif "#range_special" in ii[10]: file.write("spc")
        elif ii[5] == 0: file.write("unlim")
        elif ii[5]%5280 == 0: file.write("%3u mi"%(ii[5]//5280))
        else: file.write("%3u ft"%ii[5])
        file.write("</th>\n"+" "*4+"<th headers=\"dur\"   >")
        if "#indefinite" in ii[10]: file.write("inf")
        elif "#dur_special" in ii[10]: file.write("spc")
        elif ii[6] == 0: file.write("inst")
        elif ii[6]%1440 == 0: file.write(str(ii[6]//1440)+" dys")
        elif ii[6]%60 == 0: file.write(str(ii[6]//60)+" hrs")
        elif "#rounds" in ii[10]: file.write(str(ii[6])+" rnd")
        else: file.write(str(ii[6])+" min")
        file.write("</th>\n"+" "*4+"<th headers=\"tags\"  >")
        if "#ritual" in ii[10]: file.write("R")
        if "#concentration" in ii[10]: file.write("C")
        file.write("</th>\n")
        file.write(" "*4+"<th headers=\"source\">"+ii[11]+"</th>\n")
        file.write("</tr>\n")
    file.write("</table>\n</div>\n")
    file.write("""
<br>
<div>
<table id="key" align="center" border="5">
<caption>Key</caption>
<tr>
    <th style="width:20%" id="abbr" >Shorthand</th>
    <th style="width:80%" id="src"  >Reference</th>
</tr>""")
    for ii in srcs:
        file.write("<tr>\n")
        file.write(" "*4+"<th headers=\"abbr\" align=\"left\">"+ii[0]+"</th>\n")
        file.write(" "*4+"<th headers=\"src\"  align=\"left\">"+ii[1]+"</th>\n")
        file.write("</tr>\n")
    file.write("</table>\n</div>\n")
    for ii in spells:
        file.write("<br>\n<div class=\"spell\" id=\""+ii[0]+"\">\n")
        if ii[3]: file.write(spellCard(dnddb, ii))
        else: file.write(spellCard(dnddb, ii).replace("\n", "<br>\n"))
        file.write("<br>\n<a href=\"#index\">Back to Top</a><br>\n<br>\n</div>\n")
    file.write("""<br><br>
<div id="footer">
    Spell Output from {}<br>
    Written by Jacob Slaton.
</div>
</div>
</body>

</html>


""".format(version.version))
    file.close()
def fileFeatQuery(dnddb, feats):
    srcs = []
    for ii in feats:
        for jj in ii[4].split(", "):
            if not jj[:jj.rfind(" ")] in [kk[0] for kk in srcs]:
                src = dnddb.query("sources", jj[:jj.rfind(" ")])
                if src != []:
                    srcs.append(src[0])
    file = open("Queries/FeatQuery.html", "w")
    file.write("""<!DOCTYPE html>
<html lang="en">

<head>
<title>D&amp;D Feat Query</title>
<meta charset="utf-8"/>
<meta name="robots" content="noindex,nofollow"/>
<style>
body
{
    color: lime;
    background-color: black;
}
h1, h2
{
    color: lime;
    background-color: #2e2e2e;
    font-family: Papyrus, serif;
    text-align: center;
    border: thin solid lime;
}
a
{
    color: lime;
}
#wrapper
{
    background-color: #5c5c5c;
    font-family: Lucida Console;
    width: 85%;
    margin: auto;
}
#index
{
    background-color: #5c5c5c;
    font-family: Lucida Console;
    margin: auto;
}
#footer
{
    background-color: #2e2e2e;
    font-size: small;
    font-style: italic;
    border-top: thin solid lime;
}
</style>
</head>

<body>
<div id="wrapper">
<h1>D&amp;D Feat Query</h1>

<div id="index">
<table align="center" border="5" style="margin: 0 auto; width: 75%;">
<tr>
    <th style="width:20%" id="name"  >Name</th>
    <th style="width:25%" id="req"   >Prerequisite</th>
    <th style="width:20%" id="source">Source</th>
</tr>
""")
    for ii in feats:
        file.write("<tr>\n")
        file.write(" "*4+"<th headers=\"name\" align=\"left\">\n")
        file.write(" "*8+"<a href=\"#"+ii[0]+"\">"+ii[0]+"</a>\n"+" "*4+"</th>\n")
        file.write(" "*4+"<th headers=\"req\"   >")
        if ii[1] != "": file.write(ii[1])
        file.write("</th>\n")
        file.write(" "*4+"<th headers=\"source\">"+ii[4]+"</th>\n")
        file.write("<tr>\n")
    file.write("</table>\n</div>\n")
    file.write("""
<br>
<div id="key" style=\"width: 50%; margin: 0 auto\">
<table align="center" border="5" style="margin: 0 auto; width: 85%;">
<caption>Key</caption>
<tr>
    <th style="width:20%" id="abbr" >Shorthand</th>
    <th style="width:80%" id="src"  >Reference</th>
</tr>""")
    for ii in srcs:
        file.write("<tr>\n")
        file.write(" "*4+"<th headers=\"abbr\" align=\"left\">"+ii[0]+"</th>\n")
        file.write(" "*4+"<th headers=\"src\"  align=\"left\">"+ii[1]+"</th>\n")
        file.write("</tr>\n")
    file.write("</table>\n</div>\n")
    for ii in feats:
        file.write("<br>\n<div id=\""+ii[0]+"\" style=\"width: 75%; margin: 0 auto; text-align: left\">\n<h3>"+ii[0]+"</h3>\n")
        if ii[1] != "": file.write("Prerequisite: "+ii[1]+"<br>\n")
        file.write("<br>\n"+ii[2].replace("\n", "<br>\n")+"<br>\n<br>\nSource: ("+ii[4]+")<br>\n<a href=\"#index\">Back to Top</a><br>\n<br>\n</div>\n")
    file.write("""<br><br>
<div id="footer">
    Feat Output from {}<br>
    Written by Jacob Slaton.
</div>
</div>
</body>

</html>


""".format(version.version))
    file.close()
def fileRaceQuery(dnddb, races):
    srcs = []
    for ii in races:
        for jj in ii[14].split(", "):
            if not jj[:jj.rfind(" ")] in [kk[0] for kk in srcs]:
                src = dnddb.query("sources", jj[:jj.rfind(" ")])
                if src != []:
                    srcs.append(src[0])
    file = open("Queries/RaceQuery.html", "w")
    file.write("""<!DOCTYPE html>
<html lang="en">

<head>
<title>D&amp;D Race Query</title>
<meta charset="utf-8"/>
<meta name="robots" content="noindex,nofollow"/>
<style>
body
{
    color: lime;
    background-color: black;
}
h1, h2
{
    color: lime;
    background-color: #2e2e2e;
    font-family: Papyrus, serif;
    text-align: center;
    border: thin solid lime;
}
a
{
    color: lime;
}
#wrapper
{
    background-color: #5c5c5c;
    font-family: Lucida Console;
    width: 85%;
    margin: auto;
}
#index
{
    background-color: #5c5c5c;
    font-family: Lucida Console;
    margin: auto;
}
#footer
{
    background-color: #2e2e2e;
    font-size: small;
    font-style: italic;
    border-top: thin solid lime;
}
</style>
</head>

<body>
<div id="wrapper">
<h1>D&amp;D Race Query</h1>

<div id="index">
<table align="center" border="5" style="margin: 0 auto; width: 75%;">
<tr>
    <th style="width:10%" id="race"   >Race</th>
    <th style="width:10%" id="subrace">Subrace</th>
    <th style="width: 5%" id="size"   >Size</th>
    <th style="width: 1%" id="str"    >STR</th>
    <th style="width: 1%" id="dex"    >DEX</th>
    <th style="width: 1%" id="con"    >CON</th>
    <th style="width: 1%" id="int"    >INT</th>
    <th style="width: 1%" id="wis"    >WIS</th>
    <th style="width: 1%" id="cha"    >CHA</th>
    <th style="width: 9%" id="source" >Source</th>
</tr>
""")
    races = [list(xx) for xx in races]
    for ii in races:
        file.write("<tr>\n")
        file.write(" "*4+"<th headers=\"race\" align=\"left\">\n")
        file.write(" "*8+"<a href=\"#")
        if ii[1] == None: ii[1] = ""
        else: ii[1] += " "
        file.write(ii[1]+ii[0]+"\">"+ii[0]+"</a>\n"+" "*4+"</th>\n")
        file.write(" "*4+"<th headers=\"subrace\"   >"+ii[1][:-1]+"</th>\n")
        ii[6] = dnddb.getSizeString(ii[6])
        file.write("<th headers=\"size\">"+ii[6]+"</th>\n")
        rawstats = []
        if ii[2] != None: rawstats += ii[2].split(";")
        if ii[3] != None: rawstats += ii[3].split(";")
        rawstats = [xx for xx in rawstats if xx != ""]
        ii[2] = ", ".join([xx for xx in rawstats if xx != ""])
        stats = {"STR":"0", "DEX":"0", "CON":"0", "INT":"0", "WIS":"0", "CHA":"0"}
        for jj in rawstats:
            if jj[:3] == "STR": stats["STR"] = jj[3:]
            elif jj[:3] == "DEX": stats["DEX"] = jj[3:]
            elif jj[:3] == "CON": stats["CON"] = jj[3:]
            elif jj[:3] == "INT": stats["INT"] = jj[3:]
            elif jj[:3] == "WIS": stats["WIS"] = jj[3:]
            elif jj[:3] == "CHA": stats["CHA"] = jj[3:]
            elif jj[:3] == "ALL":
                for kk in stats:
                    stats[kk] = int(stats[kk])+1
                    if stats[kk] > 0:
                        stats[kk] = "+"+str(stats[kk])
                    elif stats[kk] < 0:
                        stats[kk] = "-"+str(stats[kk])
        file.write("<th headers=\"str\">"+stats["STR"]+"</th>\n")
        file.write("<th headers=\"dex\">"+stats["DEX"]+"</th>\n")
        file.write("<th headers=\"con\">"+stats["CON"]+"</th>\n")
        file.write("<th headers=\"int\">"+stats["INT"]+"</th>\n")
        file.write("<th headers=\"wis\">"+stats["WIS"]+"</th>\n")
        file.write("<th headers=\"cha\">"+stats["CHA"]+"</th>\n")
        lang = []
        if ii[10] != None: lang += ii[10].split(";")
        if ii[11] != None: lang += ii[11].split(";")
        ii[10] = ", ".join([xx for xx in lang if xx != ""])
        ii[14] = ii[14] if ii[15] == None else ii[15]
        file.write(" "*4+"<th headers=\"source\">"+ii[14]+"</th>\n")
        file.write("<tr>\n")
    file.write("</table>\n</div>\n")
    file.write("""
<br>
<div id="key" style=\"width: 50%; margin: 0 auto\">
<table align="center" border="5" style="margin: 0 auto; width: 85%;">
<caption>Key</caption>
<tr>
    <th style="width:20%" id="abbr" >Shorthand</th>
    <th style="width:80%" id="src"  >Reference</th>
</tr>""")
    for ii in srcs:
        file.write("<tr>\n")
        file.write(" "*4+"<th headers=\"abbr\" align=\"left\">"+ii[0]+"</th>\n")
        file.write(" "*4+"<th headers=\"src\"  align=\"left\">"+ii[1]+"</th>\n")
        file.write("</tr>\n")
    file.write("</table>\n</div>\n")
    for ii in races:
        file.write("""<br>
<div style="text-align:center" width="75%" id="{0[1]}{0[0]}">
<table border="5" width="75%" align="center">
    <caption><h2>{0[1]}{0[0]}</h2></caption>
    <tr>
        <th width="20%">Stats</th>
        <td width="30%" align="center">{0[2]}</td>
        <th width="20%">Age</th>
        <td width="30%" align="center">{0[4]}-{0[5]}</td>
    </tr>
    <tr>
        <th>Size</th>
        <td align="center">{0[6]}</td>
        <th>Speed</th>
        <td align="center">{0[7]}</td>
    </tr>
    <tr>
        <th>Height</th>
        <td align="center">{0[8]}</td>
        <th>Weight</th>
        <td align="center">{0[9]}</td>
    </tr>
    <tr>
        <th>Languages</th>
        <td align="center">{0[10]}</td>
        <th>Source</th>
        <td align="center">{0[14]}</td>
    </tr>
</table>
<div style="width: 75%; margin: 0 auto; text-align: left">
<a href="#index">Back to Top</a><br>
""".format(ii))
        feats = []
        if ii[12] != None: feats += ii[12].split(";")
        if ii[13] != None: feats += ii[13].split(";")
        feats = " or ".join(["name is \""+xx+"\"" for xx in feats if xx != ""])
        if feats != "": feats = dnddb.query("feats", feats)
        else: feats = []
        for jj in feats:
            file.write("<br>\n<div id=\""+jj[0]+"\">\n<h3>"+jj[0]+"</h3>\n")
            if jj[1] != "": file.write("Prerequisite: "+jj[1]+"<br>\n")
            file.write("<br>\n"+jj[2].replace("\n", "<br>\n")+"<br>\n<br>\nSource: ("+jj[4]+")<br>\n<a href=\"#index\">Back to Top</a><br>\n<br>\n</div>\n")
        file.write("""<br>
</div>
</div>
""".format(ii))
    file.write("""<br><br>
<div id="footer">
    Race Output from {}<br>
    Written by Jacob Slaton.
</div>
</div>
</body>

</html>


""".format(version.version))
    file.close()


