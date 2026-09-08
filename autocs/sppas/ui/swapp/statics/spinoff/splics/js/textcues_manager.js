const wexa_statics_js = window.WEXA_JS_PATH;
const wexa_log_level = window.WEXA_LOG_LEVEL;

const { WexaLogger } = await import(`${wexa_statics_js}/logger.js`);
WexaLogger.setLogLevel(wexa_log_level);

const { BaseCuesManager, cuesDialogs } = await import('./base_cues_manager.js');

/**
 * :filename: sppas.ui.swapp.statics.spinoff.splics.js.textcues_manager.js
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
 * response. It relies on BaseCuesManager for communication logic, form
 * submission, and shared "cues" app behavior, and on WexaLogger for debug
 * output.
 *
 * handleCuesManagerOnLoad() (inherited from BaseCuesManager) has to be
 * invoked **after** the DOM is loaded.
 *
 */
export default class TextCueSManager extends BaseCuesManager {

    // ----------------------------------------------------------------------
    // CONSTANTS (DOM ids/names + reused selectors only)
    // ----------------------------------------------------------------------

    // IDs & NAMES
    static #ID_PATHWAY_FORM = 'pathway_form';
    static #ID_OPTIONS_FORM = 'options_form';

    static #ID_WELCOME_FORM = 'pathway_welcome_form';
    static #ID_PATHWAY_TEXT_ACTION_BTN = 'pathway_text_action_btn';
    static #ID_PATHWAY_SOUND_ACTION_BTN = 'pathway_sound_action_btn';
    static #ID_PATHWAY_CODE_ACTION_BTN = 'pathway_code_action_btn';

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

    // Sound page: personalized-entry phoneme piano, shared by every row.
    // The toggle repeats once per row (a class, queried via closest() for
    // event delegation); validate/cancel are single, unique controls of the
    // one shared dialog, found by id, not by a styling class.
    static #ID_SOUND_PIANO_DIALOG = 'sound-piano-dialog';
    static #ID_SOUND_PIANO_TOKEN = 'sound-piano-dialog-token';
    static #ID_SOUND_PIANO_STAGING = 'sound-piano-staging';
    static #SEL_SOUND_PIANO_TOGGLE = '.sound-piano-toggle';
    static #ID_SOUND_PIANO_VALIDATE = 'sound-piano-validate';
    static #ID_SOUND_PIANO_CANCEL = 'sound-piano-cancel';

