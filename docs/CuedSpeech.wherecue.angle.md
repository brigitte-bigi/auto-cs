# CuedSpeech.wherecue.angle module

## List of classes

## Class `BaseWhereAnglePredictor`

### Description

*Base class to predict the angle of the hand.*

Currently, 5 vowel positions are possible, and they are associated to
only one angle value.
For English langage, this will have to be changed because some vowels have
a movement effect: side-forward, side-down.

Angle value is given relatively to the horizontal axis, like in the
following unit circle:

90°
|
|
180° ------- + ------- 0°
|
|
270°
-90°


### Constructor

#### __init__

```python
def __init__(self):
    """Instantiate a hand angle's predictor.

    """
    self._description = MSG_DESCRIPTION_BASE
    self._vowels = dict()
    self._radius = 10
    self.__vowel_mapping = {'b': self._calculate_angle_b, 'c': self._calculate_angle_c, 'm': self._calculate_angle_m, 's': self._calculate_angle_s, 't': self._calculate_angle_t, 'n': self._calculate_angle_n}
```

*Instantiate a hand angle's predictor.*





### Public functions

#### vowel_codes

```python
def vowel_codes(self) -> tuple:
    """Return the list of vowel codes the class can calculate hand angles for."""
    return tuple(self.__vowel_mapping.keys())
```

*Return the list of vowel codes the class can calculate hand angles for.*

#### get_radius

```python
def get_radius(self) -> int:
    """Vagueness of angle value."""
    return self._radius
```

*Vagueness of angle value.*

#### set_radius

```python
def set_radius(self, r: int):
    """Fix a new radius value.

        :param r: (int) The new radius value between 0 and MAX_RADIUS.
        :raises: ValueError: Invalid given radius value.

        """
    r = int(r)
    if r < 0 or r > self.MAX_RADIUS:
        raise IntervalRangeException(r, 0, BaseWhereAnglePredictor.MAX_RADIUS)
    self._radius = r
```

*Fix a new radius value.*

##### Parameters

- **r**: (*int*) The new radius value between 0 and MAX_RADIUS.


##### Raises

- *ValueError*: Invalid given radius value.

#### get_angle

```python
def get_angle(self, vowel: str='n') -> tuple:
    """Return the angle at a given position.

        :param vowel: (char) Vowel position name. If unknown, 'n' is used instead.
        :return: (int)
        :raises: sppasKeyError: Invalid given vowel code.

        """
    if vowel in self._vowels:
        return self._vowels[vowel]
    raise sppasKeyError(vowel, 'Predicted Angles')
```

*Return the angle at a given position.*

##### Parameters

- **vowel**: (char) Vowel position name. If unknown, 'n' is used instead.


##### Returns

- (*int*)


##### Raises

- *sppasKeyError*: Invalid given vowel code.

#### predict_angle_values

```python
def predict_angle_values(self, vowels=('n',)) -> None:
    """Estimate the angle of the hand for all the given positions.

        It uses predefined angles and stores them in a dictionary.

        :param vowels: (tuple) List of vowel position names. If unknown, 'n' is used instead.
        :raises: sppasKeyError: Invalid given vowel code.

        """
    self.check(vowels)
    self._vowels = dict()
    codes = self.vowel_codes()
    for vowel in vowels:
        if vowel not in codes:
            raise sppasKeyError(vowel, 'Position Code')
        self._vowels[vowel] = self.__vowel_mapping[vowel]()
```

*Estimate the angle of the hand for all the given positions.*

It uses predefined angles and stores them in a dictionary.

##### Parameters

- **vowels**: (*tuple*) List of vowel position names. If unknown, 'n' is used instead.


##### Raises

- *sppasKeyError*: Invalid given vowel code.

#### check

```python
def check(self, vowels: list):
    """Check if the given vowel codes are valid.

        :param vowels: (list of characters)
        :raises: sppasKeyError: Invalid given vowel code.

        """
    codes = self.vowel_codes()
    for vowel in vowels:
        if vowel not in codes:
            raise sppasKeyError(vowel, 'Position Code')
```

*Check if the given vowel codes are valid.*

##### Parameters

- **vowels**: (*list* of characters)


##### Raises

- *sppasKeyError*: Invalid given vowel code.



### Private functions

#### _calculate_angle_n

```python
def _calculate_angle_n(self) -> int:
    """To be overridden. Calculate the angle at the neutral position.

        :return: (int) angle in degrees

        """
    return 60
```

*To be overridden. Calculate the angle at the neutral position.*

##### Returns

- (*int*) angle in degrees

#### _calculate_angle_b

```python
def _calculate_angle_b(self) -> int:
    """To be overridden. Calculate the angle at the cheek bone position.

        :return: (int) angle in degrees

        """
    return 60
```

*To be overridden. Calculate the angle at the cheek bone position.*

##### Returns

- (*int*) angle in degrees

#### _calculate_angle_c

```python
def _calculate_angle_c(self) -> int:
    """To be overridden. Calculate the angle at the chin position.

        :return: (int) angle in degrees

        """
    return 60
```

