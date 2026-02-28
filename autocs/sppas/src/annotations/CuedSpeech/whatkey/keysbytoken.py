"""
:filename: sppas.src.annotations.CuedSpeech.whatkey.keysbytoken.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Make keys segmented by tokens from an already cued text.

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

from .phonestokeys import CuedSpeechKeys

# ---------------------------------------------------------------------------


class _CueingRulesAdapter:
    """Normalize phoneme sequences for stable alignment with Cued Speech output.

    This helper applies the same transformations as the Cued Speech pipeline:
    - Split diphthongs (class 'W') into 2 vowel phones.
    - Merge specific consonant sequences when the rules define a single phone.

    :param cued_rules: (CuedSpeechKeys) The rules of the cued speech.

    """

    def __init__(self, cued_rules: CuedSpeechKeys):
        """Create a new instance.

        :param cued_rules: (CuedSpeechKeys) The rules of the cued speech.

        """
        if isinstance(cued_rules, CuedSpeechKeys) is False:
            raise TypeError(f"Given cued_rules must be a CuedSpeechKeys object. "
                            f"Got {type(cued_rules)} instead.")
        self.__cs = cued_rules

    # -----------------------------------------------------------------------

    def normalize_word_phones(self, phones: list) -> list:
        """Return a normalized list of phones for word-level alignment.

        :param phones: (list) List of phones of a word (split by '-').
        :return: (list) Normalized list of phones.

        """
        if isinstance(phones, list) is False:
            raise TypeError(f"Given phones must be a list. "
                            f"Got '{type(phones)}' instead.")

        normalized = list()
        i = 0
        while i < len(phones):

            current = phones[i]
            if isinstance(current, str) is False:
                raise TypeError("Each item of phones must be a str.")

            merged = self.__try_merge_sequence(phones, i)
            if merged is not None:
                normalized.append(merged)
                i += 2
                continue

            phone_class = self.__cs.get_class(current)
            if phone_class == 'W':
                split_items = self.__split_diphthong(current)
                for item in split_items:
                    normalized.append(item)
            else:
                normalized.append(current)

            i += 1

        return normalized

    # -----------------------------------------------------------------------
    # Private
    # -----------------------------------------------------------------------

    def __split_diphthong(self, phone: str) -> list:
        """Split a diphthong phone into two vowel phones.

        :param phone: (str) A phone declared in class 'W'.
        :return: (list) The two phones.

        """
        if len(phone) <= 1:
            return [phone]
        return [phone[0], phone[1:]]

    # -----------------------------------------------------------------------

    def __try_merge_sequence(self, phones: list, index: int):
        """Merge a 2-phones sequence into a single token when defined by rules.

        :param phones: (list) List of phones.
        :param index: (int) Index of the current phone.
        :return: (str or None) The merged token, or None.

        """
        if index + 1 >= len(phones):
            return None

        first = phones[index]
        second = phones[index + 1]
        effective_class = self.__cs.get_merged_class((first, second))
        if effective_class != 'C':
            return None

        return first + second


# ---------------------------------------------------------------------------


class CueingPronTokenizer:
    """Tokenize and normalize word pronunciations for stable Cued Speech alignment.

    This helper converts the per-word pronunciation strings (split with '-') into
    normalized strings, using CsNormalizationRules as the single normalization layer.

    """

    def __init__(self, key_rules: CuedSpeechKeys):
        """Create a new instance.

        """
        self.__rules = _CueingRulesAdapter(key_rules)

    # -----------------------------------------------------------------------

    def normalize_word_phonemes(self, word_phonemes: tuple) -> tuple:
        """Return normalized pronunciations for each word.

        Input example: ('w-aI-t', '@-dZ-OI-n', 'OI-l')
        Output example: ('w-a-I-t', '@-dZ-O-I-n', 'O-I-l')

        :param word_phonemes: (tuple) Pronunciation of each token, as '-' separated phones.
        :raises: ValueError: Invalid type or empty item.
        :return: (tuple) Normalized pronunciations, same token count as input.

        """
        if isinstance(word_phonemes, (list, tuple)) is False:
            raise ValueError('word_phonemes must be a tuple or list')

        normalized_items = list()

        for item in word_phonemes:

            if isinstance(item, str) is False:
                raise ValueError('Each item of word_phonemes must be a str')
            if len(item) == 0:
                raise ValueError('Empty pronunciation item in word_phonemes')

            phones = item.split('-')
            phones = [p for p in phones if len(p) > 0]
            if len(phones) == 0:
                raise ValueError('Empty phoneme list for a token.')

            normalized_phones = self.__rules.normalize_word_phones(phones)
            normalized_items.append('-'.join(normalized_phones))

        return tuple(normalized_items)

# ---------------------------------------------------------------------------


class CueingKeysByToken:
    """Segment an already cued text into per-token keys and per-token phones.

    The cueing result is a list of items: (keys_str, phones_str).
    Each string can contain multiple key pairs separated with '.'.

    The segmentation rule assigns each key to the token that consumes its vowel phones.

    """

    __PLACEHOLDER_CODE = '0-n'
    __PLACEHOLDER_PHON = 'cnil-vnil'

    def __init__(self):
        """Create a new instance."""
        pass

    # -----------------------------------------------------------------------

    def segment(self, word_phonemes: tuple, key_items: list) -> tuple:
        """Return per-token keys and per-token phones.

        :param word_phonemes: (tuple) Pronunciation of each token ('-' separated phones).
        :param key_items: (list) Cueing result: list of (keys_str, phones_str).
        :return: (tuple) (codes_by_token, phones_by_token), each is a tuple of strings ('.' separated).

        """
        words_phones = self.__parse_words(word_phonemes)
        flat_codes, flat_phons = self.__flatten_key_items(key_items)

        token_codes = [[] for _ in range(len(words_phones))]
        token_phons = [[] for _ in range(len(words_phones))]
        token_consumed = [False for _ in range(len(words_phones))]

        cursor = _PhonesCursor(words_phones, token_consumed)

        for i in range(len(flat_codes)):
            code_item = flat_codes[i]
            phon_item = flat_phons[i]

            consonants, vowels = self.__parse_key_pair(phon_item)
            token_index = None
            if len(consonants) > 0:
                token_index = cursor.consume(consonants, 'consonants')

            cursor.advance_if_done()

            if len(vowels) > 0:
                token_index = cursor.consume(vowels, 'vowels')
            if token_index is None:
                raise ValueError('Key has neither consonant nor vowel phones: ' + phon_item)

            token_codes[token_index].append(code_item)
            token_phons[token_index].append(phon_item)

        for i in range(len(words_phones)):
            if token_consumed[i] is True and len(token_codes[i]) == 0:
                token_codes[i].append(self.__PLACEHOLDER_CODE)
                token_phons[i].append(self.__PLACEHOLDER_PHON)

        codes_by_token = tuple(['.'.join(items) for items in token_codes])
        phons_by_token = tuple(['.'.join(items) for items in token_phons])

        return codes_by_token, phons_by_token

    # -----------------------------------------------------------------------
    # Private
    # -----------------------------------------------------------------------

    def __parse_words(self, word_phonemes: tuple) -> list:
        """Return a list of list of phones per token."""
        if isinstance(word_phonemes, (list, tuple)) is False:
            raise ValueError('word_phonemes must be a tuple or list')

        words = list()

        for item in word_phonemes:
            if isinstance(item, str) is False:
                raise ValueError('Each item of word_phonemes must be a str')

            phones = self.__split_non_empty(item, '-')
            if len(phones) == 0:
                raise ValueError('Empty phoneme list for a token')

            words.append(phones)

        if len(words) == 0:
            raise ValueError('word_phonemes is empty')

        return words

    # -----------------------------------------------------------------------

    def __flatten_key_items(self, key_items: list) -> tuple:
        """Return flat lists of codes and phones."""
        if isinstance(key_items, list) is False:
            raise ValueError('key_items must be a list')

        codes_flat = list()
        phons_flat = list()

        for item in key_items:
            if isinstance(item, (list, tuple)) is False or len(item) != 2:
                raise ValueError('Each item of key_items must be a (codes_str, phon_str) pair.')

            codes_str, phon_str = item

            if isinstance(codes_str, str) is False:
                raise ValueError('codes_str must be a str')
            if isinstance(phon_str, str) is False:
                raise ValueError('phon_str must be a str')

            codes = self.__split_non_empty(codes_str, '.')
            phons = self.__split_non_empty(phon_str, '.')

            if len(codes) != len(phons):
                raise ValueError(
                    "codes_str '" + codes_str + "' and phon_str '" + phon_str + "' do not have the same number of keys."
                )

            for c in codes:
                codes_flat.append(c)
            for p in phons:
                phons_flat.append(p)

        if len(codes_flat) == 0:
            raise ValueError('No key found in key_items')

        return codes_flat, phons_flat

    # -----------------------------------------------------------------------

    def __parse_key_pair(self, pair_str: str) -> tuple:
        """Return (consonants, vowels) lists from a 'C-V' pair string."""
        if isinstance(pair_str, str) is False:
            raise ValueError('Invalid key-phoneme pair: ' + str(pair_str))

        if pair_str.count('-') == 0:
            raise ValueError('Invalid key-phoneme pair: ' + pair_str)

        left, right = pair_str.split('-', 1)
        left = left.strip()
        right = right.strip()

        consonants = list()
        vowels = list()

        if left != 'cnil':
            consonants = self.__split_non_empty(left, '-')
        if right != 'vnil':
            vowels = self.__split_non_empty(right, '-')

        return consonants, vowels

    # -----------------------------------------------------------------------

    @staticmethod
    def __split_non_empty(value: str, sep: str) -> list:
        """Split and remove empty items."""
        out = list()
        for part in value.split(sep):
            if len(part) > 0:
                out.append(part)
        return out

# ---------------------------------------------------------------------------


class _PhonesCursor:
    """Consume expected phones from tokenized phones."""

    def __init__(self, words_phones: list, token_consumed: list):
        """Create a new cursor.

        :param words_phones: (list) List of token phones.
        :param token_consumed: (list) Mutable list of booleans per token.

        """
        self.__words = words_phones
        self.__token_consumed = token_consumed
        self.token_index = 0
        self.phone_index = 0

    # -----------------------------------------------------------------------

    def advance_if_done(self) -> None:
        """Advance to the next token when current token is fully consumed."""
        while self.token_index < len(self.__words) and self.phone_index >= len(self.__words[self.token_index]):
            self.token_index += 1
            self.phone_index = 0

    # -----------------------------------------------------------------------

    def consume(self, expected_phones: list, label: str) -> int:
        """Consume expected phones and return the token index where consumption started."""
        if len(expected_phones) == 0:
            raise ValueError('Empty expected list for ' + label)

        self.advance_if_done()

        if self.token_index >= len(self.__words):
            raise ValueError('Ran out of tokens while aligning ' + label)

        start_token = self.token_index

        for expected in expected_phones:

            self.advance_if_done()
            if self.token_index >= len(self.__words):
                raise ValueError('Ran out of tokens while aligning ' + label)

            current = self.__words[self.token_index][self.phone_index]
            if current != expected:
                raise ValueError('Alignment mismatch: expected ' + expected + ' got ' + current + ' in ' + label)

            self.__token_consumed[self.token_index] = True
            self.phone_index += 1

        return start_token
