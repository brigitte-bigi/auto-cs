# CuedSpeech.wherecue module

## List of classes

## Class `sppasWhereCuedSightsValueError`

### Description

*:ERROR 1332:.*

{:d} sights were expected for a face but got {:d}.


### Constructor

#### __init__

```python
def __init__(self, value, frame):
    self._status = 1332
    self.parameter = error(self._status) + error(self._status, 'annotations').format(value, frame)
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





## Class `sppasFaceHeight`

### Description

*Estimate a smoothed height of the face from its 2D sights.*




### Public functions

#### eval_height

```python
@staticmethod
def eval_height(face_sights):
    """Estimate the size coefficient of the given face using facial landmarks.

        This method computes a face size coefficient based on three facial sights:
        points 19 and 24 (which define a segment across the face), and point 8
        (typically the chin).

        It calculates the midpoint between points 19 and 24, then returns the
        Euclidean distance from this midpoint to point 8. This value is useful
        for normalizing hand size relative to face size in images.

        :param face_sights: (sppasSights) The facial landmarks (68 points expected).
        :return: (float) A coefficient representing the size of the given face.
        :raises: sppasTypeError: Invalid given face sights argument
        :raises: sppasError: Invalid number of given face sights

        """
    if isinstance(face_sights, sppasSights) is False:
        raise sppasTypeError(type(face_sights), 'sppasSights')
    if len(face_sights) != 68:
        raise sppasError(f'Invalid number of sights. Expected 68. Got {len(face_sights)} instead')
    _dx = abs(face_sights.x(19) - face_sights.x(24))
    _dy = abs(face_sights.y(19) - face_sights.y(24))
    _x = float(face_sights.x(19)) + _dx / 2.0
    _y = float(face_sights.y(19)) + _dy / 2.0
    return euclidian((_x, _y), (face_sights.x(8), face_sights.y(8)))
```

*Estimate the size coefficient of the given face using facial landmarks.*

This method computes a face size coefficient based on three facial sights:
points 19 and 24 (which define a segment across the face), and point 8
(typically the chin).

It calculates the midpoint between points 19 and 24, then returns the
Euclidean distance from this midpoint to point 8. This value is useful
for normalizing hand size relative to face size in images.

##### Parameters

- **face_sights**: (sppasSights) The facial landmarks (68 points expected).


##### Returns

- (*float*) A coefficient representing the size of the given face.


##### Raises

- *sppasTypeError*: Invalid given face sights argument
- *sppasError*: Invalid number of given face sights



## Class `TargetProbabilitiesEstimator`

### Description

*Generate the probabilities of the targets (pos&shape).*

For each image of the video (each interval in vowels_coords tier), an
interval with the probability of the shape, and another one with the
probability of the position are estimated.


### Constructor

#### __init__

```python
def __init__(self, cue_rules: CuedSpeechCueingRules=CuedSpeechCueingRules()):
    """Create a new instance.

    :param cue_rules: (CuedSpeechKeys) Rules and codes for vowel positions and hand shapes

    """
    self.__cued = None
    self._vrank = ()
    self.set_cue_rules(cue_rules)
```

*Create a new instance.*

##### Parameters

- **cue_rules**: (CuedSpeechKeys) Rules and codes for vowel positions and hand shapes



### Public functions

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
    self._vrank = tuple(self.__cued.get_vowels_codes())
```

*Set new rules.*

##### Parameters

- **cue_rules**: (CuedSpeechKeys) Rules and codes for vowel positions and hand shapes


##### Raises

- *sppasTypeError*: given parameter is not CuedSpeechCueingRules

#### positions_discretization

```python
def positions_discretization(self, tier_pos_coords, tier_pos_transitions):
    """Generate the probabilities of the positions for each annotation in tier_pos_coords.

        Discretizing the transitions between a position to the next 
        one implies to assign a probability to the source and to the 
        destination during the whole transition time.

        :param tier_pos_coords: (sppasTier) Tier with coordinates of the vowel positions and neutral
        :param tier_pos_transitions: (sppasTier) Tier with transition intervals between vowels
        :return: (sppasTier) Tier "CS-PosProbas" with probabilities for each position 

        """
    pos_tier = sppasTier('CS-PosProbas')
    pos_probas = self.__discretize_positions(tier_pos_transitions, tier_pos_coords)
    if len(pos_probas) != len(tier_pos_coords):
        raise Exception('Target vowels probas estimation: {:d} != {:d}'.format(len(pos_probas), len(tier_pos_coords)))
    for (i, ann) in enumerate(tier_pos_coords):
        loc = ann.get_location()
        (tags, scores) = self.__probas_to_lists(pos_probas[i])
        label = sppasLabel(None)
        for t in range(len(tags)):
            label.append(tags[t], score=scores[t], add=False)
        pos_tier.create_annotation(loc.copy(), [label])
    return pos_tier
```

*Generate the probabilities of the positions for each annotation in tier_pos_coords.*

Discretizing the transitions between a position to the next
one implies to assign a probability to the source and to the
destination during the whole transition time.

##### Parameters

- **tier_pos_coords**: (sppasTier) Tier with coordinates of the vowel positions and neutral
- **tier_pos_transitions**: (sppasTier) Tier with transition intervals between vowels


##### Returns

- (sppasTier) Tier "CS-PosProbas" with probabilities for each position

#### shapes_discretization

