"""
:filename: sppas.ui.swpapp.textcues.views.nodes.footer.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: A footer node to display at the bottom of a page.

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

from whakerpy.htmlmaker.htmnodes.htmnode import TagNode
from sppas.ui.swapp.wappsg import wapp_settings

from ...textcues_msg import MSG_APP_TITLE
from ...textcues_msg import MSG_ACS_PROJECT

from .button_action import MenuLinkButtonNode

# -----------------------------------------------------------------------


class NavUtils:
    """Utility class to create HTML nodes for the menu.

    """

    @staticmethod
    def append_acs_link_button(parent: TagNode) -> None:
        """Create and append a link button redirecting to auto-cuedspeech.org.

        :param parent: (TagNode) Parent node

        """
        _acs = MenuLinkButtonNode(
            parent.identifier,
        "link-acs_button",
            "https://auto-cuedspeech.org/"
        )
        _acs.set_icon(None, wapp_settings.icons + "Refine/ACS_project.png")
        _acs.set_text(MSG_ACS_PROJECT)
        parent.append_child(_acs)

    # -----------------------------------------------------------------------

    @staticmethod
    def append_home_link_button(parent: TagNode) -> None:
        """Create and append a link button redirecting to welcome page.

        :param parent: (TagNode) Parent node

        """
        _acs = MenuLinkButtonNode(
            parent.identifier,
        "link-welcome_button",
            "textcues.html"
        )
        _acs.set_icon(None, wapp_settings.icons + "Refine/textcues.png")
        _acs.set_text(MSG_APP_TITLE)
        parent.append_child(_acs)

