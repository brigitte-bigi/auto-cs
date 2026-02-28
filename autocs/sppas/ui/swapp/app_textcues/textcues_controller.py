"""
:filename: sppas.ui.swapp.app_textcues.textcues_controller.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Main controller of "TextCueS" app.

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

import traceback
import logging

from .textcues_msg import MSG_ERROR_NO_TEXT
from .textcues_msg import MSG_ERROR_NO_PRON
from .textcues_msg import MSG_ERROR_EMPTY_PRON
from .textcues_msg import MSG_ERROR_INVALID_FORMAT
from .textcues_msg import MSG_YOYO_NOT_YET
from .textcues_msg import MSG_ERROR_LEN_MISMATCH
from .textcues_record import TextCueSRecord
from .views.pathway_text_view import PathwayTextView
from .views.pathway_sound_view import PathwaySoundView
from .views.pathway_code_view import PathwayCodeView

from .controllers.record_controller import TextCueSRecordController

# ---------------------------------------------------------------------------


class TextCueSController:
    """Coordinate model execution and view preparation for the TextCueS application.

    This controller implements the Controller role of the MVC pattern. It receives
    serialized data from the client, rebuilds and validates the application record,
    dispatches processing to the appropriate model pathways (Text, Sound, Code),
    and prepares the data required by the views. It ensures consistency between
    pathway steps, handles error conditions, and manages the progressive flow of
    the application from text input to coded output.

    """
    def __init__(self, model, view):
        """Initialize the controller with a model and a view.

        :param model: (TextCueSModel) The model managing the applications.
        :param view: (TextCueSView) The view managing the HTML structure.

        """
        self.__model = model
        self.__view = view

        # Create a data record controller with default values.
        self.__record_controller = TextCueSRecordController(self.__model)
        self.__record = self.__record_controller.init_record()

    # -----------------------------------------------------------------------

    def handle(self, data: dict) -> None:
        """Dispatch the received data to the appropriate pathway handler.

        The internal record is rebuilt from the received serialized data, mandatory
        extras are set, and the model language is updated from the record. According
        to the current pathway identifier, the corresponding step is executed:
        text normalization/phonetization (Text), pronunciation selection and coding
        (Sound), or coding/render preparation (Code). When inconsistencies are found,
        the record is adjusted to fall back to a previous step.

        :param data: (dict) Data received from the client, expected to match a serialized TextCueSRecord.

        """
        # First access to the app: no previous record.
        if "pathway" not in data:
            self.__record = self.__record_controller.init_record()
            return

        # Fill in the record with the received data. Preserves options if any.
        self.__record = self.__record_controller.populate_record(self.__record, data)
        self.__record_controller.set_record_extras(self.__record)
        self.__model.set_lang(self.__record.lang)

        if self.__record.pathway == "":
            return

        # The current page is "pathway_text". The user filled in the lang & text.
        # Launch the model for normalization and phonetization.
        if self.__record.pathway == PathwayTextView.get_id():
            if self.__record.text is None:
                self.__record.pathway = ""
                return
            self._handle_pathway_text()

        # The current page is "pathway_sound".
        # textnorm should be properly assigned.
        elif self.__record.pathway == PathwaySoundView.get_id():
            self._handle_pathway_sound(data)
            if "error" not in self.__record.extras:
                self._handle_pathway_code()

        # The current page is "pathway_code".
        # cuedphons & cuedkeys should be properly assigned.
        elif self.__record.pathway == PathwayCodeView.get_id():
            if self.__record.phonetize is not None:
                self._handle_pathway_code()
            elif self.__record.textnorm is not None:
                # an error ... we should not be here.
                # redirect to the previous page.
                self.__record.textnorm = None
                self.__record.pathway = PathwaySoundView.get_id()

        if "error" in self.__record.extras:
            logging.error(self.__record.extras["error"])

    # -----------------------------------------------------------------------

    def populate_view(self) -> None:
        """Populate the TextCueS view with data from the model.

        The method instructs the view to create the page content according
        to the current record.

        """
        self.__view.populate_tree_content(self.__record)

    # -----------------------------------------------------------------------

    def handle_display_mode(self, data: dict) -> TextCueSRecord:
        """Handle a display mode change request and prepare updated HTML content.

        If no 'pathway' key is provided, the current record is returned unchanged.
        Otherwise, a new record is created from the received data, mandatory extras
        are set, and the Code pathway is processed to obtain a cued result. The
        produced result is validated, then the view is asked to generate the HTML
        fragment corresponding to the selected display mode. The method returns the
        record containing either extras['content'] on success or extras['error'] on
        failure.

        :param data: (dict) Data received from the client for rebuilding the record.
        :return: (TextCueSRecord) Record updated with extras['content'] or extras['error'].

        """
        if "pathway" not in data:
            # Use the current record
            return self.__record

        # Fill in the record with the received data
        self.__record = self.__record_controller.populate_record(self.__record, data)
        self.__record_controller.set_record_extras(self.__record)
        self._handle_pathway_code()

        # In any case, the view has to send the HTML content
        _content = self.__view.get_displaymode_content(self.__record)
        if len(_content) == 0:
            if "error" not in self.__record.extras:
                self.__record.set_extra(
                    "error",
                    "Unknown error in 'handle_display_mode: Got an empty HTML content."
                )
        else:
            self.__record.set_extra("content", _content)

        return self.__record

    # -----------------------------------------------------------------------
    # Workers
    # -----------------------------------------------------------------------

    def _reconstruct_phonetize_from_events(self, data: dict) -> list:
        """Reconstruct the selected pronunciations from received event data.

        The event keys are expected to end with '-sound_input' and to follow the
        pattern '<index>-sound_input'. The index is used to place each
        selected pronunciation at the correct position in the returned list.

        :param data: (dict) Event dictionary received from the client.
        :raises: KeyError: No key ending with '-sound_input' was found in data.
        :raises: ValueError: A key has an invalid '<token>-<index>-sound_input' format.
        :raises: ValueError: A selected pronunciation is empty.
        :return: (list) Pronunciations ordered by their extracted index.

        """
        _nb = 0
        for _e in data:
            if _e.endswith("-sound_input"):
                _nb += 1
        if _nb == 0:
            raise KeyError(MSG_ERROR_NO_PRON)

        _tokens = data["textnorm"].split(" ")
        if len(_tokens) != _nb:
            raise Exception(MSG_ERROR_LEN_MISMATCH.format(len(_tokens), _nb))

        _prons = ["-"]*_nb
        for _e in data:
            if _e.endswith("-sound_input"):
                _tmp = _e.split("-")
                if len(_tmp) != 2:
                    raise ValueError(MSG_ERROR_INVALID_FORMAT.format(str(_tmp)))
                _pron_idx = int(_tmp[0])

                _this_pron = data[_e]
                if len(_this_pron) == 0:
                    raise ValueError(MSG_ERROR_EMPTY_PRON.format(_tokens[_pron_idx]))

                _prons[_pron_idx] = self.__model.validate_phonemes(_this_pron)

        return _prons

    # -----------------------------------------------------------------------

    def _handle_pathway_text(self):
        """Handle the Text pathway and store either normalized data or an error message.

        If a text is available in the record, the model is called to obtain the normalized
        token list and the corresponding pronunciation variants. The result is validated:
        an error is stored if no token is produced or if token and pronunciation lists
        do not match in length. If valid, both the normalized text and the phonetization
        variants are stored in the record. If no text is provided, an error is stored.
        Any exception is caught and an error message is stored in the record extras.

        """
        try:
            if self.__record.text is not None:
                # Ask the model to annotate and get the normalization and
                # phonetization with pronunciation variants
                _tokens, _prons = self.__model.pathway_text(self.__record.text)
                self.__record.textnorm = _tokens
                self.__record.textprons = _prons

            else:
                raise Exception(MSG_ERROR_NO_TEXT)

        except Exception as e:
            logging.error(traceback.format_exc())
            self.__record.extras["error"] = str(e)

        # Invalidate the previously estimated results
        if "error" in self.__record.extras:
            self.__record.reset_results()

    # -----------------------------------------------------------------------

    def _handle_pathway_sound(self, data: dict):
        """Handle the Sound pathway and store an error message if something fails.

        If the record does not already contain a reconstructed phonetization, the user
        selections are reconstructed from the given event data and stored in the record.
        The model is then called to annotate the normalized text and produce both coded
        keys and the corresponding phoneme sequence. Any exception is caught and an error
        message is stored in the record extras under the key 'error'.

        :param data: (dict) Event data used to reconstruct the selected pronunciations

        """
        try:
            # the pronunciations the user choose were not already re-constructed
            if self.__record.phonetize is None:

                # Make a list with the pronunciation the user selected for each token
                _p = self._reconstruct_phonetize_from_events(data)
                self.__record.phonetize = _p

                # Ask the model to annotate and get the coded keys
                self.__record.cuedkeys, self.__record.cuedphons = self.__model.pathway_sound(
                    self.__record.textnorm,
                    self.__record.phonetize
                )
        except Exception as e:
            logging.error(traceback.format_exc())
            self.__record.set_extra("error", str(e))

    # -----------------------------------------------------------------------

    def _handle_pathway_code(self):
        """Handle the Code pathway and store either an error message or the generated result.

        Depending on the selected display mode, the corresponding model method is called:
        overlay (mode 1), video (mode 2), or images (other modes). If an exception occurs,
        an error message is stored in the record extras under the key 'error'. If no exception
        occurs, the generated result is stored under the key 'cuedresult'.

        """
        try:
            # Overlay image: shape over the face at the expected position
            if self.__record.mode == 1:
                _result = self.__model.pathway_code_overlay(
                    self.__record.cuedkeys,
                    self.__record.model_pos,
                    self.__record.model_angle
                )

            # Video with hand motion
            elif self.__record.mode == 2:
                _result = self.__model.pathway_code_video(
                    self.__record.cuedkeys,
                    self.__record.model_pos,
                    self.__record.model_angle,
                    self.__record.model_timing
                )

            # Separated images: shape + position
            else:
                _result = self.__model.pathway_code_images(
                    self.__record.cuedkeys
                )

            # Check the estimated result
            if self.__record.mode in (1, 2) and len(_result) != len(self.__record.cuedkeys):
                raise Exception("The number of cued tokens does not match the number of tokens. "
                                "Expected {:d}, got {:d}."
                                "".format(len(self.__record.cuedkeys), len(_result)))
            # Normal: store the result for the view
            self.__record.extras["cuedresult"] = _result

        except NotImplementedError:
            self.__record.set_extra("info", MSG_YOYO_NOT_YET)

        except Exception as e:
            logging.error(traceback.format_exc())
            self.__record.set_extra("error", str(e))

        else:
            # Transfer the result to the view via record.extras
            self.__record.set_extra("cuedresult", _result)
