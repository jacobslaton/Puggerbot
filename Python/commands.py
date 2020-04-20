import asyncio
import compiler as cplr
import dice
import discord
import formatInfo
import hpages as hpgs
import money
import os
import random
import sqlite3
import time
import version

###########################
## Bot Utility Functions ##
###########################
@asyncio.coroutine
async def send(bot, dest, msg):
    await bot.send_message(dest, msg)
@asyncio.coroutine
async def embed(bot, dest, title, desc):
    msg = discord.Embed(title=title, description=desc, colour=0xE5AA70)
    await bot.send_message(dest, embed=msg)
@asyncio.coroutine
async def upload(bot, dest, msg, fname):
    with open(fname, "rb") as file:
        await bot.send_file(dest, file, content=msg)

##############################
## Command Helper Functions ##
##############################
prefix = ">"
def checkCmd(string, cmds):
    string += " "
    for ii in cmds:
        if prefix+ii+" " in string:
            return True
    return False
def parseCmd(string, cmds):
    comment = string.find("#")
    if comment == -1:
        comment = len(string)+1
    for ii in cmds:
        if prefix+ii+" " in string:
            return string[string.find("/"+ii)+len(ii)+2:comment]
    return ""
def isMaster(msg):
    return int(msg.author.id) == 151535689102655488
def isAdmin(msg):
    if isMaster(msg):
        return True
    return msg.channel.permissions_for(msg.author).administrator

#######################
## Command Functions ##
#######################
index = 0

##############
## barkbork ##
##############
@asyncio.coroutine
async def barkbork(bot, msg, db):
    response = ""
    raw = msg.content
    while 'bark' in raw or 'bork' in raw:
        bark = raw.find("bark")
        bork = raw.find("bork")
        if bark == -1:
            response += "bark "
            raw = raw[bork+4:]
        elif bork == -1:
            response += "bork "
            raw = raw[bark+4:]
        elif bark < bork:
            response += "bork "
            raw = raw[bark+4:]
        elif bork < bark:
            response += "bark "
            raw = raw[bork+4:]
    await send(bot, msg.channel, response.capitalize()[:-1]+"!")
    return 0
hpgs.cmds[index]["func"] = barkbork
index += 1
###########
## feats ##
###########
@asyncio.coroutine
async def feats(bot, msg, db):
    here = msg.channel
    command = parseCmd(msg.content, ["feats", "ft"])
    feats = db.query("feats", command)
    if len(feats) == 0:
        response = random.choice(hpgs.botMsgs["emptyQuery"])
        await embed(bot, here, "", response+" (No feats match your query.)")
    elif len(feats) == 1:
        feat = feats[0][0]+"\n"
        if feats[0][1] != "": feat += "Prerequisite: "+feats[0][1]+"\n"
        feat += "\n"+feats[0][2]+"\n\nSource: ("+feats[0][4]+")"
        await embed(bot, here, "", feat)
    else:
        formatInfo.fileFeatQuery(db, feats)
        await upload(bot, here, "Bork! :muscle:", "Queries/FeatQuery.html")
    return 0
hpgs.cmds[index]["func"] = feats
index += 1
##########
## help ##
##########
@asyncio.coroutine
async def help(bot, msg, db):
    arg = parseCmd(msg.content, hpgs.cmds[help.index]["cmd"]).replace(" ", "")
    # Assume the request is for the help command until proven otherwise
    cmd = hpgs.cmds[help.index]
    for ii in hpgs.cmds:
        if arg in ii["cmd"]:
            cmd = ii
    page =[]
    # Build page 0 first
    page.append("NAMES\n"+" "*4+", ".join(cmd["cmd"])+"\n\n")
    page[0] += "USAGE\n"+" "*4+">"+cmd["cmd"][0]
    for ii in cmd["args"]:
        page[0] += " "+ii[0]
    page[0] += "\n\n"
    if cmd["args"]:
        page[0] += "ARGUMENTS\n"
        for jj in cmd["args"]:
            page[0] += " "*4+jj[0]+" - "+jj[1]+"\n"
        page[0] += "\n"
    # Add the rest of the page from the help page description
    page.append("DESCRIPTION\n"+cmd["desc"][0]+"\n")
    for ii in cmd["desc"][1:]:
        page.append(ii)
    # Send each section of the page
    for ii in page:
        await embed(bot, msg.author, "", ii)
    return 0
