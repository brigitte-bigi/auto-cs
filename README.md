```
-------------------------------------------------------------------------

         █████╗ ██╗   ██╗████████╗ ██████╗        ██████╗███████╗
        ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗      ██╔════╝██╔════╝
        ███████║██║   ██║   ██║   ██║   ██║█████╗██║     ███████╗
        ██╔══██║██║   ██║   ██║   ██║   ██║╚════╝██║     ╚════██║
        ██║  ██║╚██████╔╝   ██║   ╚██████╔╝      ╚██████╗███████║
        ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝        ╚═════╝╚══════╝
                                                    
               Copyright (C) 2021-2026  Brigitte Bigi, CNRS
        Laboratoire Parole et Langage, Aix-en-Provence, France
-------------------------------------------------------------------------
```

# Auto-CS

## Motivations

Access to spoken language remains a challenge for deaf and hard-of-hearing individuals
due to the limitations of lipreading. Cued Speech (CS) addresses this by combining lip 
movements with hand cues—specific handshapes and placements near the face—making each 
syllable visually distinct. This system complements cochlear implants and supports oral 
language development, phonological awareness, and literacy.


## Scope and Scientific Purpose

`SPPAS+Auto-CS` is the first open-source system for automatically generating CS in video 
format. It takes as input a video recording, the corresponding audio signal, and an
orthographic transcript. These inputs are processed through a modular pipeline that 
includes phonetic mapping, temporal alignment, spatial placement, and real-time rendering
of a virtual coding hand. The output is a new version of the video in which a synchronized 
virtual hand encodes the CS transcription.

The architecture was built from scratch, with each stage formally defined, from segmentation 
to cue rendering. It is designed for multilingual use, and it has been implemented and tested 
for French. An evaluation under varied conditions reported decoding rates up to 92% for 
manually coded stimuli, and average scores above 80% for automatically generated cues.

`Auto-CS` addresses the scientific need to formalize and operationalize automatic Cued Speech
generation in a reproducible and fully documented way, in a context where no open-source 
operational system previously existed.

`Auto-CS` is a Python program developed within the project AutoCuedSpeech: 
<https://auto-cuedspeech.org>.

See also: <https://sppas.org/>


## Examples and Media

This repository includes illustrative material to facilitate understanding of the software.

The `media/` directory contains:

- A demo video generated with Auto-CS (identical to the demo distributed with SPPAS), 
  illustrating the automatic generation of Cued Speech from annotated data.
- Screenshots of TextCueS showing a complete guided pathway (text → sounds → code), including 
  intermediate representations and final output.

These materials are provided for demonstration and documentation purposes and do not affect 
the reproducibility instructions described above.


## Requirements and Installation

`Auto-CS` contains all the components dedicated to the automatic annotation of Cued Speech. 
This source code is not a standalone tool: it runs exclusively within SPPAS. It is integrated 
through the **spin-off** mechanism provided by SPPAS, which allows external code 
bases to remain separate while still being dynamically discovered and used by the main 
framework. Download and install SPPAS: <https://sppas.org/>

To generate coded videos only with `Auto-CS` (assuming prior preprocessing, as in the 
`demo` folder distributed with SPPAS), or to generate cues from written text, 
the following components must be enabled during SPPAS setup: video and autocs.

To run the full processing pipeline (using `SPPAS + Auto-CS`), the following components 
must be enabled during the SPPAS setup:

* Third-party programs: julius, wxpython, video, mediapipe
* Language resources: none (French and American English are included by default)
* Annotation resources: facedetect, facemark
* Spin-off programs: autocs


### Version compatibility

For reproducible experiments, the exact version of Auto-CS is determined by the SPPAS 
version used. The installed version of Auto-CS during the SPPAS Setup corresponds to the version 
bundled with the installed SPPAS release (see file `sppas/etc/features.ini` of SPPAS package). 

Version mapping between Auto-CS and SPPAS is indicated in the “Versions” section of this README.


### Release structure

For each version, two distributions are available:

1. Full distribution: complete source code, documentation, and project files (available 
   on both SourceForge and GitHub), with name "Auto-CS-version-dist.zip".
2. Spin-off distribution: code only, retrieved automatically by SPPAS from SourceForge and 
   installed as a spin-off, with name "autocs-version.zip".

SPPAS fetches the spin-off package directly from SourceForge during installation.


## Architecture

Auto-CS follows the modular pipeline architecture of SPPAS.
At repository level, the code base is organized as follows:
- `src/`: API (core implementation of Auto-CS modules).
- `ui/`: UI integration (TextCueS web app).
- `core/`: localization resources (gettext locale files).
- `bin/`: command-line entry points (e.g., `cuedspeech.py`).
- `etc/`: JSON configuration file used by SPPAS to integrate Auto-CS in its graphical interface.

