# -*- coding: UTF-8 -*-
"""
:filename: sppas.src.annotations.CuedSpeech.whatkey.phonestokeys.py
:author:   Brigitte Bigi
:contact:  contact@sppas.org
:summary:  Apply Cued Speech rules to a sequence of phonemes.

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
from sppas.core.config import separators

from .keysrules import CuedSpeechCueingRules

# ----------------------------------------------------------------------------


class CuedSpeechKeys(CuedSpeechCueingRules):
    """Cued Speech keys generation from a sequence of phonemes.

    :Example:

        >>> # Define the input: a list of phonemes
        >>> phonemes = ["#", "s", "p", "a", "s"]
        >>> # Create the instance
        >>> self.lfpc = CuedSpeechKeys(FRA_KEYS)
        >>> # Apply the rules to get result in various formats
        >>> sgmts = self.lfpc.syllabify(phonemes)
        >>> [(1, 1), (2, 3), (4, 4)]
        >>> phons = self.lfpc.phonetize_syllables(phonemes, sgmts)
        >>> "s-vnil.p-a.s-vnil"
        >>> keys = self.lfpc.keys_phonetized(phons)
        >>> "3-s.1-s.3-s"

    """

    def __init__(self, keyrules_filename=None):
        """Create a new instance.

        Load keys from a text file, depending on the language and phonemes
        encoding. See documentation for details about this file.

        :param keyrules_filename: (str) Name of the file with the list of keys.

        """
        super(CuedSpeechKeys, self).__init__(keyrules_filename)

    # -----------------------------------------------------------------------

    def syllabify(self, phonemes: list) -> list:
        """Return the key boundaries of a sequence of phonemes.

        Perform the segmentation of the sequence of phonemes into the
        syllables-structure of the Cued Speech coding scheme.
        A syllable structure is CV, or V or C.

        :exemple:
        >>> phonemes = ['b', 'O~', 'Z', 'u', 'R']
        >>> CuedSpeechKeys("fra-config-file").syllabify(phonemes)
        >>> [ (0, 1), (2, 3), (4, 4) ]

        :exemple:
        >>> phonemes = ['E', 'n', 'i:', 'h', 'w', 'E', 'r\\\\']
        >>> CuedSpeechKeys("eng-config-file").syllabify(phonemes)
        >>> [ (0, 0), (1, 2), (3, 5), (6, 6) ]

        :param phonemes: (list of str) List of phonemes
        :returns: list of tuples (begin index, end index)

        """
        # Convert a list of phonemes into a list of key classes.
        classes = [self.get_class(p) for p in phonemes]
        syll = list()

        spans = CuedSpeechKeys.compute_phonmerge_spans(phonemes, self)
        def _effective_class_and_len(index: int) -> tuple:
            span = spans.get(index, None)
            if span is None:
                return classes[index], 1
            return span[1], span[0]

        i = 0
        while i < len(phonemes):
            c, span_len = _effective_class_and_len(i)
            # c = classes[i]

            # Syllables are made of phonemes exclusively, i.e. 'C','V','W' classes.
            # Not neutral.
            if c in ("W", "V", "C"):
                if c in ("V", "W") or i + span_len >= len(phonemes):
                    # Either the current phoneme is a vowel
                    # or it's the last in the list.
                    syll.append((i, i + span_len - 1))  # W, V, or C if last phoneme (or merged)
                else:
                    # The current phoneme is a consonant.
                    # See the next one to decide what is the segmentation.
                    i_next = i + span_len
                    c_next, span_len_next = _effective_class_and_len(i_next)

                    if c_next in ("V", "W"):
                        # The next phoneme is a vowel.
                        syll.append((i, i_next + span_len_next - 1))  # CV (with merges)
                        i += span_len + span_len_next
                        continue
                    else:
                        # Both cases:
                        #  - the next phoneme is a consonant
                        #  - the next phoneme is neither a vowel nor a consonant.
                        syll.append((i, i + span_len - 1))  # C (with merges)

            i += span_len

        return syll

    # -----------------------------------------------------------------------
    # Output formatting
    # -----------------------------------------------------------------------

    def phonetize_syllables(self, phonemes: list, syllables: list) -> str:
        """Return the phonetized sequence of syllables.

        The output string is using the X-SAMPA standard to indicate the
        phonemes and syllables segmentation.

        :example:
        >>> phonemes = ['b', 'O~', 'Z', 'u', 'R']
        >>> lpc_keys = CuedSpeechKeys("fra-config-file")
        >>> syllables = lpc_keys.syllabify(phonemes)
        >>> [ (0, 1), (2, 3), (4, 4) ]
        >>> lpc_keys.phonetize_syllables(phonemes, syllables)
        >>> "b-O~.Z-u.R-vnil"

        Notice that a diphtong implies 2 keys to be created!

        :example:
        >>> phonemes = [ '@', 'dZ', 'OI', 'n' ]
        >>> lpc_keys = CuedSpeechKeys("eng-config-file")
        >>> syllables = lpc_keys.syllabify(phonemes)
        >>> [ (0, 0), (1, 2), (3, 3) ]
        >>> lpc_keys.phonetize_syllables(phonemes, syllables)
        >>> "cnil-@.dZ-O.cnil-I.n-vnil"

        The challenging word: nonwhite: n A n h w aI t
        because
         - 'aI' is a diphtong (2 positions, 2 keys then), and
         - 'h-w' sequence is only one shape (one key then)!

        :param phonemes: (list) List of phonemes
        :param syllables: list of tuples (begin index, end index)
        :return: (str) String representing the syllables segmentation

        """
        str_syll = list()
        for (begin, end) in syllables:

            if begin == end:
                # A single phoneme. Either a 'C', or 'V' or 'W' key structure.
                p = phonemes[begin]
                c = self.get_class(p)

                if c == "W":
                    # Split the diphtong into 2 parts. Append into 2 syllables: 'V' + 'V'
                    if len(p) > 1:
                        str_syll.append("cnil" + separators.phonemes + p[0])
                        str_syll.append("cnil" + separators.phonemes + p[1:])
                    else:
                        # we should never be here!
                        logging.error(f"Hum... the vowel {p} is declared in class 'W' but it can be split!")
                        str_syll.append("cnil" + separators.phonemes + p)

                elif c == "V":
                    str_syll.append("cnil" + separators.phonemes + p)

                else:
                    str_syll.append(p + separators.phonemes + "vnil")

            else:
                # A key spanning multiple phonemes:
                # - consonant + vowel,
                # - or consonant cluster + vowel (V or W),
                # - or consonant cluster only (merged consonants)
                span_phones = phonemes[begin:end + 1]
                last_phone = span_phones[-1]
                last_class = self.get_class(last_phone)

                if last_class in ("V", "W"):
                    consonant_items = self._merge_consonant_cluster(span_phones[:-1])
                    consonant_cluster = separators.phonemes.join(consonant_items)

                    if last_class == "W":
                        if len(last_phone) > 1:
                            str_syll.append(consonant_cluster + separators.phonemes + last_phone[0])
                            str_syll.append("cnil" + separators.phonemes + last_phone[1:])
                        else:
                            logging.error(
                                f"Hum... the vowel {last_phone} is declared in class 'W' but it can be split!"
                            )
                            str_syll.append(consonant_cluster + separators.phonemes + last_phone)
                    else:
                        str_syll.append(consonant_cluster + separators.phonemes + last_phone)

                else:
                    consonant_items = self._merge_consonant_cluster(span_phones)
                    consonant_cluster = separators.phonemes.join(consonant_items)
                    str_syll.append(consonant_cluster + separators.phonemes + "vnil")

        return separators.syllables.join(str_syll)

    def _merge_consonant_cluster(self, phones: list) -> list:
        merged = list()
        i = 0
        while i < len(phones):
            if i + 1 < len(phones):
                eff = self.get_merged_class((phones[i], phones[i + 1]))
                if eff == 'C':
                    merged.append(phones[i] + phones[i + 1])
                    i += 2
                    continue
            merged.append(phones[i])
            i += 1
        return merged

    # -----------------------------------------------------------------------

    def keys_phonetized(self, phonetized_syllables: str) -> str:
        """Return the keys of a phonetized syllable as C-V sequences.

        The input string is using the X-SAMPA standard to indicate the
        phonemes and syllables segmentation.

        :example:
        >>> phonetized_syllable = "cnil-e.p-a.R-vnil"
        >>> lpc_keys = CuedSpeechKeys("fra-config-file")
        >>> lpc_keys.keys_phonetized(phonetized_syllable)
        >>> "0-t.1-s.3-s"

        :example:
        >>> phonetized_syllable = "cnil-E.n-i:.hw-E.r\-vnil"
        >>> lpc_keys = CuedSpeechKeys("eng-config-file")
        >>> lpc_keys.keys_phonetized(phonetized_syllable)
        >>> "5-c.4-m.4-c.3-s"

        :param phonetized_syllables: (str) String representing the keys segments
        :return: (str)

        """
        key_codes = list()
        for syll in phonetized_syllables.split(separators.syllables):
            try:
                phones = syll.split(separators.phonemes)
                if len(phones) == 2:
                    if self.get_class(phones[1]) == "W":
                        (c1, v1), (c2, v2) = self.syll_to_key(syll)
                        key_codes.append(c1 + separators.phonemes + v1)
                        key_codes.append(c2 + separators.phonemes + v2)
                    else:
                        consonant, vowel = self.syll_to_key(syll)
                        key_codes.append(consonant + separators.phonemes + vowel)
                else:
                    logging.error(f"Syllables must have two phonemes. Ignored: {syll}")
            except ValueError as e:
                import traceback
                logging.warning(str(e))
                key_codes.append(separators.phonemes)

        return separators.syllables.join(key_codes)

    # -----------------------------------------------------------------------

    @staticmethod
    def compute_phonmerge_spans(phonemes: list, rules: CuedSpeechCueingRules) -> dict:
        """Return the best merge span starting at each index.

        The input phonemes list is NEVER modified.
        A span is defined only if the rules contain a PHONMERGE entry.
        The "best" span is the longest matching sequence starting at index i.

        :param phonemes: (list) Sequence of phonemes (strings).
        :param rules: (CuedSpeechCueingRules) Rules containing PHONMERGE entries.
        :return: (dict) Mapping start_index -> (length, effective_class).

        """
        spans = dict()

        for i in range(len(phonemes)):

            best_len = 0
            best_class = None

            for length in range(2, len(phonemes) - i + 1):
                seq = tuple(phonemes[i:i + length])
                cls = rules.get_merged_class(seq)
                if cls is None:
                    continue
                if length > best_len:
                    best_len = length
                    best_class = cls

            if best_len > 0:
                spans[i] = (best_len, best_class)

        return spans

