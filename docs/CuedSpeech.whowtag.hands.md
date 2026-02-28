# CuedSpeech.whowtag.hands module

## List of classes

## Class `sppasHandProperties`

### Description

*Data storage of a hand.*

Angle estimation is performed thanks to both sights S0 (wrist) and S9
(middle finger mcp).
- angle is 0 degree if: x0 = x9 ; y0 <= y9
- angle is 180 degrees if: x0 = x9 ; y0 > y9
Size estimation is performed thanks to both sights S0 and S9 too.

Estimations from coordinates in a picture:

A---------------------S9
|                   /
|               /
|          /
|     /
S0

S0 = (x0, y0)
S9 = (x9, y9)
A = (x0, y9)

Let's introduce:
- a: the distance between S0 and S9 to be estimated
- b: the distance between A and S9: abs(y9 - y0)
- c: the distance between A and S0: abs(x9 - x0)
- alpha = angle A = 90 degrees
- beta = angle S0 to be estimated

then:
a = sqrt(b*b - c*c) [pythagore]
beta = arccos( (c*c + a*a - b*b) / (2*c*a) )


### Constructor

#### __init__

```python
def __init__(self, image: sppasImage, sights: sppasSights, target_index: int):
    """The constructor of the SppasHandProperties.

    This class stores data for a hand.

    :param image: (sppasImage) The hand image associated of all data stored
    :param sights: (sppasSights) The sights annotation of the hand
    :param target_index: (int) Index of the target sight
    :raises: sppasTypeError: If the parameters have a wrong type
    :raises: IntervalRangeException: If the target index parameter is negative or too huge

    """
    if isinstance(image, sppasImage) is False:
        raise sppasTypeError(image, 'sppasImage')
    if isinstance(sights, sppasSights) is False:
        raise sppasTypeError(sights, 'sppasSights')
    self.__beta = 0
    self.__dist = 0
    self.__target = (0, 0)
    self.__distances_with_s0 = list()
    self.__angles_with_s0 = list()
    self.__image = image
    self.__sights = sights
    if 0 <= target_index < len(sights):
        try:
            (x, y, _, _) = sights.get_sight(target_index)
        except IntervalRangeException:
            (x, y) = (None, None)
        self.__target = (x, y)
    else:
        raise IntervalRangeException(target_index, 0, len(sights))
    self.__estimation()
```

*The constructor of the SppasHandProperties.*

This class stores data for a hand.

##### Parameters

- **image**: (sppasImage) The hand image associated of all data stored
- **sights**: (sppasSights) The sights annotation of the hand
- **target_index**: (*int*) Index of the target sight


##### Raises

- *sppasTypeError*: If the parameters have a wrong type
- *IntervalRangeException*: If the target index parameter is negative or too huge



### Public functions

#### distance

```python
def distance(self) -> int:
    """Return the [s0,s9] estimated distance value.

        :return: (int) The distance between the s0 and s9 point of the hand

        """
    return self.__dist
```

*Return the [s0,s9] estimated distance value.*

##### Returns

- (*int*) The distance between the s0 and s9 point of the hand

#### angle

```python
def angle(self) -> int:
    """Return the default angle of the hand in the image.

        :return: (int) The beta angle

        """
    return self.__beta
```

*Return the default angle of the hand in the image.*

##### Returns

- (*int*) The beta angle

#### nb_sights

```python
def nb_sights(self) -> int:
    """Return the number of sights of the hand.

        :return: (int) The sights length

        """
    return len(self.__sights)
```

*Return the number of sights of the hand.*

##### Returns

- (*int*) The sights length

#### image

```python
def image(self) -> sppasImage:
    """Return the image of the hand associated to the data structure.

        :return: (sppasImage) The hand image

        """
    return self.__image
```

*Return the image of the hand associated to the data structure.*

##### Returns

- (sppasImage) The hand image

#### image_size

```python
def image_size(self) -> tuple:
    """Return the image size of the hand (width, height).

        :return: (tuple) The size of the image

        """
    return self.__image.size()
```

*Return the image size of the hand (width, height).*

##### Returns

- (*tuple*) The size of the image

#### target_coords

```python
def target_coords(self) -> tuple:
    """Return coordinate (x, y) of the target point of the hand.

        :return: (tuple) The target point coordinate

        """
    return self.__target
```

*Return coordinate (x, y) of the target point of the hand.*

##### Returns

- (*tuple*) The target point coordinate

#### get_sight

```python
def get_sight(self, index: int) -> tuple:
    """Return a sight with the given index.

        :param index: (int) The index of the sight that we want
        :raises: IntervalRangeException: If the index is negative or out of bounds
        :return: (tuple) The coordinates of the sight

        """
    if 0 <= index < len(self.__sights):
        (x, y, _, _) = self.__sights.get_sight(index)
        return (x, y)
    else:
        raise IntervalRangeException(index, 0, len(self.__sights))
```

