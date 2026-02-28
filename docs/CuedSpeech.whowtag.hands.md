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

### Constructor

#### __init__

```python
def __init__(self, *args, **kwargs):
    raise sppasEnableFeatureError('video')
```





### Public functions

#### get_filter_names

```python
@staticmethod
def get_filter_names() -> list:
    return []
```





## Class `sppasHandsSet`

### Constructor

#### __init__

```python
def __init__(self, *args, **kwargs):
    raise sppasEnableFeatureError('video')
```







~ Created using [Clamming](https://clamming.sf.net) version 2.1 ~
