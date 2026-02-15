"""
:filename: sppas.ui.swapp.app_textcues.textcues_view.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Main view of "TextCueS" app.

..
    This file is part of AutoCS: <https://autocs.sourceforge.io>
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

from whakerpy.htmlmaker import HTMLTree
from whakerpy.htmlmaker import HTMLNode
from whakerpy.htmlmaker import EmptyNode
from whakerpy.htmlmaker.htmnodes.htmnode import TagNode

from sppas.ui import _
from sppas.ui.swapp.wappsg import wapp_settings
from sppas.ui.swapp.apps.swapp_view import swappBaseView
from sppas.ui.swapp.apps.swapp_view import JS_INIT
from sppas.ui.swapp.apps.swapp_view import JS_WEXA_ONLOAD

from .textcues_record import TextCueSRecord
from .textcues_msg import MSG_APP_TITLE
from .textcues_msg import MSG_APP_TITLE1
from .textcues_msg import MSG_APP_TITLE2
from .textcues_msg import MSG_ERROR_DETAILS
from .views.nodes.footer import FooterNode
from .views.nodes.nav import NavUtils
from .views.nodes.yoyo_message import YoyoInfoNode
from .views.nodes.yoyo_message import YoyoErrorNode
from .views.welcome_view import TextCueSWelcomeView
from .views.pathway_text_view import PathwayTextView
from .views.pathway_sound_view import PathwaySoundView
from .views.pathway_code_view import PathwayCodeView

# ---------------------------------------------------------------------------

MSG_SKIP = _("Skip to content")

BODY_SCRIPT = f"""
        import {{ TextCueSManager }} from '/{wapp_settings.js}textcues_manager.js';
        const textcuesManager = new TextCueSManager();
        textcuesManager.handleTextCueSManagerOnLoad();
