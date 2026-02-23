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

### Description

*Tag the image of vowel positions with colored circles.*




### Constructor

#### __init__

```python
def __init__(self, cue_rules: CuedSpeechKeys=CuedSpeechKeys()):
    """The constructor of the SppasImageVowelsTagger class.

    :param cue_rules: (CuedSpeechKeys) Rules and codes for vowel positions and hand shapes
    :raises: sppasTypeError: If the parameter are not an instance of CuedSpeechKeys class

    """
    if not isinstance(cue_rules, CuedSpeechKeys):
        raise sppasTypeError(cue_rules, 'CuedSpeechKeys')
    self.__cued = cue_rules
    self.__colors = dict()
    self.__colors['b'] = [128, 0, 200, 0, 180, 100, 50, 100]
    self.__colors['g'] = [128, 120, 100, 80, 0, 0, 170, 220]
    self.__colors['r'] = [128, 0, 0, 160, 80, 180, 50, 100]
    self.__vowel_name_option = False
    self.__thickness = 2
```

*The constructor of the SppasImageVowelsTagger class.*

##### Parameters

- **cue_rules**: (CuedSpeechKeys) Rules and codes for vowel positions and hand shapes


##### Raises

- *sppasTypeError*: If the parameter are not an instance of CuedSpeechKeys class



### Public functions

#### set_cue_rules

```python
def set_cue_rules(self, cue_rules: CuedSpeechKeys):
    """Set the CuedSpeechKeys used to tag the video.

        :param cue_rules: (CuedSpeechKeys) The instance of the cuedSpeechKeys to set

        """
    self.__cued = cue_rules
```

*Set the CuedSpeechKeys used to tag the video.*

##### Parameters

- **cue_rules**: (CuedSpeechKeys) The instance of the cuedSpeechKeys to set

#### get_vowel_text

```python
def get_vowel_text(self, vowel_index: int) -> str:
    """Return the text code for the given vowel index.

        :param vowel_index: (int) The vowel rank
        :return: (str) The text code associated with the given index, or empty string if the index is wrong

        """
    vowels_code = self.__cued.get_vowels_codes()
    if 0 <= vowel_index < len(vowels_code):
        return vowels_code[vowel_index]
    return ''
```

*Return the text code for the given vowel index.*

##### Parameters

- **vowel_index**: (*int*) The vowel rank


##### Returns

- (*str*) The text code associated with the given index, or empty string if the index is wrong

#### get_vowel_color

```python
def get_vowel_color(self, color_index: int) -> tuple:
    """Return the color for the given vowel index.

        :param color_index: (int) The vowel rank
        :return: (tuple) The bgr color of the vowel associated with the given index
                 If we have a wrong index the method return (128, 128, 128) bgr color by default

        """
    bgr_color = (128, 128, 128)
    if 0 <= color_index < len(self.__colors['r']):
        r = self.__colors['r'][color_index]
        g = self.__colors['g'][color_index]
        b = self.__colors['b'][color_index]
        bgr_color = (b, g, r)
    return bgr_color
```

*Return the color for the given vowel index.*

##### Parameters

- **color_index**: (*int*) The vowel rank


##### Returns

- (*tuple*) The bgr color of the vowel associated with the given index If we have a wrong index the method return (128, 128, 128) bgr color by default

#### enable_vowel_name

```python
def enable_vowel_name(self, value: bool=True) -> None:
    """Set the option to tag the name of each vowel in its circle.

        :param value: (bool) Boolean value representing if the option "tag name" is activated or not
                      Optional parameter, value = True by default

        """
    self.__vowel_name_option = value
```

*Set the option to tag the name of each vowel in its circle.*

##### Parameters

- **value**: (*bool*) Boolean value representing if the option "tag name" is activated or not Optional parameter, value = True by default

#### set_thickness

```python
def set_thickness(self, value: int=1) -> None:
    """Set the thickness of the pen to draw the text into vowel circles.

        :param value: (int) The thickness value
                      Optional parameter, value = 1 by default

        """
    if value < 1:
        value = 1
    self.__thickness = value
```

*Set the thickness of the pen to draw the text into vowel circles.*

##### Parameters

- **value**: (*int*) The thickness value Optional parameter, value = 1 by default

#### slap_on

