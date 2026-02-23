# CuedSpeech.wherecue.position module

## List of classes

## Class `FaceTwoDim`

### Description

*Some (x, y) coordinates among the 68 sights on a 1000x1000px face.*

##### Example




##### Example

    >>> with FaceTwoDim() as face:
    >>> print(face.sights.x(0))
    >>> print(face.dim)


### Constructor

#### __init__

```python
def __init__(self):
    """Create the dictionary with sights coords.

    """
    s = sppasSights(68)
    s.set_sight(0, 0, 165)
    s.set_sight(1, 2, 300)
    s.set_sight(2, 15, 435)
    s.set_sight(3, 40, 570)
    s.set_sight(4, 90, 695)
    s.set_sight(5, 170, 805)
    s.set_sight(6, 260, 905)
    s.set_sight(7, 375, 980)
    s.set_sight(8, 500, 1000)
    s.set_sight(9, 625, 980)
    s.set_sight(10, 760, 905)
    s.set_sight(11, 830, 805)
    s.set_sight(12, 910, 695)
    s.set_sight(13, 960, 570)
    s.set_sight(14, 985, 435)
    s.set_sight(15, 998, 300)
    s.set_sight(16, 1000, 165)
    s.set_sight(17, 99, 70)
    s.set_sight(18, 170, 15)
    s.set_sight(19, 250, 0)
    s.set_sight(20, 330, 20)
    s.set_sight(21, 410, 55)
    s.set_sight(22, 590, 55)
    s.set_sight(23, 680, 20)
    s.set_sight(24, 750, 0)
    s.set_sight(25, 820, 15)
    s.set_sight(26, 910, 70)
    s.set_sight(27, 500, 150)
    s.set_sight(28, 500, 240)
    s.set_sight(29, 500, 330)
    s.set_sight(30, 500, 420)
    s.set_sight(31, 390, 480)
    s.set_sight(32, 445, 500)
    s.set_sight(33, 500, 510)
    s.set_sight(34, 555, 500)
    s.set_sight(35, 620, 480)
    s.set_sight(36, 200, 160)
    s.set_sight(37, 255, 132)
    s.set_sight(38, 315, 132)
    s.set_sight(39, 370, 170)
    s.set_sight(40, 315, 185)
    s.set_sight(41, 255, 185)
    s.set_sight(42, 630, 170)
    s.set_sight(43, 685, 132)
    s.set_sight(44, 745, 132)
    s.set_sight(45, 800, 160)
    s.set_sight(46, 745, 185)
    s.set_sight(47, 685, 185)
    s.set_sight(48, 302, 633)
    s.set_sight(49, 375, 610)
    s.set_sight(50, 445, 600)
    s.set_sight(51, 500, 605)
    s.set_sight(52, 555, 600)
    s.set_sight(53, 625, 610)
    s.set_sight(54, 698, 633)
    s.set_sight(55, 625, 705)
    s.set_sight(56, 555, 745)
    s.set_sight(57, 500, 750)
    s.set_sight(58, 445, 745)
    s.set_sight(59, 375, 705)
    s.set_sight(60, 328, 635)
    s.set_sight(61, 445, 645)
    s.set_sight(62, 500, 650)
    s.set_sight(63, 555, 645)
    s.set_sight(64, 672, 635)
    s.set_sight(65, 555, 677)
    s.set_sight(66, 500, 682)
    s.set_sight(67, 445, 677)
    self.__dict__ = dict(dim=68, sights=s, size=1000)
```

*Create the dictionary with sights coords.*





## Class `BaseWherePositionPredictor`

### Description

*Base class to predict vowel positions around the face.*

The vowel positions are considered targets in the hand trajectory.
Currently, 5 vowel positions are possible and they have only one coordinate.
For English language, this will have to be changed because some vowels have
a movement effect: side-forward, side-down.


### Constructor

#### __init__

