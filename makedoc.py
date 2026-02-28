# -*- coding: UTF-8 -*-
# File: makedoc.py
# Author: Brigitte Bigi
# Purpose: Generate the Auto-CS documentation using ClammingPy (>= 2.0).
#
# Install:
#   $SPPAS/.sppaspyenv~/bin/python -m pip install ClammingPy
#
# Run:
#   $SPPAS/.sppaspyenv~/bin/python makedoc.py
#
# Output:
#   - HTML documentation is generated into ./docs/
#   - The generated site includes the root README.md and all README.md files
#     found inside the exported packages.
#   - Open: ./docs/index.html
#
# Accessibility / UI:
#   - Semantic HTML5 output (better support with screen readers).
#   - Themes supported by the statics: light, dark, and (if provided) contrast.
#   - Contrast mode targets WCAG-friendly readability (spacing) and can use a
#     dyslexia-friendly font (if provided by the statics).
#
# This file is part of Auto-CS tool.
# Copyright (C) 2022-2026 Brigitte Bigi, CNRS
# Laboratoire Parole et Langage, Aix-en-Provence, France.
#
# Use of this software is governed by the GNU Affero Public License, version 3.
#
# Auto-CS is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Auto-CS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Auto-CS. If not, see <https://www.gnu.org/licenses/>.
#
# This banner notice must not be removed.
#
# ---------------------------------------------------------------------------

import sys
import logging
import os

PROGRAM = os.path.abspath(__file__)
SPPAS = os.getenv('SPPAS')
if SPPAS is None:
    raise ImportError("SPPAS environment variable is not defined.")
sys.path.append(SPPAS)
sys.path.append(os.path.join("autocs", "sppas", "src", "annotations"))

import autocs
import CuedSpeech

try:
    import clamming
except ImportError:
    print("This program requires ClammingPy (documentation generator).")
    print("Install it with: python -m pip install ClammingPy")
    print("Then run: python makedoc.py")
    sys.exit(-1)

# ---------------------------------------------------------------------------
logging.getLogger().setLevel(0)

# List of modules to be documented.
packages = list()
packages.append(CuedSpeech)
packages.append(CuedSpeech.whatkey)
packages.append(CuedSpeech.whenhand)
packages.append(CuedSpeech.whenhand.transition)
packages.append(CuedSpeech.wherecue)
packages.append(CuedSpeech.wherecue.angle)
packages.append(CuedSpeech.wherecue.position)
packages.append(CuedSpeech.whowtag)
packages.append(CuedSpeech.whowtag.hands)
packages.append(CuedSpeech.whowtag.whowimgtag)

# Options for HTML exportation
opts_export = clamming.ExportOptions()
opts_export.software = 'Auto-CS ' + autocs.__version__
opts_export.url = 'https://sourceforge.net/projects/autocs/'
opts_export.copyright = autocs.__copyright__
opts_export.title = 'Auto-CS doc'
# ... statics is the relative path to a folder with custom CSS, JS, etc.
opts_export.statics = './statics'
# ... the favicon and icon are files in the statics folder
opts_export.favicon = 'autocs32x32.ico'
opts_export.icon = 'autocs.png'
# ... the theme corresponds to a statics/<theme>.css file or "light" or "dark"
opts_export.theme = 'light'
# ... path to 'wexa_statics' folder, relatively to "docs"
opts_export.wexa_statics = "./Whakerexa-2.0/wexa_statics"


# -------------------------------------------------
# Generate documentation
# -------------------------------------------------
clams_modules = clamming.ClamsModules(packages)

# Export documentation into HTML files.
# One .html file = one documented class.
clams_modules.html_export_packages("docs", opts_export, "README.md")
print("HTML Documentation generated. Open: docs/index.html")

# Export documentation into a Markdown file.
# One .md file = one documented module.
clams_modules.markdown_export_packages("docs", opts_export)
print("Markdown Documentation generated. Open: docs/*.md files.")

