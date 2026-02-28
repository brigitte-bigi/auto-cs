# CuedSpeech.whowtag.whowimgtag module

## List of classes

## Class `sppasHandCoords`

### Description

*Estimate the coordinates of the S0 and S9 points of the hand.*

This class estimates the coordinates of the S0 and S9 hand points,
enabling precise placement of the hand in an image based on:

- the (x, y) coordinates of the target position,
- a list of tuples specifying shape code(s) and their probabilities,
- the angle to apply to the S0–S9 axis,
- the face size in pixels.

Example input values when the hand shape is neutral (shape "0"):

- target: (447, 864)
- shapes: [('0', 1.0)]
- vowel_angle: 45
- face_height: 259

Example return value:
[(426, 682, 'target'), (346, 831, 'sights_00'), (409, 733, 'sights_09')]

Example input values for a shape transition from neutral to shape "3":

- target: (426, 682)
- shapes: [('3', 0.320), ('0', 0.680)]
- vowel_angle: 57
- face_height: 260

Example return value:
[(426, 682, 'target'), (346, 831, 'sights_00'), (409, 733, 'sights_09')]


### Constructor

#### __init__

```python
def __init__(self, cue_rules: CuedSpeechCueingRules=CuedSpeechCueingRules(), img_hand_tagger=None):
    """Create a new instance.

    :param cue_rules: (CuedSpeechKeys) Rules and codes for vowel positions and hand shapes

    """
    self.__cued = None
    self._vrank = ()
    self.__hand_tagger = None
    self.set_hand_tagger(img_hand_tagger)
    self.set_cue_rules(cue_rules)
```

*Create a new instance.*

##### Parameters

- **cue_rules**: (CuedSpeechKeys) Rules and codes for vowel positions and hand shapes



### Public functions

#### set_cue_rules

```python
def set_cue_rules(self, cue_rules: CuedSpeechCueingRules) -> None:
    """Set new rules.

        :param cue_rules: (CuedSpeechCueingRules) Rules and codes for vowel positions and hand shapes

        """
    if isinstance(cue_rules, CuedSpeechCueingRules) is False:
        raise sppasTypeError(str(type(cue_rules)), 'CuedSpeechCueingRules')
    self.__cued = cue_rules
    self._vrank = tuple(self.__cued.get_vowels_codes())
```

*Set new rules.*

##### Parameters

- **cue_rules**: (CuedSpeechCueingRules) Rules and codes for vowel positions and hand shapes

#### get_vowel_rank

```python
def get_vowel_rank(self, vowel_code):
    """Return an index from the code of a vowel or -1.

        :param vowel_code: (char) One of n, b, c, s, m, t for French.

        """
    if vowel_code in self._vrank:
        return self._vrank.index(vowel_code)
    return -1
```

*Return an index from the code of a vowel or -1.*

##### Parameters

- **vowel_code**: (char) One of n, b, c, s, m, t for French.

#### set_hand_tagger

```python
def set_hand_tagger(self, hand_tagger) -> None:
    """Set the hand tagger or None.

        :param hand_tagger: (sppasImageHandTagger) Allows to get hand sights of the choose handset

        """
    if hand_tagger is None:
        self.__hand_tagger = None
    elif hasattr(hand_tagger, 'slap_on') is True:
        self.__hand_tagger = hand_tagger
    else:
        raise sppasTypeError(str(type(hand_tagger)), 'sppasImageHandTagger')
```

*Set the hand tagger or None.*

##### Parameters

- **hand_tagger**: (sppasImageHandTagger) Allows to get hand sights of the choose handset

#### eval_hand_points