```python
def shapes_discretization(self, tier_pos_coords, tier_shapes_transitions):
    """Generate the probabilities of the shapes for each annotation in tier_pos_coords.

        Discretizing the transitions between a shape to the next 
        one implies to assign a probability to the source and to the 
        destination during the whole transition time.

        :param tier_pos_coords: (sppasTier) Tier with coordinates of the vowel positions and neutral
        :param tier_shapes_transitions: (sppasTier) Tier with transition intervals between shapes
        :return: (sppasTier) Tier "CS-ShapeProbas" with probabilities for each shape 

        """
    shape_tier = sppasTier('CS-ShapeProbas')
    shape_probas = self.__discretize_shapes(tier_shapes_transitions, tier_pos_coords)
    if len(shape_probas) != len(tier_pos_coords):
        raise Exception('Target consonants probas estimation: {:d} != {:d}'.format(len(shape_probas), len(tier_pos_coords)))
    for (i, ann) in enumerate(tier_pos_coords):
        loc = ann.get_location()
        (tags, scores) = self.__probas_to_lists(shape_probas[i])
        label = sppasLabel(None)
        for t in range(len(tags)):
            label.append(tags[t], score=scores[t], add=False)
        shape_tier.create_annotation(loc.copy(), [label])
    return shape_tier
```

*Generate the probabilities of the shapes for each annotation in tier_pos_coords.*

Discretizing the transitions between a shape to the next
one implies to assign a probability to the source and to the
destination during the whole transition time.

##### Parameters

- **tier_pos_coords**: (sppasTier) Tier with coordinates of the vowel positions and neutral
- **tier_shapes_transitions**: (sppasTier) Tier with transition intervals between shapes


##### Returns

- (sppasTier) Tier "CS-ShapeProbas" with probabilities for each shape

#### hands_to_target_coords

```python
def hands_to_target_coords(self, hand_pos_probas, vowels_coords):
    """Generate the coordinates of the target finger.

        :param hand_pos_probas: (sppasTier) Tier with hand position probabilities
        :param vowels_coords: (sppasTier) Tier with coordinates of the vowels and neutral
        :return: (sppasTier) CS-TargetCoords

        """
    position_coords = self.__eval_hand_target_coords_straight(hand_pos_probas, vowels_coords)
    if len(position_coords) != len(vowels_coords):
        raise Exception('Target vowels coords estimation: {:d} != {:d}'.format(len(position_coords), len(vowels_coords)))
    pos_tier = sppasTier('CS-TargetCoords')
    for (i, ann) in enumerate(vowels_coords):
        loc = ann.get_location()
        if len(position_coords[i]) == 1:
            (x, y, r) = position_coords[i][0][0]
            label_pos = sppasLabel(sppasTag((x, y, r), tag_type='point'))
        elif len(position_coords[i]) == 2:
            pos1 = position_coords[i][0]
            (x1, y1, r1) = pos1[0]
            tag1 = sppasTag((x1, y1, r1), tag_type='point')
            pos2 = position_coords[i][1]
            (x2, y2, r2) = pos2[0]
            tag2 = sppasTag((x2, y2, r2), tag_type='point')
            label_pos = sppasLabel([tag1, tag2], [pos1[1], pos2[1]])
        else:
            label_pos = sppasLabel(None)
        pos_tier.create_annotation(loc.copy(), [label_pos])
    return pos_tier
```

*Generate the coordinates of the target finger.*

##### Parameters

- **hand_pos_probas**: (sppasTier) Tier with hand position probabilities
- **vowels_coords**: (sppasTier) Tier with coordinates of the vowels and neutral


##### Returns

- (sppasTier) CS-TargetCoords



### Protected functions

#### __discretize_positions

```python
def __discretize_positions(self, hand_pos, vowels_coords_tier):
    """Return proba of the hand position for each ann in given tier.

        :return: (sppasTier)

        """
    positions = list()
    cur_pos = [self.__cued.get_neutral_vowel()]
    i = 0
    while i < len(vowels_coords_tier):
        loc = vowels_coords_tier[i].get_location().get_best()
        new_content = self.__get_label_contents_at(hand_pos, loc)
        if new_content is None:
            if len(cur_pos) == 2:
                cur_pos.pop(0)
        else:
            cur_pos = new_content
        c1 = cur_pos[0]
        if len(cur_pos) == 1:
            positions.append(((c1, 1.0),))
            i += 1
        else:
            c2 = cur_pos[1]
            new_pos = cur_pos
            nb_img = 0
            while new_pos == cur_pos:
                if i + nb_img == len(vowels_coords_tier):
                    break
                nb_img += 1
                if i + nb_img == len(vowels_coords_tier):
                    break
                loc = vowels_coords_tier[i + nb_img].get_location().get_best()
                new_pos = self.__get_label_contents_at(hand_pos, loc)
            if nb_img == 1:
                p2 = 0.65
            elif nb_img == 2:
                p2 = 0.4
            else:
                p_step_straight = 1.0 / float(nb_img)
                p2 = max(0.1, p_step_straight)
            positions.append(((c1, 1.0 - p2), (c2, p2)))
            i += 1
            proba_step = (1.0 - p2) / float(nb_img + 1)
            for j in range(1, nb_img):
                proba_pos2 = p2 + round((j + 1) * proba_step, 2)
                positions.append(((c1, 1 - proba_pos2), (c2, proba_pos2)))
                i += 1
    return positions
```

*Return proba of the hand position for each ann in given tier.*

##### Returns

- (sppasTier)

#### __discretize_shapes

