"""
:filename: sppas.ui.swapp.app_textcues.views.pathway_code_view.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: View of the "TextCueS" pathway "Code" page (result).

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
from whakerpy.htmlmaker.htmnodes.htmnode import TagNode
from whakerpy.htmlmaker import EmptyNode

from ..textcues_msg import MSG_CUES_TITLE
from ..textcues_msg import MSG_CUES_BREADCRUMB
from ..textcues_msg import MSG_BUTTON_BACK
from ..textcues_msg import MSG_SEE_ALSO
from ..textcues_msg import MSG_MODES
from ..textcues_msg import MSG_MODE_DISPLAY
from ..textcues_msg import MSG_POSITIONS
from ..textcues_msg import MSG_POSITION_MODEL
from ..textcues_msg import MSG_ANGLES
from ..textcues_msg import MSG_ANGLE_MODEL
from ..textcues_msg import MSG_TIMINGS
from ..textcues_msg import MSG_TIMING_MODEL
from ..textcues_msg import MSG_BUTTON_APPLY
from ..textcues_msg import MSG_RESULT
from ..textcues_record import TextCueSRecord

from .nodes.tags import HTMLTag
from .nodes.cuedcode import CuedCode
from .pathway_base_view import PathwayBaseView

# ---------------------------------------------------------------------------

HTML_REFERENCE = """
    <h3>{:s}</h3>

    <blockquote>
        <p>
            Maroula S. Bratakos, Paul Duchnowski and Louis D. Braida (1998).
            <a class="external-link" href="https://cuedspeech.org/wp-content/uploads/2023/10/CS_Journal_Vol6_Toward_Automatic_Generation_of_Cued_Speech.pdf">
            Toward the Automatic Generation of Cued Speech.</a>
            Cued Speech Journal VI 1998 p1-37.
        </p>
    </blockquote>
    
    <blockquote>
        <p>
            Paul Duchnowski, Louis D. Braida, David S. Lum, Matthew G. Sexton, Jean C. Krause, Smriti Banthia (1998).
            <a class="external-link" href="https://www.isca-archive.org/avsp_1998/duchnowski98_avsp.pdf">AUTOMATIC GENERATION OF CUED SPEECH FOR THE DEAF: STATUS AND OUTLOOK</a>
        </p>    
    </blockquote>
    
    <blockquote>
        <p>
            Paul Duchnowski, Louis D. Braida, Maroula Bratakos, David S. Lum, Matthew G. Sexton, Jean C. Krause. (1998)
            <a class="external-link" href="https://www.isca-archive.org/icslp_1998/duchnowski98_icslp.pdf">A SPEECHREADING AID BASED ON PHONETIC ASR</a>
        </p>
    </blockquote>
    
    <blockquote>
        <p>
            Paul Duchnowski, David S. Lum, Jean C. Krause, Matthew G. Sexton,
            Maroula S. Bratakos, and Louis D. Braida (2000).
            Development of Speechreading Supplements Based in Automatic Speech Recognition.
            IEEE Transactions on Biomedical Engineering, vol. 47, no. 4, pp. 487-496. doi: 10.1109/10.828148.
        </p>
    </blockquote>
    
    <blockquote>
        <p>
            Virginie Attina Dubesset (2005).
            <a class="external-link" href="https://tel.archives-ouvertes.fr/file/index/docid/384080/filename/these_attina.pdf">La langue française parlée complétée (LPC) : production et perception.</a>
            PhD Thesis of INPG Grenoble, France.
        </p>
    </blockquote>
