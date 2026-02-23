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

`Auto-CS` is a Python program developed within the project AutoCuedSpeech: 
<https://auto-cuedspeech.org>. 
It contains all the components dedicated to the automatic annotation of Cued Speech. 
This source code is not a standalone tool: it only runs inside SPPAS. It is integrated 
by means of the **spin-off** mechanism provided by SPPAS, which allows external code 
bases to remain separate while still being dynamically discovered and used by the main 
framework.

> To create a coded video, Auto-CS requires video feature of SPPAS to be enabled.


## Automatic Annotation


### Overview

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

TextCues (incoming doc).

Another user interface is under development. It allows the automatic encoding 
of a video. Its development is less than 30%.


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


## How to cite AutoCuedSpeech

By using AutoCuedSpeech, you are encouraged to mention it in your publications 
or products, in accordance with the best practices of the AGPL license.

Use the following reference to cite AutoCuedSpeech:

> Brigitte Bigi. AutoCuedSpeech, Automatic generation of Cued Speech.
> Version 2.0. 2026. <https://autocs.sourceforge.net>

Check version for update.


### Logos and images

Logos and images were designed by Brigitte Bigi.
They are under the terms of CC BY-NC-ND 4.0,
Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International.

The AutoCuedSpeech project logo, included in this tool, was designed by 
Laurent Lopez - see "le Nébleu" at <https://laurentlopez-creations.com/>, 
and is used with full rights granted to the project. 
It is not covered by the AGPL license. All rights reserved.


## Versions

### 1.0 - Attached to SPPAS-4.29

First release.

### 1.1 - Attached to SPPAS-4.30

Migrated to Whakerexa 2.0.


### 2.0 - Attached to SPPAS-4.31

- Deleted textcued app.
- Introduced TextCueS app, described here: <https://hal.science/hal-5511364/>

See TextCueS in action at: <https://sppas.org/textcues.html>
and at: <https://auto-cuedspeech.org/textcues.html>