```python
def __discretize_shapes(self, hand_shapes, vowels_coords_tier):
    """Return proba of the hand shape for each ann in given tier.

        :return: (sppasTier)

        """
    shapes = list()
    cur_shape = [self.__cued.get_neutral_consonant()]
    i = 0
    while i < len(vowels_coords_tier):
        loc = vowels_coords_tier[i].get_location().get_best()
        new_content = self.__get_label_contents_at(hand_shapes, loc)
        if new_content is None:
            if len(cur_shape) == 2:
                cur_shape.pop(0)
        else:
            cur_shape = new_content
        c1 = cur_shape[0]
        if len(cur_shape) == 1:
            shapes.append(((c1, 1.0),))
            i += 1
        else:
            c2 = cur_shape[1]
            new_shape = cur_shape
            nb_img = 0
            while new_shape == cur_shape:
                if i + nb_img == len(vowels_coords_tier):
                    break
                nb_img += 1
                if i + nb_img == len(vowels_coords_tier):
                    break
                loc = vowels_coords_tier[i + nb_img].get_location().get_best()
                new_shape = self.__get_label_contents_at(hand_shapes, loc)
            if nb_img == 1:
                shapes.append(((c1, 0.25), (c2, 0.75)))
                i += 1
            elif nb_img == 2:
                shapes.append(((c1, 0.45), (c2, 0.55)))
                shapes.append(((c1, 0.15), (c2, 0.85)))
                i += 2
            elif nb_img == 3:
                shapes.append(((c1, 0.6), (c2, 0.4)))
                shapes.append(((c1, 0.25), (c2, 0.75)))
                shapes.append(((c1, 0.1), (c2, 0.9)))
                i += 3
            else:
                p = 0.35
                shapes.append(((c1, 1.0 - p), (c2, p)))
                i += 1
                proba_step = (1.0 - p) / float(nb_img)
                for j in range(1, nb_img - 2):
                    proba_shape1 = p + round((j + 1) * proba_step, 2)
                    proba_shape0 = 1.0 - proba_shape1
                    shapes.append(((c1, proba_shape0), (c2, proba_shape1)))
                    i += 1
                proba_shape1 = 1.0 - proba_step / 2.0
                proba_shape0 = 1.0 - proba_shape1
                shapes.append(((c1, proba_shape0), (c2, proba_shape1)))
                i += 1
                proba_shape1 = 1.0 - proba_step / 4.0
                proba_shape0 = 1.0 - proba_shape1
                shapes.append(((c1, proba_shape0), (c2, proba_shape1)))
                i += 1
    return shapes
```

*Return proba of the hand shape for each ann in given tier.*

##### Returns

- (sppasTier)

#### __eval_hand_target_coords_straight

```python
def __eval_hand_target_coords_straight(self, hand_pos_probas, vowels_coords_tier):
    """Return coords of the hand position for each ann in given tier.

        Coordinates are following a straight line to go from a position to
        the next one. It is ignoring the fact that keys have a different
        target finger: it is a straight line from a target position to the
        next one.

        :return: (list)

        """
    pos_coords = list()
    for i in range(len(hand_pos_probas)):
        labels = vowels_coords_tier[i].get_labels()
        vowels_coords = [label.get_best().get_typed_content() for label in labels]
        cur_vowels = list()
        cur_probas = list()
        for label in hand_pos_probas[i].get_labels():
            for (tag, score) in label:
                cur_vowels.append(tag.get_content())
                cur_probas.append(score)
        from_vowel_idx = self._vrank.index(cur_vowels[0])
        coord1 = vowels_coords[from_vowel_idx]
        (x1, y1) = coord1.get_midpoint()
        r1 = coord1.get_radius()
        if len(cur_vowels) == 1:
            pos_coords.append([((x1, y1, r1), 1.0)])
        elif len(cur_vowels) == 2:
            try:
                to_vowel_idx = self._vrank.index(cur_vowels[1])
            except ValueError:
                logging.error('Unknown vowel: {}'.format(cur_vowels[1]))
                continue
            coord2 = vowels_coords[to_vowel_idx]
            (x2, y2) = coord2.get_midpoint()
            r2 = coord2.get_radius()
            if from_vowel_idx == to_vowel_idx and r2 is not None:
                if cur_probas[0] > cur_probas[1]:
                    x2 = x2 - r2
                    y2 = y2 + r2
                else:
                    x1 = x1 - r2
                    y1 = y1 + r2
            dx = x2 - x1
            dy = y2 - y1
            x = x1 + int(float(dx) * cur_probas[1])
            y = y1 + int(float(dy) * cur_probas[1])
            r = 1
            if r1 is not None and r2 is not None:
                dr = r2 - r1
                r = r1 + int(float(dr) * cur_probas[1])
            pos_coords.append([((x, y, r), 1.0)])
        else:
            pos_coords.append([])
            logging.error('No vowel at index {:d}'.format(i))
    return pos_coords
```

*Return coords of the hand position for each ann in given tier.*

Coordinates are following a straight line to go from a position to
the next one. It is ignoring the fact that keys have a different
target finger: it is a straight line from a target position to the
next one.

##### Returns

- (*list*)

#### __eval_hand_target_coords_fixed

```python
def __eval_hand_target_coords_fixed(self, hand_pos_probas, vowels_coords_tier):
    """Return coords of the hand position for each ann in given tier.

        The hand does not move from a position to the next one.
        Its position is the one of the vowel.

        :return: (list)

        """
    pos_coords = list()
    for i in range(len(hand_pos_probas)):
        labels = vowels_coords_tier[i].get_labels()
        vowels_coords = [label.get_best().get_typed_content() for label in labels]
        cur_vowels = list()
        cur_probas = list()
        for label in hand_pos_probas[i].get_labels():
            for (tag, score) in label:
                cur_vowels.append(tag.get_content())
                cur_probas.append(score)
        from_vowel_idx = self._vrank.index(cur_vowels[0])
        coord1 = vowels_coords[from_vowel_idx]
        (x1, y1) = coord1.get_midpoint()
        r1 = coord1.get_radius()
        if len(cur_vowels) == 1:
            pos_coords.append([((x1, y1, r1), 1.0)])
        elif len(cur_vowels) == 2:
            to_vowel_idx = self._vrank.index(cur_vowels[1])
            coord2 = vowels_coords[to_vowel_idx]
            (x2, y2) = coord2.get_midpoint()
            r2 = coord2.get_radius()
            if from_vowel_idx == to_vowel_idx:
                xm = x2 - r2
                ym = y2 + r2
                pos_coords.append([((xm, ym, r2), cur_probas[1])])
            else:
                pos_coords.append([((x1, y1, r1), cur_probas[0]), ((x2, y2, r2), cur_probas[1])])
        else:
            pos_coords.append([])
            logging.error('No vowel at index {:d}'.format(i))
    return pos_coords
```

