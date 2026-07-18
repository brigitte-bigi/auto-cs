This package implements the SPPAS spin-off ListCueS web application following a
Model–View–Controller (MVC) architecture.

- **ListCueSResponseRecipe** is the single *HTTP transport layer* recipe,
  for the single page `listcues.html`. There is no separate launcher: a
  language having reached the controller (welcome form, or a `convert`
  event) is the only thing distinguishing the conversion state from the
  welcome one -- the application is stateless (no session, no server-side
  memory), so this distinction cannot rely on anything else.

- **ListCueSController** represents the *MVC controller*.
  It manages the application logic: dispatching the received sequence of keys
  to the model, and invoking the view to build the HTML fragment of the result.
  `handle_convert()` is used identically whether the language arrives alone
  (from the welcome form) or together with a cue (from the "Validate" button).

- **ListCueSView** is the *View* component responsible for building the static
  and dynamic HTML structure (head, header, body, footer, scripts) using
  WhakerPy's HTMLTree utilities. It shows **ListCueSWelcomeView** while
  `record.lang` is `None`, and **ListCueSPageView** (piano and result) once a
  language is known.

- **ListCueSModel** restricts the Cued Speech key -> phoneme(s) rules of the
  current language to the phonemes actually attested in its pronunciation
  dictionary, then dispatches to **Keys2PronsModel** to enumerate the
  pronounceable phoneme sequences of the input keys and their matching words.

A key ("<shape>-<position>") is ambiguous by design: several consonants can
share the same shape, several vowels can share the same position, so a
sequence of keys can expand into a very large number of raw candidate
phoneme sequences (e.g. a single French key repeated 7 times, all-consonants
-- 19 candidates per key, ~19^7 leaf paths without pruning). Pronounceability
alone (PHONMERGE consonant-cluster legality) is not enough to bound this: for
some phonemes, nearly every 2-consonant combination is a legal cluster, so
branching stays close to the unpruned maximum. **Keys2PronsModel** instead
prunes the search itself, the same way the first pass of an ASR system based
on Viterbi/Baum-Welch decoding cuts a lattice: the set of every contiguous
4-phoneme window actually observed across the pronunciation dictionary is
built once (`NGRAM_SIZE = 4`, in the same pass as `ListCueSModel`'s dictionary
index), and a branch is cut as soon as its trailing 4-phoneme window was
never observed -- it can then never lead to a real word. 4 was determined
empirically to be the smallest window that keeps the worst case (7 maximally
ambiguous keys) tractable; 3 was not enough. The surviving sequences are
reported with the word(s) sharing each of them, or an empty list if none
exists: a pronounceable sequence with no matching word is still reported.

Page: `listcues.html`, in two states.
- Welcome (no language chosen): intro, and a plain GET form choosing the
  language. Submitting it navigates to `listcues.html?lang=xxx` -- a real
  page reload, since the whole layout changes; only the accessibility
  parameters are added to that navigation client-side (same mechanism as
  the menu links).
- Conversion (a language is known): a hidden field carries that language
  forward, a textarea holds the "cue" (a sequence of keys), and a
  Whakerexa **KeyPiano** (see `whakerexa/wexa_statics/js/extras/keypiano/`)
  lets the shape and position of each key be composed by clicking rather
  than typed by hand. Clicking "Validate" sends a `convert` event to the
  server (no page reload) and the result section -- a 2-column table,
  pronunciation and matching word(s) -- is updated in place.

Missing assets (to be added):
- The icon referenced by `sppasImagesAccess.get_icon_filename("listcues")`
  is only defined for the "Refine" theme.
- The piano keys are plain text codes for now (e.g. "1", "s"); images may
  replace them later without changing `KeyPianoNode`'s HTML contract.
