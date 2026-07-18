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

from sppas.core.config import paths
from sppas.src.resources import sppasDictPron

from sppas.ui.swapp.app_cues_utils.models.text_normalizer import CueingTextNormalizer
from sppas.ui.swapp.app_cues_utils.models.phonetizer import CueingPhonetizer

# ---------------------------------------------------------------------------


class PathwayTextModel:
    """Generates normalization and phonetization results for a given text.

    """

    def __init__(self):
        """Create a new instance."""
        self.__lang = "und"
        self.__normalizer = CueingTextNormalizer()

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

        The implementation lives in
        :class:`sppas.ui.swapp.app_cues_utils.models.text_normalizer.CueingTextNormalizer`.

        :param text: (str) Input text to be normalized
        :return: (list) List of tokens

        """
        return self.__normalizer.normalize(self.__lang, text)

    # ---------------------------------------------------------------------------

    def _phonetizer(self, text: str) -> list:
        """Return the result of "Phonetization" on the given normalized text.

        The phonetizer implementation lives in
        :class:`sppas.ui.swapp.app_cues_utils.models.phonetizer.CueingPhonetizer`.
        Known tokens get their dictionary pronunciation(s); unknown tokens
        get up to 4 generated variants.

        :param text: (str) Normalized text to be phonetized
        :return: (list) List of pronunciations

        """
        lang = self.__lang
        if lang == "fra":
            lang = "fre"
        pdict_file = os.path.join(paths.resources, 'dict', lang + '.dict')
        pdict = sppasDictPron(pdict_file, nodump=False)

        phonetizer = CueingPhonetizer(pdict)

        # Phonetization of the given input normalized text
        results = list()
        for line in text.split("#"):
            results.extend(phonetizer.phonetize(line.split(' ')))

        return results
