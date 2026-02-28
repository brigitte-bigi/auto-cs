# CuedSpeech.whenhand module

## List of classes

## Class `sppasCuedPredictorError`

### Description

*:ERROR 1325:.*

No predictor system is defined.


### Constructor

#### __init__

```python
def __init__(self):
    self._status = 1325
    self.parameter = error(self._status) + error(self._status, 'annotations')
```





### Public functions

#### get_status

```python
def get_status(self):
    return self._status
```





### Overloads

#### __str__

```python
def __str__(self):
    return repr(self.parameter)
```





## Class `WhenTransitionPredictor`

### Description

*Hand transitions predictor for both hand shape and hand position.*

There are several solutions to estimate transition intervals. These
solutions make use of A1-A3 values, i.e., the 'begin' and 'end' time
values of a key interval:

A1             A2             A3
| ---- C ----- | ----- V ---- |
| ---- C -------------------- |
| -------------------- V -----|

Five solutions are implemented in the form of generator classes predicting the
transition intervals [M1, M2] and [D1, D2]:

Implemented predictors will predict:

- the moments [M1, M2] when the hand is moving from a previous position to
the current one (the vowel);
- the moments [D1, D2] when the hand is changing from a previous shape to
the current one (the consonant).

Implemented models are:

- model 0 (Base): moments at the same time as the key
- model 1 (Duchnowski et al. 1998): moments M1-M2 are both 100ms before the key
- model 2 (Duchnowski et al. 2000): moment M2 100ms before the key, M1-M2 transition is 150ms
- model 3 (Attina, 2005): moments proportional to key duration
- model 4 (custom rules): custom rules based on our expertise in coding.
- model 5 (revised rules): revised rules based on observed values in CleLfPC dataset.


### Constructor

#### __init__

```python
def __init__(self, version_number: int=DEFAULT):
    """Create a hand transitions predictor.

    :param version_number: (int) Version of the predictor system ranging (0-3).

    """
    self.__predictor = None
    self.__version = WhenTransitionPredictor.DEFAULT
    self.set_version_number(version_number)
```

*Create a hand transitions predictor.*

##### Parameters

- **version_number**: (*int*) Version of the predictor system ranging (0-3).



### Public functions

#### version_numbers

```python
@staticmethod
def version_numbers() -> list:
    """Return the whole list of supported version numbers."""
    return list(WhenTransitionPredictor.HAND_TRANSITIONS.keys())
```

*Return the whole list of supported version numbers.*

#### get_a1a3_avg_duration

```python
def get_a1a3_avg_duration(self) -> float:
    """Return the average of stored [A1;A3] durations or the fixed one.

        If there's not enough known [A1;A3] durations, the fixed value is
        returned.

        """
    return self.__predictor.get_a1a3_avg_duration()
```

*Return the average of stored [A1;A3] durations or the fixed one.*

If there's not enough known [A1;A3] durations, the fixed value is
returned.

#### get_version_number

```python
def get_version_number(self) -> int:
    """Return the version number of the selected predictor (int)."""
    return self.__version
```

*Return the version number of the selected predictor (int).*

#### set_version_number

```python
def set_version_number(self, version_number: int) -> None:
    """Change the predictor version number.

        It invalidates the current values of A1 and A3.

        :param version_number: (int) One of the supported versions.
        :raises: sppasKeyError: if invalid version number

        """
    authorized = self.version_numbers()
    try:
        v = int(version_number)
        if v not in authorized:
            raise sppasKeyError(str(authorized), version_number)
    except ValueError:
        logging.error('Hand transition: invalid predictor version {}. Expected one of: {}'.format(version_number, authorized))
        raise sppasKeyError(str(authorized), version_number)
    self.__version = v
    self.__predictor = WhenTransitionPredictor.HAND_TRANSITIONS[self.__version]()
```

*Change the predictor version number.*

It invalidates the current values of A1 and A3.

##### Parameters

- **version_number**: (*int*) One of the supported versions.


##### Raises

- *sppasKeyError*: if invalid version number

#### set_a

```python
def set_a(self, a1: float, a3: float, store: bool=True) -> None:
    """Set [A1,A3] the moments of the sounds of a newly observed key.

        Instantiate the predictor with the given interval:

            - a1 - when the 1st phoneme of the key starts in the audio;
            - a3 - when the 2nd phoneme of the key ends in the audio.

        :param a1: (float) Start time value of a key
        :param a3: (float) End time value of a key
        :param store: (bool) Store the a1 and a3 values into a list
        :raises: sppasTypeError: one of a1 or a3 is not a float
        :raises: RangeBoundsException: if a3 is lesser than a1
        :raises: sppasCuedPredictorError: No predictor system is defined

        """
    if self.__predictor is None:
        raise sppasCuedPredictorError
    self.__predictor.set_key_interval(a1, a3, store)
```

