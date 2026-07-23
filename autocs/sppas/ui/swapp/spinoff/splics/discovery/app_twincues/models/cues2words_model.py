"""
:filename: sppas.ui.swapp.spinoff.splics.discovery.app_twincues.models.cues2words_model.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Return, for a given cue, the words sharing it.

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

# ---------------------------------------------------------------------------


class Cues2WordsModel:
    """Return the words sharing a given cue.

    """

    def __init__(self, cue_index: dict):
        """Create a new instance.

        :param cue_index: (dict) cue -> tuple of (word, pronunciation)

        """
        self.__cue_index = cue_index

    # -----------------------------------------------------------------------

    def convert(self, cue: str) -> tuple:
        """Return the words sharing the given cue.

        :param cue: (str) Cue to be converted.
        :return: (tuple) {"word": str, "pron": str}, one entry per matching word.

        """
        _cue = cue.strip()
        _entries = self.__cue_index.get(_cue, tuple())

        return tuple({"word": _w, "pron": _p} for _w, _p in _entries)
