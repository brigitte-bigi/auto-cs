"""
:filename: sppas.ui.swapp.spinoff.splics.discovery.app_listcues.listcues_model.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Main model of "ListCueS" app.

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
import os

from sppas.core.coreutils import ISO639
from sppas.core.config import paths
from sppas.core.config import separators
from sppas.src.annotations import sppasParam
from sppas.src.annotations.CuedSpeech import CuedSpeechKeys
from sppas.src.resources import sppasDictPron

from sppas.ui.swapp.spinoff.splics.models.images_model import KeyPianoImagesModel
from sppas.ui.swapp.spinoff.splics.models.key_candidates import NIL_CONSONANT_CODES
from sppas.ui.swapp.spinoff.splics.models.key_candidates import NIL_VOWEL_CODES
from sppas.ui.swapp.spinoff.splics.models.key_candidates import NO_PHONEME_MARKER
from sppas.ui.swapp.spinoff.splics.models.key_candidates import build_key_candidates

from .listcues_msg import MSG_ERROR_INVALID_CUE
from .models.keys2prons_model import Keys2PronsModel

# ---------------------------------------------------------------------------


class ListCueSModel:
    """Model for the ListCueS application.

    Loads a pronunciation dictionary for the current language, restricts the
    Cued Speech key -> phoneme(s) rules to the phonemes actually attested in
    that dictionary, and builds the word index required to answer the only
    conversion direction of this application: a sequence of 1 to 7 keys ->
    its pronounceable phoneme sequences and the word(s) sharing each of them.

    """

    # Maximum number of keys accepted in an input cue.
    MAX_KEYS = 7

    def __init__(self):
        """Create the model to convert a sequence of keys into pronunciations."""
        annotation_id = "cuedspeech"
        config_name = annotation_id + ".json"
        self._parameters = sppasParam([config_name])
        self._ann_step_idx = self._parameters.activate_annotation(annotation_id)

        self.__lang = None
        self.__cued_rules = None
        self.__valid_shapes = set()
        self.__valid_positions = set()
        self.__keys2prons = None
        self.__cons_by_shape = None
        self.__vow_by_pos = None
        self.__cons_absent = None
        self.__vow_absent = None

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
        """Fix the language and (re)build the key/word index if needed.

        The index is only rebuilt when the language actually changes: building
        it requires iterating the whole pronunciation dictionary.

        :param lang: (str) The language code.
        :raises: KeyError: Unsupported language.
        :raises: FileNotFoundError: Missing Cued Speech rule file or dictionary.

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

        attested, pron_index, ngrams = self.__build_dict_index(pdict)
        cons_by_shape, cons_absent = build_key_candidates(
            cued_rules.get_consonants_codes(), cued_rules, attested, NIL_CONSONANT_CODES)
        vow_by_pos, vow_absent = build_key_candidates(
            cued_rules.get_vowels_codes(), cued_rules, attested, NIL_VOWEL_CODES)

        self.__keys2prons = Keys2PronsModel(
            cons_by_shape, cons_absent, vow_by_pos, vow_absent, ngrams, pron_index)
        self.__cons_by_shape = cons_by_shape
        self.__vow_by_pos = vow_by_pos
        self.__cons_absent = cons_absent
        self.__vow_absent = vow_absent
        self.__valid_shapes = set(cued_rules.get_consonants_codes())
        self.__valid_positions = set(cued_rules.get_vowels_codes())
        self.__cued_rules = cued_rules
        self.__lang = lang

    # -----------------------------------------------------------------------

    def keys_to_prons(self, cue: str) -> tuple:
        """Return the pronounceable phoneme sequences of the given key sequence, and their words.

        :param cue: (str) 1 to 7 '<shape>-<position>' segments separated by '.'.
        :raises: ValueError: The language was not set, or the cue is invalid.
        :return: (tuple) See :class:`Keys2PronsModel.convert`.

        """
        if self.__keys2prons is None:
            raise ValueError("The 'lang' was not defined in the model.")

        _keys = self.__parse_cue(cue)
        return self.__keys2prons.convert(_keys)

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

    def __parse_cue(self, cue: str) -> tuple:
        """Return the sequence of (shape, position) tuples of a validated cue.

        A valid cue is made of 1 to 7 '<shape>-<position>' segments, separated
        by '.'. Both the shape and the position must be codes defined by the
        Cued Speech rules of the current language.

        :param cue: (str) Cue to be validated and parsed.
        :raises: ValueError: The cue is empty, malformed, or has too many keys.
        :return: (tuple) Sequence of (shape, position) tuples.

        """
        _cue = cue.strip()
        if len(_cue) == 0:
            raise ValueError(MSG_ERROR_INVALID_CUE.format(cue))

        _segments = _cue.split(separators.syllables)
        if len(_segments) > ListCueSModel.MAX_KEYS:
            raise ValueError(MSG_ERROR_INVALID_CUE.format(cue))

        _keys = list()
        for _segment in _segments:
            _parts = _segment.split(separators.phonemes)
            if len(_parts) != 2:
                raise ValueError(MSG_ERROR_INVALID_CUE.format(cue))

            _shape, _position = _parts
            if _shape not in self.__valid_shapes or _position not in self.__valid_positions:
                raise ValueError(MSG_ERROR_INVALID_CUE.format(cue))

            _keys.append((_shape, _position))

        return tuple(_keys)

    # -----------------------------------------------------------------------

    @staticmethod
    def __build_dict_index(pdict: sppasDictPron) -> tuple:
        """Build the dictionary-attested phonemes, n-grams, and the pron->words index.

        The n-grams (see Keys2PronsModel.NGRAM_SIZE) are collected in this
        same pass over the dictionary: iterating it a second time just for
        that would be wasteful.

        :param pdict: (sppasDictPron) The pronunciation dictionary of the language.
        :return: (tuple) (set of attested phonemes, dict: phoneme tuple -> tuple of words,
                 set of attested phoneme n-grams)

        """
        _attested = set()
        _pron_index = dict()
        _ngrams = set()
        _n = Keys2PronsModel.NGRAM_SIZE

        for _word in pdict:
            if pdict.is_unk(_word) is True:
                continue

            _prons = pdict.get_pron(_word).split(separators.variants)
            for _pron in _prons:
                _phons = tuple(_pron.split(separators.phonemes))
                _attested.update(_phons)
                _pron_index.setdefault(_phons, list()).append(_word)
                for _i in range(len(_phons) - _n + 1):
                    _ngrams.add(_phons[_i:_i + _n])

        return (_attested,
                {_phons: tuple(_words) for _phons, _words in _pron_index.items()},
                _ngrams)

