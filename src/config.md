# Tag Toggler 1.2.2 (2017-02-06)
# Copyright: Don March <don@ohspite.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Tag Toggler is an Anki 2 add-on for quickly adding tags while reviewing.

# Based in part on Quick Tagging by Cayenne Boyer
# (https://github.com/cayennes/Quick_Tagging)

########################################
## CONFIGURATION INSTRUCTIONS

## There are two variables to edit--tag_dialog_shortcut and tag_shortcuts.

## Lines with a leading `#` are comments and have no effect.  Lines with a
## single `#` are code examples that you can use by removing the leading `#`.

## You can overwrite some previously existing shortcuts, but it's easiest if
## you pick keys that are unused or that are shortcuts when reviewing cards
## only (defined in Reviewer._keyHandler).  Some keys (such as 'A' for Add or
## 'B' for Browse are defined elsewhere; the effect of adding Tag Toggle
## functionality to these keys is not well defined.

## Keybindings are strings that specify modifiers plus the primary key that
## triggers the action.  If the primary key is a letter, it must be uppercase.

## You can specify keybindings that include any combination of the following
## modifier keys: Meta, Ctrl, Alt, Shift.  When including modifiers they must
## be listed in that order (Meta, Ctrl, Alt, Shift), omitting any that you
## don't want to use.

## Examples of correct and incorrect keybindings:
##
##     'T'                     # correct (T key without any modifiers)
##     'Shift+T                # correct (T key while holding Shift)
##     'Meta+Ctrl+Alt+Shift+T' # correct
##     'Ctrl+Shift+T'          # correct
##
##     't'                     # incorrect (letter keys must be uppercase)
##     'Shift+Ctrl+T'          # incorrect (wrong modifier order)
##     'ctrl+shift+T'          # incorrect (case is significant)

## If you are unsure how to bind a particular key combination, you can
## uncomment the following line in the tagKeyHandler function:
##
##     showInfo(key_sequence)
##
## When reviewing cards, this will catch and display all key combinations that
## are pressed.

########################################
## CONFIGURATION OPTIONS

## Change `tag_dialog_shortcut` to the key you want to open a dialog to
## quickly edit tags.  Set `tag_dialog_shortcut = None` to disable the
## shortcut.
tag_dialog_shortcut = 'T'
# tag_dialog_shortcut = 'Shift+T'
# tag_dialog_shortcut = None

## Add items to the `tag_shortcuts` dict to create shortcuts that modify
## tags. The dict keys are the key for the keyboard shortcut, and each should
## refer to a dict to specify the command.  Valid keys in that dict are
## 'tags', 'action', and 'after'.
##
## 'tags': Specify tags to modify in a string; separate multiple tags in the
## string with spaces.
##
## 'action': How to modify tags; options are 'add' (the default), 'delete',
## and 'toggle' (delete tag if present, add it if absent).
##
## 'after': What to do to a card after modifying the tags; options are
## 'bury-card', 'bury-note', 'suspend-card' or 'suspend-note'.  Also 'suspend'
## and 'bury, which are the same as the '-note' versions.
##
## Example keybinding to add tags:
##    'h': {'tags': 'hard'}
## 'add' is the default action, so this is the same:
##    'h': {'tags': 'hard', 'action': 'add'}
## Modify multiple tags by separating them with spaces:
##    'h': {'tags': 'hard marked'}
## Keybinding to delete tags (if they are present):
##    'h': {'tags': 'hard marked', 'action': 'delete'}
## Keybinding to toggle tag:
##    'Shift+H': {'tags': 'hard', 'action': 'toggle'}
## Bury a card after adding a tag:
##    'Shift+T': {'tags': 'TODO', 'after': 'bury-card'}
## Suspend a note after adding a tag:
##    'Shift+E': {'tags': 'easy', 'after': 'suspend-note'}
## Use all modifier keys to do the same thing:
##    'Meta+Ctr+Alt+Shift+E': {'tags': 'easy', 'after': 'suspend-note'}

tag_shortcuts = {
#    'Shift+H': {'tags': 'hard', 'action': 'toggle'},
#    'Shift+T': {'tags': 'TODO', 'after': 'bury-note'},
#    'Shift+A': {'tags': 'easy', 'after': 'suspend-card'},
}

## END CONFIGURATION
########################################

# Testing:

# As far as I know, there is no easy way to automatically test this.  Here are
# some keybindings to add to `tag_shortcuts` that cover most cases.  (Be sure
# to test `tag_dialog_shortcut` as well).

# The first two should cause a graceful error when Anki is starting up.
    # 'Z': {'tags': 'test-a', 'action': 'blah'},
    # 'Shift+Z': {'tags': 'test-a', 'after': 'blah'},
    # 'Z': {'tags': 'test-a'},
    # 'Shift+Z': {'tags': 'test-b'},
    # 'X': {'tags': 'test-a', 'action': 'delete'},
    # 'Shift+X': {'tags': 'test-b', 'action': 'delete'},
    # 'C': {'tags': 'test-a test-b'},
    # 'Alt+C': {'tags': 'test-a test-b', 'action': 'delete'},
    # 'Alt+Shift+C': {'tags': 'test-a test-b', 'action': 'toggle'},
    # 'Alt+Z': {'tags': 'test-a test-b', 'after': 'bury-card'},
    # 'Alt+Shift+Z': {'tags': 'test-a test-b', 'after': 'suspend-card'},
    # 'Meta+Ctrl+Alt+Shift+Z': {'tags': 'lots-of-modifier-keys'} 
