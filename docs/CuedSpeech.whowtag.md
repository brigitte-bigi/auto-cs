# CuedSpeech.whowtag module

## List of classes

## Class `sppasHandFilters`

### Constructor

#### __init__

```python
def __init__(self, *args, **kwargs):
    raise sppasError("The hand filters can't be used. No hands available.")
```





## Class `CuedSpeechVideoTagger`

### Constructor

#### __init__

```python
def __init__(self, *args, **kwargs):
    raise sppasError("The 'resources/cuedspeech' folder doesn't contains any hand-set.")
```





### Public functions

#### get_hands_filters

```python
@staticmethod
def get_hands_filters() -> list:
    return []
```







~ Created using [Clamming](https://github.com/brigitte-bigi/ClammingPy) version 3.3 ~