    // Piano instance, constructed once, eagerly, when the Sound page loads
    // (not lazily on first use): the dialog must never be shown before its
    // icons have finished loading.
    #soundPiano = null;
    // The toggle button that opened the dialog, to restore focus on close.
    #soundPianoOpener = null;
    // Id of the row's real field "Apply" must write the staging value into.
    #soundPianoRealTargetId = null;

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
     * Attach click listeners to every button in the main container.
     *
     * Also attaches the submit/invalid handlers of the pathway form when
     * present. Overrides BaseCuesManager's abstract "attachCuesListeners()",
     * called by the inherited "handleCuesManagerOnLoad()" once the DOM is ready.
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
        const welcomeForm = document.getElementById(TextCueSManager.#ID_WELCOME_FORM);
        if (welcomeForm instanceof HTMLFormElement) {
            welcomeForm.addEventListener('submit', (e) => this.#onWelcomeFormSubmit(e));
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
            await this.#attachSoundFormListeners(form);
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
    // PATHWAY: Welcome
    // ----------------------------------------------------------------------

    /**
     * Handle submit of the welcome form (language choice).
     *
     * The form itself already navigates to a random "textcues_<hex>.html"
     * page with "?lang=..." (a plain GET, see HTMLTag.page_random()): this
     * only adds the accessibility parameters (theme, contrast...) to that
     * navigation, exactly as the menu links do.
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

        // An empty submission is not blocked here: the server reports it
        // through the (translated, Yoyo) info dialog, exactly like any
        // other pathway step.
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
     * @returns {Promise<void>}
     */
    async #attachSoundFormListeners(form) {
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

        await this.#setupSoundPianoDialog();
    }

    // ----------------------------------------------------------------------

    /**
     * Construct the shared phoneme piano and wire the dialog's own controls.
     *
     * The piano is built once here, eagerly, while the dialog is still
     * hidden: its icons (fetched asynchronously) have every chance to be
     * ready well before the user ever opens the dialog, unlike a
     * construct-on-first-click approach that would race the reveal.
     *
     * @returns {Promise<void>}
     */
    async #setupSoundPianoDialog() {
        const dialog = document.getElementById(TextCueSManager.#ID_SOUND_PIANO_DIALOG);
        if (!(dialog instanceof HTMLDialogElement)) {
            return;
        }

        const pianoContainer = dialog.querySelector('.wexa-key-piano');
        if (pianoContainer instanceof HTMLElement) {
            // Resolved from window.WEXA_JS_PATH (see wexa_statics_js at the
            // top of this file), itself server-injected from
            // wapp_settings.wexa_statics: never a path hardcoded relative to
            // this file's own location, which would silently break if
            // Whakerexa's install location changes.
            const { KeyPiano } = await import(`${wexa_statics_js}/extras/keypiano/keypiano.js`);
            this.#soundPiano = new KeyPiano(pianoContainer);
        }

        const validateButton = document.getElementById(TextCueSManager.#ID_SOUND_PIANO_VALIDATE);
        if (validateButton instanceof HTMLButtonElement) {
            validateButton.addEventListener('click', () => this.#onSoundPianoValidate(dialog));
        }

        const cancelButton = document.getElementById(TextCueSManager.#ID_SOUND_PIANO_CANCEL);
        if (cancelButton instanceof HTMLButtonElement) {
            cancelButton.addEventListener('click', () => cuesDialogs.close(dialog.id));
        }

        // Restores focus on the button that opened the dialog: neither the
        // native <dialog> close (Escape) nor DialogManager's injected close
        // button do this on their own, and a screen reader user closing the
        // dialog must land back where they were, not at the top of the page.
        dialog.addEventListener('close', () => {
            if (this.#soundPianoOpener instanceof HTMLElement) {
                this.#soundPianoOpener.focus();
            }
        });
    }

    // ----------------------------------------------------------------------

    /**
     * Handle click inside the pronunciation table.
     *
     * @param {MouseEvent} event
     * @returns {void}
     */
    #onPronunciationTableClick(event) {
        // event.target is whatever element was actually under the pointer:
        // for the icon-only piano toggle, that can be its inline <svg> or
        // one of its <circle> children, neither an HTMLButtonElement --
        // closest("button") walks back up to the real button regardless of
        // which of its descendants was hit.
        const target = event.target.closest('button');
        if (!(target instanceof HTMLButtonElement)) {
            return;
        }

        if (target.matches(TextCueSManager.#SEL_SOUND_PIANO_TOGGLE) === true) {
            event.preventDefault();
            event.stopPropagation();
            this.#openSoundPiano(target);
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
     * Open the shared phoneme-piano dialog for the clicked row.
     *
     * The staging field is preloaded with the row's current value (so
     * re-opening resumes an earlier entry rather than always starting
     * blank), and the piano's own undo history is reset (KeyPiano.setTarget()
     * on its own, unchanged, target field) so a partial entry from a
     * previous row never leaks into this one.
     *
     * @param {HTMLButtonElement} toggle - The row's "Phoneme keyboard" button.
     * @returns {void}
     */
    #openSoundPiano(toggle) {
        const dialog = document.getElementById(TextCueSManager.#ID_SOUND_PIANO_DIALOG);
        if (!(dialog instanceof HTMLDialogElement)) {
            WexaLogger.error('TextCueSManager: sound piano dialog not found.');
            return;
        }

        this.#soundPianoOpener = toggle;
        this.#soundPianoRealTargetId = toggle.dataset.targetInput;

        const tokenElt = document.getElementById(TextCueSManager.#ID_SOUND_PIANO_TOKEN);
        if (tokenElt instanceof HTMLElement) {
            tokenElt.textContent = toggle.dataset.token ?? '';
        }

        const realField = document.getElementById(this.#soundPianoRealTargetId);
        const stagingField = document.getElementById(TextCueSManager.#ID_SOUND_PIANO_STAGING);
        if (realField instanceof HTMLInputElement && stagingField instanceof HTMLInputElement) {
            stagingField.value = realField.value;
        }

        if (this.#soundPiano !== null) {
            this.#soundPiano.setTarget(TextCueSManager.#ID_SOUND_PIANO_STAGING);
        }

        cuesDialogs.open(dialog.id, true);
    }

    // ----------------------------------------------------------------------

    /**
     * Apply the staging field's value to the row that opened the dialog, and close it.
     *
     * A real "input" event is dispatched on the row's field, exactly as a
     * keystroke would: the pronunciation table's own "input" listener
     * (#onPronunciationTableInput) reacts to it the same way either way
     * (e.g. deselecting the row's choice buttons).
     *
     * @param {HTMLDialogElement} dialog
     * @returns {void}
     */
    #onSoundPianoValidate(dialog) {
        const stagingField = document.getElementById(TextCueSManager.#ID_SOUND_PIANO_STAGING);
        const realField = document.getElementById(this.#soundPianoRealTargetId);

        if (stagingField instanceof HTMLInputElement && realField instanceof HTMLInputElement) {
            realField.value = stagingField.value;
            realField.dispatchEvent(new Event('input', {bubbles: true}));
        }

        cuesDialogs.close(dialog.id);
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
     * Each field is independently null when the corresponding <select> is
     * absent or not a select (e.g. a simplified interface without model
     * choices): unlike an all-or-nothing null, callers can still act on
     * whichever selects are actually present.
     *
     * @param {HTMLFormElement} form
     * @returns {{positionSelect: HTMLSelectElement|null, angleSelect: HTMLSelectElement|null, timingSelect: HTMLSelectElement|null}}
     */
    #getModelSelects(form) {
        const positionSelect = form.querySelector('#' + TextCueSManager.#ID_SELECT_POSITION_MODEL);
        const angleSelect = form.querySelector('#' + TextCueSManager.#ID_SELECT_ANGLE_MODEL);
        const timingSelect = form.querySelector('#' + TextCueSManager.#ID_SELECT_TIMING_MODEL);

        return {
            positionSelect: positionSelect instanceof HTMLSelectElement ? positionSelect : null,
            angleSelect: angleSelect instanceof HTMLSelectElement ? angleSelect : null,
            timingSelect: timingSelect instanceof HTMLSelectElement ? timingSelect : null
        };
    }

    // ----------------------------------------------------------------------

    /**
     * Enable/disable selects according to display mode.
     *
     * Silently skips any select that is not present in the form.
     *
     * @param {HTMLFormElement} form
     * @param {number} mode 0, 1 or 2.
     * @returns {void}
     */
    #applyDisplayModeToSelects(form, mode) {
        const { positionSelect, angleSelect, timingSelect } = this.#getModelSelects(form);

        // UI constraints derived from display mode.
        const positionDisabled = mode === 0;
        const angleDisabled = mode === 0;
        const timingDisabled = mode === 0 || mode === 1;

        if (positionSelect !== null) {
            positionSelect.disabled = positionDisabled;
        }
        if (angleSelect !== null) {
            angleSelect.disabled = angleDisabled;
        }
        if (timingSelect !== null) {
            timingSelect.disabled = timingDisabled;
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
        // -1 signals "no selection": the corresponding <select> is absent
        // from the form (e.g. a simplified interface). It is not this
        // interface's role to invent a default: the server decides the
        // default of each model on its own.
        const { positionSelect, angleSelect, timingSelect } = this.#getModelSelects(form);

        data['mode'] = String(parseInt(checkedMode.value, 10));
        data['model_pos'] = positionSelect !== null ? String(parseInt(positionSelect.value, 10)) : '-1';
        data['model_angle'] = angleSelect !== null ? String(parseInt(angleSelect.value, 10)) : '-1';
        data['model_timing'] = timingSelect !== null ? String(parseInt(timingSelect.value, 10)) : '-1';

        // Keep the "Start Over" form (pathway_form) hidden inputs in sync:
        // this AJAX call only refreshes displaymode_section, so without this,
        // "Start Over" would keep submitting the mode/model values from the
        // page's initial load instead of the ones just applied here.
        const pathwayForm = document.getElementById(TextCueSManager.#ID_PATHWAY_FORM);
        if (pathwayForm instanceof HTMLFormElement) {
            for (const name of ['mode', 'model_pos', 'model_angle', 'model_timing']) {
                const hiddenInput = pathwayForm.querySelector(`input[type="hidden"][name="${name}"]`);
                if (hiddenInput instanceof HTMLInputElement) {
                    hiddenInput.value = data[name];
                }
            }
        }

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

        // Video generation can take a long time. Give feedback and prevent
        // re-submit while the request is in flight.
        const submitButton = form.querySelector('button[type="submit"]');
        this._setButtonBusy(submitButton, true);
        let response;
        try {
            response = await this.postEvents(events);
        } finally {
            this._setButtonBusy(submitButton, false);
        }

        // Update only if server returned a non-empty content.
        if (this._requestManager.status === 200) {

            if (response && response.error) {
                this._showDialog(BaseCuesManager.ID_ERROR_DIALOG, response.error)
            }
            if (response && response.info) {
                this._showDialog(BaseCuesManager.ID_INFO_DIALOG, response.info)
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