```python
def slap_on(self, image: sppasImage, fuzzy_points: list) -> sppasImage:
    """Tag the given vowels to the image.

        :param image: (sppasImage or numpy.ndarray) The image to draw vowel positions on
        :param fuzzy_points: (list[sppasFuzzyPoint]) The coordinates of vowels
        :raises: sppasTypeError: If any parameters is of a wrong type
        :return: (sppasImage) The image with the vowels applied on it

        """
    img = self.__check_image(image)
    self.draw_pos_circles(img, fuzzy_points)
    self.draw_pos_names(img, fuzzy_points)
    return img
```

*Tag the given vowels to the image.*

##### Parameters

- **image**: (sppasImage or numpy.ndarray) The image to draw vowel positions on
- **fuzzy_points**: (*list*[sppasFuzzyPo*int*]) The coordinates of vowels


##### Raises

- *sppasTypeError*: If any parameters is of a wrong type


##### Returns

- (sppasImage) The image with the vowels applied on it

#### draw_pos_circles

```python
def draw_pos_circles(self, img: sppasImage, fuzzy_points: list) -> None:
    """Draw vowel positions on an image at given fuzzy points.

        :param img: (sppasImage) The image to draw vowel positions on
        :param fuzzy_points: (list[sppasFuzzyPoint]) The coordinates of vowels
        :return: (None)

        """
    if isinstance(fuzzy_points, list) is False:
        raise sppasTypeError(fuzzy_points, 'list')
    if isinstance(img, sppasImage) is False:
        raise sppasTypeError(img, 'sppasImage')
    for (index, current_fuzzy_point) in enumerate(fuzzy_points):
        if current_fuzzy_point is None or isinstance(current_fuzzy_point, sppasFuzzyPoint) is False:
            continue
        (x, y) = current_fuzzy_point.get_midpoint()
        radius = max(5, current_fuzzy_point.get_radius())
        bgr = self.get_vowel_color(index)
        for _r in range(1, radius, 4):
            blue = min(255, bgr[0] + _r * 3)
            green = min(255, bgr[1] + _r * 3)
            red = min(255, bgr[2] + _r * 3)
            img.surround_point((x, y), (blue, green, red), 2, _r)
```

*Draw vowel positions on an image at given fuzzy points.*

##### Parameters

- **img**: (sppasImage) The image to draw vowel positions on
- **fuzzy_points**: (*list*[sppasFuzzyPo*int*]) The coordinates of vowels


##### Returns

- (None)

#### draw_pos_names

```python
def draw_pos_names(self, img: sppasImage, fuzzy_points: list) -> None:
    """Draw vowel position names on an image at given fuzzy points.

        :param img: (sppasImage) The image to draw vowel positions on
        :param fuzzy_points: (list[sppasFuzzyPoint]) The coordinates of vowels
        :return: (None)

        """
    if isinstance(fuzzy_points, list) is False:
        raise sppasTypeError(fuzzy_points, 'list')
    if isinstance(img, sppasImage) is False:
        raise sppasTypeError(img, 'sppasImage')
    for (index, current_fuzzy_point) in enumerate(fuzzy_points):
        if current_fuzzy_point is None or isinstance(current_fuzzy_point, sppasFuzzyPoint) is False:
            continue
        (x, y) = current_fuzzy_point.get_midpoint()
        radius = max(6, current_fuzzy_point.get_radius())
        if self.__vowel_name_option:
            text = self.get_vowel_text(index)
            if x >= 0 and y >= 0 and (len(text) > 0):
                img.put_text((x - radius // 2, y + radius // 2), (250, 250, 250), self.__thickness, text)
```

*Draw vowel position names on an image at given fuzzy points.*

##### Parameters

- **img**: (sppasImage) The image to draw vowel positions on
- **fuzzy_points**: (*list*[sppasFuzzyPo*int*]) The coordinates of vowels


##### Returns

- (None)



### Protected functions

#### __check_image

```python
def __check_image(self, image: numpy.ndarray) -> sppasImage:
    """Check the given image and return it as a sppasImage object.

        :param image: (numpy.ndarray) The image to check
        :return: (sppasImage) The converted image
        :raises: sppasTypeError: If any parameters is of a wrong type

        """
    if isinstance(image, sppasImage) is True:
        img = image.copy()
    elif isinstance(image, numpy.ndarray) is True:
        img = sppasImage(input_aray=image)
    else:
        raise sppasTypeError(image, 'sppasImage')
    return img
```

*Check the given image and return it as a sppasImage object.*

##### Parameters

- **image**: (numpy.ndarray) The image to check


##### Returns

- (sppasImage) The converted image


##### Raises

- *sppasTypeError*: If any parameters is of a wrong type



## Class `sppasImageHandTagger`

### Description

