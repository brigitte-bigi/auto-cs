# CuedSpeech.whenhand.transition module

## List of classes

## Class `BaseWhenTransitionPredictor`

### Description

*Base class to predict hand transition moments [D1,D2] and [M1,M2].*

A Cued Speech key is defined as follows:

A1             A2             A3
| ---- C ----- | ----- V ---- |
| ---- C -------------------- |
| -------------------- V -----|

- A1 is the start time value of the first phoneme of the key;
- A3 is the end time value of the second phoneme of the key.

The system aims to predict both the interval [M1,M2], the moments the hand
is moving from its previous position to the one of the key, and interval
[D1,D2], the moments the fingers are changing from the previous shape to
the one of the key.

In this base class, no transition time values are estimated. The returned
intervals are [A1,A1] and [A1,A1]. It corresponds to the system presented
in (Bratakos et al., 1998):
"Appearance of the cue typically began at the frame corresponding to the
start of the consonant segment in the acoustic waveform and was maintained
until the end of the following vowel segment (for CV combinations) or of the
consonant segment (for consonants occurring alone)."

Reference is:
>Maroula S. Bratakos, Paul Duchnowski and Louis D. Braida
>Toward the Automatic Generation of Cued Speech
>Cued Speech Journal, vol. VI, pp 1-37, 1998.

##### Example

    >>> p = BaseWhenTransitionPredictor()
    >>> p.set_key_interval(2.3, 2.8)
    >>> p.a1
    > 2.3
    >>> p.a3
    > 2.8
    >>> m1, m2 = p.predict_position()
    >>> print(m1)
    > 2.3
    >>> print(m2)
    > 2.3
    >>> d1, d2 = p.predict_shape()
    >>> print(d1)
    > 2.3
    >>> print(d2)
    > 2.3
    >>> p.get_static_duration()      # a default key duration
    > 0.3

All given intervals [A1;A3] are stored until the reset method is invoked.
Their average value can be estimated with 'get_a1a3_avg_duration()' method.

##### Example

    >>> p = BaseWhenTransitionPredictor()
    >>> p.set_key_interval(2., 3.)   # duration is 1.
    >>> p.set_key_interval(3., 5.)   # duration is 2.
    >>> p.get_a1a3_avg_duration()    # average is 1.5
    > 1.5


### Constructor

#### __init__

```python
def __init__(self):
    """Instantiate a hand transition moment's predictor.

    """
    self._description = MSG_DESCRIPTION_BASE
    self.__a1 = None
    self.__a3 = None
    self.__avg = BaseWhenTransitionPredictor.DEFAULT_KEY_DURATION
    self.__dur = list()
```

*Instantiate a hand transition moment's predictor.*





### Public functions

#### get_key_interval

```python
def get_key_interval(self) -> tuple:
    """Return [A1;A3] the moments of the sounds of the last key.

        :return: tuple(a1,a3) if a1 and a3 are known or (0.,0.) if unknown

        """
    if self.__a1 is None:
        return (0.0, 0.0)
    return (self.__a1, self.__a3)
```

*Return [A1;A3] the moments of the sounds of the last key.*

##### Returns

- tuple(a1,a3) if a1 and a3 are known or (0.,0.) if unknown

#### set_key_interval

```python
def set_key_interval(self, a1: float, a3: float, store: bool=True) -> None:
    """Set [A1;A3] the moments of the sounds of the key.

        Given a1 value represents when the 1st phoneme of the key starts in
        the audio, and a3 represents when the 2nd phoneme of the key ends in
        the audio.

        :param a1: (float) Start time value of a key
        :param a3: (float) End time value of a key
        :param store: (bool) Store the a1 and a3 values into a list
        :raises: sppasTypeError: one of a1 or a3 is not a float
        :raises: RangeBoundsException: if a3 is lesser than a1

        """
    try:
        a1 = float(a1)
    except ValueError:
        raise sppasTypeError(type(a1), 'float')
    try:
        a3 = float(a3)
    except ValueError:
        raise sppasTypeError(type(a3), 'float')
    if a3 < a1:
        raise RangeBoundsException(a1, a3)
    self.__a1 = a1
    self.__a3 = a3
    if store is True:
        self.__dur.append(a3 - a1)
```

*Set [A1;A3] the moments of the sounds of the key.*

Given a1 value represents when the 1st phoneme of the key starts in
the audio, and a3 represents when the 2nd phoneme of the key ends in
the audio.

##### Parameters

- **a1**: (*float*) Start time value of a key
- **a3**: (*float*) End time value of a key
- **store**: (*bool*) Store the a1 and a3 values into a list