*Return coords of the hand position for each ann in given tier.*

The hand does not move from a position to the next one.
Its position is the one of the vowel.

##### Returns

- (*list*)

#### __create_tier

```python
def __create_tier(self, transition_tier, vowels_coords, consonant=True):
    """Create a tier with a content for each given vowels coords."""
    if consonant is True:
        tier = sppasTier('CS-Shapes')
        cur_content = [self.__cued.get_neutral_consonant()]
    else:
        tier = sppasTier('CS-Positions')
        cur_content = [self.__cued.get_neutral_vowel()]
    for ann in vowels_coords:
        loc = ann.get_location().get_best()
        new_content = self.__get_label_contents_at(transition_tier, loc)
        if new_content is None:
            if len(cur_content) == 2:
                cur_content.pop(0)
        labels = [sppasLabel(sppasTag(c)) for c in cur_content]
        tier.create_annotation(ann.get_location().copy(), labels)
    return tier
```

*Create a tier with a content for each given vowels coords.*

#### __get_label_contents_at

```python
@staticmethod
def __get_label_contents_at(tier, point):
    """Return the list of label contents of the annotation at the given moment."""
    content = None
    ann_idx = tier.mindex(point, bound=2)
    if ann_idx != -1:
        labels = tier[ann_idx].get_labels()
        if len(labels) == 1:
            content = [labels[0].get_best().get_content()]
        elif len(labels) == 2:
            c1 = labels[0].get_best().get_content()
            c2 = labels[1].get_best().get_content()
            content = [c1, c2]
        else:
            raise ValueError('One or two labels were expected. Got {:d} instead.'.format(len(labels)))
    return content
```

*Return the list of label contents of the annotation at the given moment.*

#### __probas_to_lists

```python
@staticmethod
def __probas_to_lists(probas):
    """Return the tags and scores of the given list of probabilities."""
    tags = list()
    scores = list()
    for s in probas:
        tags.append(sppasTag(s[0]))
        scores.append(s[1])
    return (tags, scores)
```

*Return the tags and scores of the given list of probabilities.*



## Class `BaseWhereModelPredictor`

### Description

*Base class for any multi-models predictor.*




### Constructor

#### __init__

```python
def __init__(self, *args):
    """Create a hand transitions predictor.

    :param version_number: (int) Version of the predictor system.

    """
    self._models = dict()
    self._model = None
    self._version = BaseWhereModelPredictor.DEFAULT_VERSION
```

*Create a hand transitions predictor.*

##### Parameters

- **version_number**: (*int*) Version of the predictor system.



### Public functions

#### version_numbers

```python
def version_numbers(self) -> list:
    """Return the whole list of supported version numbers."""
    return list(self._models.keys())
```

*Return the whole list of supported version numbers.*

#### get_version_number

```python
def get_version_number(self) -> int:
    """Return the version number of the selected predictor (int)."""
    return self._version
```

*Return the version number of the selected predictor (int).*

#### set_version_number

```python
def set_version_number(self, version_number: int) -> None:
    """Change the predictor version number.

        :param version_number: (int) One of the supported versions.
        :raises: sppasKeyError: if invalid version number
        :raises: sppasTypeError: invalid type for given version_number

        """
    try:
        v = int(version_number)
    except ValueError:
        raise sppasTypeError('int', str(type(version_number)))
    authorized = self.version_numbers()
    try:
        if v not in authorized:
            raise sppasKeyError(str(authorized), version_number)
    except ValueError:
        logging.error('{}: Invalid predictor version {}. Expected one of: {}'.format(self.__name__, version_number, authorized))
        raise sppasKeyError(str(authorized), version_number)
    self._version = v
    self._model = self._models[self._version]()
```

*Change the predictor version number.*

##### Parameters

- **version_number**: (*int*) One of the supported versions.


##### Raises

- *sppasKeyError*: if invalid version number
- *sppasTypeError*: invalid type for given version_number

#### vowel_codes

```python
def vowel_codes(self) -> tuple:
    """Return the list of vowel codes the class can predict.

        """
    if self._model is None:
        return ()
    if hasattr(self._model, 'vowel_codes') is False:
        return ()
    return self._model.vowel_codes()
```

*Return the list of vowel codes the class can predict.*





## Class `WhereVowelPositionsPredictor`

### Description

*Predict the coordinates of vowels from 2D sights of a face.*




### Constructor

#### __init__

```python
def __init__(self, version_number: int=DEFAULT_VERSION):
    """Create a hand transitions predictor.

    :param version_number: (int) Version of the predictor system ranging (0-3).

    """
    super(WhereVowelPositionsPredictor, self).__init__()
    self._models[0] = BaseWherePositionPredictor
    self._models[1] = WherePositionPredictorCustoms
    self._models[2] = WherePositionPredictorObserved
    self._models[3] = WherePositionPredictorUnified
    self.set_version_number(version_number)
```