*Overlay the picture of a hand or a badge on an image.*

This class loads a hand set


### Constructor

#### __init__

```python
def __init__(self, cue_rules: CuedSpeechKeys=CuedSpeechKeys()):
    """The constructor of the SppasImageHandTagger class.

    :param cue_rules: (CuedSpeechKeys) Rules and codes for vowel positions and hand shapes
                      Optional parameter, new instance of CuedSpeechKeys class by default
    :raises: sppasTypeError: If the parameter are not an instance of CuedSpeechKeys class

    """
    if not isinstance(cue_rules, CuedSpeechKeys):
        raise sppasTypeError(cue_rules, 'CuedSpeechKeys')
    self.__cued = cue_rules
    self._vrank = tuple(self.__cued.get_vowels_codes())
    self.__badge_color = (64, 64, 64)
    self.__hands = sppasHandsSet(cue_rules)
    self.__hand_mode = False
```

*The constructor of the SppasImageHandTagger class.*

##### Parameters

- **cue_rules**: (CuedSpeechKeys) Rules and codes for vowel positions and hand shapes Optional parameter, new instance of CuedSpeechKeys class by default


##### Raises

- *sppasTypeError*: If the parameter are not an instance of CuedSpeechKeys class



### Public functions

#### set_cue_rules

```python
def set_cue_rules(self, cue_rules: CuedSpeechKeys):
    """Set the CuedSpeechKeys used to tag the video.

        :param cue_rules: (CuedSpeechKeys) The instance of the cuedSpeechKeys to set

        """
    self.__cued = cue_rules
    self._vrank = tuple(self.__cued.get_vowels_codes())
    self.__hands.set_cue_rules(self.__cued)
```

*Set the CuedSpeechKeys used to tag the video.*

##### Parameters

- **cue_rules**: (CuedSpeechKeys) The instance of the cuedSpeechKeys to set

#### apply_hands_filter

```python
def apply_hands_filter(self, filter_name: str):
    """Apply a filter on all hands images loaded.

        :param filter_name: (str) The name of the filter to apply
        :raises: sppasError: If no hands are loaded
        :raises: sppasValueError: If the given name of the filter is unknown

        """
    self.__hands.apply_hands_filter(filter_name)
```

*Apply a filter on all hands images loaded.*

##### Parameters

- **filter_name**: (*str*) The name of the filter to apply


##### Raises

- *sppasError*: If no hands are loaded
- *sppasValueError*: If the given name of the filter is unknown

#### get_vowel_rank

```python
def get_vowel_rank(self, vowel_code: str) -> int:
    """Get the index from the code of a vowel passed as parameter.

        :param vowel_code: (str) The character code of the vowel
                           One of these characters (for French language) : n, b, c, s, m, t
        :return: (int) The index of the vowel or -1 if the vowel doesn't exist

        """
    if vowel_code in self._vrank:
        return self._vrank.index(vowel_code)
    return -1
```

*Get the index from the code of a vowel passed as parameter.*

##### Parameters

- **vowel_code**: (*str*) The character code of the vowel One of these characters (for French language) : n, b, c, s, m, t


##### Returns

- (*int*) The index of the vowel or -1 if the vowel doesn't exist

#### load_hands

```python
def load_hands(self, prefix: str) -> bool:
    """Load the hands sets (hands image and sights annotations).

        The hand mode is automatically enabled if all hand pictures and sights
        are properly loaded.

        :param prefix: (str) Prefix in hand image filenames
        :raises: sppasIOError: If a hands set found has a missing file (image or annotation)
        :raises: sppasIOError: Or if a file to read is not found
        :return: (bool) True if the hands set has correctly loaded or False else

        """
    hands_loaded_count = self.__hands.load(prefix)
    self.__hand_mode = hands_loaded_count > 0
    return self.__hand_mode
```

*Load the hands sets (hands image and sights annotations).*

The hand mode is automatically enabled if all hand pictures and sights
are properly loaded.

##### Parameters

- **prefix**: (*str*) Prefix in hand image filenames


##### Raises

- *sppasIOError*: If a hands set found has a missing file (image or annotation)
- *sppasIOError*: Or if a file to read is not found


##### Returns

- (*bool*) True if the hands set has correctly loaded or False else

#### hand_mode

```python
def hand_mode(self) -> bool:
    """Return True if the hand mode is enabled: a handset is defined."""
    return self.__hand_mode
```

*Return True if the hand mode is enabled: a handset is defined.*

#### enable_hand_mode

