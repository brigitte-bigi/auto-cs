"""
:filename: sppas.ui.swapp.app_textcues.textcuesmaker.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Launcher for the pathway in "TextCueS" application of Auto-CS.

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

from ..htmltags.hstatusnode import HTMLTreeError410
from ..apps.swapp_response import swappBaseResponse

from .textcues_model import TextCueSModel
from .textcues_view import TextCueSView
from .textcues_controller import TextCueSController

# -----------------------------------------------------------------------


class TextCueSResponseRecipe(swappBaseResponse):
    """The textcues_*.html HTTPD response baker.

    """

    def __init__(self, name="TextCueSCoding", tree=None):
        self.__model = TextCueSModel()
        self.__view = None
        self.__controller = None
        super(TextCueSResponseRecipe, self).__init__(name, tree)

    # -----------------------------------------------------------------------
    # OVERRIDE METHODS FROM Whakerpy -- Create une UI
    # -----------------------------------------------------------------------

    @classmethod
    def page(cls) -> str:
        """Return a short description of the application."""
        return "textcues_code.html"

    # -----------------------------------------------------------------------

    def create(self) -> None:
        """Override. Create the fixed page content in HTML.

        The fixed content corresponds to the parts that can't be invalidated:
        head, body_header, body_footer.

        """
        super().create()
        self.__view = TextCueSView(self._htree)
        self.__controller = TextCueSController(self.__model, self.__view)

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

        # Received events from an HTTP Post.
        if "event_name" in events:
            e_name = events["event_name"]
            if e_name == "displaymode":
                self.__process_displaymode_event(events.get('event_value', dict()))
            else:
                self._status.code = 400
                self._data["error"] = f"The server received an unknown event name: {e_name}."
            return False

        else:
            # Events are propagated to the controller.
            # The controller returns the status code and the data to be posted (if any)
            self.__controller.handle(events)
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

    # -----------------------------------------------------------------------
    # PRIVATE
    # -----------------------------------------------------------------------

    def __process_displaymode_event(self, event_value: dict) -> None:
        """Process the given event value coming from the POST of options_form.

        :param event_value: (dict) Data to fill in a TextCueSRecord

        """
        if isinstance(event_value, dict) is False:
            self._data["error"] = f"The server received an invalid event value type: {type(event_value)}."
            self._status.code = 400
            return

        if len(event_value) == 0:
            self._data["error"] = f"The server received an empty event value: {event_value}."
            self._status.code = 400
            return

        record = self.__controller.handle_display_mode(event_value)

        if "content" in record.extras:
            self._status.code = 200
            self._data["content"] = record.extras["content"]

            if "error" in record.extras:
                self._data["error"] = record.extras["error"]
            if "info" in record.extras:
                self._data["info"] = record.extras["info"]

        else:
            self._status.code = 400
            self._data["error"] = record.extras.get("error", "An unidentified error has occurred.")