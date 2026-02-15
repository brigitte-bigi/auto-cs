"""
:filename: sppas.ui.swpapp.textcues.views.nodes.footer.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: A footer node to display at the bottom of a page.

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

from whakerpy.htmlmaker import HTMLNode

from sppas.ui.swapp.wappsg import wapp_settings


FOOTER = """
    <hr>
    
    <p>This site respects your privacy.<br>
    We do not collect any information and do not use cookies.</p>
    <p><a href="legal-notices.html">-- Legal notices -- </a></p>

    <p>Copyright 2021-2026 Brigitte Bigi, CNRS<br>
    Laboratoire Parole et Langage, Aix-en-Provence, France</p>
    <p class="email">contact[at]sppas.org</p>
    <p>
        <a title="ORCID profile" href="https://orcid.org/0000-0003-1834-6918" target="_blank">
            <img class="socialnet" src="{PATH}/orcid.png" />
        </a>
        <a title="HAL profile" href="https://cv.hal.science/brigittebigi" target="_blank">
            <img class="socialnet" src="{PATH}/idhal.svg" />
        </a>
        <a title="SourceForge profile" href="https://sourceforge.net/u/brigittebigi/profile" target="_blank">
            <img class="socialnet" src="{PATH}/sf.png" />
        </a>
        <a title="Pypi.org profile" href="https://pypi.org/user/bigi_lpl/" target="_blank">
            <img class="socialnet" src="{PATH}/pypi.svg" />
        </a>
        <a title="Google Scholar Profile" href="https://scholar.google.fr/citations?user=eNGX8bUAAAAJ&hl=fr" target="_blank">
            <img class="socialnet" src="{PATH}/scholar.ico" />
        </a>
    </p>

    <hr>
    
    <p><a href="https://www.gnu.org/licenses/fdl-1.3.en.html" class="external-link">
        This site is under the terms of the GNU Free Documentation License, v1.3.</a></p>
    
""".format(PATH=wapp_settings.icons)

# ---------------------------------------------------------------------------


class FooterNode(HTMLNode):
    """Represent a footer element to display legal notices.

    """

    def __init__(self, parent):
        """Create a  footer node to.

        """
        super(FooterNode, self).__init__(parent, "body_footer","footer")
        self.add_attribute("id", "footer-content")
        self.set_value(FOOTER)

