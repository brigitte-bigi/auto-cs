"""
:filename: sppas.ui.swapp.app_textcues.app_launcher.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Launcher for the web-based application "TextCueS" of Auto-CS.

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

import logging

from ..apps.swapp_response import swappBaseResponse
from ..htmltags.hstatusnode import HTMLTreeError410

from .textcues_view import TextCueSView

# -----------------------------------------------------------------------


class TextCueSLauncherRecipe(swappBaseResponse):
    """The textcues.html HTTPD response baker.

    This page displays an introductory message and allows to launch the
    TextCueS app.

    """

    def __init__(self, name="TextCueSWelcome", tree=None):
        self.__view = None
        super(TextCueSLauncherRecipe, self).__init__(name, tree)

    # -----------------------------------------------------------------------
    # STATIC METHODS
    # -----------------------------------------------------------------------

    @classmethod
    def page(cls) -> str:
        """Return a short description of the application.

        """
        return "textcues.html"

    # -----------------------------------------------------------------------

    def create(self) -> None:
        """Override. Create the fixed page content in HTML.

        The fixed content corresponds to the parts that can't be invalidated:
        head, body_header, body_footer.

        """
        super().create()
        self.__view = TextCueSView(self._htree, is_welcome=True)

    # -----------------------------------------------------------------------
    # Callbacks
    # -----------------------------------------------------------------------

    def _process_events(self, events: dict, **kwargs) -> bool:
        """Override. Process the given events coming from the POST of any form.

        :param events (dict): key=event_name, value=event_value
        :return: (bool) True if the whole page must be re-created.

        """
        logging.debug(f" >>>>> Page Application TextCueS -- Process events: {events} <<<<<< ")
        self._data = dict()
        self._status.code = 200

        # Accessibility events can be received in the same post
        if "accessibility_color" in events:
            self.__view.set_accessibility(color=events["accessibility_color"])
            return False

        if "accessibility_contrast" in events:
            self.__view.set_accessibility(contrast=events["accessibility_contrast"])
            return False

        return True

    # -----------------------------------------------------------------------

    def _bake(self) -> None:
        """Override. Create the dynamic page content in HTML.

        It replaces the current HTMLTree if status is 410 or update the
        content of the current HTMLTree.

        """
        self.comment("Body content")

        if self._status.code == 410:
            # The 410 is "Gone" response sent when the requested content has been
            # permanently deleted from server, with no forwarding address.
            self._htree = HTMLTreeError410()

        elif self._status.code == 200:
            # Fills-in the body_main node
            self.__view.populate_tree_content(record=None)

        else:
            msg = f"Unexpected status '{self._status.code}' while baking the page content."
            logging.error(msg)
            p = self._htree.element("p")
            p.set_value(msg)
