"""
:filename: sppas.ui.swapp.app_cues_utils.nodes.illustration.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Shared "yoyo" hand/face illustration nodes for a coded (shape+position) key.

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
import logging

from whakerpy.htmlmaker import EmptyNode
from whakerpy.htmlmaker.htmnodes.htmnode import TagNode

from sppas.ui.swapp.wappcore.wappsg import wapp_settings

# ---------------------------------------------------------------------------


class CuedIllustration:
    """Build the "key-illus" figure and its hand/face "yoyo" images.

    Used identically by TextCueS (a coded result, already determined) and
    ListCueS (a piano key, not tied to a specific word yet): both display
    the same illustration of a shape (hand) or a position (face) code.

    """

    @staticmethod
    def coded_illus(parent: TagNode) -> TagNode:
        """Create and append the "figure" container of a coded key illustration.

        :param parent: (TagNode) The parent node.
        :return: (TagNode) The created figure node.

        """
        _figure = TagNode(parent.identifier, None, "figure")
        _figure.add_attribute("class", "key-illus")
        _figure.add_attribute("aria-hidden", "true")
        parent.append_child(_figure)

        return _figure

    # -----------------------------------------------------------------------

    @staticmethod
    def yoyo_hand_image(parent, img_path: str) -> EmptyNode:
        """Create and append the hand (shape) image, with a fallback if missing.

        :param parent: The parent node.
        :param img_path: (str) Path of the hand image.
        :return: (EmptyNode) The created image node.

        """
        _img = EmptyNode(parent.identifier, None, "img")
        if os.path.exists(img_path):
            _img.add_attribute("src", img_path)
        else:
            # Fall back to a default hand in black&white
            dest = os.path.join(wapp_settings.images + "textcues/yoyo_0_bw.png")
            _img.add_attribute("src", dest)
            logging.error(f"Can't find hand image file: {img_path}")
        _img.add_attribute("alt", "")
        _img.add_attribute("class", "hand-img")
        parent.append_child(_img)

        return _img

    # -----------------------------------------------------------------------

    @staticmethod
    def yoyo_face_image(parent, img_path: str) -> EmptyNode:
        """Create and append the face (position) image, with a fallback if missing.

        :param parent: The parent node.
        :param img_path: (str) Path of the face image.
        :return: (EmptyNode) The created image node.

        """
        _img = EmptyNode(parent.identifier, None, "img")
        if os.path.exists(img_path):
            _img.add_attribute("src", img_path)
        else:
            # Fall back to a default selfie in black&white
            dest = os.path.join(wapp_settings.images + "textcues/yoyo_bw.jpg")
            _img.add_attribute("src", dest)
            logging.error(f"Can't find face image file: {img_path}")
        _img.add_attribute("alt", "")
        _img.add_attribute("class", "face-img")
        parent.append_child(_img)

        return _img