The project also provides `makedoc.py` to generate the API documentation. It relies on 
the external documentation generator `ClammingPy`. With this generator, the API documentation 
is produced as accessible HTML5, including modes designed for visual impairments.
The generated documentation is located in the `Docs/` directory, provided both as accessible HTML 
and Markdown files.

The Cued Speech generation itself is implemented in `src/`, under `annotations/CuedSpeech/`. 
The remainder of this section describes this module-level architecture.

`Auto-CS` divides the problem of automatically cueing speech into four sequential tasks:

    1. WHAT? From the time-aligned phonemes, what are the keys?
    2. WHEN? From the time-aligned keys, when moving the hand (position and shape)?
    3. WHERE? Where should the hand be located, looking at the face?
    4. HOW? How the hand should look like?

The Proof-of-Concept of this system is described in the following reference:

> Brigitte Bigi, Núria Gala (2024).
> Preuve de concept d'un système de génération automatique en Langue française Parlée Complétée.
> In XXXVe Journées d’Études sur la Parole (JEP), pp. 512-520, Toulouse, France.
> <https://inria.hal.science/hal-04623112>

And the 1st stable version of this system is described in the following reference:
> Brigitte Bigi (2025).
> Bridging the Gap: Design and Evaluation of an Automated System for French Cued Speech
> International Conference on Natural Language and Speech Processing, Odense, Danemark.
> <https://hal.science/hal-05242638>


![Auto-CS processing pipeline](../media/workflow_sppas_autocs.png)

Figure: Global processing architecture of SPPAS + Auto-CS, from text/audio input to coded 
video output.


### What?

The conversion of phonemes into keys of CS is performed using a rule-based system. 
This RBS phoneme-to-key segmentation system is based on the following principle: 
a key is always of the form CV. A neutral position or a neutral shape is applied 
when respectively no vowel or no consonant is applicable.
To cite this work, use the following reference:

>Brigitte Bigi (2023).
>An analysis of produced versus predicted French Cued Speech keys.
>In 10th Language & Technology Conference: Human Language Technologies
>as a Challenge for Computer Science and Linguistics, Poznań, Poland.

The "what" question is implemented into the `whatkey` package. This is a package 
to predict the key code to be coded. It requires time-aligned phonemes. 
Its result is 3 tiers like in the following example:

```
    CS-PhonSegments:      |  b O~     |  Z u    |   R   |   #   |
    CS-PhonStructs:       |  C V      |  C V    |   C   |       |
    CS-Keys:              |  4 m      |  1 c    |  3 n  |  0 n  |
    CS-KeysClass:         |  C V      |  C V    |  C N  |  N N  |
```

Example of use:

```python
>>># Get the time-aligned phonemes
>>>trs_input = sppasTrsRW("file-palign.xra")
>>>phonemes = trs_input.find("PhonAlign")
>>># What? Create the transition predictor
>>>cued = CuedSpeechKeys("path/cueConfig-fra.txt")
>>>genkey = sppasWhatKeyPredictor()
>>>genkey.set_cue_rules(cued)
>>># Create the tiers with the CS keys from the phonemes
>>>cs_segments = genkey.phons_to_segments(phonemes)
>>>cs_keys, cs_class, cs_struct = genkey.segments_to_keys(cs_segments, phonemes.get_first_point(), phonemes.get_last_point())
```


### When ?

In Cued Speech, a key corresponds to a specific group of speech sounds 
(consonant+vowel, consonant alone or vowel alone) and the hand movements are 
timed to coincide with the relevant speech sound being produced. 

The issue to be raised here is a matter of timing: the temporal organization 
between the movements of the lips and hands in Cued Speech is a crucial aspect
of the system. This precise coordination is essential to accurately convey the
nuances of spoken language  and to bridge the gap between visual and auditory
communication.

It was already found in (Cornett, 1967) that lips and hand movements are 
asynchronous in CS. The study (Duchnowski et al., 1998) indicates that decoding
results were better when the hand was proposed 100ms before lip movements.
Then, (Duchnowski et al., 2000) indicated that a transition time of 150ms
for both the position and the shape increases decoding results. Studies of 
such temporal organization were performed on French language (Cathiard et al.,
2003; Attina, 2005; Aboutabit, 2007) with the proposal of a synchronization
model in the scope of CS decoding and recognition. They observed that lips 
movement is more related to the phoneme production and hand movement is
more related to the speech syllabic cycle, and that the handshape began to be
formed a long time before the acoustic consonant.

The "when" question is implemented into the `whenhand` package. 
This is a package to predict the key times. It requires key codes, the result 
of the "what" question. Its result is the following tiers:

- CS-HandPositions
- CS-HandShapes

The scope of this package is to implement hand transition predictors.
They will predict:

