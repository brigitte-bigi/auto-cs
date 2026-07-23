"""
:filename: sppas.ui.swapp.spinoff.splics.discovery.app_listcues.listcues_controller.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Main controller of "ListCueS" app.

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

import logging

from .listcues_msg import MSG_INFO_NO_INPUT
from .listcues_msg import MSG_INFO_NO_PRONS
from .listcues_record import ListCueSRecord

# ---------------------------------------------------------------------------


class ListCueSController:
    """Coordinate model execution and view preparation for the ListCueS application.

    This controller implements the Controller role of the MVC pattern. It receives
    serialized data from the client, dispatches the cue to the model conversion,
    and prepares the data required by the view.

    """
    def __init__(self, model, view):
        """Initialize the controller with a model and a view.

        :param model: (ListCueSModel) The model managing the conversion.
        :param view: (ListCueSView) The view managing the HTML structure.

        """
        self.__model = model
        self.__view = view
        self.__record = None
        self.reset()

    # -----------------------------------------------------------------------

    def reset(self) -> None:
        """Reset to the initial (welcome) state: no language chosen yet.

        The recipe instance is reused by the server across unrelated
        requests (the model's per-language dictionary index is expensive to
        rebuild): without this, a plain navigation back to "listcues.html"
        (e.g. the header logo link) would keep showing whatever a previous,
        unrelated request left the record in, instead of the welcome page.

        """
        self.__record = ListCueSRecord()
        self.__record.set_extra("lang_choices", self.__model.get_lang_choices())

    # -----------------------------------------------------------------------

    def populate_view(self) -> None:
        """Populate the ListCueS view with data from the model.

        """
        self.__view.populate_tree_content(self.__record)

    # -----------------------------------------------------------------------

    def handle_convert(self, data: dict) -> ListCueSRecord:
        """Handle a conversion request and update the record accordingly.

        A new record is built from the received data. The cue, when given, is
        converted into its pronounceable phoneme sequences and their words.
        The returned record contains extras['error'] or extras['info'] when
        applicable; populate_view() renders it, including the Yoyo dialogs.

        :param data: (dict) Data received from the client, expected to contain 'cue'.
        :return: (ListCueSRecord) The updated record.

        """
        self.__record = ListCueSRecord()
        self.__record.parse(data)
        self.__record.set_extra("lang_choices", self.__model.get_lang_choices())

        try:
            self.__model.set_lang(self.__record.lang)
        except Exception as e:
            logging.exception(e)
            self.__record.set_extra("error", str(e))
        else:
            # A language is now known: the view can build the key piano.
            self.__record.set_extra("shape_keys", self.__model.get_shape_keys())
            self.__record.set_extra("position_keys", self.__model.get_position_keys())

            if self.__record.cue is None:
                # Only hint at entering a cue when one was actually submitted
                # empty (a real "Validate" click): arriving here for the first
                # time, right after the welcome form, never submitted a cue at
                # all -- showing the hint immediately would be a premature,
                # unsolicited popup.
                if "cue" in data:
                    self.__record.set_extra("info", MSG_INFO_NO_INPUT)
            else:
                self._handle_cue(self.__record)

        return self.__record

    # -----------------------------------------------------------------------
    # Workers
    # -----------------------------------------------------------------------

    def _handle_cue(self, record: ListCueSRecord) -> None:
        """Convert the cue of the record into pronunciations and store the result.

        :param record: (ListCueSRecord) The record to update.

        """
        try:
            _entries = self.__model.keys_to_prons(record.cue)
            record.set_extra("prons_result", _entries)
            if len(_entries) == 0:
                record.set_extra("info", MSG_INFO_NO_PRONS)
        except Exception as e:
            logging.exception(e)
            record.set_extra("error", str(e))
