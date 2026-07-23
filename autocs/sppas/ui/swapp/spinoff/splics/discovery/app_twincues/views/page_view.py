"""
:filename: sppas.ui.swapp.spinoff.splics.discovery.app_twincues.views.page_view.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: View of the "TwinCueS" conversion page.

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
from whakerpy.htmlmaker import EmptyNode
from whakerpy.htmlmaker.htmnodes.htmnode import TagNode

from ..twincues_msg import MSG_WORD_LABEL
from ..twincues_msg import MSG_WORD_PLACEHOLDER
from ..twincues_msg import MSG_CUE_LABEL
from ..twincues_msg import MSG_CUE_PLACEHOLDER
from ..twincues_msg import MSG_VALIDATE_BUTTON
from ..twincues_msg import MSG_RESULT_CUE_LABEL
from ..twincues_msg import MSG_RESULT_WORD_LABEL
from ..twincues_record import TwinCueSRecord

from sppas.ui.swapp.spinoff.splics.nodes.layout.tags import HTMLTag
from sppas.ui.swapp.spinoff.splics.nodes.cues.key_piano import KeyPianoNode

# ---------------------------------------------------------------------------


class TwinCueSPageView:
    """View of the conversion page: 2 textarea (word, cue) and their result.

    """

    def __init__(self, parent: HTMLNode, record: TwinCueSRecord) -> None:
        """Create the HTML node of the conversion page of "TwinCueS".

        :param parent: (HTMLNode) The parent id of the HTML node
        :param record: (TwinCueSRecord) The data to fill-in the view content

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

        self._form = HTMLTag.create_form(_content, "twincues_form")
        self._fill_form()

        self.display_result()

    # -----------------------------------------------------------------------

    def display_result(self) -> TagNode:
        """Create and fill-in the result section from the record extras.

        Errors and info messages are exclusively reported through the Yoyo
        dialogs (see :class:`TwinCueSController`), not inline in this section.

        :return: (TagNode) The result section node

        """
        _s = self.__create_result_container()

        if "cues_result" in self._record.extras:
            self.__append_cues_result(_s, self._record.extras["cues_result"])

        if "words_result" in self._record.extras:
            self.__append_words_result(_s, self._record.extras["words_result"])

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
        self._append_word_input()
        self._append_cue_label()
        self._append_key_piano()
        self._append_cue_textarea()
        HTMLTag.append_submit_in_form(self._form, "twincues", MSG_VALIDATE_BUTTON)

    # -----------------------------------------------------------------------

    def _append_hidden_lang(self) -> None:
        """Carry the language chosen on the welcome page along with every submit.

        The conversion page has no language selector of its own: the model
        depends on a language fixed once and for all on the welcome page.

        """
        _input = EmptyNode(self._form.identifier, None, "input",
                           attributes={"id": "lang", "name": "lang", "type": "hidden",
                                      "value": self._record.lang})
        self._form.append_child(_input)

    # -----------------------------------------------------------------------

    def _append_word_input(self) -> None:
        """Add the "word" textarea to the form.

        """
        label = HTMLNode(self._form.identifier, None, "label",
                         attributes={"for": "word"},
                         value=MSG_WORD_LABEL)
        self._form.append_child(label)

        att = dict()
        att["id"] = "word"
        att["name"] = "word"
        att["class"] = "cue-textarea"
        att["placeholder"] = MSG_WORD_PLACEHOLDER
        att["rows"] = "1"
        textarea = HTMLNode(self._form.identifier, None, "textarea", attributes=att)
        self._form.append_child(textarea)

        if self._record.word is not None:
            textarea.set_value(self._record.word)

    # -----------------------------------------------------------------------

    def _append_cue_label(self) -> None:
        """Add the label of the "cue" textarea to the form.

        """
        label = HTMLNode(self._form.identifier, None, "label",
                         attributes={"for": "cue"},
                         value=MSG_CUE_LABEL)
        self._form.append_child(label)

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

    def _append_cue_textarea(self) -> None:
        """Add the "cue" textarea to the form.

        """
        att = dict()
        att["id"] = "cue"
        att["name"] = "cue"
        att["class"] = "cue-textarea"
        att["placeholder"] = MSG_CUE_PLACEHOLDER
        att["rows"] = "1"

        _max_length = self._record.extras.get("max_cue_length", 0)
        if _max_length > 0:
            att["maxlength"] = str(_max_length)

        textarea = HTMLNode(self._form.identifier, None, "textarea", attributes=att)
        self._form.append_child(textarea)

        if self._record.cue is not None:
            textarea.set_value(self._record.cue)

    # -----------------------------------------------------------------------
    # PRIVATE
    # -----------------------------------------------------------------------

    def __create_result_container(self) -> TagNode:
        _s = HTMLTag.create_section(self._parent)
        _s.add_attribute("id", "result_section")
        return _s

    # -----------------------------------------------------------------------

    @staticmethod
    def __append_cues_result(parent: TagNode, entries: tuple) -> None:
        """Append, for each distinct cue of the queried word, its pronunciations and twins.

        :param parent: (TagNode) The parent node
        :param entries: (tuple) See :class:`Word2CuesModel.convert`

        """
        for entry in entries:
            _prons = ", ".join(entry["prons"])
            _p = HTMLNode(parent.identifier, None, "p",
                          value=f"{MSG_RESULT_CUE_LABEL} {_prons} -> {entry['cue']}")
            _p.add_attribute("class", "coded-token")
            parent.append_child(_p)

            if len(entry["twins"]) == 0:
                continue

            _ul = HTMLNode(parent.identifier, None, "ul")
            parent.append_child(_ul)
            for twin in entry["twins"]:
                _li = HTMLNode(_ul.identifier, None, "li",
                               value=f"{twin['word']} ({twin['pron']})")
                _ul.append_child(_li)

    # -----------------------------------------------------------------------

    @staticmethod
    def __append_words_result(parent: TagNode, entries: tuple) -> None:
        """Append the words sharing the queried cue.

        :param parent: (TagNode) The parent node
        :param entries: (tuple) See :class:`Cues2WordsModel.convert`

        """
        _p = HTMLNode(parent.identifier, None, "p", value=MSG_RESULT_WORD_LABEL)
        _p.add_attribute("class", "coded-token")
        parent.append_child(_p)

        if len(entries) == 0:
            return

        _ul = HTMLNode(parent.identifier, None, "ul")
        parent.append_child(_ul)
        for entry in entries:
            _li = HTMLNode(_ul.identifier, None, "li",
                           value=f"{entry['word']} ({entry['pron']})")
            _ul.append_child(_li)
