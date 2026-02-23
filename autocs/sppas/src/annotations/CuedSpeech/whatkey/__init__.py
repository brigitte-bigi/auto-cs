"""
:filename: sppas.src.annotations.CuedSpeech.whatkey.__init__.py
:author:   Brigitte Bigi
:contact:  contact@sppas.org
:summary:  Cued Speech keys predictor. Answer the "What?" question.

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

To cite this work, use the following reference:

Brigitte Bigi (2023).
An analysis of produced versus predicted French Cued Speech keys.
In 10th Language & Technology Conference: Human Language Technologies
as a Challenge for Computer Science and Linguistics, Poznań, Poland.

Abstract:
    Cued Speech is a communication system developed for deaf people to
    complement speechreading at the phonetic level with hands. This
    visual communication mode uses handshapes in different placements
    near the face in combination with the mouth movements of speech
    to make the phonemes of spoken language look different from each other.
    This paper presents an analysis on produced cues in 5 topics of CLeLfPC,
    a large corpus of read speech in French with Cued Speech.
    A phonemes-to-cues automatic system is proposed in order to predict the
    cue to be produced while speaking. This system is part of SPPAS -
    the automatic annotation an analysis of speech, an open source software
    tool. The predicted keys of the automatic system are compared to the
    produced keys of cuers. The number of inserted, deleted and substituted
    keys are analyzed. We observed that most of the differences between
    predicted and produced keys comes from 3 common position’s substitutions
    by some of the cuers.

"""

from .whatkeyexc import sppasCuedRulesValueError
from .whatkeyexc import sppasCuedRulesMinValueError
from .whatkeyexc import sppasCuedRulesMaxValueError
from .keysrules import CuedSpeechCueingRules
from .phonestokeys import CuedSpeechKeys
from .keysbytoken import CueingPronTokenizer
from .keysbytoken import CueingKeysByToken
from .whatkey import sppasWhatKeyPredictor


__all__ = (
    "sppasCuedRulesValueError",
    "sppasCuedRulesMinValueError",
    "sppasCuedRulesMaxValueError",
    "CuedSpeechCueingRules",
    "CuedSpeechKeys",
    "CueingPronTokenizer",
    "CueingKeysByToken",
    "sppasWhatKeyPredictor"
)
