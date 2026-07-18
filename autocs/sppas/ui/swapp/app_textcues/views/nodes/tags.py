"""
:filename: sppas.ui.swapp.app_textcues.views.nodes.tags.py
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

The generic building blocks (create_section, append_hidden_input_in_form,
append_submit_in_form) are shared with the other Auto-CS spin-off
applications and inherited from
`sppas.ui.swapp.app_cues_utils.nodes.tags.HTMLTag`. This subclass only adds
the TextCueS-specific pathway page navigation (a fresh page name per step
of the wizard).

"""

import secrets
from whakerpy.htmlmaker.htmnodes.htmnode import TagNode

from sppas.ui.swapp.app_cues_utils.nodes.tags import HTMLTag as _BaseHTMLTag

# ---------------------------------------------------------------------------


class HTMLTag(_BaseHTMLTag):
    """Utility class to create HTML nodes, with the TextCueS pathway extension.

    """

    @staticmethod
    def create_form(parent: TagNode, identifier: str) -> TagNode:
        """Create the form to be filled-in with the pathway page.

        :param parent: (TagNode) The parent of the form node
        :param identifier: (str) The identifier of the form node

        """
        _form = TagNode(parent.identifier, identifier, "form")
        _form.add_attribute("id", identifier)
        _form.add_attribute("method", "POST")
        if identifier.startswith("pathway"):
            _form.add_attribute("action", HTMLTag.page_random())
        parent.append_child(_form)
        return _form

    # -----------------------------------------------------------------------

    @staticmethod
    def page_random() -> str:
        return 'textcues_' + secrets.token_hex(16) + '.html'
