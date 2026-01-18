"""
:filename: sppas.ui.swapp.app_textcued.textcuedmaker.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Response for the web-based application "Text Cued" of SPPAS.

.. _This file is part of AutoCuedSpeech: <https://auto-cuedspeech.org/>
.. _Originally developed in SPPAS: <https://sppas.org/>
..
    ---------------------------------------------------------------------

    Copyright (C) 2011-2025  Brigitte Bigi, CNRS
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

import logging

from whakerpy.htmlmaker import HTMLNode
from whakerkit.responses import WhakerKitResponse

from sppas.ui.swapp.wappsg import wapp_settings
from sppas.ui.swapp import sppasImagesAccess
from sppas.ui.swapp.htmltags import SwappHeader
from sppas.ui.swapp.htmltags import SwappFooter
from sppas.ui import _

from .annotate_manager import AnnViewManager
from .annotate_manager import AnnViewBar

# -----------------------------------------------------------------------


JS_SCRIPT = """
// Function to change button selected
function select_token_phon(button) {
    if (button.classList.contains("phon_chosen")) {
        console.log("button phon already chosen!");
        return null;
    }

    const token_buttons = document.getElementsByName(button.name);
    token_buttons.forEach(current_btn => {
        current_btn.classList.remove("phon_chosen");
        current_btn.classList.add("phon_not_chosen");
        current_btn.disabled = false;
    });

    button.classList.add("phon_chosen");
    button.disabled = true;

    // remove text in the input
    const token = button.name.split('_')[0];
    let input_phon = document.getElementById(token + "_phon_input");
    input_phon.value = "";
}

// Function onchange of the input to deselected the phon button
function input_onchange(input) {
    if (input.value.length > 0) {
        const token = input.name.split('_')[0];
        const phon_buttons = document.getElementsByName(token + "_button");

        for (let current_button of phon_buttons) {
            current_button.classList.remove("phon_chosen");
            current_button.classList.add("phon_not_chosen");
            current_button.disabled = false;
        }
    }
}
"""

JS_WEXA_ONLOAD = """
window.Wexa.onload.addLoadFunction(() => {
    // Override submit of the cuedspeech form to send phonemes chooses by the user
    let base_form = document.getElementById("annotate_form");

    base_form.addEventListener("submit", event => {
        // create a new form
        const valid_form = document.createElement("form");
        valid_form.method = "POST";
        valid_form.style.display = "none";

        // find all phon inputs to set the correct phon values selected
        for (let input of base_form) {
            let name = input.name;
            let value = input.value;

            // if it's an input where the user write the custom phon
            if (name.endsWith("phon_input")) {
                // if it's empty we take the selected phon
                if (value.length === 0) {
                    const token = name.split('_')[0];
                    const phonemes = document.getElementsByName(token + "_button");

                    // find the selected phon
                    for (let phon_button of phonemes) {
                        if (phon_button.classList.contains("phon_chosen")) {
                            input.value = phon_button.innerText;
                            break;
                        }
                    }
                }
            }
        }

        return true;
    });
});

"""

MSG_APP_TITLE = _("Automatic CuedSpeech from Text")
MSG_TITLE = _("Text Cueing")
MSG_DESCR = _("Allows to generate automatically the sequence of keys to be cued from a written text")
MSG_H1 = _("Cueing from a written text")

# -----------------------------------------------------------------------


class TextCuedResponseRecipe(WhakerKitResponse):
    """The textcueing.html HTTPD response baker.

    This application allows to generate automatically the sequence of keys to
    be cued from a written text in the UI. It performs the followings:

    1. Text Normalization
    2. Phonetization
    3. Basic Alignment
    4. Cued Speech (the 'what' question only)

    """

    def __init__(self, name="TextCuedMaker", tree=None, title=MSG_TITLE):
        super(TextCuedResponseRecipe, self).__init__(name, tree, title)

        # create the fieldsets manager and instantiate all fieldsets
        self.__views = AnnViewManager(self._htree.body_main.identifier)

    # -----------------------------------------------------------------------
    # STATIC METHODS
    # -----------------------------------------------------------------------

    @classmethod
    def page(cls) -> str:
        """Return a short description of the application."""
        return "textcueing.html"

    # -----------------------------------------------------------------------
    # PUBLIC METHODS
    # -----------------------------------------------------------------------

    def create(self) -> None:
        """Override. Create the fixed page content in HTML.

        The fixed content corresponds to the parts that can't be invalidated:
        head, body_header, body_footer.

        """
        super().create()
        self._htree.head.link(rel="logo icon", href=wapp_settings.icons + "ACS_text.png")

        # Add custom statics
        self._htree.head.link("stylesheet", wapp_settings.css + "/main_swapp.css", link_type="text/css")
        self._htree.head.link("stylesheet", wapp_settings.css + "/page_textcued.css", link_type="text/css")

        # JS for CS generation -- required only for the cuedspeech fieldset.
        script = HTMLNode(self._htree.head.identifier, None, "script",
                          value=JS_WEXA_ONLOAD, attributes={'type': "module"})
        self._htree.head.append_child(script)
        script = HTMLNode(self._htree.head.identifier, "view-script", "script", value=JS_SCRIPT)
        self._htree.head.append_child(script)

        self._htree.body_header = SwappHeader(self._htree.identifier, title=MSG_APP_TITLE)
        self._htree.body_footer = SwappFooter(self._htree.identifier)

    # -----------------------------------------------------------------------

    def _process_events(self, events: dict, **kwargs) -> bool:
        """Process the given events coming from the POST of any form.

        :param events (dict): The events received by the server (key=event_name, value=event_value)
        :return: (bool) True if the whole page must be re-created

        """
        logging.debug(f" >>>>> Page Text Cued Annotation -- Process events: {events} <<<<<< ")
        success = self.__views.process_annotate_events(events)
        if success is True:
            self._status.code = 200
        else:
            self._status.code = 400
            # 400 Bad Request response status code indicates that the server
            # cannot or will not process the request due to something that is
            # perceived to be a client error.

        return True

    # -----------------------------------------------------------------------

    def _bake(self):
        """Create the dynamic page content in HTML.

        """
        sec = HTMLNode(self._htree.body_main.identifier, None, "section")
        self._htree.body_main.append_child(sec)

        node = HTMLNode(sec.identifier, None, "h1", value=MSG_H1)
        sec.append_child(node)

        # Create the HTML current view --
        # The view **must** be created before the wizard.
        view = self.__views.get_current_view()
        view.update()

        # Create the views bar and append -- before the view to display it at top
        self.__views_bar = AnnViewBar(self._htree.body_main.identifier, self.__views)
        self._htree.body_main.append_child(self.__views_bar)

        # Append view in the body_main
        self._htree.body_main.append_child(view)

        # Special for cued speech view
        if view.identifier == "cuedspeech":
            script = view.get_js_script(self._htree.head.identifier)
            self._htree.head.remove_child(script.identifier)
            self._htree.head.append_child(script)
            wexa_module = view.get_js_module(self._htree.head.identifier)
            self._htree.head.remove_child(wexa_module.identifier)
            self._htree.head.append_child(wexa_module)
