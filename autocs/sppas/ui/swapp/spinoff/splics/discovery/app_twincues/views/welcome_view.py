"""
:filename: sppas.ui.swapp.spinoff.splics.discovery.app_twincues.views.welcome_view.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: View of the "TwinCueS" welcome page.

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

from ..twincues_msg import MSG_INTRO
from ..twincues_msg import MSG_LAUNCH
from ..twincues_msg import MSG_YOYO_WELCOME
from ..twincues_msg import MSG_LANG
from ..twincues_record import TwinCueSRecord

from sppas.ui.swapp.spinoff.splics.nodes.feedback.yoyo_message import BaseYoyoMessageNode
from sppas.ui.swapp.spinoff.splics.nodes.layout.tags import HTMLTag

# ---------------------------------------------------------------------------


class TwinCueSWelcomeView:

    def __init__(self, parent: HTMLNode, record: TwinCueSRecord):
        """Create the HTML node for the welcome page of "TwinCueS".

        The language is chosen here, not on the conversion page: it is
        needed to build the model's dictionary index, and the application
        is stateless, so it must travel with the navigation to the
        conversion content (a plain GET, exactly like the accessibility
        parameters already do).

        :param parent: (HTMLNode) The parent id of the HTML node
        :param record: (TwinCueSRecord) The data to fill-in the language choices

        """
        _lang_choices = record.extras.get("lang_choices", dict())

        # section 1: intro + yoyo message
        # -----------------------------------------
        _part_1 = HTMLNode(parent.identifier, None, "section")
        _part_1.add_attribute("class", "flex-panel")
        parent.append_child(_part_1)

        _intro = HTMLNode(_part_1.identifier, None, "article")
        _intro.add_attribute("class", "intro")
        _intro.set_value(MSG_INTRO)
        _part_1.append_child(_intro)

        _yoyo = BaseYoyoMessageNode.welcome(_part_1.identifier, MSG_YOYO_WELCOME,
                                            len(_lang_choices) > 0)
        _part_1.append_child(_yoyo)

        # section 2: language choice, then launch
        # -----------------------------------------
        _form = HTMLTag.create_form(parent, "twincues_welcome_form")
        _form.set_attribute("method", "get")
        # A random name: a bot can reach the welcome page but can't guess
        # this URL, so it never triggers the expensive per-language
        # processing directly.
        _form.set_attribute("action", HTMLTag.page_random("twincues"))

        if len(_lang_choices) > 0:
            _label = HTMLNode(_form.identifier, None, "label",
                              attributes={"for": "lang"},
                              value=MSG_LANG)
            _form.append_child(_label)

            _select = HTMLNode(_form.identifier, None, "select",
                              attributes={"id": "lang", "name": "lang", "class": "width-half"})
            _form.append_child(_select)

            for iso in _lang_choices:
                _description = _lang_choices[iso]
                _option = HTMLNode(_select.identifier, None, "option", value=_description)
                _option.set_attribute("value", iso)
                _select.append_child(_option)

        HTMLTag.append_submit_in_form(_form, "twincues_welcome", MSG_LAUNCH,
                                      enabled=len(_lang_choices) > 0)
