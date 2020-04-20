import asyncio
import commands as cmds
import datetime
import discord
import DnD_DB
import hpages as hpgs
import sys
import time
import traceback

lines = []
with open("Login/"+"-".join(["login"]+sys.argv[1:])+".txt", "r") as file:
    for ii in file:
        lines.append(ii.replace("\n", ""))
token, masterID = lines[0], int(lines[1])
puggerbot = discord.Client()
dnddb = DnD_DB.DnD_DB()

@asyncio.coroutine
async def report(bot, title, desc):
    await cmds.embed(bot, report.master, "Report: "+title, desc)
report.master = None

@puggerbot.event
async def on_ready():
    print(puggerbot.user.name, "is online.")
    for server in puggerbot.servers:
        for member in server.members:
            if int(member.id) == 151535689102655488:
                print("Found master!")
                report.master = member
                return

@puggerbot.event
async def on_message(msg):
    if msg.author == puggerbot.user:
        return
    for ii in hpgs.cmds:
        if cmds.checkCmd(msg.content, ii["cmd"]) and ii["func"] != None:
            try:
                on_message.exitCode = await ii["func"](puggerbot, msg, dnddb)
            except Exception as err:
                tb = traceback.format_exc()
                errmsg = hpgs.botMsgs["report"]
                errmsg = errmsg.format(msg.author, msg.content, tb)
                await report(puggerbot, str(type(err)), errmsg)
        elif cmds.checkCmd(msg.content, ii["cmd"]):
            await cmds.embed(puggerbot, msg.channel, "", "Command is missing.")
            errmsg = hpgs.botMsgs["report"].format(msg.author, msg.content, "")
            await report(puggerbot, master, "Command is missing.", errmsg)
    if on_message.exitCode != 0:
        print(puggerbot.user.name, "is offline.")
        await puggerbot.logout()
on_message.exitCode = 0

@asyncio.coroutine
async def restart():
    puggerbot.wait_until_ready()
    midnight = datetime.datetime.now()+datetime.timedelta(days=1)
    midnight = midnight.replace(hour=0, minute=0, second=0, microsecond=0)
    midnight = time.mktime(midnight.timetuple())
    await asyncio.sleep(midnight-time.time())
    print("Puggerbot is restarting...")
    on_message.exitCode = 2
    await puggerbot.logout()

future = asyncio.ensure_future(restart())
try:
    puggerbot.run(token)
except discord.errors.LoginFailure as err:
    print("LoginFailure:", str(err))
dnddb.close()
if future.done():
    if future.exception():
        print(traceback.format_exc())
        on_message.exitCode = 1
else:
    future.set_result(0)
sys.exit(on_message.exitCode)
