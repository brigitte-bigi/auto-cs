This package implements the SPPAS spin-off TwinCueS web application following a
Model–View–Controller (MVC) architecture.

- **TwinCueSResponseRecipe** is the single *HTTP transport layer* recipe,
  for the single page `twincues.html`. There is no separate launcher: a
  language having reached the controller (welcome form, or a `convert`
  event) is the only thing distinguishing the conversion state from the
  welcome one -- the application is stateless (no session, no server-side
  memory), so this distinction cannot rely on anything else.

- **TwinCueSController** represents the *MVC controller*.
  It manages the application logic: dispatching the received word and/or cue
  to the model, and invoking the view to build the HTML fragment of the result.
  `handle_convert()` is used identically whether the language arrives alone
  (from the welcome form) or together with a word/cue (from the "Validate"
  button).

- **TwinCueSView** is the *View* component responsible for building the static
  and dynamic HTML structure (head, header, body, footer, scripts) using
  WhakerPy's HTMLTree utilities. It shows **TwinCueSWelcomeView** while
  `record.lang` is `None`, and **TwinCueSPageView** (word/cue textareas,
  piano and result) once a language is known.

- **TwinCueSModel** dispatches to two conversion models:
  **Word2CuesModel** (word -> cue) and **Cues2WordsModel** (cue -> word(s)).

Page: `twincues.html`, in two states.
- Welcome (no language chosen): intro, and a plain GET form choosing the
  language. Submitting it navigates to `twincues.html?lang=xxx` -- a real
  page reload, since the whole layout changes; only the accessibility
  parameters are added to that navigation client-side (same mechanism as
  the menu links).
- Conversion (a language is known): a hidden field carries that language
  forward, one textarea holds the "word", the other the "cue" (a sequence
  of keys). A Whakerexa **KeyPiano** (see
  `whakerexa/wexa_statics/js/extras/keypiano/`) lets the shape and position
  of each key be composed by clicking rather than typed by hand. The two
  textareas are mutually exclusive: typing in one, or composing a cue with
  the piano, clears the other -- KeyPiano dispatches a real `input` event on
  every change it makes, precisely so this listener (and any other relying
  on `input`) reacts the same way to a piano click as to a keystroke.
  Clicking "Validate" sends a `convert` event to the server (no page reload)
  and the result section is updated in place.
