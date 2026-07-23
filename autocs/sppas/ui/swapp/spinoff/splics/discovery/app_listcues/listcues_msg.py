"""
:filename: sppas.ui.swapp.spinoff.splics.discovery.app_listcues.listcues_msg.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: This file contains translated message of the views.

..
    This file is part of Auto-CS: <https://autocs.sourceforge.io>
    -------------------------------------------------------------------------

    Copyright (C) 2024-2026  Brigitte Bigi, CNRS
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
    return msg(message, "splics")

# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


MSG_ERROR_DETAILS = _("Error details: ")
MSG_ERROR_INVALID_CUE = _("Invalid cue: '{:s}'. Expected 1 to 7 '<shape>-<position>' "
                          "segments separated by '.', with codes known by the language.")

# ---------------------------------------------------------------------------
# Info
# ---------------------------------------------------------------------------


MSG_INFO_NO_INPUT = _("Enter a sequence of 1 to 7 keys to get its matching pronunciations.")
MSG_INFO_NO_PRONS = _("No pronounceable sequence matches this cue.")

# ---------------------------------------------------------------------------
# Global messages
# ---------------------------------------------------------------------------


MSG_APP_TITLE = _("ListCueS")
MSG_APP_SUBTITLE = _("Key sequence conversion")
MSG_DESCR = _("Allows to get the words matching a sequence of Cued Speech keys.")
MSG_ACS_PROJECT = _("ACS Project")
MSG_HOME = _("Home")

# ---------------------------------------------------------------------------
# Welcome page
# ---------------------------------------------------------------------------


MSG_INTRO = _("LISTCUES_INTRO")
MSG_LAUNCH = _("Start")
MSG_YOYO_WELCOME = _("LISTCUES_YOYO_HELLO")

# ---------------------------------------------------------------------------
# Conversion page
# ---------------------------------------------------------------------------


MSG_LANG = _("I select the language:")
MSG_CUE_LABEL = _("I enter a sequence of keys:")
MSG_CUE_PLACEHOLDER = _("Enter a sequence of keys here (e.g. 1-s.3-t)")
MSG_VALIDATE_BUTTON = _("Validate")
MSG_TABLE_COL_PRON = _("Pronunciation")
MSG_TABLE_COL_WORDS = _("Words")