*Create a hand transitions predictor.*

##### Parameters

- **version_number**: (*int*) Version of the predictor system ranging (0-3).



### Public functions

#### get_sights_dim

```python
def get_sights_dim(self):
    """Return the number of sights this predictor was trained for."""
    return self._model.get_sights_dim()
```

*Return the number of sights this predictor was trained for.*

#### set_sights_and_predict_coords

```python
def set_sights_and_predict_coords(self, sights: sppasSights=None, vowels: tuple=None):
    """Set the sights of a face and predict all vowel positions.

        If no sights are provided, it uses default sights. It validates the
        input type and the number of sights before setting them and predicting
        vowel coordinates.

        :param sights: (sppasSights | None)
        :param vowels: (tuple | None) List of vowel position names. Default is all known ones.
        :raises: sppasTypeError: given parameter is not a sppasSights type.
        :raises: NotImplementedError: not the expected number of sights

        """
    if self._model is None:
        raise sppasCuedPredictorError
    self._model.set_sights_and_predict_coords(sights, vowels)
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

#### predict_vowels_coords

```python
def predict_vowels_coords(self, vowels=('n',)) -> None:
    """Estimate the absolute position of all the vowels.

        Estimate the absolute positions of specified vowels relative to the
        sights of a face. It uses predefined coordinates and calculations
        to determine these positions and stores them in a dictionary.
        Sights must be set before using this method.

        :param vowels: (tuple) List of vowel position names. If unknown, 'n' is used instead.
        :raises: sppasKeyError: Invalid given vowel code.

        """
    self._model.predict_vowels_coords(vowels)
```

*Estimate the absolute position of all the vowels.*

Estimate the absolute positions of specified vowels relative to the
sights of a face. It uses predefined coordinates and calculations
to determine these positions and stores them in a dictionary.
Sights must be set before using this method.

##### Parameters

- **vowels**: (*tuple*) List of vowel position names. If unknown, 'n' is used instead.


##### Raises

- *sppasKeyError*: Invalid given vowel code.

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
    return self._model.get_vowel_coords(vowel)
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



## Class `sppasWherePositionsPredictor`

### Description

*Predict the position of all the vowels from sights in a file.*

Create a tier indicating the position of CS vowels.


### Constructor

#### __init__

```python
def __init__(self, predictor_version=WhereVowelPositionsPredictor.DEFAULT_VERSION):
    """Create a new instance of vowels predictor.

    """
    self.__predictor = WhereVowelPositionsPredictor(predictor_version)
    self.__data_sights = list()
```

*Create a new instance of vowels predictor.*





### Public functions

#### version_numbers

```python
def version_numbers(self) -> list:
    """Return the whole list of supported version numbers."""
    return self.__predictor.version_numbers()
```

*Return the whole list of supported version numbers.*

#### get_version_number

```python
def get_version_number(self) -> int:
    """Return the version number of the selected predictor (int)."""
    return self.__predictor.get_version_number()
```

*Return the version number of the selected predictor (int).*

#### set_version_number

```python
def set_version_number(self, version_number: int) -> None:
    """Change the predictor version number.

        :param version_number: (int) One of the supported versions.
        :raises: sppasKeyError: if invalid version number

        """
    self.__predictor.set_version_number(version_number)
```

*Change the predictor version number.*

##### Parameters

- **version_number**: (*int*) One of the supported versions.


##### Raises

- *sppasKeyError*: if invalid version number

#### get_nb_sights

```python
def get_nb_sights(self) -> int:
    """Return the number of sights."""
    return len(self.__data_sights)
```

*Return the number of sights.*

#### set_sights

```python
def set_sights(self, data_sights: list) -> None:
    """Load a filename and store the sights of a given kid.

        The given data is a list of tuples with:

        - at index 0: midpoint time value
        - at index 1: radius time value
        - at index 2: the 68 sights of a face

        :param data_sights: (list) List of sights of a face
        :raises: TypeError: if data_sights is not a list
        :raises: TypeError: if data_sights is not a list of tuples
        :raises: sppasWhereCuedSightsValueError: there are sights but there are not of the expected size

        """
    if isinstance(data_sights, (list, tuple)) is True:
        for s in data_sights:
            if isinstance(s, (tuple, list)) is False or len(s) != 3:
                raise TypeError('Invalid item in the list of sights: {:s}'.format(str(s)))
            cur_sights = s[2]
            if cur_sights is not None and len(cur_sights) != self.__predictor.get_sights_dim():
                raise sppasWhereCuedSightsValueError(self.__predictor.get_sights_dim(), len(cur_sights))
        self.__data_sights = data_sights
    else:
        raise TypeError('Invalid given sights. Expected a list. Got {:s}'.format(str(type(data_sights))))
