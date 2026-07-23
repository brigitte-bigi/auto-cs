"""
:filename: sppas.ui.swapp.spinoff.splics.discovery.app_listcues.listcues_record.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Data class.

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

from __future__ import annotations
import re

# ---------------------------------------------------------------------------


class ListCueSRecord:
    """Container for the cue data of a conversion request.

    Allows data check, and transport between the model and the views.

    """

    # -----------------------------------------------------------------------

    def __init__(self):
        """Initialize an empty record."""
        self.__lang = None
        self.set_lang(None)
        self.__cue = None

        # Any extra data: prons_result, error, content, ...
        self.__extras = dict()

    # -----------------------------------------------------------------------
    # Formatters and converters
    # -----------------------------------------------------------------------

    @staticmethod
    def strip_string(entry: str) -> str:
        """Strip the string: multiple whitespace, tab and CR/LF.

        :param entry: (str) String to strip
        :return: (str)

        """
        e = re.sub("[\t]+", r" ", entry)
        e = re.sub("[\n]+", r" ", e)
        e = re.sub("[\r]+", r" ", e)
        if "﻿" in e:
            e = re.sub("﻿", r" ", e)

        e = re.sub("[\\s]+", r" ", e)
        return e.strip()

    # -----------------------------------------------------------------------
    # Functions
    # -----------------------------------------------------------------------

    def serialize(self) -> dict:
        """Return a dictionary with serialized record data for transport.

        :return: (dict)

        """
        d = dict()
        d["lang"] = "" if self.__lang is None else self.__lang
        if self.__cue is not None and len(self.__cue) > 0:
            d["cue"] = self.__cue
        return d

    # -----------------------------------------------------------------------

    def parse(self, data: dict) -> None:
        """Fill-in the record with the given data.

        :param data: (dict) Dictionary

        """
        if "lang" in data:
            self.set_lang(data["lang"])
        if "cue" in data:
            self.set_cue(data["cue"])

    # -----------------------------------------------------------------------
    # lang
    # -----------------------------------------------------------------------

    def get_lang(self) -> str:
        """Return the stored lang code."""
        return self.__lang

    def set_lang(self, value: str) -> None:
        """Set the stored 'lang' after validating it.

        No default is applied: a language must be explicitly chosen on the
        welcome form. This is how the controller distinguishes the welcome
        state (lang is None) from the conversion state (lang is set) -- the
        application is stateless, nothing is remembered between requests.

        :param value: (str|None) Stored value, or None if no language was chosen yet.
        :raises: TypeError: Invalid value type.

        """
        if value is not None and type(value) is not str:
            raise TypeError(f"Given value must be a string or None. "
                            f"Got '{type(value)}' instead.")
        if value is not None and len(value.strip()) == 0:
            value = None

        self.__lang = value

    lang = property(get_lang, set_lang)

    # -----------------------------------------------------------------------
    # cue
    # -----------------------------------------------------------------------

    def get_cue(self) -> str:
        """Return the stored input cue."""
        return self.__cue

    def set_cue(self, value: str) -> None:
        """Set the stored cue after validating it.

        :param value: (str|None) Stored value.
        :raises: TypeError: Invalid type.

        """
        if value is not None and type(value) is not str:
            raise TypeError(f"Given value must be a string or None. "
                            f"Got '{type(value)}' instead.")
        if value is not None:
            value = ListCueSRecord.strip_string(value)
            if len(value) == 0:
                value = None

        self.__cue = value

    cue = property(get_cue, set_cue)

    # -----------------------------------------------------------------------
    # Extras
    # -----------------------------------------------------------------------

    def get_extras(self) -> dict:
        """Return the extra data.

        :return: (dict) Extra data

        """
        return self.__extras

    def set_extras(self, extras: dict) -> None:
        """Replace the extras mapping.

        :param extras: (dict|None) Mapping of extra data
        :raises: TypeError: extras is not a dict

        """
        if extras is None:
            self.__extras = dict()
            return

        if type(extras) is not dict:
            raise TypeError(f"extras must be of type 'dict'. Got {type(extras)} instead.")

        self.__extras = extras

    extras = property(get_extras, set_extras, None)

    def set_extra(self, key: str, value) -> None:
        """Set one extra entry.

        :param key: (str) Entry name
        :param value: (any) Raw entry value

        """
        if type(key) is not str:
            raise TypeError(f"key must be of type 'str'. Got {type(key)} instead.")

        self.__extras[key] = value

    # -----------------------------------------------------------------------
    # Overloads
    # -----------------------------------------------------------------------

    def __str__(self):
        return str(self.serialize()) + "\n"

    def __repr__(self):
        return repr(self)