```python
def __init__(self, nb_sights=68):
    """Instantiate a vowel position's predictor.

    :param nb_sights: (int) Number of face sights. Must match the one of FaceTwoDim().
    :raises: NotImplementedError: given nb sights is not supported.
    :raises: sppasTypeError: given nb sights is not of 'int' type.

    """
    self._description = MSG_DESCRIPTION_BASE
    self.__sights = None
    self._f2 = FaceTwoDim()
    try:
        nb_sights = int(nb_sights)
    except ValueError:
        raise sppasTypeError(type(nb_sights), 'int')
    nb_sights = int(nb_sights)
    if nb_sights != self._f2.dim:
        raise NotImplementedError('The support for vowel prediction with {:d} sights is not implemented yet. Expected {:d}.'.format(nb_sights, self._f2.dim))
    self._vowels = dict()
    self.__vowel_mapping = {'b': self._calculate_vowel_b, 'c': self._calculate_vowel_c, 'm': self._calculate_vowel_m, 's': self._calculate_vowel_s, 'sf': self._calculate_vowel_sf, 'sd': self._calculate_vowel_sd, 't': self._calculate_vowel_t, 'n': self._calculate_vowel_n}
```

*Instantiate a vowel position's predictor.*

##### Parameters

- **nb_sights**: (*int*) Number of face sights. Must match the one of FaceTwoDim().


##### Raises

- *NotImplementedError*: given nb sights is not supported.
- *sppasTypeError*: given nb sights is not of 'int' type.



### Public functions

#### vowel_codes

```python
def vowel_codes(self) -> tuple:
    """Return the list of vowel codes the class can calculate position."""
    return tuple(self.__vowel_mapping.keys())
```

*Return the list of vowel codes the class can calculate position.*

#### get_sights_dim

```python
def get_sights_dim(self) -> int:
    """Return the number of sights this predictor was trained for."""
    return self._f2.dim
```

*Return the number of sights this predictor was trained for.*

#### set_sights_and_predict_coords

```python
def set_sights_and_predict_coords(self, sights: sppasSights | None=None, vowels: tuple | None=None) -> None:
    """Set the sights of a face and predict all vowel positions.

        If no sights are provided, it uses default sights. It validates the
        input type and the number of sights before setting them and predicting
        vowel coordinates.

        :param sights: (sppasSights | None)
        :param vowels: (tuple | None) List of vowel position names. Default is all known ones.
        :raises: sppasTypeError: given parameter is not a sppasSights type.
        :raises: NotImplementedError: not the expected number of sights

        """
    if sights is None:
        self.__sights = self._f2.sights
    else:
        if isinstance(sights, sppasSights) is False:
            raise sppasTypeError(type(sights), 'sppasSights')
        if len(sights) != self._f2.dim:
            raise NotImplementedError('The support for vowel prediction with {:d} sights is not implemented yet. Expected {:d}.'.format(len(sights), self._f2.dim))
        self.__sights = sights
    if vowels is None:
        vowels = self.vowel_codes()
    self.predict_vowels_coords(vowels)
```

*Set the sights of a face and predict all vowel positions.*

If no sights are provided, it uses default sights. It validates the
input type and the number of sights before setting them and predicting
vowel coordinates.

##### Parameters

- **sights**: (sppasSights | None)
- **vowels**: (*tuple* | None) List of vowel position names. Default is all known ones.


##### Raises

- *sppasTypeError*: given parameter is not a sppasSights type.
- *NotImplementedError*: not the expected number of sights

#### get_vowel_coords

```python
def get_vowel_coords(self, vowel: str='n') -> tuple:
    """Return the absolute position of the given vowel.

        Estimated relatively to the sights of a face. Sights must be set
        before using this method.

        :param vowel: (char) Vowel position name. If unknown, 'n' is used instead.
        :return: tuple(x, y, r) with point coordinates and radius
        :raises: sppasKeyError: Invalid given vowel code.

        """
    if vowel in self._vowels:
        return self._vowels[vowel]
    raise sppasKeyError(vowel, 'Predicted Vowels')
```

*Return the absolute position of the given vowel.*

Estimated relatively to the sights of a face. Sights must be set
before using this method.

##### Parameters

- **vowel**: (char) Vowel position name. If unknown, 'n' is used instead.


##### Returns

- tuple(x, y, r) with point coordinates and radius


