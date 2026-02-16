"""
:filename: sppas.ui.swapp.app_textcues.app_textcues.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Bakery for the web-based application "TextCueS".

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
import logging

from whakerpy.httpd import BaseResponseRecipe
from sppas.ui.swapp import sppasImagesAccess
from sppas.ui.swapp.apps.swapp_bakery import swappWebData

from .textcuesmaker import TextCueSResponseRecipe
from .app_launcher import TextCueSLauncherRecipe
from .textcues_msg import MSG_DESCR

# ---------------------------------------------------------------------------


class TextCueSWebData(swappWebData):
    """Parse the JSON file, store data and create the bakery system.

    """

    def __init__(self, json_filename: str | None = None) -> None:
        """Create a TextCueSWebData instance.

        :param json_filename: (str|None) Path of the JSON file to parse, or None.
        :return: (None)

        """
        super(TextCueSWebData, self).__init__(json_filename)
        # Filename of the default page.
        self._default = TextCueSLauncherRecipe.page()

    # -----------------------------------------------------------------------

    def id(self):
        return "TextCueS"

    # -----------------------------------------------------------------------

    @staticmethod
    def icon() -> str:
        """Return the page icon name."""
        return sppasImagesAccess.get_icon_filename("textcues")

    @staticmethod
    def description() -> str:
        """Return a short description of the application."""
        return MSG_DESCR

    @staticmethod
    def name() -> str:
        """Return a short name of the application."""
        return "TextCueS"

    # -----------------------------------------------------------------------

    def is_page(self, page_name: str) -> bool:
        """Override. Return true if the given page name can be baked.

        :param page_name: The name of the page to check.
        :return: (bool) True if the given page name can be baked.

        """
        if page_name in self._pages:
            return True

        # If it's one of the pages for the pathway
        if page_name.startswith("textcues_") is True and page_name.endswith(".html") is True:
            return True

        # If it's the welcome of the application
        if page_name == "textcues.html":
            return True

        return False

    # -----------------------------------------------------------------------

    def bake_response(self, page_name: str, default: str = "") -> BaseResponseRecipe | None:
        """Return the recipe used to bake the requested page.

        :param page_name: (str) Name of the page to bake.
        :param default: (str) Default page name if the requested page does not exist.
        :return: (BaseResponseRecipe|None) A recipe instance, or None.

        """
        return TextCueSResponseRecipe()
        logging.info(f"Requested page name: {page_name}")

        # Create the Pathway ResponseRecipe
        if page_name.startswith("textcues_") is True and page_name.endswith(".html") is True:
            return TextCueSResponseRecipe()

        # Create the welcome ResponseRecipe
        if page_name == TextCueSLauncherRecipe.page():
            return TextCueSLauncherRecipe()

        # Any other page name
        return None
