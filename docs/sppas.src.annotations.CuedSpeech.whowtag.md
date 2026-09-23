# sppas.src.annotations.CuedSpeech.whowtag module

## List of classes

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



## Class `CuedSpeechVideoTagger`

### Description

*Create a video with hands tagged on the face of a video.*




### Constructor

#### __init__

```python
def __init__(self, cue_rules: CuedSpeechKeys=CuedSpeechKeys()):
    """Create a new instance.

    :param cue_rules: (CuedSpeechKeys) Rules and codes for vowel positions and hand shapes

    """
    self.__gencoords = sppasHandCoordsGenerator()
    self.__video_buffer = sppasVideoReaderBuffer()
    self.__video_writer = sppasBufferVideoWriter()
    self.__video_path = None
    if isinstance(cue_rules, CuedSpeechKeys) is False:
        raise sppasTypeError(type(cue_rules), 'CuedSpeechKeys')
    self.__options = dict()
    for key in CuedSpeechVideoTagger.OPTIONS:
        self.__options[key] = CuedSpeechVideoTagger.OPTIONS[key]
    self._img_vowel_tagger = sppasImageVowelPosTagger(cue_rules)
    self._img_hand_tagger = sppasImageHandTagger(cue_rules)
    self.set_cue_rules(cue_rules)
```

*Create a new instance.*

##### Parameters

- **cue_rules**: (CuedSpeechKeys) Rules and codes for vowel positions and hand shapes



### Public functions

#### set_cue_rules

```python
def set_cue_rules(self, cue_rules: CuedSpeechKeys) -> None:
    """Set the CuedSpeechKeys used to tag the video.

        :param cue_rules: (CuedSpeechKeys) The instance of the cuedSpeechKeys to set
        :raises: : sppasTypeError: If the parameter is not an instance of the CuedSpeechKeys class

        """
    if isinstance(cue_rules, CuedSpeechKeys) is False:
        raise sppasTypeError(cue_rules, 'CuedSpeechKeys')
    self._img_hand_tagger.set_cue_rules(cue_rules)
    self._img_vowel_tagger.set_cue_rules(cue_rules)
    self.__gencoords.set_cue_rules(cue_rules)
```

*Set the CuedSpeechKeys used to tag the video.*

##### Parameters

- **cue_rules**: (CuedSpeechKeys) The instance of the cuedSpeechKeys to set


##### Raises

- **: sppasTypeError: If the parameter is not an instance of the CuedSpeechKeys class

#### load_hands

```python
def load_hands(self, prefix: str) -> None:
    """Load the hand pictures with given name.

        :param prefix: (str) A hand set name (handcue, ...)
        :raises: sppasIOError: If no hands are loaded (not found the hands files)

        """
    success = self._img_hand_tagger.load_hands(prefix)
    if success is False:
        raise sppasIOError(f'Hand pictures with name {prefix} not loaded.')
```

*Load the hand pictures with given name.*

##### Parameters

- **prefix**: (*str*) A hand set name (handcue, ...)


##### Raises

- *sppasIOError*: If no hands are loaded (not found the hands files)

#### load

```python
def load(self, video_path: str) -> None:
    """Open the video.

        Closes automatically the video if already was an open video.

        :param video_path: (str) File path of the input video
        :raises: VideoBrowseError: Can't open/read the video

        """
    self.close()
    self.__video_buffer.open(video_path)
    self.__video_path = video_path
    self.__video_writer.set_fps(self.__video_buffer.get_framerate())
```

*Open the video.*

Closes automatically the video if already was an open video.

##### Parameters

- **video_path**: (*str*) File path of the input video


##### Raises

- *VideoBrowseError*: Can't open/read the video

#### is_loaded

```python
def is_loaded(self) -> bool:
    """Return the information of if a video is loaded or not.

        :return: (bool) True if the buffer is currently opened or False else

        """
    if self.__video_buffer is None:
        return False
    return self.__video_buffer.is_opened()
```

*Return the information of if a video is loaded or not.*

##### Returns

- (*bool*) True if the buffer is currently opened or False else

#### close

```python
def close(self) -> None:
    """Release video streams."""
    self.__video_buffer.close()
    self.__video_writer.close()
```

*Release video streams.*

#### is_opened

```python
def is_opened(self) -> bool:
    """Return the information of if the writer is currently opened.

        :return: (bool) True if the video writer is open or False else.

        """
    return self.__video_writer.is_opened()
```