##### Raises

- *sppasKeyError*: Invalid given vowel code.

#### predict_vowels_coords

```python
def predict_vowels_coords(self, vowels: tuple=('n',)) -> None:
    """Estimate the absolute position of all the requested vowels.

        Estimate the absolute positions of specified vowels relative to the
        sights of a face. It uses predefined coordinates and calculations
        to determine these positions and stores them in a dictionary.
        Sights must be set before using this method.

        :param vowels: (tuple) List of vowel position names. If unknown, 'n' is used instead.
        :raises: sppasKeyError: Invalid given vowel code.

        """
    self.check(vowels)
    self._vowels = dict()
    for vowel in vowels:
        try:
            self._vowels[vowel] = self.__vowel_mapping[vowel]()
        except NotImplementedError:
            logging.warning(f"No vowel position calculation for vowel '{vowel}'")
            pass
```

*Estimate the absolute position of all the requested vowels.*

Estimate the absolute positions of specified vowels relative to the
sights of a face. It uses predefined coordinates and calculations
to determine these positions and stores them in a dictionary.
Sights must be set before using this method.

##### Parameters

- **vowels**: (*tuple*) List of vowel position names. If unknown, 'n' is used instead.


##### Raises

- *sppasKeyError*: Invalid given vowel code.

#### check

```python
def check(self, vowels: tuple):
    """Check if the given vowel codes are valid.

        :param vowels: (tuple) The character codes of vowels
        :raises: sppasKeyError: Invalid given vowel code.

        """
    if self.__sights is None:
        logging.warning('Attempting to predict vowel positions but no sights were defined.')
        self.set_sights_and_predict_coords()
    codes = self.vowel_codes()
    for vowel in vowels:
        if vowel not in codes:
            raise sppasKeyError(vowel, 'Vowel Position Code')
```

*Check if the given vowel codes are valid.*

##### Parameters

- **vowels**: (*tuple*) The character codes of vowels


##### Raises

- *sppasKeyError*: Invalid given vowel code.



### Private functions

#### _calculate_vowel_n

```python
def _calculate_vowel_n(self) -> tuple:
    """To be overridden. Calculate the position of the neutral position.

        :return: (tuple) coordinates and radius of the neutral position

        """
    x = self._x(8)
    y = self._y(8) + 4 * (self._y(8) - self._y(57))
    return (x, y, 0)
```

*To be overridden. Calculate the position of the neutral position.*

##### Returns

- (*tuple*) coordinates and radius of the neutral position

#### _calculate_vowel_b

```python
def _calculate_vowel_b(self) -> tuple:
    """To be overridden. Calculate the position of a cheek bone vowel.

        :return: (tuple) coordinates and radius of the cheek bone vowel

        """
    x = self._x(4) + abs(self._x(36) - self._x(0)) // 2
    y = self._y(1) - abs(self._y(1) - self._y(0)) // 3
    return (x, y, 0)
```

*To be overridden. Calculate the position of a cheek bone vowel.*

##### Returns

- (*tuple*) coordinates and radius of the cheek bone vowel

#### _calculate_vowel_c

```python
def _calculate_vowel_c(self) -> tuple:
    """To be overridden. Calculate the position of a chin vowel.

        :return: (tuple) coordinates and radius of the chin vowel

        """
    x = self._x(8)
    y = self._y(8) - abs(self._y(8) - self._y(57)) // 5
    return (x, y, 0)
```

*To be overridden. Calculate the position of a chin vowel.*

##### Returns

- (*tuple*) coordinates and radius of the chin vowel

#### _calculate_vowel_m

```python
def _calculate_vowel_m(self) -> tuple:
    """To be overridden. Calculate the position of a mouth vowel.

        :return: (tuple) coordinates and radius of the mouth vowel

        """
    x = self._x(48) - abs(self._x(48) - self._x(4)) // 4
    y = self._y(60)
    return (x, y, 0)
```

*To be overridden. Calculate the position of a mouth vowel.*

##### Returns

- (*tuple*) coordinates and radius of the mouth vowel

#### _calculate_vowel_s

