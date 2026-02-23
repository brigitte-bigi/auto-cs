
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
