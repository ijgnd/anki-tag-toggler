### Config

You may use only keys/key combinations that are not used by Anki or other add-ons. If you
set a key/key combinatino that"s already used the key/key combination won"t work.

There's no option to disable a shortcut: just delete lines that you don't want to use.

The config consists of a so-called "dictionary" which assigns a key combination like "shift+h"
to a dictionary of values. Valid keys in that dict are `tags`, `action`, and `after`.

`tags`: Specify tags to modify in a string; separate multiple tags in the
string with spaces.

`action`: How to modify tags; options are "add" (the default), "delete",
and "toggle" (delete tag if present, add it if absent).

`after`: What to do to a card after modifying the tags; options are
"bury-card", "bury-note", "suspend-card" or "suspend-note".  Also "suspend"
and "bury", which are the same as the "-note" versions.

Example keybinding to add tags: 
    `"h": {"tags": "hard"}`
"add" is the default action, so this is the same:
    `"h": {"tags": "hard", "action": "add"}`
Modify multiple tags by separating them with spaces:
    `"h": {"tags": "hard marked"}`
Keybinding to delete tags (if they are present):
    `"h": {"tags": "hard marked", "action": "delete"}`
Keybinding to toggle tag:
    `"Shift+H": {"tags": "hard", "action": "toggle"}`
Bury a card after adding a tag:
    `"Shift+T": {"tags": "TODO", "after": "bury-card"}`
Suspend a note after adding a tag:
    `"Shift+E": {"tags": "easy", "after": "suspend-note"}`
Use all modifier keys to do the same thing:
    `"Meta+Ctr+Alt+Shift+E": {"tags": "easy", "after": "suspend-note"}`


### Config: Changes in comparison to Anki 2.0

In 2.0 you set 

    tag_dialog_shortcut = "T" 

This has been changed to 

    "shift+r": {
        "action": "tag_dialog_shortcut"
    }

In 2.0 you could set

    'Shift+E': {'tags': 'easy', 'after': 'suspend-note',}

In 2.1 you need to write this as:

    "Shift+E": {"tags": "easy", "after": "suspend-note"}

In Anki 2.1 you no longer may use single quotes(") around strings and you may no longer end 
a dictionary with a comma. These are limitations of the json format.