```

*Load a filename and store the sights of a given kid.*

The given data is a list of tuples with:

- at index 0: midpoint time value
- at index 1: radius time value
- at index 2: the 68 sights of a face

##### Parameters

- **data_sights**: (*list*) List of sights of a face


##### Raises

- *TypeError*: if data_sights is not a list
- *TypeError*: if data_sights is not a list of tuples
- *sppasWhereCuedSightsValueError*: there are sights but there are not of the expected size

#### vowels_coords

```python
def vowels_coords(self, vowels: list, smooth_len: int=20):
    """Predict the coordinates of the given vowels.

        Notice that the coordinates of the position can have negative values.

        The 'smooth_len' variable is used to smooth the coordinates in order to
        eliminate micro-movements caused by the imprecision in detecting points
        and facial movements, preventing any visible 'shaking'.

        :param smooth_len: (int) Length of the queue used to smooth coords.
        :param vowels: (None | list) List of the vowel codes to predict.
        :return: (sppasTier) tier with name 'CS-VowelsCoords'

        """
    tier = sppasTier('CS-VowelsCoords')
    if vowels is None:
        vowels = self.__predictor.vowel_codes()
    points_x = dict()
    points_y = dict()
    points_r = dict()
    for vowel in vowels:
        points_x[vowel] = deque(maxlen=smooth_len)
        points_y[vowel] = deque(maxlen=smooth_len)
        points_r[vowel] = deque(maxlen=smooth_len)
    for (midpoint, radius, sights) in self.__data_sights:
        self.__predictor.set_sights_and_predict_coords(sights, vowels)
        labels = list()
        for vowel in vowels:
            if vowel in self.__predictor.vowel_codes():
                (x, y, r) = self.__predictor.get_vowel_coords(vowel)
                x = self.__append_and_smooth(points_x[vowel], x)
                y = self.__append_and_smooth(points_y[vowel], y)
                r = self.__append_and_smooth(points_r[vowel], r)
                tag = sppasTag((x, y, r), tag_type='point')
                label = sppasLabel(tag)
                label.set_key(vowel)
                labels.append(label)
        loc = sppasLocation(sppasPoint(midpoint, radius))
        tier.create_annotation(loc, labels)
    return tier
```

*Predict the coordinates of the given vowels.*

Notice that the coordinates of the position can have negative values.

The 'smooth_len' variable is used to smooth the coordinates in order to
eliminate micro-movements caused by the imprecision in detecting points
and facial movements, preventing any visible 'shaking'.

##### Parameters

- **smooth_len**: (*int*) Length of the queue used to smooth coords.
- **vowels**: (None | *list*) List of the vowel codes to predict.


##### Returns

- (sppasTier) tier with name 'CS-VowelsCoords'



### Protected functions

#### __append_and_smooth

```python
@staticmethod
def __append_and_smooth(deck: deque, value: int):
    """Append into the queue and return the smoothed value.

        """
    deck.append(value)
    if len(deck) > 1:
        return int(fmean(deck))
    return value
```

*Append into the queue and return the smoothed value.*





## Class `sppasWhereAnglesPredictor`

### Description

*Predict the angle of the wrist at all vowel positions.*

Create a tier indicating the angles.


### Constructor

#### __init__

```python
def __init__(self, predictor_version=WhereAnglesPredictor.DEFAULT_VERSION):
    """Create a new instance of angles predictor.

    """
    self.__predictor = WhereAnglesPredictor(predictor_version)
```

*Create a new instance of angles predictor.*





### Public functions

#### version_numbers

```python
def version_numbers(self) -> list:
    """Return the whole list of supported version numbers."""
    return self.__predictor.version_numbers()
```

*Return the whole list of supported version numbers.*

#### get_version_number

```python
def get_version_number(self) -> int:
    """Return the version number of the selected predictor (int)."""
    return self.__predictor.get_version_number()
```

*Return the version number of the selected predictor (int).*

#### set_version_number

```python
def set_version_number(self, version_number: int) -> None:
    """Change the predictor version number.

        :param version_number: (int) One of the supported versions.
        :raises: sppasKeyError: if invalid version number

        """
    self.__predictor.set_version_number(version_number)
```

*Change the predictor version number.*

##### Parameters

- **version_number**: (*int*) One of the supported versions.


##### Raises

- *sppasKeyError*: if invalid version number

#### get_use_face

```python
def get_use_face(self) -> bool:
    """Return True if the hand angle must be corrected by the one of the face."""
    return self.__predictor.use_face
```

*Return True if the hand angle must be corrected by the one of the face.*

#### set_use_face

```python
def set_use_face(self, value: bool) -> None:
    """The angle of the hand is corrected by the one of the face or not.

        :param value: (bool) True if the angle of the hand has to be corrected.

        """
    self.__predictor.use_face = value
```

*The angle of the hand is corrected by the one of the face or not.*

##### Parameters

- **value**: (*bool*) True if the angle of the hand has to be corrected.

#### hand_angles

```python
def hand_angles(self, tier_pos: sppasTier, face_sights: sppasTier=None):
    """Predict the angles for the given vowels.

        Notice that the coordinates of the position can have negative values.

        :param tier_pos: (sppasTier) Coordinates of the vowel positions.
        :param face_sights: (sppasTier) Sights of the face corresponding to each vowel.
        :return: (sppasTier) tier with name 'CS-HandAngle'

        """
    angles = self.__eval_hand_angle(tier_pos, face_sights)
    angles_tier = sppasTier('CS-HandAngle')
    for (ann, angle) in zip(tier_pos, angles):
        loc = ann.get_location().copy()
        tag = sppasTag(angle, tag_type='int')
        angles_tier.create_annotation(loc, sppasLabel(tag))
    return angles_tier