*Return the information of if the writer is currently opened.*

##### Returns

- (*bool*) True if the video writer is open or False else.

#### set_option

```python
def set_option(self, option_key: str, option_value: object) -> None:
    """Set an option of the video tagger.

        Available options are :
            - handsset
            - handsfilter
            - infotext
            - vowelspos

        :param option_key: (str) Name of the option
        :param option_value: (any) Value of the option
        :raises: AnnotationOptionError: If the given key is unknown

        """
    if option_key in self.__options.keys():
        self.__options[option_key] = option_value
    else:
        raise AnnotationOptionError(option_key)
```

*Set an option of the video tagger.*

Available options are :
- handsset
- handsfilter
- infotext
- vowelspos

##### Parameters

- **option_key**: (*str*) Name of the option
- **option_value**: (any) Value of the option


##### Raises

- *AnnotationOptionError*: If the given key is unknown

#### tag_with_keys

```python
def tag_with_keys(self, transcription: sppasTranscription, output: str) -> list:
    """Tag the video with the given keys.

        The possible tiers of the given transcription are:
            - CS-ShapeProbas: probabilities of the shapes of the hand
            - CS-PosProbas: probabilities of the positions of the hand
            - CS-VowelsCoords: Coordinates of the position of the vowels
            - CS-TargetCoords: Coordinates of the target sight
            - CS-HandAngle: Coordinates of the target sight
            - PhonAlign: Time-aligned phonemes

        The video streams (buffer/writer) are not released... Use close().

        :param transcription: (sppasTranscription) The transcription to use to tag the video.
        :param output: (str) Output video filename
        :raises: sppasError: If no video is load.
        :return: (list) created files -- expected 1

        """
    if self.is_loaded() is False:
        raise sppasError('No video in the buffer. Nothing can be tagged.')
    self.__load_options()
    self.__check_tiers(transcription)
    if self._img_hand_tagger.hand_mode() is True:
        _tagger = self._img_hand_tagger
    else:
        _tagger = None
    hand_coords_tier = self.__gencoords.hands_to_handcoords(transcription.find('CS-ShapeProbas'), transcription.find('CS-TargetCoords'), transcription.find('CS-HandAngle'), transcription.find('CS-FaceHeight'), _tagger)
    result = list()
    index = 0
    nb_buffer = 0
    read_next = True
    self.__video_buffer.seek_buffer(0)
    image_duration = 1.0 / self.__video_buffer.get_framerate()
    while read_next:
        logging.info(f' ... buffer number {nb_buffer + 1}')
        read_next = self.__video_buffer.next()
        start_time = index * image_duration
        self.__tag_buffer(start_time, hand_coords_tier, transcription.find('CS-ShapeProbas'), transcription.find('CS-PosProbas'), transcription.find('CS-VowelsCoords'), transcription.find('PhonAlign'))
        if output is not None:
            new_files = self.__video_writer.write_video(self.__video_buffer, output, '')
            result.extend(new_files)
        nb_buffer += 1
        index += len(self.__video_buffer)
    self.load(self.__video_path)
    return result
```

*Tag the video with the given keys.*

The possible tiers of the given transcription are:
- CS-ShapeProbas: probabilities of the shapes of the hand
- CS-PosProbas: probabilities of the positions of the hand
- CS-VowelsCoords: Coordinates of the position of the vowels
- CS-TargetCoords: Coordinates of the target sight
- CS-HandAngle: Coordinates of the target sight
- PhonAlign: Time-aligned phonemes

The video streams (buffer/writer) are not released... Use close().

##### Parameters

- **transcription**: (sppasTranscription) The transcription to use to tag the video.
- **output**: (*str*) Output video filename


##### Raises

- *sppasError*: If no video is load.


##### Returns

- (*list*) created files -- expected 1

#### get_hands_filters

```python
@staticmethod
def get_hands_filters() -> list:
    """List of all available hands filters.

        :return: (list[str]) A list of all hands filters.

        """
    return ['cartoon', 'sights', 'skeleton', 'sticks']
```

*List of all available hands filters.*

##### Returns

- (*list*[*str*]) A list of all hands filters.

#### get_annotation_index