*Return a sight with the given index.*

##### Parameters

- **index**: (*int*) The index of the sight that we want


##### Raises

- *IntervalRangeException*: If the index is negative or out of bounds


##### Returns

- (*tuple*) The coordinates of the sight

#### get_sights

```python
def get_sights(self) -> sppasSights:
    """Return the sight of the hand

        :return: (sppasSights) The sights of the hand

        """
    return self.__sights
```

Return the sight of the hand

##### Returns

- (sppasSights) The sights of the hand

#### set_image

```python
def set_image(self, hand_image: sppasImage) -> None:
    """Setter of the hand image (used in the program to apply the filters).

        :param hand_image: (sppasImage) The new hand image

        :raises: sppasTypeError: If the 'hand_image' parameter is not an instance of sppasImage class

        """
    if isinstance(hand_image, sppasImage) is False:
        raise sppasTypeError(hand_image, 'sppasImage')
    self.__image = hand_image
```

*Setter of the hand image (used in the program to apply the filters).*

##### Parameters

- **hand_image**: (sppasImage) The new hand image

##### Raises

- *sppasTypeError*: If the 'hand_image' parameter is not an instance of sppasImage class

#### get_distance_with_s0

```python
def get_distance_with_s0(self, sight_index: int) -> int:
    """Get the distance between s0 and a sight of the hand.

        :param sight_index: (int) The index of the sight
        :raises: IntervalRangeException: If the index is negative or out of bounds
        :return: (int) the computed distance

        """
    if sight_index < 0 or sight_index > len(self.__distances_with_s0):
        raise IntervalRangeException(sight_index, 0, len(self.__distances_with_s0))
    return self.__distances_with_s0[sight_index]
```

*Get the distance between s0 and a sight of the hand.*

##### Parameters

- **sight_index**: (*int*) The index of the sight


##### Raises

- *IntervalRangeException*: If the index is negative or out of bounds


##### Returns

- (*int*) the computed distance

#### get_angle_with_s0

```python
def get_angle_with_s0(self, sight_index: int) -> int:
    """Get the angle between s0 and a sight of the hand.

        :param sight_index: (int) The index of the sight
        :raises: IntervalRangeException: If the index is negative or out of bounds
        :return: (int) the computed angle

        """
    if sight_index < 0 or sight_index > len(self.__angles_with_s0):
        raise IntervalRangeException(sight_index, 0, len(self.__angles_with_s0))
    return self.__angles_with_s0[sight_index]
```

*Get the angle between s0 and a sight of the hand.*

##### Parameters

- **sight_index**: (*int*) The index of the sight


##### Raises

- *IntervalRangeException*: If the index is negative or out of bounds


##### Returns

- (*int*) the computed angle

#### pythagoras

```python
@staticmethod
def pythagoras(side1: float, side2: float) -> float:
    """Estimate with the Pythagoras theorem the hypotenuse of the right triangle.

        Compute the hypotenuse with the two sides passed as parameters.
        The method doesn't verify if the sides and the hypotenuse represent a right triangle or a simple triangle.

        :param side1: (float) The first side of the right triangle
        :param side2: (float) The second side of the right triangle
        :return: (float) The computed hypotenuse

        """
    return math.sqrt(side1 * side1 + side2 * side2)
```

*Estimate with the Pythagoras theorem the hypotenuse of the right triangle.*

Compute the hypotenuse with the two sides passed as parameters.
The method doesn't verify if the sides and the hypotenuse represent a right triangle or a simple triangle.

##### Parameters

- **side1**: (*float*) The first side of the right triangle
- **side2**: (*float*) The second side of the right triangle


##### Returns

- (*float*) The computed hypotenuse



### Protected functions

#### __estimation