*Set [A1,A3] the moments of the sounds of a newly observed key.*

Instantiate the predictor with the given interval:

- a1 - when the 1st phoneme of the key starts in the audio;
- a3 - when the 2nd phoneme of the key ends in the audio.

##### Parameters

- **a1**: (*float*) Start time value of a key
- **a3**: (*float*) End time value of a key
- **store**: (*bool*) Store the a1 and a3 values into a list


##### Raises

- *sppasTypeError*: one of a1 or a3 is not a float
- *RangeBoundsException*: if a3 is lesser than a1
- *sppasCuedPredictorError*: No predictor system is defined

#### reset_key_intervals

```python
def reset_key_intervals(self):
    """Forget the stored A1,A3 moments."""
    self.__predictor.reset_key_intervals()
```

*Forget the stored A1,A3 moments.*

#### predict_m

```python
def predict_m(self, **kwargs) -> tuple:
    """Predict [M1,M2] the moments when the hand is moving.

        Make use of the defined predictor and estimates the position
        transition moments:

            - Predict M1 - when leaving the current position
            - Predict M2 - when arrived to the expected position

        Neutral means it's not a phoneme: the key is 0-n.
        A nil shape means it's a key of type -V.

        Depending on the predictor, possible arguments are:

         - rank: (int) The rank of the key after a silence (sil=0, 1st key=1, ...)
         - is_nil_shape: (bool) The shape is nil, i.e. there's no consonant in the syllable (N-V)

        :return: tuple(float, float) The interval [M1,M2] or (0.,0.)
        :raises: sppasCuedPredictorError: No predictor defined.

        """
    if self.__predictor is None:
        raise sppasCuedPredictorError
    return self.__predictor.predict_position(**kwargs)
```

*Predict [M1,M2] the moments when the hand is moving.*

Make use of the defined predictor and estimates the position
transition moments:

- Predict M1 - when leaving the current position
- Predict M2 - when arrived to the expected position

Neutral means it's not a phoneme: the key is 0-n.
A nil shape means it's a key of type -V.

Depending on the predictor, possible arguments are:

- rank: (int) The rank of the key after a silence (sil=0, 1st key=1, ...)
- is_nil_shape: (bool) The shape is nil, i.e. there's no consonant in the syllable (N-V)

##### Returns

- tuple(*float*, *float*) The interval [M1,M2] or (0.,0.)


##### Raises

- *sppasCuedPredictorError*: No predictor defined.

#### predict_d

```python
def predict_d(self, **kwargs) -> tuple:
    """Predict [D1,D2] the moments when fingers are changing.

        Make use of the defined predictor and estimates the shape transition
        moments:

            - Predict D1 - when starting to move fingers
            - Predict D2 - when ending to move fingers

        Depending on the predictor, possible arguments are:
         - rank: (int) The rank of the key after a silence (sil=0, 1st key=1, ...)
         - is_nil_shape: (bool) The shape is nil, i.e. there's no consonant in the syllable (N-V)

        :return: tuple(float, float) The interval [D1,D2] or (0.,0.)
        :raises: sppasCuedPredictorError: No predictor defined.

        """
    if self.__predictor is None:
        raise sppasCuedPredictorError
    return self.__predictor.predict_shape(**kwargs)
```

*Predict [D1,D2] the moments when fingers are changing.*

Make use of the defined predictor and estimates the shape transition
moments:

- Predict D1 - when starting to move fingers
- Predict D2 - when ending to move fingers

Depending on the predictor, possible arguments are:
- rank: (int) The rank of the key after a silence (sil=0, 1st key=1, ...)
- is_nil_shape: (bool) The shape is nil, i.e. there's no consonant in the syllable (N-V)

##### Returns

- tuple(*float*, *float*) The interval [D1,D2] or (0.,0.)


##### Raises

- *sppasCuedPredictorError*: No predictor defined.



## Class `sppasWhenHandTransitionPredictor`

### Description

*Create the CS coding scheme from time-aligned phonemes.*

From the time-aligned keys, this class can estimate the moments of the
hand shape transitions (consonants) and the moments of the hand position
transitions (vowels).

It aims to predict when the hand changes both its position and its shape.
It results in two tiers indicating intervals with transitions:

- CS-HandPositions predicting [M1,M2] intervals when position is changing;
- CS-HandShapes predicting [D1,D2] intervals when shape is changing.


### Constructor

#### __init__

```python
def __init__(self, predictor_version=WhenTransitionPredictor.DEFAULT, cue_rules=CuedSpeechCueingRules()):
    """Instantiate a CS generator.

    :param cue_rules: (CuedSpeechKeys) Rules to convert phonemes => keys

    """
    self.__cued = None
    self.set_cue_rules(cue_rules)
    self.__transitions = WhenTransitionPredictor()
    self.set_whenpredictor_version(predictor_version)
```

*Instantiate a CS generator.*

##### Parameters

- **cue_rules**: (CuedSpeechKeys) Rules to convert phonemes => keys



### Public functions

#### set_cue_rules

```python
def set_cue_rules(self, cue_rules: CuedSpeechCueingRules) -> None:
    """Set new rules.

        :param cue_rules: (CuedSpeechKeys) Rules and codes for vowel positions and hand shapes
        :raises: sppasTypeError: given parameter is not CuedSpeechCueingRules

        """
    if isinstance(cue_rules, CuedSpeechCueingRules) is False:
        raise sppasTypeError('cue_rules', 'CuedSpeechCueingRules')
    self.__cued = cue_rules
```

*Set new rules.*

##### Parameters

- **cue_rules**: (CuedSpeechKeys) Rules and codes for vowel positions and hand shapes


##### Raises

- *sppasTypeError*: given parameter is not CuedSpeechCueingRules

#### get_whenpredictor_version

```python
def get_whenpredictor_version(self) -> int:
    """Return the version number of the generation system."""
    return self.__transitions.get_version_number()
```

*Return the version number of the generation system.*

#### get_whenpredictor_versions

```python
@staticmethod
def get_whenpredictor_versions() -> list:
    """Return the list of version numbers of the generation system."""
    return WhenTransitionPredictor.version_numbers()
```

*Return the list of version numbers of the generation system.*

#### set_whenpredictor_version

```python
def set_whenpredictor_version(self, value: int) -> None:
    """Set the prediction system version.

        - 0: no time estimation.
        - 1: system based on P. Duchnowski et al. (1998)
        - 2: system based on P. Duchnowski et al. (2000)
        - 3: system based on V. Attina (2005) synchronization model
        - 4: empirical rules from B. Bigi & Datha
        - 5: revised rules by B. Bigi

        :raises: sppasKeyError:
        :raises: TypeError:

        """
    value = int(value)
    self.__transitions = WhenTransitionPredictor(value)
```

*Set the prediction system version.*

- 0: no time estimation.
- 1: system based on P. Duchnowski et al. (1998)
- 2: system based on P. Duchnowski et al. (2000)
- 3: system based on V. Attina (2005) synchronization model
- 4: empirical rules from B. Bigi & Datha
- 5: revised rules by B. Bigi

##### Raises

- *sppasKeyError*
- *TypeError*

#### shape_is_neutral

```python
def shape_is_neutral(self, s: str) -> bool:
    """Return True if the given character is the neutral shape.

        :param s: (str) Character representing a shape
        :return: (bool) The shape is neutral

        """
    return s == self.__cued.get_neutral_consonant()
```

*Return True if the given character is the neutral shape.*

##### Parameters

- **s**: (*str*) Character representing a shape


##### Returns

- (*bool*) The shape is neutral

#### position_is_neutral

```python
def position_is_neutral(self, p: str) -> bool:
    """Return True if the given character is the neutral position.

        :param p: (str) Character representing a position
        :return: (bool) The position is neutral

        """
    return p == self.__cued.get_neutral_vowel()
```

*Return True if the given character is the neutral position.*

##### Parameters

- **p**: (*str*) Character representing a position


##### Returns

- (*bool*) The position is neutral

#### get_a1a3_avg_duration

```python
def get_a1a3_avg_duration(self):
    """Return the average of stored [A1;A3] durations or the fixed one.

        If there's not enough known [A1;A3] durations, the fixed value is
        returned.

        """
    return self.__transitions.get_a1a3_avg_duration()
```

*Return the average of stored [A1;A3] durations or the fixed one.*

If there's not enough known [A1;A3] durations, the fixed value is
returned.

#### has_nil_pos

```python
def has_nil_pos(self, phns: str) -> bool:
    """Return True if the given string does not contain a vowel.

        :param phns: (str) Phonemes of a key in the form "C-V" or "V" or "C"
        :return: (bool) True if the phns are of "C" structure

        """
    return self.__cued.get_class(phns) == 'C' if '-' not in phns else False
```

