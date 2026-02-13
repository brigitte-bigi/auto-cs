"""
:filename: sppas.ui.swapp.app_textcues.views.pathway_text_view.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: View of the "TextCueS" pathway "Input Lang & Text" page.

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

from ..textcues_msg import MSG_LANGTEXT_TITLE
from ..textcues_msg import MSG_LANGTEXT_BREADCRUMB
from ..textcues_msg import MSG_LANGTEXT_ANN_BUTTON
from ..textcues_msg import MSG_LANGTEXT_FIELD_LEGEND
from ..textcues_msg import MSG_SEE_ALSO
from ..textcues_msg import MSG_LANG
from ..textcues_msg import MSG_TEXT_LABEL
from ..textcues_msg import MSG_TEXT_HERE
from ..textcues_record import TextCueSRecord

from .nodes.tags import HTMLTag
from .pathway_base_view import PathwayBaseView

# ---------------------------------------------------------------------------


HTML_REFERENCE = """
    <h3>{:s}</h3>

    <blockquote>
            Brigitte Bigi (2014).
            <a class="external-link" href="http://link.springer.com/chapter/10.1007/978-3-319-08958-4_42">
                  A Multilingual Text Normalization Approach.
            </a>
            Human Language Technology. Challenges for Computer Science and Linguistics,
            LNAI 8387, pp. 515–526.
    </blockquote>
    <blockquote>
            Brigitte Bigi (2016).
            <a class="external-link" href="http://link.springer.com/chapter/10.1007%2F978-3-319-43808-5_30">
                  A phonetization approach for the forced-alignment task in SPPAS.
            </a>
            Human Language Technology. Challenges for Computer Science and Linguistics, 
            LNAI 9561, pp. 397-410.
    </blockquote>
""".format(MSG_SEE_ALSO)

# ---------------------------------------------------------------------------


class PathwayTextView(PathwayBaseView):

    def __init__(self, parent: HTMLNode, record: TextCueSRecord) -> None:
        """Create the view "Text" of the Pathway in "TextCueS".

        :param parent: (HTMLNode) The parent id of the HTML node
        :raises: KeyError: Missing 'lang_choices' in the given data

        """
        if "lang_choices" not in record.extras:
            raise KeyError("Missing 'lang_choices' in the given record "
                           "to PathwayTextView.__init__")

        super(PathwayTextView, self).__init__(parent, record)
        record.pathway = self.get_id()

    # -----------------------------------------------------------------------
    # PUBLIC METHODS
    # -----------------------------------------------------------------------

    @staticmethod
    def get_id() -> str:
        """Return the identifier of the view (str)."""
        return "pathway_text"

    @staticmethod
    def get_title() -> str:
        """Return the title of the view (str)."""
        return MSG_LANGTEXT_TITLE

    @staticmethod
    def get_msg() -> str:
        """Return the breadcrumb message of the view (str)."""
        return MSG_LANGTEXT_BREADCRUMB

    # -----------------------------------------------------------------------
    # PUBLIC METHOD -- construct the UI
    # -----------------------------------------------------------------------

    def create(self) -> None:
        """Create and append the children nodes.

        :raises: TypeError: The given pathway_msg is not a tuple.
        :raises: ValueError: The given pathway_msg is empty.
        :raises: ValueError: The current given 'id' must be in pathway_msg.
        :raises: TypeError: The given pathway_msg does not contain strings

        """
        _paths = self._pathway_msg_to_dict(self._record.extras['pathway_msg'], self.get_msg())

        # Section: main container
        _content = HTMLTag.create_section(self._parent, MSG_LANGTEXT_TITLE)

        # The tiles to indicate progress in the pathway
        self._create_tiles(_content, _paths, [None, None, None])

        # A fieldset with its legend
        _fieldset = self._append_fieldset(_content, MSG_LANGTEXT_FIELD_LEGEND)

        # A form for user inputs
        self._form = HTMLTag.create_form(_fieldset, "pathway_form")
        self._fill_form()

        # Any other Section container to be added below
        self._append_references()

    # -----------------------------------------------------------------------
    # Protected -- construct the UI
    # -----------------------------------------------------------------------

    def _fill_form(self) -> None:
        """Fill-in the inputs form.

        """
        # Hidden fields
        dictionarized = self._record.serialize()
        for item in dictionarized:
            if item not in ("lang", "text", "textnorm", "phonetize", "cuedspeech"):
                HTMLTag.append_hidden_input_in_form(self._form, item, dictionarized[item])

        # Choose language if more than one is available
        if len(self._record.extras["lang_choices"]) > 1:
            self._append_lang_choices()
        else:
            _p = HTMLNode(self._form.identifier, None, "p",
                          value=MSG_LANG + " " + self._record.extras["lang_choices"][0])

        # Input text
        self._append_input_textarea()

        # Submit button
        HTMLTag.append_submit_in_form(self._form, self.get_id(), MSG_LANGTEXT_ANN_BUTTON)

    # -----------------------------------------------------------------------

    def _append_lang_choices(self) -> None:
        """Append a select/options to the form.

        """
        label = HTMLNode(self._form.identifier, None, "label",
                         attributes={"for": "lang"},
                         value=MSG_LANG)
        self._form.append_child(label)

        select = HTMLNode(self._form.identifier, None, "select",
                          attributes={"id": "lang", "name": "lang", "class": "width-half"})
        self._form.append_child(select)

        for iso in self._record.extras["lang_choices"]:
            description = self._record.extras["lang_choices"][iso]
            option = HTMLNode(select.identifier, None, "option", value=description)
            option.set_attribute("value", iso)
            if iso == self._record.lang:
                option.set_attribute("selected", "")
            select.append_child(option)

    # -----------------------------------------------------------------------

    def _append_input_textarea(self) -> None:
        """Add a textarea to the form.

        """
        label = HTMLNode(self._form.identifier, None, "label",
                         attributes={"for": "text"},
                         value=MSG_TEXT_LABEL)
        self._form.append_child(label)

        att = dict()
        att["id"] = "text"
        att["name"] = "text"
        att["required"] = None
        att["class"] = "text-input width-full"
        att["placeholder"] = MSG_TEXT_HERE
        att["maxlength"] = "160"  # max nb of chars
        att["rows"] = "4"
        textarea = HTMLNode(self._form.identifier, None, "textarea", attributes=att)
        self._form.append_child(textarea)

        # the textarea content, if already existing.
        if self._record.text is not None:
            textarea.set_value(self._record.text)

    # -----------------------------------------------------------------------

    def _append_references(self) -> None:
        """Append a section with bibliographical references to the parent.

        """
        section = HTMLNode(self._parent.identifier, "references", "section",
                           value=HTML_REFERENCE)
        self._parent.append_child(section)