```python
def __estimation(self) -> None:
    """Estimate the distance and the angle of the hand shape of this class.

        :raises: sppasError: If the number sights is different of 21 or 4

        """
    (x0, y0, _, _) = self.__sights.get_sight(0)
    if len(self.__sights) == 21:
        (s9_x, s9_y, _, _) = self.__sights.get_sight(9)
    elif len(self.__sights) == 4:
        (s9_x, s9_y, _, _) = self.__sights.get_sight(2)
    else:
        raise sppasError(f'21 or 4 sights were expected. Got {len(self.__sights)} instead.')
    s0s9_x = s9_x - x0
    s0s9_y = s9_y - y0
    s0s9_dist = self.pythagoras(s0s9_x, s0s9_y)
    bottom_number = math.sqrt(s0s9_x * s0s9_x + s0s9_y * s0s9_y)
    angle = math.degrees(math.acos(s0s9_x / bottom_number))
    if s0s9_y > 0:
        angle = -angle
    self.__dist = int(round(s0s9_dist, 0))
    self.__beta = int(round(angle, 0))
    for (i, current_sight) in enumerate(self.__sights):
        if i > 0:
            sight_dist_x = current_sight[0] - x0
            sight_dist_y = current_sight[1] - y0
            sight_dist = self.pythagoras(sight_dist_x, sight_dist_y)
            self.__distances_with_s0.append(round(sight_dist, 0))
            if i == 9:
                self.__angles_with_s0.append(0)
            else:
                top_number = s0s9_x * sight_dist_y - s0s9_y * sight_dist_x
                bottom_number = s0s9_dist * sight_dist
                sight_angle = math.degrees(math.asin(top_number / bottom_number))
                self.__angles_with_s0.append(round(sight_angle, 0))
        else:
            self.__distances_with_s0.append(0)
            self.__angles_with_s0.append(0)
```

*Estimate the distance and the angle of the hand shape of this class.*

##### Raises

- *sppasError*: If the number sights is different of 21 or 4



## Class `sppasHandFilters`

### Description

*Apply filters on hand pictures.*

##### Example

    >>> f = sppasHandFilters()
    >>> f.get_filter_names()
    > ["cartoon", "sights", "skeleton", "sticks", "tgtline"]


### Constructor

#### __init__

```python
def __init__(self, radius: int=20, circles_color: tuple=(0, 100, 200), line_thickness: int=10, lines_color: tuple=(60, 50, 40)):
    """Create an instance of the sppasHanddFilters class.

    :param radius: (int) Radius of the circles.
    :param circles_color: (tuple) Color of the circles in (B, G, R)
    :param line_thickness: (int) Thickness of the lines.
    :param lines_color: (tuple) Color of the lines in (B, G, R)

    """
    sppasHandFilters.__check_init_parameters(radius, circles_color, line_thickness, lines_color)
    self.__radius = radius
    self.__circles_color = circles_color
    self.__line_thickness = line_thickness
    self.__lines_color = lines_color
    self.__sights_hidden = {'0': [2, 3, 4, 6, 7, 8, 10, 11, 12, 14, 15, 16, 18, 19, 20], '1': [2, 3, 4, 11, 12, 15, 16, 19, 20], '2': [2, 3, 4, 15, 16, 19, 20], '3': [2, 3, 4, 7, 8], '4': [2, 3, 4], '5': [], '6': [11, 12, 15, 16, 19, 20], '7': [15, 16, 19, 20], '8': [2, 3, 4, 15, 16, 19, 20]}
    self.__sights_link = [(0, 1), (0, 5), (0, 17), (1, 2), (2, 3), (3, 4), (5, 6), (5, 9), (6, 7), (7, 8), (9, 10), (9, 13), (10, 11), (11, 12), (13, 14), (13, 17), (14, 15), (15, 16), (17, 18), (18, 19), (19, 20)]
```

*Create an instance of the sppasHanddFilters class.*

##### Parameters

- **radius**: (*int*) Radius of the circles.
- **circles_color**: (*tuple*) Color of the circles in (B, G, R)
- **line_thickness**: (*int*) Thickness of the lines.
- **lines_color**: (*tuple*) Color of the lines in (B, G, R)



### Public functions

#### get_filter_names

```python
@staticmethod
def get_filter_names() -> list:
    """Return the list of available filters."""
    fcts = list()
    for func in inspect.getmembers(sppasHandFilters, predicate=inspect.isroutine):
        if callable(getattr(sppasHandFilters, func[0])) and func[0].startswith('_') is False and (func[0] != 'get_filter_names'):
            fcts.append(func[0])
    return fcts
```

*Return the list of available filters.*

#### cartoon

```python
def cartoon(self, hand_properties: sppasHandProperties, shape_code: str) -> sppasImage:
    """Apply a cartoon filter on a hand image.

        :param hand_properties: (sppasHandProperties) An hands set
        :param shape_code: (str) The hand shape code
        :raises sppasTypeError: If the parameter doesn't have a type expected
        :raises sppasValueError: If the 'shape_code' parameter value is unknown
        :return: (sppasImage) The image with the filter applied on it

        """
    hand_img = hand_properties.image()
    sights = hand_properties.get_sights()
    self.__check_fct_parameters(hand_img, shape_code, sights)
    return hand_img.icartoon()
```

*Apply a cartoon filter on a hand image.*

##### Parameters

- **hand_properties**: (sppasHandProperties) An hands set
- **shape_code**: (*str*) The hand shape code


##### Raises

