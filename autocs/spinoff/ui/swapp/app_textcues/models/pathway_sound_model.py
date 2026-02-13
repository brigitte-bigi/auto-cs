"""
:filename: sppas.ui.swapp.app_textcues.models.pathway_sound_model.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Perform Alignement and Cued Speech on given phonetized text.

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

from sppas.core.config import symbols
from sppas.src.annotations.Align.aligners import BasicAligner
from sppas.src.annotations.CuedSpeech import CuedSpeechKeys
from sppas.src.annotations.CuedSpeech.whatkey.keysbytoken import CueingPronTokenizer
from sppas.src.annotations.CuedSpeech.whatkey.keysbytoken import CueingKeysByToken

# ---------------------------------------------------------------------------


class PathwaySoundModel:
    """Generates cuedspeech result for given (tokens, prons).

    """

    def __init__(self, cued_rules: CuedSpeechKeys):
        """Create a new instance.

        :param cued_rules: (CuedSpeechKeys) The rules of the cued speech.

        """
        if isinstance(cued_rules, CuedSpeechKeys) is False:
            raise TypeError(f"Given cued_rules must be a CuedSpeechKeys object. "
                            f"Got {type(cued_rules)} instead.")
        self.__cs = cued_rules
        self.__cue_tokenizer = CueingPronTokenizer(self.__cs)
        self.__keys_by_token = CueingKeysByToken()

        self._stops = list(symbols.phone.keys())
        self._stops.append('#')
        self._stops.append('*')
        self._stops.append('@@')
        self._stops.append('+')
        self._stops.append('sil')
        self._stops.append('sp')
        self._stops.append('gb')
        self._stops.append('lg')
        self._stops.append('fp')
        self._stops.append('dummy')
        self._stops.append('noise')
        self._stops.append('laugh')

    # ---------------------------------------------------------------------------

    def annotate(self, tokens: list, prons: list) -> tuple:
        """Return the sequence of keys from the list of tokens and their pronunciations.

        Input tokens: ["test", "hello"]
        Input prons: ['t-E-s-t', 'E-l-o']
        Code result: [('5-c.3-s.5-c.6-s', 't-E.s-vnil.t-E.l-o')]
        Returned keys by token: (('5-c.3-s', '5-c.6-s'), ('t-E.s-vnil', 't-E.l-o'))

        :param tokens: (list) List of tokens
        :param prons: (list) List of pronunciations
        :raises: TypeError: Invalid text type.
        :return: tuple(str) List of keys

        """
        if type(prons) not in (list, tuple):
            raise TypeError(f"Given pronunciations must be a list. "
                            f"Got '{type(prons)}' instead.")

        if type(tokens) not in (list, tuple):
            raise TypeError(f"Given tokens must be a list. "
                            f"Got '{type(tokens)}' instead.")

        cued = self._cuer(prons)

        normalized_word_phonemes = self.__cue_tokenizer.normalize_word_phonemes(tuple(prons))
        codes, phons = self.__keys_by_token.segment(normalized_word_phonemes, cued)
        return codes, phons

    # ---------------------------------------------------------------------------
    # Private WORKERS
    # ---------------------------------------------------------------------------

    @staticmethod
    def _aligner(normalized: str, phonetized: str) -> list:
        """Choose the phonetization variant.

        :return: (list) List of (begin, end, phoneme)

        """
        if len(normalized) == 0:
            return list()

        aligner = BasicAligner()
        aligner.set_tokens(normalized)
        aligner.set_phones(phonetized)
        # Get selected pronunciation and pseudo time-alignment values
        aligned = aligner.run_basic()

        # The aligned result is a list of tuple(begin, end, phone) with
        # faked time values
        return aligned

    # ---------------------------------------------------------------------------

    def _cuer(self, token_prons: list) -> list:
        """Return the result of "CuedSpeech" on the given phonetized text.

        :param token_prons: (list) Pronunciation of each token.
        :return: (list) List of keys

        """
        results = list()
        prons = list()
        for token_pron in token_prons:
            prons.extend(token_pron.split("-"))
        phonemes = list()
        for p in prons:
            if p in self._stops:
                if len(phonemes) > 0:
                    sgmts = self.__cs.syllabify(phonemes)
                    phons = self.__cs.phonetize_syllables(phonemes, sgmts)
                    keys = self.__cs.keys_phonetized(phons)
                    results.append((keys, phons))
                    phonemes = list()
                ##### HACK ####
                if p in ("#", "sil", "lg", "laugh"):
                    # Code neutral key
                    results.append(("0-n", "cnil-"+p))
                else:
                    # Code neutral shape at side position
                    results.append(("0-s", "cnil-"+p))
            else:
                # A known phoneme. Aggregate.
                phonemes.append(p)

        # last segment
        if len(phonemes) > 0:
            sgmts = self.__cs.syllabify(phonemes)
            phons = self.__cs.phonetize_syllables(phonemes, sgmts)
            keys = self.__cs.keys_phonetized(phons)
            results.append((keys, phons))

        return results
