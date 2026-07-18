const wexa_statics_js = window.WEXA_JS_PATH;

const { BaseManager } = await import(`${wexa_statics_js}/transport/base_manager.js`);

/**
 * :filename: sppas.ui.swapp.statics.js.base_cues_manager.js
 * :author: Brigitte Bigi
 * :contact: contact@sppas.org
 * :summary: Shared base class for the "cues" apps managers (TextCueS, TwinCueS, ListCueS)
 *
 *   This file is part of Auto-CS: <https://autocs.sourceforge.io>
 *   -------------------------------------------------------------------------
 *
 *   Copyright (C) 2026  Brigitte Bigi, CNRS
 *   Laboratoire Parole et Langage, Aix-en-Provence, France
 *
 *   This program is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU Affero General Public License as published by
 *   the Free Software Foundation, either version 3 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU Affero General Public License for more details.
 *
 *   You should have received a copy of the GNU Affero General Public License
 *   along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 *   This banner notice must not be removed.
 *
 *   -------------------------------------------------------------------------
 *
 */

'use strict';

/**
 * Common behavior shared by every "cues" app manager.
 *
 * Extracted once a third manager (ListCueS) needed the exact same
 * "busy button" logic, the exact same "menu links + auto-open error/info
 * dialogs" block, and the exact same "handleXxxManagerOnLoad()" bootstrap,
 * already duplicated identically in TextCueSManager and TwinCueSManager.
 *
 * "handleCuesManagerOnLoad()" / "attachCuesListeners()" is a template
 * method: the base class owns the DOM-ready wiring, each subclass overrides
 * "attachCuesListeners()" with its own page-specific listeners.
 *
 * These are plain (not "#" private) members: unlike true private fields,
 * they are inherited and reachable from -- or overridable by -- subclasses
 * ("ListCueSManager.ID_ERROR_DIALOG", "this._attachSharedListeners()").
 *
 */
export default class BaseCuesManager extends BaseManager {

    static ID_MAIN_CONTENT = 'main-content';
    static ID_NAV_CONTENT = 'nav-content';
    static ID_ERROR_DIALOG = 'error_dialog';
    static ID_INFO_DIALOG = 'info_dialog';
    static ID_HOME_MENU_BUTTON = 'link-welcome_button';
    static ID_ACS_MENU_BUTTON = 'link-acs_button';
    static ID_SPPAS_MENU_BUTTON = 'link-sppas_button';

    /**
     * Register event listeners once the DOM content is loaded.
     *
     * Template method: waits for the DOM to be ready, then calls the
     * subclass's own "attachCuesListeners()" override -- identical in every
     * "cues" app manager except for that call, so it belongs here once.
     *
     * @returns {void}
     */
    handleCuesManagerOnLoad() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.attachCuesListeners());
        } else {
            this.attachCuesListeners();
        }
    }

    /**
     * Attach the page-specific event listeners.
     *
     * Abstract: every subclass must override this. Mirrors Python's
     * "raise NotImplementedError" for a method with no default behavior.
     *
     * @returns {void}
     */
    attachCuesListeners() {
        throw new Error('attachCuesListeners() must be overridden by the subclass.');
    }

    /**
     * Wire the shared menu links, and auto-open the error/info dialogs if populated.
     *
     * Every "cues" app page has the same "nav-content" (Home, ACS project,
     * SPPAS website links) and the same "main-content" carrying the error
     * and info dialogs. This is the common part of every subclass's own
     * "attachXxxListeners()", which should return early when this returns
     * null, and continue with its own page-specific listeners otherwise.
     *
     * @returns {HTMLElement|null} The "main-content" container, or null if
     *          absent from the current page (nothing to attach to).
     */
    _attachSharedListeners() {
        const menu = document.getElementById(BaseCuesManager.ID_NAV_CONTENT);
        if (menu === null) {
            return null;
        }
        // Menu links (Home, ACS project, SPPAS website): handled by
        // whakerexa's own LinkController (data-target="_self"/"_blank",
        // preserves accessibility parameters) -- not reimplemented here.
        window.Wexa.links.handleLinksWithParameters([
            BaseCuesManager.ID_HOME_MENU_BUTTON,
            BaseCuesManager.ID_ACS_MENU_BUTTON,
            BaseCuesManager.ID_SPPAS_MENU_BUTTON
        ]);

        const container = document.getElementById(BaseCuesManager.ID_MAIN_CONTENT);
        if (container === null) {
            return null;
        }

        const errorDlg = container.querySelector('#' + BaseCuesManager.ID_ERROR_DIALOG);
        if (errorDlg instanceof HTMLDialogElement && errorDlg.textContent.trim().length > 0) {
            window.Wexa.dialog.open(BaseCuesManager.ID_ERROR_DIALOG, true);
        }

        const infoDlg = container.querySelector('#' + BaseCuesManager.ID_INFO_DIALOG);
        if (infoDlg instanceof HTMLDialogElement && infoDlg.textContent.trim().length > 0) {
            window.Wexa.dialog.open(BaseCuesManager.ID_INFO_DIALOG, true);
        }

        return container;
    }

    /**
     * Toggle a busy/loading state on a button during a slow async action.
     *
     * @param {HTMLButtonElement} button - The button to toggle.
     * @param {boolean} busy - Whether the button must show a busy state.
     * @returns {void}
     */
    _setButtonBusy(button, busy) {
        if (!(button instanceof HTMLButtonElement)) {
            return;
        }
        button.disabled = busy;
        button.setAttribute('aria-busy', busy ? 'true' : 'false');
        button.classList.toggle('is-loading', busy);
    }

}

export { BaseCuesManager };