```python
@staticmethod
def get_annotation_index(tier: sppasTier, timepoint) -> int:
    """Return the index corresponding to the given time point.

        :param tier: (sppasTier) The tier that contains the annotation who searched
        :param timepoint: (sppasPoint or float) The time to search for the index

        :return: (int) The index or -1 if no index associated with the given time point

        """
    if tier is None:
        annotation_index = -1
    elif tier.is_point():
        annotation_index = tier.index(timepoint)
    else:
        annotation_index = tier.mindex(timepoint, bound=2)
    return annotation_index
```

*Return the index corresponding to the given time point.*

##### Parameters

- **tier**: (sppasTier) The tier that contains the annotation who searched
- **timepoint**: (sppasPo*int* or *float*) The time to search for the index

##### Returns

- (*int*) The index or -1 if no index associated with the given time point

#### get_annotation_index_starting_to

```python
@staticmethod
def get_annotation_index_starting_to(tier: sppasTier, timepoint, start_index: int) -> int:
    """Return the next index corresponding to the given time point starting to the start_index parameter.

        :param tier: (sppasTier) The tier that  contains the annotation who searched
        :param timepoint: (sppasPoint or float) The time to search for the index
        :param start_index: (int) The index to start to search for the index

        :return: (int) The next annotation index that corresponding with the given timepoint
                 Or -1 if no annotation found

        """
    if tier is None:
        return -1
    if start_index >= len(tier):
        return -1
    elif start_index <= 0:
        return CuedSpeechVideoTagger.get_annotation_index(tier, timepoint)
    new_index = start_index
    while new_index != -1:
        if tier[new_index].get_lowest_localization() <= timepoint <= tier[new_index].get_highest_localization():
            break
        new_index += 1
        if new_index == len(tier):
            new_index = -1
        if timepoint > tier[new_index].get_highest_localization():
            new_index = -1
    return new_index
```

*Return the next index corresponding to the given time point starting to the start_index parameter.*

##### Parameters

- **tier**: (sppasTier) The tier that  contains the annotation who searched
- **timepoint**: (sppasPo*int* or *float*) The time to search for the index
- **start_index**: (*int*) The index to start to search for the index

##### Returns

- (*int*) The next annotation index that corresponding with the given timepoint Or -1 if no annotation found



### Protected functions

#### __load_options

```python
def __load_options(self) -> None:
    """Check the activated options and load the corresponding resources."""
    hand_set = self.__options.get('handsset')
    if len(hand_set) > 0:
        self.load_hands(hand_set)
        logging.info(f"Successfully loaded the hands set '{hand_set}'.")
        hand_filter = self.__options.get('handsfilter')
        if len(hand_filter) > 0:
            self._img_hand_tagger.apply_hands_filter(hand_filter)
            logging.info(f"Successfully applied the hands filter '{hand_filter}'.")
    else:
        logging.info('No hands set was defined. The video is tagged with badges.')
```

*Check the activated options and load the corresponding resources.*

#### __check_tiers

```python
def __check_tiers(self, transcription: sppasTranscription) -> None:
    """Find the tiers used to tag the video.

        Searched tiers (on the order of the return list):
            - CS-ShapeProbas: probabilities of the shapes of the hand
            - CS-PosProbas: probabilities of the positions of the hand
            - CS-VowelsCoords: Coordinates of the position of the vowels
            - PhonAlign: Time-aligned phonemes

        """
    tiers = list()
    tiers.append(transcription.find('CS-ShapeProbas'))
    if tiers[0] is None:
        logging.error('Missing tier with shape probabilities.')
    tiers.append(transcription.find('CS-PosProbas'))
    if tiers[1] is None:
        logging.error('Missing tier with position probabilities.')
    tiers.append(transcription.find('CS-VowelsCoords'))
    if tiers[2] is None:
        logging.error('Missing tier with vowels coords.')
    tiers.append(transcription.find('PhonAlign'))
    if tiers[3] is None:
        logging.error('Missing tier with time-aligned phonemes.')
    tiers.append(transcription.find('CS-TargetCoords'))
    if tiers[4] is None:
        logging.error('Missing tier with target coordinates.')
    tiers.append(transcription.find('CS-HandAngle'))
    if tiers[5] is None:
        logging.error('Missing tier with angle values.')
    tiers.append(transcription.find('CS-FaceHeight'))
    if tiers[6] is None:
        logging.error('Missing tier with face heights.')
    if None in tiers:
        raise sppasError('At least one of the expected tiers was not found in the transcription. Video tagging is aborted. See logging for details.')
```

