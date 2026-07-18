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

from ..textcues_msg import MSG_YOYO_WELCOME
from ..textcues_msg import MSG_INTRO
from ..textcues_msg import MSG_LAUNCH
from ..textcues_msg import MSG_LANG
from ..textcues_msg import MSG_TEXTCUES_CONCEPT
from ..textcues_msg import MSG_SUPPORT
from ..textcues_msg import MSG_SEE_ALSO
from ..textcues_record import TextCueSRecord

from .nodes.yoyo_message import YoyoMessageNode
from .nodes.tags import HTMLTag

# ---------------------------------------------------------------------------


class TextCueSWelcomeView:

    def __init__(self, parent: HTMLNode, record: TextCueSRecord):
        """Create the HTML node for the welcome page of "TextCueS".

        The language is chosen here, not on the "Text" pathway page: it is
        needed by the model, and the application is stateless, so it must
        travel with the navigation to the pathway content (a plain GET,
        exactly like the accessibility parameters already do).

        :param parent: (HTMLNode) The parent id of the HTML node
        :param record: (TextCueSRecord) The data to fill-in the language choices

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

        # section 2: language choice, then launch
        # -----------------------------------------
        # The form's identifier starts with "pathway": create_form() already
        # gives it a random action (see HTMLTag.page_random()) -- a bot can
        # reach the welcome page but can't guess this URL, so it never
        # triggers the expensive per-language processing directly.
        _form = HTMLTag.create_form(parent, "pathway_welcome_form")
        _form.set_attribute("method", "get")

        _label = HTMLNode(_form.identifier, None, "label",
                          attributes={"for": "lang"},
                          value=MSG_LANG)
        _form.append_child(_label)

        _select = HTMLNode(_form.identifier, None, "select",
                          attributes={"id": "lang", "name": "lang", "class": "width-half"})
        _form.append_child(_select)

        _lang_choices = record.extras.get("lang_choices", dict())
        for iso in _lang_choices:
            _description = _lang_choices[iso]
            _option = HTMLNode(_select.identifier, None, "option", value=_description)
            _option.set_attribute("value", iso)
            _select.append_child(_option)

        HTMLTag.append_submit_in_form(_form, "pathway_welcome", MSG_LAUNCH)

        # section 3
        # ---------
        _s = HTMLNode(parent.identifier, None, "section")
        parent.append_child(_s)

        _h3 = HTMLNode(_s.identifier, None, "h3", value=MSG_SEE_ALSO)
        _s.append_child(_h3)

        _p = HTMLNode(_s.identifier, None, "p", value=MSG_TEXTCUES_CONCEPT)
        _a = HTMLNode(_p.identifier, None, "a", value="PDF")
        _a.add_attribute("href", "https://hal.science/hal-05511364/")
        _a.add_attribute("class", "external-link")
        _p.append_child(_a)
        _s.append_child(_p)

        _p = HTMLNode(_s.identifier, None, "p", value=MSG_SUPPORT)
        _s.append_child(_p)

