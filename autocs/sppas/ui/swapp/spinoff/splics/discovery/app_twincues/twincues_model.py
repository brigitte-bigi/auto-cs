"""
:filename: sppas.ui.swapp.spinoff.splics.discovery.app_twincues.twincues_model.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Main model of "TwinCueS" app.

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

from sppas.core.coreutils import ISO639
from sppas.core.config import paths
from sppas.core.config import separators
from sppas.src.annotations import sppasParam
from sppas.src.annotations.CuedSpeech import CuedSpeechKeys
from sppas.src.annotations.CuedSpeech.whatkey import CueingWordKeys
from sppas.src.resources import sppasDictPron

from sppas.ui.swapp.spinoff.splics.models.text_normalizer import CueingTextNormalizer
from sppas.ui.swapp.spinoff.splics.models.phonetizer import CueingPhonetizer
from sppas.ui.swapp.spinoff.splics.models.images_model import KeyPianoImagesModel
from sppas.ui.swapp.spinoff.splics.models.key_candidates import NIL_CONSONANT_CODES
from sppas.ui.swapp.spinoff.splics.models.key_candidates import NIL_VOWEL_CODES
from sppas.ui.swapp.spinoff.splics.models.key_candidates import NO_PHONEME_MARKER
from sppas.ui.swapp.spinoff.splics.models.key_candidates import build_key_candidates

from .twincues_msg import MSG_ERROR_INVALID_CUE
from .twincues_msg import MSG_ERROR_INVALID_WORD
from .models.word2cues_model import Word2CuesModel
from .models.cues2words_model import Cues2WordsModel

# ---------------------------------------------------------------------------


class TwinCueSModel:
    """Model for the TwinCueS application.

    Loads a pronunciation dictionary for the current language, computes the
    Cued Speech cue of each of its entries, and builds the index required to
    answer both conversion directions: word -> twin words, and cue -> words.

    """

    def __init__(self):
        """Create the model to convert a word into a cue, and a cue into a word."""
        annotation_id = "cuedspeech"
        config_name = annotation_id + ".json"
        self._parameters = sppasParam([config_name])
        self._ann_step_idx = self._parameters.activate_annotation(annotation_id)

        self.__lang = None
        self.__word2cues = None
        self.__cues2words = None
        self.__valid_shapes = set()
        self.__valid_positions = set()
        self.__cued_rules = None
        self.__cons_by_shape = None
        self.__vow_by_pos = None
        self.__cons_absent = None
        self.__vow_absent = None
        self.__max_cue_length = 0
        self.__normalizer = CueingTextNormalizer()

    # -----------------------------------------------------------------------

    def get_langlist(self) -> list:
        """Return the list of supported language codes."""
        return self._parameters.get_langlist(self._ann_step_idx)

    # -----------------------------------------------------------------------

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

    def set_lang(self, lang: str) -> None:
        """Fix the language and (re)build the word/cue index if needed.

        The index is only rebuilt when the language actually changes: building
        it requires computing the cue of every entry of the pronunciation
        dictionary, which is costly.

        :param lang: (str) The language code.
        :raises: KeyError: Unsupported language.
        :raises: FileNotFoundError: Missing Cued Speech rule file.

        """
        if lang not in self.get_lang_choices():
            raise KeyError(f"Language {lang} is not supported.")

        if lang == self.__lang:
            return

        self._parameters.set_lang(lang, self._ann_step_idx)
        rule_file = self._parameters.get_langresource(self._ann_step_idx)[0]
        if os.path.exists(rule_file) is False:
            raise FileNotFoundError(f"CuedSpeech resource file {rule_file} not found.")
        cued_rules = CuedSpeechKeys(rule_file)

        dict_lang = lang
        if lang == "fra":
            dict_lang = "fre"
        pdict_file = os.path.join(paths.resources, "dict", dict_lang + ".dict")
        if os.path.exists(pdict_file) is False:
            raise FileNotFoundError(f"Pronunciation dictionary {pdict_file} not found.")
        pdict = sppasDictPron(pdict_file, nodump=False)

        sound_model = CueingWordKeys(cued_rules)
        phonetizer = CueingPhonetizer(pdict)

        cue_index, attested = self.__build_index(sound_model, pdict)
        self.__word2cues = Word2CuesModel(phonetizer, sound_model, cue_index)
        self.__cues2words = Cues2WordsModel(cue_index)
        self.__max_cue_length = max((len(_cue) for _cue in cue_index), default=0)

        cons_by_shape, cons_absent = build_key_candidates(
            cued_rules.get_consonants_codes(), cued_rules, attested, NIL_CONSONANT_CODES)
        vow_by_pos, vow_absent = build_key_candidates(
            cued_rules.get_vowels_codes(), cued_rules, attested, NIL_VOWEL_CODES)

        self.__cons_by_shape = cons_by_shape
        self.__vow_by_pos = vow_by_pos
        self.__cons_absent = cons_absent
        self.__vow_absent = vow_absent
        self.__valid_shapes = set(cued_rules.get_consonants_codes())
        self.__valid_positions = set(cued_rules.get_vowels_codes())
        self.__cued_rules = cued_rules
        self.__lang = lang

    # -----------------------------------------------------------------------

    def word_to_cues(self, word: str) -> tuple:
        """Return, for each pronunciation of the given word, its cue and twins.

        The raw input is normalized into a token first (e.g. "parce que"
        becomes "parce_que"): the pronunciation dictionaries are indexed by
        tokens, not by raw words.

        :param word: (str) Word to be converted.
        :raises: ValueError: The language was not set, or the word is invalid.
        :return: (tuple) See :class:`Word2CuesModel.convert`.

        """
        if self.__word2cues is None:
            raise ValueError("The 'lang' was not defined in the model.")

        _tokens = self.__normalizer.normalize(self.__lang, word)
        if len(_tokens) != 1:
            raise ValueError(MSG_ERROR_INVALID_WORD.format(word))

        return self.__word2cues.convert(_tokens[0])

    # -----------------------------------------------------------------------

    def cues_to_words(self, cue: str) -> tuple:
        """Return the words sharing the given cue.

        :param cue: (str) Cue to be converted.
        :raises: ValueError: The language was not set, or the cue is invalid.
        :return: (tuple) See :class:`Cues2WordsModel.convert`.

        """
        if self.__cues2words is None:
            raise ValueError("The 'lang' was not defined in the model.")

        self.__validate_cue_format(cue)
        return self.__cues2words.convert(cue)

    # -----------------------------------------------------------------------

    def get_max_cue_length(self) -> int:
        """Return the character length of the longest cue in the current dictionary.

        A TwinCueS cue is a whole word's cue: its length is only bounded by
        the longest word actually indexed for the current language.

        :raises: ValueError: The language was not set.
        :return: (int) Max character length of a cue matching a real word.

        """
        if self.__cues2words is None:
            raise ValueError("The 'lang' was not defined in the model.")

        return self.__max_cue_length

    # -----------------------------------------------------------------------

    def get_shape_codes(self) -> tuple:
        """Return the piano's shape codes of the current language, in a stable display order.

        The neutral shape (no consonant) is excluded: it is a valid code when
        typing a cue by hand, but not a meaningful piano key.

        :raises: ValueError: The language was not set.
        :return: (tuple) Shape codes, e.g. ("1", ..., "8") for French.

        """
        if self.__cued_rules is None:
            raise ValueError("The 'lang' was not defined in the model.")

        _neutral = self.__cued_rules.get_neutral_consonant()
        return tuple(_code for _code in self.__cued_rules.get_consonants_codes() if _code != _neutral)

    # -----------------------------------------------------------------------

    def get_position_codes(self) -> tuple:
        """Return the piano's position codes of the current language, in a stable display order.

        The neutral position (no vowel) is excluded: it is a valid code when
        typing a cue by hand, but not a meaningful piano key.

        :raises: ValueError: The language was not set.
        :return: (tuple) Position codes, e.g. ("t", "s", "m", "c", "b") for French.

        """
        if self.__cued_rules is None:
            raise ValueError("The 'lang' was not defined in the model.")

        _neutral = self.__cued_rules.get_neutral_vowel()
        return tuple(_code for _code in self.__cued_rules.get_vowels_codes() if _code != _neutral)

    # -----------------------------------------------------------------------

    def get_shape_keys(self) -> tuple:
        """Return, for each shape code, its code, image, and matching phonemes.

        A shape that can also mean "no consonant at all" (the nil-consonant
        code) has "&empty;" appended to its phonemes, in addition to its
        real ones.

        :raises: ValueError: The language was not set.
        :return: (tuple) {"code": str, "image": str, "phonemes": tuple(str, ...)}, one per shape.

        """
        if self.__cons_by_shape is None:
            raise ValueError("The 'lang' was not defined in the model.")

        _result = list()
        for _code in self.get_shape_codes():
            _phonemes = self.__cons_by_shape.get(_code, tuple())
            if self.__cons_absent.get(_code, False) is True:
                _phonemes = _phonemes + (NO_PHONEME_MARKER,)
            _result.append({"code": _code, "image": KeyPianoImagesModel.shape_image(_code),
                            "phonemes": _phonemes})

        return tuple(_result)

    # -----------------------------------------------------------------------

    def get_position_keys(self) -> tuple:
        """Return, for each position code, its code, image, and matching phonemes.

        A position that can also mean "no vowel at all" (the nil-vowel code)
        has "&empty;" appended to its phonemes, in addition to its real ones.

        :raises: ValueError: The language was not set.
        :return: (tuple) {"code": str, "image": str, "phonemes": tuple(str, ...)}, one per position.

        """
        if self.__vow_by_pos is None:
            raise ValueError("The 'lang' was not defined in the model.")

        _result = list()
        for _code in self.get_position_codes():
            _phonemes = self.__vow_by_pos.get(_code, tuple())
            if self.__vow_absent.get(_code, False) is True:
                _phonemes = _phonemes + (NO_PHONEME_MARKER,)
            _result.append({"code": _code, "image": KeyPianoImagesModel.position_image(_code),
                            "phonemes": _phonemes})

        return tuple(_result)

    # -----------------------------------------------------------------------
    # Private
    # -----------------------------------------------------------------------

    def __validate_cue_format(self, cue: str) -> None:
        """Raise if the given cue does not match the language's key rules.

        A valid cue is made of one or more '<shape>-<position>' segments,
        separated by '.'. Both the shape and the position must be codes
        defined by the Cued Speech rules of the current language.

        :param cue: (str) Cue to be validated.
        :raises: ValueError: The cue is empty or does not match the expected format.

        """
        _cue = cue.strip()
        if len(_cue) == 0:
            raise ValueError(MSG_ERROR_INVALID_CUE.format(cue))

        for _segment in _cue.split(separators.syllables):
            _parts = _segment.split(separators.phonemes)
            if len(_parts) != 2:
                raise ValueError(MSG_ERROR_INVALID_CUE.format(cue))

            _shape, _position = _parts
            if _shape not in self.__valid_shapes or _position not in self.__valid_positions:
                raise ValueError(MSG_ERROR_INVALID_CUE.format(cue))

    @staticmethod
    def __build_index(sound_model: CueingWordKeys, pdict: sppasDictPron) -> tuple:
        """Build the cue->(word,pron) index, used to find the twins of a cue.

        The set of dictionary-attested phonemes is also collected in this
        same pass over the dictionary, since it is needed to feed the piano
        (see get_shape_keys()/get_position_keys()) and iterating the whole
        dictionary a second time just for that would be wasteful.

        :param sound_model: (CueingWordKeys) The Cued Speech key generator of the language.
        :param pdict: (sppasDictPron) The pronunciation dictionary of the language.
        :return: (tuple) (dict: cue -> tuple of (word, pronunciation), set of attested phonemes)

        """
        _cue_index = dict()
        _attested = set()

        for _word in pdict:
            if pdict.is_unk(_word) is True:
                continue

            _prons = pdict.get_pron(_word).split(separators.variants)
            for _pron in _prons:
                _attested.update(_pron.split(separators.phonemes))
                try:
                    _codes, _unused_phons = sound_model.annotate([_word], [_pron])
                    _cue = _codes[0]
                except Exception:
                    continue

                _cue_index.setdefault(_cue, list()).append((_word, _pron))

        _result = {_cue: tuple(_entries) for _cue, _entries in _cue_index.items()}
        return _result, _attested
