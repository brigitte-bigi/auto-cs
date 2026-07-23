"""
:filename: sppas.ui.swapp.spinoff.splics.nodes.layout.tags.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Create and/or fill nodes for HTMLTags

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

import secrets

from whakerpy.htmlmaker.emptynodes import EmptyNode
from whakerpy.htmlmaker.htmnodes.htmnode import TagNode
from whakerpy.htmlmaker.htmnodes.htmnode import HTMLNode

from sppas.ui.swapp.spinoff.splics.splicssg import splics_paths

from ..buttons.button_action import ActionSubmitButton
from ..feedback.yoyo_message import YoyoMessageNode
from ..feedback.yoyo_message import YoyoErrorNode
from ..feedback.yoyo_message import MSG_NO_LANG

# ---------------------------------------------------------------------------


class HTMLTag:
    """Utility class to create HTML nodes.

    """

    @staticmethod
    def create_section(parent: TagNode, h3_title: str = "") -> TagNode:
        """Create a 'section' container and append the given message as 'h3'.

        :param parent: (HTMLNode|None) The parent of the HTML node
        :param h3_title: (str) Optional section title
        :return: (TagNode) The section container

        """
        if parent is None:
            _s = TagNode(None, None, "section")
        else:
            _s = TagNode(parent.identifier, None, "section")
            parent.append_child(_s)

        if len(h3_title) > 0:
            _h3 = HTMLNode(_s.identifier, None, "h3", value=h3_title)
            _s.append_child(_h3)

        return _s

    # -----------------------------------------------------------------------

    @staticmethod
    def create_form(parent: TagNode, identifier: str) -> TagNode:
        """Create a form node.

        :param parent: (TagNode) The parent of the form node
        :param identifier: (str) The identifier of the form node

        """
        _form = TagNode(parent.identifier, identifier, "form")
        _form.add_attribute("id", identifier)
        _form.add_attribute("method", "POST")
        parent.append_child(_form)
        return _form

    # -----------------------------------------------------------------------

    @staticmethod
    def page_random(prefix: str) -> str:
        """Return a random page name, "<prefix>_<32 hex chars>.html".

        Same convention as TextCueS's own pathway pages (see
        app_textcues.views.nodes.tags.HTMLTag.page_random()): a bot can't
        guess this URL, so it can only reach the (cheap) welcome page and
        never trigger the expensive per-language processing directly.

        :param prefix: (str) Application prefix, e.g. "listcues".
        :return: (str) The random page name.

        """
        return prefix + '_' + secrets.token_hex(16) + '.html'

    # -----------------------------------------------------------------------

    @staticmethod
    def append_hidden_input_in_form(form: TagNode, name: str, value: str) -> None:
        """Indicate a value in a hidden input of the form.

        :param form: (TagNode) The form to fill in with a hidden input
        :param name: (str) The name of the hidden input of the form.
        :param value: (str) The value of the hidden input of the form.

        """
        _node = EmptyNode(
            form.identifier, None, "input",
            attributes={"name": name, "type": "hidden", "value": value}
        )
        form.append_child(_node)

    # -----------------------------------------------------------------------

    @staticmethod
    def append_submit_in_form(form: TagNode, identifier: str, message: str,
                              enabled: bool = True) -> None:
        """Append the action button to the form.

        :param form: (TagNode) The form to fill in with a submit button
        :param identifier: (str) The identifier of the submit button
        :param message: (str) The button message.
        :param enabled: (bool) Allow the user to submit the form.

        """
        _btn = ActionSubmitButton(
            form.identifier,
            identifier + "_action_btn"
        )
        _btn.set_icon(None, splics_paths.images + "textcues/yoyo_1.png")
        _btn.set_text(message)
        if enabled is False:
            _btn.set_attribute("disabled", "disabled")
        form.append_child(_btn)