```python
def _calculate_vowel_s(self) -> tuple:
    """To be overridden. Calculate the position of a side vowel.

        :return: (tuple) coordinates and radius of the side vowel

        """
    x = self._x(0) - 2 * abs(self._x(8) - self._x(0)) // 3
    y = self._y(4) - abs(self._y(4) - self._y(3)) // 2
    return (x, y, 0)
```

*To be overridden. Calculate the position of a side vowel.*

##### Returns

- (*tuple*) coordinates and radius of the side vowel

#### _calculate_vowel_sf

```python
def _calculate_vowel_sf(self) -> tuple:
    """To be overridden. Calculate the position of a side-forward vowel.

        :return: (tuple) coordinates and radius of the side-forward vowel

        """
    raise NotImplementedError
```

*To be overridden. Calculate the position of a side-forward vowel.*

##### Returns

- (*tuple*) coordinates and radius of the side-forward vowel

#### _calculate_vowel_sd

```python
def _calculate_vowel_sd(self) -> tuple:
    """To be overridden. Calculate the position of a side-down vowel.

        :return: (tuple) coordinates and radius of the side-down vowel

        """
    raise NotImplementedError
```

*To be overridden. Calculate the position of a side-down vowel.*

##### Returns

- (*tuple*) coordinates and radius of the side-down vowel

#### _calculate_vowel_t

```python
def _calculate_vowel_t(self) -> tuple:
    """To be overridden. Calculate the position of a throat vowel.

        :return: (tuple) coordinates and radius of the throat vowel

        """
    x = self._x(8)
    y = self._y(8) + int(1.2 * float(abs(self._y(8) - self._y(57))))
    return (x, y, 0)
```

*To be overridden. Calculate the position of a throat vowel.*

##### Returns

- (*tuple*) coordinates and radius of the throat vowel

#### _x

```python
def _x(self, idx) -> int:
    return self.__sights.x(idx)
```



#### _y

```python
def _y(self, idx) -> int:
    return self.__sights.y(idx)
```



#### _radius_ratio

```python
def _radius_ratio(self) -> float:
    """Return the width/height ratio of the face sights."""
    return (float(self._x(16) - self._x(0)) + float(self._y(8) - self._y(27))) / 1.85
```

*Return the width/height ratio of the face sights.*



## Class `WherePositionPredictorCustoms`

### Description

*Predict the coordinates of vowels from 2D sights.*

Extend the base class to predict the coordinates of vowels from 2D sights.
It overrides methods to provide specific calculations for different vowel
positions based on facial landmarks.

It adds the calculation of a radius for each vowel: it allows to define
an area in which the target is acceptable.


### Constructor

#### __init__

```python
def __init__(self, nb_sights=68):
    super(WherePositionPredictorCustoms, self).__init__(nb_sights)
    self._description = MSG_DESCRIPTION_CUSTOMS
```





### Private functions

#### _calculate_vowel_n

```python
def _calculate_vowel_n(self) -> tuple:
    """Override. Calculate the position of the neutral vowel.

        :return: (tuple) coordinates and radius of the neutral vowel

        """
    x = self._x(8) - abs(self._x(8) - self._x(7)) // 4
    y = self._y(8) + 4 * (self._y(8) - self._y(57))
    r = int(0.2 * self._radius_ratio())
    return (x, y, r)
```

*Override. Calculate the position of the neutral vowel.*

##### Returns

- (*tuple*) coordinates and radius of the neutral vowel

#### _calculate_vowel_b

```python
def _calculate_vowel_b(self) -> tuple:
    """Override. Calculate the position of the cheek bone vowel.

        :return: (tuple) coordinates and radius of the cheek bone vowel

        """
    x = self._x(4) + abs(self._x(36) - self._x(0)) // 6
    y = self._y(1)
    r = int(0.114 * self._radius_ratio())
    return (x, y, r)
```

*Override. Calculate the position of the cheek bone vowel.*

##### Returns

- (*tuple*) coordinates and radius of the cheek bone vowel

#### _calculate_vowel_c