*To be overridden. Calculate the angle at the chin position.*

##### Returns

- (*int*) angle in degrees

#### _calculate_angle_m

```python
def _calculate_angle_m(self) -> int:
    """To be overridden. Calculate the angle at the mouse position.

        :return: (int) angle in degrees

        """
    return 60
```

*To be overridden. Calculate the angle at the mouse position.*

##### Returns

- (*int*) angle in degrees

#### _calculate_angle_s

```python
def _calculate_angle_s(self) -> int:
    """To be overridden. Calculate the angle at the side position.

        :return: (int) angle in degrees

        """
    return 60
```

*To be overridden. Calculate the angle at the side position.*

##### Returns

- (*int*) angle in degrees

#### _calculate_angle_t

```python
def _calculate_angle_t(self) -> int:
    """To be overridden. Calculate the angle at the throat position.

        :return: (int) angle in degrees

        """
    return 60
```

*To be overridden. Calculate the angle at the throat position.*

##### Returns

- (*int*) angle in degrees



## Class `WhereAnglePredictorCustoms`

### Description

*Predict hand angles with experts rules.*




### Constructor

#### __init__

```python
def __init__(self):
    """Instantiate a custom hand angle predictor.

    """
    super(WhereAnglePredictorCustoms, self).__init__()
    self._description = MSG_DESCRIPTION_CUSTOMS
    self._radius = 5
```

*Instantiate a custom hand angle predictor.*





### Private functions

#### _calculate_angle_n

```python
def _calculate_angle_n(self) -> int:
    """Calculate the angle at the neutral position.

        :return: (int) angle in degrees

        """
    return 50
```

*Calculate the angle at the neutral position.*

##### Returns

- (*int*) angle in degrees

#### _calculate_angle_b

```python
def _calculate_angle_b(self) -> int:
    """Calculate the angle at the cheek bone position.

        :return: (int) angle in degrees

        """
    return 75
```

*Calculate the angle at the cheek bone position.*

##### Returns

- (*int*) angle in degrees

#### _calculate_angle_c

```python
def _calculate_angle_c(self) -> int:
    """Calculate the angle at the chin position.

        :return: (int) angle in degrees

        """
    return 67
```

*Calculate the angle at the chin position.*

##### Returns

- (*int*) angle in degrees

#### _calculate_angle_m

```python
def _calculate_angle_m(self) -> int:
    """Calculate the angle at the mouse position.

        :return: (int) angle in degrees

        """
    return 73
```

*Calculate the angle at the mouse position.*

##### Returns

- (*int*) angle in degrees

#### _calculate_angle_s

```python
def _calculate_angle_s(self) -> int:
    """Calculate the angle at the side position.

        :return: (int) angle in degrees

        """
    return 83
```

*Calculate the angle at the side position.*

##### Returns

- (*int*) angle in degrees

#### _calculate_angle_t

```python
def _calculate_angle_t(self) -> int:
    """Calculate the angle at the throat position.

        :return: (int) angle in degrees

        """
    return 58
```

*Calculate the angle at the throat position.*

##### Returns

- (*int*) angle in degrees



## Class `WhereAnglePredictorObserved`

### Description

*Predict hand angles with experts rules.*

Observed values are for each measured key on 5 professional cuers:
1 ; b ; 53
2 ; b ; 73
6 ; b ; 57
7 ; b ; 63
8 ; b ; 62
3 ; c ; 64
4 ; c ; 69
5 ; c ; 52
6 ; c ; 51
7 ; c ; 59
1 ; m ; 55
4 ; m ; 56
5 ; m ; 62
6 ; m ; 39
8 ; m ; 70
2 ; s ; 73
3 ; s ; 93
4 ; s ; 90
6 ; s ; 80
7 ; s ; 85
1 ; t ; 48
3 ; t ; 52
4 ; t ; 42
5 ; t ; 57
6 ; t ; 44

Average and standard deviations:
- b: 62.0  (5.3)
- c: 59.0  (6.0)
- m: 56.4  (7.7)
- t: 48.6  (4.7)
- s: 83.0  (5.0)


### Constructor

#### __init__

```python
def __init__(self):
    """Instantiate a custom hand angle predictor.

    """
    super(WhereAnglePredictorObserved, self).__init__()
    self._description = MSG_DESCRIPTION_RULES
    self._radius = 5
```

*Instantiate a custom hand angle predictor.*





### Private functions

#### _calculate_angle_n

```python
def _calculate_angle_n(self) -> int:
    """Calculate the angle at the neutral position.

        :return: (int) angle in degrees

        """
    return 50
```

*Calculate the angle at the neutral position.*

##### Returns

- (*int*) angle in degrees

#### _calculate_angle_b

```python
def _calculate_angle_b(self) -> int:
    """Calculate the angle at the cheek bone position.

        :return: (int) angle in degrees

        """
    return 62
```

*Calculate the angle at the cheek bone position.*

##### Returns

- (*int*) angle in degrees

#### _calculate_angle_c