##### Raises

- *sppasTypeError*: one of a1 or a3 is not a float
- *RangeBoundsException*: if a3 is lesser than a1

#### reset_key_intervals

```python
def reset_key_intervals(self) -> None:
    """Forget the stored A1-A3 durations."""
    self.__dur = list()
```

*Forget the stored A1-A3 durations.*

#### get_a1

```python
def get_a1(self) -> float:
    """Return the lastly given A1 time value.

        :raises: ValueError: Unknown A1 value.

        """
    if self.__a1 is None:
        raise ValueError('Interval [A1;A3] un-defined. A1 un-defined.')
    return self.__a1
```

*Return the lastly given A1 time value.*

##### Raises

- *ValueError*: Unknown A1 value.

#### get_a3

```python
def get_a3(self) -> float:
    """Return the lastly given A3 time value.

        :raises: ValueError: Unknown A3 value.

        """
    if self.__a1 is None:
        raise ValueError('Interval [A1;A3] un-defined. A3 un-defined.')
    return self.__a3
```

*Return the lastly given A3 time value.*

##### Raises

- *ValueError*: Unknown A3 value.

#### get_static_duration

```python
def get_static_duration(self) -> float:
    """Return the duration of a key."""
    return self.__avg
```

*Return the duration of a key.*

#### set_static_duration

```python
def set_static_duration(self, duration: float) -> None:
    """Set the duration of a key.

        :param duration: (float) Fixed duration of a key.
        :raises: sppasTypeError: if given duration can't be a float.
        :raises: IntervalRangeException: if given duration is < 0.1 or > 1.0.

        """
    try:
        duration = float(duration)
    except ValueError:
        raise sppasTypeError(type(duration), 'float')
    if 0.1 <= duration <= 1.0:
        self.__avg = duration
    else:
        raise IntervalRangeException(duration, 0.1, 1.0)
```

*Set the duration of a key.*

##### Parameters

- **duration**: (*float*) Fixed duration of a key.


##### Raises

- *sppasTypeError*: if given duration can't be a float.
- *IntervalRangeException*: if given duration is < 0.1 or > 1.0.

#### get_a1a3_avg_duration

```python
def get_a1a3_avg_duration(self) -> float:
    """Return the average of stored [A1;A3] durations or the fixed one.

        :return: (float) Average value or if there's not enough known [A1;A3] durations, the fixed value is returned.

        """
    if len(self.__dur) < 2:
        return self.__avg
    elif len(self.__dur) < 3:
        return (sum(self.__dur) + self.__avg) / float(len(self.__dur) + 1)
    else:
        return sum(self.__dur) / float(len(self.__dur))
```

*Return the average of stored [A1;A3] durations or the fixed one.*

##### Returns

- (*float*) Average value or if there's not enough known [A1;A3] durations, the fixed value is returned.

#### get_description

```python
def get_description(self) -> str:
    """Return a brief description of the transition estimation method."""
    return self._description
```

*Return a brief description of the transition estimation method.*

#### predict_position

```python
def predict_position(self, **kwargs) -> tuple:
    """Predict [M1, M2] the moments when the hand is moving.

        Predict M1 - when leaving the current position
        Predict M2 - when arrived to the expected position

        :return: tuple(m1: float, m2: float)

        """
    if self.__a1 is None:
        raise ValueError('Interval [A1;A3] un-defined.')
    return (self.__a1, self.__a1)
```

*Predict [M1, M2] the moments when the hand is moving.*

Predict M1 - when leaving the current position
Predict M2 - when arrived to the expected position

##### Returns

- **tuple(m1**: float, m2: float)

#### predict_shape

```python
def predict_shape(self, **kwargs) -> tuple:
    """Predict [D1, D2] the moments when fingers are changing.

        Predict D1 - when fingers are starting to move
        Predict D2 - when fingers finished representing the expected shape

        :return: tuple(d1: float, d2: float)

        """
    if self.__a1 is None:
        raise ValueError('Interval [A1;A3] un-defined.')
    return (self.__a1, self.__a1)
```

*Predict [D1, D2] the moments when fingers are changing.*

Predict D1 - when fingers are starting to move
Predict D2 - when fingers finished representing the expected shape

##### Returns

- **tuple(d1**: float, d2: float)



## Class `WhenTransitionPredictorDuchnowski1998`

### Description

*Predict hand transition moments with (Duchnowski et al., 1998) method.*

> Paul Duchnowski, Louis D. Braida, David S. Lum, Matthew G. Sexton, Jean C. Krause, Smriti Banthia
> AUTOMATIC GENERATION OF CUED SPEECH FOR THE DEAF: STATUS AND OUTLOOK
> https://www.isca-speech.org/archive/pdfs/avsp_1998/duchnowski98_avsp.pdf

