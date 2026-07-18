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

from __future__ import annotations
import os
import logging

from sppas.core.coreutils import ISO639
from sppas.core.config import paths
from sppas.core.config import separators
from sppas.core.config import symbols
from sppas.core import sppasKeyError
from sppas.src.annotations import sppasParam
from sppas.src.annotations.CuedSpeech import CuedSpeechKeys
from sppas.src.annotations.CuedSpeech.wherecue.positions import WhereVowelPositionsPredictor
from sppas.src.annotations.CuedSpeech.wherecue.angles import WhereAnglesPredictor
from sppas.src.annotations.CuedSpeech.whenhand.transitions import WhenTransitionPredictor
from sppas.src.resources import sppasDictPron

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

    # Reasons why overlay/video generation can be unavailable, returned by
    # test_overlay_available()/test_video_available(). Two distinct causes
    # were collapsed into a single bool before: a missing dependency/resource
    # (environment) and a language whose Cued Speech rules are not yet
    # covered by the prediction models (content) call for two different
    # messages in the view.
    REASON_AVAILABLE = "available"
    REASON_NOT_INSTALLED = "not_installed"
    REASON_NOT_IMPLEMENTED = "not_implemented"

    def __init__(self):
        """Create the model to get an automated cued speech sequence from text.

        """
        annotation_id = "cuedspeech"
        config_name = annotation_id + ".json"
        self._parameters = sppasParam([config_name])
        self._ann_step_idx = self._parameters.activate_annotation(annotation_id)
        self.__cs = None
        self.__consonants = tuple()
        self.__vowels = tuple()

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
        self.__consonants, self.__vowels = self.__build_phoneme_inventory(lang)

    # -----------------------------------------------------------------------

    def __build_phoneme_inventory(self, lang: str) -> tuple:
        """Classify every dictionary-attested phoneme as a consonant or a vowel.

        Computed once per set_lang(), in a single pass over the pronunciation
        dictionary, and cached: get_consonants()/get_vowels() must not each
        re-read and re-parse the whole dictionary on every call.

        The phonemes offered are those actually attested in the dictionary --
        not every phoneme the rules could theoretically produce, since that
        would include phonemes no word of the language ever uses. The rules
        are used only to classify each attested phoneme: "C" (consonant),
        "V"/"W" (vowel, including diphthongs), anything else is ignored (e.g.
        break symbols).

        :param lang: (str) The language code.
        :return: (tuple) (consonants: tuple, vowels: tuple), both sorted.

        """
        dict_lang = lang
        if lang == "fra":
            dict_lang = "fre"
        pdict_file = os.path.join(paths.resources, "dict", dict_lang + ".dict")
        pdict = sppasDictPron(pdict_file, nodump=False)

        _attested = set()
        for _word in pdict:
            if pdict.is_unk(_word) is True:
                continue
            for _pron in pdict.get_pron(_word).split(separators.variants):
                _attested.update(_pron.split(separators.phonemes))

        _consonants = set()
        _vowels = set()
        for _phoneme in _attested:
            _class = self.__cs.get_class(_phoneme)
            if _class == "C":
                _consonants.add(_phoneme)
            elif _class in ("V", "W"):
                _vowels.add(_phoneme)

        return tuple(sorted(_consonants)), tuple(sorted(_vowels))

    # -----------------------------------------------------------------------

    def get_consonants(self) -> tuple:
        """Return every dictionary-attested consonant phoneme of the current language.

        :raises: ValueError: The language was not set.
        :return: (tuple) Sorted consonant phonemes.

        """
        if self.__cs is None:
            raise ValueError("Cued Speech rules is not defined.")

        return self.__consonants

    # -----------------------------------------------------------------------

    def get_vowels(self) -> tuple:
        """Return every dictionary-attested vowel phoneme of the current language.

        :raises: ValueError: The language was not set.
        :return: (tuple) Sorted vowel phonemes.

        """
        if self.__cs is None:
            raise ValueError("Cued Speech rules is not defined.")

        return self.__vowels

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

    def pathway_code_overlay(self, cuedkeys: list, cuedphons: list, model_pos: int, model_angle: int) -> tuple:
        """Generate overlay images and return them with the model versions actually used.

        :param model_pos: (int|None) Position model version, or None to use the model's own default.
        :param model_angle: (int|None) Angle model version, or None to use the model's own default.
        :return: (tuple) (result, model_pos_used, model_angle_used)

        """
        if self.__cs is None:
            raise ValueError("Cued Speech rules is not defined.")

        PathwayCodeImagesModel.cleanup_tmp()

        p = PathwayCodeOverlayModel(self.__cs)
        if model_pos is not None:
            p.set_model_position(model_pos)
        if model_angle is not None:
            p.set_model_angle(model_angle)

        _result = p.generate(cuedkeys, cuedphons)
        return _result, p.get_wherepositionpredictor_version(), p.get_whereanglepredictor_version()

    # -----------------------------------------------------------------------

    def pathway_code_video(self, cuedkeys: list, cuedphons: list, model_pos: int, model_angle: int, model_timing: int) -> tuple:
        """Generate a video and return it with the model versions actually used.

        :param model_pos: (int|None) Position model version, or None to use the model's own default.
        :param model_angle: (int|None) Angle model version, or None to use the model's own default.
        :param model_timing: (int|None) Timing model version, or None to use the model's own default.
        :return: (tuple) (result, model_pos_used, model_angle_used, model_timing_used)

        """
        if self.__cs is None:
            raise ValueError("Cued Speech rules is not defined.")

        PathwayCodeImagesModel.cleanup_tmp()

        p = PathwayCodeVideoModel(self.__cs)
        if model_timing is not None:
            p.set_whenpredictor_version(model_timing)
        if model_pos is not None:
            p.set_wherepositionpredictor_version(model_pos)
        if model_angle is not None:
            p.set_whereanglepredictor_version(model_angle)

        _result = p.generate(cuedkeys, cuedphons)
        return (
            _result,
            p.get_wherepositionpredictor_version(),
            p.get_whereanglepredictor_version(),
            p.get_whenpredictor_version()
        )

    # -----------------------------------------------------------------------

    def test_overlay_available(self) -> str:
        """Test whether overlay generation is available, and why not otherwise.

        Overlay generation requires opencv/numpy and hand-set resources
        (environment); it also requires the current language's vowel codes
        to be covered by the position/angle prediction models (content).
        This attempts a real instantiation and lets it fail, rather than
        duplicating the checks already done by the underlying classes.

        :return: (str) One of REASON_AVAILABLE, REASON_NOT_INSTALLED
                 (environment) or REASON_NOT_IMPLEMENTED (this language).

        """
        if self.__cs is None:
            raise ValueError("Cued Speech rules is not defined.")

        try:
            PathwayCodeOverlayModel(self.__cs)
        except sppasKeyError as e:
            logging.exception(e)
            return TextCueSModel.REASON_NOT_IMPLEMENTED
        except Exception as e:
            logging.exception(e)
            return TextCueSModel.REASON_NOT_INSTALLED

        return TextCueSModel.REASON_AVAILABLE

    # -----------------------------------------------------------------------

    def test_video_available(self) -> str:
        """Test whether video generation is available, and why not otherwise.

        Video generation requires opencv/numpy, ffmpeg and hand-set
        resources (environment); it also requires the current language's
        vowel codes to be covered by the position/angle prediction models
        (content). This attempts a real instantiation and lets it fail,
        rather than duplicating the checks already done by the underlying
        classes.

        :return: (str) One of REASON_AVAILABLE, REASON_NOT_INSTALLED
                 (environment) or REASON_NOT_IMPLEMENTED (this language).

        """
        if self.__cs is None:
            raise ValueError("Cued Speech rules is not defined.")

        try:
            PathwayCodeVideoModel(self.__cs)
        except sppasKeyError as e:
            logging.exception(e)
            return TextCueSModel.REASON_NOT_IMPLEMENTED
        except Exception as e:
            logging.exception(e)
            return TextCueSModel.REASON_NOT_INSTALLED

        if self.__test_positions_complete() is False:
            return TextCueSModel.REASON_NOT_IMPLEMENTED

        return TextCueSModel.REASON_AVAILABLE

    # -----------------------------------------------------------------------

    def __test_positions_complete(self) -> bool:
        """Test whether every vowel code required by the current language is computable.

        Unlike overlay/images, a video can't fall back to a default image
        for a missing shape or position: a single unsupported code (e.g.
        'sf'/'sd', not implemented for English) must disable the whole mode,
        not just degrade one frame. Each required code is tried once, rather
        than duplicating the checks already done by the underlying classes.

        :return: (bool) True if every code required by the current CS rules
                 can be predicted, for both position and angle.

        """
        codes = self.__cs.get_vowels_codes()

        pos_predictor = WhereVowelPositionsPredictor()
        angle_predictor = WhereAnglesPredictor()

        for code in codes:
            try:
                pos_predictor.set_sights_and_predict_coords(None, (code,))
                pos_predictor.get_vowel_coords(code)
                angle_predictor.predict_angle_values((code,))
                angle_predictor.get_angle(code)
            except Exception as e:
                logging.exception(e)
                return False

        return True

    # -----------------------------------------------------------------------

    @staticmethod
    def get_default_models() -> tuple:
        """Return the default (model_pos, model_angle, model_timing) versions.

        These defaults are those of the underlying Cued Speech prediction
        systems themselves: this application does not invent them.

        :return: (tuple) (model_pos, model_angle, model_timing)

        """
        return (
            WhereVowelPositionsPredictor.DEFAULT_VERSION,
            WhereAnglesPredictor.DEFAULT_VERSION,
            WhenTransitionPredictor.DEFAULT
        )

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