- *sppasTypeError*: If the parameter doesn't have a type expected
- *sppasValueError*: If the 'shape_code' parameter value is unknown


##### Returns

- (sppasImage) The image with the filter applied on it

#### sights

```python
def sights(self, hand_properties: sppasHandProperties, shape_code: str) -> sppasImage:
    """Apply a sights filter on a hand image.

        Put a circle for each sight on the hand linked with line.

        :param hand_properties: (sppasHandProperties) An hands set
        :param shape_code: (str) The hand shape code
        :raises sppasTypeError: If the parameter doesn't have a type expected
        :raises sppasValueError: If the 'shape_code' parameter value is unknown
        :return: (sppasImage) The image with the filter applied on it

        """
    hand_img = hand_properties.image()
    sights = hand_properties.get_sights()
    self.__check_fct_parameters(hand_img, shape_code, sights)
    (data, red, green, blue) = sppasHandFilters.__img_to_data(hand_img)
    data = self.__apply_sights(data, shape_code, sights)
    return sppasHandFilters.__data_to_img(data, red, green, blue)
```

*Apply a sights filter on a hand image.*

Put a circle for each sight on the hand linked with line.

##### Parameters

- **hand_properties**: (sppasHandProperties) An hands set
- **shape_code**: (*str*) The hand shape code


##### Raises

- *sppasTypeError*: If the parameter doesn't have a type expected
- *sppasValueError*: If the 'shape_code' parameter value is unknown


##### Returns

- (sppasImage) The image with the filter applied on it

#### skeleton

```python
def skeleton(self, hand_properties: sppasHandProperties, shape_code: str) -> sppasImage:
    """Apply a skeleton image filter from a hand image.

        :param hand_properties: (sppasHandProperties) An hands set
        :param shape_code: (str) The hand shape code
        :raises: sppasTypeError: If the parameter doesn't have a type expected
        :raises: sppasValueError: If the 'shape_code' parameter value is unknown
        :return: (sppasImage) The skeleton image

        """
    hand_img = hand_properties.image()
    sights = hand_properties.get_sights()
    self.__check_fct_parameters(hand_img, shape_code, sights)
    img = sppasImage(0).blank_image(hand_img.width, hand_img.height)
    self.__apply_sights(img, shape_code, sights)
    temp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (_, alpha) = cv2.threshold(temp, 0, 255, cv2.THRESH_BINARY)
    (b, g, r) = cv2.split(img)
    bgra = [b, g, r, alpha]
    img = sppasImage(input_array=cv2.merge(bgra, 4))
    return img
```

*Apply a skeleton image filter from a hand image.*

##### Parameters

- **hand_properties**: (sppasHandProperties) An hands set
- **shape_code**: (*str*) The hand shape code


##### Raises

- *sppasTypeError*: If the parameter doesn't have a type expected
- *sppasValueError*: If the 'shape_code' parameter value is unknown


##### Returns

- (sppasImage) The skeleton image

#### sticks

```python
def sticks(self, hand_properties: sppasHandProperties, shape_code: str) -> sppasImage:
    """Draw sticks on a specific hand image of a hand set.

        :param hand_properties: (sppasHandProperties) An hands set
        :param shape_code: (str) The hand shape code
        :raises: sppasTypeError: If the parameter doesn't have a type expected
        :raises: sppasValueError: If the 'shape_code' parameter value is unknown
        :return: (sppasImage) The skeleton image

        """
    hand_img = hand_properties.image()
    sights = hand_properties.get_sights()
    self.__check_fct_parameters(hand_img, shape_code, sights)
    (data, red, green, blue) = sppasHandFilters.__img_to_data(hand_img)
    if shape_code == '3':
        (s5_x, s5_y, _, _) = sights.get_sight(5)
        (s6_x, s6_y, _, _) = sights.get_sight(6)
        data = cv2.line(data, (s5_x, s5_y), (s6_x, s6_y), self.__lines_color, self.__line_thickness)
    elif shape_code == '8':
        (s5_x, s5_y, _, _) = sights.get_sight(5)
        (s8_x, s8_y, _, _) = sights.get_sight(8)
        data = cv2.line(data, (s5_x, s5_y), (s8_x, s8_y), self.__lines_color, self.__line_thickness)
        (s9_x, s9_y, _, _) = sights.get_sight(9)
        (s12_x, s12_y, _, _) = sights.get_sight(12)
        data = cv2.line(data, (s9_x, s9_y), (s12_x, s12_y), self.__lines_color, self.__line_thickness)
    data = cv2.circle(data, hand_properties.target_coords(), self.__radius, self.__circles_color, -1)
    return sppasHandFilters.__data_to_img(data, red, green, blue)
```

*Draw sticks on a specific hand image of a hand set.*

##### Parameters

