"""
:filename: sppas.ui.swapp.spinoff.splics.models.images_model.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Image paths of the shape/position keys of a key piano.

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
from sppas.ui.swapp.spinoff.splics.splicssg import splics_paths

# ---------------------------------------------------------------------------


class KeyPianoImagesModel:
    """Return the image path of a shape or a position code.

    Same shared "yoyo" illustrations and naming convention as TextCueS
    (see :class:`app_textcues.models.images_model.PathwayCodeImagesModel`):
    "<prefix>_<code>.png" for a shape (hand), "<prefix>_<code>.jpg" for a
    position (face).

    """

    IMAGES_PATH = splics_paths.images + "/textcues/"
    PREFIX = "yoyo"

    # -----------------------------------------------------------------------

    @staticmethod
    def shape_image(code: str) -> str:
        """Return the image path of the given shape code.

        :param code: (str) Shape code, e.g. "1".
        :return: (str) Image path.

        """
        return f"{KeyPianoImagesModel.IMAGES_PATH}{KeyPianoImagesModel.PREFIX}_{code}.png"

    # -----------------------------------------------------------------------

    @staticmethod
    def position_image(code: str) -> str:
        """Return the image path of the given position code.

        :param code: (str) Position code, e.g. "s".
        :return: (str) Image path.

        """
        return f"{KeyPianoImagesModel.IMAGES_PATH}{KeyPianoImagesModel.PREFIX}_{code}.jpg"