*Return True if the given string does not contain a vowel.*

##### Parameters

- **phns**: (*str*) Phonemes of a key in the form "C-V" or "V" or "C"


##### Returns

- (*bool*) True if the phns are of "C" structure

#### has_nil_shape

```python
def has_nil_shape(self, phns: str) -> bool:
    """Return True if the given string does not contain a consonant.

        :param phns: (str) Phonemes of a key in the form "C-V" or "V" or "C"
        :return: (bool) True if the phns are of "V" structure

        """
    return self.__cued.get_class(phns) == 'V' if '-' not in phns else False
```

*Return True if the given string does not contain a consonant.*

##### Parameters

- **phns**: (*str*) Phonemes of a key in the form "C-V" or "V" or "C"


##### Returns

- (*bool*) True if the phns are of "V" structure

#### asset_a1a3

```python
def asset_a1a3(self, tier_keys: sppasTier) -> None:
    """Reset then store all [a1;a3] values in the transitions model.

        :param tier_keys: (sppasTier)

        """
    self.__transitions.reset_key_intervals()
    for ii in range(len(tier_keys)):
        ann = tier_keys[ii]
        interval = ann.get_location()
        labels = ann.get_labels()
        if len(labels) != 2:
            logging.error('Expected 2 labels of annotation: {:s}'.format(str(ann)))
            raise sppasCuedRulesValueError(serialize_labels(labels))
        a1 = interval.get_lowest_localization().get_midpoint()
        a3 = interval.get_highest_localization().get_midpoint()
        cur_pos = labels[1].copy()
        is_neutral = self.position_is_neutral(cur_pos.get_best().get_content())
        self.__transitions.set_a(a1, a3, store=not is_neutral)
```

*Reset then store all [a1;a3] values in the transitions model.*

##### Parameters

- **tier_keys**: (sppasTier)

#### when_hands

```python
def when_hands(self, tier_keys: sppasTier, tier_segments: sppasTier) -> tuple:
    """Create two tiers with the transition periods of the hand.

        :param tier_keys: (sppasTier)
        :param tier_segments: (sppasTier) Tier with name 'CS-PhonSegments', phonemes of each key
        :return: (sppasTier, sppasTier) Position transitions and Shape transitions
        :raises: sppasCuedRulesValueError

        """
    if len(tier_keys) * len(tier_segments) == 0:
        cs_pos = sppasTier('CS-HandPositions')
        cs_shapes = sppasTier('CS-HandShapes')
    else:
        (positions_moves, shapes_moves) = self.predict_transitions(tier_keys, tier_segments)
        cs_pos = self.predicted_to_tier(positions_moves)
        cs_pos.set_name('CS-HandPositions')
        cs_shapes = self.predicted_to_tier(shapes_moves)
        cs_shapes.set_name('CS-HandShapes')
    cs_pos.set_meta('cued_speech_position_of_keys_tier', tier_keys.get_name())
    cs_shapes.set_meta('cued_speech_shape_of_keys_tier', tier_keys.get_name())
    cs_pos.set_meta('cued_speech_position_of_phns_tier', tier_segments.get_name())
    cs_shapes.set_meta('cued_speech_shape_of_phns_tier', tier_segments.get_name())
    return (cs_pos, cs_shapes)
```

*Create two tiers with the transition periods of the hand.*

##### Parameters

- **tier_keys**: (sppasTier)
- **tier_segments**: (sppasTier) Tier with name 'CS-PhonSegments', phonemes of each key


##### Returns

- (sppasTier, sppasTier) Position transitions and Shape transitions


##### Raises

sppasCuedRulesValueError

#### predict_transitions

