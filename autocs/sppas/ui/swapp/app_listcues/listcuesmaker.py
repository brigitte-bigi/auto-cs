"""
:filename: sppas.ui.swapp.app_listcues.listcuesmaker.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Single response baker (welcome and conversion) of "ListCueS" application of Auto-CS.

..
    This file is part of Auto-CS: <https://autocs.sourceforge.io>
    -------------------------------------------------------------------------

    Copyright (C) 2026  Brigitte Bigi, CNRS
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

from ..components.hstatusnode import HTMLTreeError410
from ..components.swapp_response import swappBaseResponse

from .listcues_model import ListCueSModel
from .listcues_view import ListCueSView
from .listcues_controller import ListCueSController

# -----------------------------------------------------------------------


class ListCueSResponseRecipe(swappBaseResponse):
    """The listcues.html HTTPD response baker: welcome and conversion in one page.

    No language is chosen yet -> the welcome content is shown (an intro and a
    language choice form). Once a language has reached the controller -- via
    the welcome form's GET navigation, or via a "convert" POST event -- the
    conversion content (key piano and its result) is shown instead. Both
    cases are handled by the very same :meth:`ListCueSController.handle_convert`,
    so there is only one code path to keep in sync.

    """

    def __init__(self, name="ListCueSConversion", tree=None):
        self.__model = ListCueSModel()
        self.__view = None
        self.__controller = None
        # Default: the fixed welcome page, until bake_response() records the
        # actual requested page name (see set_requested_page()).
        self.__requested_page = self.page()
        super(ListCueSResponseRecipe, self).__init__(name, tree)

    # -----------------------------------------------------------------------
    # OVERRIDE METHODS FROM Whakerpy -- Create the UI
    # -----------------------------------------------------------------------

    @classmethod
    def page(cls) -> str:
        """Return the name of the page."""
        return "listcues.html"

    # -----------------------------------------------------------------------

    def set_requested_page(self, page_name: str) -> None:
        """Record which actual URL this instance is serving.

        The fixed, guessable welcome page ("listcues.html") must never
        process a "lang" query directly: only a random page name (see
        HTMLTag.page_random(), used by the welcome form's own action) is
        allowed to trigger the expensive per-language processing, so a bot
        that only knows the fixed URL can never reach it directly.

        :param page_name: (str) The page name actually requested.

        """
        self.__requested_page = page_name

    # -----------------------------------------------------------------------

    def create(self) -> None:
        """Override. Create the fixed page content in HTML.

        The fixed content corresponds to the parts that can't be invalidated:
        head, body_header, body_footer.

        """
        super().create()
        self.__view = ListCueSView(self._htree)
        self.__controller = ListCueSController(self.__model, self.__view)

    # -----------------------------------------------------------------------
    # Callbacks
    # -----------------------------------------------------------------------

    def _process_events(self, events: dict, **kwargs) -> bool:
        """Override. Process the given events coming from the POST of any form.

        :param events (dict): key=event_name, value=event_value
        :return: (bool) True if the whole page must be re-created.

        """
        logging.debug(f" >>>>> Page Application ListCueS -- Process events: {events} <<<<<< ")
        self._data = dict()
        self._status.code = 200

        # Accessibility events can be received in the same post
        if "accessibility_color" in events:
            self.__view.set_accessibility(color=events["accessibility_color"])
            if len(events) == 1:
                return False
            else:
                events.pop("accessibility_color")

        if "accessibility_contrast" in events:
            self.__view.set_accessibility(contrast=events["accessibility_contrast"])
            if len(events) == 1:
                return False
            else:
                events.pop("accessibility_contrast")

        # Both the welcome form ("?lang=xxx", a plain GET) and the conversion
        # form ("lang" + "cue", a plain POST) are real page navigations,
        # parsed into "events" the very same way (see WhakerPy's
        # process_post() and parse_query_string()). The whole page must be
        # re-created (True) so that _bake() renders the conversion content,
        # including the Yoyo dialogs for any error or info.
        #
        # Except on the fixed "listcues.html" itself: a bot only knows that
        # guessable URL, never the random one the welcome form actually
        # submits to (see set_requested_page()), so a "lang" query received
        # there is never legitimate and is silently ignored -- welcome shows
        # regardless, and the expensive per-language processing never runs.
        if "lang" in events and self.__requested_page != self.page():
            self.__controller.handle_convert(events)
            return True

        # A plain navigation with no query string/body at all -- e.g. the
        # header logo link back to "listcues.html" -- or a "lang" query
        # ignored above because it targeted the fixed welcome URL. The
        # controller is reused by the server across unrelated requests:
        # without an explicit reset, it would keep showing whatever a
        # previous request left it
        # in, instead of going back to the welcome page.
        self.__controller.reset()
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
            self.__controller.populate_view()

        else:
            msg = f"Unexpected status '{self._status.code}' while baking the page content."
            logging.error(msg)
            p = self._htree.element("p")
            p.set_value(msg)