```python
def eval_hand_points(self, target, shapes, vowel_angle, face_height):
    """A solution to return hand coords from target, angle and face height.

        It allows to fix where to place the hand, i.e., S0 and S9 coordinates,
        in an image based on:

        :param target: (tuple) x,y coordinates of the targeted position
        :param shapes: (list) List of tuples describing the shape and its probability
        :param vowel_angle: (float) Angle to be applied to S0-S9 axes
        :param face_height: (int) Size of the face, in pixels
        :return: (list) [target, S0, S9] with coordinates of hand points

        The returned list contains sppasLabel() instances with:

        - sppasFuzzyPoint() to store the coordinates of hand points
        - label key to indicate its definition ('target' or 'sights_00' or 'sights_09')

        """
    names = ['sights_00', 'sights_09']
    hand_pts = [self.__create_label(target[0], target[1], 'target')]
    try:
        if len(shapes) == 1:
            _pts = self.target_to_hand_sights(shapes[0][0], target, vowel_angle, face_height)
            if None not in _pts:
                hand_pts.append(self.__create_label(_pts[0][0], _pts[0][1], names[0]))
                hand_pts.append(self.__create_label(_pts[1][0], _pts[1][1], names[1]))
        else:
            _pts1 = self.target_to_hand_sights(shapes[0][0], target, vowel_angle, face_height)
            _pts2 = self.target_to_hand_sights(shapes[1][0], target, vowel_angle, face_height)
            if None not in _pts1 and None not in _pts2:
                for (i, pt1) in enumerate(_pts1):
                    pt2 = _pts2[i]
                    proba1 = shapes[0][1]
                    proba2 = shapes[1][1]
                    p_x = int(proba1 * pt1[0] + proba2 * pt2[0])
                    p_y = int(proba1 * pt1[1] + proba2 * pt2[1])
                    hand_pts.append(self.__create_label(p_x, p_y, names[i]))
        return hand_pts
    except:
        import traceback
        print(traceback.format_exc())
        return list()
```

*A solution to return hand coords from target, angle and face height.*

It allows to fix where to place the hand, i.e., S0 and S9 coordinates,
in an image based on:

##### Parameters

- **target**: (*tuple*) x,y coordinates of the targeted position
- **shapes**: (*list*) List of tuples describing the shape and its probability
- **vowel_angle**: (*float*) Angle to be applied to S0-S9 axes
- **face_height**: (*int*) Size of the face, in pixels


##### Returns

- (*list*) [target, S0, S9] with coordinates of hand points

The returned list contains sppasLabel() instances with:

- sppasFuzzyPoint() to store the coordinates of hand points
- label key to indicate its definition ('target' or 'sights_00' or 'sights_09')

#### angle_to_s0

```python
def angle_to_s0(self, shape_code: str, sight_index: int=0) -> int:
    """Return the angle of the given sight compared to S0-S9 axis.

        :param shape_code: (str) Hand shape vowel code
        :param sight_index: (int) The index of the sight
        :return: (int) the computed angle
        :raises: IntervalRangeException: If the index is negative or out of bounds

        """
    if self.__hand_tagger is None:
        if shape_code == '0':
            return 30
        else:
            return 0
    else:
        return self.__hand_tagger.angle_to_s0(shape_code, sight_index)
```

*Return the angle of the given sight compared to S0-S9 axis.*

##### Parameters

- **shape_code**: (*str*) Hand shape vowel code
- **sight_index**: (*int*) The index of the sight


##### Returns

- (*int*) the computed angle


##### Raises

- *IntervalRangeException*: If the index is negative or out of bounds

#### distance_to_s0

```python
def distance_to_s0(self, shape_code: str, sight_index: int=0) -> int:
    """Get the distance between s0 and a sight of the hand.

        :param shape_code: (str) Shape code name
        :param sight_index: (int) The index of the sight
        :raises: IntervalRangeException: If the index is negative or out of bounds
        :return: (int) the computed distance

        """
    if self.__hand_tagger is None:
        if sight_index == 9:
            return 71
        elif sight_index == 12:
            return 172
        elif sight_index == 5:
            return 73
        elif sight_index == 8:
            return 165
        else:
            return 0
    return self.__hand_tagger.distance_to_s0(shape_code, sight_index)
```

*Get the distance between s0 and a sight of the hand.*

##### Parameters

- **shape_code**: (*str*) Shape code name
- **sight_index**: (*int*) The index of the sight


##### Raises

- *IntervalRangeException*: If the index is negative or out of bounds


##### Returns

- (*int*) the computed distance

#### target_to_hand_sights

