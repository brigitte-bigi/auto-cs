"""
:filename: sppas.ui.swapp.app_textcues.views.pathway_sound_view.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: View of the "TextCueS" pathway "Pronunciation" page.

..
    This file is part of AutoCS: <https://autocs.sourceforge.io>
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

from ..textcues_msg import MSG_PHON_TITLE
from ..textcues_msg import MSG_PHON_BREADCRUMB
from ..textcues_msg import MSG_PHON_FIELD_LEGEND
from ..textcues_msg import MSG_PHON_ANN_BUTTON
from ..textcues_msg import MSG_SEE_ALSO
from ..textcues_msg import MSG_ERROR_NO_RESULT
from ..textcues_record import TextCueSRecord

from .nodes.tags import HTMLTag
from .pathway_base_view import PathwayBaseView
from .nodes.table_sounds import SoundsTableNode

# ---------------------------------------------------------------------------


HTML_REFERENCE = """
        <h3>{:s}</h3>

        <blockquote>
            <p>
                Brigitte Bigi (2023).
                <a class="external-link" href="https://hal.science/hal-04081282">
                An analysis of produced versus predicted French Cued Speech keys.
                </a>
                In 10th Language & Technology Conference: Human Language Technologies
                as a Challenge for Computer Science and Linguistics,
                ISBN: 978-83-232-4176-8, pp. 24-28, Poznań, Poland.
            </p>
        </blockquote>
        
        <blockquote>
            <p>
                Núria Gala, Brigitte Bigi, Marie Bauer (2024).
                <a class="external-link" href="https://hal.science/hal-04580180">
                Automatically Estimating Textual and Phonemic Complexity for Cued Speech:
                How to See the Sounds from French Texts</a>
                In the 2024 Joint International Conference on Computational Linguistics,
                Language Resources and Evaluation (LREC-COLING), pp. 1817-1824, Turin, Italy.</a>
            </p>
        </blockquote>
""".format(MSG_SEE_ALSO)

# ---------------------------------------------------------------------------


class PathwaySoundView(PathwayBaseView):

    def __init__(self, parent: HTMLNode, record: TextCueSRecord) -> None:
        """Create the HTML node for the pathway "sound" page of "TextCueS".

        :param parent: (HTMLNode) The parent id of the HTML node

        """
        super(PathwaySoundView, self).__init__(parent, record)
        record.pathway = self.get_id()

    # -----------------------------------------------------------------------
    # PUBLIC METHODS
    # -----------------------------------------------------------------------

    @staticmethod
    def get_id() -> str:
        """Return the identifier of the view (str)."""
        return "pathway_sound"

    @staticmethod
    def get_title() -> str:
        """Return the title of the view (str)."""
        return MSG_PHON_TITLE

    @staticmethod
    def get_msg() -> str:
        """Return the breadcrumb message of the view (str)."""
        return MSG_PHON_BREADCRUMB

    # -----------------------------------------------------------------------
    # PUBLIC METHOD -- construct the UI
    # -----------------------------------------------------------------------

    def extract_sounds_from_data(self) -> list:
        """Return the sounds extracted from the data.

        """
        _sounds = list()
        for token, phonetization in zip( self._record.textnorm,  self._record.textprons):
            _sounds.append((token, phonetization))
        return _sounds

    # -----------------------------------------------------------------------
    # Protected -- construct the UI
    # -----------------------------------------------------------------------

    def create(self) -> None:
        """Create and append the children nodes.

        :raises: TypeError: The given pathway_msg is not a tuple.
        :raises: ValueError: The given pathway_msg is empty.
        :raises: ValueError: The current given 'id' must be in pathway_msg.
        :raises: TypeError: The given pathway_msg does not contain strings

        """
        _paths = self._pathway_msg_to_dict( self._record.extras["pathway_msg"], self.get_msg())

        # Section: main container
        _content = HTMLTag.create_section(self._parent, MSG_PHON_TITLE)

        # The tiles to indicate progress in the pathway
        self._create_tiles(_content, _paths, [self._record.textnorm, None, None])

        # A fieldset with its legend
        _fieldset = self._append_fieldset(_content, MSG_PHON_FIELD_LEGEND)

        # A form for user inputs
        self._form = HTMLTag.create_form(_fieldset, "pathway_form")
        self._fill_form()

        # Any other Section container to be added below
        self._append_references()

    # -----------------------------------------------------------------------

    def _fill_form(self) -> None:
        """Fill-in the redirection form.

        """
        # Hidden fields
        dictionarized =  self._record.serialize()
        for item in dictionarized:
            if item not in ("phonetize", "cuedkeys", "cuedphons"):
                HTMLTag.append_hidden_input_in_form(self._form, item, dictionarized[item])

        # The pronunciations table
        if self._record.textnorm is None or self._record.textprons is None:
            _p = HTMLNode(self._form.identifier, None, "p", value=MSG_ERROR_NO_RESULT)
            self._form.append_child(_p)
        else:
            _sounds = self.extract_sounds_from_data()
            _table = SoundsTableNode(self._form.identifier, _sounds)
            self._form.append_child(_table)

        # Submit button
        HTMLTag.append_submit_in_form(self._form, self.get_id(), MSG_PHON_ANN_BUTTON)

    # -----------------------------------------------------------------------

    def _append_references(self) -> None:
        """Append a section with bibliographical references to the parent.

        """
        section = HTMLNode(
            self._parent.identifier, "references", "section",
            value=HTML_REFERENCE
        )
        self._parent.append_child(section)

