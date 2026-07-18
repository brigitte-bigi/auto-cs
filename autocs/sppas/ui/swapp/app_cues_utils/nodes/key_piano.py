"""
:filename: sppas.ui.swapp.app_cues_utils.nodes.key_piano.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: HTMLNode for a shape/position key piano, shared by the "cue" apps.

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
from whakerpy.htmlmaker import HTMLNode
from whakerpy.htmlmaker import EmptyNode

from sppas.core.coreutils import msg
from sppas.ui.swapp.wappcore.wappsg import wapp_settings

from .illustration import CuedIllustration

# ---------------------------------------------------------------------------

# Shared translation domain/catalog with TextCueS (see textcues.po).
MSG_PIANO_SHAPE_GROUP = msg("Shape", "textcues")
MSG_PIANO_POSITION_GROUP = msg("Position", "textcues")
MSG_KEY_CODE = msg("Code", "textcues")
MSG_KEY_PHONES = msg("Phonemes", "textcues")

# ---------------------------------------------------------------------------


class KeyPianoNode(HTMLNode):
    """The Whakerexa "KeyPiano" markup, filled with the shape and position keys.

    Used by any "cue" app needing to compose a "<shape>-<position>" key
    sequence by clicking rather than typing it by hand (ListCueS, TwinCueS).
    This node only declares the HTML contract of the generic Whakerexa
    ``KeyPiano`` component (see ``whakerexa/wexa_statics/js/extras/keypiano``):
    a container with the target field id, and one "radio" group per part of
    a key.

    Each key reuses the very same illustration builder as TextCueS's coded
    result (:class:`app_cues_utils.nodes.illustration.CuedIllustration`), so
    a piano key looks the same size and style, in the same order: the
    matching phonemes above the illustration, the code below it (in the
    figcaption). Both are marked ``aria-hidden``, because the key's own
    accessible name (on the ``<label>``) already carries the same
    information -- this avoids announcing it twice to screen readers.

    """

    def __init__(self, parent_id: str, target_id: str, shape_keys: tuple, position_keys: tuple):
        """Create the key piano node.

        :param parent_id: (str) The parent id of the HTML node
        :param target_id: (str) Id of the field the piano writes into
        :param shape_keys: (tuple) {"code": str, "image": str, "phonemes": tuple}, one per shape
        :param position_keys: (tuple) {"code": str, "image": str, "phonemes": tuple}, one per position

        """
        super(KeyPianoNode, self).__init__(parent_id, "cue_piano", "div")
        self.add_attribute("class", "wexa-key-piano")
        self.add_attribute("data-target", target_id)
        # A proven-correct URL prefix (already used for this app's own CSS/JS
        # links to whakerexa): more robust than a JS-side relative computation.
        self.add_attribute("data-icons-path", wapp_settings.wexa_statics + "icons/mono-svg")

        self.__append_group(MSG_PIANO_SHAPE_GROUP, shape_keys, CuedIllustration.yoyo_hand_image)
        self.__append_group(MSG_PIANO_POSITION_GROUP, position_keys, CuedIllustration.yoyo_face_image)

    # -----------------------------------------------------------------------
    # PRIVATE
    # -----------------------------------------------------------------------

    def __append_group(self, group_label: str, keys: tuple, image_builder) -> None:
        """Append one "radio" group of keys, one per shape/position key.

        :param group_label: (str) Accessible name of the group.
        :param keys: (tuple) {"code": str, "image": str, "phonemes": tuple}, one per key.
        :param image_builder: (Callable) CuedIllustration.yoyo_hand_image for shapes,
               CuedIllustration.yoyo_face_image for positions.

        """
        _group = HTMLNode(self.identifier, None, "div")
        _group.add_attribute("class", "wexa-key-piano-group")
        _group.add_attribute("data-mode", "radio")
        _group.add_attribute("aria-label", group_label)
        self.append_child(_group)

        for _key in keys:
            self.__append_key(_group, _key["code"], _key["image"], _key["phonemes"], image_builder)

    # -----------------------------------------------------------------------

    @staticmethod
    def __append_key(group: HTMLNode, code: str, image: str, phonemes: tuple, image_builder) -> None:
        """Append one key: a radio input, and its TextCueS-style illustration.

        :param group: (HTMLNode) The "wexa-key-piano-group" parent node.
        :param code: (str) Shape or position code, e.g. "1" or "s".
        :param image: (str) Path of the illustration image.
        :param phonemes: (tuple) Phonemes matching this code.
        :param image_builder: (Callable) CuedIllustration.yoyo_hand_image or yoyo_face_image.

        """
        _phones = " ".join(phonemes)
        _key = HTMLNode(group.identifier, None, "label")
        # "wexa-key-piano-key": whakerexa mechanics (hides the radio, shows the
        # checked/disabled state). "coded-key": TextCueS's own box styling
        # (app_cues.css), reused as-is for the exact same look.
        _key.add_attribute("class", "wexa-key-piano-key coded-key")
        _key.add_attribute("aria-label", f"{MSG_KEY_PHONES}: {_phones}, {MSG_KEY_CODE} :{code}")
        group.append_child(_key)

        _input = EmptyNode(_key.identifier, None, "input", attributes={"type": "radio", "value": code})
        _key.append_child(_input)

        # Phonemes above the illustration, code below it (in the figcaption) --
        # same DOM order as TextCueS's coded_phon()/coded_illus(). Both are
        # aria-hidden: the label above already carries the same information.
        _span = HTMLNode(_key.identifier, None, "span", value=_phones)
        _span.add_attribute("aria-hidden", "true")
        _key.append_child(_span)

        _figure = CuedIllustration.coded_illus(_key)
        image_builder(_figure, image)

        _caption = HTMLNode(_figure.identifier, None, "figcaption", value=code)
        _figure.append_child(_caption)
