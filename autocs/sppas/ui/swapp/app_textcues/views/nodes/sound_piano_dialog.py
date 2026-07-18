"""
:filename: sppas.ui.swapp.app_textcues.views.nodes.sound_piano_dialog.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: HTMLNode for the shared phoneme-piano dialog of the "Sound" page.

..
    This file is part of Auto-CS: <https://autocs.sourceforge.io>
    -------------------------------------------------------------------------

    Copyright (C) 2021-2026  Brigitte Bigi, CNRS
    Laboratoire Parole et Langage, Aix-en-Provence, France

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    This banner notice must not be removed.

    -------------------------------------------------------------------------

"""

from __future__ import annotations
from whakerpy.htmlmaker import HTMLNode

from sppas.ui.swapp.wappcore.wappsg import wapp_settings

from ...textcues_msg import MSG_SOUND_PIANO_TITLE
from ...textcues_msg import MSG_SOUND_PIANO_PREVIEW
from ...textcues_msg import MSG_SOUND_PIANO_VALIDATE
from ...textcues_msg import MSG_SOUND_PIANO_CANCEL
from ...textcues_msg import MSG_PIANO_CONSONANTS_GROUP
from ...textcues_msg import MSG_PIANO_VOWELS_GROUP

# ---------------------------------------------------------------------------

# Id of the staging field the piano always writes into: never one of the
# table rows' "<index>-sound_input" fields directly, since those stay
# hidden behind the modal dialog while it is open. "Apply" copies this
# staging value into whichever row's field the dialog was opened for;
# "Cancel" (or Escape) discards it untouched.
STAGING_FIELD_ID = "sound-piano-staging"

# ---------------------------------------------------------------------------


class SoundPianoDialogNode(HTMLNode):
    """A single dialog, shared by every row of the pronunciation table.

    It is opened by a row's "Phoneme keyboard" toggle button (see
    :class:`SoundsTableNode`): the staging field is filled with that row's
    current value, the dialog's title names the row's token, and "Apply"
    copies the (possibly piano-composed, possibly hand-edited) staging
    value back into that row's "<index>-sound_input" field.

    This composes a plain phoneme sequence: both groups are in "free" mode,
    and both separators are the same character, so every click -- consonant
    or vowel, in any order -- is joined the same way (e.g. "p-a-p-a").

    """

    def __init__(self, parent_id: str, consonants: tuple, vowels: tuple):
        """Create the dialog, its staging field and its phoneme piano.

        :param parent_id: (str) The parent id of the HTML node
        :param consonants: (tuple) Every consonant phoneme of the current language
        :param vowels: (tuple) Every vowel phoneme of the current language

        """
        super(SoundPianoDialogNode, self).__init__(parent_id, "sound-piano-dialog", "dialog")
        self.add_attribute("id", "sound-piano-dialog")
        self.add_attribute("class", "hidden-alert")
        self.add_attribute("aria-labelledby", "sound-piano-dialog-title")

        _title = HTMLNode(self.identifier, None, "h2", value=MSG_SOUND_PIANO_TITLE)
        _title.add_attribute("id", "sound-piano-dialog-title")
        self.append_child(_title)
        _token = HTMLNode(_title.identifier, None, "span")
        _token.add_attribute("id", "sound-piano-dialog-token")
        _title.append_child(_token)

        # The staging/preview field: both the piano's target and a plain
        # text input the user can edit by hand. Order matters: label ->
        # piano -> field -- the label/field association is by "for"/"id",
        # not DOM order, so this does not affect how a screen reader names
        # the field.
        _label = HTMLNode(self.identifier, None, "label",
                          attributes={"for": STAGING_FIELD_ID}, value=MSG_SOUND_PIANO_PREVIEW)
        self.append_child(_label)

        _piano = HTMLNode(self.identifier, "sound-piano", "div")
        _piano.add_attribute("class", "wexa-key-piano")
        _piano.add_attribute("data-target", STAGING_FIELD_ID)
        _piano.add_attribute("data-group-sep", "-")
        _piano.add_attribute("data-key-sep", "-")
        _piano.add_attribute("data-icons-path", wapp_settings.wexa_statics + "icons/mono-svg")
        self.append_child(_piano)

        self.__append_free_group(_piano, MSG_PIANO_CONSONANTS_GROUP, consonants)
        self.__append_free_group(_piano, MSG_PIANO_VOWELS_GROUP, vowels)

        _staging = HTMLNode(self.identifier, None, "input",
                            attributes={"id": STAGING_FIELD_ID, "type": "text", "class": "cue-textarea"})
        self.append_child(_staging)

        _actions = HTMLNode(self.identifier, None, "div")
        self.append_child(_actions)

        _validate = HTMLNode(_actions.identifier, "sound-piano-validate", "button",
                             value=MSG_SOUND_PIANO_VALIDATE)
        _validate.add_attribute("id", "sound-piano-validate")
        _validate.add_attribute("type", "button")
        _actions.append_child(_validate)

        _cancel = HTMLNode(_actions.identifier, "sound-piano-cancel", "button",
                           value=MSG_SOUND_PIANO_CANCEL)
        _cancel.add_attribute("id", "sound-piano-cancel")
        _cancel.add_attribute("type", "button")
        _actions.append_child(_cancel)

    # -----------------------------------------------------------------------
    # PRIVATE
    # -----------------------------------------------------------------------

    @staticmethod
    def __append_free_group(piano: HTMLNode, group_label: str, phonemes: tuple) -> None:
        """Append one "free" group of plain phoneme buttons.

        :param piano: (HTMLNode) The "wexa-key-piano" parent node.
        :param group_label: (str) Accessible name of the group.
        :param phonemes: (tuple) Phonemes to turn into buttons.

        """
        _group = HTMLNode(piano.identifier, None, "div")
        _group.add_attribute("class", "wexa-key-piano-group")
        _group.add_attribute("data-mode", "free")
        _group.add_attribute("aria-label", group_label)
        piano.append_child(_group)

        for _phoneme in phonemes:
            _btn = HTMLNode(_group.identifier, None, "button", value=_phoneme)
            _btn.add_attribute("type", "button")
            _btn.add_attribute("class", "wexa-key-piano-key")
            _btn.add_attribute("value", _phoneme)
            _group.append_child(_btn)