"""

# ---------------------------------------------------------------------------


class TextCueSView(swappBaseView):
    """View class is responsible for populating the *textcues_*.html* page.

    This class represents the **View** component of the MVC pattern for the
    TextCueS web application. It receives an existing :class:`HTMLTree`
    instance and fills it with all static and dynamic visual content.

    The :class:`TextCueSView` does not manage user events nor business logic;
    it focuses solely on defining the HTML structure and resources required
    for rendering the TextCueS coding interface.

    The generated content includes:
        - Head section with meta, stylesheets, and JS imports.
        - Header (title, navigation buttons, accessibility controls).
        - Main content area .
        - Footer with copyright information.
        - Script element

    """

    def __init__(self, tree: HTMLTree, is_welcome: bool = False):
        """Initialize and populate the TextCueS view structure.

        :param tree: (HTMLTree) An existing HTML tree to populate with
                     the setup-specific content.
        :param is_welcome: (bool) Whether to display the welcome content of the coding one.
        :raises: TypeError: tree is not an instance of HTMLTree

        """
        if isinstance(tree, HTMLTree) is False:
            raise TypeError("TextCueSView: tree must be an instance of HTMLTree. "
                            "Got {} instead.".format(type(tree)))
        self._is_welcome = bool(is_welcome)
        super().__init__(tree, MSG_APP_TITLE)

    # -----------------------------------------------------------------------
    # Populate the tree
    # -----------------------------------------------------------------------

    def populate_head(self) -> None:
        """Override. Populate the `<head>` section of the HTML document.

        Adds favicon, CSS stylesheets, and JavaScript imports required for
        rendering the base web interface, including both Whakerexa and
        application-specific resources.

        """
        self._htree.head.title(MSG_APP_TITLE)

        # CSS
        # ----
        self._htree.head.link(rel="logo icon", href=wapp_settings.icons + "Refine/textcues.png")
        self._htree.head.link("stylesheet", wapp_settings.css + "main_swapp.css", link_type="text/css")
        self._htree.head.link("stylesheet", wapp_settings.wexa_statics + "css/dialog.css", link_type="text/css")
        self._htree.head.link("stylesheet", wapp_settings.css + "app_textcues.css", link_type="text/css")

        # JS
        # ----
        script = HTMLNode(self._htree.head.identifier, None, "script", value=JS_INIT)
        self._htree.head.append_child(script)
        script = HTMLNode(self._htree.head.identifier, None, "script")
        script.add_attribute("src", wapp_settings.js + "textcues_manager.js")
        script.add_attribute("type", "module")
        self._htree.head.append_child(script)

        # JS of the application -- used to load the menu manager.
        script = HTMLNode(self._htree.head.identifier, None, "script",
                          value=JS_WEXA_ONLOAD, attributes={'type': "module"})
        self._htree.head.append_child(script)

    # -----------------------------------------------------------------------

    def populate_body_header(self, title, *args, **kwargs):
        """Override. Populate the `<header>` section of the page.

        Replaces the current header with a :class:`SwappHeader` instance and
        delegates additional customization to `_populate_body_header()`.

        """
        self._htree.body_header.set_attribute("id", "header-content")

        # Skip button, for accessibility compliance
        a = HTMLNode(self._htree.body_header.identifier, None, "a", value=MSG_SKIP)
        a.set_attribute("role", "button")
        a.set_attribute("class", "skip")
        a.set_attribute("href", "#main-content")
        a.set_attribute("aria-label", "skip-to-content")
        self._htree.body_header.append_child(a)

        _c = TagNode(self._htree.body_header.identifier, None, "section")
        _c.set_attribute("id", "link-title-header")
        self._htree.body_header.append_child(_c)

        # Application logo
        home_link = TagNode(_c.identifier, None, "a")
        home_link.set_attribute("href", "textcues.html")
        home_link.set_attribute("role", "button")
        logo = EmptyNode(home_link.identifier, None, "img")
        logo.set_attribute("src", wapp_settings.icons + "Refine/textcues.png")
        logo.set_attribute("id", "home-link-logo")
        home_link.append_child(logo)
        _c.append_child(home_link)

        # Application title
        h1 = HTMLNode(_c.identifier, None, "h1", value=title)
        _c.append_child(h1)

        # Application page title
        self.append_responsive_menu_button(self._htree.body_header)
        _value = MSG_APP_TITLE1 if self._is_welcome else MSG_APP_TITLE2
        _h2 = HTMLNode(self._htree.body_header.identifier, None, "h2", value=_value)
        self._htree.body_header.append_child(_h2)

    # -----------------------------------------------------------------------

    def populate_body_nav(self, *args, **kwargs):
        """Override. Populate the `<nav>` body section."""
        self._htree.body_nav.add_attribute("id", "nav-content")
        self._htree.body_nav.add_attribute("name", "nav-content")
        self._htree.body_nav.add_attribute("class", "nav-wexa")
        self._htree.body_nav.add_attribute("class", "side")
        self._htree.body_nav.add_attribute("class", "collapsible")

        _s = TagNode(self._htree.body_nav.identifier, None, "section")
        self.append_pin_button(_s)
        self.append_accessibility_buttons(_s)
        self._htree.body_nav.append_child(_s)

        _s = TagNode(self._htree.body_nav.identifier, None, "section")
        NavUtils.append_home_link_button(_s)
        NavUtils.append_acs_link_button(_s)
        self.append_sppas_link_button(_s)
        self._htree.body_nav.append_child(_s)

    # -----------------------------------------------------------------------

    def populate_body_footer(self) -> None:
        """Override. Replace the footer body section."""
        self._htree.body_footer = FooterNode(self._htree.get_body_main())

    # -----------------------------------------------------------------------

    def populate_body_script(self) -> None:
        """Override. Populate the script body section."""
        self._htree.body_script.add_attribute("type", "module")
        self._htree.body_script.set_value(BODY_SCRIPT)

    # -----------------------------------------------------------------------
    # Update the tree -- for baking the page
    # -----------------------------------------------------------------------

    def populate_tree_content(self, record: TextCueSRecord) -> None:
        """Populate the tree content.

        :param record: (TextCueSRecord) The data to choose and fill-in the view content.
        :raises: KeyError: invalid or missing entry in given data.

        """
        if record is None:
            TextCueSWelcomeView(self._htree.body_main, f"textcues_guid.html")
        else:
            self._populate_pathway_tree(record)
            self._populate_dialogs(record)

    # -----------------------------------------------------------------------

    def _populate_pathway_tree(self, record: TextCueSRecord) -> None:
        """Populate the tree content.

        Choose and create the page view matching the given record fields.

        :param record: (TextCueSRecord) The data allowing to choose and create the view.

        """
        p = None
        if "error" in record.extras:
            # Stay on the same page
            # ---------------------

            if record.pathway in ("", PathwayTextView.get_id()):
                p = PathwayTextView(self._htree.body_main, record)

            elif record.pathway == PathwaySoundView.get_id():
                p = PathwaySoundView(self._htree.body_main, record)

            elif record.pathway == PathwayCodeView.get_id():
                p = PathwayCodeView(self._htree.body_main, record)

        else:
            # Follow the pathway: Text -> Sound -> Code
            # -----------------------------------------

            if record.pathway == PathwaySoundView.get_id():
                p = PathwayCodeView(self._htree.body_main, record)

            elif record.pathway == PathwayTextView.get_id():
                p = PathwaySoundView(self._htree.body_main, record)

            else:
            #if record.pathway in ("", PathwayCodeView.get_id()) or record.text is None:
                p = PathwayTextView(self._htree.body_main, record)

        # Create the full HTML nodes for the page content
        p.create()

    # -----------------------------------------------------------------------

    def _populate_dialogs(self, record: TextCueSRecord) -> None:
        """Add dialogs for messages and fill in if necessary.

        :param record: (TextCueSRecord) The data to choose and fill-in the view content.

        """
        self.append_alert_dialogs(self._htree.body_main)
        if "error" in record.extras:
            error_dlg = self._htree.body_main.get_child("error_dialog")
            _n = YoyoErrorNode(error_dlg.identifier)
            _n.add_attribute("class", "width_30")
            error_dlg.append_child(_n)

            _p = HTMLNode(error_dlg.identifier, None, "p", value=MSG_ERROR_DETAILS)
            _p.add_attribute("class", "error-details-title")
            error_dlg.append_child(_p)
            _p = HTMLNode(error_dlg.identifier, None, "p", value=record.extras["error"].replace("\n", "<br>"))
            _p.add_attribute("class", "error-details-content")
            error_dlg.append_child(_p)

        elif "info" in record.extras:
            info_dlg = self._htree.body_main.get_child("info_dialog")
            _n = YoyoInfoNode(info_dlg.identifier, record.extras['info'])
            _n.add_attribute("class", "width_30")
            info_dlg.append_child(_n)

    # -----------------------------------------------------------------------

    def get_displaymode_content(self, record: TextCueSRecord) -> str:
        """Return the display mode content of the cued text.

        Allows to not *create* the full PathwayCodeView but the cued result only.

        :param record: (TextCueSRecord) The data to choose and fill-in the view content.
        :raises: KeyError: invalid or missing entry in given data.
        :return: (str) The serialized HTML content depending on the displayed mode.

        """
        p = PathwayCodeView(self._htree.body_main, record)
        content = p.display_content()
        return content.serialize()
