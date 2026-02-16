# -*- coding: UTF-8 -*-
"""
:filename: sppas.ui.swpapp.textcues.views.nodes.cuedcode.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Create nodes for the generated cued result.

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
from whakerpy.htmlmaker import HTMLNode
from whakerpy.htmlmaker.htmnodes.htmnode import TagNode
from whakerpy.htmlmaker import EmptyNode
from sppas.core.config import separators
from sppas.ui.swapp.wappsg import wapp_settings

from ...textcues_msg import MSG_KEY_PHONES
from ...textcues_msg import MSG_KEY_CODE
from ...textcues_msg import MSG_ERROR_NO_RESULT
from ...textcues_record import TextCueSRecord

# ---------------------------------------------------------------------------


class CuedCode:
    """Create nodes to construct the displayed result HTML content.

    """
    
    def __init__(self, record: TextCueSRecord):
        """Initialize the CuedCode object.

        :param record: (TextCueSRecord) The record with all results to be displayed.

        """
        self._record = record

    # -----------------------------------------------------------------------

    def images_mode_content_nodes(self, parent: TagNode):
        """Fills-in the node with images of the cued keys.

        Create a table with: each line is a token, each column represents a
        key, represented by 2 different images (shape and position).

        :return: (TagNode) The container HTML node with links to images of the cued keys

        """
        if self._record.textnorm is None or self._record.cuedphons is None or self._record.cuedkeys is None:
            CuedCode.__no_content_nodes(parent)
            return

        _tok_idx = 0
        for token, pron, keys in zip(self._record.textnorm, self._record.cuedphons, self._record.cuedkeys):

            CuedCode.coded_token(parent, token)
            _ol = CuedCode.coded_list(parent)

            _i = 0
            for _phon, _key in zip(pron.split(separators.syllables), keys.split(separators.syllables)):
                if _phon == "cnil" + separators.phonemes + "vnil":
                    continue
                if "cnil" in _phon:
                    _phon = _phon.replace("cnil", "&empty;")
                if "vnil" in _phon:
                    _phon = _phon.replace("vnil", "&empty;")

                _li = CuedCode.coded_phon(_ol, _phon, _key)
                _figure = CuedCode.coded_illus(_li)

                if "cuedresult" in self._record.extras:
                    if len(self._record.extras["cuedresult"]) > _tok_idx:
                        _r = self._record.extras["cuedresult"][_tok_idx][_i]
                        if len(_r) == 1:
                            # the shape overlays the face and the target finger indicates the
                            # position on an estimated image
                            CuedCode.yoyo_face_image(_figure, _r[0])
                        elif len(_r) == 2:
                            # shape and position in 2 different static images
                            CuedCode.yoyo_hand_image(_figure, _r[0])
                            CuedCode.yoyo_face_image(_figure, _r[1])

                _caption = HTMLNode(_figure.identifier, None, "figcaption", value=_key)
                _figure.append_child(_caption)

                _i += 1

            _tok_idx += 1

    # -----------------------------------------------------------------------

    def overlay_mode_content_nodes(self, parent: TagNode):
        """Fills-in the node with an overlay image of the cued keys.

        Create a table with: each line is a token, each column represents a
        key, represented by 1 image (shape and position).

        :return: (TagNode) The container HTML node with links to images of the cued keys

        """
        self.images_mode_content_nodes(parent)

    # -----------------------------------------------------------------------

    def video_mode_content_nodes(self, parent: TagNode):
        """Fills-in the node with a video of the cued keys.

        :return: (TagNode) The container HTML node with links to images of the cued keys

        """
        if "cuedresult" not in self._record.extras:
            self.images_mode_content_nodes(parent)
        else:
            if len(self._record.extras["cuedresult"]) != 1:
                self.__no_content_nodes(parent)
            else:
                _figure = TagNode(parent.identifier, None, "figure")
                parent.append_child(_figure)

    # -----------------------------------------------------------------------

    @staticmethod
    def __no_content_nodes(parent: TagNode):
        """Fills-in the node with a message. """
        _p = HTMLNode(parent.identifier, None, "p", value=MSG_ERROR_NO_RESULT)
        parent.append_child(_p)

    # -----------------------------------------------------------------------
    # Utilities
    # -----------------------------------------------------------------------

    @staticmethod
    def coded_token(parent: TagNode, token: str) -> HTMLNode:
        _p = HTMLNode(parent.identifier, None, "p", value=token)
        _p.add_attribute("class", "coded-token")
        parent.append_child(_p)
        return _p

    # -----------------------------------------------------------------------

    @staticmethod
    def coded_list(parent: TagNode) -> TagNode:
        _ol = TagNode(parent.identifier, None, "ol")
        _ol.add_attribute("class", "flex-panel coded-text")
        parent.append_child(_ol)
        return _ol

    # -----------------------------------------------------------------------

    @staticmethod
    def coded_phon(parent: TagNode, phon: str, cs_key: str) -> TagNode:
        _li = TagNode(parent.identifier, None, "li")
        _li.add_attribute("class", "coded-key")
        _li.add_attribute("aria-label", MSG_KEY_PHONES + ": " + phon + ", " + MSG_KEY_CODE + " :" + cs_key)
        parent.append_child(_li)

        _span = HTMLNode(_li.identifier, None, "span", value=phon)
        _span.add_attribute("aria-hidden", "true")
        _li.append_child(_span)

        return _li

    # -----------------------------------------------------------------------

    @staticmethod
    def coded_illus(parent: TagNode) -> TagNode:
        _figure = TagNode(parent.identifier, None, "figure")
        _figure.add_attribute("class", "key-illus")
        _figure.add_attribute("aria-hidden", "true")
        parent.append_child(_figure)

        return _figure

    # -----------------------------------------------------------------------

    @staticmethod
    def yoyo_face_image(parent, img_path: str) -> EmptyNode:
        _img = EmptyNode(parent.identifier, None, "img")
        if os.path.exists(img_path):
            _img.add_attribute("src", img_path)
        else:
            # Fall back to a default selfie in black&white
            dest = os.path.join(wapp_settings.images + "textcues/yoyo_selfie_bw.jpg")
            _img.add_attribute("src", dest)
        _img.add_attribute("alt", "")
        _img.add_attribute("class", "face-img")
        parent.append_child(_img)

        return _img

    # -----------------------------------------------------------------------

    @staticmethod
    def yoyo_hand_image(parent, img_path: str) -> EmptyNode:
        _img = EmptyNode(parent.identifier, None, "img")
        if os.path.exists(img_path):
            _img.add_attribute("src", img_path)
        else:
            # Fall back to a default hand in black&white
            dest = os.path.join(wapp_settings.images + "textcues/yoyo_0_bw.png")
            _img.add_attribute("src", dest)
        _img.add_attribute("alt", "")
        _img.add_attribute("class", "hand-img")
        parent.append_child(_img)

        return _img


