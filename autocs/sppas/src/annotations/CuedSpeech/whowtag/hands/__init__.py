"""
:filename: sppas.src.annotations.CuedSpeech.whowtag.hands.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Cued speech hands.

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

from .handproperties import sppasHandProperties
from sppas.src.imgdata import sppasImageDataError
from sppas.core.config import cfg

if cfg.feature_installed("video") is True:
    from .handfilters import sppasHandFilters
    from .handsset import sppasHandsSet
else:

    class sppasHandFilters(sppasImageDataError):
        @staticmethod
        def get_filter_names() -> list:
            return []

    class sppasHandsSet(sppasImageDataError):
        pass

__all__ = (
    "sppasHandProperties",
    "sppasHandFilters",
    "sppasHandsSet"
)