"""
:filename: sppas.ui.swapp.app_textcues.views.pathway_base_view.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Base class for Pathway Views of "TextCueS" app.

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

from whakerpy.htmlmaker import HTMLNode
from whakerpy.htmlmaker.htmnodes.htmnode import TagNode

from ..textcues_record import TextCueSRecord

# ---------------------------------------------------------------------------


class PathwayBaseView:
    """Base class representing a step in the TextCueS pathway.

    """

    def __init__(self, parent: HTMLNode, record: TextCueSRecord) -> None:
        """Create a view of the Pathway in "TextCueS".

        :param parent: (HTMLNode) The parent id of the HTML node
        :raises: TypeError: The given parent is not a HTMLNode
        :raises: TypeError: The given record is not a TextCueSRecord.
        :raises: KeyError: The given record has no "pathway_msg" in extras.

        """
        if isinstance(parent, HTMLNode) is False:
            raise TypeError("The parent of PathwayBaseView arg must be a HTMLNode."
                            "Got {} instead.".format(type(parent)))
        if isinstance(record, TextCueSRecord) is False:
            raise TypeError("The record of PathwayBaseView arg must be a TextCueSRecord."
                            "Got {} instead.".format(type(record)))
        if "pathway_msg" not in record.extras:
            raise KeyError("Missing 'pathway_msg' in the given record "
                           "to PathwayBaseView.__init__")

        self._parent = parent
        self._form = None
        self._record = record

    # -----------------------------------------------------------------------
    # PUBLIC METHODS
    # -----------------------------------------------------------------------

    @staticmethod
    def get_id() -> str:
        """Return the identifier of the view (str)."""
        raise NotImplementedError

    @staticmethod
    def get_title() -> str:
        """Return the title of the view (str)."""
        raise NotImplementedError

    @staticmethod
    def get_msg() -> str:
        """Return the breadcrumb message of the view (str)."""
        raise NotImplementedError

    # -----------------------------------------------------------------------

    def create(self) -> None:
        """Create and append the children nodes of the view.

        :raises: TypeError: The given pathway_msg is not a tuple.
        :raises: ValueError: The given pathway_msg is empty.
        :raises: TypeError: The given pathway_msg does not contain strings

        """
        raise NotImplementedError

    # -----------------------------------------------------------------------
    # PRIVATE -- Utilities for inherited class.
    # -----------------------------------------------------------------------

    @staticmethod
    def _create_tiles(parent: TagNode, items: dict, contents: list) -> None:
        """Return a list node with given items.

        :param parent: (TagNode) The parent of the HTML node
        :param items: (dict) The item's dict. key=message, value is in ("visited", "active" or any)
        :param contents: (list) The content's list.
        :return: (HTMLNode) The tilesWrap list node with given li elements for items.

        """
        _ul = TagNode(
            parent.identifier,
            "tiles_ul",
            "ul",
            attributes={"class": "flex-panel tilesWrap"}
        )
        parent.append_child(_ul)
        if len(items) == len(contents):

            for _i, text in enumerate(items):
                _li = HTMLNode(_ul.identifier, f"tiles_{_i+1}_li", "li")
                _ul.append_child(_li)
                if items[text] in ("visited", "active"):
                    _li.set_attribute("class", items[text])

                # Step number -- aria-hidden
                _span = HTMLNode(_li.identifier, None, "span", value=f"{_i + 1}")
                _span.add_attribute("class", "tile-step-nb")
                # _span.add_attribute("aria-hidden", "true")
                _li.append_child(_span)

                # Step name
                _span = HTMLNode(_li.identifier, None, "span", value=text)
                _span.add_attribute("class", "tile-step-name")
                _li.append_child(_span)

                # Step content
                if contents[_i] is not None:
                    _p = HTMLNode(
                        _li.identifier, None, "p",
                        value=" ".join(contents[_i])
                    )
                    _li.append_child(_p)

    # -----------------------------------------------------------------------

    @staticmethod
    def _append_fieldset(parent: TagNode, legend: str) -> TagNode:
        """Append a fieldset to the parent with the given message as legend.

        :param parent: (TagNode) The parent of the fieldset node
        :param legend: (str) The legend of the fieldset
        :return: (TagNode) The fieldset node

        """
        _fieldset = TagNode(
            parent.identifier,
            "wizard_fieldset",
            "fieldset",
            attributes={"class": "wizard-fieldset"}
        )
        parent.append_child(_fieldset)

        _node = HTMLNode(
            _fieldset.identifier, None, "legend",
            value=legend
        )
        _fieldset.append_child(_node)
        return _fieldset

    # -----------------------------------------------------------------------

    @staticmethod
    def _pathway_msg_to_dict(pathway_msg: tuple, current_id: str) -> dict:
        """Fix the list of view message for the tiles the pathway is made of.

        The pathway ids are required to fill in the tree with a tilesWrap.

        :param pathway_msg: (tuple) The list of each view tile messages.
        :param current_id: (str) The current pathway id.
        :raises: TypeError: The given pathway_msg is not a tuple.
        :raises: ValueError: The given pathway_msg is empty.
        :raises: ValueError: The current given 'id' must be in pathway_msg.
        :raises: TypeError: The given pathway_msg does not contain strings
        :return: (dict) pathway_msg with value in ("visited", "active" or "")

        """
        if isinstance(pathway_msg, (list, tuple)) is False:
            raise TypeError("The pathway_msg arg must be a list or tuple.")
        if len(pathway_msg) == 0:
            raise ValueError("The pathway_msg arg must not be empty.")
        if current_id not in pathway_msg:
            raise ValueError("The current given 'id' must be in pathway_msg.")

        _paths = dict()
        active = False
        for item in pathway_msg:
            if isinstance(item, str) is False:
                raise TypeError("The pathway_msg items must be string.")
            if item == current_id:
                active = True
                _paths[item] = "active"
            else:
                if active is False:
                    _paths[item] = "visited"
                else:
                    _paths[item] = ""

        return _paths
