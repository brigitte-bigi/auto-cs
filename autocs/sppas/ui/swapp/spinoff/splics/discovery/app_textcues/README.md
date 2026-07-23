This package implements the SPPAS spin-off TextCueS web application following a
Model–View–Controller (MVC) architecture with a clear separation of concerns.

- **TextCueSResponseRecipe** is the single *HTTP transport layer* recipe,
  for the fixed welcome page `textcues.html` and every random pathway page
  `textcues_<hex>.html`. There is no separate launcher: a language having
  reached the controller (welcome form, or a pathway step) is the only
  thing distinguishing the pathway state from the welcome one -- the
  application is stateless (no session, no server-side memory), so this
  distinction cannot rely on anything else. A "lang" query received with no
  "pathway" yet, on the fixed welcome URL itself, is silently ignored: only
  the random URL the welcome form actually submits to may trigger it (see
  `set_requested_page()`).

- **TextCueSController** represents the *MVC controller*.
  It manages the application logic: interacting with the model, and invoking the
  view to construct the HTML representation of the content. According to the
  pathway identifier carried by the record, it dispatches to the corresponding
  step (Text, Sound, Code); `handle()` treats "a language with no pathway yet"
  (the welcome form's navigation) the same way it treats a normal step, so
  there is only one code path to keep in sync.

- **TextCueSView** is the *View* component responsible for building the static
  and dynamic HTML structure (head, header, body, footer, scripts) using
  WhakerPy's HTMLTree utilities. It shows **TextCueSWelcomeView** while
  `record.lang` is `None`, and the pathway views (Text, Sound, Code) once a
  language is known.

- **TextCueSModel** is an interface with the CuedSpeech automatic annotation.
  `test_overlay_available()`/`test_video_available()` do not return a plain
  bool: they return one of `REASON_AVAILABLE`, `REASON_NOT_INSTALLED`
  (a dependency or resource is missing in this environment) or
  `REASON_NOT_IMPLEMENTED` (the current language is not covered yet by the
  position/angle prediction models) -- two different causes that used to be
  collapsed into a single "unavailable" boolean, and so could not be told
  apart in the resulting message.

This structure ensures a clean separation between transport (HTTP),
application logic (Controller), data (Model), and presentation (View), improving
maintainability and scalability of this web interface.

Pages:
- `textcues.html`: welcome page. Intro, and a plain GET form choosing the
  language. Submitting it navigates to a random `textcues_<hex>.html?lang=xxx`
  -- a real page reload, since the whole layout changes; only the
  accessibility parameters are added to that navigation client-side (same
  mechanism as the menu links).
- `textcues_<hex>.html`: the pathway, in three steps (Text, Sound, Code),
  each carrying the language forward as a hidden field. The language has no
  selector of its own past welcome.

`TextCueSRecord.overlay_status`/`video_status` carry the model's reason
forward across pathway steps (transport only, no business logic): the Code
view picks the "not installed" and/or "not implemented" message(s) actually
in play, showing both if overlay and video fail for different reasons.
