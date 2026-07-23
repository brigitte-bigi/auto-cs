"""
:filename: sppas.ui.swapp.spinoff.splics.discovery.app_listcues.app_listcues.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Bakery for the web-based application "ListCueS".

..
    This file is part of Auto-CS: <https://autocs.sourceforge.io>
    -------------------------------------------------------------------------

    Copyright (C) 2024-2026  Brigitte Bigi, CNRS
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
from sppas.ui.swapp.spinoff.splics.splicssg import splics_paths
from sppas.ui.swapp.spinoff.splics.splicssg import splics_categories
from sppas.ui.swapp.wappbase.wappbakery import swappWebData

from .listcuesmaker import ListCueSResponseRecipe
from .listcues_msg import MSG_DESCR

# ---------------------------------------------------------------------------


class ListCueSWebData(swappWebData):
    """Parse the JSON file, store data and create the bakery system.

    """

    # The category this application belongs to.
    CATEGORY = splics_categories.discovery

    def __init__(self, json_filename: str | None = None) -> None:
        """Create a ListCueSWebData instance.

        :param json_filename: (str|None) Path of the JSON file to parse, or None.
        :return: (None)

        """
        super(ListCueSWebData, self).__init__(json_filename)
        # Filename of the default page.
        self._default = ListCueSResponseRecipe.page()

    # -----------------------------------------------------------------------

    def id(self):
        return "ListCueS"

    # -----------------------------------------------------------------------

    @staticmethod
    def icon() -> str:
        """Return the page icon name."""
        return splics_paths.icons + "listcues.png"

    @staticmethod
    def description() -> str:
        """Return a short description of the application."""
        return MSG_DESCR

    @staticmethod
    def name() -> str:
        """Return a short name of the application."""
        return "ListCueS"

    # -----------------------------------------------------------------------

    def is_page(self, page_name: str) -> bool:
        """Override. Return true if the given page name can be baked.

        :param page_name: The name of the page to check.
        :return: (bool) True if the given page name can be baked.

        """
        if page_name in self._pages:
            return True

        # The conversion page, reached with a random name once a language
        # has been chosen on welcome (see HTMLTag.page_random()).
        if page_name.startswith("listcues_") is True and page_name.endswith(".html") is True:
            return True

        # The welcome page of the application.
        if page_name == ListCueSResponseRecipe.page():
            return True

        return False

    # -----------------------------------------------------------------------

    def bake_response(self, page_name: str, default: str = "") -> BaseResponseRecipe | None:
        """Return the recipe used to bake the requested page.

        :param page_name: (str) Name of the page to bake.
        :param default: (str) Default page name if the requested page does not exist.
        :return: (BaseResponseRecipe|None) A recipe instance, or None.

        """
        logging.info(f"Requested page name: {page_name}")

        # The conversion page (a random name), or the fixed welcome page.
        is_conversion = page_name.startswith("listcues_") is True and page_name.endswith(".html") is True
        is_welcome = page_name == ListCueSResponseRecipe.page()

        if is_conversion is True or is_welcome is True:
            recipe = ListCueSResponseRecipe()
            # Tells the recipe which of the two it actually is, so it can
            # refuse to process a "lang" query received on the fixed,
            # guessable welcome URL (see set_requested_page()).
            recipe.set_requested_page(page_name)
            return recipe

        # Any other page name
        return None
