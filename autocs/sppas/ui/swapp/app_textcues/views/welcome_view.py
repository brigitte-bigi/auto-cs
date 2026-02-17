"""
:filename: sppas.ui.swapp.app_textcues.views.welcome_view.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: View of the "TextCueS" welcome page.

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
from sppas.ui.swapp.wappsg import wapp_settings

from ..textcues_msg import MSG_YOYO_WELCOME
from ..textcues_msg import MSG_INTRO
from ..textcues_msg import MSG_LAUNCH
from ..textcues_msg import MSG_TEXTCUES_CONCEPT
from ..textcues_msg import MSG_SUPPORT
from ..textcues_msg import MSG_SEE_ALSO

from .nodes.yoyo_message import YoyoMessageNode
from .nodes.button_action import ActionLinkNode
from .nodes.tags import HTMLTag

# ---------------------------------------------------------------------------


class TextCueSWelcomeView:

    def __init__(self, parent: HTMLNode, btn_target_page: str):
        """Create the HTML node for the welcome page of "TextCueS".

        :param parent: (HTMLNode) The parent id of the HTML node
        :param btn_target_page: (str) The target page for the "launch" button

        """
        # section 1
        # ---------
        _part_1 = HTMLNode(parent.identifier,None,"section")
        _part_1.add_attribute("class", "flex-panel")
        parent.append_child(_part_1)

        # At left, the page content
        _left = HTMLNode(_part_1.identifier, None, "article")
        _left.add_attribute("class", "intro")
        _left.set_value(MSG_INTRO)
        _part_1.append_child(_left)

        # At right, the yoyo welcome message
        yoyo = YoyoMessageNode(_part_1.identifier, MSG_YOYO_WELCOME)
        yoyo.add_attribute("class", "width_20")
        _part_1.append_child(yoyo)

        # section 2
        # ---------
        _action = ActionLinkNode(parent.identifier, "pathway_welcome_button", HTMLTag.page_random())
        _action.set_icon(None, wapp_settings.images + "textcues/yoyo_1.png")
        _action.set_text(MSG_LAUNCH)
        parent.append_child(_action)

        # section 3
        # ---------
        _s = HTMLNode(parent.identifier, None, "section")
        parent.append_child(_s)

        _h3 = HTMLNode(_s.identifier, None, "h3", value=MSG_SEE_ALSO)
        _s.append_child(_h3)

        _p = HTMLNode(_s.identifier, None, "p", value=MSG_TEXTCUES_CONCEPT)
        _a = HTMLNode(_p.identifier, None, "a", value="PDF")
        _a.add_attribute("href", "https://hal.science/hal-5511364/")
        _a.add_attribute("class", "external-link")
        _p.append_child(_a)
        _s.append_child(_p)

        _p = HTMLNode(_s.identifier, None, "p", value=MSG_SUPPORT)
        _s.append_child(_p)

