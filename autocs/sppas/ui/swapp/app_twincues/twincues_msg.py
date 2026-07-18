"""
:filename: sppas.ui.swapp.app_twincues.twincues_msg.py
:author: Brigitte Bigi
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
    # Translation domain/catalog: see textcues.po.
    return msg(message, "textcues")

# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


MSG_ERROR_DETAILS = _("Error details: ")
MSG_ERROR_NOT_YET_IMPLEMENTED = _("Not yet implemented")
MSG_ERROR_INVALID_CUE = _("Invalid cue: '{:s}'. Expected one or more '<shape>-<position>' "
                          "segments separated by '.', with codes known by the language.")
MSG_ERROR_INVALID_WORD = _("'{:s}' is not recognized as a single word. Enter only one word.")

# ---------------------------------------------------------------------------
# Info
# ---------------------------------------------------------------------------


MSG_INFO_NO_INPUT = _("Enter a word or a cue to get a conversion.")
MSG_INFO_NO_TWIN_WORD = _("This word has no twin. Pronunciations tried: {:s}.")
MSG_INFO_NO_TWIN_CUE = _("No word shares this cue.")

# ---------------------------------------------------------------------------
# Global messages
# ---------------------------------------------------------------------------


MSG_APP_TITLE = _("TwinCueS")
MSG_APP_TITLE2 = _("Word / Cue conversion")
MSG_DESCR = _("Allows to get twin words from its matching cues.")
MSG_ACS_PROJECT = _("ACS Project")
MSG_HOME = _("Home")

# ---------------------------------------------------------------------------
# Welcome page
# ---------------------------------------------------------------------------


MSG_INTRO = _("TWINCUES_INTRO")
MSG_LAUNCH = _("Start")
MSG_YOYO_WELCOME = _("TWINCUES_YOYO_HELLO")

# ---------------------------------------------------------------------------
# Conversion page
# ---------------------------------------------------------------------------


MSG_LANG = _("I select the language:")
MSG_WORD_LABEL = _("I enter a word:")
MSG_WORD_PLACEHOLDER = _("Enter a word here")
MSG_CUE_LABEL = _("Or I enter a cue:")
MSG_CUE_PLACEHOLDER = _("Enter a cue here")
MSG_VALIDATE_BUTTON = _("Validate")
MSG_RESULT_CUE_LABEL = _("Corresponding cue:")
MSG_RESULT_WORD_LABEL = _("Corresponding word(s):")
