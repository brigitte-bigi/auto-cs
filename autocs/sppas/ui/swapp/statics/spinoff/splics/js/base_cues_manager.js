const wexa_statics_js = window.WEXA_JS_PATH;

const { BaseManager } = await import(`${wexa_statics_js}/transport/base_manager.js`);
const { DialogManager } = await import(`${wexa_statics_js}/dialog.js`);

/**
 * The dialogs of the cues apps, opened and closed through this one manager.
 *
 * Taken from its own module, as the Dashboard takes it, and not from the
 * namespace the loader builds: a page opening a dialog as soon as its DOM is
 * there would be asking for that namespace before it exists.
 *
 * @type {DialogManager}
 */
export const cuesDialogs = new DialogManager();

/**
 * :filename: sppas.ui.swapp.statics.spinoff.splics.js.base_cues_manager.js
 * :author: Brigitte Bigi
 * :contact: contact@sppas.org
 * :summary: Shared base class for the "cues" apps managers (TextCueS, TwinCueS, ListCueS)
 *
 *   This file is part of Auto-CS: <https://autocs.sourceforge.io>
 *   -------------------------------------------------------------------------
 *
 *   Copyright (C) 2021-2026  Brigitte Bigi, CNRS
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
    static ID_APP_MENU_BUTTON = 'link-app_button';
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
        // Menu links (App, Home, ACS project, SPPAS website): bound with plain
        // listeners, as the Dashboard binds its own. The framework is reached
        // from inside the handler only, once the loader has built it: asking
        // for it here would be asking before it exists.
        const linkIds = [
            BaseCuesManager.ID_APP_MENU_BUTTON,
            BaseCuesManager.ID_HOME_MENU_BUTTON,
            BaseCuesManager.ID_ACS_MENU_BUTTON,
            BaseCuesManager.ID_SPPAS_MENU_BUTTON
        ];
        for (const linkId of linkIds) {
            const link = document.getElementById(linkId);
            if (link === null) {
                continue;
            }
            link.addEventListener('click', (event) => this._onMenuLinkActivated(event));
            link.addEventListener('keydown', (event) => {
                if (event.key === 'Enter' || event.key === ' ') {
                    this._onMenuLinkActivated(event);
                }
            });
        }

        const container = document.getElementById(BaseCuesManager.ID_MAIN_CONTENT);
        if (container === null) {
            return null;
        }

        const errorDlg = container.querySelector('#' + BaseCuesManager.ID_ERROR_DIALOG);
        if (errorDlg instanceof HTMLDialogElement && errorDlg.textContent.trim().length > 0) {
            cuesDialogs.open(BaseCuesManager.ID_ERROR_DIALOG, true);
        }

        const infoDlg = container.querySelector('#' + BaseCuesManager.ID_INFO_DIALOG);
        if (infoDlg instanceof HTMLDialogElement && infoDlg.textContent.trim().length > 0) {
            cuesDialogs.open(BaseCuesManager.ID_INFO_DIALOG, true);
        }

        return container;
    }

    /**
     * Open the address a menu link carries, keeping the accessibility
     * parameters of the current page.
     *
     * "data-target" says where: "_self" replaces the page, any other name
     * opens or reuses the tab of that name, and nothing at all opens a new
     * one -- the same reading as the LinkController of Whakerexa.
     *
     * @param {Event} event - The click or key event on the link.
     * @returns {void}
     */
    _onMenuLinkActivated(event) {
        event.preventDefault();

        const link = event.currentTarget;
        const href = link.getAttribute('data-href');
        if (typeof href !== 'string' || href.trim().length === 0) {
            return;
        }

        const absolute = new URL(href, window.location.href).href;
        const finalUrl = window.Wexa.accessibility.setUrlWithParameters(absolute);
        const where = link.getAttribute('data-target');

        if (where === '_self') {
            window.location.href = finalUrl;
        } else {
            window.open(finalUrl, where === null ? '_blank' : where);
        }
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
