"""
:filename: sppas.ui.swapp.app_twincues.models.word2cues_model.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Return, for a given word, its cue(s) and the twin words sharing it.

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

from sppas.core.config import separators
from sppas.src.annotations.CuedSpeech.whatkey import CueingWordKeys

from sppas.ui.swapp.app_cues_utils.models.phonetizer import CueingPhonetizer

# ---------------------------------------------------------------------------


class Word2CuesModel:
    """Return the cue(s) of a word and its twin words.

    The word is phonetized on demand (known words get their dictionary
    pronunciation(s), unknown words get generated variants -- the phonetizer
    itself makes the distinction, there is no dictionary lookup here). A
    "twin word" is another word of the dictionary sharing the same cue, for
    one of the resulting pronunciations.

    """

    def __init__(self, phonetizer: CueingPhonetizer, sound_model: CueingWordKeys, cue_index: dict):
        """Create a new instance.

        :param phonetizer: (CueingPhonetizer) Phonetizer of the current language.
        :param sound_model: (CueingWordKeys) Cued Speech key generator of the current language.
        :param cue_index: (dict) cue -> tuple of (word, pronunciation)

        """
        self.__phonetizer = phonetizer
        self.__sound_model = sound_model
        self.__cue_index = cue_index

    # -----------------------------------------------------------------------

    def convert(self, word: str) -> tuple:
        """Return, for each distinct cue of the given word, its pronunciations and twins.

        Different pronunciations of the same word can be coded exactly the
        same way (e.g. French "petit" said /pti/ or /p@ti/): they are
        grouped under their shared cue instead of being reported -- and
        matched against twins -- twice with identical results.

        :param word: (str) Word to be converted.
        :return: (tuple) One entry per distinct cue of the word:
                 {"prons": tuple(str, ...), "cue": str, "twins": tuple({"word": str, "pron": str}, ...)}

        """
        _word = word.strip().lower()
        _variants = self.__phonetizer.phonetize([_word])[0]
        _prons = _variants.split(separators.variants)

        _prons_by_cue = dict()
        _cue_order = list()
        for _pron in _prons:
            _codes, _unused_phons = self.__sound_model.annotate([_word], [_pron])
            _cue = _codes[0]
            if _cue not in _prons_by_cue:
                _prons_by_cue[_cue] = list()
                _cue_order.append(_cue)
            _prons_by_cue[_cue].append(_pron)

        _result = list()
        for _cue in _cue_order:
            _twins = tuple(
                {"word": _w, "pron": _p}
                for _w, _p in self.__cue_index.get(_cue, tuple())
                if _w != _word
            )
            _result.append({"prons": tuple(_prons_by_cue[_cue]), "cue": _cue, "twins": _twins})

        return tuple(_result)
