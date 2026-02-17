const wexa_statics_js = window.WEXA_JS_PATH;
const wexa_log_level = window.WEXA_LOG_LEVEL;

const { WexaLogger } = await import(`${wexa_statics_js}/logger.js`);
WexaLogger.setLogLevel(wexa_log_level);

const { BaseManager } = await import(`${wexa_statics_js}/transport/base_manager.js`);

/**
 * :filename: sppas.ui.swapp.statics.js.textcues_manager.js
 * :author: Brigitte Bigi
 * :contact: contact@sppas.org
 * :summary: JS for the TextCueS application
 *
 *   This file is part of AutoCS: <https://autocs.sourceforge.io>
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

// --------------------------------------------------------------------------
// Class: TextCueSManager. Controls the pages `texcues_guid.html`
// --------------------------------------------------------------------------

/**
 * This class orchestrates user interactions within *textcues_guid.html*. It
 * attaches event listeners to the buttons of the main container, sends
 * corresponding asynchronous requests to the server, and updates the DOM in
 * response. It relies on BaseManager for communication logic and form
 * submission, and on WexaLogger for debug output.
 *
 * handleTextCueSManagerOnLoad() has to be invoked **after** the DOM is loaded.
 *
 */
export default class TextCueSManager extends BaseManager {

    // ----------------------------------------------------------------------
    // CONSTANTS (DOM ids/names + reused selectors only)
    // ----------------------------------------------------------------------

    // IDs & NAMES
    static #ID_MAIN_CONTENT = 'main-content';
    static #ID_NAV_CONTENT = 'nav-content';
    static #ID_ERROR_DIALOG = 'error_dialog';
    static #ID_INFO_DIALOG = 'info_dialog';

    static #ID_PATHWAY_FORM = 'pathway_form';
    static #ID_OPTIONS_FORM = 'options_form';

    static #ID_PATHWAY_WELCOME_BUTTON = 'pathway_welcome_button';
    static #ID_PATHWAY_TEXT_ACTION_BTN = 'pathway_text_action_btn';
    static #ID_PATHWAY_SOUND_ACTION_BTN = 'pathway_sound_action_btn';
    static #ID_PATHWAY_CODE_ACTION_BTN = 'pathway_code_action_btn';

    static #ID_TEXTAREA_TEXT = 'text';
    static #ID_SELECT_POSITION_MODEL = 'select_position_model';
    static #ID_SELECT_ANGLE_MODEL = 'select_angle_model';
    static #ID_SELECT_TIMING_MODEL = 'select_timing_model';
    static #NAME_DISPLAYMODE_INPUT = 'displaymode_input';

    static #ID_DISPLAYMODE_SECTION = 'displaymode_section';

    // SELECTORS (reused)
    static #SEL_SOUNDS_TABLE = 'table.sounds-table';

    // INTERNAL PATTERNS
    static #PATTERN_PAGE = 'textcues_';
    static #SOUND_INPUT_SUFFIX = '-sound_input';
    static #SOUND_BUTTON_SUFFIX = '-sound_button';

    // EVENTS
    static #EVENT_NAME_DISPLAYMODE = 'displaymode';

