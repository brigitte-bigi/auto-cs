"""
:filename: sppas.ui.swapp.app_textcues.views.nodes.button_action.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: A button node to perform an action

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

Shared with the other Auto-CS spin-off applications: the implementation
lives in `sppas.ui.swapp.app_cues_utils.nodes.button_action`.

"""

from sppas.ui.swapp.app_cues_utils.nodes.button_action import MenuLinkButtonNode
from sppas.ui.swapp.app_cues_utils.nodes.button_action import ActionLinkNode
from sppas.ui.swapp.app_cues_utils.nodes.button_action import ActionButton
from sppas.ui.swapp.app_cues_utils.nodes.button_action import ActionSubmitButton

__all__ = (
    "MenuLinkButtonNode",
    "ActionLinkNode",
    "ActionButton",
    "ActionSubmitButton"
)
