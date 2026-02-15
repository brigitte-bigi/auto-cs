"""
:filename: sppas.ui.swapp.app_textcues.models.pathway_text_model.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Perform Normalization and Phonetization given "Input Lang & Text".

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

from sppas.core.config import symbols
from sppas.core.config import paths
from sppas.src.resources import sppasDictRepl
from sppas.src.resources import sppasVocabulary
from sppas.src.resources import sppasDictPron
from sppas.src.resources import sppasMapping
from sppas.src.annotations.TextNorm.normalize import TextNormalizer
from sppas.src.annotations.Phon.phonetize import sppasDictPhonetizer

# ---------------------------------------------------------------------------


class PathwayTextModel:
    """Generates normalization and phonetization results for a given text.

    """

    def __init__(self):
        """Create a new instance."""
        self.__lang = "und"

    # ---------------------------------------------------------------------------

    def annotate(self, lang: str, text: str) -> tuple:
        """Return the list of tokens and their pronunciations.

        :param lang: (str) Language of the text (iso639-1)
        :param text: (str) Raw input text
        :raises: TypeError: Invalid text type.
        :raises: Exception: Invalid result.
        :return: tuple(list, list) List of tokens and pronunciations

        """
        if type(text) is not str:
            raise TypeError(f"Given text must be a string. Got '{text}' instead.")

        self.__lang = lang
        tokens = self._normalizer(text)
        prons = self._phonetizer(" ".join(tokens))
        return tokens, prons

    # ---------------------------------------------------------------------------
    # Private WORKERS
    # ---------------------------------------------------------------------------

    def _normalizer(self, text: str) -> list:
        """Return the result of "Text Normalization" on the given text.

        :param text: (str) Input text to be normalized
        :return: (list) List of tokens

        """
        # Vocabulary of the given language
        vocab_file = os.path.join(paths.resources, 'vocab', self.__lang + '.vocab')
        vocab = sppasVocabulary(vocab_file)
        # The normalizer
        normalizer = TextNormalizer(vocab, self.__lang)

        # List of systematic replacements
        replace_file = os.path.join(paths.resources, "repl", self.__lang + ".repl")
        if os.path.exists(replace_file) is True:
            repl = sppasDictRepl(replace_file, nodump=True)
            normalizer.set_repl(repl)

        # List of punctuations -- for removing
        punct_file = os.path.join(paths.resources, "vocab", "Punctuations.txt")
        if os.path.exists(punct_file):
            punct = sppasVocabulary(punct_file, nodump=True)
            normalizer.set_punct(punct)

        # Numbers to letters conversion
        number_filename = os.path.join(paths.resources, 'num', self.__lang + '_num.repl')
        if os.path.exists(number_filename) is True:
            numbers = sppasDictRepl(number_filename, nodump=True)
            normalizer.set_num(numbers)

        # Custom options
        normalizer.set_delim("_")   # default is '_'

        # Text Normalization of the input text. The result is a list.
        _toks = normalizer.normalize(text)

        # The text is not en Enriched Ortho. Transcription.
        # IMPORTANT: Remove EOT symbols.
        _tokens = list()
        for _t in _toks:
            if _t not in ('@', '+', '#', '*'):
                _tokens.append(_t)
        return _tokens

    # ---------------------------------------------------------------------------

    def _phonetizer(self, text: str) -> list:
        """Return the result of "Phonetization" on the given normalized text.

        :param text: (str) Normalized text to be phonetized
        :return: (list) List of pronunciations

        """
        lang = self.__lang
        if lang == "fra":
            lang = "fre"
        pdict_file = os.path.join(paths.resources, 'dict', lang + '.dict')
        pdict = sppasDictPron(pdict_file, nodump=False)

        # A mapping table: sampa -> IPA for example: map_table = sppasMapping(file)
        mapping = sppasMapping()
        # The phonetizer
        phonetizer = sppasDictPhonetizer(pdict, mapping)
        # Custom options: number of phonetization variants
        phonetizer.set_unk_variants(4)
        # Phonetization of the given input normalized text
        results = list()
        for line in text.split("#"):
            # the result is a list of tuple(token, phones, status)
            # status (int): annots.ok or annots.warning or annots.error
            results.extend(phonetizer.get_phon_tokens(line.split(' '), phonunk=True))

        # The result of phonetization is a list of tuple(token, phones, status)
        return [p[1] for p in results]