*Find the tiers used to tag the video.*

Searched tiers (on the order of the return list):
- CS-ShapeProbas: probabilities of the shapes of the hand
- CS-PosProbas: probabilities of the positions of the hand
- CS-VowelsCoords: Coordinates of the position of the vowels
- PhonAlign: Time-aligned phonemes

#### __tag_buffer

```python
def __tag_buffer(self, start_time: float, coords_tier, shape_tier, pos_tier, vowels_tier, info_tier) -> None:
    """Browse the buffer and tag the images.

        :param start_time: (float) The time when the tag begin
        :param coords_tier: (sppasTier or None) The sights of the hand for the target, S0 and S9
        :param pos_tier: (sppasTier or None) Positions and probabilities (CS-PosProbas)
        :param shape_tier: (sppasTier or None) Shape codes and probabilities (CS-ShapeProbas)
        :param vowels_tier: (sppasTier or None) The vowels positions (CS-VowelsCoords)
        :param info_tier: (sppasTier or None) The phonemes, used to print on the image in debug mode (PhonAlign)

        """
    image_duration = 1.0 / self.__video_buffer.get_framerate()
    radius = 0.0005
    pos_index = shape_index = vowels_index = info_index = coords_index = -1
    (start_buffer_index, _) = self.__video_buffer.get_buffer_range()
    iter_images = self.__video_buffer.__iter__()
    for i in range(len(self.__video_buffer)):
        video_image_number = start_buffer_index + i
        img = next(iter_images)
        if img is None:
            logging.warning('No frame at index {:d}.'.format(video_image_number))
            continue
        img = img.ialpha(254)
        s = start_time + i * image_duration
        middle_time = s + image_duration / 2.0
        point = sppasPoint(middle_time, radius)
        coords_index = self.get_annotation_index_starting_to(coords_tier, point, coords_index)
        pos_index = self.get_annotation_index_starting_to(pos_tier, point, pos_index)
        shape_index = self.get_annotation_index_starting_to(shape_tier, point, shape_index)
        vowels_index = self.get_annotation_index_starting_to(vowels_tier, point, vowels_index)
        info_index = self.get_annotation_index_starting_to(info_tier, point, info_index)
        sights = self.__extract_coords_data(coords_tier, coords_index)
        (shape_text, shapes) = self.__extract_shape_data(shape_tier, shape_index)
        (pos_text, score) = self.__extract_position_data(pos_tier, pos_index)
        vowels_positions = self.__extract_vowels_data(vowels_tier, vowels_index)
        if shape_index != -1 and pos_index != -1 and (len(sights) > 0) and (sights[0] is not None):
            img = self._img_hand_tagger.slap_on(img, shapes, sights)
        if self.__options['vowelspos'] is True and len(vowels_positions) > 0:
            img = self._img_vowel_tagger.slap_on(img, vowels_positions)
        if self.__options['infotext'] is True:
            info_text = 'Info: '
            if info_index != -1:
                info_text += str(round(info_tier[info_index].get_lowest_localization().get_midpoint(), 3))
                info_text += ' '
                info_text += serialize_labels(info_tier[info_index].get_labels())
            frame_text = f'Frame: {video_image_number} ({round(middle_time, 3)},{round(radius, 3)})'
            self.__put_debug_texts(img, [frame_text, shape_text, pos_text, info_text])
        self.__video_buffer.set_at(img.ibgra_to_bgr(), i)
```

*Browse the buffer and tag the images.*

##### Parameters

- **start_time**: (*float*) The time when the tag begin
- **coords_tier**: (sppasTier or None) The sights of the hand for the target, S0 and S9
- **pos_tier**: (sppasTier or None) Positions and probabilities (CS-PosProbas)
- **shape_tier**: (sppasTier or None) Shape codes and probabilities (CS-ShapeProbas)
- **vowels_tier**: (sppasTier or None) The vowels positions (CS-VowelsCoords)
- **info_tier**: (sppasTier or None) The phonemes, used to print on the image in debug mode (PhonAlign)

#### __put_debug_texts

```python
def __put_debug_texts(self, img: sppasImage, texts: list) -> None:
    """Put debug information on the given image.

        :param img: (sppasImage) The image to put the text on it.
        :param texts: (list) The list that contains all texts to put in the image.

        """
    step = 30
    for (i, text) in enumerate(texts):
        img.put_text((100, (i + 1) * step), (10, 10, 10), 1, text)
```