- the moments [M1, M2] when the hand is moving from a previous position to
  the current one (the vowel);
- the moments [D1, D2] when the hand is changing from a previous shape to
  the current one (the consonant).

There are several solutions to estimate transition intervals. These solutions 
make use of A1-A3 values, i.e., the 'begin' and 'end' time values of a key 
interval:

```
    A1             A2             A3
    | ---- C ----- | ----- V ---- |
    | ---- C -------------------- |
    | -------------------- V -----|
```

Five solutions are implemented in the form of generator classes predicting the
transition intervals [M1, M2] for the hand position transition times and 
[D1, D2] for the handshape transition times:

- model 0. No transition time values; returned intervals are [A1,A1] and [A1,A1].
- model 1. (Duchnowski et al., 1998) estimator. No transition times.
- model 2. (Duchnowski et al., 2000) estimator. Fixed 150 ms for all transitions.
- model 3. (Attina, 2005) estimators: p.117 for positions and p.136 for shapes.
- model 4. A proposed RBS-system based on the previous system and our expertise.
- model 5. A revised version of the previous system resulting of the analysis of CLeLfPC annotations.

Example of use:

```python
>>># When? Predict hand shapes and hand positions
>>>genhand = sppasWhenHandTransitionPredictor(predictor_version=4)
>>>genhand.set_cue_rules(cued)
>>>cs_pos, cs_shapes = genhand.when_hands(cs_keys, cs_segments)
```


### Where?

Another challenge is to model the hand’s trajectory: the research effort 
concerns the proposal of efficient models and algorithms that can predict
at any time the exact location of the cue position based on a general 
positioning of the speaker’s head. 

At first, we have to define the position of the vowels around the face. 
However, it’s variability is currently unknown. Then, the system is 
calculating a ”rate” between sights on the face thanks to a 68-sights 
face landmarks output. The ”rate” of each vowel was determined by experts 
and is always the same. For example, coordinates of the vowel
”m”, close to the mouth, are estimated by: 

- x = x48 − |(x54 − x48)/4|
- y = y60

Secondly, the trajectory between vowel positions has to be estimated during 
the hand transitions. The hand is moving from a position to another following 
a straight line, with a constant speed.

Finally, the angle of the arm has to be adjusted.

The "where" question is implemented into the `wherecue` package. 
This is a package to predict the hand positions at any time in the video. 
It requires predicted position and shape transitions. It produces a file
with the hand coordinates.

Two predictors are implemented for the vowel positions and 4 for the angle predictions.

```python
>>>gencue = sppasWhereCuePredictor()
>>>gencue.set_cue_rules(cued)
>>>gencue.set_wherepositionpredictor_version(1)
>>>gencue.set_whereanglepredictor_version(1)
>>># adjust annotations boundaries on frames of the video
>>>ann_on_media = sppasAnnsOnFrames(fps=60.)
>>>vf_pos = ann_on_media.adjust_boundaries(cs_pos.copy())
>>>vf_shape = ann_on_media.adjust_boundaries(cs_shape.copy())
>>>trs_coords = gencue.predict_where("path/file-ident.xra", vf_pos, vf_shape)
```


### How?

The final module of the system handles the visual rendering of the cueing 
hand, based on the timing and spatial information computed in the previous
stages. This component determines how the hand appears in the video and 
offers several options in terms of style and visual clarity

The "how" question is implemented into the `whowtag` package. 
This is a package to overlay a hand picture in images of the video. 
It requires predicted position, shape transitions and hand coordinates. 
It produces a video file.


```python
>>>tagger = CuedSpeechVideoTagger(cued)
>>>tagger.load(video_file)
>>>tagger.tag_with_keys(trs_coords, output)
>>>tagger.close()
```


## User Interfaces

### Command-line User Interface

Annotations of a video or a written text can be both performed thanks 
to `sppas/bin/cuedspeech.py`.


### Graphical-User Interface

TextCueS is the graphical user interface of Auto-CS. It is a guided web application integrated 
in SPPAS (SWApp) to generate Cued Speech keys from text, optionally allowing the user to review
intermediate representations before producing the final Cued Speech code.
A detailed conceptual description of TextCueS (needs analysis, architecture, UI design, 
accessibility principles) is available in the dedicated HAL dossier:
TextCueS – Dossier conceptuel (2026). HAL Id: hal-05511364.

Currently, the automatic generation of videos has to be performed with SPPAS wxPython GUI.
A guided web application integrated in SPPAS (SWApp) allowing the automatic encoding of 
a video is under development.


## Reproducibility / Availability of data and materials

Because Auto-CS is distributed as a SPPAS spin-off, it is not intended to run standalone.
The `demo/` folder (distributed with SPPAS) provides example inputs to reproduce the outputs 
described below.

