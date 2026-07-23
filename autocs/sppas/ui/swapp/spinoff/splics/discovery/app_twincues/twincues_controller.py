"""
:filename: sppas.ui.swapp.spinoff.splics.discovery.app_twincues.twincues_controller.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Main controller of "TwinCueS" app.

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

from .twincues_msg import MSG_ERROR_NOT_YET_IMPLEMENTED
from .twincues_msg import MSG_INFO_NO_INPUT
from .twincues_msg import MSG_INFO_NO_TWIN_WORD
from .twincues_msg import MSG_INFO_NO_TWIN_CUE
from .twincues_record import TwinCueSRecord

# ---------------------------------------------------------------------------


class TwinCueSController:
    """Coordinate model execution and view preparation for the TwinCueS application.

    This controller implements the Controller role of the MVC pattern. It receives
    serialized data from the client, dispatches the word and/or the cue to the
    appropriate model conversion, and prepares the data required by the view.

    """
    def __init__(self, model, view):
        """Initialize the controller with a model and a view.

        :param model: (TwinCueSModel) The model managing the conversions.
        :param view: (TwinCueSView) The view managing the HTML structure.

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
        rebuild): without this, a plain navigation back to "twincues.html"
        (e.g. the header logo link) would keep showing whatever a previous,
        unrelated request left the record in, instead of the welcome page.

        """
        self.__record = TwinCueSRecord()
        self.__record.set_extra("lang_choices", self.__model.get_lang_choices())

    # -----------------------------------------------------------------------

    def populate_view(self) -> None:
        """Populate the TwinCueS view with data from the model.

        """
        self.__view.populate_tree_content(self.__record)

    # -----------------------------------------------------------------------

    def handle_convert(self, data: dict) -> TwinCueSRecord:
        """Handle a conversion request and update the record accordingly.

        A new record is built from the received data. The word, when given, is
        converted into its cue; the cue, when given, is converted into its
        matching word(s). The returned record contains extras['error'] or
        extras['info'] when applicable; populate_view() renders it, including
        the Yoyo dialogs.

        :param data: (dict) Data received from the client, expected to contain 'word' and/or 'cue'.
        :return: (TwinCueSRecord) The updated record.

        """
        self.__record = TwinCueSRecord()
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
            self.__record.set_extra("max_cue_length", self.__model.get_max_cue_length())

            if self.__record.word is None and self.__record.cue is None:
                # Only hint at entering a word/cue when the form was
                # actually submitted empty (a real "Validate" click):
                # arriving here for the first time, right after the welcome
                # form, never submitted either field at all -- showing the
                # hint immediately would be a premature, unsolicited popup.
                if "word" in data or "cue" in data:
                    self.__record.set_extra("info", MSG_INFO_NO_INPUT)
            else:
                self._handle_word(self.__record)
                self._handle_cue(self.__record)

        return self.__record

    # -----------------------------------------------------------------------
    # Workers
    # -----------------------------------------------------------------------

    def _handle_word(self, record: TwinCueSRecord) -> None:
        """Convert the word of the record into a cue and store the result.

        :param record: (TwinCueSRecord) The record to update.

        """
        if record.word is None:
            return

        try:
            _entries = self.__model.word_to_cues(record.word)
            record.set_extra("cues_result", _entries)
            _has_twin = any(len(_entry["twins"]) > 0 for _entry in _entries)
            if _has_twin is False:
                _tried = ", ".join(_pron for _entry in _entries for _pron in _entry["prons"])
                record.set_extra("info", MSG_INFO_NO_TWIN_WORD.format(_tried))
        except NotImplementedError:
            record.set_extra("error", MSG_ERROR_NOT_YET_IMPLEMENTED)
        except Exception as e:
            logging.exception(e)
            record.set_extra("error", str(e))

    # -----------------------------------------------------------------------

    def _handle_cue(self, record: TwinCueSRecord) -> None:
        """Convert the cue of the record into word(s) and store the result.

        :param record: (TwinCueSRecord) The record to update.

        """
        if record.cue is None:
            return

        try:
            _entries = self.__model.cues_to_words(record.cue)
            record.set_extra("words_result", _entries)
            if len(_entries) == 0:
                record.set_extra("info", MSG_INFO_NO_TWIN_CUE)
        except NotImplementedError:
            record.set_extra("error", MSG_ERROR_NOT_YET_IMPLEMENTED)
        except Exception as e:
            logging.exception(e)
            record.set_extra("error", str(e))