```python
def enable_hand_mode(self, value: bool=True) -> None:
    """Allows to add the pictures of a hand.

        :param value: (bool) True to add a hand, False to draw a badge
        :raises: sppasError: If we activate the hand mode, but we don't have hands loaded

        """
    if value is True and len(self.__hands) == 0:
        raise sppasError("Hand mode can't be enable: no hand pictures loaded.")
    self.__hand_mode = value
```

*Allows to add the pictures of a hand.*

##### Parameters

- **value**: (*bool*) True to add a hand, False to draw a badge


##### Raises

- *sppasError*: If we activate the hand mode, but we don't have hands loaded

#### angle_to_s0

```python
def angle_to_s0(self, shape_code: str, sight_index: int=0) -> int:
    """Return the angle of the given sight compared to S0-S9 axis.

        :param shape_code: (str) Hand shape vowel code
        :param sight_index: (int) The index of the sight
        :return: (int) the computed angle
        :raises: IntervalRangeException: If the index is negative or out of bounds

        """
    return self.__hands.angle_to_s0(shape_code, sight_index)
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
    return self.__hands.distance_to_s0(shape_code, sight_index)
```

*Get the distance between s0 and a sight of the hand.*

##### Parameters

- **shape_code**: (*str*) Shape code name
- **sight_index**: (*int*) The index of the sight


##### Raises

- *IntervalRangeException*: If the index is negative or out of bounds


##### Returns

- (*int*) the computed distance

#### slap_on

```python
def slap_on(self, image: numpy.ndarray, shapes: tuple, hand_sights: list | None) -> sppasImage:
    """Overlay a hand to the given image.

        hand_sights is the list of S0, S9 and target finger coordinates
        where the hand sights have to be put on the image.
        For example:
        [sppasFuzzyPoint: (368,780), sppasFuzzyPoint: (432,684), sppasFuzzyPoint: (540,573)],

        :param image: (sppasImage or numpy.ndarray) The image that we want tag the hand on it
        :param shapes: (list[str, float]) One or two consonant names and their probabilities
        :param hand_sights: (list|None) The s0, s9 and target coords. Used to compute the scale factor
        :return: (sppasImage) The image with the hand applied on it
        :raises: sppasTypeError: If the parameters have the wrong type

        """
    img = self.__check_image(image)
    if len(shapes) == 0:
        return img
    if hand_sights is None:
        hand_sights = list()
    for i in reversed(range(len(shapes))):
        (shape_code, shape_proba) = shapes[i]
        if self.__hand_mode is True:
            (x, y, _) = self.get_coordinates(hand_sights, 'sights_00')
            scale_factor = self.__eval_hand_scale(shape_code, hand_sights)
            angle = self.__eval_hand_rotate_angle(shape_code, hand_sights)
            img = self.__tag_image_with_hand(img, shape_code, shape_proba, x, y, angle, scale_factor)
        else:
            (x, y, r) = self.get_coordinates(hand_sights, 'target')
            img = self.__tag_image_with_badge(img, shape_code, shape_proba, x, y, r)
    return img
```

*Overlay a hand to the given image.*

hand_sights is the list of S0, S9 and target finger coordinates
where the hand sights have to be put on the image.
For example:
[sppasFuzzyPoint: (368,780), sppasFuzzyPoint: (432,684), sppasFuzzyPoint: (540,573)],

##### Parameters

- **image**: (sppasImage or numpy.ndarray) The image that we want tag the hand on it
- **shapes**: (*list*[*str*, *float*]) One or two consonant names and their probabilities
- **hand_sights**: (*list*|None) The s0, s9 and target coords. Used to compute the scale factor


##### Returns

- (sppasImage) The image with the hand applied on it


##### Raises

- *sppasTypeError*: If the parameters have the wrong type

#### get_coordinates

```python
@staticmethod
def get_coordinates(sights: list, label_key: str) -> tuple | None:
    """Return the coordinates of the given sights for the given label.

        :param sights: (list) List of sppasLabel() with sppasFuzzyPoint representing hand sights
        :param label_key: (str) The key of the label to search for coordinates
        :return: (tuple|None) The (x,y,radius) coordinates of the given sights

        """
    for sight_label in sights:
        if sight_label.get_key() == label_key:
            tag = sight_label.get_best()
            point = tag.get_typed_content()
            (x, y) = point.get_midpoint()
            return (x, y, point.get_radius())
    return None
```

*Return the coordinates of the given sights for the given label.*

##### Parameters

