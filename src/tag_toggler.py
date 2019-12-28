# Tag Toggler 2
# Copyright: 2019 ijngd (port to 2.1)
#            Don March <don@ohspite.net>
#            2012 Cayenne Boyer (tag toggler says that it's "Based in part on Quick Tagging by Cayenne Boyer")
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

import os

from anki.lang import _
from anki.hooks import addHook, wrap

from aqt import mw
from aqt.utils import getTag, tooltip, showInfo
from aqt.qt import *
from aqt.reviewer import Reviewer


addon_path = os.path.dirname(__file__)
foldername = os.path.basename(addon_path)
addonname = mw.addonManager.addonName(foldername)


def gc(arg, fail=False):
    return mw.addonManager.getConfig(__name__).get(arg, fail)


def check_conf(conf):
    not_a_dict = []
    illegal_actions = []
    illegal_after = []
    for k, v in conf.items():
        if not isinstance(v, dict):
            not_a_dict.append(k)
            tooltip('illegal value in config')
        else:
            if 'action' in v:
                if v['action'] not in ['add', 'delete', 'toggle', "tag_dialog_shortcut"]:
                    illegal_actions.append(k)
            if 'after' in v:
                aa = ['bury', 'bury-card', 'bury-note', 'suspend', 'suspend-card', 'suspend-note']
                if v['after'] not in aa:
                    illegal_after.append(k)
    infostr = 'Error in config for the addon "{}"\n\n'.format(addonname)
    if not_a_dict:
        infostr += "These values are not a dict:\n"
        infostr += "\n, ".join([str(x) for x in not_a_dict])
    if illegal_actions:
        infostr += "\n\nthe values for these keys don't contain a valid action:\n"
        infostr += "\n, ".join([str(x) for x in illegal_actions])
    if illegal_after:
        infostr += "\n\nthe values for these keys don't contain a valid value for \"after\":\n"
        infostr += "\n, ".join([str(x) for x in illegal_after])
    showInfo(infostr)
mw.addonManager.setConfigUpdatedAction(__name__, check_conf)


def addShortcuts(cuts):
    for k, v in mw.addonManager.getConfig(__name__).items():
        cuts.append((k, lambda vals=v: tagactions(vals)))
addHook("reviewStateShortcuts", addShortcuts)


def tagactions(v):
    # tooltip(v)
    card = mw.reviewer.card
    note = card.note()
    if v.get("action", "") == "tag_dialog_shortcut": 
        mw.checkpoint(_("Edit Tags"))
        edit_tag_dialog(note)
    else:
        if 'action' not in v:
            v['action'] = 'add'
        same_card_shown = False
        if ('after' in v and v['after'] in ['suspend', 'suspend-note']):
            mw.checkpoint("Edit Tags and Suspend Note")
            ttmsg = 'Suspended note and edited tags: {}'
            mw.col.sched.suspendCards(
                [c.id for c in note.cards()])
        elif 'after' in v and v['after'] in ['bury', 'bury-note']:
            mw.checkpoint("Edit Tags and Bury Note")
            ttmsg = 'Buried note and edited tags: {}'
            mw.col.sched.buryNote(note.id)
        elif 'after' in v and v['after'] == 'suspend-card':
            mw.checkpoint("Edit Tags and Suspend Card")
            ttmsg = 'Suspended card and edited tags: {}'
            mw.col.sched.suspendCards([card.id])
        elif 'after' in v and v['after'] == 'bury-card':
            mw.checkpoint("Edit Tags and Bury Card")
            ttmsg = 'Buried card and edited tags: {}'
            mw.col.sched.buryCards([card.id])
        else:
            mw.checkpoint(_("edit Tags"))
            ttmsg = 'Edited tags: {}'
            same_card_shown = True
        tag_edits = edit_note_tags(note, v['tags'], v['action'])
        reset_and_redraw(same_card_shown)
        tooltip(ttmsg.format(tag_edits))


def edit_tag_dialog(note):
    """Prompt for tags and add the results to note."""
    prompt = _("Edit tag list:")
    (tag_string, dialog_status) = getTag(mw, mw.col, prompt, default=note.stringTags())
    if dialog_status:
        note.setTagsFromStr(tag_string)
        note.flush()
        reset_and_redraw(same_card_shown=True)
        tooltip('Tags set to: "{}"'.format(tag_string))


def edit_note_tags(note, tags, action='add'):
    """Apply action to each space separated tag in the string `tags`."""
    tag_list = mw.col.tags.split(tags)
    additions = []
    deletions = []
    for tag in tag_list:
        if action == 'delete':
            if note.hasTag(tag):
                note.delTag(tag)
                deletions.append(tag)
        elif action == 'toggle':
            if note.hasTag(tag):
                note.delTag(tag)
                deletions.append(tag)
            else:
                note.addTag(tag)
                additions.append(tag)
        else:  # action == 'add'
            if not note.hasTag(tag):
                note.addTag(tag)
                additions.append(tag)
    note.flush()

    messages = []
    if additions:
        messages.append("added: \"{}\"".format(" ".join(additions)))
    if deletions:
        messages.append("removed: \"{}\"".format(" ".join(deletions)))
    if messages:
        return "\n".join(messages)
    else:
        return "(no changes)"


def reset_and_redraw(same_card_shown=False):
    """Rebuild the scheduler and redraw the card."""
    in_answer_state = (mw.reviewer.state == "answer")
    if same_card_shown:
        mw.reviewer.card.load()
        mw.reviewer.cardQueue.append(mw.reviewer.card)
    mw.moveToState("review")

    if in_answer_state and same_card_shown:
        try:
            mw.reviewer._showAnswer()
        except:
            pass