""".format(MSG_SEE_ALSO)

# ---------------------------------------------------------------------------


class PathwayCodeView(PathwayBaseView):

    def __init__(self, parent: HTMLNode, record: TextCueSRecord) -> None:
        """Create the HTML node for the pathway "lang&text" page of "TextCueS".

        :param parent: (HTMLNode) The parent id of the HTML node

        """
        if record.mode is None:
            record.mode = 0
        super(PathwayCodeView, self).__init__(parent, record)
        record.pathway = self.get_id()

    # -----------------------------------------------------------------------
    # PUBLIC METHODS
    # -----------------------------------------------------------------------

    @staticmethod
    def get_id() -> str:
        """Return the identifier of the view (str)."""
        return "pathway_code"

    @staticmethod
    def get_title() -> str:
        """Return the title of the view (str)."""
        return MSG_CUES_TITLE

    @staticmethod
    def get_msg() -> str:
        """Return the breadcrumb message of the view (str)."""
        return MSG_CUES_BREADCRUMB

    # -----------------------------------------------------------------------
    # PUBLIC METHODS -- construct the UI
    # -----------------------------------------------------------------------

    def display_content(self) -> TagNode:
        """Create and fills-in the node of the cued keys.

        :return: (TagNode) The container HTML node

        """
        _s = self.__create_display_container()
        _view = CuedCode(self._record)

        if self._record.mode == 1:
            _view.overlay_mode_content_nodes(_s)

        elif self._record.mode == 2:
            _view.video_mode_content_nodes(_s)

        else:
            _view.images_mode_content_nodes(_s)

        return _s

    # -----------------------------------------------------------------------

    def create(self) -> None:
        """Create and append the children nodes.

        :raises: TypeError: The given pathway_msg is not a tuple.
        :raises: ValueError: The given pathway_msg is empty.
        :raises: ValueError: The current given 'id' must be in pathway_msg.
        :raises: TypeError: The given pathway_msg does not contain strings

        """
        _paths = self._pathway_msg_to_dict( self._record.extras['pathway_msg'], self.get_msg())

        # Section: main container
        _container = HTMLTag.create_section(self._parent, MSG_CUES_TITLE)

        # The tiles to indicate progress in the pathway
        self._create_tiles(_container, _paths, [self._record.textnorm, self._record.phonetize, self._record.cuedkeys])

        # Create and fills-in the fieldset with user inputs
        # _fieldset = self._append_fieldset(_container, MSG_CUES_FIELD_LEGEND)
        # self._fills_in_inputs(_fieldset)

        # The coded sequence
        _h3 = HTMLNode(self._parent.identifier, None, "section", value="<h3>" + MSG_RESULT + "</h3>")
        self._parent.append_child(_h3)

        # The container, and its content, for the visual display of the coded sequence
        self.display_content()

        # Redirect
        self._form = HTMLTag.create_form(self._parent, "pathway_form")
        self._fill_form()

        # Any content to be added below the form
        self._append_references()

    # -----------------------------------------------------------------------
    # PROTECTED METHODS -- construct the UI
    # -----------------------------------------------------------------------

    def _fills_in_inputs(self, parent: TagNode) -> None:
        """Create and fill in the content of a fieldset to fix user inputs.

        :param parent: (HTMLNode) The parent id of the HTML node

        """
        _f = HTMLTag.create_form(parent, "options_form")

        # Hidden fields
        # -------------
        dictionarized =  self._record.serialize()
        for item in dictionarized:
            HTMLTag.append_hidden_input_in_form(_f, item, dictionarized[item])

        # Form: display mode
        # --------------------
        _p = HTMLNode(_f.identifier, None, "p", value=MSG_MODE_DISPLAY)
        _f.append_child(_p)
        _container = TagNode(_f.identifier, None, "div")
        _container.add_attribute("class", "wexa-toggle-group")
        _f.append_child(_container)
        for _i, _msg in enumerate(MSG_MODES):
            _label = HTMLNode(_container.identifier, None, "label")
            _label.add_attribute("class", "wexa-toggle")
            _container.append_child(_label)

            _input = EmptyNode(_label.identifier, None, "input")
            _input.add_attribute("id", f"displaymode_{_i}_input")
            _input.add_attribute("name", f"displaymode_input")
            _input.add_attribute("type", "radio")
            _input.add_attribute("value", str(_i))
            if _i == self._record.mode:
                _input.add_attribute("checked", None)
            _label.append_child(_input)

            _span = HTMLNode(_label.identifier, None, "span", value=_msg)
            _label.append_child(_span)

        # Form: Models
        # --------------
        # The models to display the code
        self.__create_options(_f, "position", MSG_POSITION_MODEL, MSG_POSITIONS)
        self.__create_options(_f, "angle", MSG_ANGLE_MODEL, MSG_ANGLES)
        self.__create_options(_f, "timing", MSG_TIMING_MODEL, MSG_TIMINGS)

        HTMLTag.append_submit_in_form(_f, "options_code", MSG_BUTTON_APPLY)

    # -----------------------------------------------------------------------

    def _fill_form(self) -> None:
        """Fill-in the redirection form.

        """
        # Hidden fields
        dictionarized = self._record.serialize()
        for item in dictionarized:
            if item not in ("text", "textnorm", "textprons", "phonetize", "cuedkeys", "cuedphons"):
                HTMLTag.append_hidden_input_in_form(self._form, item, dictionarized[item])

        # Submit button
        HTMLTag.append_submit_in_form(self._form, self.get_id(), MSG_BUTTON_BACK)

    # -----------------------------------------------------------------------

    def _append_references(self) -> None:
        """Append a section with bibliographical references to the parent.

        """
        section = HTMLNode(
            self._parent.identifier, "references", "section",
            value=HTML_REFERENCE
        )
        self._parent.append_child(section)

    # -----------------------------------------------------------------------
    # Create nodes
    # -----------------------------------------------------------------------

    @staticmethod
    def __create_options(parent: TagNode, model_key: str, msg_label:str, msg_options: str, selected: int = 0) -> None:
        """Create the options to choose the model of position for the face.

        :param parent: (TagNode) Parent node
        :param model_key: (str) The key of the model to choose (position, angle or timing).
        :param msg_label: (str) The text of the mail label.
        :param msg_options: (str) The text of the options.
        :param selected: (int) The index of the selected option.

        """
        _label = HTMLNode(parent.identifier, None, "label", value=msg_label)
        _label.add_attribute("for", f"select_{model_key}_model")
        parent.append_child(_label)

        _select = HTMLNode(parent.identifier, None, "select")
        _select.add_attribute("id", f"select_{model_key}_model")
        parent.append_child(_select)

        # Append the options (model choice) to the select element
        for _i, _msg in enumerate(msg_options):
            _opt = HTMLNode(_select.identifier, None, "option", value=_msg)
            _opt.add_attribute("value", str(_i))
            _opt.add_attribute("name", f"model_{model_key}_{_i}_option")
            if selected == _i:
                _opt.add_attribute("selected", None)

            _select.append_child(_opt)

    # -----------------------------------------------------------------------

    def __create_display_container(self):
        _s = HTMLTag.create_section(self._parent)
        _s.add_attribute("id", "displaymode_section")
        return _s