- **sights**: (*list*) List of sppasLabel() with sppasFuzzyPoint representing hand sights
- **label_key**: (*str*) The key of the label to search for coordinates


##### Returns

- (*tuple*|None) The (x,y,radius) coordinates of the given sights



### Protected functions

#### __eval_hand_scale

```python
def __eval_hand_scale(self, shape_code: str, sights: list) -> float:
    """Estimate the scale factor for the image of the hand.

        :param shape_code: (str) The code of the hand shape
        :param sights: (list[sppasFuzzyPoint]) The sights to compute the scale factor
        :return: (float) The scale factor computed

        """
    default_value = 0.4
    hand_distance = self.__hands.distance(shape_code)
    if hand_distance == 0:
        return default_value
    (s0_x, s0_y, _) = self.get_coordinates(sights, 'sights_00')
    (s9_x, s9_y, _) = self.get_coordinates(sights, 'sights_09')
    dist_x = abs(s9_x - s0_x)
    dist_y = abs(s9_y - s0_y)
    real_distance = sppasHandProperties.pythagoras(dist_x, dist_y)
    return real_distance / float(hand_distance)
```

*Estimate the scale factor for the image of the hand.*

##### Parameters

- **shape_code**: (*str*) The code of the hand shape
- **sights**: (*list*[sppasFuzzyPo*int*]) The sights to compute the scale factor


##### Returns

- (*float*) The scale factor computed

#### __eval_hand_rotate_angle

```python
def __eval_hand_rotate_angle(self, shape_code: str, sights: list) -> int:
    """Estimate the rotate angle to the hand corresponds with the sights generated.

        :param shape_code: (str) The hand shape code
        :param sights: (list[sppasFuzzyPoint]) A list that contains the s0, s5, s8, s9 and s12
        :return: (int) The hand rotate angle in degree

        """
    (s0_x, s0_y, _) = self.get_coordinates(sights, 'sights_00')
    (s9_x, s9_y, _) = self.get_coordinates(sights, 'sights_09')
    opposite = abs(s9_y - s0_y)
    hypotenuse = sppasHandProperties.pythagoras(abs(s9_x - s0_x), abs(s9_y - s0_y))
    if 0.0 <= opposite * hypotenuse <= 1.0:
        return 0
    angle = math.degrees(math.asin(float(opposite) / float(hypotenuse)))
    if s9_x - s0_x > 0:
        if s9_y - s0_y > 0:
            angle = -angle
    elif s9_y - s0_y > 0:
        angle += 180
    else:
        angle = 180 - angle
    angle = -angle
    target = self.__cued.get_shape_target(shape_code)
    angle += self.__hands.angle(shape_code)
    angle -= self.__hands.angle_to_s0(shape_code, target)
    return int(round(angle, 0))
```

*Estimate the rotate angle to the hand corresponds with the sights generated.*

##### Parameters

- **shape_code**: (*str*) The hand shape code
- **sights**: (*list*[sppasFuzzyPo*int*]) A list that contains the s0, s5, s8, s9 and s12


##### Returns

- (*int*) The hand rotate angle in degree

#### __tag_image_with_hand

```python
def __tag_image_with_hand(self, img: sppasImage, shape_code: str, shape_proba: float, x: int, y: int, angle: int, scale_factor: float=0.2) -> sppasImage:
    """Add a cued speech hand shape on an image.

        The hand with the passed parameters is automatically resized, rotated and cropped.

        :param img: (sppasImage) The image that we want to put the hand on it
        :param shape_code: (str) The code of the hand shape
        :param shape_proba: (float) The probability of the shape to define the transparency
        :param x: (int) The X coordinate of the S0, where to place the hand
        :param y: (int) The Y coordinate of S0, where to place the hand
        :param angle: (int) The degree angle to rotate the hand
        :param scale_factor: (float) Optional parameter, 0.20 by default
                                    The scale factor of the hand to be proportional with the face (image)
        :return: (sppasImage) The image with the hand applied on it

        """
    hand_img = self.__hands.image(shape_code)
    if hand_img is None:
        raise sppasKeyError(self.__cued.get_consonants_codes(), shape_code)
    (original_hand_width, original_hand_height) = hand_img.size()
    (s0_x, s0_y) = self.__hands.get_sight(shape_code, 0)
    hand_img = hand_img.iresize(int(float(original_hand_width) * scale_factor), int(float(original_hand_height) * scale_factor))
    s0_x = int(float(s0_x) * scale_factor)
    s0_y = int(float(s0_y) * scale_factor)
    (resize_hand_width, resize_hand_height) = hand_img.size()
    shape_proba = min(shape_proba * 1.25, 1)
    if shape_proba < 1:
        hand_img = hand_img.ialpha(int(shape_proba * 255.0), direction=-1)
    hand_img = hand_img.icenter(width=img.width, height=img.height)
    s0_x = s0_x + (img.width - resize_hand_width) // 2
    s0_y = s0_y + (img.height - resize_hand_height) // 2
    hand_img = hand_img.irotate(angle, center=(s0_x, s0_y), redimension=False)
    top_left_corner_x = x - s0_x
    top_left_corner_y = y - s0_y
    crop_x = 0
    crop_y = 0
    if top_left_corner_x < 0:
        crop_x = -top_left_corner_x
        top_left_corner_x = 0
    if top_left_corner_y < 0:
        crop_y = -top_left_corner_y
        top_left_corner_y = 0
    if crop_x > 0 or crop_y > 0:
        hand_img = hand_img.icrop(sppasCoords(crop_x, crop_y, max(0, hand_img.width - crop_x), max(0, hand_img.height - crop_y)))
    img = img.ioverlay(hand_img, sppasCoords(top_left_corner_x, top_left_corner_y))
    return img
```