- **hand_properties**: (sppasHandProperties) An hands set
- **shape_code**: (*str*) The hand shape code


##### Raises

- *sppasTypeError*: If the parameter doesn't have a type expected
- *sppasValueError*: If the 'shape_code' parameter value is unknown


##### Returns

- (sppasImage) The skeleton image

#### tgtline

```python
def tgtline(self, hand_properties: sppasHandProperties, shape_code: str) -> sppasImage:
    """Draw a circle on the target sight and a line on S0-S9.

        :param hand_properties: (sppasHandProperties) An hands set
        :param shape_code: (str) The hand shape code
        :raises: sppasTypeError: If the parameter doesn't have a type expected
        :raises: sppasValueError: If the 'shape_code' parameter value is unknown
        :return: (sppasImage) The skeleton image

        """
    hand_img = hand_properties.image()
    sights = hand_properties.get_sights()
    self.__check_fct_parameters(hand_img, shape_code, sights)
    (data, red, green, blue) = sppasHandFilters.__img_to_data(hand_img)
    (s0_x, s0_y, _, _) = sights.get_sight(0)
    (s9_x, s9_y, _, _) = sights.get_sight(9)
    data = cv2.line(data, (s9_x, s9_y), (s0_x, s0_y), self.__lines_color, self.__line_thickness)
    data = cv2.circle(data, hand_properties.target_coords(), self.__radius, self.__circles_color, -1)
    return sppasHandFilters.__data_to_img(data, red, green, blue)
```

*Draw a circle on the target sight and a line on S0-S9.*

##### Parameters

- **hand_properties**: (sppasHandProperties) An hands set
- **shape_code**: (*str*) The hand shape code


##### Raises

- *sppasTypeError*: If the parameter doesn't have a type expected
- *sppasValueError*: If the 'shape_code' parameter value is unknown


##### Returns

- (sppasImage) The skeleton image



### Protected functions

#### __img_to_data

```python
@staticmethod
def __img_to_data(img):
    bgr_img = img.ibgra_to_bgr()
    data = np.array(bgr_img)
    (r1, g1, b1) = (0, 0, 0)
    (r2, g2, b2) = (255, 255, 255)
    (red, green, blue) = (data[:, :, 0], data[:, :, 1], data[:, :, 2])
    mask = (red == r1) & (green == g1) & (blue == b1)
    data[:, :, :3][mask] = [r2, g2, b2]
    return (data, red, green, blue)
```



#### __data_to_img

```python
@staticmethod
def __data_to_img(data, red, green, blue):
    (r2, g2, b2) = (255, 255, 255)
    img = sppasImage(input_array=cv2.cvtColor(data, cv2.COLOR_RGB2RGBA))
    mask = (red == r2) & (green == g2) & (blue == b2)
    img[:, :, :4][mask] = [r2, g2, b2, 0]
    return img
```



#### __check_init_parameters

```python
@staticmethod
def __check_init_parameters(radius, circles_color, line_thickness, lines_color) -> None:
    """Check filters parameters and raise exception if one of them has a problem.

        :param radius: (int) The radius of the circles
        :param circles_color: (tuple[int, int, int]) The color of the circles
        :param line_thickness: (int) The thickness of the lines
        :param lines_color: (tuple[int, int, int]) The color of the lines

        :raises: sppasTypeError: If a parameter doesn't have a type expected
        :raises: sppasValueError: If a parameter value is not correct

        """
    if isinstance(circles_color, (tuple, list)) is False or isinstance(lines_color, (tuple, list)) is False:
        raise sppasTypeError(circles_color, 'tuple')
    if len(circles_color) != 3 and len(lines_color) == 3:
        raise sppasValueError('colors', len(circles_color) + len(lines_color))
    if isinstance(radius, int) is False:
        raise sppasTypeError(radius, 'int')
    if isinstance(line_thickness, int) is False:
        raise sppasTypeError(line_thickness, 'int')
    if radius < 1:
        raise sppasValueError('radius', radius)
    if line_thickness < 1:
        raise sppasValueError('line_thickness', line_thickness)
```

*Check filters parameters and raise exception if one of them has a problem.*

##### Parameters

- **radius**: (*int*) The radius of the circles
- **circles_color**: (*tuple*[*int*, *int*, *int*]) The color of the circles
- **line_thickness**: (*int*) The thickness of the lines
- **lines_color**: (*tuple*[*int*, *int*, *int*]) The color of the lines

##### Raises

- *sppasTypeError*: If a parameter doesn't have a type expected
- *sppasValueError*: If a parameter value is not correct

#### __check_fct_parameters

