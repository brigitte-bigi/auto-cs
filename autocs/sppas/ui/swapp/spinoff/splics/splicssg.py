"""
:filename: sppas.ui.swapp.spinoff.splics.splicssg.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: The global settings of the SPLI:CS spin-off applications.

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

from sppas.ui.swapp.wappcore.wappsg import wapp_settings

# ---------------------------------------------------------------------------


class splicsPathSettings:
    """Immutable class to manage the statics paths of SPLICS.

    The spin-off owns its statics: they are all gathered into the
    "spinoff/splics/" folder of the swapp statics, so that no file of a
    spin-off is mixed with the ones of SPPAS nor with the ones of another
    spin-off. The only thing the spin-off asks to swapp is where its statics
    are served from.

    :Example:
    >>> with splicsPathSettings() as paths:
    >>>     print(paths.css)
    >>>     # Outputs the relative path to the CSS of the spin-off

    """

    def __init__(self):
        """Create the splicsPathSettings dictionary.

        """
        # Temporarily mutable
        self._is_frozen = False
        # Where the statics of the spin-off are served from
        statics = wapp_settings.statics + "spinoff/splics/"

        # Define the relative paths
        self.__dict__ = dict(
            statics=statics,
            css=statics + "css/",
            js=statics + "js/",
            icons=statics + "icons/",
            images=statics + "images/"
        )

        # Freeze the instance
        self._is_frozen = True

    # -----------------------------------------------------------------------
    # Overloads
    # -----------------------------------------------------------------------

    def __enter__(self):
        return self

    # -----------------------------------------------------------------------

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    # -----------------------------------------------------------------------

    def __setattr__(self, key, value):
        """Override to prevent any attribute setter."""
        if getattr(self, "_is_frozen", False):
            raise AttributeError(f"{self.__class__.__name__} object is immutable")
        super().__setattr__(key, value)

    # -----------------------------------------------------------------------

    def __delattr__(self, key):
        """Override to prevent any attribute deletion."""
        if getattr(self, "_is_frozen", False):
            raise AttributeError(f"{self.__class__.__name__} object is immutable")
        super().__delattr__(key)

# ---------------------------------------------------------------------------


class splicsCategorySettings:
    """Immutable class of the application categories of SPLI:CS.

    The SPLI:CS applications are sorted into three categories, the three
    learning modules of the application. Each application declares its category
    by setting its CATEGORY member to one of the members of this class:

    >>> CATEGORY = splics_categories.discovery

    The `ordered` member gives the categories in their display order, for the
    dashboard to build one section per category.

    :Example:
    >>> with splicsCategorySettings() as categories:
    >>>     print(categories.discovery)

    """

    def __init__(self):
        """Create the splicsCategorySettings dictionary.

        """
        # Temporarily mutable
        self._is_frozen = False
        self.__dict__ = dict(
            # The learning module: the Cued Speech coding applications.
            discovery="discovery",
            # The self-testing module: the interactive assessments.
            exploration="exploration",
            # The consolidation module: the games.
            recreation="recreation"
        )
        # The three categories, in display order.
        self.ordered = (self.discovery, self.exploration, self.recreation)
        # Freeze the instance
        self._is_frozen = True

    # -----------------------------------------------------------------------
    # Overloads
    # -----------------------------------------------------------------------

    def __enter__(self):
        return self

    # -----------------------------------------------------------------------

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    # -----------------------------------------------------------------------

    def __setattr__(self, key, value):
        """Override to prevent any attribute setter."""
        if getattr(self, "_is_frozen", False):
            raise AttributeError(f"{self.__class__.__name__} object is immutable")
        super().__setattr__(key, value)

    # -----------------------------------------------------------------------

    def __delattr__(self, key):
        """Override to prevent any attribute deletion."""
        if getattr(self, "_is_frozen", False):
            raise AttributeError(f"{self.__class__.__name__} object is immutable")
        super().__delattr__(key)

# ---------------------------------------------------------------------------


# Instantiate the global paths of the spin-off
splics_paths = splicsPathSettings()

# Instantiate the application categories of the spin-off
splics_categories = splicsCategorySettings()
