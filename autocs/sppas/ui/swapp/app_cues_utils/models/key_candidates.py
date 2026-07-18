"""
:filename: sppas.ui.swapp.app_cues_utils.models.key_candidates.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Restrict shape/position codes to the phonemes attested in a dictionary.

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

Shared with the "cue" apps needing a key piano fed with dictionary-attested
phonemes only (ListCueS, TwinCueS): a theoretical rule-file phoneme not
attested in the dictionary would never be reachable anyway.

"""

from __future__ import annotations

from sppas.src.annotations.CuedSpeech import CuedSpeechCueingRules

# ---------------------------------------------------------------------------

# A shape/position code can appear under these names in
# CuedSpeechCueingRules.get_phonemes() to mean "no consonant"/"no vowel"
# instead of -- or in addition to -- a real phoneme.
NIL_CONSONANT_CODES = (CuedSpeechCueingRules.CONSONANT_NIL, CuedSpeechCueingRules.CONSONANT_NONE)
NIL_VOWEL_CODES = (CuedSpeechCueingRules.VOWEL_NIL, CuedSpeechCueingRules.VOWEL_NONE)

# HTML string to display the absence of a phoneme
NO_PHONEME_MARKER = "&empty;"

# ---------------------------------------------------------------------------


def build_key_candidates(codes: list, cued_rules, attested: set, nil_codes: tuple) -> tuple:
    """Restrict the phonemes of each shape/position code to the attested ones.

    :param codes: (list) Shape codes, or position codes.
    :param cued_rules: (CuedSpeechKeys) Rules of the current language.
    :param attested: (set) Phonemes actually occurring in the dictionary.
    :param nil_codes: (tuple) Names meaning "no consonant"/"no vowel" for this code.
    :return: (tuple) (dict: code -> tuple of attested phonemes, dict: code -> has "absent" option)

    """
    _by_code = dict()
    _absent = dict()

    for _code in codes:
        _phonemes = cued_rules.get_phonemes(_code)
        _by_code[_code] = tuple(_p for _p in _phonemes if _p not in nil_codes and _p in attested)
        _absent[_code] = any(_p in nil_codes for _p in _phonemes)

    return _by_code, _absent
