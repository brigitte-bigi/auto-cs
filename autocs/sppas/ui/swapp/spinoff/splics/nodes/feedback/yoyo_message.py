"""
:filename: sppas.ui.swapp.spinoff.splics.nodes.feedback.yoyo_message.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: HTMLNode to display yoyo and its message.

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
from sppas.ui.swapp.spinoff.splics.splicssg import splics_paths

# ---------------------------------------------------------------------------

# Shared translation domain/catalog of the spin-off (see splics.po).
MSG_YOYO_SORRY = msg("An error occurred", "splics")
MSG_NO_LANG = msg("No language is available.", "splics")

# Images are currently stored under the "textcues" statics folder and
# shared as-is by the other Cued Speech spin-off applications.
YOYO_IMAGES_PATH = "textcues"

# ---------------------------------------------------------------------------


class BaseYoyoMessageNode(HTMLNode):
    """Base view node to render a Yoyo message block.

    This node creates a <div> container with CSS class 'yoyo-says'.
    It is responsible for appending a text message and an image.
    It does not define the message content or the image by itself.

    """

    def __init__(self, parent_id: str, **kwargs):
        """Initialize the base Yoyo message node.

        :param parent_id: (str) Identifier of the parent HTML node.

        """
        super(BaseYoyoMessageNode, self).__init__(parent_id, None, "div")
        self.add_attribute("class", "yoyo-says")

    # -----------------------------------------------------------------------

    def append_message(self, message: str) -> HTMLNode:
        """Append the Yoyo message in a "<p>" node.

        :param message: (str) The message Yoyo is saying.
        :return: (HTMLNode) The created "<p>" node.

        """
        _p = HTMLNode(
            self.identifier, None, "p",
            value=message,
            attributes={"id": "yoyo-says-message"}
        )
        self.append_child(_p)
        return _p

    # -----------------------------------------------------------------------

    def append_image(self, yoyo_image: str) -> EmptyNode:
        """Append a Yoyo image in an "<img>" node.

        :param yoyo_image: (str) The Yoyo image filename.
        :return: (EmptyNode) The created "<img>" node.

        """
        _img = EmptyNode(
            self.identifier, None, "img",
            attributes={
                "alt": "YOYO",
                "src": splics_paths.images + YOYO_IMAGES_PATH + "/" + yoyo_image
            }
        )
        self.append_child(_img)
        return _img

    # -----------------------------------------------------------------------

    @staticmethod
    def welcome(parent_id: str, welcome_message: str,
                has_language: bool) -> "BaseYoyoMessageNode":
        """Return the Yoyo of a welcome page.

        The welcome Yoyo is replaced by an error Yoyo when no language is
        available: nothing can then be chosen nor launched.

        :param parent_id: (str) Identifier of the parent HTML node.
        :param welcome_message: (str) The message Yoyo says when all is well.
        :param has_language: (bool) At least one language is available.
        :return: (BaseYoyoMessageNode) The Yoyo node to append to the page.

        """
        if has_language is True:
            yoyo = YoyoMessageNode(parent_id, welcome_message)
        else:
            yoyo = YoyoErrorNode(parent_id, MSG_NO_LANG)
        yoyo.add_attribute("class", "width_20")
        return yoyo

# ---------------------------------------------------------------------------


class YoyoMessageNode(BaseYoyoMessageNode):
    """A standard message Yoyo says."""

    def __init__(self, parent_id: str, message: str):
        """Create the HTML node for a standard message.

        :param parent_id: (str) Identifier of the parent HTML node.
        :param message: (str) The message Yoyo is saying.

        """
        super(YoyoMessageNode, self).__init__(parent_id)
        self.append_message(message)
        self.append_image("yoyo_says.png")

# ---------------------------------------------------------------------------


class YoyoInfoNode(BaseYoyoMessageNode):
    """A standard message Yoyo says."""

    def __init__(self, parent_id: str, message: str):
        """Create the HTML node for an information message.

        :param parent_id: (str) Identifier of the parent HTML node.
        :param message: (str) The message Yoyo is saying.

        """
        super(YoyoInfoNode, self).__init__(parent_id)
        self.append_message(message)
        self.append_image("yoyo_says_info.png")

# ---------------------------------------------------------------------------


class YoyoErrorNode(BaseYoyoMessageNode):
    """An error Yoyo explains."""

    def __init__(self, parent_id: str, message: str = MSG_YOYO_SORRY):
        """Create the HTML node for an error message.

        :param parent_id: (str) Identifier of the parent HTML node.
        :param message: (str) The message Yoyo is saying.

        """
        super(YoyoErrorNode, self).__init__(parent_id)
        # The "error" modifier, on the bubble itself, turns it red.
        _bubble = self.append_message(message)
        _bubble.add_attribute("class", "error")
        self.append_image("yoyo_says_error.png")
