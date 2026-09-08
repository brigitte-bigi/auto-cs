"""
:filename: sppas.ui.swapp.spinoff.splics.nodes.buttons.button_action.py
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

"""

from whakerpy.htmlmaker import HTMLNode
from whakerpy.htmlmaker import EmptyNode

# ---------------------------------------------------------------------------


class MenuLinkButtonNode(HTMLNode):

    def __init__(self, parent_id, identifier: str, target_page: str):
        """Create a menu button to redirect to target page.

        """
        super(MenuLinkButtonNode, self).__init__(parent_id, identifier, "button")
        self.add_attribute("id", identifier)
        self.add_attribute("name", identifier)
        self.add_attribute("type", "button")
        if len(target_page.strip()) > 0:
            self.add_attribute("data-href", target_page)
        self.add_attribute("class", "menuitem")

    def set_text(self, text):
        if len(text.strip()) > 0:
            _text = HTMLNode(self.identifier, None, "span", value=text)
            self.append_child(_text)

    def set_icon(self, identifier, full_path):
        _img = EmptyNode(self.identifier, identifier, "img")
        _img.set_attribute('src', full_path)
        _img.set_attribute('alt', "")
        self.append_child(_img)
        return _img

    def set_named_icon(self, icon_name: str, text: str) -> None:
        """Ask for an icon by its name, and write the text of the button.

        The name is written on the button itself, which already carries the
        meaning: the loader of Whakerexa writes the drawing before the text
        once the icon sets are declared, and it takes the colour of what
        surrounds it in every mode and every theme (see icon_demand.js).

        :param icon_name: (str) Name of an icon of a declared set.
        :param text: (str) The button text.

        """
        self.add_attribute("data-icon", icon_name)
        self.set_text(text)

# ---------------------------------------------------------------------------


class ActionLinkNode(HTMLNode):
    """Represent a link element to perform an action."""

    def __init__(self, parent_id, identifier: str, target_page: str):
        """Create a button to redirect to target page.

        """
        super(ActionLinkNode, self).__init__(parent_id, identifier, "a")
        self.add_attribute('id', identifier)
        if len(target_page.strip()) > 0:
            self.add_attribute('href', target_page)
        self.add_attribute('role', "button")
        self.add_attribute('class', "app-cues-button")

    def set_text(self, text):
        if len(text.strip()) > 0:
            _text = HTMLNode(self.identifier, None, "span", value=text)
            self.append_child(_text)

    def set_icon(self, identifier, full_path):
        _img = EmptyNode(self.identifier, identifier, "img")
        _img.set_attribute('src', full_path)
        _img.set_attribute('alt', "")
        self.append_child(_img)
        return _img

# ---------------------------------------------------------------------------


class ActionButton(HTMLNode):
    """Represent a button element to perform an action."""

    def __init__(self, parent_id: str, identifier: str):
        """Create a button to redirect to target page.

        """
        super(ActionButton, self).__init__(parent_id, identifier, "button")
        self.add_attribute('id', identifier)
        self.add_attribute('class', "app-cues-button")

    def set_text(self, text):
        if len(text.strip()) > 0:
            _text = HTMLNode(self.identifier, None, "span", value=text)
            self.append_child(_text)

    def set_icon(self, identifier, full_path):
        _img = EmptyNode(self.identifier, identifier, "img")
        _img.set_attribute('src', full_path)
        _img.set_attribute('alt', "")
        self.append_child(_img)
        return _img

# ---------------------------------------------------------------------------


class ActionSubmitButton(ActionButton):
    """Represent a submit element to submit a form."""
    def __init__(self, parent_id: str, identifier: str):
        super(ActionSubmitButton, self).__init__(parent_id, identifier)
        self.add_attribute('type', "submit")
