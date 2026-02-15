"""
:filename: sppas.ui.app_textcues.textcues_record.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Data class.

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
import re

from .textcues_settings import TextCueSSettings

# ---------------------------------------------------------------------------


class TextCueSRecord:
    """Container for all extracted data.

    Allows data check, and transport between the models and the views.

    """

    # Known TextCuesRecord fields, by expected type.
    INT_FIELDS = {
        'mode',
        'model_pos',
        'model_angle',
        'model_timing',
    }

    STR_FIELDS = {
        'pathway',
        'lang',
        'alphabet',
        'text'
    }

    LIST_FIELDS = { # can be a tuple instead
        'textnorm',
        'phonetize',
        'cuedphons'
        'cuedkeys'
    }

    # -----------------------------------------------------------------------

    def __init__(self, pathway_id: str = "", lang: str = None, alphabet: str = None):
        """Initialize the minimal required data.

        :param pathway_id: (str) An 'id' of a PathwayBaseView inherited class.
        :param lang: (str|None) ISO639-3 of a supported language. Set to default if None.
        :param alphabet: (str|None) One of the supported alphabets. Set to default if None.

        """
        # Required fields
        self.__pathway = ""
        self.__lang = None
        self.__alphabet = None
        self.set_pathway(pathway_id)
        self.set_lang(lang)
        self.set_alphabet(alphabet)

        # Optional ones
        self.__text = None        # given input text
        self.__textnorm = None    # normalized text
        self.__textprons = None   # phonetized text with variants
        self.__phonetize = None   # phonetized text -- one pronunciation per token
        self.__cuedphons = None   # phonetized keys
        self.__cuedkeys = None    # coded keys
        self.__mode = None

        self.__model_pos = None
        self.__model_angle = None
        self.__model_timing = None

        # Any extra data
        self.__extras = dict()

    # -----------------------------------------------------------------------

    def reset(self):
        """Reset all entries but pathway."""
        self.__lang = None
        self.__alphabet = None

        # Optional ones
        self.__text = None
        self.__mode = None
        self.reset_results()

        self.__model_pos = None
        self.__model_angle = None
        self.__model_timing = None

        # Any extra data
        self.__extras = dict()

    # -----------------------------------------------------------------------

    def reset_results(self):
        """Reset the estimated data."""
        self.__textnorm = None
        self.__textprons = None
        self.__phonetize = None
        self.__cuedphons = None
        self.__cuedkeys = None

    # -----------------------------------------------------------------------
    # Formatters and converters
    # -----------------------------------------------------------------------

    @staticmethod
    def remove_ascii_punctuation(text: str) -> str:
        """Remove ASCII punctuation characters from text."""
        return text.translate(str.maketrans('', '', '"\n\r\t#'))

    # -----------------------------------------------------------------------

    @staticmethod
    def strip_string(entry) -> str:
        """Strip the string: multiple whitespace, tab and CR/LF.

         Remove multiple whitespace, tab and CR/LF inside the string.

         :return: (str)

         """
        e = re.sub("[\t]+", r" ", entry)
        e = re.sub("[\n]+", r" ", e)
        e = re.sub("[\r]+", r" ", e)
        if "\ufeff" in e:
            e = re.sub("\ufeff", r" ", e)

        e = re.sub("[\\s]+", r" ", e)
        return e

    # ---------------------------------------------------------------------------

    @staticmethod
    def format_string(entry: str) -> str:
        """Convert the string into a string.

        :param entry: (str) String

        """
        e = TextCueSRecord.strip_string(entry)
        return e.replace("'", "%27")

    # -----------------------------------------------------------------------

    @staticmethod
    def parse_string(entry: str) -> str:
        """Convert the string into a string.

        :param entry: (str) String

        """
        e = TextCueSRecord.strip_string(entry)
        return e.replace("%27", "'")

    # -----------------------------------------------------------------------

    @staticmethod
    def format_entry(entry: list) -> str:
        """Stringifies the given list of entries.

        :param entry: (list|tuple) List of entries
        :return: (str)

        """
        serialized = " ".join(entry)
        return TextCueSRecord.format_string(serialized)

    # -----------------------------------------------------------------------

    @staticmethod
    def parse_entry(entry: str) -> list:
        """Convert the string into a list.

        :param entry: (str) String
        :return: (list) List

        """
        _s = TextCueSRecord.parse_string(entry)
        return _s.split(" ")

    # -----------------------------------------------------------------------
    # Functions
    # -----------------------------------------------------------------------

    def serialize(self) -> dict:
        """Return a dictionary with serialized record data for transport.

        :return: (dict)

        """
        d = dict()

        # Mandatory data for transport
        # ----------------------------
        d["pathway"] = self.__pathway
        d["lang"] = "" if self.__lang is None else self.__lang
        d["alphabet"] = "" if self.__alphabet is None else self.__alphabet
        d["mode"] = "0" if self.__mode is None else str(self.__mode)

        # Other data are optional
        # -----------------------
        if self.__text is not None and len(self.__text) > 0:
            d["text"] = self.format_string(self.__text)
        if self.__textnorm is not None and len(self.__textnorm) > 0:
            d["textnorm"] = self.format_entry(self.__textnorm)
        if self.__textprons is not None and len(self.__textprons) > 0:
            d["textprons"] = self.format_entry(self.__textprons)
        if self.__phonetize is not None and len(self.__phonetize) > 0:
            d["phonetize"] = self.format_entry(self.__phonetize)
        if self.__cuedphons is not None and len(self.__cuedphons) > 0:
            d["cuedphons"] = self.format_entry(self.__cuedphons)
        if self.__cuedkeys is not None and len(self.__cuedkeys) > 0:
            d["cuedkeys"] = self.format_entry(self.__cuedkeys)

        if self.__model_pos is not None:
            d["model_pos"] = str(self.__model_pos)
        if self.__model_angle is not None:
            d["model_angle"] = str(self.__model_angle)
        if self.__model_timing is not None:
            d["model_timing"] = str(self.__model_timing)

        return d

    # -----------------------------------------------------------------------
    
    def parse(self, data: dict):
        """Fills-in the record with data.
        
        :param data: (dict) Dictionary
        
        """
        self.reset()
        if "pathway" in data:
            self.set_pathway(data["pathway"])
        if "lang" in data:
            self.set_lang(data["lang"])
        if "alphabet" in data:
            self.set_alphabet(data["alphabet"])
        if "mode" in data:
            self.set_mode(int(data["mode"]))

        if "text" in data:
            self.set_text(TextCueSRecord.parse_string(data["text"]))

        if "textnorm" in data:
            self.set_textnorm(TextCueSRecord.parse_entry(data["textnorm"]))
        if "textprons" in data:
            self.set_textprons(TextCueSRecord.parse_entry(data["textprons"]))
        if "phonetize" in data:
            self.set_phonetize(TextCueSRecord.parse_entry(data["phonetize"]))
        if "cuedphons" in data:
            self.set_cuedphons(TextCueSRecord.parse_entry(data["cuedphons"]))
        if "cuedkeys" in data:
            self.set_cuedkeys(TextCueSRecord.parse_entry(data["cuedkeys"]))

        if "model_pos" in data:
            self.set_model_pos(int(data["model_pos"]))
        if "model_angle" in data:
            self.set_model_angle(int(data["model_angle"]))
        if "model_timing" in data:
            self.set_model_timing(int(data["model_timing"]))

    # -----------------------------------------------------------------------
    # pathway
    # -----------------------------------------------------------------------

    def get_pathway(self) -> str:
        """Return the stored 'id' of the current view."""
        return self.__pathway

    def set_pathway(self, value: str) -> None:
        """Set the stored 'id' after validating it.

        :param value: (str) Stored value among the allowed ones.
        :raises: TypeError: Invalid value.
        :raises: ValueError: Invalid value.

        """
        if type(value) is not str:
            raise TypeError(f"Given value must be a string. "
                            f"Got '{type(value)}' instead.")
        self.__pathway = value

    pathway = property(get_pathway, set_pathway)

    # -----------------------------------------------------------------------
    # lang
    # -----------------------------------------------------------------------

    def get_lang(self) -> str:
        """Return the stored lang code."""
        return self.__lang

    def set_lang(self, value: str) -> None:
        """Set the stored 'lang' after validating it.

        :param value: (str|None) Stored value among the allowed ones.
        :raises: TypeError: Invalid value type.

        """
        if value is not None and type(value) is not str:
            raise TypeError(f"Given value must be a string or None. "
                            f"Got '{type(value)}' instead.")
        if value is None:
            with TextCueSSettings() as st:
                value = st.lang

        self.__lang = value

    lang = property(get_lang, set_lang)

    # -----------------------------------------------------------------------
    # alphabet
    # -----------------------------------------------------------------------

    def get_alphabet(self) -> str:
        """Return the stored lang code."""
        return self.__alphabet

    def set_alphabet(self, value: str) -> None:
        """Set the stored 'alphabet' after validating it.

        :param value: (str|None) Stored value among the allowed ones.
        :raises: ValueError: Invalid value.

        """
        if value is None:
            with TextCueSSettings() as st:
                value = st.alphabet
        accepted = (None, "X-SAMPA", "IPA")
        if value not in accepted:
            raise ValueError(f"Invalid given alphabet value: '{value}'.")
        self.__alphabet = value

    alphabet = property(get_alphabet, set_alphabet)

    # -----------------------------------------------------------------------
    # text (user input)
    # -----------------------------------------------------------------------

    def get_text(self) -> str:
        """Return the stored input text."""
        return self.__text

    def set_text(self, value: str) -> None:
        """Set the stored text after validating it.

        :param value: (str) Stored value.
        :raises: TypeError: Invalid type.
        :raises: ValueError: Invalid value.

        """
        if value is not None and type(value) is not str:
            raise TypeError(f"Given value must be a string or None. "
                            f"Got '{type(value)}' instead.")
        if value is not None:
            value = TextCueSRecord.strip_string(value)
            if len(value) == 0:
                raise ValueError("Given value can't be an empty string.")

        self.__text = self.remove_ascii_punctuation(value)

    text = property(get_text, set_text)

    # -----------------------------------------------------------------------
    # textnorm
    # -----------------------------------------------------------------------

    def get_textnorm(self) -> list:
        """Return the stored normalized tokens."""
        return self.__textnorm

    def set_textnorm(self, value: list) -> None:
        """Set the sored normalized text after validating it.

        :param value: (list) Stored value among the allowed ones.
        :raises: TypeError: Invalid type.
        :raises: ValueError: Invalid value.

        """
        if value is not None and type(value) not in (tuple, list):
            raise TypeError(f"Given value must be a list, tuple or None. "
                            f"Got '{type(value)}' instead.")
        if value is not None:
            if len(value) == 0:
                raise ValueError("Given value can't be an empty list.")
            for item in value:
                if isinstance(item, str) is False or len(item) == 0:
                    raise ValueError(f"Invalid value item '{item}'.")

            self.__textnorm = value
        else:
            self.__textnorm = None

    textnorm = property(get_textnorm, set_textnorm)

    # -----------------------------------------------------------------------
    # textprons
    # -----------------------------------------------------------------------

    def get_textprons(self) -> list:
        """Return the stored pronunciation with variants of each token."""
        return self.__textprons

    def set_textprons(self, value: list) -> None:
        """Set the stored pronunciations of the text after validating it.

        :param value: (list) Stored value among the allowed ones.
        :raises: TypeError: Invalid type.
        :raises: ValueError: Invalid value.

        """
        if value is not None and type(value) not in (tuple, list):
            raise TypeError(f"Given value must be a list, tuple or None. "
                            f"Got '{type(value)}' instead.")
        if value is not None:
            if len(value) == 0:
                raise ValueError("Given value can't be an empty list.")
            for item in value:
                if isinstance(item, str) is False or len(item) == 0:
                    raise ValueError(f"Invalid value item '{item}'.")

            self.__textprons = value
        else:
            self.__textprons = None

    textprons = property(get_textprons, set_textprons)

    # -----------------------------------------------------------------------
    # phonetize
    # -----------------------------------------------------------------------

    def get_phonetize(self) -> list:
        """Return the stored selected pronunciation of each token."""
        return self.__phonetize

    def set_phonetize(self, value: list) -> None:
        """Set the stored phonetized text after validating it.

        :param value: (list) Stored value among the allowed ones.
        :raises: TypeError: Invalid type.
        :raises: ValueError: Invalid value.

        """
        if value is not None and type(value) not in (tuple, list):
            raise TypeError(f"Given value must be a list, tuple or None. "
                            f"Got '{type(value)}' instead.")
        if value is not None:
            if len(value) == 0:
                raise ValueError("Given value can't be an empty list.")
            for item in value:
                if isinstance(item, str) is False or len(item) == 0:
                    raise ValueError(f"Invalid value item '{item}'.")

            self.__phonetize = value
        else:
            self.__phonetize = None

    phonetize = property(get_phonetize, set_phonetize)

    # -----------------------------------------------------------------------
    # cuedspeech
    # -----------------------------------------------------------------------

    def get_cuedphons(self) -> list:
        """Return the stored sequence of coded phonemes."""
        return self.__cuedphons

    def set_cuedphons(self, value: list) -> None:
        """Set the stored sequence coded phonemes after validating it.

        :param value: (list) Stored value among the allowed ones.
        :raises: TypeError: Invalid type.
        :raises: ValueError: Invalid value.

        """
        if value is not None and type(value) not in (tuple, list):
            raise TypeError(f"Given value must be a list, tuple or None. "
                            f"Got '{type(value)}' instead.")
        if value is not None:
            if len(value) == 0:
                raise ValueError("Given value can't be an empty list.")

            self.__cuedphons = value
        else:
            self.__cuedphons = None

    cuedphons = property(get_cuedphons, set_cuedphons)

    # -----------------------------------------------------------------------

    def get_cuedkeys(self) -> list:
        """Return the stored sequence of coded keys."""
        return self.__cuedkeys

    def set_cuedkeys(self, value: list) -> None:
        """Set the stored sequence of coded keys after validating it.

        :param value: (list) Stored value among the allowed ones.
        :raises: TypeError: Invalid type.
        :raises: ValueError: Invalid value.

        """
        if value is not None and type(value) not in (tuple, list):
            raise TypeError(f"Given value must be a list, tuple or None. "
                            f"Got '{type(value)}' instead.")
        if value is not None:
            if len(value) == 0:
                raise ValueError("Given value can't be an empty list.")

            self.__cuedkeys = value
        else:
            self.__cuedkeys = None

    cuedkeys = property(get_cuedkeys, set_cuedkeys)

    # -----------------------------------------------------------------------
    # mode
    # -----------------------------------------------------------------------

    def get_mode(self) -> int:
        """Return the displayed mode for the result.

        """
        return self.__mode

    def set_mode(self, value: int) -> None:
        """Set the mode value.

        Allowed modes:
        - 0: images
        - 1: overlays
        - 2: video

        :param value: (str|None) Mode among the allowed ones.
        :raises: TypeError: Invalid type of the given value.
        :raises: ValueError: Invalid mode value.

        """
        if value is not None and type(value) is not int:
            raise TypeError("Given value must be an int or None")

        accepted = (None, 0, 1, 2)
        if value not in accepted:
            raise ValueError(f"Invalid given value: '{value}'.")

        self.__mode = value

    mode = property(get_mode, set_mode)

    # -----------------------------------------------------------------------
    # model_pos
    # -----------------------------------------------------------------------

    def get_model_pos(self) -> int:
        """Return the model position value."""
        return self.__model_pos

    def set_model_pos(self, value: int) -> None:
        """Set the model position value.

        :param value: (int|None) Model number
        :raises: TypeError: Invalid type of the given value.
        :raises: ValueError: Invalid model value.

        """
        if value is not None and type(value) is not int:
            raise TypeError("Given value must be an int or None")

        accepted = (None, 0, 1, 2, 3, 4)
        if value not in accepted:
            raise ValueError(f"Invalid given value: '{value}'.")

        self.__model_pos = value

    model_pos = property(get_model_pos, set_model_pos)

    # -----------------------------------------------------------------------
    # model_angle
    # -----------------------------------------------------------------------

    def get_model_angle(self) -> int:
        """Return the model angle value."""
        return self.__model_angle

    def set_model_angle(self, value: int) -> None:
        """Set the model angle value.

        :param value: (int|None) Model number
        :raises: TypeError: Invalid type of the given value.
        :raises: ValueError: Invalid model value.

        """
        if value is not None and type(value) is not int:
            raise TypeError("Given value must be an int or None")

        accepted = (None, 0, 1, 2, 3, 4)
        if value not in accepted:
            raise ValueError(f"Invalid given value: '{value}'.")

        self.__model_angle = value

    model_angle = property(get_model_angle, set_model_angle)

    # -----------------------------------------------------------------------
    # model_timing
    # -----------------------------------------------------------------------

    def get_model_timing(self) -> int:
        """Return the model timing value."""
        return self.__model_timing

    def set_model_timing(self, value: int) -> None:
        """Set the model timing value.

        :param value: (int|None) Model number
        :raises: TypeError: Invalid type of the given value.
        :raises: ValueError: Invalid model value.

        """
        if value is not None and type(value) is not int:
            raise TypeError("Given value must be an int or None")

        accepted = (None, 0, 1, 2, 3, 4)
        if value not in accepted:
            raise ValueError(f"Invalid given value: '{value}'.")

        self.__model_timing = value

    model_timing = property(get_model_timing, set_model_timing)

    # -----------------------------------------------------------------
    # Extras
    # -----------------------------------------------------------------

    def get_extras(self) -> dict:
        """Return extra CSV columns.

        :return: (dict) Extra columns

        """
        return self.__extras

    def set_extras(self, extras: dict) -> None:
        """Replace extras mapping.

        :param extras: (dict) Mapping of extra columns
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
        """Set one extra column.

        :param key: (str) Column name
        :param value: (any) Raw cell value

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