*Add a cued speech hand shape on an image.*

The hand with the passed parameters is automatically resized, rotated and cropped.

##### Parameters

- **img**: (sppasImage) The image that we want to put the hand on it
- **shape_code**: (*str*) The code of the hand shape
- **shape_proba**: (*float*) The probability of the shape to define the transparency
- **x**: (*int*) The X coordinate of the S0, where to place the hand
- **y**: (*int*) The Y coordinate of S0, where to place the hand
- **angle**: (*int*) The degree angle to rotate the hand
- **scale_factor**: (*float*) Optional parameter, 0.20 by default The scale factor of the hand to be proportional with the face (image)


##### Returns

- (sppasImage) The image with the hand applied on it

#### __tag_image_with_badge

```python
def __tag_image_with_badge(self, img: sppasImage, code: str, shape_proba: float, x: int, y: int, radius: int) -> sppasImage:
    """Tag the image with a circle and a text inside.

        :param img: (sppasImage) The image that we want to put the circle and text inside on it
        :param code: (str) The code of the hand shape
        :param shape_proba: (float) The probability of the hand shape to define the transparency
        :param x: (int) The X coordinate (abscissa) where we want to add the hand
        :param y: (int) The Y coordinate (ordinate) where we want to add the hand
        :param radius: (int) The radius of the circle
        :return: (sppasImage) The image with the circle and text inside applied on it

        """
    if radius is None:
        radius = 20
    cv2.circle(img, (x, y), radius - 2, self.__badge_color, -1)
    cv2.circle(img, (x, y), radius, (5, 5, 5), 3)
    if shape_proba < 1.0:
        b = int(250.0 * shape_proba)
        img.put_text((x - radius // 2, y + radius // 2), (b, b, b), 1, code)
    else:
        img.put_text((x - radius // 2, y + radius // 2), (250, 250, 250), 2, code)
    return img
```

*Tag the image with a circle and a text inside.*

##### Parameters

- **img**: (sppasImage) The image that we want to put the circle and text inside on it
- **code**: (*str*) The code of the hand shape
- **shape_proba**: (*float*) The probability of the hand shape to define the transparency
- **x**: (*int*) The X coordinate (abscissa) where we want to add the hand
- **y**: (*int*) The Y coordinate (ordinate) where we want to add the hand
- **radius**: (*int*) The radius of the circle


##### Returns

- (sppasImage) The image with the circle and text inside applied on it

#### __check_image

```python
def __check_image(self, image: numpy.ndarray) -> sppasImage:
    """Check the given image and return it as a sppasImage object.

        :param image: (numpy.ndarray) The image to check
        :return: (sppasImage) The converted image
        :raises: sppasTypeError: If any parameters is of a wrong type

        """
    if isinstance(image, sppasImage) is True:
        img = image.copy()
    elif isinstance(image, numpy.ndarray) is True:
        img = sppasImage(input_aray=image)
    else:
        raise sppasTypeError(image, 'sppasImage')
    return img
```

*Check the given image and return it as a sppasImage object.*

##### Parameters

- **image**: (numpy.ndarray) The image to check


##### Returns

- (sppasImage) The converted image


##### Raises

- *sppasTypeError*: If any parameters is of a wrong type





~ Created using [Clamming](https://clamming.sf.net) version 2.1 ~