In section 2.2 of this paper:
"We found that cues are often formed before the corresponding sound is
produced. To approximate this effect we adjusted the start times of cues
to begin 100 ms before the boundary determined from acoustic data by the
cue recognizer."

Reference is:
> Paul Duchnowski, Louis Braida, Maroula Bratakos, David Lum, Matthew Sexton, Jean Krause
> A SPEECHREADING AID BASED ON PHONETIC ASR
> https://isca-speech.org/archive_v0/archive_papers/icslp_1998/i98_0589.pdf

In section 3.2 of this paper:
"We observed that human cuers often begin to form a cue before producing
the corresponding audible sound. To approximate this effect we adjusted
the start times of the cues to begin 100 ms before the boundary determined
by the cue recognizer."

In this class, no transition time values are estimated. The returned
intervals are [A1-0.1,A1-0.1] and [A1-0.1,A1-0.1].


### Constructor

#### __init__

```python
def __init__(self):
    """Instantiate (Duchnowski et al. 1998) hand transition moment's predictor.

    """
    super(WhenTransitionPredictorDuchnowski1998, self).__init__()
    self._description = MSG_DESCRIPTION_DUCHNOWSKI
```

*Instantiate (Duchnowski et al. 1998) hand transition moment's predictor.*





### Public functions

#### predict_position

```python
def predict_position(self, **kwargs) -> tuple:
    """Predict [M1,M2] the moments when the hand is moving.

        :return: (m1: float, m2: float)

        """
    m1 = max(0.0, self.a1 - 0.1)
    m2 = max(0.0, self.a1 - 0.1)
    return (m1, m2)
```

*Predict [M1,M2] the moments when the hand is moving.*

##### Returns

- **(m1**: float, m2: float)

#### predict_shape

```python
def predict_shape(self, **kwargs) -> tuple:
    """Predict [D1,D2] the moments when fingers are changing.

        :return: (d1: float, d2: float)

        """
    d1 = max(0.0, self.a1 - 0.1)
    d2 = max(0.0, self.a1 - 0.1)
    return (d1, d2)
```

*Predict [D1,D2] the moments when fingers are changing.*

##### Returns

- **(d1**: float, d2: float)



## Class `WhenTransitionPredictorDuchnowski2000`

### Description

*Predict hand transition moments with (Duchnowski et al., 2000) method.*

> Paul Duchnowski, David S. Lum, Jean C. Krause, Matthew G. Sexton,
> Maroula S. Bratakos, and Louis D. Braida
> Development of Speechreading Supplements Based in Automatic Speech Recognition
> IEEE Transactions on Biomedical Engineering, vol. 47, no. 4, pp. 487-496, 2000.
> doi: 10.1109/10.828148.

In section III.C (page 491) of this paper:
"The 'dynamic' display used heuristic rules to apportion cue display time
between time paused at target positions and time spent in transition
between these positions. Typically, 150 ms was allocated to the transition
provided the hand could pause at the target position for at least 100 ms.
The movement between target positions was, thus, smooth unless the cue was
short, in which case it would tend to resemble the original 'static'
display."

The 'static' system mentioned here is their previous system with no
transition duration described in (Duchnowski et al., 1998).


### Constructor

#### __init__

```python
def __init__(self):
    """Instantiate (Duchnowski et al. 2000) hand transition moment's predictor.

    """
    super(WhenTransitionPredictorDuchnowski2000, self).__init__()
    self._description = MSG_DESCRIPTION_DUCHNOWSKI
```

*Instantiate (Duchnowski et al. 2000) hand transition moment's predictor.*





### Public functions

#### predict_position

```python
def predict_position(self, **kwargs) -> tuple:
    """Predict [M1,M2] the moments when the hand is moving.

        :return: (m1: float, m2: float)

        """
    m1 = max(0.0, self.a1 - 0.25)
    m2 = max(0.0, self.a1 - 0.1)
    return (m1, m2)
```

*Predict [M1,M2] the moments when the hand is moving.*

##### Returns

- **(m1**: float, m2: float)

#### predict_shape

```python
def predict_shape(self, **kwargs) -> tuple:
    """Predict [D1,D2] the moments when fingers are changing.

        :return: (d1: float, d2: float)

        """
    d1 = max(0.0, self.a1 - 0.25)
    d2 = max(0.0, self.a1 - 0.1)
    return (d1, d2)
```

*Predict [D1,D2] the moments when fingers are changing.*

##### Returns

