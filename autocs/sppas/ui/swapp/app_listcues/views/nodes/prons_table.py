"""
:filename: sppas.ui.swapp.app_listcues.views.nodes.prons_table.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: HTMLNode to display the table of pronunciations and their words.

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

from ...listcues_msg import MSG_TABLE_COL_PRON
from ...listcues_msg import MSG_TABLE_COL_WORDS

# ---------------------------------------------------------------------------


class PronsTableNode(HTMLNode):
    """Manage the nodes for the table representing pronunciations and their words.

    """

    def __init__(self, parent_id: str, entries: tuple):
        """Create the HTML node for the table.

        :param parent_id: (str) The parent id of the HTML node
        :param entries: (tuple) See :class:`Keys2PronsModel.convert`

        """
        super(PronsTableNode, self).__init__(parent_id, "prons_table", "table")
        self.add_attribute("role", "grid")
        self.add_attribute("class", "sounds-table")

        self.__append_thead()
        self.__append_tbody(entries)

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

        self.__append_head_th(_head_tr, MSG_TABLE_COL_PRON, 40)
        self.__append_head_th(_head_tr, MSG_TABLE_COL_WORDS, 60)

    # -----------------------------------------------------------------------

    def __append_head_th(self, parent: HTMLNode, message: str, width: int) -> None:
        """Append a <th> element to the parent."""
        _th = HTMLNode(parent.identifier, None, "th", value=message)
        _th.add_attribute("scope", "col")
        _th.add_attribute("style", f"width:{width}%")
        parent.append_child(_th)

    # -----------------------------------------------------------------------

    def __append_tbody(self, entries: tuple) -> None:
        """Create one row per pronunciation, with its matching words.

        """
        _tbody = HTMLNode(self.identifier, None, "tbody")
        self.append_child(_tbody)

        for _index, _entry in enumerate(entries):
            _row = HTMLNode(_tbody.identifier, f"row-{_index}", "tr")
            _tbody.append_child(_row)

            _th = HTMLNode(_row.identifier, None, "th", value=_entry["pron"],
                           attributes={"scope": "row"})
            _row.append_child(_th)

            _td = HTMLNode(_row.identifier, None, "td", value=", ".join(_entry["words"]))
            _row.append_child(_td)