```python
def predict_transitions(self, tier_keys: sppasTier, tier_segments: sppasTier) -> tuple:
    """Return the predicted position transitions and shape transitions.

        The two returned lists contain:

        - the estimated m1 and m2 values (in seconds), or d1 and d2;
        - the transition position in a tuple with origin and target; and
        - the origin/target annotation identifiers.

        :param tier_keys: (sppasTier)
        :param tier_segments: (sppasTier) Tier with name 'CS-PhonSegments', phonemes of each key
        :return: tuple(PredictedWhenHand, PredictedWhenHand)
        :raises: sppasCuedRulesValueError

        """
    pos_moves = PredictedWhenHand()
    shp_moves = PredictedWhenHand()
    self.asset_a1a3(tier_keys)
    ann = tier_keys[0]
    labels = ann.get_labels()
    prev_shape = labels[0].copy()
    prev_pos = labels[1].copy()
    interval = ann.get_location()
    key_rank_ipu = 1
    prev_phns = self.__get_phones(tier_segments, interval)
    for ii in range(1, len(tier_keys)):
        ann = tier_keys[ii]
        labels = ann.get_labels()
        cur_shape = labels[0].copy()
        cur_pos = labels[1].copy()
        cur_phns = self.__get_phones(tier_segments, ann.get_location())
        interval = ann.get_location()
        a1 = interval.get_lowest_localization().get_midpoint()
        a3 = interval.get_highest_localization().get_midpoint()
        if self.position_is_neutral(cur_pos.get_best().get_content()) is True:
            key_rank_ipu = 0
        self.__transitions.set_a(a1, a3, store=False)
        if prev_pos != cur_pos or (prev_pos == cur_pos and prev_pos != 's') or (prev_pos == cur_pos and prev_pos == 's' and (prev_shape == cur_shape)):
            (m1, m2) = self.__transitions.predict_m(rank=key_rank_ipu, is_nil_shape=self.has_nil_shape(cur_phns), is_nil_pos=self.has_nil_pos(cur_phns))
            prev_pos.set_key(prev_phns)
            cur_pos.set_key(cur_phns)
            pos_moves.append(m1, m2, (prev_pos, cur_pos), tier_keys[ii - 1].get_id(), ann.get_id())
        if cur_shape != prev_shape:
            (d1, d2) = self.__transitions.predict_d(rank=key_rank_ipu, is_nil_shape=self.has_nil_shape(cur_phns), is_nil_pos=self.has_nil_pos(cur_phns))
            shp_moves.append(d1, d2, (prev_shape, cur_shape), tier_keys[ii - 1].get_id(), ann.get_id())
        prev_shape = cur_shape
        prev_pos = cur_pos
        prev_phns = cur_phns
        key_rank_ipu += 1
    return (pos_moves, shp_moves)
```

*Return the predicted position transitions and shape transitions.*

The two returned lists contain:

- the estimated m1 and m2 values (in seconds), or d1 and d2;
- the transition position in a tuple with origin and target; and
- the origin/target annotation identifiers.

##### Parameters

- **tier_keys**: (sppasTier)
- **tier_segments**: (sppasTier) Tier with name 'CS-PhonSegments', phonemes of each key


##### Returns

- tuple(Pre*dict*edWhenHand, Pre*dict*edWhenHand)


##### Raises

sppasCuedRulesValueError

#### predicted_to_tier

```python
@staticmethod
def predicted_to_tier(predicted: PredictedWhenHand) -> sppasTier:
    """Turn the given values into sppasPoint.

        :param predicted: (PredictedWhenHand) Result of the prediction model.
        :return: (sppasTier) Predicted values turned into a sppasTier

        """
    tier = sppasTier('CS-Predicted')
    prev_end = sppasPoint(0.0)
    for i in range(len(predicted)):
        (start, end, tags, source_id, target_id) = predicted[i]
        if prev_end >= start:
            p1 = prev_end.copy()
        else:
            p1 = sppasPoint(start)
        next_start = None if i + 1 == len(predicted) else predicted[i + 1][0]
        radius = None
        if next_start is not None and end > next_start:
            radius = (end - next_start) / 2.0
            if end - radius > start:
                end = end - radius
            else:
                radius = (end - start) / 2.0
        p2 = sppasPoint(end, radius)
        if p2 > p1:
            p2 = sppasPoint(end)
        if p2 > p1:
            tier.create_annotation(sppasLocation(sppasInterval(p1, p2)), list(tags))
            tier.set_meta('from_id', source_id)
            tier.set_meta('to_id', target_id)
            prev_end = p2
        else:
            prev_end = p1
    return tier
```

*Turn the given values into sppasPoint.*

##### Parameters

- **predicted**: (Pre*dict*edWhenHand) Result of the prediction model.


##### Returns

- (sppasTier) Predicted values turned into a sppasTier



### Protected functions

#### __get_phones

```python
@staticmethod
def __get_phones(tier, interval) -> str:
    """Return the serialized best label of the tier in the given interval."""
    begin = interval.get_lowest_localization()
    end = interval.get_highest_localization()
    anns = tier.find(begin, end)
    if len(anns) > 0:
        return serialize_labels(anns[0].get_labels(), separator='-')
    return ''
```

*Return the serialized best label of the tier in the given interval.*





~ Created using [Clamming](https://clamming.sf.net) version 2.1 ~