```

*Predict the angles for the given vowels.*

Notice that the coordinates of the position can have negative values.

##### Parameters

- **tier_pos**: (sppasTier) Coordinates of the vowel positions.
- **face_sights**: (sppasTier) Sights of the face corresponding to each vowel.


##### Returns

- (sppasTier) tier with name 'CS-HandAngle'



### Protected functions

#### __eval_hand_angle

```python
def __eval_hand_angle(self, hand_pos_probas, face_sights):
    """Return angle of the hand for each ann in given tier.

        :param hand_pos_probas: (sppasTier) Coordinates of the vowel positions.
        :param face_sights: (sppasTier) Sights of the face corresponding to each vowel.
        :return: (list) Angle values -- one for each ann in given tier.

        """
    angles = list()
    for i in range(len(hand_pos_probas)):
        cur_vowels = list()
        cur_probas = list()
        for label in hand_pos_probas[i].get_labels():
            for (tag, score) in label:
                cur_vowels.append(tag.get_content())
                cur_probas.append(score)
        face_angle = 90
        if face_sights is not None:
            (_, _, sights) = face_sights[i]
            face_angle = observed_angle((sights.x(8), sights.y(8)), (sights.x(27), sights.y(27)))
        self.__predictor.predict_angle_values(cur_vowels)
        if len(cur_vowels) == 1:
            angles.append(self.__predictor.get_angle(cur_vowels[0], face_angle))
        elif len(cur_vowels) == 2:
            angle1 = self.__predictor.get_angle(cur_vowels[0], face_angle)
            angle2 = self.__predictor.get_angle(cur_vowels[1], face_angle)
            da = angle2 - angle1
            na = angle1 + int(float(da) * cur_probas[1])
            angles.append(na)
    return angles
```

*Return angle of the hand for each ann in given tier.*

##### Parameters

- **hand_pos_probas**: (sppasTier) Coordinates of the vowel positions.
- **face_sights**: (sppasTier) Sights of the face corresponding to each vowel.


##### Returns

- (*list*) Angle values -- one for each ann in given tier.



## Class `sppasWhereCuePredictor`

### Description

*Create a tier indicating the position of 2 points of the hand.*

Predict the position of points S0 and S9 of an hand relatively to
sights of a face.


### Constructor

#### __init__

```python
def __init__(self, pos_predictor_version: int=WhereVowelPositionsPredictor.DEFAULT_VERSION, angle_predictor_version: int=WhereAnglesPredictor.DEFAULT_VERSION, cue_rules: CuedSpeechCueingRules=CuedSpeechCueingRules()):
    """Create a new instance.

    :param cue_rules: (CuedSpeechKeys) Rules and codes for vowel positions and hand shapes

    """
    if isinstance(cue_rules, CuedSpeechCueingRules) is False:
        raise sppasTypeError('cue_rules', 'CuedSpeechCueingRules')
    self.__fps = 50
    self.__pos_predictor = sppasWherePositionsPredictor(pos_predictor_version)
    self.__angle_predictor = sppasWhereAnglesPredictor(angle_predictor_version)
    self.__cued = None
    self.__gentargets = TargetProbabilitiesEstimator()
    self.set_cue_rules(cue_rules)
```

*Create a new instance.*

##### Parameters

- **cue_rules**: (CuedSpeechKeys) Rules and codes for vowel positions and hand shapes



### Public functions

#### get_wherepositionpredictor_versions

```python
def get_wherepositionpredictor_versions(self) -> list:
    """Return the list of version numbers of the vowel positions generator system."""
    return self.__pos_predictor.version_numbers()
```

*Return the list of version numbers of the vowel positions generator system.*

#### get_whereanglepredictor_versions

```python
def get_whereanglepredictor_versions(self) -> list:
    """Return the list of version numbers of the angles generation system."""
    return self.__angle_predictor.version_numbers()
```

*Return the list of version numbers of the angles generation system.*

#### get_wherepositionpredictor_version

```python
def get_wherepositionpredictor_version(self) -> int:
    """Return the version number of the vowel positions prediction system."""
    return self.__pos_predictor.get_version_number()
```

*Return the version number of the vowel positions prediction system.*

#### get_whereanglepredictor_version

```python
def get_whereanglepredictor_version(self) -> int:
    """Return the version number of the angle prediction system."""
    return self.__angle_predictor.get_version_number()
```

*Return the version number of the angle prediction system.*

#### set_wherepositionpredictor_version

```python
def set_wherepositionpredictor_version(self, version_number: int) -> None:
    """Change the vowel position predictor version number.

        :param version_number: (int) One of the supported versions.
        :raises: sppasKeyError: if invalid version number

        """
    self.__pos_predictor.set_version_number(version_number)
```

*Change the vowel position predictor version number.*

##### Parameters

- **version_number**: (*int*) One of the supported versions.


##### Raises

- *sppasKeyError*: if invalid version number

#### set_whereanglepredictor_version

```python
def set_whereanglepredictor_version(self, version_number: int) -> None:
    """Change the angle predictor version number.

        :param version_number: (int) One of the supported versions.
        :raises: sppasKeyError: if invalid version number

        """
    self.__angle_predictor.set_version_number(version_number)
```

*Change the angle predictor version number.*

##### Parameters

- **version_number**: (*int*) One of the supported versions.


##### Raises

- *sppasKeyError*: if invalid version number

#### set_cue_rules

```python
def set_cue_rules(self, cue_rules: CuedSpeechCueingRules) -> None:
    """Set new rules.

        :param cue_rules: (CuedSpeechCueingRules) Rules and codes for vowel positions and hand shapes
        :raises: sppasTypeError: given parameter is not CuedSpeechCueingRules

        """
    if isinstance(cue_rules, CuedSpeechCueingRules) is False:
        raise sppasTypeError('cue_rules', 'CuedSpeechCueingRules')
    self.__cued = cue_rules
    self.__gentargets.set_cue_rules(cue_rules)
```

*Set new rules.*

##### Parameters

- **cue_rules**: (CuedSpeechCueingRules) Rules and codes for vowel positions and hand shapes


##### Raises

- *sppasTypeError*: given parameter is not CuedSpeechCueingRules

#### get_angle_use_face

```python
def get_angle_use_face(self) -> bool:
    """Return True if the hand angle must be corrected by the one of the face."""
    return self.__angle_predictor.get_use_face()
