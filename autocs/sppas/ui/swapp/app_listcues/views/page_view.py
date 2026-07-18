"""
:filename: sppas.ui.swapp.app_listcues.views.page_view.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: View of the "ListCueS" conversion page.

..
    This file is part of Auto-CS: <https://autocs.sourceforge.io>
    -------------------------------------------------------------------------

    Copyright (C) 2026  Brigitte Bigi, CNRS
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
from whakerpy.htmlmaker import EmptyNode
from whakerpy.htmlmaker.htmnodes.htmnode import TagNode

from sppas.core.config import separators

from ..listcues_msg import MSG_CUE_LABEL
from ..listcues_msg import MSG_CUE_PLACEHOLDER
from ..listcues_msg import MSG_VALIDATE_BUTTON
from ..listcues_record import ListCueSRecord
from ..listcues_model import ListCueSModel

from sppas.ui.swapp.app_cues_utils.nodes.tags import HTMLTag
from sppas.ui.swapp.app_cues_utils.nodes.key_piano import KeyPianoNode
from .nodes.prons_table import PronsTableNode

# ---------------------------------------------------------------------------


class ListCueSPageView:
    """View of the conversion page: 1 textarea (cue) and its result table.

    """

    def __init__(self, parent: HTMLNode, record: ListCueSRecord) -> None:
        """Create the HTML node of the conversion page of "ListCueS".

        :param parent: (HTMLNode) The parent id of the HTML node
        :param record: (ListCueSRecord) The data to fill-in the view content

        """
        self._parent = parent
        self._record = record
        self._form = None

    # -----------------------------------------------------------------------
    # PUBLIC METHOD -- construct the UI
    # -----------------------------------------------------------------------

    def create(self) -> None:
        """Create and append the children nodes.

        """
        _content = HTMLTag.create_section(self._parent)

        self._form = HTMLTag.create_form(_content, "listcues_form")
        self._fill_form()

        self.display_result()

    # -----------------------------------------------------------------------

    def display_result(self) -> TagNode:
        """Create and fill-in the result section from the record extras.

        Errors and info messages are exclusively reported through the Yoyo
        dialogs (see :class:`ListCueSController`), not inline in this section.

        :return: (TagNode) The result section node

        """
        _s = self.__create_result_container()

        if "prons_result" in self._record.extras:
            self.__append_prons_result(_s, self._record.extras["prons_result"])

        return _s

    # -----------------------------------------------------------------------
    # PROTECTED -- construct the UI
    # -----------------------------------------------------------------------

    def _fill_form(self) -> None:
        """Fill-in the inputs form.

        The piano sits between the label and the textarea it writes into:
        the label/textarea association is by "for"/"id", not DOM order, so
        this does not affect how a screen reader names the textarea.

        """
        self._append_hidden_lang()
        self._append_cue_label()
        self._append_key_piano()
        self._append_cue_textarea()
        HTMLTag.append_submit_in_form(self._form, "listcues", MSG_VALIDATE_BUTTON)

    # -----------------------------------------------------------------------

    def _append_hidden_lang(self) -> None:
        """Carry the language chosen on the welcome page along with every "convert" event.

        The conversion page has no language selector of its own: the piano
        depends on a language fixed once and for all on the welcome page.

        """
        _input = EmptyNode(self._form.identifier, None, "input",
                           attributes={"id": "lang", "name": "lang", "type": "hidden",
                                      "value": self._record.lang})
        self._form.append_child(_input)

    # -----------------------------------------------------------------------

    def _append_key_piano(self) -> None:
        """Add the shape/position key piano, if the model provided its keys.

        """
        _shape_keys = self._record.extras.get("shape_keys", tuple())
        _position_keys = self._record.extras.get("position_keys", tuple())
        if len(_shape_keys) == 0 or len(_position_keys) == 0:
            return

        _piano = KeyPianoNode(self._form.identifier, "cue", _shape_keys, _position_keys)
        self._form.append_child(_piano)

    # -----------------------------------------------------------------------

    def _append_cue_label(self) -> None:
        """Add the label of the "cue" textarea to the form.

        """
        label = HTMLNode(self._form.identifier, None, "label",
                         attributes={"for": "cue"},
                         value=MSG_CUE_LABEL)
        self._form.append_child(label)

    # -----------------------------------------------------------------------

    def _append_cue_textarea(self) -> None:
        """Add the "cue" textarea to the form.

        """
        att = dict()
        att["id"] = "cue"
        att["name"] = "cue"
        att["class"] = "cue-textarea"
        att["placeholder"] = MSG_CUE_PLACEHOLDER
        att["rows"] = "1"
        att["maxlength"] = str(self.__max_cue_length())
        textarea = HTMLNode(self._form.identifier, None, "textarea", attributes=att)
        self._form.append_child(textarea)

        if self._record.cue is not None:
            textarea.set_value(self._record.cue)

    # -----------------------------------------------------------------------

    def __max_cue_length(self) -> int:
        """Return the max character length of a valid cue, for the current language.

        The model accepts up to ListCueSModel.MAX_KEYS '<shape>-<position>'
        segments separated by '.': the actual max length depends on the
        language's longest shape/position codes (e.g. English has 2-character
        position codes "sf"/"sd", unlike French's single-character ones).

        :return: (int) Max number of characters a valid cue can hold.

        """
        _shape_keys = self._record.extras.get("shape_keys", tuple())
        _position_keys = self._record.extras.get("position_keys", tuple())
        _max_shape = max((len(_k["code"]) for _k in _shape_keys), default=1)
        _max_position = max((len(_k["code"]) for _k in _position_keys), default=1)

        _one_key = _max_shape + len(separators.phonemes) + _max_position
        _nb_seps = ListCueSModel.MAX_KEYS - 1
        return (_one_key * ListCueSModel.MAX_KEYS) + (len(separators.syllables) * _nb_seps)

    # -----------------------------------------------------------------------
    # PRIVATE
    # -----------------------------------------------------------------------

    def __create_result_container(self) -> TagNode:
        _s = HTMLTag.create_section(self._parent)
        _s.add_attribute("id", "result_section")
        return _s

    # -----------------------------------------------------------------------

    @staticmethod
    def __append_prons_result(parent: TagNode, entries: tuple) -> None:
        """Append the table of pronunciations and their matching words.

        :param parent: (TagNode) The parent node
        :param entries: (tuple) See :class:`Keys2PronsModel.convert`

        """
        if len(entries) == 0:
            return

        _table = PronsTableNode(parent.identifier, entries)
        parent.append_child(_table)