```python
def __check_fct_parameters(self, hand_img: sppasImage, shape_code: str, sights: sppasSights) -> None:
    """Check filters parameters and raise exception if one of them has a problem.

        :param hand_img: (sppasImage) The hand shape image
        :param shape_code: (str) The hand shape code
        :param sights: (sppasSight) The sights of hand shape
        :raises: sppasTypeError: If a parameter doesn't have a type expected
        :raises: sppasValueError: If a parameter value is not correct

        """
    if isinstance(hand_img, sppasImage) is False:
        raise sppasTypeError(hand_img, 'sppasImage')
    if isinstance(sights, sppasSights) is False:
        raise sppasTypeError(sights, 'sppasSights')
    if shape_code not in self.__sights_hidden:
        raise sppasValueError('shape_code', shape_code)
```

*Check filters parameters and raise exception if one of them has a problem.*

##### Parameters

- **hand_img**: (sppasImage) The hand shape image
- **shape_code**: (*str*) The hand shape code
- **sights**: (sppasSight) The sights of hand shape


##### Raises

- *sppasTypeError*: If a parameter doesn't have a type expected
- *sppasValueError*: If a parameter value is not correct

#### __apply_sights

```python
def __apply_sights(self, img: np.ndarray, shape_code: str, sights: sppasSights) -> np.ndarray:
    """Put the sights circles and the connected lines on the given image.

        :param img: (numpy.ndarray) The hand shape image
        :param shape_code: (str) The hand shape code
        :param sights: (sppasSight) The sights of hand shape
        :return: (numpy.ndarray) The image with the sights and connected lines on it

        """
    (s0_x, s0_y, _, _) = sights.get_sight(0)
    (s9_x, s9_y, _, _) = sights.get_sight(9)
    if s9_x - s0_x > 0:
        s_arm_x = s0_x - abs(s9_x - s0_x)
    else:
        s_arm_x = s0_x + abs(s9_x - s0_x)
    if s9_y - s0_y > 0:
        s_arm_y = s0_y - abs(s9_y - s0_y)
    else:
        s_arm_y = s0_y + abs(s9_y - s0_y)
    img = cv2.line(img, (s_arm_x, s_arm_y), (s0_x, s0_y), self.__lines_color, self.__line_thickness)
    img = cv2.circle(img, (s_arm_x, s_arm_y), self.__radius, self.__circles_color, -1)
    for item in self.__sights_link:
        if item[0] not in self.__sights_hidden[shape_code] and item[1] not in self.__sights_hidden[shape_code]:
            (start_x, start_y, _, _) = sights.get_sight(item[0])
            (end_x, end_y, _, _) = sights.get_sight(item[1])
            img = cv2.line(img, (start_x, start_y), (end_x, end_y), self.__lines_color, self.__line_thickness)
    for i in range(len(sights)):
        if i not in self.__sights_hidden[shape_code]:
            (x, y, _, _) = sights.get_sight(i)
            img = cv2.circle(img, (x, y), self.__radius, self.__circles_color, -1)
    return img
```

*Put the sights circles and the connected lines on the given image.*

##### Parameters

- **img**: (numpy.ndarray) The hand shape image
- **shape_code**: (*str*) The hand shape code
- **sights**: (sppasSight) The sights of hand shape


##### Returns

- (numpy.ndarray) The image with the sights and connected lines on it



## Class `sppasHandsSet`

### Description

*Data structure to load and store all hands.*




### Constructor

#### __init__

```python
def __init__(self, cue_rules: CuedSpeechKeys=CuedSpeechKeys()):
    """Store an image of a hand for each given consonant.

    :param cue_rules: (CuedSpeechKeys) Cued speech rules
                      Optional parameter, new instance of CuedSpeechKeys class by default
    :raises: sppasTypeError: If the parameter is not an instance of CuedSpeechKeys

    """
    if isinstance(cue_rules, CuedSpeechKeys) is False:
        raise sppasTypeError(cue_rules, 'CuedSpeechKeys')
    self.__cued = cue_rules
    self.__hands_properties = dict()
    self.__hands_filter = sppasHandFilters()
```

*Store an image of a hand for each given consonant.*

##### Parameters

- **cue_rules**: (CuedSpeechKeys) Cued speech rules Optional parameter, new instance of CuedSpeechKeys class by default


##### Raises

- *sppasTypeError*: If the parameter is not an instance of CuedSpeechKeys



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

#### image

```python
def image(self, shape_code: str):
    """Return a deep copy of the hand image matching with the given code.

        Return None if no image associated with the given code.

        :param shape_code: (str) Hand shape vowel code
        :return: (sppasImage or None) The hand image corresponding to the code, or None if the code is wrong

        """
    if shape_code in self.__hands_properties.keys():
        return self.__hands_properties[shape_code].image().copy()
    else:
        return None
```

