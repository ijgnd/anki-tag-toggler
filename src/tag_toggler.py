from PyQt4.QtCore import Qt
from PyQt4.QtGui import QKeySequence

from aqt import mw
from aqt.utils import getTag, tooltip, showInfo
from aqt.reviewer import Reviewer
from anki.hooks import wrap


def tagKeyHandler(self, event, _old):
    """Wrap default _keyHandler with new keybindings."""
    key = event.key()

    if key == Qt.Key_unknown:
        _old(self, event)
    # only modifier pushed
    if (key == Qt.Key_Control or
        key == Qt.Key_Shift or
        key == Qt.Key_Alt or
        key == Qt.Key_Meta):
        _old(self, event)

    # check for combination of keys and modifiers
    modifiers = event.modifiers()
    if modifiers & Qt.ShiftModifier:
        key += Qt.SHIFT
    if modifiers & Qt.ControlModifier:
        key += Qt.CTRL
    if modifiers & Qt.AltModifier:
        key += Qt.ALT
    if modifiers & Qt.MetaModifier:
        key += Qt.META

    key_sequence = QKeySequence(key).toString(QKeySequence.PortableText)

    ## Uncomment this to display keybinding strings for keys that are pressed
    ## when reviewing cards:

    # showInfo(key_sequence)

    note = mw.reviewer.card.note()
    if tag_dialog_shortcut and key_sequence == tag_dialog_shortcut:
        mw.checkpoint(_("Edit Tags"))
        edit_tag_dialog(note)
    elif key_sequence in tag_shortcuts:
        binding = tag_shortcuts[key_sequence]
        if 'action' not in binding:
            binding['action'] = 'add'

        same_card_shown = False
        if ('after' in binding and
            binding['after'] in ['suspend', 'suspend-note']):
            mw.checkpoint("Edit Tags and Suspend Note")
            tooltip_message = 'Suspended note and edited tags: {}'
            self.mw.col.sched.suspendCards(
                [card.id for card in self.card.note().cards()])
        elif 'after' in binding and binding['after'] in ['bury', 'bury-note']:
            mw.checkpoint("Edit Tags and Bury Note")
            tooltip_message = 'Buried note and edited tags: {}'
            mw.col.sched.buryNote(note.id)
        elif 'after' in binding and binding['after'] == 'suspend-card':
            mw.checkpoint("Edit Tags and Suspend Card")
            tooltip_message = 'Suspended card and edited tags: {}'
            self.mw.col.sched.suspendCards([self.card.id])
        elif 'after' in binding and binding['after'] == 'bury-card':
            mw.checkpoint("Edit Tags and Bury Card")
            tooltip_message = 'Buried card and edited tags: {}'
            mw.col.sched.buryCards([self.card.id])
        else:
            mw.checkpoint(_("edit Tags"))
            tooltip_message = 'Edited tags: {}'
            same_card_shown = True

        tag_edits = edit_note_tags(note, binding['tags'], binding['action'])
        reset_and_redraw(same_card_shown)
        tooltip(tooltip_message.format(tag_edits))
    else:
        _old(self, event)


def edit_tag_dialog(note):
    """Prompt for tags and add the results to note."""
    prompt = _("Edit tag list:")
    (tag_string, dialog_status) = getTag(mw, mw.col, prompt, default=note.stringTags())
    if dialog_status != 0:  # means "Cancel"
        note.setTagsFromStr(tag_string)
        note.flush()
        reset_and_redraw(same_card_shown=True)
        tooltip('Tags set to: "{}"'.format(tag_string))


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


def shortcuts_are_okay():
    error_message = (
        "The Tag Toggle add-on will not be started.\n\n"
        "Check the configuration for an undefined '{}' "
        "value '{}' in tag_shortcuts:\n\n"
        "{}")

    def check_command(command, command_type, options):
        if command_type in command:
            value = command[command_type]
            if value not in options:
                showInfo(error_message.format(command_type, value, command))
                return False
        return True

    for shortcut in tag_shortcuts:
        command = tag_shortcuts[shortcut]
        if not check_command(command, 'action', ['add', 'delete', 'toggle']):
            return False
        if not check_command(command, 'after',
                             ['bury', 'bury-card', 'bury-note',
                              'suspend', 'suspend-card', 'suspend-note']):
            return False

    return True


if shortcuts_are_okay():
    Reviewer._keyHandler = wrap(Reviewer._keyHandler, tagKeyHandler, "around")