```

*Return True if the hand angle must be corrected by the one of the face.*

#### set_angle_use_face

```python
def set_angle_use_face(self, value: bool) -> None:
    """The angle of the hand is corrected by the one of the face or not.

        :param value: (bool) True if the angle of the hand has to be corrected.

        """
    self.__angle_predictor.set_use_face(value)
```

*The angle of the hand is corrected by the one of the face or not.*

##### Parameters

- **value**: (*bool*) True if the angle of the hand has to be corrected.

#### predict_where

```python
def predict_where(self, file_sights, tier_pos_transitions, tier_shapes_transitions):
    """Prodict where to cue, hand angle and hand size from face sights.

        :param file_sights: (str) Filename with 68 sights of a face for each image of a video
        :param tier_pos_transitions: (sppasTier) Predicted hand position transitions
        :param tier_shapes_transitions: (sppasTier) Predicted hand shapes transitions
        :return: (sppasTranscription)

        """
    face_sights = self._load_sights(file_sights, kid_index=0)
    self.__set_fps(face_sights)
    tier_sizes = sppasFaceHeightGenerator(face_sights).face_height(fps=self.__fps)
    self.__pos_predictor.set_sights(face_sights)
    tier_pos_coords = self.__pos_predictor.vowels_coords(self.__cued.get_vowels_codes(), smooth_len=self.__fps // 5)
    tier_pos_probas = self.__gentargets.positions_discretization(tier_pos_coords, tier_pos_transitions)
    tier_shp_probas = self.__gentargets.shapes_discretization(tier_pos_coords, tier_shapes_transitions)
    tier_target_coords = self.__gentargets.hands_to_target_coords(tier_pos_probas, tier_pos_coords)
    tier_angles = self.__angle_predictor.hand_angles(tier_pos_probas, face_sights)
    trs = sppasTranscription('WhereToCue')
    trs.append(tier_pos_coords)
    trs.append(tier_shp_probas)
    trs.append(tier_pos_probas)
    trs.append(tier_angles)
    trs.append(tier_sizes)
    trs.append(tier_target_coords)
    return trs
```

*Prodict where to cue, hand angle and hand size from face sights.*

##### Parameters

- **file_sights**: (*str*) Filename with 68 sights of a face for each image of a video
- **tier_pos_transitions**: (sppasTier) Predicted hand position transitions
- **tier_shapes_transitions**: (sppasTier) Predicted hand shapes transitions


##### Returns

- (sppasTranscription)



### Private functions

#### _load_sights

```python
def _load_sights(self, filename: str, kid_index: int=0) -> list:
    """Load a filename and store the sights of a given kid.

        The returned data is a list of tuples with:

        - at index 0: midpoint time value
        - at index 1: radius time value
        - at index 2: the 68 sights of a face

        :param filename: (str) Filename of the XRA/CSV with sights
        :param kid_index: (int) index of the kid to get sights
        :raises: sppasWhereCuedSightsValueError: there are sights but there are not of the expected size
        :raises: Exception:
        :return: (list)

        """
    data = sppasSightsVideoReader(filename)
    cur_sights = self.__get_current_sights(data, kid_index)
    data_sights = list()
    for (i, kids_sights) in enumerate(data.sights):
        midpoint = data.midpoints[i]
        if midpoint is None:
            raise Exception('No time point value at index {:d}.'.format(i))
        if 0 < len(kids_sights) <= kid_index + 1:
            s = kids_sights[kid_index]
            if s is not None:
                cur_sights = s
            else:
                logging.warning('No estimated sights at frame number {:d} for kid {:d}.'.format(i + 1, kid_index))
        else:
            logging.warning('No estimated sights at frame number {:d} for kid {:d}.'.format(i + 1, kid_index))
        data_sights.append((midpoint, data.radius[i], cur_sights))
    return data_sights
```

*Load a filename and store the sights of a given kid.*

The returned data is a list of tuples with:

- at index 0: midpoint time value
- at index 1: radius time value
- at index 2: the 68 sights of a face

##### Parameters

- **filename**: (*str*) Filename of the XRA/CSV with sights
- **kid_index**: (*int*) index of the kid to get sights


##### Raises

- *sppasWhereCuedSightsValueError*: there are sights but there are not of the expected size
- *Exception*


##### Returns

- (*list*)



### Protected functions

#### __set_fps

```python
def __set_fps(self, data_sights: list) -> None:
    """Fix the video frames-per-seconds value."""
    if len(data_sights) == 0:
        self.__fps = 50
    else:
        first_midpoint = data_sights[0][0]
        self.__fps = int(1.0 / first_midpoint)
        logging.debug(f'Video fps={self.__fps}')
```

*Fix the video frames-per-seconds value.*

#### __get_current_sights

```python
def __get_current_sights(self, data: sppasSightsVideoReader, kid_index: int) -> sppasSights:
    """Return the sights at given index.

        :param data: (sppasSightsVideoReader) Video reader with sights
        :param kid_index: (int) index of the kid to get sights
        :raises: sppasWhereCuedSightsValueError: there are sights but there are not of the expected size
        :raises: Exception:

        """
    cur_sights = sppasSights()
    for (i, kids_sights) in enumerate(data.sights):
        if 0 < len(kids_sights) <= kid_index + 1:
            cur_sights = kids_sights[kid_index]
            if cur_sights is not None:
                break
    return cur_sights
```

*Return the sights at given index.*

##### Parameters

- **data**: (sppasSightsVideoReader) Video reader with sights
- **kid_index**: (*int*) index of the kid to get sights


##### Raises

- *sppasWhereCuedSightsValueError*: there are sights but there are not of the expected size
- *Exception*





~ Created using [Clamming](https://clamming.sf.net) version 2.1 ~