### 1) Generate Cued Speech keys from text (TextCueS)

Launch:
```bash
.sppaspyenv~\Scripts\python sppas\ui\swapp
```

This opens a browser tab. 
Click the “TextCueS” application, then follow the guided interface.

Example: 
text `An example.` with language = American English produces: 
`5-t 4-m.7-s.2-t.5-s.1-sd.6-s`

### 2) Generate a cued video from command line

Get help:
```bash 
.\.sppaspyenv~\Scripts\python.exe .\sppas\bin\cuedspeech.py 
```

Re-generate the demo video (`demo/demo-cuedsp.mp4`):
```bash
.\.sppaspyenv~\Scripts\python.exe .\sppas\bin\cuedspeech.py -I demo -l fra --createvideo=true --handsset=yoyo --vowelspos=true
```

### 3) Generate a cued video from the wx GUI

Launch `sppas.bat`.
1. Add the files from the `demo/` folder to the file list and select any one of them.
2. Go to the “Annotate” tab and select language “fra”.
3. Click “Standalone annotations”, then check “Cued Speech coding”.
4. Set options in “Configure”: check video generation and enter "yoyo" in the hand set field.
5. Go back, then click “Let’s go”.


## Legal issues

### Help / How to contribute

If you want to report a bug, please send an e-mail to the author.
Any and all constructive comments are welcome.

If you plan to contribute to the code, please read carefully and agree both the 
code of conduct and the code style guide.
If you are contributing code or documentation to the WhakerPy project, you are 
agreeing to the DCO certificate <http://developercertificate.org>. 
Copy/paste the DCO, then you just add a line saying:
```
Signed-off-by: Random J Developer <random@developer.example.org>
```
Send this file by e-mail to the author.


### License/Copyright

See the accompanying `LICENSE` and `AUTHORS.md` files for the full list of contributors.

Copyright (C) 2021-2026 [Brigitte Bigi](https://sppas.org/bigi/), CNRS - <contact@sppas.org>
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
along with this program. If not, see <https://www.gnu.org/licenses/>.


## How to cite Auto-CS

By using `Auto-CS`, you are encouraged to mention it in your publications 
or products, in accordance with the best practices of the AGPL license.

Use the following reference to cite it:

> Brigitte Bigi. Auto-CS, Automatic generation of Cued Speech.
> ⟨hal-05462773v2⟩. Version 2.0. 2026. 
> <https://autocs.sourceforge.net>


### Logos and images

Logos and images of `Auto-CS` were all designed by Brigitte Bigi.
They are under the terms of CC BY-NC-ND 4.0,
Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International.

The AutoCuedSpeech project logo, included in this tool, was designed by 
Laurent Lopez - see "le Nébleu" at <https://laurentlopez-creations.com/>, 
and is used with full rights granted to the project. All rights reserved.


## Software Metadata

Metadata of Auto-CS is provided in the standard `codemeta.json` file included in this 
repository as it is recommended for Research Software. 
See <https://codemeta.github.io/> for details.


## Conflict of Interest

The author declares no conflict of interest.


## Funding / Acknowledgements

This research was funded by the FIRAH (Recherche Appliquée sur le Handicap, Applied Disability 
Research), project APa2022_022.


## Versions


### Pre spin-off version

Before becoming an independent spin-off, the initial Auto-CS proof-of-concept was distributed 
within SPPAS (versions >= 3.5).
SPPAS 4.22, which included the Auto-CS PoC, is registered with APP (Agence pour la Protection 
des Programmes, French software copyright agency) under IDDN.FR.001.500008.000.S.C.2024.000.31235.

<https://secure2.iddn.org/app.server/certificate/?sn=2024500008000&key=65723c3f60e753c66d72f5b621abc89301514489e6f88e4b5e4682ed4e2d4020&lang=fr>

It was awarded by the French Ministry of Higher Education, Research and Innovation at the 2022 
Open Source Research Software Competition.


### 1.0 - Attached to SPPAS-4.29

First release.


### 1.1 - Attached to SPPAS-4.30

Migrated to Whakerexa 2.0.


### 2.0 - Attached to SPPAS-4.31

- Deleted textcued app.
- Introduced **TextCueS** app, described here: <https://hal.science/hal-5511364/>

See TextCueS -with UI in French- in action at: <https://auto-cuedspeech.org/textcues.html>

It will be available -with UI in English- asap at: <https://sppas.org/textcues.html>




# Help

## Installation error

> Failed to establish a connection to the url https://sourceforge.net/projects/autocs/files/autocs-2.0.zip/download: 
> [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer 
> certificate (_ssl.c:1147).

Your Python installation cannot validate HTTPS connections (missing or outdated SSL certificates).
Install a recent version of Python, then reinstall and retry.