```python
def target_to_hand_sights(self, shape_code, target, angle, face_height):
    """Estimate coordinates of S0 and S9 sights of the hand.

        The given angle is the one between the target and the S0 sight
        relatively to the vertical axis.

        :param shape_code: (char) Consonant shape name. If unknown, '0' is used instead.
        :param target: (tuple(x,y))
        :param angle: (int) Value between -360 and 360 in the unit circle
        :param face_height: (int) Height of the face
        :return: tuple(x0, y0), tuple(x9, y9) or (None, None) if error in distance estimation

        Target(x,y)
        *-------------------A'(x0,y)
        |  \\ alpha          |
        |      \\            |
        |         \\         |
        |            \\sigma |
        |               \\   |
       A(x,y0)-----------S(x0,y0)

        alpha = angle - 90
        hypotenuse = [TS] ; adjacent = [AS] ; opposite = [AT]

        sinus(any_angle) = opposite / hypotenuse
        sinus(ATS) = AS / TS    = >  AS = sin(sigma) * TS    = >  y0 = y + sin(sigma) * hypotenuse
        sinus(AST) = AT / TS    = >  AT = sin(alpha) * TS    = >  x0 = x + sin(alpha) * hypotenuse

        """
    ref_dist = self.distance_to_s0(shape_code, 9)
    if int(round(ref_dist, 0)) == 0:
        logging.error("Distance between S0 and S9 is 0. It probably means there's a problem in hand sights.")
        return (None, None)
    ratio = face_height * 0.45 / ref_dist
    alpha = angle - 90
    target_index = self.__cued.get_shape_target(shape_code)
    alpha = alpha - self.angle_to_s0(shape_code, target_index)
    dist = self.distance_to_s0(shape_code, target_index)
    hypotenuse = dist * ratio
    sigma = 90 - alpha
    x_s0 = target[0] + int(self.sinus(alpha) * hypotenuse)
    y_s0 = target[1] + int(self.sinus(sigma) * hypotenuse)
    hypotenuse = ref_dist * ratio
    alpha = angle - 90
    sigma = 90 - alpha
    x_s9 = x_s0 - int(self.sinus(alpha) * hypotenuse)
    y_s9 = y_s0 - int(self.sinus(sigma) * hypotenuse)
    return ((x_s0, y_s0), (x_s9, y_s9))
```

*Estimate coordinates of S0 and S9 sights of the hand.*

The given angle is the one between the target and the S0 sight
relatively to the vertical axis.

##### Parameters

- **shape_code**: (char) Consonant shape name. If unknown, '0' is used instead.
- **target**: (*tuple*(x,y))
- **angle**: (*int*) Value between -360 and 360 in the unit circle
- **face_height**: (*int*) Height of the face


##### Returns

- tuple(x0, y0), tuple(x9, y9) or (None, None) if error in distance estimation

Target(x,y)
*-------------------A'(x0,y)
|  \ alpha          |
|      \            |
|         \         |
|            \sigma |
|               \   |
A(x,y0)-----------S(x0,y0)

alpha = angle - 90
hypotenuse = [TS] ; adjacent = [AS] ; opposite = [AT]

sinus(any_angle) = opposite / hypotenuse
sinus(ATS) = AS / TS    = >  AS = sin(sigma) * TS    = >  y0 = y + sin(sigma) * hypotenuse
sinus(AST) = AT / TS    = >  AT = sin(alpha) * TS    = >  x0 = x + sin(alpha) * hypotenuse



#### sinus

```python
@staticmethod
def sinus(degree):
    """Return sinus value of the given degree.

        To find the sine of degrees, it must first be converted into radians
        with the math.radians() method.

        :param degree: (int, float) A degree value
        :return: Sine value in degrees.

        """
    degree = float(degree) % 360.0
    return math.sin(math.radians(degree))
```

*Return sinus value of the given degree.*

To find the sine of degrees, it must first be converted into radians
with the math.radians() method.

##### Parameters

- **degree**: (*int*, *float*) A degree value


##### Returns

- Sine value in degrees.



### Protected functions

#### __create_label

```python
def __create_label(self, x, y, s):
    tag = sppasTag((x, y), tag_type='point')
    label = sppasLabel(tag)
    label.set_key(s)
    return label
```





## Class `sppasImageVowelPosTagger`

### Constructor

#### __init__

```python
def __init__(self, *args, **kwargs):
    raise sppasEnableFeatureError('video')
```





## Class `sppasImageHandTagger`

### Constructor

#### __init__

```python
def __init__(self, *args, **kwargs):
    raise sppasEnableFeatureError('video')
```







~ Created using [Clamming](https://clamming.sf.net) version 2.1 ~
