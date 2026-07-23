# SPLI:CS — the Cued Speech spin-off of SPPAS

`splics` is a spin-off of SPPAS: a separate application, developed under its
own name and license (part of Auto-CS, <https://autocs.sourceforge.io>), that
is grafted into the SPPAS web interface. It is dropped into the `spinoff/`
package of `swapp` and discovered dynamically: removing this folder leaves
SPPAS whole, and adding it back does not require a single change to SPPAS.

The long-term goal is a full learning application for the Cued Speech coding.
The web applications served here are only its coding part; the rest
of the application -- accounts, sessions, progression, and the standalone
program doing `import sppas` -- lives in the separate `splics` project, never
in this repository.


## How SPLI:CS is grafted into swapp

The `spinoff/` loader of swapp ignores sub-packages: what it discovers are the
declaration modules dropped directly into `spinoff/` (`listcues.py`,
`textcues.py`, `twincues.py`). Each exposes a `SWAPP_CLASS` -- the app's
`WebData` class -- collected into the `SPINOFF_SWAPPS` registry and served
exactly like a native swapp application.

The whole spin-off code lives under a single `splics/` namespace, so no module
or class of SPLI:CS can ever collide with one of SPPAS nor with one of another
spin-off.


## The three categories

The SPLI:CS applications are sorted into three categories, the three learning
modules of the application:

- **Discovery** (`discovery/`) — the learning module: the LPC coding apps
  (ListCueS, TextCueS, TwinCueS, ...);
- **Exploration** (`exploration/`) — the self-testing module: the interactive
  assessments;
- **Recreation** (`recreation/`) — the consolidation module: the games.

The three categories are declared once, as the members of the immutable
`splics_categories` instance in `splicssg.py`. Each application declares the
one it belongs to with a `CATEGORY` class member on its `WebData` (for
example, `CATEGORY = splics_categories.discovery`). The SPLI:CS dashboard then
builds itself by grouping the registered applications by their `CATEGORY` --
one section per category, in the order of `splics_categories.ordered`, no
hardcoded list: adding an app to a category is declaring its `CATEGORY`,
nothing else.

Only the categories that have applications get a directory: `discovery/`
exists today; `exploration/` and `recreation/` are added when they get their
first app. The three categories, however, exist from the start, so the
dashboard mechanism is complete before the modules are.


## Organization of the package

- `splicssg.py` holds the immutable global settings of the spin-off:
  `splics_paths` (its statics, all gathered under `statics/spinoff/splics/`
  of swapp, so that no file of SPLI:CS is mixed with the ones of SPPAS nor with
  those of another spin-off) and `splics_categories` (the three application
  categories);
- `discovery/` (and later `exploration/`, `recreation/`) holds the `app_*`
  applications of the category;
- `nodes/` holds the reusable HTML nodes shared across the apps, grouped by
  role: `buttons/`, `layout/`, `feedback/`, `cues/` -- the same convention as
  swapp's own `nodes/`, plus the `cues/` role for the LPC-specific nodes;
- `models/` holds the pure-domain models shared across the apps (phonetizer,
  text normalizer, key candidates, key-piano images).

An `app_*` application keeps its own `models/` and `views/` for what is
specific to it; only what is shared by several apps goes up to the `nodes/`
and `models/` of `splics/`.


## Dependencies on swapp

SPLI:CS depends on swapp through a stable surface only: `wappcore` (settings),
`wappbase` (the `WebData`, response and view base classes) and the shared
`nodes/`. It never reaches into another app of swapp. This keeps the graft
detachable and lets the future standalone `splics` program reuse the same apps
through `import sppas`.
