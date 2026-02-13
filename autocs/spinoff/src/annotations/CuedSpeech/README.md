
## Overview

> CuedSpeech package requires video feature, for opencv and numpy dependencies.

The problem of cueing speech is divided into 4 sequential tasks:

    1. WHAT? From the time-aligned phonemes, what are the keys?
    2. WHEN? From the time-aligned keys, when moving the hand (position and shape)?
    3. WHERE? Where should the hand be located, looking at the face?
    4. HOW? How the hand should look like?

In French, Cued Speech is LfPC, the "Langue française Parlée Complétée".
The Proof-of-Concept of this system is described in the following reference:

> Brigitte Bigi, Núria Gala (2024).
> Preuve de concept d'un système de génération automatique en Langue française Parlée Complétée.
> In XXXVe Journées d’Études sur la Parole (JEP), pp. 512-520, Toulouse, France.
> <https://inria.hal.science/hal-04623112>


## What?

### Overview

The conversion of phonemes into keys of CS is performed using a rule-based system. 
This RBS phoneme-to-key segmentation system is based on the following principle: 
a key is always of the form CV. 
A neutral position or a neutral shape is applied when respectively no vowel or no consonant is applicable.

### Implementation

The "what" question is implemented into the `whatkey` package. This is a package to predict the key code to be coded. It requires time-aligned phonemes. 
Its result is 3 tiers like in the following example:

```
    CS-PhonSegments:      |  b O~     |  Z u    |   R   |   #   |
    CS-PhonStructs:       |  C V      |  C V    |   C   |       |
    CS-Keys:              |  4 m      |  1 c    |  3 n  |  0 n  |
    CS-KeysClass:         |  C V      |  C V    |  C N  |  N N  |
```

### Reference

To cite this work, use the following reference:

>Brigitte Bigi (2023).
>An analysis of produced versus predicted French Cued Speech keys.
>In 10th Language & Technology Conference: Human Language Technologies
>as a Challenge for Computer Science and Linguistics, Poznań, Poland.

#### Abstract

Cued Speech is a communication system developed for deaf people to
complement speechreading at the phonetic level with hands. This
visual communication mode uses handshapes in different placements
near the face in combination with the mouth movements of speech
to make the phonemes of spoken language look different from each other.
This paper presents an analysis on produced cues in 5 topics of CLeLfPC,
a large corpus of read speech in French with Cued Speech.
A phonemes-to-cues automatic system is proposed in order to predict the
cue to be produced while speaking. This system is part of SPPAS -
the automatic annotation an analysis of speech, an open source software
tool. The predicted keys of the automatic system are compared to the
produced keys of cuers. The number of inserted, deleted and substituted
keys are analyzed. We observed that most of the differences between
predicted and produced keys comes from 3 common position’s substitutions
by some of the cuers.

#### Example of use

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

## When ?

### Overview

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

### Implementation

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
- model 4. a newly proposed RBS-system based on the previous system and our expertise.

#### Example of use

```python
>>># When? Predict hand shapes and hand positions
>>>genhand = sppasWhenHandTransitionPredictor(predictor_version=4)
>>>genhand.set_cue_rules(cued)
>>>cs_pos, cs_shapes = genhand.when_hands(cs_keys, cs_segments)
```

## Where?

### Overview

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

### Implementation

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

## How?

This section will be fully documented in a further version SPPAS.

```python
>>>tagger = CuedSpeechVideoTagger(cued)
>>>tagger.load(video_file)
>>>tagger.tag_with_keys(trs_coords, output)
>>>tagger.close()
```