    // MESSAGES
    static #MSG_ENTER_TEXT = "Vous devez saisir ou copier-coller un texte dans le bloc pour pouvoir passer à l'étape suivante.";

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
     * Register event listeners once the DOM content is loaded.
     *
     * This method must be called after the page structure is available.
     * It attaches listeners to all buttons within the main container.
     *
     * @returns {void}
     */
    handleTextCueSManagerOnLoad() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.attachTextCueSListeners());
        } else {
            this.attachTextCueSListeners();
        }
    }

    // ----------------------------------------------------------------------

    /**
     * Attach click listeners to every button in the main container.
     *
     * Also attaches the submit/invalid handlers of the pathway form when present.
     *
     * @returns {void}
     */
    attachTextCueSListeners() {

        // Menu
        const menu = document.getElementById(TextCueSManager.#ID_NAV_CONTENT);
        if (menu === null) {
            return;
        }
        // Redirections in any button
        const redirectButtons = menu.querySelectorAll('button[data-href]');
        for (const redirectButton of redirectButtons) {
            if (!(redirectButton instanceof HTMLButtonElement)) {
                continue;
            }
            redirectButton.addEventListener('click', (event) => this.#onRedirectButtonClick(event));
            redirectButton.addEventListener('keydown', (event) => this.#onRedirectButtonKeydown(event));
        }

        // Main
        const container = document.getElementById(TextCueSManager.#ID_MAIN_CONTENT);
        if (container === null) {
            return;
        }

        const errorDlg = container.querySelector('#' + TextCueSManager.#ID_ERROR_DIALOG);
        if (errorDlg instanceof HTMLDialogElement && errorDlg.textContent.trim().length > 0) {
            window.Wexa.dialog.open(TextCueSManager.#ID_ERROR_DIALOG, true);
        }

        const infoDlg = container.querySelector('#' + TextCueSManager.#ID_INFO_DIALOG);
        if (infoDlg instanceof HTMLDialogElement && infoDlg.textContent.trim().length > 0) {
            window.Wexa.dialog.open(TextCueSManager.#ID_INFO_DIALOG, true);
        }

        // The welcome page
        const startLink = document.getElementById(TextCueSManager.#ID_PATHWAY_WELCOME_BUTTON);
        if (startLink instanceof HTMLAnchorElement) {
            startLink.addEventListener('click', (e) => this.#onPathwayStartLinkClick(e));
            return;
        }

        // Each page has a "pathway_form"; this listener is managing its 'submit' button.
        const form = document.getElementById(TextCueSManager.#ID_PATHWAY_FORM);
        if (form === null) {
            return;
        }

        // Page "Text": textarea + submit button.
        const isTextPage = (form.querySelector('#' + TextCueSManager.#ID_PATHWAY_TEXT_ACTION_BTN) !== null);

        // Page "Sound": pronunciation table + submit button.
        const isSoundPage = (form.querySelector('#' + TextCueSManager.#ID_PATHWAY_SOUND_ACTION_BTN) !== null);

        // Page "Code": submit button alone.
        const isCodePage = (form.querySelector('#' + TextCueSManager.#ID_PATHWAY_CODE_ACTION_BTN) !== null);

        if (isTextPage === true) {
            WexaLogger.debug(`"Text page: ": ${form instanceof HTMLFormElement}`);
            form.addEventListener('submit', (e) => this.#onPathwayTextFormSubmit(e));
            return;
        }

        if (isSoundPage === true) {
            this.#attachSoundFormListeners(form);
            WexaLogger.debug(`"Sound page: ": ${form instanceof HTMLFormElement}`);
            form.addEventListener('submit', (e) => this.#onPathwaySoundFormSubmit(e));
            return;
        }

        if (isCodePage === true) {
            WexaLogger.debug(`"Code page: ": ${form instanceof HTMLFormElement}`);
            form.addEventListener('submit', (e) => this.#onPathwayCodeFormSubmit(e));

            const optionsForm = document.getElementById(TextCueSManager.#ID_OPTIONS_FORM);
            if (optionsForm instanceof HTMLFormElement) {
                this.#attachCodeFormListeners(optionsForm);
                optionsForm.addEventListener('submit', (e) => this.#onPathwayCodeOptionsFormSubmit(e), true);
            } else {
                WexaLogger.error("Form with options not found.");
            }
        }
    }

    // ----------------------------------------------------------------------
    // MENU
    // ----------------------------------------------------------------------

    /**
     * Open data-href in a new tab (Enter/Space support) while preserving
     * accessibility parameters.
     *
     * @param {KeyboardEvent} event
     * @returns {void}
     */
    #onRedirectButtonKeydown(event) {
        if (event.key !== 'Enter' && event.key !== ' ') {
            return;
        }
        event.preventDefault();
        this.#openRedirectFromEventTarget(event);
    }

    // ----------------------------------------------------------------------

    /**
     * Open data-href in a new tab while preserving accessibility parameters.
     *
     * @param {MouseEvent} event
     * @returns {void}
     */
    #onRedirectButtonClick(event) {
        event.preventDefault();
        this.#openRedirectFromEventTarget(event);
    }

    // ----------------------------------------------------------------------

    /**
     * Extract data-href from the event target and open it in a new tab.
     *
     * @param {Event} event
     * @returns {void}
     */
    #openRedirectFromEventTarget(event) {
        const button = event.currentTarget;
        if (!(button instanceof HTMLButtonElement)) {
            return;
        }

        const href = button.getAttribute('data-href');
        if (typeof href !== 'string' || href.trim().length === 0) {
            return;
        }

        const absolute = new URL(href, window.location.href).href;
        const target = window.Wexa.accessibility.setUrlWithParameters(absolute);
        window.open(target, '_blank', 'noopener');
    }


    // ----------------------------------------------------------------------
    // PATHWAY: Welcome
    // ----------------------------------------------------------------------

    /**
     * Handle click on the welcome "start" link.
     *
     * This handler generates a random TextCueS page, preserves accessibility
     * parameters (theme/contrast/etc.), then redirects in the current tab.
     * It also stops other link listeners (Whakerexa accessibility link handler)
     * to avoid being redirected back to the current page.
     *
     * @param {MouseEvent} event
     * @returns {void}
     */
    #onPathwayStartLinkClick(event) {
        event.stopImmediatePropagation();

        const relative = event.currentTarget.getAttribute('href');
        const absolute = new URL(relative, window.location.href).href;

        const target = window.Wexa.accessibility.setUrlWithParameters(absolute);
        window.location.href = target;
    }

    // ----------------------------------------------------------------------
    // PATHWAY: Text
    // ----------------------------------------------------------------------

    /**
     * Handle pathway form submit (mouse + keyboard).
     *
     * Blocks navigation when invalid and shows the existing error dialog.
     * When valid, sets a random target page and preserves accessibility parameters.
     *
     * @param {SubmitEvent} event - The submit event.
     * @returns {void}
     */
    #onPathwayTextFormSubmit(event) {
        if (event === null || typeof event === 'undefined') {
            return;
        }

        const form = event.currentTarget;
        if (!(form instanceof HTMLFormElement)) {
            return;
        }

        const textArea = form.querySelector('#' + TextCueSManager.#ID_TEXTAREA_TEXT);
        if (textArea instanceof HTMLTextAreaElement) {
            const trimmedValue = textArea.value.trim();
            if (trimmedValue.length === 0) {
                event.preventDefault();
                this._showDialog(TextCueSManager.#ID_ERROR_DIALOG, TextCueSManager.#MSG_ENTER_TEXT);
                textArea.focus();
                return;
            }
        }

        //
        form.action = window.Wexa.accessibility.setUrlWithParameters(form.action);
    }

    // ----------------------------------------------------------------------
    // PATHWAY: Sound
    // ----------------------------------------------------------------------

    /**
     * Attach listeners to the pronunciation table of pathway_sound.
     *
     * It creates listeners to implement a toggle group per row.
     *
     * @param {HTMLFormElement} form
     * @returns {void}
     */
    #attachSoundFormListeners(form) {
        const soundsTable = form.querySelector(TextCueSManager.#SEL_SOUNDS_TABLE);
        if (soundsTable === null) {
            return;
        }

        const buttonSuffix = TextCueSManager.#SOUND_BUTTON_SUFFIX;
        const inputSuffix = TextCueSManager.#SOUND_INPUT_SUFFIX;

        const choiceButtons = soundsTable.querySelectorAll(`button[name$="${buttonSuffix}"]`);
        for (const choiceButton of choiceButtons) {
            choiceButton.type = 'button';
            choiceButton.disabled = false;

            if (choiceButton.getAttribute("aria-pressed") === "true") {
                choiceButton.setAttribute("aria-pressed", "true");
            } else {
                choiceButton.setAttribute("aria-pressed", "false");
            }
        }

        const customInputs = soundsTable.querySelectorAll(`input[name$="${inputSuffix}"]`);
        for (const customInput of customInputs) {
            customInput.removeAttribute('onchange');
        }

        soundsTable.addEventListener('click', (event) => this.#onPronunciationTableClick(event));
        soundsTable.addEventListener('input', (event) => this.#onPronunciationTableInput(event));
    }

    // ----------------------------------------------------------------------

    /**
     * Handle click inside the pronunciation table.
     *
     * @param {MouseEvent} event
     * @returns {void}
     */
    #onPronunciationTableClick(event) {
        const target = event.target;
        if (!(target instanceof HTMLButtonElement)) {
            return;
        }

        const buttonName = target.name;
        if (typeof buttonName !== 'string' || buttonName.endsWith(TextCueSManager.#SOUND_BUTTON_SUFFIX) === false) {
            return;
        }

        event.preventDefault();
        event.stopPropagation();

        this.#selectPronunciationChoiceButton(target);
    }

    // ----------------------------------------------------------------------

    /**
     * Handle edits in the custom pronunciation input fields.
     *
     * Rules:
     * - When custom input is non-empty: no button selected in the row group.
     * - When custom input becomes empty: select choice #1 of the row group.
     *
     * @param {Event} event
     * @returns {void}
     */
    #onPronunciationTableInput(event) {
        const target = event.target;
        if (!(target instanceof HTMLInputElement)) {
            return;
        }

        const inputName = target.name;
        if (typeof inputName !== 'string' || inputName.endsWith(TextCueSManager.#SOUND_INPUT_SUFFIX) === false) {
            return;
        }

        const tokenKey = this.#tokenKeyFromInputName(inputName);
        const groupName = tokenKey + TextCueSManager.#SOUND_BUTTON_SUFFIX;

        const trimmedValue = target.value.trim();
        if (trimmedValue.length > 0) {
            this.#clearPronunciationButtonGroup(groupName);
            return;
        }

        this.#selectFirstButtonInGroup(groupName);
    }

    // ----------------------------------------------------------------------

    /**
     * Select a pronunciation choice button and clear the custom input of the row.
     *
     * @param {HTMLButtonElement} chosenButton
     * @returns {void}
     */
    #selectPronunciationChoiceButton(chosenButton) {
        if (chosenButton.classList.contains("aria-pressed") === true) {
            return;
        }

        const groupName = chosenButton.name;

        this.#clearPronunciationButtonGroup(groupName);

        chosenButton.setAttribute("aria-pressed", "true");
        if (document.activeElement instanceof HTMLButtonElement) {
            chosenButton.focus();
        }

        const tokenKey = this.#tokenKeyFromButtonName(groupName);
        const customInput = document.getElementById(tokenKey + TextCueSManager.#SOUND_INPUT_SUFFIX);
        if (customInput instanceof HTMLInputElement) {
            WexaLogger.error(`No -sound_input found for tokenKey=${tokenKey}`);
            customInput.value = '';
        } else {
            WexaLogger.debug(`Found -sound_input for tokenKey=${tokenKey}`);
        }
    }

    // ----------------------------------------------------------------------

    /**
     * Clear selection for all buttons of one row group.
     *
     * @param {string} groupName
     * @returns {void}
     */
    #clearPronunciationButtonGroup(groupName) {
        const groupButtons = document.getElementsByName(groupName);
        for (const groupButton of groupButtons) {
            if (groupButton instanceof HTMLButtonElement) {
                groupButton.disabled = false;
                groupButton.setAttribute("aria-pressed", "false");
            }
        }
    }

    // ----------------------------------------------------------------------

    /**
     * Select choice #1 of the group.
     *
     * @param {string} groupName
     * @returns {void}
     */
    #selectFirstButtonInGroup(groupName) {
        const firstButton = this.#getFirstButtonInGroup(groupName);
        if (firstButton === null) {
            return;
        }

        this.#selectPronunciationChoiceButton(firstButton);
    }

    // ----------------------------------------------------------------------

    /**
     * Extract the token key from a button group name.
     *
     * Expected format: "<index>_button".
     *
     * @param {string} groupName
     * @returns {string}
     */
    #tokenKeyFromButtonName(groupName) {
        return groupName.slice(0, groupName.length - TextCueSManager.#SOUND_BUTTON_SUFFIX.length);
    }

    // ----------------------------------------------------------------------

    /**
     * Extract the token key from a custom input name.
     *
     * Expected format: "<token>-<index>_SOUND_INPUT_SUFFIX".
     *
     * @param {string} inputName
     * @returns {string}
     */
    #tokenKeyFromInputName(inputName) {
        return inputName.slice(0, inputName.length - TextCueSManager.#SOUND_INPUT_SUFFIX.length);
    }

    // ----------------------------------------------------------------------

    /**
     * Fill empty custom phon inputs from the selected buttons.
     *
     * If the custom input is empty and no button is selected, choice #1 is selected.
     *
     * @param {HTMLFormElement} form
     * @returns {void}
     */
    #applyPronunciationChoicesToInputs(form) {
        const soundsTable = form.querySelector(TextCueSManager.#SEL_SOUNDS_TABLE);
        if (soundsTable === null) {
            return;
        }

        const phonInputs = soundsTable.querySelectorAll('input.pron');
        for (const phonInput of phonInputs) {
            if (!(phonInput instanceof HTMLInputElement)) {
                continue;
            }

            const trimmedValue = phonInput.value.trim();
            if (trimmedValue.length > 0) {
                continue;
            }

            const tokenKey = this.#tokenKeyFromInputName(phonInput.name);
            const groupName = tokenKey + TextCueSManager.#SOUND_BUTTON_SUFFIX;

            let chosenButton = this.#findChosenButtonInGroup(groupName);
            if (chosenButton === null) {
                chosenButton = this.#getFirstButtonInGroup(groupName);
                if (chosenButton !== null) {
                    this.#selectPronunciationChoiceButton(chosenButton);
                }
            }

            if (chosenButton !== null) {
                const chosenText = chosenButton.textContent;
                if (typeof chosenText === 'string') {
                    phonInput.value = chosenText.trim();
                }
            }
        }
    }

    // ----------------------------------------------------------------------

    /**
     * Find the chosen button of a group.
     *
     * @param {string} groupName
     * @returns {HTMLButtonElement|null}
     */
    #findChosenButtonInGroup(groupName) {
        const groupButtons = document.getElementsByName(groupName);
        for (const groupButton of groupButtons) {
            if (groupButton instanceof HTMLButtonElement) {
                if (groupButton.getAttribute("aria-pressed") === "true") {
                    return groupButton;
                }
            }
        }
        return null;
    }

    // ----------------------------------------------------------------------

    /**
     * Get the first button of a group (choice #1).
     *
     * @param {string} groupName
     * @returns {HTMLButtonElement|null}
     */
    #getFirstButtonInGroup(groupName) {
        const groupButtons = document.getElementsByName(groupName);
        for (const groupButton of groupButtons) {
            if (groupButton instanceof HTMLButtonElement) {
                return groupButton;
            }
        }
        return null;
    }

    // ----------------------------------------------------------------------

    /**
     * Handle submit of the pathway_sound form.
     *
     * WARNING: The prefix of each pronunciation input name and its button group name MUST match.
     * Required naming:
     * - input:  "<key>-sound_input"
     * - button: "<key>-sound_button"
     * The same <key> is used to map one input row to its corresponding button group.
     *
     * For each "*-sound_input" field:
     * - Keep the user-typed value when non-empty (trimmed).
     * - Otherwise copy the selected button value ("aria-pressed"="true") of the same <key>.
     * - If no button is selected, select the first button for this <key> and copy its value.
     *
     * @param {SubmitEvent} event
     * @returns {void}
     */
    #onPathwaySoundFormSubmit(event) {
        const form = event.currentTarget;
        if (!(form instanceof HTMLFormElement)) {
            return;
        }

        const inputs = form.querySelectorAll(`input[name$="${TextCueSManager.#SOUND_INPUT_SUFFIX}"]`);
        for (const input of inputs) {
            if (!(input instanceof HTMLInputElement)) {
                continue;
            }

            const typed = input.value.trim();
            if (typed.length > 0) {
                input.value = typed;
                continue;
            }

            const tokenKey = input.name.slice(0, -TextCueSManager.#SOUND_INPUT_SUFFIX.length);
            const groupName = tokenKey + TextCueSManager.#SOUND_BUTTON_SUFFIX;
            const buttons = form.querySelectorAll(`button[name="${groupName}"]`);

            let chosen = null;
            for (const btn of buttons) {
                if (btn instanceof HTMLButtonElement && btn.getAttribute("aria-pressed") === "true") {
                    chosen = btn;
                    break;
                }
            }

            if (chosen === null) {
                for (const btn of buttons) {
                    if (btn instanceof HTMLButtonElement) {
                        chosen = btn;
                        break;
                    }
                }
                if (chosen !== null) {
                    this.#selectPronunciationChoiceButton(chosen);
                }
            }

            if (chosen instanceof HTMLButtonElement) {
                input.value = chosen.innerText.trim();
            }
        }

        //
        form.action = window.Wexa.accessibility.setUrlWithParameters(form.action);
    }

    // ----------------------------------------------------------------------
    // PATHWAY: Code
    // ----------------------------------------------------------------------

    /**
     * Handle "code" form submit.
     *
     * @param {SubmitEvent} event
     * @returns {void}
     */
    #onPathwayCodeFormSubmit(event) {
        const form = event.currentTarget;
        if (!(form instanceof HTMLFormElement)) {
            return;
        }

        //
        form.action = window.Wexa.accessibility.setUrlWithParameters(form.action);
    }

    // ----------------------------------------------------------------------
    // CODE: Options form (display mode)
    // ----------------------------------------------------------------------

    /**
     * Attach listeners to the inputs of options_form (pathway_code).
     *
     * The selects are enabled/disabled according to the selected display mode:
     * - Mode 0: Disable position, angle and timing.
     * - Mode 1: Enable position and angle; disable timing.
     * - Mode 2: Enable position, angle and timing.
     *
     * @param {HTMLFormElement} form
     * @returns {void}
     */
    #attachCodeFormListeners(form) {
        if (!(form instanceof HTMLFormElement)) {
            return;
        }

        const onModeChanged = () => {
            const mode = this.#getSelectedDisplayMode(form);
            if (mode !== null) {
                this.#applyDisplayModeToSelects(form, mode);
            }
        };

        const radios = form.querySelectorAll(`input[name="${TextCueSManager.#NAME_DISPLAYMODE_INPUT}"][type="radio"]`);
        for (const radio of radios) {
            if (radio instanceof HTMLInputElement) {
                radio.addEventListener('change', onModeChanged);
            }
        }

        onModeChanged();
    }

    // ----------------------------------------------------------------------

    /**
     * Return the current display mode selected in options_form.
     *
     * @param {HTMLFormElement} form
     * @returns {number|null} 0, 1, 2 or null if missing.
     */
    #getSelectedDisplayMode(form) {
        const checked = form.querySelector(`input[name="${TextCueSManager.#NAME_DISPLAYMODE_INPUT}"][type="radio"]:checked`);
        if (!(checked instanceof HTMLInputElement)) {
            return null;
        }
        return parseInt(checked.value, 10);
    }

    // ----------------------------------------------------------------------

    /**
     * Return the 3 model selects of the code options form.
     *
     * It validates the presence and types of the selects. If one is missing or not a select, null is returned.
     *
     * @param {HTMLFormElement} form
     * @returns {{positionSelect: HTMLSelectElement, angleSelect: HTMLSelectElement, timingSelect: HTMLSelectElement}|null}
     */
    #getModelSelects(form) {
        const positionSelect = form.querySelector('#' + TextCueSManager.#ID_SELECT_POSITION_MODEL);
        const angleSelect = form.querySelector('#' + TextCueSManager.#ID_SELECT_ANGLE_MODEL);
        const timingSelect = form.querySelector('#' + TextCueSManager.#ID_SELECT_TIMING_MODEL);

        if (!(positionSelect instanceof HTMLSelectElement)) {
            return null;
        }
        if (!(angleSelect instanceof HTMLSelectElement)) {
            return null;
        }
        if (!(timingSelect instanceof HTMLSelectElement)) {
            return null;
        }

        return {
            positionSelect: positionSelect,
            angleSelect: angleSelect,
            timingSelect: timingSelect
        };
    }

    // ----------------------------------------------------------------------

    /**
     * Enable/disable selects according to display mode.
     *
     * @param {HTMLFormElement} form
     * @param {number} mode 0, 1 or 2.
     * @returns {void}
     */
    #applyDisplayModeToSelects(form, mode) {
        const selects = this.#getModelSelects(form);
        if (selects === null) {
            return;
        }
        const positionSelect = selects.positionSelect;
        const angleSelect = selects.angleSelect;
        const timingSelect = selects.timingSelect;

        // UI constraints derived from display mode.
        if (mode === 0) {
            positionSelect.disabled = true;
            angleSelect.disabled = true;
            timingSelect.disabled = true;
        } else if (mode === 1) {
            positionSelect.disabled = false;
            angleSelect.disabled = false;
            timingSelect.disabled = true;
        } else if (mode === 2) {
            positionSelect.disabled = false;
            angleSelect.disabled = false;
            timingSelect.disabled = false;
        }
    }

    // ----------------------------------------------------------------------

    /**
     * Handle submit of options_form (code page options).
     *
     * - Read hidden form data (context + previous step results).
     * - Read current user-selected options (display mode + models).
     * - Stop if no option changed (avoid server call and avoid page refresh).
     * - Otherwise send event to server and update the code section if content is not empty.
     *
     * @param {SubmitEvent} event
     * @returns {Promise<void>}
     */
    async #onPathwayCodeOptionsFormSubmit(event) {
        const form = event.currentTarget;
        if (!(form instanceof HTMLFormElement)) {
            return;
        }

        // Cancel the regular "Submit" action of the browser
        event.preventDefault();

        // Read hidden form data (context + previous step results).
        const data = {};
        for (const input of form.querySelectorAll('input[type="hidden"][name]')) {
            if (input instanceof HTMLInputElement) {
                data[input.name] = input.value;
            }
        }

        // Keep previous option values coming from hidden inputs (server state).
        const previous = {
            mode: data['mode'],
            model_pos: data['model_pos'],
            model_angle: data['model_angle'],
            model_timing: data['model_timing']
        };

        // Read current user-selected options (display mode + models).
        const checkedMode = form.querySelector(`input[name="${TextCueSManager.#NAME_DISPLAYMODE_INPUT}"][type="radio"]:checked`);
        if (!(checkedMode instanceof HTMLInputElement)) {
            return;
        }
        const selects = this.#getModelSelects(form);
        if (selects === null) {
            return;
        }
        const positionSelect = selects.positionSelect;
        const angleSelect = selects.angleSelect;
        const timingSelect = selects.timingSelect;

        data['mode'] = String(parseInt(checkedMode.value, 10));
        data['model_pos'] = String(parseInt(positionSelect.value, 10));
        data['model_angle'] = String(parseInt(angleSelect.value, 10));
        data['model_timing'] = String(parseInt(timingSelect.value, 10));

        // If nothing changed: stop here (no request, no DOM update).
        if (
            data['mode'] === previous['mode']
            && (previous['model_pos'] === undefined || data['model_pos'] === previous['model_pos'])
            && (previous['model_angle'] === undefined || data['model_angle'] === previous['model_angle'])
            && (previous['model_timing'] === undefined || data['model_timing'] === previous['model_timing'])
        ) {
            return;
        }

        // Post the data to the server and wait for its answer
        const events = {
            event_name: TextCueSManager.#EVENT_NAME_DISPLAYMODE,
            event_value: data
        };
        const response = await this.postEvents(events);

        // Update only if server returned a non-empty content.
        if (this._requestManager.status === 200) {

            if (response && response.error) {
                this._showDialog(TextCueSManager.#ID_ERROR_DIALOG, response.error)
            }
            if (response && response.info) {
                this._showDialog(TextCueSManager.#ID_INFO_DIALOG, response.info)
            }

            if (response && typeof response.content === 'string' && response.content.trim().length > 0) {
                const displaymodeSection = document.getElementById(TextCueSManager.#ID_DISPLAYMODE_SECTION);
                if (displaymodeSection instanceof HTMLElement) {
                    // Replace the whole section node, i.e. including the <section...>
                    displaymodeSection.outerHTML = response.content;
                }
            }

        }

    }

}

export { TextCueSManager };
