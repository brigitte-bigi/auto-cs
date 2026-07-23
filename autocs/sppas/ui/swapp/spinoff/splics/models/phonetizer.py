"""
:filename: sppas.ui.swapp.spinoff.splics.models.phonetizer.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Phonetize tokens, including unknown ones, from a pronunciation dictionary.

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

from sppas.src.resources import sppasDictPron
from sppas.src.resources import sppasMapping
from sppas.src.annotations.Phon.phonetize import sppasDictPhonetizer

# ---------------------------------------------------------------------------


class CueingPhonetizer:
    """Return the pronunciation(s) of tokens, known or not, from a dictionary.

    This is the same phonetizer as used for full texts: if a token is a
    dictionary entry, its real pronunciation variants are returned; if not,
    up to 4 pronunciation variants are generated for it. The caller does not
    need to check dictionary membership: the phonetizer already handles both
    cases.

    """

    def __init__(self, pdict: sppasDictPron):
        """Create a new instance.

        :param pdict: (sppasDictPron) The pronunciation dictionary of the language.

        """
        self.__phonetizer = sppasDictPhonetizer(pdict, sppasMapping())
        self.__phonetizer.set_unk_variants(4)

    # -----------------------------------------------------------------------

    def phonetize(self, tokens: list) -> list:
        """Return the pronunciation variants string of each of the given tokens.

        Each returned string can contain several variants, separated by the
        standard variants separator (see :class:`sppas.core.config.separators`).

        :param tokens: (list) Tokens to be phonetized.
        :return: (list) One pronunciation variants string per token.

        """
        _results = self.__phonetizer.get_phon_tokens(tokens, phonunk=True)
        return [_p[1] for _p in _results]
