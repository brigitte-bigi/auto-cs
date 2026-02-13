# -*- coding: UTF-8 -*-
"""
:filename: sppas.src.annotations.CuedSpeech.videotagger.__init__.py
:author:   Brigitte Bigi
:contact:  contact@sppas.org
:summary:  Tag a hand on a video for Cued Speech automatic annotation.

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

import os.path
import sys

from sppas.core.config import cfg
from sppas.core.config import paths
from sppas.core.coreutils import sppasError
from sppas.core.coreutils import sppasEnableFeatureError
from sppas.core.coreutils import sppasPythonFeatureError
import sppas.src.videodata

# ---------------------------------------------------------------------------

class sppasHandFilters:
    def __init__(self, *args, **kwargs):
        raise sppasError("The hand filters can't be used.")


if os.path.exists(os.path.join(paths.resources, "cuedspeech")) is False:
    # The feature is enabled but the corresponding resources are missing.
    cfg.set_feature("cuedspeech", False)

if cfg.feature_installed("video") and cfg.feature_installed("cuedspeech"):

    # -----------------------------------------------------------------------
    # Import the classes in case the "video" feature is enabled: opencv&numpy
    # are both installed and the automatic detections can work.
    # -----------------------------------------------------------------------
    if sys.version_info > (3, 6):

        # -----------------------------------------------------------------------
        # Check if we have at least one hands set in the 'resources/cuedspeech' folder to tag a video.
        # -----------------------------------------------------------------------
        from sppas.src.resources import sppasHandResource

        hands_manager = sppasHandResource()
        hands_manager.automatic_loading()

        if len(hands_manager) > 0:
            from .whowtagvideo import CuedSpeechVideoTagger
            from .handfilters import sppasHandFilters

        else:
            # -----------------------------------------------------------------------
            # Define class in case we have no hands set in the 'resources/cuedspeech' folder.
            # -----------------------------------------------------------------------
            class CuedSpeechVideoTagger:
                def __init__(self, *args, **kwargs):
                    raise sppasError("The 'resources/cuedspeech' folder doesn't contains any hand-set.")

                @staticmethod
                def get_hands_filters() -> list:
                    return []

            class sppasHandFilters:
                def __init__(self, *args, **kwargs):
                    raise sppasError("The hand filters can't be used.")

                @staticmethod
                def get_filter_names() -> list:
                    return []

    else:
        # -----------------------------------------------------------------------
        # Define class in case python version is inferior to 3.6
        # -----------------------------------------------------------------------

        class CuedSpeechVideoTagger:
            def __init__(self, *args, **kwargs):
                raise sppasPythonFeatureError("cuedspeech", "3.6+")

else:
    # -----------------------------------------------------------------------
    # Define class in case opencv&numpy are not installed.
    # -----------------------------------------------------------------------

    class CuedSpeechVideoTagger:
        def __init__(self, *args, **kwargs):
            raise sppasEnableFeatureError("cuedspeech")


__all__ = (
    "CuedSpeechVideoTagger"
)
