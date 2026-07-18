const wexa_statics_js = window.WEXA_JS_PATH;
const wexa_log_level = window.WEXA_LOG_LEVEL;

const { WexaLogger } = await import(`${wexa_statics_js}/logger.js`);
WexaLogger.setLogLevel(wexa_log_level);

const { BaseCuesManager } = await import('./base_cues_manager.js');

/**
 * :filename: sppas.ui.swapp.statics.js.listcues_manager.js
 * :author: Brigitte Bigi
 * :contact: contact@sppas.org
 * :summary: JS for the ListCueS application
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

// --------------------------------------------------------------------------
// Class: ListCueSManager. Controls the `listcues.html` page (welcome and conversion states)
// --------------------------------------------------------------------------

/**
 * This class orchestrates user interactions within the ListCueS pages. It
 * attaches event listeners to the welcome form and to the conversion form
 * (both real, plain page navigations; the server reports errors/info and
 * renders results while baking the resulting page), and activates the key
 * piano. It relies on BaseCuesManager for shared "cues" app behavior, and
 * on WexaLogger for debug output.
 *
 * handleCuesManagerOnLoad() (inherited from BaseCuesManager) has to be
 * invoked **after** the DOM is loaded.
 *
 */
export default class ListCueSManager extends BaseCuesManager {

    // ----------------------------------------------------------------------
    // CONSTANTS (DOM ids/names + reused selectors only)
    // ----------------------------------------------------------------------

    static #ID_WELCOME_FORM = 'listcues_welcome_form';
    static #ID_LISTCUES_FORM = 'listcues_form';

    // ----------------------------------------------------------------------
    // Constructor
    // ----------------------------------------------------------------------

    constructor() {
        super();
    }

    // ----------------------------------------------------------------------
    // Initialization
    // ----------------------------------------------------------------------

    /**
     * Attach listeners to the welcome form and to the conversion form.
     *
     * Overrides BaseCuesManager's abstract "attachCuesListeners()", called
     * by the inherited "handleCuesManagerOnLoad()" once the DOM is ready.
     *
     * @returns {Promise<void>}
     */
    async attachCuesListeners() {

        const container = this._attachSharedListeners();
        if (container === null) {
            return;
        }

        // The welcome page: a plain GET form, only intercepted to preserve
        // accessibility parameters across the navigation (same mechanism as
        // the menu links above).
        const welcomeForm = document.getElementById(ListCueSManager.#ID_WELCOME_FORM);
        if (welcomeForm instanceof HTMLFormElement) {
            welcomeForm.addEventListener('submit', (e) => this.#onWelcomeFormSubmit(e));
            return;
        }

        // The conversion page
        const form = document.getElementById(ListCueSManager.#ID_LISTCUES_FORM);
        if (form instanceof HTMLFormElement) {
            form.addEventListener('submit', (e) => this.#onListCueSFormSubmit(e));
        }

        const pianoContainer = container.querySelector('.wexa-key-piano');
        if (pianoContainer instanceof HTMLElement) {
            // Resolved from window.WEXA_JS_PATH (see wexa_statics_js above),
            // itself server-injected from wapp_settings.wexa_statics: never
            // a path hardcoded relative to this file's own location, which
            // would silently break if Whakerexa's install location changes.
            const { KeyPiano } = await import(`${wexa_statics_js}/extras/keypiano/keypiano.js`);
            new KeyPiano(pianoContainer);
        }
    }

    // ----------------------------------------------------------------------
    // WELCOME FORM
    // ----------------------------------------------------------------------

    /**
     * Handle submit of the welcome form (language choice).
     *
     * The form itself already navigates to "listcues.html?lang=..." as a
     * plain GET: this only adds the accessibility parameters (theme,
     * contrast...) to that navigation, exactly as the menu links do.
     *
     * Building the word index of a language not seen yet can take a long
     * time (whole dictionary). The browser tears down this page only once
     * the new one starts arriving, so the busy button stays visible for
     * the whole wait -- same feedback as the "Validate" button.
     *
     * @param {SubmitEvent} event
     * @returns {void}
     */
    #onWelcomeFormSubmit(event) {
        event.preventDefault();

        const form = event.currentTarget;
        const langSelect = form.querySelector('#lang');
        const action = form.getAttribute('action');
        const url = new URL(action, window.location.href);

        const submitButton = form.querySelector('button[type="submit"]');
        this._setButtonBusy(submitButton, true);

        // Accessibility parameters first, chosen language after:
        // setUrlWithParameters() forwards every parameter of the current URL
        // and overwrites those of the target URL, so a residual "lang" left
        // by a previous navigation would silently cancel the user's choice.
        const finalUrl = new URL(window.Wexa.accessibility.setUrlWithParameters(url.href));
        if (langSelect instanceof HTMLSelectElement) {
            finalUrl.searchParams.set('lang', langSelect.value);
        }

        window.location.href = finalUrl.href;
    }

    // ----------------------------------------------------------------------
    // CONVERSION FORM
    // ----------------------------------------------------------------------

    /**
     * Handle submit of the conversion form (cue textarea).
     *
     * A real form POST, only intercepted to preserve accessibility
     * parameters across the navigation: the server reports any error or
     * info through the (Yoyo) dialogs during the resulting
     * full-page bake. Converting a language not seen yet can take a long
     * time (whole dictionary): the busy button gives feedback for that
     * whole wait, since the browser only tears down this page once the new
     * one starts arriving -- same idiom as the welcome form's own submit.
     *
     * @param {SubmitEvent} event
     * @returns {void}
     */
    #onListCueSFormSubmit(event) {
        const form = event.currentTarget;
        if (!(form instanceof HTMLFormElement)) {
            return;
        }
        form.action = window.Wexa.accessibility.setUrlWithParameters(form.action);

        const submitButton = form.querySelector('button[type="submit"]');
        this._setButtonBusy(submitButton, true);
    }

}

export { ListCueSManager };
