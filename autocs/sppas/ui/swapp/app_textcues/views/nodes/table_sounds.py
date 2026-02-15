"""
:filename: sppas.ui.app_textcues.views.nodes.table_sounds.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: HTMLNode to display the table with pronunciations of tokens.

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
from sppas.core.config import separators
from whakerpy.htmlmaker import HTMLNode
from whakerpy.htmlmaker import EmptyNode

from ...textcues_msg import MSG_TOKENS
from ...textcues_msg import MSG_CHOICE_1
from ...textcues_msg import MSG_CHOICE_2
from ...textcues_msg import MSG_CHOICE_3
from ...textcues_msg import MSG_CHOICE_4
from ...textcues_msg import MSG_PERSONALIZED

# ---------------------------------------------------------------------------


class SoundsTableNode(HTMLNode):
    """Manage the nodes for the table representing word pronunciation variants.

    """

    def __init__(self, parent_id: str, sounds: list):
        """Create the HTML node for the table.

        :param parent_id: (str) The parent id of the HTML node
        :param sounds: (list) List of tokens with their pronunciation variants

        """
        super(SoundsTableNode, self).__init__(parent_id, "sounds_table", "table")
        self.add_attribute("role", "grid")
        self.add_attribute("class", "sounds-table")

        self.__append_thead()
        self.__append_tbody(sounds)

    # -----------------------------------------------------------------------
    # PRIVATE: construct the nodes
    # -----------------------------------------------------------------------

    def __append_thead(self) -> None:
        """Create and append the node representing <thead> element.

        """
        _thead = HTMLNode(self.identifier, None, "thead")
        self.append_child(_thead)
        _head_tr = HTMLNode(_thead.identifier, None, "tr")
        _thead.append_child(_head_tr)

        self.__append_head_th(_head_tr, MSG_TOKENS, 15)
        self.__append_head_th(_head_tr, MSG_CHOICE_1, 10)
        self.__append_head_th(_head_tr, MSG_CHOICE_2, 10)
        self.__append_head_th(_head_tr, MSG_CHOICE_3, 10)
        self.__append_head_th(_head_tr, MSG_CHOICE_4, 10)
        self.__append_head_th(_head_tr, MSG_PERSONALIZED, 10)

    # -----------------------------------------------------------------------

    def __append_head_th(self, parent: HTMLNode, message: str, width: int):
        """Append a <th> element to the parent."""
        _th = HTMLNode(parent.identifier, None, "th", value=message)
        _th.add_attribute("scope", "col")
        _th.add_attribute("style", f"width:{width}%")
        parent.append_child(_th)

    # -----------------------------------------------------------------------

    def __append_tbody(self, sounds: list) -> None:
        """Create rows for each token and fill cells with pronunciations.

        """
        _tbody = HTMLNode(self.identifier, None, "tbody")
        self.append_child(_tbody)

        for index, element in enumerate(sounds):
            if len(element) < 2:
                return

            # get token and phonemes list
            token = element[0]
            phonemes = element[1].split(separators.variants)

            # create row and first&second column
            current_row = HTMLNode(_tbody.identifier, f"row-{token}", "tr")
            _tbody.append_child(current_row)

            current_token = HTMLNode(
                current_row.identifier, None, "th",
                value=token,
                attributes={'scope': 'row'}
            )
            current_row.append_child(current_token)

            # Append phonemes cell.
            # The default selected variant is the first shortest one.
            self.__create_phon_cells(current_row, index, token, phonemes)

            # Create phon input
            _td = HTMLNode(current_row.identifier, None, "td")
            _input = EmptyNode(_td.identifier, None, "input")
            _input.add_attribute('id', f"{index}-sound_input")
            _input.add_attribute('name', f"{index}-sound_input")
            _input.add_attribute('class', "sound_input")

            current_row.append_child(_td)
            _td.append_child(_input)

    # ---------------------------------------------------------------------------

    @staticmethod
    def __create_phon_cells(row: HTMLNode, token_index: int, token: str, phonemes: list,
                            chosen: int = 0) -> None:
        """Create the cells for the phon table.

        :param row: (HTMLNode) Row of phons.
        :param token_index: (int) Token index.
        :param token: (str) CuedSpeech token.
        :param phonemes: (list) List of phonemes.
        :param chosen: (int) Index of chosen phon.

        """
        # Sort phonemes: from shortest to longest
        sorted_phonemes = sorted(phonemes, key=lambda s: len(s.split('-')))

        # Create 4 cells for a current row
        for i in range(4):
            phon_cell = HTMLNode(row.identifier, None, "td")
            row.append_child(phon_cell)

            if len(sorted_phonemes) >= i + 1:
                phon_btn = HTMLNode(phon_cell.identifier, None, "button",
                                    value=sorted_phonemes[i])
                phon_btn.set_attribute('name', f"{token_index}-sound_button")
                phon_btn.set_attribute("class", f"pron")
                if chosen == i:
                    phon_btn.set_attribute("aria-pressed", "true")
                else:
                    phon_btn.set_attribute("aria-pressed", "false")

                phon_cell.append_child(phon_btn)

