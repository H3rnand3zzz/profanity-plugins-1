"""
Read message out loud.

On linux requires 'espeak' which is available on most distributions e.g.:
    sudo apt-get install espeak

On OSX will use the built in 'say' command.
"""

import prof
import os
import shlex
from sys import platform

def say(message):
    args = prof.settings_string_get("say", "args", "")

    if platform == "darwin":
        os.system("say " + args + " " + shlex.quote(message) + " 2>/dev/null")
    elif platform == "linux" or platform == "linux2":
        os.system("echo " + shlex.quote(message) + " | espeak " + args + " 2>/dev/null")


def prof_post_chat_message_display(barejid, resource, message):
    enabled = prof.settings_string_get("say", "enabled", "off")
    current_recipient = prof.get_current_recipient()
    if enabled == "on" or (enabled == "active" and current_recipient == barejid):
        say(barejid + " says " + message)

    return message


def prof_post_room_message_display(barejid, nick, message):
    enabled = prof.settings_string_get("say", "enabled", "off")
    current_muc = prof.get_current_muc()
    if enabled == "on":
        say(nick + " in " + barejid + " says " + message)
    elif enabled == "active" and current_muc == barejid:
        say(nick + " says " + message)

    return message


def prof_post_priv_message_display(barejid, nick, message):
    # TODO add get current nick hook for private chats
    if enabled:
        say(nick + " says " + message)

    return message


def _cmd_say(arg1=None, arg2=None):
    if arg1 == "on":
        prof.settings_string_set("say", "enabled", "on")
        prof.cons_show("Say plugin enabled")
    elif arg1 == "off":
        prof.settings_string_set("say", "enabled", "off")
        prof.cons_show("Say plugin disabled")
    elif arg1 == "active":
        prof.settings_string_set("say", "enabled", "active")
        prof.cons_show("Say plugin enabled for active window only")
    elif arg1 == "args":
        if arg2 == None:
            prof.cons_bad_cmd_usage("/say")
        else:
            prof.settings_string_set("say", "args", arg2)
            prof.cons_show("Say plugin arguments set to: " + arg2)
    elif arg1 == "clearargs":
        prof.settings_string_set("say", "args", "")
        prof.cons_show("Say plugin arguments cleared")
    elif arg1 == "test":
        if arg2 == None:
            prof.cons_bad_cmd_usage("/say")
        else:
            say(arg2)
    else:
        enabled = prof.settings_string_get("say", "enabled", "off")
        args = prof.settings_string_get("say", "args", "")
        prof.cons_show("Say plugin settings:")
        prof.cons_show("enabled : " + enabled)
        if args != "":
            prof.cons_show("args    : " + args)


def prof_init(version, status, account_name, fulljid):
    synopsis = [ 
        "/say on|off|active",
        "/say args <args>",
        "/say clearargs",
        "/say test <message>"
    ]
    description = "Read messages out loud"
    args = [
        [ "on|off",         "Enable/disable say for all windows" ],
        [ "active",         "Enable say for active window only" ],
        [ "args <args>",    "Arguments to pass to command" ],
        [ "clearargs",      "Clear command arguments" ],
        [ "test <message>", "Say message" ]
    ]
    examples = []

    prof.register_command("/say", 0, 2, synopsis, description, args, examples, _cmd_say)
    prof.completer_add("/say", [ "on", "off", "test", "active", "args", "clearargs" ])