help.index = index
hpgs.cmds[index]["func"] = help
index += 1
##########
## hype ##
##########
@asyncio.coroutine
async def hype(bot, msg, db):
    await bot.add_reaction(msg, "🇭")
    await bot.add_reaction(msg, "🇾")
    await bot.add_reaction(msg, "🇵")
    await bot.add_reaction(msg, "🇪")
    return 0
hpgs.cmds[index]["func"] = hype
index += 1
#########
## pet ##
#########
@asyncio.coroutine
async def pet(bot, msg, db):
    fname = "PugMedia/pet"+str(random.randrange(0, 11))+".gif"
    await upload(bot, msg.channel, "", fname)
    return 0
hpgs.cmds[index]["func"] = pet
index += 1
###########
## purge ##
###########
@asyncio.coroutine
async def purge(bot, msg, db):
    here = msg.channel
    if time.time()-purge.stamp > 60:
        purge.mentions = msg.mentions
        purge.limit = 100
        try:
            purge.limit = int(parseCmd(msg.content, ["purge"]))
        except:
            pass
    if isAdmin(msg) and purge.limit > 50 and time.time()-purge.stamp >= 60:
        purge.stamp = time.time()
        await upload(bot, here, hpgs.botMsgs["purge"], "PugMedia/purge.gif")
        return 0
    elif not isAdmin(msg):
        await send(bot, here, hpgs.botMsgs["adminOnly"], "error")
        return 0
    # Attempt purge
    def shouldPurge(msg):
        if not purge.mentions:
            return True
        return msg.author in purge.mentions
    purge.stamp = 0
    try:
        # Mass purge
        await bot.purge_from(here, limit=purge.limit, check=shouldPurge)
    except discord.errors.Forbidden:
        await send(bot, here, hpgs.botMsgs["noPerm"])
    except discord.errors.HTTPException:
        # Purge one-by-one
        async for chaff in bot.logs_from(here, limit=purge.limit):
            if shouldPurge(chaff):
                await bot.delete_message(chaff)
    await send(bot, here, "Bork! (Finished purge.)")
    return 0
purge.mentions = None
purge.limit = 100
purge.stamp = 0
hpgs.cmds[index]["func"] = purge
index += 1
###########
## races ##
###########
@asyncio.coroutine
async def races(bot, msg, db):
    here = msg.channel
    command = parseCmd(msg.content, ["races", "rc"])
    races = db.query("races", command)
    if len(races) == 0:
        response = random.choice(hpgs.botMsgs["emptyQuery"])
        await embed(bot, here, "", response+" (No races match your query.)")
    else:
        formatInfo.fileRaceQuery(db, races)
        await upload(bot, here, "Bork! :squid:", "Queries/RaceQuery.html")
    return 0
hpgs.cmds[index]["func"] = races
index += 1
#############
## rebuild ##
#############
@asyncio.coroutine
async def rebuild(bot, msg, db):
    if bot.user in msg.mentions and isMaster(msg):
        return 4
    elif not isAdmin(msg):
        await send(bot, msg.channel, helpPages.botMsgs["masterOnly"])
    return 0
hpgs.cmds[index]["func"] = rebuild
index += 1
#############
## restart ##
#############
@asyncio.coroutine
async def restart(bot, msg, db):
    if not bot.user in msg.mentions:
        return 0
    elif not isMaster(msg):
        await send(bot, msg.channel, helpPages.botMsgs["masterOnly"])
        return 0
    return 2