```python
def _calculate_vowel_c(self) -> tuple:
    """Override. Calculate the position of the chin vowel.

        :return: (tuple) coordinates and radius of the chin vowel

        """
    x = self._x(8)
    y = self._y(8) - abs(self._y(8) - self._y(57)) // 5
    r = int(0.062 * self._radius_ratio())
    return (x, y, r)
```

*Override. Calculate the position of the chin vowel.*

##### Returns

- (*tuple*) coordinates and radius of the chin vowel

#### _calculate_vowel_m

```python
def _calculate_vowel_m(self) -> tuple:
    """Override. Calculate the position of the mouth vowel.

        :return: (tuple) coordinates and radius of the mouth vowel

        """
    x = self._x(48) - abs(self._x(48) - self._x(4)) // 4
    y = self._y(60)
    r = int(0.094 * self._radius_ratio())
    return (x, y, r)
```

*Override. Calculate the position of the mouth vowel.*

##### Returns

- (*tuple*) coordinates and radius of the mouth vowel

#### _calculate_vowel_s

```python
def _calculate_vowel_s(self) -> tuple:
    """Override. Calculate the position of the side vowel.

        :return: (tuple) coordinates and radius of the side vowel

        """
    x = self._x(0) - 2 * abs(self._x(8) - self._x(0)) // 3
    y = self._y(4)
    r = int(0.18 * self._radius_ratio())
    return (x, y, r)
```

*Override. Calculate the position of the side vowel.*

##### Returns

- (*tuple*) coordinates and radius of the side vowel

#### _calculate_vowel_t

```python
def _calculate_vowel_t(self) -> tuple:
    """Override. Calculate the position of the throat vowel.

        :return: (tuple) coordinates and radius of the throat vowel

        """
    x = self._x(8)
    y = self._y(8) + int(1.2 * float(abs(self._y(8) - self._y(57))))
    r = int(0.14 * self._radius_ratio())
    return (x, y, r)
```

*Override. Calculate the position of the throat vowel.*

##### Returns

- (*tuple*) coordinates and radius of the throat vowel



## Class `WherePositionPredictorObserved`

### Description

*Predict the coordinates of vowels from 2D sights.*

Extend the base class to predict the coordinates of vowels from 2D sights.
It overrides methods to provide specific calculations for different vowel
positions based on facial landmarks.

It adds the calculation of a radius for each vowel: it allows to define
an area in which the target is acceptable.

Observed values are for each measured key on 5 professional cuers:
1 ; b ; 64 ; 375
2 ; b ; 141 ; 425
6 ; b ; 60 ; 370
7 ; b ; 145 ; 339
8 ; b ; -15 ; 397
3 ; c ; 349 ; 836
4 ; c ; 461 ; 967
5 ; c ; 393 ; 944
6 ; c ; 499 ; 927
7 ; c ; 488 ; 904
1 ; m ; 309 ; 710
4 ; m ; 215 ; 742
5 ; m ; 233 ; 653
6 ; m ; 213 ; 656
8 ; m ; 304 ; 713
2 ; s ; -337 ; 753
3 ; s ; -622 ; 726
4 ; s ; -453 ; 667
6 ; s ; -331 ; 774
7 ; s ; -415 ; 370
1 ; t ; 543 ; 1429
3 ; t ; 339 ; 1305
4 ; t ; 505 ; 1382
5 ; t ; 448 ; 1272
6 ; t ; 434 ; 1573

Average and standard deviations:
- b : mean(79.0, 381.2), stdev(66.37, 32.07)
- c : mean(438.0, 915.6), stdev(64.61, 50.12)
- m : mean(254.8, 694.8), stdev(47.87, 38.87)
- s : mean(-431.6, 658.0), stdev(118.38, 165.93)
- t : mean(453.8, 1392.2), stdev(77.75, 118.53)


### Constructor

#### __init__

```python
def __init__(self, nb_sights=68):
    super(WherePositionPredictorObserved, self).__init__(nb_sights)
    self._description = MSG_DESCRIPTION_OBSERVED
```





### Private functions

#### _calculate_vowel_n

