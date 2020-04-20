botMsgs = {"adminOnly":"Grrr, bark! (You're not my supervisor! Only admins can use that command.)",
           "masterOnly":"Grrr, bark! (You're not my supervisor! Only DrPuggo can use that command.)",
           "purge":":warning: An admin has requested to purge more than 50 messages. To confirm, purge again. :warning:",
           "noPerm":"Bork? (I do not have the proper permissions to use that command.)",
           "report":"An issue was encountered when {} executed:\n```{}```\n\n{}",
           "emptyQuery":["*Rolls a natural 1.*",
                         "All out of szechuan sauce.",
                         "Geeettttttt dunked on!!!",
                         "Just Monika.",
                         "I'm sorry Dave, I'm afraid I can't do that.",
                         "Your query has been counterspelled!",
                         "Your query has been exiled!",
                         "Your query has been sent to the Shadow Realm!",
                         "Your query has entered the *danger zone*."]}
cmds = [{"cmd":["bark", "bork"],
         "func":None,
         "args":[],
         "desc":["""
    Bork bark!"""[1:]]},
        {"cmd":["feats", "ft"],
         "func":None,
         "args":[["<query>", "a boolean expression detailing the attributes of a set of feats, see description"]],
         "desc":["""
    Search through Puggerbot's database of feats to get a set of feats that are specified by the query. This command works more like a search language than a search engine. Each feat in the database is sectioned into fields such as 'name' and 'source'. Restrictions can be placed on a field by using an operator. A restriction and operator can be applied to a field to form an expression. Expressions can be structured in one of two ways: "field operator restriction" or "restriction operator field". The way that the restriction and operator are applied to the field depends on the operator. Below is a list of each field and operator with a brief description and a few examples. All operators are case insensitive ("Fireball" is treated the same as "fireball"). Restrictions must be surrounded by double quotes.
"""[1:], """
Operators:
=, is
    - Format: field = restriction
    - checks if the entire field matches the restriction
    - Ex: name = "Mobile"
    - Ex: name is "Mobile"
!=
    - Format: field != restriction
    - checks if the entire field does not match the restriction
    - Ex: name != "Mobile"
in
    - Format: restriction in field
    - functionally the same as "contains"
    - checks if the restriction is in the field
    - Ex: "Master" in name
contains
    - Format: field contains restriction
    - functionally the same as "in"
    - checks if the field contains the restriction
    - Ex: name contains "Master"
and
    - Format: expression and expression
    - can be used to combine the effects of two or more expressions
    - checks if a feat matches all expressions
    - Ex: desc contains "increase" and prereq = ""
or
    - Format: expression or expression
    - can be used to combine the effects of two or more expressions
    - checks if a feat matches at least one of the expressions
    - Ex: desc contains "Strength" or desc contains "Constitution"
not, !
    - Format: not expression
    - negates the effect of an expression
    - this operator must go on the outside of an expression
    - Ex: not prereq is ""
    - Ex: ! prereq = ""
"""[1:], """
Note on complex queries:
    The operators "and" and "or" can be used together to create more complex and specific queries.
Ex: desc contains "increase" and (desc contains "Strength" or desc contains "Constitution")

Fields:
name
    - the name of the feat
    - Ex: name is "Mobile"
    - Ex: "Master" in name
prereq
    - the prerequisite a character needs to meet in order to take the feat
    - Example: "DEX" in prereq
    - Example: "Dragonborn" in prereq
desc
    - the description of the feat
    - Ex: "armor" in desc
type
    - the type of feat; usually general, racial, or class
    - Note: general feats are feats that characters can take when they level up
    - Ex: "general" in type
    - Ex: "racial" in type
source
    - a reference to the origin of the feat
    - Ex: source is "PHB 165"
    - Ex: "homebrew" in source"""[1:]]},
        {"cmd":["help", "h"],
         "func":None,
         "args":[["<command>", "the name of a command, defaults to \"help\""]],
         "desc":["""
    Displays the help page for the given command. In order to keep channels from being cluttered with help pages, Puggerbot will send requested help pages via private message.

Commands:"""[1:]]},
        {"cmd":["hype"],
         "func":None,
         "args":[],
         "desc":["""
    :regional_indicator_h: :regional_indicator_y: :regional_indicator_p: :regional_indicator_e:"""[1:]]},
        {"cmd":["pet"],
         "func":None,
         "args":[],
         "desc":["""
    Show Puggerbot some love."""[1:]]},
        {"cmd":["purge"],
         "func":None,
         "args":[["<number>", "an unsigned integer, defaults to 100"]],
         "desc":["""
    You need admin permissions to run this command.
    Delete the specified number of messages from the current channel. If users are mentioned, then only messages posted by those users within the specified number of messages will be purged. Puggerbot will ask for confirmation of the purge. To confirm, issue the purge command again within 1 minute. Puggerbot will use the arguments of the first purge, not the confirmational purge."""[1:]]},
        {"cmd":["races", "rc"],
         "func":None,
         "args":[["<query>", "a boolean expression detailing the attributes of a set of races, see description"]],
         "desc":["""
    Search through Puggerbot's database of races to get a set of races that are specified by the query. This command works more like a search language than a search engine. Each race in the database is sectioned into fields such as 'name' and 'feats'. Restrictions can be placed on a field by using an operator. A restriction and operator can be applied to a field to form an expression. Expressions can be structured in one of two ways: "field operator restriction" or "restriction operator field". The way that the restriction and operator are applied to the field depends on the operator. Below is a list of each field and operator with a brief description and a few examples. All operators are case insensitive ("Fireball" is treated the same as "fireball"). Numerical restrictions do not have to surrounded by double quotes, however words and phrases must be.
"""[1:], """
Operators:
=, is
    - Format: field = restriction
    - checks if the entire field matches the restriction
    - Ex: race = "Human"
    - Ex: race is "Human"
!=
    - Format: field != restriction
    - checks if the entire field does not match the restriction
    - Ex: race != "Elf"
in
    - Format: restriction in field
    - functionally the same as "contains"
    - checks if the restriction is in the field
    - Ex: "Elf" in race
contains
    - Format: field contains restriction
    - functionally the same as "in"
    - checks if the field contains the restriction
    - Ex: feats contains "Darkvision"
and
    - Format: expression and expression
    - can be used to combine the effects of two or more expressions
    - checks if a feat matches all expressions
    - Ex: "STR+" in stats and "CON+" in stats
or
    - Format: expression or expression
    - can be used to combine the effects of two or more expressions
    - checks if a feat matches at least one of the expressions
    - Ex: stats contains "STR+" or stats contains "DEX+"
not, !
    - Format: not expression
    - negates the effect of an expression
    - this operator must go on the outside of an expression
    - Ex: not feats contains "Darkvision"
    - Ex: ! "Half" in race
"""[1:], """
Note on complex queries:
    The operators "and" and "or" can be used together to create more complex and specific queries.
Ex: desc contains "increase" and (desc contains "Strength" or desc contains "Constitution")

Fields:
name
    - the name of the race
    - Ex: name is "Human"
subrace
    - the name of the subrace
    - Ex: subrace is "Lightfoot"
stats
    - the ability score increase of the race
    - Ex: "INT+" in stats
    - Ex: stats contains "STR-"
    - Ex: stats contains "-"
size
    - the size of the race
    - Ex: size is "small"
lang
    - the languages that the race can speak
    - Ex: "draconic" in lang
feats
    - the traits a race has
    - Ex: "darkvision" in feats
src
    - a reference to the official documentation of the race
    - Ex: src is "PHB 20"
    - Ex: "homebrew" in src"""[1:]]},
        {"cmd":["rebuild", "rb"],
         "func":None,
         "args":[["<bot>", "a mention of a bot"]],
         "desc":["""
    You need master permissions to run this command.
    Use to refresh Puggerbot's memory. Manually restarts Puggerbot and rebuilds its database if it is mentioned in bot.
    Example: >rebuild @Puggerbot"""[1:]]},
        {"cmd":["restart", "rs"],
         "func":None,
         "args":[["<bot>", "a mention of a bot"]],
         "desc":["""
    You need master permissions to run this command.
    Use if Puggerbot seems a little off today. Manually restarts Puggerbot if it is mentioned in bot.
    Example: >restart @Puggerbot"""[1:]]},
        {"cmd":["roll", "r"],
         "func":None,
         "args":[["<expression>", "an arithmetic expression, see description"]],
         "desc":["""
    Tutorial pages exist for this command.
    Roll dice and do simple arithmetic.
    To learn more about how to use this command, please see its tutorial pages."""[1:]]},
        {"cmd":["shutdown", "sd"],
         "func":None,
         "args":[["<bot>", "a mention of a bot"]],
         "desc":["""
    You need master permissions to run this command.
    Use in case of rogue Puggerbot. Manually shuts down Puggerbot if it is mentioned in bot.
    Example: >shutdown @Puggerbot"""[1:]]},
        {"cmd":["spells", "sp"],
         "func":None,
         "args":[["<query>", "an expression detailing the attributes of a set of spells, see description"]],
         "desc":["""
    Search through Puggerbot's database of spells to get a set of spells that are specified by the query.
    To learn more about how to use this command, please see its tutorial pages."""]},
        {"cmd":["split", "s"],
         "func":None,
         "args":[["<coins>", "a string detailing the number and type of coins"],
                 ["<number>", "the number of party members to split the coins amongst"]],
         "desc":["""
    Equally split coins amongst a number of party members. Remaining change is also displayed.
    Example: >split 1 platinum 1337 cp 69gold 420sp, 6"""[1:]]},
        {"cmd":["tutorial", "tut"],
         "func":None,
         "args":[["<command>", "the name of a command"],
                 ["<index>", "the tutorial number, defaults to 1"]],
         "desc":["""
    Displays a tutorial page for certain commands. If a command has tutorial pages, it will be stated in the description of its help page. Tutorial pages start at index 1."""[1:]]},
        {"cmd":["update", "up"],
         "func":None,
         "args":[["<bot>", "a mention of a bot"]],
         "desc":["""
    You need master permissions to run this command.
    Use to build a better bot. Remotely updates Puggerbot if mentioned in bot.
    Example: >update @Puggerbot"""[1:]]},
        {"cmd":["version", "v"],
         "func":None,
         "args":[],
         "desc":["""
    Get the current version of Puggerbot."""[1:]]},
        {"cmd":["worth", "w"],
         "func":None,
         "args":[["<coins>", "a string detailing the number and type of coins"]],
         "desc":["""
    Convert a number of coins into the minimum number of coins with the same value.
    Makes comparing the worth of sets of coins easier.
    Example: >w 1 platinum 1337 cp 69gold 420sp"""[1:]]}]
for ii in cmds:
    cmds[2]["desc"][-1] += "\n"+" "*8+"- "+ii["cmd"][0]