- **(d1**: float, d2: float)



## Class `WhenTransitionPredictorAttina`

### Description

*Predict hand transition moments with (Attina, 2005) method.*

> Virginie Attina Dubesset (2005)
> La langue française parlée complétée (LPC) : production et perception.
> PhD Thesis of INPG Grenoble, France.
> Page 117, page 136 and page 148
> https://tel.archives-ouvertes.fr/file/index/docid/384080/filename/these_attina.pdf

See page 112 (Experiment 1, no shape change, position changes, CV syllables):

- The average key duration is 399.5ms
- M1A1: mean duration is 239 ms (std is 87ms)  => 60%
- A1M2: mean duration is 37 ms (std is 76ms)   => 9%

See page 113 (Experiment 1, no shape change, position changes, V syllables):

- The average key duration is 383.6ms
- M1A1: mean duration is 183 ms (std is 79ms)  => 47%
- A1M2: mean duration is 84 ms (std is 64ms)   => 22%

Both results are summarized in the scheme page 117.

See page 118 (Experiment 2, shape changes, position doesn't), results page 123-124:

- The average CV key duration is 275ms
- D1A1: mean duration is 124 ms (std is 34ms)
- A1D2: mean duration is 46 ms (std is 35ms)

See page 119 (Experiment 2, both shape/position change), results page 124-

- The average CV key duration is 316.3ms
- D1A1: mean duration is 171 ms (std is 48ms)    => 54%
- A1D2: mean duration is -3 ms (std is 45ms)     => 0%
- M1A1: mean duration is 205 ms (std is 54.5ms)  => 65%
- A1M2: mean duration is 33 ms (std is 50ms)     => 10%

Both results are summarized in the scheme page 128.

A general synchronization scheme is proposed page 136 with percentages
instead of durations; and extended to 3 more speakers page 148.

The percentages implemented in this class are related to an average
key duration of 399.5ms (Experiment 1).


### Constructor

#### __init__

```python
def __init__(self):
    """Instantiate (Attina, 2005) hand transition moment's predictor.

    """
    super(WhenTransitionPredictorAttina, self).__init__()
    self._description = MSG_DESCRIPTION_ATTINA
    self.set_static_duration(0.4)
```

*Instantiate (Attina, 2005) hand transition moment's predictor.*





### Public functions

#### predict_position

```python
def predict_position(self, is_nil_shape: bool=False, **kwargs) -> tuple:
    """Predict [M1,M2] the moments when the hand is moving.

        To predict M2:
            - if CV key: both page 136 and page 117, M2 is 10% later than A1.
            - if -V key: page 117, M2 is 21% later than A1.
            - if C- key: no information. CV key case is used.

        To predict M1:
            - if CV key: page 136 M1 is 62-65% of A1A3, but page 117, M1 is 60% of A1A3
            - if -V key: page 117, M1 is 46% of A1A3
            - if C- key: no information. CV key case is used.

        :param is_nil_shape: (bool) True is the key is of the form "-V", i.e. no consonant
        :return: tuple(m1: float, m2: float)

        """
    a3a1 = self.get_a1a3_avg_duration()
    if is_nil_shape is False:
        a1m2 = a3a1 * 0.1
        m1a1 = a3a1 * 0.62
    else:
        a1m2 = a3a1 * 0.21
        m1a1 = a3a1 * 0.46
    m1 = max(0.0, self.a1 - m1a1)
    m2 = self.a1 + a1m2
    return (m1, m2)
```

*Predict [M1,M2] the moments when the hand is moving.*

To predict M2:
- if CV key: both page 136 and page 117, M2 is 10% later than A1.
- if -V key: page 117, M2 is 21% later than A1.
- if C- key: no information. CV key case is used.

To predict M1:
- if CV key: page 136 M1 is 62-65% of A1A3, but page 117, M1 is 60% of A1A3
- if -V key: page 117, M1 is 46% of A1A3
- if C- key: no information. CV key case is used.

##### Parameters

- **is_nil_shape**: (*bool*) True is the key is of the form "-V", i.e. no consonant


##### Returns

- **tuple(m1**: float, m2: float)

#### predict_shape

```python
def predict_shape(self, is_nil_shape: bool=False, **kwargs) -> tuple:
    """Predict [D1,D2] the moments when fingers are changing.

        D1 and D2 are predicted from the key duration only. Following the
        model proposed page 136:

        - D2 is right before A1 (1%).
        - Estimating D1D2 interval, which is 55% of A3A1, gives D1 position
          related to D2.

        :return: (d1: float, d2: float)

        """
    a3a1 = self.get_a1a3_avg_duration()
    if is_nil_shape is False:
        d2d1 = a3a1 * 0.54
    else:
        d2d1 = a3a1 * 0.36
    d1 = max(0.0, self.a1 - d2d1)
    d2 = self.a1
    return (d1, d2)
```

*Predict [D1,D2] the moments when fingers are changing.*

D1 and D2 are predicted from the key duration only. Following the
model proposed page 136:

- D2 is right before A1 (1%).
- Estimating D1D2 interval, which is 55% of A3A1, gives D1 position
related to D2.

##### Returns

- **(d1**: float, d2: float)



## Class `WhenTransitionPredictorRules`

### Description

*Predict hand transition moments with a rule-based system.*

It is inspired from the synchronization model in Attina (2005) and the
automatic system in (Duchnowski et al. 2000).
It is also inspired by (Bratakos et al., 1998): "A critical delay
to display the hand cue is +165ms. The max delay is +100ms.
A non-significant delay is +33ms.":

> Maroula S. Bratakos, Paul Duchnowski and Louis D. Braida
> Toward the Automatic Generation of Cued Speech
> Cued Speech Journal VI 1998 p1-37.
> (c) 1998 National Cued Speech Association, Inc.

The system implements the following rules to estimate [M1;M2]:
- Like (Duchnowski et al. 1998), the structure of the key does not matter.
- M2 is before A1, like in (Duchnowski et al. 1998) but not that much
- The position transition of the first key after a silence (from neutral)
is very early before the sound. The 2nd key of a speech segment
is also proportionally earlier than the next ones. See predict_pos_generic().
- The position transition from the last key of a speech segment to the
neutral one (to a long silence), is delayed. See predict_pos_to_neutral().
- They are estimated proportionally to the average duration of *observed*
A1A3 intervals.


### Constructor

#### __init__

```python
def __init__(self):
    """Instantiate a custom hand transition moment's predictor.

    """
    super(WhenTransitionPredictorRules, self).__init__()
    self._description = MSG_DESCRIPTION_RULES
```

*Instantiate a custom hand transition moment's predictor.*





### Public functions

#### predict_position

```python
def predict_position(self, rank: int=4, **kwargs) -> tuple:
    """Predict [M1;M2] the moments when the hand is moving.

        :param rank: (int) The rank of the key. 0=silence, 1=1st key after a silence, etc.
        :return: (m1: float, m2: float)

        """
    if rank == 0:
        return self._predict_pos_to_neutral()
    (m1, m2) = self._predict_pos_generic(rank)
    m2 = min(m2, self.a3)
    m1 = min(m1, m2)
    return (m1, m2)
```

*Predict [M1;M2] the moments when the hand is moving.*

##### Parameters

- **rank**: (*int*) The rank of the key. 0=silence, 1=1st key after a silence, etc.


##### Returns

- **(m1**: float, m2: float)

#### predict_shape

```python
def predict_shape(self, rank: int=3, **kwargs) -> tuple:
    """Predict [D1;D2] the moments when fingers are changing.

        It is considered but not proved that:

        - D1 is after M1; and
        - D2 is before M2;
        - [D1;D2] is a relative fast change and must occur asap.

        SPPAS 4.22, which was evaluated at ALPC 2024, was:
            - d2a1 = a3a1 * 0.4
             - d1a1 =
             if rank == 1: d1a1 = max(0.500, a3a1 * 1.25)
             if rank == 2: d1a1 = max(0.250, a3a1)
             else: d1a1 = a3a1 * 0.7

        :param rank: (int) The rank of the key. 0=silence, 1=1st key after a silence, etc.
        :return: (d1: float, d2: float)

        """
    a3a1 = self.get_a1a3_avg_duration()
    if rank == 0:
        return self._predict_shp_to_neutral()
    elif rank == 1:
        d1a1 = max(0.45, a3a1 * 1.1)
        d2a1 = a3a1 * 0.8
    elif rank == 2:
        d1a1 = max(0.3, a3a1 * 0.95)
        d2a1 = a3a1 * 0.65
    elif rank == 3:
        d1a1 = max(0.2, a3a1 * 0.8)
        d2a1 = a3a1 * 0.5
    else:
        d1a1 = a3a1 * 0.7
        d2a1 = a3a1 * 0.4
    d1 = max(0.0, self.a1 - d1a1)
    d2 = max(d1, self.a1 - d2a1)
    return (d1, d2)
```

*Predict [D1;D2] the moments when fingers are changing.*

It is considered but not proved that:

- D1 is after M1; and
- D2 is before M2;
- [D1;D2] is a relative fast change and must occur asap.

SPPAS 4.22, which was evaluated at ALPC 2024, was:
- d2a1 = a3a1 * 0.4
- d1a1 =
if rank == 1: d1a1 = max(0.500, a3a1 * 1.25)
if rank == 2: d1a1 = max(0.250, a3a1)
else: d1a1 = a3a1 * 0.7

##### Parameters

- **rank**: (*int*) The rank of the key. 0=silence, 1=1st key after a silence, etc.


##### Returns

- **(d1**: float, d2: float)



### Private functions

#### _predict_pos_to_neutral

```python
def _predict_pos_to_neutral(self) -> tuple:
    """Predict [M1;M2] for a destination key NN.

        [A1;A3] is a silence, so the transition is from a previous sounded key
        (CV, -V or C-) to the neutral one. This transition is delayed compared
        to the other ones.

        :return: tuple(float, float)

        """
    a3a1 = self.get_static_duration()
    m1 = self.a1 + a3a1 * 0.2
    m2 = m1 + a3a1 * 0.8
    return (m1, m2)
```

*Predict [M1;M2] for a destination key NN.*

[A1;A3] is a silence, so the transition is from a previous sounded key
(CV, -V or C-) to the neutral one. This transition is delayed compared
to the other ones.

##### Returns

- tuple(*float*, *float*)

#### _predict_pos_generic

```python
def _predict_pos_generic(self, rank: int=3) -> tuple:
    """Predict [M1;M2] for a destination key CV or C-.

        SPPAS 4.22, which was evaluated at ALPC 2024, was:
            - m2a1 = a3a1 * 0.05
            - m1a1 =
                if rank == 1: m1a1 = max(0.500, a3a1 * 1.25)
                if rank == 2: m1a1 = max(0.250, a3a1)
                else: a3a1 * 0.9

        m2a1 is a compromise value between the 100ms before a1 of (Duchnowski
        et al., 2000), and the 10% after a1 of (Attina, 2005).

        :param rank: (int) Rank of the key into the speech segment
        :return: tuple(float, float)

        """
    a3a1 = self.get_a1a3_avg_duration()
    if rank == 1:
        m1a1 = max(0.5, a3a1 * 1.4)
        m2a1 = min(0.15, a3a1 * 0.2)
    elif rank == 2:
        m1a1 = max(0.35, a3a1 * 1.15)
        m2a1 = min(0.15, a3a1 * 0.15)
    elif rank == 3:
        m1a1 = max(0.25, a3a1)
        m2a1 = min(0.1, a3a1 * 0.1)
    else:
        m1a1 = a3a1 * 0.9
        m2a1 = a3a1 * 0.05
    m1 = max(0.0, self.a1 - m1a1)
    m2 = max(m1, self.a1 - m2a1)
    return (m1, m2)
```

*Predict [M1;M2] for a destination key CV or C-.*

SPPAS 4.22, which was evaluated at ALPC 2024, was:
- m2a1 = a3a1 * 0.05
- m1a1 =
if rank == 1: m1a1 = max(0.500, a3a1 * 1.25)
if rank == 2: m1a1 = max(0.250, a3a1)
else: a3a1 * 0.9

m2a1 is a compromise value between the 100ms before a1 of (Duchnowski
et al., 2000), and the 10% after a1 of (Attina, 2005).

##### Parameters

- **rank**: (*int*) Rank of the key into the speech segment


##### Returns

- tuple(*float*, *float*)

#### _predict_shp_to_neutral

```python
def _predict_shp_to_neutral(self) -> tuple:
    """Predict [D1;D2] for a destination key NN.

        [A1;A3] is a silence, so the transition is from a previous sounded key
        (CV, -V or C-) to the neutral one.

        :return: tuple(float, float)

        """
    a3a1 = self.get_static_duration()
    d1 = self.a1 + a3a1 * 0.3
    d2 = d1 + a3a1 * 0.4
    return (d1, d2)
```

*Predict [D1;D2] for a destination key NN.*

[A1;A3] is a silence, so the transition is from a previous sounded key
(CV, -V or C-) to the neutral one.

##### Returns

- tuple(*float*, *float*)



## Class `WhenTransitionPredictorRevisedRules`

### Description

*Predict hand transition moments with a revised rule-based system.*

The system implements the following rules to estimate [M1;M2]:
- The structure of the key matters.
- M2 is before A1, like in (Duchnowski et al. 1998) but not that much
- The position transition of the first key after a silence (from neutral)
is very early before the sound. The M2 of the 2nd key of a speech segment
is also earlier than the next ones.
- The position transition from the last key of a speech segment to the
neutral one (to a long silence), is delayed. See predict_pos_to_neutral().
- They are estimated proportionally to the average duration of *observed*
A1A3 intervals.


### Constructor

#### __init__

```python
def __init__(self):
    """Instantiate a custom hand transition moment's predictor.

    """
    super(WhenTransitionPredictorRevisedRules, self).__init__()
    self._description = MSG_DESCRIPTION_RULES
```

*Instantiate a custom hand transition moment's predictor.*





### Public functions

#### predict_position

```python
def predict_position(self, rank: int=4, **kwargs) -> tuple:
    """Predict [M1;M2] the moments when the hand is moving.

        :param rank: (int) The rank of the key. 0=silence, 1=1st key after a silence, etc.
        :return: (m1: float, m2: float)

        """
    rank = int(rank)
    if rank == 0:
        return self._predict_pos_to_neutral()
    if rank == 1:
        return self._predict_pos_from_neutral()
    (m1, m2) = self._predict_pos_generic(rank, **kwargs)
    m2 = min(m2, self.a3)
    m1 = min(m1, m2)
    return (m1, m2)
```

*Predict [M1;M2] the moments when the hand is moving.*

##### Parameters

- **rank**: (*int*) The rank of the key. 0=silence, 1=1st key after a silence, etc.


##### Returns

- **(m1**: float, m2: float)

#### predict_shape

```python
def predict_shape(self, rank: int=3, is_nil_shape: bool=False, is_nil_pos: bool=False, **kwargs) -> tuple:
    """Predict [D1;D2] the moments when fingers are changing.

        It is considered but not proved that:

        - D1 is after M1; and
        - D2 is before M2;
        - [D1;D2] is a relative fast change and must occur asap.

        :param rank: (int) The rank of the key. 0=silence, 1=1st key after a silence, etc.
        :param is_nil_shape: (bool) True is the key is of the form "-V", i.e. no consonant
        :param is_nil_pos: (bool) True is the key is of the form "C-", i.e. no vowel
        :return: (d1: float, d2: float)

        """
    if rank == 0:
        return self._predict_shp_to_neutral()
    elif rank == 1:
        return self._predict_shp_from_neutral()
    else:
        a3a1 = self.get_a1a3_avg_duration()
        if is_nil_pos is True:
            d1a1 = a3a1 * 1.15
            d2a1 = a3a1 * -0.55
        elif is_nil_shape is True:
            d1a1 = max(0.4, a3a1 * 1.8)
            d2a1 = a3a1 * -1.2
        elif rank == 2:
            d1a1 = a3a1 * 0.8
            d2a1 = a3a1 * -0.6
        else:
            d1a1 = a3a1 * 0.65
            d2a1 = a3a1 * -0.4
        d1 = max(0.0, self.a1 - d1a1)
        d2 = max(d1, self.a1 + d2a1)
        return (d1, d2)
```

*Predict [D1;D2] the moments when fingers are changing.*

It is considered but not proved that:

- D1 is after M1; and
- D2 is before M2;
- [D1;D2] is a relative fast change and must occur asap.

##### Parameters

- **rank**: (*int*) The rank of the key. 0=silence, 1=1st key after a silence, etc.
- **is_nil_shape**: (*bool*) True is the key is of the form "-V", i.e. no consonant
- **is_nil_pos**: (*bool*) True is the key is of the form "C-", i.e. no vowel


##### Returns

- **(d1**: float, d2: float)



### Private functions

#### _predict_pos_to_neutral

```python
def _predict_pos_to_neutral(self) -> tuple:
    """Predict [M1;M2] for a destination key NN.

        This transition is delayed compared to the other ones.

        :return: tuple(float, float)

        """
    a3a1 = self.get_static_duration()
    m1a1 = a3a1 * 0.1
    m2a1 = a3a1 * 1.25
    m1 = max(0.0, self.a1 - m1a1)
    m2 = max(m1, self.a1 + m2a1)
    return (m1, m2)
```

*Predict [M1;M2] for a destination key NN.*

This transition is delayed compared to the other ones.

##### Returns

- tuple(*float*, *float*)

#### _predict_pos_from_neutral

```python
def _predict_pos_from_neutral(self) -> tuple:
    """Predict [M1;M2] from a silence to the first key on the face.

        This transition is anticipated compared to the other ones.

        :return: tuple(float, float)

        """
    a3a1 = self.get_a1a3_avg_duration()
    m1a1 = max(0.6, a3a1 * 1.6)
    m2a1 = min(0.15, a3a1 * 0.1)
    m1 = max(0.0, self.a1 - m1a1)
    m2 = max(m1, self.a1 - m2a1)
    return (m1, m2)
```

*Predict [M1;M2] from a silence to the first key on the face.*

This transition is anticipated compared to the other ones.

##### Returns

- tuple(*float*, *float*)

#### _predict_pos_generic

```python
def _predict_pos_generic(self, rank: int=3, is_nil_shape: bool=False, is_nil_pos: bool=False, **kwargs) -> tuple:
    """Predict [M1;M2] for a destination key 'C', 'V' or 'CV'.

        Prediction algorithm is as follows:
        >    if 'C':
        >         m1 = a1 - (a3a1 * 1.60)
        >         m2 = a1 - (a3a1 * 0.30)
        >     elif 'V':
        >         m1 = a1 - (a3a1 * 2.40)
        >         m2 = a1 - (a3a1 * 0.60)
        >     else:
        >         m1 = a1 - (a3a1 * 0.80)
        >         if 2nd_key:
        >             m2 = a1
        >         else
        >             m2 = a1 + (a3a1 * 0.11)

        :param rank: (int) Rank of the key into the speech segment
        :param is_nil_shape: (bool) True is the key is of the form "-V", i.e. no consonant
        :param is_nil_pos: (bool) True is the key is of the form "C-", i.e. no vowel
        :raises: ValueError: invalid rank. It must be > 1.
        :return: tuple(float, float)

        """
    if all((is_nil_shape, is_nil_pos)) is True:
        raise ValueError("For the generic prediction, nil_shape and nil_pos can't be both True together.")
    if rank < 2:
        raise ValueError('For the generic prediction, rank must be >= 2.')
    a3a1 = self.get_a1a3_avg_duration()
    if is_nil_pos is True:
        m1a1 = max(0.5, a3a1 * 1.6)
        m2a1 = a3a1 * -0.3
    elif is_nil_shape is True:
        m1a1 = max(0.6, a3a1 * 2.4)
        m2a1 = a3a1 * -0.6
    else:
        m1a1 = max(0.35, a3a1 * 0.8)
        if rank == 2:
            m2a1 = 0.0
        else:
            m2a1 = a3a1 * 0.11
    m1 = max(0.0, self.a1 - m1a1)
    m2 = max(m1, self.a1 + m2a1)
    return (m1, m2)
```

*Predict [M1;M2] for a destination key 'C', 'V' or 'CV'.*

Prediction algorithm is as follows:
>    if 'C':
>         m1 = a1 - (a3a1 * 1.60)
>         m2 = a1 - (a3a1 * 0.30)
>     elif 'V':
>         m1 = a1 - (a3a1 * 2.40)
>         m2 = a1 - (a3a1 * 0.60)
>     else:
>         m1 = a1 - (a3a1 * 0.80)
>         if 2nd_key:
>             m2 = a1
>         else
>             m2 = a1 + (a3a1 * 0.11)

##### Parameters

- **rank**: (*int*) Rank of the key into the speech segment
- **is_nil_shape**: (*bool*) True is the key is of the form "-V", i.e. no consonant
- **is_nil_pos**: (*bool*) True is the key is of the form "C-", i.e. no vowel


##### Raises

- *ValueError*: invalid rank. It must be > 1.


##### Returns

- tuple(*float*, *float*)

#### _predict_shp_to_neutral

```python
def _predict_shp_to_neutral(self) -> tuple:
    """Predict [D1;D2] for a destination key NN.

        [A1;A3] is a silence, so the transition is from a previous sounded key
        (CV, -V or C-) to the neutral one.

        :return: tuple(float, float)

        """
    a3a1 = self.get_static_duration()
    d1 = self.a1 + a3a1 * 0.4
    d2 = self.a1 + a3a1 * 0.7
    return (d1, d2)
```

*Predict [D1;D2] for a destination key NN.*

[A1;A3] is a silence, so the transition is from a previous sounded key
(CV, -V or C-) to the neutral one.

##### Returns

- tuple(*float*, *float*)

#### _predict_shp_from_neutral

```python
def _predict_shp_from_neutral(self) -> tuple:
    """Predict [D1;D2] from a key NN to a facial one.

        :return: tuple(float, float)

        """
    a3a1 = self.get_a1a3_avg_duration()
    d1a1 = a3a1 * 1.3
    d2a1 = a3a1 * 0.9
    d1 = max(0.0, self.a1 - d1a1)
    d2 = max(d1, self.a1 - d2a1)
    return (d1, d2)
```

*Predict [D1;D2] from a key NN to a facial one.*

##### Returns

- tuple(*float*, *float*)





~ Created using [Clamming](https://clamming.sf.net) version 2.1 ~