hpgs.cmds[index]["func"] = restart
index += 1
##########
## roll ##
##########
@asyncio.coroutine
async def roll(bot, msg, db):
    command = parseCmd(msg.content, ["roll", "r"])
    await embed(bot, msg.channel, "", "`"+dice.roll(command)+"`")
    return 0
hpgs.cmds[index]["func"] = roll
index += 1
##############
## shutdown ##
##############
@asyncio.coroutine
async def shutdown(bot, msg, db):
    if bot.user in msg.mentions and isMaster(msg):
        print(bot.user.name, "is offline.")
        await bot.logout()
    elif not isAdmin(msg):
        await send(bot, msg.channel, helpPages.botMsgs["masterOnly"])
    return 0
hpgs.cmds[index]["func"] = shutdown
index += 1
############
## spells ##
############
@asyncio.coroutine
async def spells(bot, msg, db):
    here = msg.channel
    command = parseCmd(msg.content, ["spells", "sp"])
    spells = db.query("spells", command)
    if len(spells) == 0:
        response = random.choice(hpgs.botMsgs["emptyQuery"])
        await embed(bot, here, "", response+" (No spells match your query.)")
    elif len(spells) == 1 and spells[0][3] == 0:
        await embed(bot, here, "", formatInfo.spellCard(db, spells[0]))
    else:
        formatInfo.fileSpellQuery(db, spells)
        await upload(bot, here, "Bork! :sparkles:", "Queries/SpellQuery.html")
    return 0
hpgs.cmds[index]["func"] = spells
index += 1
###########
## split ##
###########
@asyncio.coroutine
async def split(bot, msg, db):
    command = parseCmd(msg.content, ["split", "s"]).split(",")
    response = ""
    try:
        response = money.split(money.parse(command[0]), int(command[1]))
        await embed(bot, msg.channel, "", response)
    except ValueError as err:
        response = random.choice(hpgs.botMsgs["emptyQuery"])
        response += " (The number of party members must be a positive integer.)"
        await embed(bot, msg.channel, "", response)
    return 0
hpgs.cmds[index]["func"] = split
index += 1
##############
## tutorial ##
##############
@asyncio.coroutine
async def tutorial(bot, msg, db):
    cmd = parseCmd(msg.content, ["tutorial", "tut"]).split()
    if len(cmd) == 0:
        errmrg = random.choice(hpgs.botMsgs["emptyQuery"])
        errmsg += " (I don't know what command you need help with!)"
        await embed(bot, msg.channel, "", errmsg)
    elif len(cmd) == 1:
        cmd.append("0")
    filename = "Tutorials/tutorial_"+cmd[0]+"-"+cmd[1]+".txt"
    if not os.path.isfile(filename):
        errmsg = "The requested tutorial page does not exist."
        await embed(bot, msg.channel, "", errmsg)
    page = ""
    with open(filename, "r") as fin:
        for ii in fin:
            page += ii
    await embed(bot, msg.author, page[:page.find("\n")], page[page.find("\n"):])
    return 0
hpgs.cmds[index]["func"] = tutorial
index += 1
############
## update ##
############
@asyncio.coroutine
async def update(bot, msg, db):
    if bot.user in msg.mentions and isMaster(msg):
        return 3
    elif not isAdmin(msg):
        await send(bot, msg.channel, helpPages.botMsgs["masterOnly"])
    return 0
hpgs.cmds[index]["func"] = update
index += 1
#############
## version ##
#############
@asyncio.coroutine
async def getVersion(bot, msg, db):
    await embed(bot, msg.channel, "", version.version)
    return 0
hpgs.cmds[index]["func"] = getVersion
index += 1
###########
## worth ##
###########
@asyncio.coroutine
async def worth(bot, msg, db):
    command = parseCmd(msg.content, ["worth", "w"])
    await embed(bot, msg.channel, "", money.worth(money.parse(command)))
    return 0
hpgs.cmds[index]["func"] = worth
index += 1
