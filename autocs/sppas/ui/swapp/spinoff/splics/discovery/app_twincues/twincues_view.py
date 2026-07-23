"""
:filename: sppas.ui.swapp.spinoff.splics.discovery.app_twincues.twincues_view.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Main view of "TwinCueS" app.

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
from whakerpy.htmlmaker import HTMLTree
from whakerpy.htmlmaker import HTMLNode
from whakerpy.htmlmaker import EmptyNode
from whakerpy.htmlmaker import TagNode

from sppas.ui import _
from sppas.ui.swapp.wappcore.wappsg import wapp_settings
from sppas.ui.swapp.spinoff.splics.splicssg import splics_paths
from sppas.ui.swapp.wappcore.wapputils import sppasImagesAccess
from sppas.ui.swapp.wappbase.wappview import swappBaseView
from sppas.ui.swapp.wappbase.wappview import JS_INIT
from sppas.ui.swapp.wappbase.wappview import JS_WEXA_ONLOAD

from sppas.ui.swapp.spinoff.splics.nodes.layout.footer import FooterNode
from sppas.ui.swapp.spinoff.splics.nodes.buttons.button_action import MenuLinkButtonNode
from sppas.ui.swapp.spinoff.splics.nodes.feedback.yoyo_message import YoyoInfoNode
from sppas.ui.swapp.spinoff.splics.nodes.feedback.yoyo_message import YoyoErrorNode

from .twincues_record import TwinCueSRecord
from .twincues_msg import MSG_APP_TITLE
from .twincues_msg import MSG_HOME
from .twincues_msg import MSG_APP_TITLE2
from .twincues_msg import MSG_ACS_PROJECT
from .twincues_msg import MSG_ERROR_DETAILS
from .views.welcome_view import TwinCueSWelcomeView
from .views.page_view import TwinCueSPageView

# ---------------------------------------------------------------------------

MSG_SKIP = _("Skip to content")

BODY_SCRIPT = f"""
        import {{ TwinCueSManager }} from '/{splics_paths.js}twincues_manager.js';
        const twincuesManager = new TwinCueSManager();
        twincuesManager.handleCuesManagerOnLoad();