*Return a deep copy of the hand image matching with the given code.*

Return None if no image associated with the given code.

##### Parameters

- **shape_code**: (*str*) Hand shape vowel code


##### Returns

- (sppasImage or None) The hand image corresponding to the code, or None if the code is wrong

#### target_coords

```python
def target_coords(self, shape_code: str):
    """Return target coords of the hand image matching with the given code.

        Return None if no image associated with the given code.

        :param shape_code: (str) Hand shape vowel code
        :return: ((int, int) or None) The target coords of the hand image, or None if the code is wrong

        """
    if shape_code in self.__hands_properties:
        return self.__hands_properties[shape_code].target_coords()
    else:
        return None
```

*Return target coords of the hand image matching with the given code.*

Return None if no image associated with the given code.

##### Parameters

- **shape_code**: (*str*) Hand shape vowel code


##### Returns

- ((*int*, *int*) or None) The target coords of the hand image, or None if the code is wrong

#### get_sight

```python
def get_sight(self, shape_code: str, index: int):
    """Return a sight of a hand with the given shape code and index.

        Return None if no image associated with the given code.

        :param shape_code: (str) Hand shape vowel code
        :param index: (int) The index of the sight that we want
        :raises: IntervalRangeException: If the index is negative or out of bounds
        :return: (tuple[int, int] or None) The coords of the sight, or None if the code is wrong

        """
    if shape_code in self.__hands_properties:
        return self.__hands_properties[shape_code].get_sight(index)
    else:
        return None
```

*Return a sight of a hand with the given shape code and index.*

Return None if no image associated with the given code.

##### Parameters

- **shape_code**: (*str*) Hand shape vowel code
- **index**: (*int*) The index of the sight that we want


##### Raises

- *IntervalRangeException*: If the index is negative or out of bounds


##### Returns

- (*tuple*[*int*, *int*] or None) The coords of the sight, or None if the code is wrong

#### angle

```python
def angle(self, shape_code: str) -> int:
    """Return the angle of the hand image matching with the given code.

        Return 0 if no image associated with the given code.

        :param shape_code: (str) Hand shape vowel code
        :return: (int) The angle of the hand image, Or 0 if the code is wrong

        """
    if shape_code in self.__hands_properties:
        return self.__hands_properties[shape_code].angle()
    return 0
```

*Return the angle of the hand image matching with the given code.*

Return 0 if no image associated with the given code.

##### Parameters

- **shape_code**: (*str*) Hand shape vowel code


##### Returns

- (*int*) The angle of the hand image, Or 0 if the code is wrong

#### angle_to_s0

```python
def angle_to_s0(self, shape_code: str, sight_index: int=0) -> int:
    """Return the angle of the given sight compared to S0-S9 axis.

        :param shape_code: (str) Hand shape vowel code
        :param sight_index: (int) The index of the sight
        :return: (int) the computed angle
        :raises: IntervalRangeException: If the index is negative or out of bounds

        """
    if shape_code in self.__hands_properties:
        return self.__hands_properties[shape_code].get_angle_with_s0(sight_index)
    return 0
```

*Return the angle of the given sight compared to S0-S9 axis.*

##### Parameters

- **shape_code**: (*str*) Hand shape vowel code
- **sight_index**: (*int*) The index of the sight


##### Returns

- (*int*) the computed angle


##### Raises

- *IntervalRangeException*: If the index is negative or out of bounds

#### distance

```python
def distance(self, shape_code: str) -> int:
    """Return the distance of the hand image matching with the given code.

        Return 0 if no image associated with the given code.

        :param shape_code: (str) Shape code name
        :return: (int) The distance of the current hand, or 0 if the code is wrong

        """
    if shape_code in self.__hands_properties:
        return self.__hands_properties[shape_code].distance()
    return 0
```

*Return the distance of the hand image matching with the given code.*

Return 0 if no image associated with the given code.

##### Parameters

- **shape_code**: (*str*) Shape code name


##### Returns

- (*int*) The distance of the current hand, or 0 if the code is wrong

#### distance_to_s0

```python
def distance_to_s0(self, shape_code: str, sight_index: int=0) -> int:
    """Get the distance between s0 and a sight of the hand.

        :param shape_code: (str) Shape code name
        :param sight_index: (int) The index of the sight
        :raises: IntervalRangeException: If the index is negative or out of bounds
        :return: (int) the computed distance

        """
    if shape_code in self.__hands_properties:
        return self.__hands_properties[shape_code].get_distance_with_s0(sight_index)
    return 0
```

*Get the distance between s0 and a sight of the hand.*

##### Parameters

- **shape_code**: (*str*) Shape code name
- **sight_index**: (*int*) The index of the sight


##### Raises