*Put debug information on the given image.*

##### Parameters

- **img**: (sppasImage) The image to put the text on it.
- **texts**: (*list*) The list that contains all texts to put in the image.

#### __extract_coords_data

```python
@staticmethod
def __extract_coords_data(coords_tier, index) -> list:
    """Extract the sights data to compute the hand scale factor.

        If the index equal to -1, this function returns a list of None.

        :param coords_tier: (sppasTier or None) The tier that contains the sights
        :param index: (int) The index of the annotation
        :return: (list) A list of the coords for s0, s9, target

        Example of returned list:
        [sppasFuzzyPoint: (368,780), sppasFuzzyPoint: (432,684), sppasFuzzyPoint: (540,573)]

        """
    sights = [None, None, None]
    if coords_tier is not None and index != -1:
        return coords_tier[index].get_labels()
    return [None, None, None]
```

*Extract the sights data to compute the hand scale factor.*

If the index equal to -1, this function returns a list of None.

##### Parameters

- **coords_tier**: (sppasTier or None) The tier that contains the sights
- **index**: (*int*) The index of the annotation


##### Returns

- (*list*) A list of the coords for s0, s9, target

Example of returned list:
[sppasFuzzyPoint: (368,780), sppasFuzzyPoint: (432,684), sppasFuzzyPoint: (540,573)]

#### __extract_shape_data

```python
@staticmethod
def __extract_shape_data(shape_tier: sppasTier, index: int) -> tuple:
    """Extract the shape data (shapes codes and scores) from a shape tier.

        :param shape_tier: (sppasTier) The tier that contains our shape data
        :param index: (int) The index of the annotation
        :return: (str, list) The shape text information and the list of shapes codes and scores

        """
    shape_text = 'Shape: '
    shapes = list()
    for shape_label in shape_tier[index].get_labels():
        for (tag, score) in shape_label:
            shape_code = tag.get_typed_content()
            if score is None:
                score = 1.0
            shape_text += shape_code
            shapes.append((shape_code, score))
    return (shape_text, shapes)
```

*Extract the shape data (shapes codes and scores) from a shape tier.*

##### Parameters

- **shape_tier**: (sppasTier) The tier that contains our shape data
- **index**: (*int*) The index of the annotation


##### Returns

- (*str*, *list*) The shape text information and the list of shapes codes and scores

#### __extract_position_data

```python
@staticmethod
def __extract_position_data(pos_tier, index: int) -> tuple:
    """Extract the position data from the position tiers.

        :param pos_tier: (sppasTier or None) The tier that contains the positions text information
        :param index: (int) The index of the annotation
        :return: (str) The position text information and the position probability

        """
    pos_text = 'Pos: '
    score = 1
    if pos_tier is not None:
        for pos_label in pos_tier[index].get_labels():
            score = pos_label.get_score(pos_label.get_best())
            for (tag, score) in pos_label:
                pos_text += tag.get_typed_content()
    return (pos_text, score)
```

*Extract the position data from the position tiers.*

##### Parameters

- **pos_tier**: (sppasTier or None) The tier that contains the positions text information
- **index**: (*int*) The index of the annotation


##### Returns

- (*str*) The position text information and the position probability

#### __extract_vowels_data

```python
@staticmethod
def __extract_vowels_data(vowels_tier, index: int) -> list:
    """Extract the vowels data from the vowels tier.

        If the vowels tier is None or the index equal to -1 return an empty list by default.

        :param vowels_tier: (sppasTier or None) The tier that contains our vowels data
        :param index: (int) The index of the annotation
        :return: (list) A list of all vowels positions

        """
    vowels_positions = list()
    if vowels_tier is not None and index != -1:
        for vowel_label in vowels_tier[index].get_labels():
            pos = vowel_label.get_best().get_typed_content()
            vowels_positions.append(pos)
    return vowels_positions
```

*Extract the vowels data from the vowels tier.*

If the vowels tier is None or the index equal to -1 return an empty list by default.

##### Parameters

- **vowels_tier**: (sppasTier or None) The tier that contains our vowels data
- **index**: (*int*) The index of the annotation


##### Returns

- (*list*) A list of all vowels positions



### Overloads

#### __del__

```python
def __del__(self):
    self.close()
```







~ Created using [Clamming](https://github.com/brigitte-bigi/ClammingPy) version 3.3 ~
