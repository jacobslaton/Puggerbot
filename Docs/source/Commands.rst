.. _Commmands:

Commands
========

Puggerbot's commands all start with '>' and end with ';'.
The last command that a user runs does not need a ';'.
A message can have multiple commands and Puggerbot will process them in sequential order.

.. TODO::
	Find a better way to store error messages and help pages.

barkbork
--------

Puggerbot steps through the entire message that contained the command. For every "bark" he replies "bork" and vice versa.
This command can be used with bark or bork, but not barkbork.

Example::

	Message: This bark will be included even though it comes before the command. >bark bork bark
	Response: Bork bork bark bork!

bible
-----

Lookup verses from the Bible.
Choose your version by passing it in the "v" flag and indicate which passage by passing it in the "p" flag.

help
----

This command displays basic information about a command.
If a command is not specified, then general info about Puggerbot will be displayed instead.
This includes how to use the help command, Puggerbot's version, and a link to Puggerbot's github page.

hype
----

Puggerbot replies to the command with emojis that spell "hype".

pet
---

Puggerbot posts a randomly selected gif of a pug.

update
------

This command restarts Puggerbot to pull from his git repository.
It can only be used by the bot owner.

shutdown
--------

This command shuts down Puggerbot.
It can only be used by the bot owner.
