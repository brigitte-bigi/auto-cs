"""
:filename: sppas.ui.app_textcues.textcues_msg.py
:author: Brigitte Bigi
:contributor: Alexandre Rizzante-Madonna
:contact: contact@sppas.org
:summary: This file contains translated message of the views.

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

from sppas.core.coreutils import msg

# ---------------------------------------------------------------------------
# The translation system for this interface
# ---------------------------------------------------------------------------


def _(message):
    return msg(message, "textcues")

# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


MSG_ERROR_DETAILS = _("Error details: ")
MSG_ERROR_NO_TEXT = _("Text is required to proceed to the next step.")
MSG_ERROR_NO_TOKENS = _("No word was extracted from the given text.")
MSG_ERROR_LEN_MISMATCH = _("Got {:d} tokens and {:d} pronunciations.")
MSG_ERROR_NO_PRON = _("No pronunciation of words was found in the given data.")
MSG_ERROR_INVALID_PRON = _("The pronunciation of word {:s} is not valid. Got {:s}.")
MSG_ERROR_EMPTY_PRON = _("No pronunciation found for token {:s}.")
MSG_ERROR_INVALID_FORMAT = _("Invalid data format: {:s}.")
MSG_ERROR_NO_RESULT = _("No result was found in the received data or the format is invalid.")
MSG_ERROR_UNKNOWN_PHON = _("Sound {:s} is unknown.")

# ---------------------------------------------------------------------------
# Yoyo
# ---------------------------------------------------------------------------


MSG_YOYO_WELCOME = _("Hello")
MSG_YOYO_SORRY = _("An error occurred")
MSG_YOYO_NOT_YET = _("Not yet implemented")

# ---------------------------------------------------------------------------
# Global messages
# ---------------------------------------------------------------------------


MSG_APP_TITLE = _("TextCueS")
MSG_APP_TITLE1 = _("Text-to-Cued Speech code generation")
MSG_APP_TITLE2 = _("Text-to-Cued Speech code conversion")
MSG_REF = _("Bibliographical references")
MSG_SEE_ALSO = _("See also")
MSG_DESCR = _("Allows to generate automatically the sequence of keys to be cued from a written text")
MSG_ACS_PROJECT = _("ACS Project")

# ---------------------------------------------------------------------------
# Step 0: Introduction
# ---------------------------------------------------------------------------


MSG_INTRO = _("INTRO")
MSG_LAUNCH = _("Start coding")

# ---------------------------------------------------------------------------
# Step 1
# ---------------------------------------------------------------------------

# Title of the view (H1)
MSG_LANGTEXT_TITLE = _("I choose the language and enter the text to code in Cued Speech")

# Title of the fieldset -- H2 element
MSG_LANGTEXT_FIELD_LEGEND = _("Step 1 of 3 — Language and text")

# Text for the breadcrumb
MSG_LANGTEXT_BREADCRUMB = _("Text")

# Text for the action button
MSG_LANGTEXT_ANN_BUTTON = _("Go to step 2")

# Fieldset content
MSG_LANG = _("Select the text language:")
MSG_TEXT_LABEL = _("Enter or edit the text to code:")
MSG_TEXT_HERE = _("Enter or paste your text here")

# ---------------------------------------------------------------------------
# Step 2
# ---------------------------------------------------------------------------

# Title of the view (H1)
MSG_PHON_TITLE = _("I check and adjust the pronunciation of the text")

MSG_PHON_FIELD_LEGEND = _("Step 2 of 3 — Pronunciation")
MSG_PHON_BREADCRUMB = _("Sounds")
MSG_CHOOSE_PRON = _("Choose or enter the pronunciation for each word to code:")
MSG_SAMPA = _("Sounds are represented with SAMPA")

# Text for the action button
MSG_PHON_ANN_BUTTON = _("Go to step 3")

MSG_TOKENS = _("Words")
MSG_CHOICE_1 = _("Choice n°1")
MSG_CHOICE_2 = _("Choice n°2")
MSG_CHOICE_3 = _("Choice n°3")
MSG_CHOICE_4 = _("Choice n°4")
MSG_PERSONALIZED = _("Personalized")

# ---------------------------------------------------------------------------
# Step 3
# ---------------------------------------------------------------------------

# Title of the view (H1)
MSG_CUES_TITLE = _("I see the corresponding Cued Speech code in text and images")

# Title of the fieldset -- H2 element
MSG_CUES_FIELD_LEGEND = _("Step 3 of 3 — Cued Speech Code")

# Text for the breadcrumb
MSG_CUES_BREADCRUMB = _("Code")

# Text for the action button
MSG_BUTTON_BACK = _("Start over")

# ---------------------------------------------------------------------------

MSG_KEY_PHONES = _("Phonemes")
MSG_KEY_CODE = _("Code")

MSG_RESULT = _("Cued text:")
MSG_BUTTON_APPLY = _("Apply")

# ---------------------------------------------------------------------------

# message for the displayed mode in the form
MSG_MODE_DISPLAY = _("Choose a display mode:")
MSG_MODES = (
    _("Beginner: Hand and face separately"),
    _("Intermediate: Hand on face"),
    _("Advanced: Video")
)

# message for model of position in the form
MSG_POSITION_MODEL = _("Choose how positions are computed:")
MSG_POSITIONS = (
    _("Theoretical positions"),
    _("Low variation"),
    _("Estimated from examples"),
    _("Learned from examples")
)

# message for model of angle in the form
MSG_ANGLE_MODEL = _("Choose how the hand angle is computed:")
MSG_ANGLES = (
    _("Fixed angle"),
    _("Small variation by position"),
    _("Large variation by position"),
    _("Medium variation by position")
)

# message for model of timing in the form
MSG_TIMING_MODEL = _("Choose the timing (video mode only):")
MSG_TIMINGS = (
    _("No transition timing: Duchnowski (1998)"),
    _("Fixed transition timing: Duchnowski (2000)"),
    _("Variable transition timing: Attina (2005)"),
    _("Variable transition timing: SPPAS solution 1"),
    _("Variable transition timing: SPPAS solution 2")
)
