# -*- coding: UTF-8 -*-
"""
:filename: sppas.src.annotations.CuedSpeech.__init__.py
:author:   Brigitte Bigi
:contact:  contact@sppas.org
:summary:  Cued Speech automatic annotation.

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

import sys

from sppas.core.coreutils import sppasPythonFeatureError

# ---------------------------------------------------------------------------
# Answering the "what" question does not require any specific feature
# ---------------------------------------------------------------------------

if sys.version_info > (3, 9):
    from .whatkey import sppasCuedRulesValueError
    from .whatkey import sppasCuedRulesMinValueError
    from .whatkey import sppasCuedRulesMaxValueError
    from .whatkey import CuedSpeechCueingRules
    from .whatkey import CuedSpeechKeys
    from .whatkey import sppasWhatKeyPredictor
    from .whowtag import CuedSpeechVideoTagger
    from .sppascuedspeech import sppasCuedSpeech

else:
    class CuedSpeechKeys(object):
        def __init__(self, *args, **kwargs):
            raise sppasPythonFeatureError("cuedspeech", "3.9+")

    class CuedSpeechVideoTagger(object):
        def __init__(self, *args, **kwargs):
            raise sppasPythonFeatureError("cuedspeech", "3.9+")

    class sppasCuedSpeech(object):
        def __init__(self, *args, **kwargs):
            raise sppasPythonFeatureError("cuedspeech", "3.9+")

# ---------------------------------------------------------------------------

__all__ = (
    # what
    "sppasCuedRulesValueError",
    "sppasCuedRulesMinValueError",
    "sppasCuedRulesMaxValueError",
    "CuedSpeechCueingRules",
    "CuedSpeechKeys",
    "sppasWhatKeyPredictor",
    # when
    # where
    # tag
    "CuedSpeechVideoTagger",
    # SPPAS integration
    "sppasCuedSpeech"
)
