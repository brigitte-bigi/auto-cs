
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