```python
def _calculate_vowel_n(self) -> tuple:
    """Override. Calculate the position of the neutral vowel.

        :return: (tuple) coordinates and radius of the neutral vowel

        """
    x = self._x(8) - abs(self._x(8) - self._x(7)) // 4
    y = self._y(8) + 4 * (self._y(8) - self._y(57))
    r = int(0.2 * self._radius_ratio())
    return (x, y, r)
```

*Override. Calculate the position of the neutral vowel.*

##### Returns

- (*tuple*) coordinates and radius of the neutral vowel

#### _calculate_vowel_b

```python
def _calculate_vowel_b(self) -> tuple:
    """Override. Calculate the position of the cheek bone vowel.

        :return: (tuple) coordinates and radius of the cheek bone vowel

        """
    x = self._x(4) - abs(self._x(36) - self._x(0)) // 20
    y = self._y(1) + int(abs(self._y(2) - self._y(1)) / 1.6)
    r = int(0.044 * self._radius_ratio())
    return (x, y, r)
```

*Override. Calculate the position of the cheek bone vowel.*

##### Returns

- (*tuple*) coordinates and radius of the cheek bone vowel

#### _calculate_vowel_c

```python
def _calculate_vowel_c(self) -> tuple:
    """Override. Calculate the position of the chin vowel.

        :return: (tuple) coordinates and radius of the chin vowel

        """
    x = self._x(8) - int(abs(self._x(8) - self._x(6)) / 3.8)
    y = self._y(8) - int(abs(self._y(8) - self._y(57)) // 3.0)
    r = int(0.059 * self._radius_ratio())
    return (x, y, r)
```

*Override. Calculate the position of the chin vowel.*

##### Returns

- (*tuple*) coordinates and radius of the chin vowel

#### _calculate_vowel_m

```python
def _calculate_vowel_m(self) -> tuple:
    """Override. Calculate the position of the mouth vowel.

        :return: (tuple) coordinates and radius of the mouth vowel

        """
    x = self._x(48) - int(abs(self._x(48) - self._x(4)) / 4.5)
    y = self._y(60) + abs(self._y(60) - self._y(4))
    r = int(0.044 * self._radius_ratio())
    return (x, y, r)
```

*Override. Calculate the position of the mouth vowel.*

##### Returns

- (*tuple*) coordinates and radius of the mouth vowel

#### _calculate_vowel_s

```python
def _calculate_vowel_s(self) -> tuple:
    """Override. Calculate the position of the side vowel.

        :return: (tuple) coordinates and radius of the side vowel

        """
    x = self._x(0) - int(abs(self._x(8) - self._x(0)) * 0.85)
    y = self._y(4) - int(abs(self._y(4) - self._y(3)) / 3.2)
    r = int(0.14 * self._radius_ratio())
    return (x, y, r)
```

*Override. Calculate the position of the side vowel.*

##### Returns

- (*tuple*) coordinates and radius of the side vowel

#### _calculate_vowel_t

```python
def _calculate_vowel_t(self) -> tuple:
    """Override. Calculate the position of the throat vowel.

        :return: (tuple) coordinates and radius of the throat vowel

        """
    x = self._x(8) - int(abs(self._x(8) - self._x(6)) / 5.2)
    y = self._y(8) + int(0.8 * float(abs(self._y(8) - self._y(33))))
    r = int(0.1 * self._radius_ratio())
    return (x, y, r)
```

*Override. Calculate the position of the throat vowel.*

##### Returns

- (*tuple*) coordinates and radius of the throat vowel



## Class `WherePositionPredictorUnified`

### Description

*Predict the coordinates of vowels from 2D sights.*

Extend the base class to predict the coordinates of vowels from 2D sights.
It overrides methods to provide specific calculations for different vowel
positions based on facial landmarks.

It adds the calculation of a radius for each vowel: it allows to define
an area in which the target is acceptable.

This model was created from observed values in a corpus.

- Collected data: 3769 values
- Filtered data: 3752 values (outliers removed)

