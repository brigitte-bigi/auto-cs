"""
:filename: sppas.ui.swapp.app_textcues.models.video_model.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Generate a video for the given sequence of keys.

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

from sppas.src.annotations.CuedSpeech import CuedSpeechKeys
from sppas.src.annotations.CuedSpeech.wherecue.positions import WhereVowelPositionsPredictor
from sppas.src.annotations.CuedSpeech.wherecue.angles import WhereAnglesPredictor

# ---------------------------------------------------------------------------


class PathwayCodeVideoModel:
    """Generates image results for a given cued sequence.

    """

    def __init__(self, cued_rules: CuedSpeechKeys):
        """Create a new instance.

        :param cued_rules: (CuedSpeechKeys) The rules of the cued speech.

        """
        if isinstance(cued_rules, CuedSpeechKeys) is False:
            raise TypeError(f"Given cued_rules must be a CuedSpeechKeys object. Got {type(cued_rules)} instead.")
        self.__cs = cued_rules

        self._model_pos = WhereVowelPositionsPredictor()
        self._model_angle = WhereAnglesPredictor()

    # -----------------------------------------------------------------------

    def generate(self, cuedkeys: tuple, model_pos: int, model_angle: int, model_timing: int) -> tuple:
        raise NotImplementedError

