"""
:filename: sppas.ui.swapp.app_textcues.models.overlays_model.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Generate overlay images for the given sequence of keys.

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
from sppas.src.imgdata import sppasImage
from sppas.src.imgdata import sppasImageSightsReader
from sppas.ui.swapp.wappsg import wapp_settings
from sppas.src.annotations.CuedSpeech.wherecue.positions import WhereVowelPositionsPredictor
from sppas.src.annotations.CuedSpeech.wherecue.angles import WhereAnglesPredictor

# ---------------------------------------------------------------------------


FILENAME_PATH = wapp_settings.images + "/textcues/yoyo_selfie.jpg"
FILENAME_PATH_SIGHTS = wapp_settings.images + "/textcues/yoyo_selfie-sights.xra"

# colors for the level of result 1 (colors for the point on the face)
COLORS = {
    "t": (90, 75, 24),
    "s": (139, 91, 42),
    "m": (9, 68, 127),
    "c": (179, 26, 95),
    "b": (88, 21, 161)
}

# ---------------------------------------------------------------------------


class PathwayCodeOverlayModel:
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

    def generate(self, cuedkeys: tuple, model_pos: int, model_angle: int) -> tuple:
        raise NotImplementedError

    # -----------------------------------------------------------------------

    def get_image_sights_coordinates(self,
                                     model_position: int, vowel_code: str
                                     ) -> tuple:
        """Get the base face image with its sights and the coordinates of positions.

        The coordinates represent the Cued Speech keys depending on the model of position.

        :param model_position: (int) Model of position to determine the coordinates of Cued Speech keys.
        :param vowel_code: (str) Vowel code of a Cued Speech key.
        :return: (tuple[sppasImage, sppasImageSightsReader, tuple[int]]) Tuple with the image, the sights
            and the coordinates of the Cued Speech keys.

        """
        # predict the position of the hand base of the code of the vowel
        position_predictor = WhereVowelPositionsPredictor(model_position)
        position_predictor.set_sights_and_predict_coords(self.sights.sights[0], [vowel_code])
        coordinates = position_predictor.get_vowel_coords(vowel_code)
        return self.image, self.sights, coordinates