Statistics by Hand Position
- b: Count = 230, Mean = (144, 397), Std Dev = (70.45, 92.26)
- c: Count = 529, Mean = (425, 888), Std Dev = (112.48, 76.10)
- m: Count = 676, Mean = (260, 682), Std Dev = (79.36, 90.67)
- s: Count = 1750, Mean = (-193, 635), Std Dev = (241.45, 232.91)
- t: Count = 584, Mean = (435, 1419), Std Dev = (143.24, 223.21)


### Constructor

#### __init__

```python
def __init__(self, nb_sights=68):
    super(WherePositionPredictorUnified, self).__init__(nb_sights)
    self._description = MSG_DESCRIPTION_UNIFIED
```





### Private functions

#### _calculate_vowel_n

```python
def _calculate_vowel_n(self) -> tuple:
    """Override. Calculate the position of the neutral vowel.

        :return: (tuple) coordinates and radius of the neutral vowel

        """
    x = self._x(0)
    y = self._y(8) + 4 * (self._y(8) - self._y(57))
    r = int(0.2 * self._radius_ratio())
    return (x, y, r)
```

*Override. Calculate the position of the neutral vowel.*

##### Returns

- (*tuple*) coordinates and radius of the neutral vowel

#### _calculate_vowel_b

```python
def _calculate_vowel_b(self) -> tuple:
    """Override. Calculate the position of the cheek bone vowel.

        :return: (tuple) coordinates and radius of the cheek bone vowel

        """
    x = self._x(4) + int(abs(self._x(36) - self._x(0)) / 3.7)
    y = self._y(1) + int(abs(self._y(2) - self._y(1)) / 1.4)
    r = int(0.08 * self._radius_ratio())
    return (x, y, r)
```

*Override. Calculate the position of the cheek bone vowel.*

##### Returns

- (*tuple*) coordinates and radius of the cheek bone vowel

#### _calculate_vowel_c

```python
def _calculate_vowel_c(self) -> tuple:
    """Override. Calculate the position of the chin vowel.

        :return: (tuple) coordinates and radius of the chin vowel

        """
    x = self._x(8) - int(abs(self._x(8) - self._x(6)) / 3.2)
    y = self._y(8) - int(abs(self._y(8) - self._y(57)) / 4.2)
    r = int(0.094 * self._radius_ratio())
    return (x, y, r)
```

*Override. Calculate the position of the chin vowel.*

##### Returns

- (*tuple*) coordinates and radius of the chin vowel

#### _calculate_vowel_m

```python
def _calculate_vowel_m(self) -> tuple:
    """Override. Calculate the position of the mouth vowel.

        :return: (tuple) coordinates and radius of the mouth vowel

        """
    x = self._x(48) - abs(self._x(48) - self._x(4)) // 5
    y = self._y(60) + int(abs(self._y(60) - self._y(4)) * 0.8)
    r = int(0.085 * self._radius_ratio())
    return (x, y, r)
```

*Override. Calculate the position of the mouth vowel.*

##### Returns

- (*tuple*) coordinates and radius of the mouth vowel

#### _calculate_vowel_s

```python
def _calculate_vowel_s(self) -> tuple:
    """Override. Calculate the position of the side vowel.

        :return: (tuple) coordinates and radius of the side vowel

        """
    x = self._x(0) - int(abs(self._x(8) - self._x(0)) / 2.6)
    y = self._y(4) - abs(self._y(4) - self._y(3)) // 2
    r = int(0.237 * self._radius_ratio())
    return (x, y, r)
```

*Override. Calculate the position of the side vowel.*

##### Returns

- (*tuple*) coordinates and radius of the side vowel

#### _calculate_vowel_t

```python
def _calculate_vowel_t(self) -> tuple:
    """Override. Calculate the position of the throat vowel.

        :return: (tuple) coordinates and radius of the throat vowel

        """
    x = self._x(8) - int(abs(self._x(8) - self._x(6)) / 3.6)
    y = self._y(8) + int(0.85 * float(abs(self._y(8) - self._y(33))))
    r = int(0.183 * self._radius_ratio())
    return (x, y, r)
```

*Override. Calculate the position of the throat vowel.*

##### Returns

- (*tuple*) coordinates and radius of the throat vowel





~ Created using [Clamming](https://clamming.sf.net) version 2.1 ~