```python
def _calculate_angle_c(self) -> int:
    """Calculate the angle at the chin position.

        :return: (int) angle in degrees

        """
    return 59
```

*Calculate the angle at the chin position.*

##### Returns

- (*int*) angle in degrees

#### _calculate_angle_m

```python
def _calculate_angle_m(self) -> int:
    """Calculate the angle at the mouse position.

        :return: (int) angle in degrees

        """
    return 56
```

*Calculate the angle at the mouse position.*

##### Returns

- (*int*) angle in degrees

#### _calculate_angle_s

```python
def _calculate_angle_s(self) -> int:
    """Calculate the angle at the side position.

        :return: (int) angle in degrees

        """
    return 83
```

*Calculate the angle at the side position.*

##### Returns

- (*int*) angle in degrees

#### _calculate_angle_t

```python
def _calculate_angle_t(self) -> int:
    """Calculate the angle at the throat position.

        :return: (int) angle in degrees

        """
    return 49
```

*Calculate the angle at the throat position.*

##### Returns

- (*int*) angle in degrees



## Class `WhereAnglePredictorUnified`

### Description

*Predict hand angles with expert rules based on observed values.*

This model was created from observed values in a corpus.
- Collected data: 3769 values
- Filtered data: 3722 values (outliers removed)

Statistics by Hand Position
- b : Mean = 64.29, Std Dev = 7.87
- c : Mean = 61.34, Std Dev = 7.37
- m : Mean = 62.58, Std Dev = 8.12
- s : Mean = 68.49, Std Dev = 11.07
- t : Mean = 54.02, Std Dev = 9.96
=> The position is strongly correlated to the angle.

Statistics by Hand Shape
- 1 : Mean = 63.37, Std Dev = 11.85
- 2 : Mean = 64.03, Std Dev = 10.54
- 3 : Mean = 65.73, Std Dev = 10.89
- 4 : Mean = 66.25, Std Dev = 11.50
- 5 : Mean = 62.38, Std Dev = 10.01
- 6 : Mean = 65.04, Std Dev = 12.08
- 7 : Mean = 60.59, Std Dev = 11.59
- 8 : Mean = 60.98, Std Dev = 9.50
=> The shape has no impact on the angle value.

Statistics by Speaker
- AM: Mean = 63.86, Std Dev = 12.91
- CH: Mean = 73.80, Std Dev = 10.41
- LM: Mean = 61.72, Std Dev = 7.35
- ML: Mean = 56.81, Std Dev = 5.88
- VT: Mean = 65.60, Std Dev = 11.10
=> There is a speaker effect, but it should be accounted for to create
a general model.

Statistics by Condition
- syll: Mean = 61.17, Std Dev = 8.68
- word: Mean = 58.30, Std Dev = 12.72
- sent: Mean = 64.88, Std Dev = 10.05
- text: Mean = 66.11, Std Dev = 10.49
=> The condition affects the angle, possibly by influencing movement
precision; so it should be accounted for to create a general model.


### Constructor

#### __init__

```python
def __init__(self):
    """Instantiate a custom hand angle predictor.

    """
    super(WhereAnglePredictorUnified, self).__init__()
    self._description = MSG_DESCRIPTION_UNIFIED
    self._radius = 5
```

*Instantiate a custom hand angle predictor.*





### Private functions

#### _calculate_angle_n

```python
def _calculate_angle_n(self) -> int:
    """Calculate the angle at the neutral position.

        :return: (int) angle in degrees

        """
    return 45
```

*Calculate the angle at the neutral position.*

##### Returns

- (*int*) angle in degrees

#### _calculate_angle_b

```python
def _calculate_angle_b(self) -> int:
    """Calculate the angle at the cheek bone position.

        :return: (int) angle in degrees

        """
    return 63
```

*Calculate the angle at the cheek bone position.*

##### Returns

- (*int*) angle in degrees

#### _calculate_angle_c

```python
def _calculate_angle_c(self) -> int:
    """Calculate the angle at the chin position.

        :return: (int) angle in degrees

        """
    return 57
```

*Calculate the angle at the chin position.*

##### Returns

- (*int*) angle in degrees

#### _calculate_angle_m

```python
def _calculate_angle_m(self) -> int:
    """Calculate the angle at the mouse position.

        :return: (int) angle in degrees

        """
    return 60
```

*Calculate the angle at the mouse position.*

##### Returns

- (*int*) angle in degrees

#### _calculate_angle_s

```python
def _calculate_angle_s(self) -> int:
    """Calculate the angle at the side position.

        :return: (int) angle in degrees

        """
    return 70
```

*Calculate the angle at the side position.*

##### Returns

- (*int*) angle in degrees

#### _calculate_angle_t

```python
def _calculate_angle_t(self) -> int:
    """Calculate the angle at the throat position.

        :return: (int) angle in degrees

        """
    return 50
```

*Calculate the angle at the throat position.*

##### Returns

- (*int*) angle in degrees





~ Created using [Clamming](https://clamming.sf.net) version 2.1 ~
