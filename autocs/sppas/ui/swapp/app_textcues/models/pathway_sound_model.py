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

from sppas.src.annotations.CuedSpeech.whatkey import CueingWordKeys

# ---------------------------------------------------------------------------


class PathwaySoundModel(CueingWordKeys):
    """Generates cuedspeech result for given (tokens, prons).

    The implementation lives in
    :class:`sppas.src.annotations.CuedSpeech.whatkey.CueingWordKeys`. This
    class is kept for backward compatibility of the TextCueS application.

    """
    pass