- *IntervalRangeException*: If the index is negative or out of bounds


##### Returns

- (*int*) the computed distance

#### load

```python
def load(self, prefix: str) -> int:
    """Load the hand images matching with the given prefix.

        :param prefix: (str) Prefix in hand image filenames
        :raises: sppasIOError: If the files with the given prefix and pattern are not found
        :return: (int) The number of hands loaded

        """
    hands_sets_manager = sppasHandResource()
    hands_sets_manager.load_hand_set(prefix)
    self.__load_hand_pictures(hands_sets_manager.get_hand_images(prefix), hands_sets_manager.get_hands_sights(prefix))
    return len(self.__hands_properties)
```

*Load the hand images matching with the given prefix.*

##### Parameters

- **prefix**: (*str*) Prefix in hand image filenames


##### Raises

- *sppasIOError*: If the files with the given prefix and pattern are not found


##### Returns

- (*int*) The number of hands loaded

#### apply_hands_filter

```python
def apply_hands_filter(self, filter_name: str) -> None:
    """Apply a filter on all hands images loaded.

        :param filter_name: (str) The name of the filter to apply
        :raises: sppasValueError: Unknown filter name

        """
    if hasattr(self.__hands_filter, filter_name):
        for (key, item) in self.__hands_properties.items():
            item.set_image(getattr(self.__hands_filter, filter_name)(item, key))
    else:
        raise sppasValueError('filter_name', filter_name)
```

*Apply a filter on all hands images loaded.*

##### Parameters

- **filter_name**: (*str*) The name of the filter to apply


##### Raises

- *sppasValueError*: Unknown filter name



### Protected functions

#### __load_hand_pictures

```python
def __load_hand_pictures(self, hands_images: list, hands_sights: list) -> None:
    """Return the dictionary of pictures filepath for the hand shapes.

        The number of images and sights should be the same and equal to the
        number of shapes for the given language.

        Notice that it is supposed that the loaded images are ranked
        in the same order as the shapes, i.e., shape "0" is
        represented in the first image, etc.

        :param hands_images: (list) Prefix in hand image filenames
        :param hands_sights: (list) Pattern in hand image filenames

        :raises: sppasError: If the number of images is different of sights
        :raises: sppasIOError: If a file to read is not found
        :raises: sppasError: If invalid number of images or sights.
        :return: (dict[str, SppasHandProperties]) The pictures filepath dictionary

        """
    _shapes = self.__cued.get_consonants_codes()
    if len(_shapes) != len(hands_images):
        raise sppasError(f'Invalid number of hand images. Expected {len(_shapes)}. Got {len(hands_images)} instead.')
    if len(_shapes) != len(hands_sights):
        raise sppasError(f'Invalid number of hand sights. Expected {len(_shapes)}. Got {len(hands_sights)} instead.')
    for (i, paths) in enumerate(zip(hands_images, hands_sights)):
        if os.path.exists(paths[0]) is False:
            logging.warning(f"Can't find hand picture file {paths[0]}.")
            break
        hand_img = sppasImage(filename=paths[0])
        if os.path.exists(paths[1]) is False:
            logging.warning(f"Can't find hand sights file {paths[1]}.")
            break
        try:
            data = sppasImageSightsReader(paths[1])
            if len(data.sights) != 1:
                raise sppasError(f'Invalid file sights {paths[1]}. ({len(data.sights)} != 1)')
            current_sights = data.sights[0]
            if current_sights.get_sight(0) is None or current_sights.get_sight(9) is None:
                raise sppasIOError(paths[1])
            target_index = self.__cued.get_shape_target(_shapes[i])
            self.__hands_properties[_shapes[i]] = sppasHandProperties(hand_img, current_sights, target_index)
        except sppasIOError as e:
            logging.error(f'Error while reading hand sights: {e}')
```

*Return the dictionary of pictures filepath for the hand shapes.*

The number of images and sights should be the same and equal to the
number of shapes for the given language.

Notice that it is supposed that the loaded images are ranked
in the same order as the shapes, i.e., shape "0" is
represented in the first image, etc.

##### Parameters

- **hands_images**: (*list*) Prefix in hand image filenames
- **hands_sights**: (*list*) Pattern in hand image filenames

##### Raises

- *sppasError*: If the number of images is different of sights
- *sppasIOError*: If a file to read is not found
- *sppasError*: If invalid number of images or sights.


##### Returns

- (*dict*[*str*, SppasHandProperties]) The pictures filepath dictionary



### Overloads

#### __len__

```python
def __len__(self):
    """Return the number of hand shapes loaded."""
    return len(self.__hands_properties)
```

*Return the number of hand shapes loaded.*





~ Created using [Clamming](https://clamming.sf.net) version 2.1 ~
