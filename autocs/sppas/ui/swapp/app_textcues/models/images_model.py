"""
:filename: sppas.ui.swapp.app_textcues.models.images_model.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Generate images for the given sequence of keys.

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

from sppas.core.config import separators
from sppas.src.annotations.CuedSpeech import CuedSpeechKeys
from sppas.ui.swapp.wappsg import wapp_settings

# ---------------------------------------------------------------------------


class PathwayCodeImagesModel:
    """Generates image results for a given cued sequence.

    """

    IMAGES_PATH = wapp_settings.images + "/textcues/"

    # -----------------------------------------------------------------------

    def __init__(self, cued_rules: CuedSpeechKeys, prefix: str = "yoyo"):
        """Create a new instance.

        :param cued_rules: (CuedSpeechKeys) The rules of the cued speech.
        :param prefix: (str) The prefix name of the images.

        """
        if isinstance(cued_rules, CuedSpeechKeys) is False:
            raise TypeError(f"Given cued_rules must be a CuedSpeechKeys object. "
                            f"Got {type(cued_rules)} instead.")
        self.__cs = cued_rules
        self.__prefix = prefix

    # -----------------------------------------------------------------------

    def generate(self, cuedkeys: tuple) -> tuple:
        """Generate the images filepath matching the given cued keys.

        Example:
        - cuedkeys: ('5-s', '2-b')
        - output: (
            ("path/textcues/'prefix'_5.png", "path/textcues/'prefix'_s.png"),
            ("path/textcues/'prefix'_2.png", "path/textcues/'prefix'_b.png")
            )
        :param cuedkeys: (tuple) Cued Speech keys of each token.
        :return: (tuple) filepath.

        """
        result = list()

        # for each coded token
        # --------------------
        for coded_seq in cuedkeys:
            images_seq = list()
            coded_keys = coded_seq.split(separators.syllables)

            # for each coded key
            # ------------------
            for _i, coded_key in enumerate(coded_keys):
                if len(coded_key) == 0:
                    raise ValueError(f"Given coded_key is an empty string, "
                                     f"at index {_i} of cued keys: {cuedkeys}.")
                _cv = coded_key.split(separators.phonemes)
                if len(_cv) != 2:
                    raise ValueError(f"Given coded_key is invalid at index {_i} of "
                                     f"cued keys: {cuedkeys}. Got '{_cv}' instead.")
                consonant, vowel = _cv
                consonant_path = self.IMAGES_PATH + f"{self.__prefix}_{consonant}.png"
                vowel_path = self.IMAGES_PATH + f"{self.__prefix}_{vowel}.jpg"
                images_seq.append( (consonant_path, vowel_path) )

            result.append(images_seq)

        return tuple(result)
