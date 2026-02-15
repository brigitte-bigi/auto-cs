"""
:filename: sppas.ui.swapp.app_textcues.controllers.record_controller.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Manage the TextCueS record lifecycle and validation.

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

from ..textcues_record import TextCueSRecord
from ..views.pathway_text_view import PathwayTextView
from ..views.pathway_sound_view import PathwaySoundView
from ..views.pathway_code_view import PathwayCodeView

# ---------------------------------------------------------------------------


class TextCueSRecordController:
    """Manage the TextCueS record lifecycle and validation.

    This helper centralizes record creation, population from client data,
    and injection of view-required extras.

    """

    def __init__(self, model):
        """Initialize the record controller.

        :param model: (TextCueSModel) The model used for validations and choices.

        """
        self.__model = model

    # -----------------------------------------------------------------------

    def init_record(self) -> TextCueSRecord:
        """Create a fresh record and set required extras.

        :return: (TextCueSRecord) A new record initialized for the first step.

        """
        _record = TextCueSRecord(pathway_id='')
        self.set_record_extras(_record)
        return _record

    # -----------------------------------------------------------------------

    def set_record_extras(self, record: TextCueSRecord) -> None:
        """Populate the record with view-required extra fields.

        :param record: (TextCueSRecord) The record to update.

        """
        record.set_extra(
            'pathway_ids',
            (
                PathwayTextView.get_id(),
                PathwaySoundView.get_id(),
                PathwayCodeView.get_id()
            )
        )
        record.set_extra(
            'pathway_msg',
            (
                PathwayTextView.get_msg(),
                PathwaySoundView.get_msg(),
                PathwayCodeView.get_msg()
            )
        )
        record.set_extra('lang_choices', self.__model.get_lang_choices())

    # -----------------------------------------------------------------------

    def populate_record(self, current_record: TextCueSRecord, data: dict) -> TextCueSRecord:
        """Create and validate a TextCueSRecord from received client data.

        :param current_record: (TextCueSRecord) Current controller record, used for consistency checks.
        :param data: (dict) Data received from the client to build the record.
        :return: (TextCueSRecord) A validated record reflecting a coherent pathway state.

        """
        _record = TextCueSRecord(data['pathway'])
        _record.parse(data)
        if 'error' in data:
            _record.set_extra('error', data['error'])
        if 'info' in data:
            _record.set_extra('info', data['info'])

        try:
            if current_record.pathway != '':
                if current_record.text is None or current_record.textnorm is None:
                    current_record.pathway = ''
                    current_record.reset_results()
                    return current_record

            if _record.textnorm is not None:
                if _record.textprons is not None:
                    self.__model.validate_pronunciations(_record.textnorm, _record.textprons)

                if _record.phonetize is not None and _record.pathway not in (
                    PathwaySoundView.get_id(),
                    PathwayCodeView.get_id()
                ):
                    _record.phonetize = None

                if _record.cuedkeys is not None and _record.pathway != PathwayCodeView.get_id():
                    _record.cuedkeys = None
                    _record.cuedphons = None
            else:
                _record.reset_results()

        except:
            _record.pathway = ''
            _record.reset_results()
            _record.set_extra('error', traceback.format_exc())

        return _record
