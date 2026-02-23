
## CuedSpeech: What key?

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

