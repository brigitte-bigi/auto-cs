"""
:filename: sppas.ui.swapp.app_textcues.textcues_model.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Main model of "TextCueS" app.

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

import os

from sppas.core.coreutils import ISO639
from sppas.core.config import separators
from sppas.core.config import symbols
from sppas.src.annotations import sppasParam
from sppas.src.annotations.CuedSpeech import CuedSpeechKeys

from .models.pathway_text_model import PathwayTextModel
from .models.pathway_sound_model import PathwaySoundModel
from .models.images_model import PathwayCodeImagesModel
from .models.overlays_model import PathwayCodeOverlayModel
from .models.video_model import PathwayCodeVideoModel

from .textcues_msg import MSG_ERROR_NO_TOKENS
from .textcues_msg import MSG_ERROR_LEN_MISMATCH
from .textcues_msg import MSG_ERROR_INVALID_PRON
from .textcues_msg import MSG_ERROR_UNKNOWN_PHON

# ---------------------------------------------------------------------------


class TextCueSModel:
    """Model for the TextCueS application.

    """

    def __init__(self):
        """Create the model to get an automated cued speech sequence from text.

        """
        annotation_id = "cuedspeech"
        config_name = annotation_id + ".json"
        self._parameters = sppasParam([config_name])
        self._ann_step_idx = self._parameters.activate_annotation(annotation_id)
        self.__cs = None

    # -----------------------------------------------------------------------

    def get_langlist(self) -> list:
        """Return the list of supported language codes."""
        return self._parameters.get_langlist(self._ann_step_idx)

    # ---------------------------------------------------------------------------

    def get_lang_choices(self) -> dict:
        """Fill-in a dictionary with language choices.

        Key is the language code for the annotation and the value is the
        language name.

        :return: (dict) The different available languages.

        """
        _choices = dict()
        for code in self.get_langlist():
            info = ISO639.LANGUAGES.get(code, None)
            if info is not None:
                lang_name = info.language_name
            else:
                lang_name = "Undefined"
            _choices[code] = lang_name

        return _choices

    # -----------------------------------------------------------------------

    def set_lang(self, lang: str):
        """Fix the language for the automation of cued speech.

        :param lang: The language code for the cued speech.

        """
        if lang not in self.get_lang_choices():
            raise KeyError(f"Language {lang} is not supported.")

        self._parameters.set_lang(lang, self._ann_step_idx)
        rule_file = self._parameters.get_langresource(self._ann_step_idx)[0]
        if os.path.exists(rule_file) is False:
            raise FileNotFoundError(f"CuedSpeech resource file {rule_file} not found.")

        self.__cs = CuedSpeechKeys(rule_file)

    # -----------------------------------------------------------------------

    def pathway_text(self, text: str) -> tuple:
        """"""
        if self.__cs is None:
            raise ValueError("The 'lang' was not defined in the model.")

        _model = PathwayTextModel()
        _tokens, _prons = _model.annotate(
            self._parameters.get_lang(self._ann_step_idx),
            text
        )
        TextCueSModel.validate_pronunciations(_tokens, _prons)

        return _tokens, _prons

    # -----------------------------------------------------------------------

    def pathway_sound(self, tokens: list, prons: list) -> tuple:
        """"""
        if self.__cs is None:
            raise ValueError("Pathway model 'lang' is not defined.")

        _model = PathwaySoundModel(self.__cs)
        return _model.annotate(tokens, prons)

    # -----------------------------------------------------------------------
    # -----------------------------------------------------------------------

    def pathway_code_images(self, cuedkeys: list) -> tuple:
        """

        :param cuedkeys:
        :raises: ValueError: CS rules not defined
        :return:

        """
        if self.__cs is None:
            raise ValueError("Cued Speech rules is not defined.")

        p = PathwayCodeImagesModel(self.__cs)
        return p.generate(cuedkeys)

    # -----------------------------------------------------------------------

    def pathway_code_overlay(self, cuedkeys: list, model_pos: int, model_angle: int) -> tuple:
        """"""
        if self.__cs is None:
            raise ValueError("Cued Speech rules is not defined.")

        p = PathwayCodeOverlayModel(self.__cs)
        return p.generate(cuedkeys, model_pos, model_angle)

    # -----------------------------------------------------------------------

    def pathway_code_video(self, cuedkeys: list, model_pos: int, model_angle: int, model_timing: int) -> tuple:
        """"""
        if self.__cs is None:
            raise ValueError("Cued Speech rules is not defined.")

        p = PathwayCodeVideoModel(self.__cs)
        return p.generate(cuedkeys, model_pos, model_angle, model_timing)

    # -----------------------------------------------------------------------

    def validate_phonemes(self, pron: str):
        """Raise an exception if a phonemes of the given pronunciations is not valid.

        :param pron: (list) Pronunciation of a token to be verified.
        :raises: ValueError: At least a phoneme is not valid.

        """
        _tab = pron.split(separators.phonemes)
        for _p in _tab:
            # Check if the phoneme is known in the given language
            _p_key = self.__cs.get_key(_p)
            if _p_key is None:
                raise ValueError(MSG_ERROR_UNKNOWN_PHON.format(_p))

        return pron

    # -----------------------------------------------------------------------

    @staticmethod
    def validate_pronunciations(tokens: list, prons: list) -> None:
        """Validate token-to-pronunciation alignment and phoneme content.

        The token list must not be empty and must have the same length as the
        pronunciation list. Each pronunciation is split into phonemes using the
        configured phoneme separator. If any extracted phoneme matches a forbidden
        symbol, an exception is raised with details about the token and the offending
        symbol.

        :param tokens: (list) Tokens to be validated against pronunciations.
        :param prons: (list) Pronunciations aligned with tokens.
        :raises: Exception: No token was provided.
        :raises: Exception: Token and pronunciation lists have different lengths.
        :raises: Exception: A pronunciation contains an invalid symbol.

        """
        if len(tokens) == 0:
            raise Exception(MSG_ERROR_NO_TOKENS)

        if len(tokens) != len(prons):
            raise Exception(MSG_ERROR_LEN_MISMATCH.format(len(tokens), len(prons)))

        for _token, _pronunciation in zip(tokens, prons):
            _phones = _pronunciation.split(separators.phonemes)
            for _p in _phones:
                if _p in symbols.phone:
                    raise Exception(MSG_ERROR_INVALID_PRON.format(_token, _p))
