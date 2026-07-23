"""
:filename: sppas.ui.swapp.spinoff.splics.models.text_normalizer.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Normalize a raw input text into tokens, for a given language.

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

from sppas.core.config import paths
from sppas.src.resources import sppasDictRepl
from sppas.src.resources import sppasVocabulary
from sppas.src.annotations.TextNorm.normalize import TextNormalizer

# ---------------------------------------------------------------------------


class CueingTextNormalizer:
    """Turn a raw input text into a list of tokens, for a given language.

    A word entered by a user (e.g. "parce que") is not necessarily the token
    used as a key in the pronunciation dictionaries (e.g. "parce_que"): this
    class applies the same normalization SPPAS uses for full texts (known
    multi-word vocabulary entries, systematic replacements, punctuation and
    numbers) to a single word or short expression.

    """

    def normalize(self, lang: str, text: str) -> list:
        """Return the list of tokens obtained by normalizing the given text.

        :param lang: (str) Language of the text (iso639-3).
        :param text: (str) Raw input text.
        :raises: TypeError: Invalid text type.
        :return: (list) List of tokens.

        """
        if type(text) is not str:
            raise TypeError(f"Given text must be a string. Got '{text}' instead.")

        # Vocabulary of the given language
        vocab_file = os.path.join(paths.resources, 'vocab', lang + '.vocab')
        vocab = sppasVocabulary(vocab_file)
        # The normalizer
        normalizer = TextNormalizer(vocab, lang)

        # List of systematic replacements
        replace_file = os.path.join(paths.resources, "repl", lang + ".repl")
        if os.path.exists(replace_file) is True:
            repl = sppasDictRepl(replace_file, nodump=True)
            normalizer.set_repl(repl)

        # List of punctuations -- for removing
        punct_file = os.path.join(paths.resources, "vocab", "Punctuations.txt")
        if os.path.exists(punct_file):
            punct = sppasVocabulary(punct_file, nodump=True)
            normalizer.set_punct(punct)

        # Numbers to letters conversion
        number_filename = os.path.join(paths.resources, 'num', lang + '_num.repl')
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