"""

# ---------------------------------------------------------------------------


class TwinCueSView(swappBaseView):
    """View class is responsible for populating the *twincues*.html* pages.

    This class represents the **View** component of the MVC pattern for the
    TwinCueS web application. It receives an existing :class:`HTMLTree`
    instance and fills it with all static and dynamic visual content.

    The :class:`TwinCueSView` does not manage user events nor business logic;
    it focuses solely on defining the HTML structure and resources required
    for rendering the TwinCueS conversion interface.

    """

    def __init__(self, tree: HTMLTree):
        """Initialize and populate the TwinCueS view structure.

        :param tree: (HTMLTree) An existing HTML tree to populate with
                     the setup-specific content.
        :raises: TypeError: tree is not an instance of HTMLTree

        """
        if isinstance(tree, HTMLTree) is False:
            raise TypeError("TwinCueSView: tree must be an instance of HTMLTree. "
                            "Got {} instead.".format(type(tree)))
        super().__init__(tree, MSG_APP_TITLE)

    # -----------------------------------------------------------------------
    # Populate the tree
    # -----------------------------------------------------------------------

    def populate_head(self) -> None:
        """Override. Populate the `<head>` section of the HTML document.

        """
        self._htree.head.title(MSG_APP_TITLE)

        # CSS
        # ----
        self._htree.head.link(rel="logo icon", href=splics_paths.icons + "twincues.png")
        self._htree.head.link("stylesheet", wapp_settings.css + "main_swapp.css", link_type="text/css")
        self._htree.head.link("stylesheet", wapp_settings.wexa_statics + "css/dialog.css", link_type="text/css")
        self._htree.head.link("stylesheet", wapp_settings.wexa_statics + "css/extras/keypiano.css", link_type="text/css")
        self._htree.head.link("stylesheet", splics_paths.css + "app_cues.css", link_type="text/css")

        # JS
        # ----
        script = HTMLNode(self._htree.head.identifier, None, "script", value=JS_INIT)
        self._htree.head.append_child(script)
        script = HTMLNode(self._htree.head.identifier, None, "script")
        script.add_attribute("src", splics_paths.js + "twincues_manager.js")
        script.add_attribute("type", "module")
        self._htree.head.append_child(script)

        # JS of the application -- used to load the menu manager.
        script = HTMLNode(self._htree.head.identifier, None, "script",
                          value=JS_WEXA_ONLOAD, attributes={'type': "module"})
        self._htree.head.append_child(script)

    # -----------------------------------------------------------------------

    def populate_body_header(self, title, *args, **kwargs):
        """Override. Populate the `<header>` section of the page.

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
        home_link.set_attribute("href", "twincues.html")
        home_link.set_attribute("role", "button")
        logo = EmptyNode(home_link.identifier, None, "img")
        logo.set_attribute("src", splics_paths.icons + "twincues.png")
        logo.set_attribute("id", "home-link-logo")
        home_link.append_child(logo)
        _c.append_child(home_link)

        # Application title
        h1 = HTMLNode(_c.identifier, None, "h1", value=title)
        _c.append_child(h1)

        # Application page title
        self.append_responsive_menu_button(self._htree.body_header)
        _h2 = HTMLNode(self._htree.body_header.identifier, None, "h2", value=MSG_APP_TITLE2)
        self._htree.body_header.append_child(_h2)

    # -----------------------------------------------------------------------

    def _populate_body_nav(self, *args, **kwargs):
        """Override. Populate the `<nav>` body section."""
        _s = TagNode(self._htree.body_nav.identifier, None, "section")
        self.append_pin_button(_s)
        self.append_accessibility_buttons(_s)
        self._htree.body_nav.append_child(_s)

        _s = TagNode(self._htree.body_nav.identifier, None, "section")
        _home = MenuLinkButtonNode(_s.identifier, "link-welcome_button", "index.html")
        # Handled by whakerexa's LinkController (see links.js): "_self"
        # navigates in the current tab, unlike the default "_blank".
        _home.add_attribute("data-target", "_self")
        _home.set_svg_icon(sppasImagesAccess.get_wexa_svg_icon("house"), MSG_HOME)
        _s.append_child(_home)

        _acs = MenuLinkButtonNode(_s.identifier, "link-acs_button", "https://auto-cuedspeech.org/")
        _acs.set_icon(None, splics_paths.icons + "ACS_project.png")
        _acs.set_text(MSG_ACS_PROJECT)
        _s.append_child(_acs)

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

    def populate_tree_content(self, record: TwinCueSRecord) -> None:
        """Populate the tree content.

        No language chosen yet (record.lang is None) shows the welcome
        content (intro and language choice form); a language having reached
        the controller shows the conversion content (word/cue and result).

        :param record: (TwinCueSRecord) The data to fill-in the view content.

        """
        if record.lang is None:
            TwinCueSWelcomeView(self._htree.body_main, record)
        else:
            self.append_alert_dialogs(self._htree.body_main)
            self._populate_dialogs(record)
            _p = TwinCueSPageView(self._htree.body_main, record)
            _p.create()

    # -----------------------------------------------------------------------

    def _populate_dialogs(self, record: TwinCueSRecord) -> None:
        """Fill-in the error or info dialog, if the record has such an extra.

        :param record: (TwinCueSRecord) The data to choose and fill-in the view content.

        """
        if "error" in record.extras:
            error_dlg = self._htree.body_main.get_child("error_dialog")
            for node in self.__build_error_dialog_nodes(error_dlg.identifier, record):
                error_dlg.append_child(node)

        elif "info" in record.extras:
            info_dlg = self._htree.body_main.get_child("info_dialog")
            info_dlg.append_child(self.__build_info_dialog_node(info_dlg.identifier, record))

    # -----------------------------------------------------------------------

    @staticmethod
    def __build_error_dialog_nodes(parent_id: str, record: TwinCueSRecord) -> list:
        """Build the Yoyo-styled error dialog nodes, not attached to any parent.

        :param parent_id: (str) Identifier to reference as the nodes' parent.
        :param record: (TwinCueSRecord) The data holding the "error" extra.
        :return: (list) The Yoyo image+message node, the title and the details paragraphs.

        """
        _n = YoyoErrorNode(parent_id)
        _n.add_attribute("class", "width_30")

        _title = HTMLNode(parent_id, None, "p", value=MSG_ERROR_DETAILS)
        _title.add_attribute("class", "error-details-title")

        _details = HTMLNode(parent_id, None, "p", value=record.extras["error"].replace("\n", "<br>"))
        _details.add_attribute("class", "error-details-content")

        return [_n, _title, _details]

    # -----------------------------------------------------------------------

    @staticmethod
    def __build_info_dialog_node(parent_id: str, record: TwinCueSRecord) -> HTMLNode:
        """Build the Yoyo-styled info dialog node, not attached to any parent.

        :param parent_id: (str) Identifier to reference as the node's parent.
        :param record: (TwinCueSRecord) The data holding the "info" extra.
        :return: (HTMLNode) The Yoyo image+message node.

        """
        _n = YoyoInfoNode(parent_id, record.extras["info"])
        _n.add_attribute("class", "width_30")
        return _n

