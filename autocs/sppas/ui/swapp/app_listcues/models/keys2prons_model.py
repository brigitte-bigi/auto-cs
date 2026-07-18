"""
:filename: sppas.ui.swapp.app_listcues.models.keys2prons_model.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Return, for a sequence of Cued Speech keys, its pronounceable
          phoneme sequences and the words sharing each of them.

..
    This file is part of Auto-CS: <https://autocs.sourceforge.io>
    -------------------------------------------------------------------------

    Copyright (C) 2026  Brigitte Bigi, CNRS
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

# ---------------------------------------------------------------------------

# A shape/position candidate of "None" means "no consonant"/"no vowel":
# the key does not produce a sound for that component.
ABSENT = None

# ---------------------------------------------------------------------------


class Keys2PronsModel:
    """Return the pronounceable phoneme sequences of a key sequence, and their words.

    A key ("<shape>-<position>") is ambiguous by design: several consonants
    can share the same shape, several vowels can share the same position.
    This model enumerates every phoneme sequence that the given key sequence
    can produce, discards the ones no window of which was ever observed in
    the dictionary, and reports the words sharing each of the remaining
    sequences, if any.

    """

    # Size of the trailing phoneme window checked against the
    # dictionary-attested n-grams while generating -- same idea as the
    # lattice pruning of an ASR system (Viterbi/Baum-Welch decoding): a
    # path is cut as soon as its last N phonemes were never observed
    # anywhere in the dictionary, since it can then never lead to a real
    # word. 3 phonemes still let the search explode on a highly ambiguous
    # 7-key cue; 4 keeps it tractable (measured: ~1.5M sequences in ~3s for
    # the worst case, instead of never terminating).
    NGRAM_SIZE = 4

    def __init__(self, cons_by_shape: dict, cons_absent: dict,
                vow_by_pos: dict, vow_absent: dict,
                ngrams: set, pron_index: dict):
        """Create a new instance.

        :param cons_by_shape: (dict) shape code -> tuple of dictionary-attested consonants
        :param cons_absent: (dict) shape code -> True if the shape can mean "no consonant"
        :param vow_by_pos: (dict) position code -> tuple of dictionary-attested vowels
        :param vow_absent: (dict) position code -> True if the position can mean "no vowel"
        :param ngrams: (set) Phoneme windows of NGRAM_SIZE actually observed in the dictionary.
        :param pron_index: (dict) phoneme sequence (tuple) -> tuple of words

        """
        self.__cons_by_shape = cons_by_shape
        self.__cons_absent = cons_absent
        self.__vow_by_pos = vow_by_pos
        self.__vow_absent = vow_absent
        self.__ngrams = ngrams
        self.__pron_index = pron_index

    # -----------------------------------------------------------------------

    def convert(self, keys: tuple) -> tuple:
        """Return the pronounceable phoneme sequences of the given keys, and their words.

        :param keys: (tuple) Sequence of (shape, position) tuples.
        :return: (tuple) One entry per pronounceable phoneme sequence:
                 {"pron": str, "words": tuple(str, ...)}

        """
        _options = [self.__key_options(_shape, _pos) for _shape, _pos in keys]

        _sequences = list()
        self.__generate(_options, 0, list(), _sequences)

        _result = list()
        for _seq in _sequences:
            _pron = separators.phonemes.join(_seq)
            _words = self.__pron_index.get(tuple(_seq), tuple())
            _result.append({"pron": _pron, "words": _words})

        return tuple(_result)

    # -----------------------------------------------------------------------
    # Private
    # -----------------------------------------------------------------------

    def __key_options(self, shape: str, position: str) -> list:
        """Return the (consonant, vowel) candidates of a single key.

        :param shape: (str) Shape code of the key.
        :param position: (str) Position code of the key.
        :return: (list) List of (consonant or ABSENT, vowel or ABSENT) tuples.

        """
        _cons = list(self.__cons_by_shape.get(shape, tuple()))
        if self.__cons_absent.get(shape, False) is True:
            _cons.append(ABSENT)

        _vows = list(self.__vow_by_pos.get(position, tuple()))
        if self.__vow_absent.get(position, False) is True:
            _vows.append(ABSENT)

        return [(_c, _v) for _c in _cons for _v in _vows if not (_c is ABSENT and _v is ABSENT)]

    # -----------------------------------------------------------------------

    def __generate(self, options: list, index: int, current_seq: list, sequences: list) -> None:
        """Depth-first generation of the phoneme sequences, pruned by n-gram plausibility.

        :param options: (list) Per-key list of (consonant, vowel) candidates.
        :param index: (int) Index of the key being expanded.
        :param current_seq: (list) Phonemes decided so far.
        :param sequences: (list) Collected complete phoneme sequences.

        """
        if index == len(options):
            sequences.append(list(current_seq))
            return

        for _cons, _vow in options[index]:
            _next_seq = current_seq \
                + ([_cons] if _cons is not ABSENT else []) \
                + ([_vow] if _vow is not ABSENT else [])

            if self.__is_plausible(_next_seq) is False:
                continue

            self.__generate(options, index + 1, _next_seq, sequences)

    # -----------------------------------------------------------------------

    def __is_plausible(self, sequence: list) -> bool:
        """Return False if the trailing phoneme window was never observed in the dictionary.

        :param sequence: (list) Phonemes decided so far.
        :return: (bool)

        """
        if len(sequence) < Keys2PronsModel.NGRAM_SIZE:
            return True

        return tuple(sequence[-Keys2PronsModel.NGRAM_SIZE:]) in self.__ngrams
