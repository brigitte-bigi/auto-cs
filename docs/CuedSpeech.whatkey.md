# CuedSpeech.whatkey module

## List of classes

## Class `sppasCuedRulesValueError`

### Description

*:ERROR 1322:.*

A Cued Speech syllable must be a sequence of C-V phonemes.
Got '{}' instead.


### Constructor

#### __init__

```python
def __init__(self, value):
    self._status = 1322
    self.parameter = error(self._status) + error(self._status, 'annotations').format(value)
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





## Class `sppasCuedRulesMinValueError`

### Description

*:ERROR 1321:.*

A Cued Speech syllable should contain at least one phoneme.
Got {} instead.


### Constructor

#### __init__

```python
def __init__(self, value):
    self._status = 1321
    self.parameter = error(self._status) + error(self._status, 'annotations').format(value)
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





## Class `sppasCuedRulesMaxValueError`

### Description

*:ERROR 1323:.*

A Cued Speech syllable should contain a maximum of two phonemes.
Got {} instead.


### Constructor

#### __init__

```python
def __init__(self, value):
    self._status = 1323
    self.parameter = error(self._status) + error(self._status, 'annotations').format(value)
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





## Class `CuedSpeechCueingRules`

### Description

*Rules data structure for a system to predict Cued Speech keys.*

##### Example

    >>> rules = CuedSpeechCueingRules()
    >>> result = rules.load(FRA_KEYS)
    >>> assert(result is True)
    >>> rules.get_key("e")
    > "t"


### Constructor

#### __init__

```python
def __init__(self, filename=None):
    """Create a new instance.

    :param filename: (str) Name of the file with the rules.

    """
    self.__phon = dict()
    self.__shptgt = dict()
    self.__phonmerge = dict()
    if filename is not None:
        self.load(filename)
    else:
        self.reset()
```

*Create a new instance.*

##### Parameters

- **filename**: (*str*) Name of the file with the rules.



### Public functions

#### reset

```python
def reset(self) -> None:
    """Reset the set of rules.

        """
    self.__phon = dict()
    self.__shptgt = dict()
    self.__phonmerge = dict()
    for phone in symbols.all:
        self.__phon[phone] = (CuedSpeechCueingRules.NEUTRAL_CLASS, None)
    self.__phon['vnone'] = (CuedSpeechCueingRules.NEUTRAL_CLASS, 'n')
    self.__phon['cnone'] = (CuedSpeechCueingRules.NEUTRAL_CLASS, '0')
    self.__phon['vnil'] = (CuedSpeechCueingRules.NEUTRAL_CLASS, None)
    self.__phon['cnil'] = (CuedSpeechCueingRules.NEUTRAL_CLASS, None)
```

*Reset the set of rules.*



#### load

```python
def load(self, filename: str) -> bool:
    """Load the rules from a file.

        Invalidate the already defined set of rules.

        :param filename: (str) Name of the file with the rules.
        :raises: sppasIOError: If the file cannot be opened.
        :raises: sppasError: File is not a regular Cued Speech file.
        :return: (bool) Rules were appended or not

        """
    self.reset()
    if os.path.exists(filename) is True and os.path.isfile(filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            f.close()
    else:
        raise sppasIOError(filename)
    added = False
    for (line_nb, line) in enumerate(lines, 1):
        sp = sppasUnicode(line)
        line = sp.to_strip()
        if line.startswith('#') is True:
            continue
        columns = line.split()
        if len(columns) == 4 and columns[0] == 'PHONMERGE':
            sequence = tuple(columns[1:-1])
            effective_class = columns[-1]
            if len(sequence) == 0:
                raise sppasError(f'Invalid PHONMERGE at line {line_nb}: empty sequence.')
            if effective_class not in CuedSpeechCueingRules.PHON_CLASSES:
                raise sppasError('Invalid PHONMERGE class. One of {:s} was expected. Got {:s} instead.'.format(CuedSpeechCueingRules.PHON_CLASSES, effective_class))
            if sequence in self.__phonmerge:
                raise sppasError(f'Duplicated PHONMERGE at line {line_nb}: {sequence} is already defined.')
            self.__phonmerge[sequence] = effective_class
            added = True
        elif len(columns) == 3:
            p = columns[1]
            if p not in self.__phon:
                self.__phon[p] = (None, None)
            tup = self.__phon[p]
            if columns[0] == 'PHONCLASS':
                if columns[2] not in CuedSpeechCueingRules.PHON_CLASSES:
                    raise sppasError('Invalid PHONCLASS. One of {:s} was expected. Got {:s} instead.'.format(CuedSpeechCueingRules.PHON_CLASSES, columns[2]))
                if columns[1] not in ('cnone', 'vnone'):
                    self.__phon[columns[1]] = (columns[2], tup[1])
                    added = True
            elif columns[0] == 'PHONKEY':
                if columns[1] not in ('cnone', 'vnone'):
                    self.__phon[columns[1]] = (tup[0], columns[2])
                    added = True
            elif columns[0] == 'SHAPETARGET':
                if columns[1] not in self.__shptgt:
                    try:
                        target = int(columns[2])
                        if 0 <= target <= 20:
                            self.__shptgt[columns[1]] = target
                        else:
                            raise sppasError(f'Invalid SHAPETARGET value {target}')
                    except ValueError:
                        raise sppasError(f"SHAPETARGET '{columns[2]}' is not an integer for shape {columns[1]}")
                else:
                    raise sppasError(f'shape {columns[1]} is already defined.')
    return added
```

*Load the rules from a file.*

Invalidate the already defined set of rules.

##### Parameters

- **filename**: (*str*) Name of the file with the rules.


##### Raises

- *sppasIOError*: If the file cannot be opened.
- *sppasError*: File is not a regular Cued Speech file.


##### Returns

- (*bool*) Rules were appended or not

#### get_class

```python
def get_class(self, phoneme: str) -> str:
    """Return the class identifier of the phoneme.

        If the phoneme is unknown, the neutral class is returned.

        :param phoneme: (str) A phoneme
        :return: class of the phoneme or neutral class

        """
    tup = self.__phon.get(phoneme, None)
    if tup is None or (tup is not None and tup[0] is None):
        for seq in self.__phonmerge:
            _joined_seq = ''.join(seq)
            if phoneme == _joined_seq:
                return self.__phonmerge[seq]
        return CuedSpeechCueingRules.NEUTRAL_CLASS
    return tup[0]
```

*Return the class identifier of the phoneme.*

If the phoneme is unknown, the neutral class is returned.

##### Parameters

- **phoneme**: (*str*) A phoneme


##### Returns

- class of the phoneme or neutral class

#### get_merged_class

```python
def get_merged_class(self, sequence: tuple):
    """Return the effective class for a phoneme sequence.

        :param sequence: (tuple) Sequence of phones to merge.
        :return: (str or None) The effective class, or None.

        """
    if isinstance(sequence, tuple) is False:
        raise TypeError(f'Given sequence must be a tuple. Got {type(sequence)} instead.')
    return self.__phonmerge.get(sequence)
```

*Return the effective class for a phoneme sequence.*

##### Parameters

- **sequence**: (*tuple*) Sequence of phones to merge.


##### Returns

- (*str* or None) The effective class, or None.

#### get_vowels_codes

```python
def get_vowels_codes(self) -> list:
    """Return the list of key codes of all the positions (vowels).

        """
    vowels_codes = list()
    for phon in self.__phon:
        phon_key = self.get_key(phon)
        if phon_key is not None:
            if self.get_class(phon) == 'V':
                vowels_codes.append(phon_key)
            elif self.get_class(phon) == 'W':
                for key_code in phon_key:
                    vowels_codes.append(key_code)
    return [self.get_neutral_vowel()] + sorted(list(set(vowels_codes)), reverse=True)
```

*Return the list of key codes of all the positions (vowels).*



#### get_consonants_codes

```python
def get_consonants_codes(self) -> list:
    """Return the list of key codes of all the shapes (consonants).

        """
    cons_codes = list()
    for phon in self.__phon:
        phon_key = self.get_key(phon)
        if self.get_class(phon) == 'C' and phon_key is not None:
            cons_codes.append(phon_key)
    return [self.get_neutral_consonant()] + sorted(list(set(cons_codes)))
```

*Return the list of key codes of all the shapes (consonants).*



#### get_key

```python
def get_key(self, phoneme: str) -> tuple:
    """Return the key identifier of the phoneme.

        None is returned if the phoneme is unknown or if it is a break.
        If the phoneme is known but no key was defined for this phoneme,
        the "nil" key is returned.

        :param phoneme: (str) A phoneme or a diphthong
        :return: key or tuple(key,key) if diphtong or None if unknown

        """
    if self.get_class(phoneme) == 'W':
        return self.get_diphthong_key(phoneme)
    tup = self.__phon.get(phoneme, None)
    if tup is None:
        return None
    key = tup[1]
    if key is None:
        if tup[0] in ('V', 'W'):
            key = self.__phon['vnil'][1]
        elif tup[0] == 'C':
            key = self.__phon['cnil'][1]
    return key
```

*Return the key identifier of the phoneme.*

None is returned if the phoneme is unknown or if it is a break.
If the phoneme is known but no key was defined for this phoneme,
the "nil" key is returned.

##### Parameters

- **phoneme**: (*str*) A phoneme or a diphthong


##### Returns

- key or tuple(key,key) if diphtong or None if unknown

#### get_diphthong_key

```python
def get_diphthong_key(self, diphthong: str) -> tuple[str, str] | None:
    """Return the key identifiers of the given diphthong.

        :param diphthong: (str) A diphthong made of 2 phonemes
        :return: tuple(key,key) or None if unknown

        """
    if len(diphthong) == 2:
        tup = self.__phon.get(diphthong[0], None)
        if tup is None:
            return None
        key1 = tup[1]
        tup = self.__phon.get(diphthong[1], None)
        if tup is None:
            return None
        key2 = tup[1]
        return (key1, key2)
    return None
```

*Return the key identifiers of the given diphthong.*

##### Parameters

- **diphthong**: (*str*) A diphthong made of 2 phonemes


##### Returns

- tuple(key,key) or None if unknown

#### get_nil_consonant

```python
def get_nil_consonant(self) -> str:
    """Return the key code for a missing consonant."""
    return self.__phon['cnil'][1]
```

*Return the key code for a missing consonant.*

#### get_nil_vowel

```python
def get_nil_vowel(self) -> str:
    """Return the key code for a missing vowel."""
    return self.__phon['vnil'][1]
```

*Return the key code for a missing vowel.*

#### get_neutral_vowel

```python
def get_neutral_vowel(self) -> str:
    """Return the key code of the neutral position (vowel)."""
    return self.__phon['vnone'][1]
```

*Return the key code of the neutral position (vowel).*

#### get_neutral_consonant

```python
def get_neutral_consonant(self) -> str:
    """Return the key code of the neutral shape (consonant)."""
    return self.__phon['cnone'][1]
```

*Return the key code of the neutral shape (consonant).*

#### get_shape_target

```python
def get_shape_target(self, shape: str) -> int:
    """Return the target index of the given shape.

        :param shape: (str) Shape code
        :return: (int) target index of the given shape or the default target index

        """
    return self.__shptgt.get(shape, CuedSpeechCueingRules.SHAPE_TARGET)
```

*Return the target index of the given shape.*

##### Parameters

- **shape**: (*str*) Shape code


##### Returns

- (*int*) target index of the given shape or the default target index

#### get_phon_target

```python
def get_phon_target(self, phoneme: str) -> int:
    """Return the target index of the given phoneme.

        :param phoneme: (str) Shape code
        :return: (int) target index of the given phoneme or the default target index

        """
    _tup = self.__phon.get(phoneme, None)
    if _tup is None:
        return CuedSpeechCueingRules.SHAPE_TARGET
    return self.__shptgt.get(_tup[1], CuedSpeechCueingRules.SHAPE_TARGET)
```

*Return the target index of the given phoneme.*

##### Parameters

- **phoneme**: (*str*) Shape code


##### Returns

- (*int*) target index of the given phoneme or the default target index

#### get_merged_phone

```python
def get_merged_phone(self, sequence: tuple):
    """Return the merged phone for a phoneme sequence.

        :param sequence: (tuple) Sequence of phones to merge.
        :return: (str or None) The merged phone, or None.

        """
    if isinstance(sequence, tuple) is False:
        raise TypeError(f'Given sequence must be a tuple. Got {type(sequence)} instead.')
    return self.__phonmerge.get(sequence)
```

*Return the merged phone for a phoneme sequence.*

##### Parameters

- **sequence**: (*tuple*) Sequence of phones to merge.


##### Returns

- (*str* or None) The merged phone, or None.

#### has_phonmerge

```python
def has_phonmerge(self) -> bool:
    """Return True if at least one merge rule is defined."""
    return len(self.__phonmerge) > 0
```

*Return True if at least one merge rule is defined.*

#### syll_to_key

```python
def syll_to_key(self, syll: str) -> tuple:
    """Return the key codes matching the given syllable.

        The given entry can be either of the form:
        C-V or C- or C or -V or V.

        :example:
        >>> syll_to_key("-E")
        ('5', 'c')
        >>> syll_to_key("E")
        ('5', 'c')
        >>> syll_to_key("p-")
        ('1', 's')
        >>> syll_to_key("p")
        ('1', 's')
        >>> syll_to_key("p-E")
        ('1', 'c')
        >>> syll_to_key("p-aI")
        (('1', 's'), ('5', 't'))
        >>> syll_to_key("hw-E")
        ('4', 'c')

        :param syll: (str) A syllable like "p-a", or "p-" or "-a" or "p-aI" or "hw-E".
        :return: (tuple or None) Key codes
        :raises: sppasCuedRulesValueError: malformed syll
        :raises: sppasCuedRulesMinValueError: not enough phonemes in syll
        :raises: sppasCuedRulesMaxValueError: too many phonemes in syll

        """
    phons = self.__syll_to_phons(syll)
    _class_1 = self.get_class(phons[0])
    _class_2 = self.get_class(phons[1])
    if _class_1 not in ('N', 'C') or _class_2 not in ('N', 'V', 'W'):
        raise sppasCuedRulesValueError(syll)
    key_cons = self.get_key(phons[0])
    key_vowel = self.get_key(phons[1])
    if key_cons is None or key_vowel is None:
        raise sppasCuedRulesValueError(syll)
    if self.get_class(phons[1]) == 'W':
        return ((key_cons, key_vowel[0]), (self.get_nil_consonant(), key_vowel[1]))
    return (key_cons, key_vowel)
```

*Return the key codes matching the given syllable.*

The given entry can be either of the form:
C-V or C- or C or -V or V.

##### Example

    >>> syll_to_key("-E")
    > ('5', 'c')
    >>> syll_to_key("E")
    > ('5', 'c')
    >>> syll_to_key("p-")
    > ('1', 's')
    >>> syll_to_key("p")
    > ('1', 's')
    >>> syll_to_key("p-E")
    > ('1', 'c')
    >>> syll_to_key("p-aI")
    > (('1', 's'), ('5', 't'))
    >>> syll_to_key("hw-E")
    > ('4', 'c')

##### Parameters

- **syll**: (*str*) A syllable like "p-a", or "p-" or "-a" or "p-aI" or "hw-E".


##### Returns

- (*tuple* or None) Key codes


##### Raises

- *sppasCuedRulesValueError*: malformed syll
- *sppasCuedRulesMinValueError*: not enough phonemes in syll
- *sppasCuedRulesMaxValueError*: too many phonemes in syll



### Protected functions

#### __syll_to_phons

```python
def __syll_to_phons(self, syll: str) -> list:
    """Return the phonemes matching the given syllable.

        :raises: sppasCuedRulesValueError: malformed syll
        :raises: sppasCuedRulesMinValueError: not enough phonemes in syll
        :raises: sppasCuedRulesMaxValueError: too many phonemes in syll
        :return: (tuple) Tuple with (consonant, vowel)

        """
    if len(syll.strip()) == 0 or syll.strip() == '-':
        raise sppasCuedRulesValueError(syll)
    phons = syll.split(separators.phonemes)
    if len(phons) == 0:
        raise sppasCuedRulesMinValueError(syll)
    elif len(phons) == 1:
        if self.get_class(phons[0]) == 'V':
            phons.insert(0, 'cnil')
        elif self.get_class(phons[0]) == 'C':
            phons.append('vnil')
        else:
            phons.insert(0, 'unknown')
    elif len(phons) == 2:
        if len(phons[0]) == 0:
            phons[0] = 'cnil'
        if len(phons[1]) == 0:
            phons[1] = 'vnil'
    else:
        raise sppasCuedRulesMaxValueError(syll)
    return phons
```

*Return the phonemes matching the given syllable.*

##### Raises

- *sppasCuedRulesValueError*: malformed syll
- *sppasCuedRulesMinValueError*: not enough phonemes in syll
- *sppasCuedRulesMaxValueError*: too many phonemes in syll


##### Returns

- (*tuple*) Tuple with (consonant, vowel)



## Class `CuedSpeechKeys`

### Description

*Cued Speech keys generation from a sequence of phonemes.*

##### Example




##### Example

    >>> # Define the input: a list of phonemes
    >>> phonemes = ["#", "s", "p", "a", "s"]
    >>> # Create the instance
    >>> self.lfpc = CuedSpeechKeys(FRA_KEYS)
    >>> # Apply the rules to get result in various formats
    >>> sgmts = self.lfpc.syllabify(phonemes)
    >>> [(1, 1), (2, 3), (4, 4)]
    >>> phons = self.lfpc.phonetize_syllables(phonemes, sgmts)
    >>> "s-vnil.p-a.s-vnil"
    >>> keys = self.lfpc.keys_phonetized(phons)
    >>> "3-s.1-s.3-s"


### Constructor

#### __init__

```python
def __init__(self, keyrules_filename=None):
    """Create a new instance.

    Load keys from a text file, depending on the language and phonemes
    encoding. See documentation for details about this file.

    :param keyrules_filename: (str) Name of the file with the list of keys.

    """
    super(CuedSpeechKeys, self).__init__(keyrules_filename)
```

*Create a new instance.*

Load keys from a text file, depending on the language and phonemes
encoding. See documentation for details about this file.

##### Parameters

- **keyrules_filename**: (*str*) Name of the file with the list of keys.



### Public functions

#### syllabify

```python
def syllabify(self, phonemes: list) -> list:
    """Return the key boundaries of a sequence of phonemes.

        Perform the segmentation of the sequence of phonemes into the
        syllables-structure of the Cued Speech coding scheme.
        A syllable structure is CV, or V or C.

        :exemple:
        >>> phonemes = ['b', 'O~', 'Z', 'u', 'R']
        >>> CuedSpeechKeys("fra-config-file").syllabify(phonemes)
        >>> [ (0, 1), (2, 3), (4, 4) ]

        :exemple:
        >>> phonemes = ['E', 'n', 'i:', 'h', 'w', 'E', 'r\\\\']
        >>> CuedSpeechKeys("eng-config-file").syllabify(phonemes)
        >>> [ (0, 0), (1, 2), (3, 5), (6, 6) ]

        :param phonemes: (list of str) List of phonemes
        :returns: list of tuples (begin index, end index)

        """
    classes = [self.get_class(p) for p in phonemes]
    syll = list()
    spans = CuedSpeechKeys.compute_phonmerge_spans(phonemes, self)

    def _effective_class_and_len(index: int) -> tuple:
        span = spans.get(index, None)
        if span is None:
            return (classes[index], 1)
        return (span[1], span[0])
    i = 0
    while i < len(phonemes):
        (c, span_len) = _effective_class_and_len(i)
        if c in ('W', 'V', 'C'):
            if c in ('V', 'W') or i + span_len >= len(phonemes):
                syll.append((i, i + span_len - 1))
            else:
                i_next = i + span_len
                (c_next, span_len_next) = _effective_class_and_len(i_next)
                if c_next in ('V', 'W'):
                    syll.append((i, i_next + span_len_next - 1))
                    i += span_len + span_len_next
                    continue
                else:
                    syll.append((i, i + span_len - 1))
        i += span_len
    return syll
```

*Return the key boundaries of a sequence of phonemes.*

Perform the segmentation of the sequence of phonemes into the
syllables-structure of the Cued Speech coding scheme.
A syllable structure is CV, or V or C.

- **exemple**


##### Example

    >>> phonemes = ['b', 'O~', 'Z', 'u', 'R']
    >>> CuedSpeechKeys("fra-config-file").syllabify(phonemes)
    >>> [ (0, 1), (2, 3), (4, 4) ]

- **exemple**


##### Example

    >>> phonemes = ['E', 'n', 'i:', 'h', 'w', 'E', 'r\\']
    >>> CuedSpeechKeys("eng-config-file").syllabify(phonemes)
    >>> [ (0, 0), (1, 2), (3, 5), (6, 6) ]

##### Parameters

- **phonemes**: (*list* of *str*) List of phonemes


##### Returns

- list of tuples(begin index, end index)

#### phonetize_syllables

```python
def phonetize_syllables(self, phonemes: list, syllables: list) -> str:
    """Return the phonetized sequence of syllables.

        The output string is using the X-SAMPA standard to indicate the
        phonemes and syllables segmentation.

        :example:
        >>> phonemes = ['b', 'O~', 'Z', 'u', 'R']
        >>> lpc_keys = CuedSpeechKeys("fra-config-file")
        >>> syllables = lpc_keys.syllabify(phonemes)
        >>> [ (0, 1), (2, 3), (4, 4) ]
        >>> lpc_keys.phonetize_syllables(phonemes, syllables)
        >>> "b-O~.Z-u.R-vnil"

        Notice that a diphtong implies 2 keys to be created!

        :example:
        >>> phonemes = [ '@', 'dZ', 'OI', 'n' ]
        >>> lpc_keys = CuedSpeechKeys("eng-config-file")
        >>> syllables = lpc_keys.syllabify(phonemes)
        >>> [ (0, 0), (1, 2), (3, 3) ]
        >>> lpc_keys.phonetize_syllables(phonemes, syllables)
        >>> "cnil-@.dZ-O.cnil-I.n-vnil"

        The challenging word: nonwhite: n A n h w aI t
        because
         - 'aI' is a diphtong (2 positions, 2 keys then), and
         - 'h-w' sequence is only one shape (one key then)!

        :param phonemes: (list) List of phonemes
        :param syllables: list of tuples (begin index, end index)
        :return: (str) String representing the syllables segmentation

        """
    str_syll = list()
    for (begin, end) in syllables:
        if begin == end:
            p = phonemes[begin]
            c = self.get_class(p)
            if c == 'W':
                if len(p) > 1:
                    str_syll.append('cnil' + separators.phonemes + p[0])
                    str_syll.append('cnil' + separators.phonemes + p[1:])
                else:
                    logging.error(f"Hum... the vowel {p} is declared in class 'W' but it can be split!")
                    str_syll.append('cnil' + separators.phonemes + p)
            elif c == 'V':
                str_syll.append('cnil' + separators.phonemes + p)
            else:
                str_syll.append(p + separators.phonemes + 'vnil')
        else:
            span_phones = phonemes[begin:end + 1]
            last_phone = span_phones[-1]
            last_class = self.get_class(last_phone)
            if last_class in ('V', 'W'):
                consonant_items = self._merge_consonant_cluster(span_phones[:-1])
                consonant_cluster = separators.phonemes.join(consonant_items)
                if last_class == 'W':
                    if len(last_phone) > 1:
                        str_syll.append(consonant_cluster + separators.phonemes + last_phone[0])
                        str_syll.append('cnil' + separators.phonemes + last_phone[1:])
                    else:
                        logging.error(f"Hum... the vowel {last_phone} is declared in class 'W' but it can be split!")
                        str_syll.append(consonant_cluster + separators.phonemes + last_phone)
                else:
                    str_syll.append(consonant_cluster + separators.phonemes + last_phone)
            else:
                consonant_items = self._merge_consonant_cluster(span_phones)
                consonant_cluster = separators.phonemes.join(consonant_items)
                str_syll.append(consonant_cluster + separators.phonemes + 'vnil')
    return separators.syllables.join(str_syll)
```

*Return the phonetized sequence of syllables.*

The output string is using the X-SAMPA standard to indicate the
phonemes and syllables segmentation.

##### Example

    >>> phonemes = ['b', 'O~', 'Z', 'u', 'R']
    >>> lpc_keys = CuedSpeechKeys("fra-config-file")
    >>> syllables = lpc_keys.syllabify(phonemes)
    >>> [ (0, 1), (2, 3), (4, 4) ]
    >>> lpc_keys.phonetize_syllables(phonemes, syllables)
    >>> "b-O~.Z-u.R-vnil"

Notice that a diphtong implies 2 keys to be created!

##### Example

    >>> phonemes = [ '@', 'dZ', 'OI', 'n' ]
    >>> lpc_keys = CuedSpeechKeys("eng-config-file")
    >>> syllables = lpc_keys.syllabify(phonemes)
    >>> [ (0, 0), (1, 2), (3, 3) ]
    >>> lpc_keys.phonetize_syllables(phonemes, syllables)
    >>> "cnil-@.dZ-O.cnil-I.n-vnil"

The challenging word: nonwhite: n A n h w aI t
because
- 'aI' is a diphtong (2 positions, 2 keys then), and
- 'h-w' sequence is only one shape (one key then)!

##### Parameters

- **phonemes**: (*list*) List of phonemes
- **syllables**: list of tuples(begin index, end index)


##### Returns

- (*str*) String representing the syllables segmentation

#### keys_phonetized

```python
def keys_phonetized(self, phonetized_syllables: str) -> str:
    """Return the keys of a phonetized syllable as C-V sequences.

        The input string is using the X-SAMPA standard to indicate the
        phonemes and syllables segmentation.

        :example:
        >>> phonetized_syllable = "cnil-e.p-a.R-vnil"
        >>> lpc_keys = CuedSpeechKeys("fra-config-file")
        >>> lpc_keys.keys_phonetized(phonetized_syllable)
        >>> "0-t.1-s.3-s"

        :example:
        >>> phonetized_syllable = "cnil-E.n-i:.hw-E.r\\-vnil"
        >>> lpc_keys = CuedSpeechKeys("eng-config-file")
        >>> lpc_keys.keys_phonetized(phonetized_syllable)
        >>> "5-c.4-m.4-c.3-s"

        :param phonetized_syllables: (str) String representing the keys segments
        :return: (str)

        """
    key_codes = list()
    for syll in phonetized_syllables.split(separators.syllables):
        try:
            phones = syll.split(separators.phonemes)
            if len(phones) == 2:
                if self.get_class(phones[1]) == 'W':
                    ((c1, v1), (c2, v2)) = self.syll_to_key(syll)
                    key_codes.append(c1 + separators.phonemes + v1)
                    key_codes.append(c2 + separators.phonemes + v2)
                else:
                    (consonant, vowel) = self.syll_to_key(syll)
                    key_codes.append(consonant + separators.phonemes + vowel)
            else:
                logging.error(f'Syllables must have two phonemes. Ignored: {syll}')
        except ValueError as e:
            import traceback
            logging.warning(str(e))
            key_codes.append(separators.phonemes)
    return separators.syllables.join(key_codes)
```

*Return the keys of a phonetized syllable as C-V sequences.*

The input string is using the X-SAMPA standard to indicate the
phonemes and syllables segmentation.

##### Example

    >>> phonetized_syllable = "cnil-e.p-a.R-vnil"
    >>> lpc_keys = CuedSpeechKeys("fra-config-file")
    >>> lpc_keys.keys_phonetized(phonetized_syllable)
    >>> "0-t.1-s.3-s"

##### Example

    >>> phonetized_syllable = "cnil-E.n-i:.hw-E.r\-vnil"
    >>> lpc_keys = CuedSpeechKeys("eng-config-file")
    >>> lpc_keys.keys_phonetized(phonetized_syllable)
    >>> "5-c.4-m.4-c.3-s"

##### Parameters

- **phonetized_syllables**: (*str*) String representing the keys segments


##### Returns

- (*str*)

#### compute_phonmerge_spans

```python
@staticmethod
def compute_phonmerge_spans(phonemes: list, rules: CuedSpeechCueingRules) -> dict:
    """Return the best merge span starting at each index.

        The input phonemes list is NEVER modified.
        A span is defined only if the rules contain a PHONMERGE entry.
        The "best" span is the longest matching sequence starting at index i.

        :param phonemes: (list) Sequence of phonemes (strings).
        :param rules: (CuedSpeechCueingRules) Rules containing PHONMERGE entries.
        :return: (dict) Mapping start_index -> (length, effective_class).

        """
    spans = dict()
    for i in range(len(phonemes)):
        best_len = 0
        best_class = None
        for length in range(2, len(phonemes) - i + 1):
            seq = tuple(phonemes[i:i + length])
            cls = rules.get_merged_class(seq)
            if cls is None:
                continue
            if length > best_len:
                best_len = length
                best_class = cls
        if best_len > 0:
            spans[i] = (best_len, best_class)
    return spans
```

*Return the best merge span starting at each index.*

The input phonemes list is NEVER modified.
A span is defined only if the rules contain a PHONMERGE entry.
The "best" span is the longest matching sequence starting at index i.

##### Parameters

- **phonemes**: (*list*) Sequence of phonemes (strings).
- **rules**: (CuedSpeechCueingRules) Rules containing PHONMERGE entries.


##### Returns

- (*dict*) Mapping start_index -> (length, effective_class).



### Private functions

#### _merge_consonant_cluster

```python
def _merge_consonant_cluster(self, phones: list) -> list:
    merged = list()
    i = 0
    while i < len(phones):
        if i + 1 < len(phones):
            eff = self.get_merged_class((phones[i], phones[i + 1]))
            if eff == 'C':
                merged.append(phones[i] + phones[i + 1])
                i += 2
                continue
        merged.append(phones[i])
        i += 1
    return merged
```



#### _effective_class_and_len

```python
def _effective_class_and_len(index: int) -> tuple:
    span = spans.get(index, None)
    if span is None:
        return (classes[index], 1)
    return (span[1], span[0])
```





## Class `CueingPronTokenizer`

### Description

*Tokenize and normalize word pronunciations for stable Cued Speech alignment.*

This helper converts the per-word pronunciation strings (split with '-') into
normalized strings, using CsNormalizationRules as the single normalization layer.


### Constructor

#### __init__

```python
def __init__(self, key_rules: CuedSpeechKeys):
    """Create a new instance.

    """
    self.__rules = _CueingRulesAdapter(key_rules)
```

*Create a new instance.*





### Public functions

#### normalize_word_phonemes

```python
def normalize_word_phonemes(self, word_phonemes: tuple) -> tuple:
    """Return normalized pronunciations for each word.

        Input example: ('w-aI-t', '@-dZ-OI-n', 'OI-l')
        Output example: ('w-a-I-t', '@-dZ-O-I-n', 'O-I-l')

        :param word_phonemes: (tuple) Pronunciation of each token, as '-' separated phones.
        :raises: ValueError: Invalid type or empty item.
        :return: (tuple) Normalized pronunciations, same token count as input.

        """
    if isinstance(word_phonemes, (list, tuple)) is False:
        raise ValueError('word_phonemes must be a tuple or list')
    normalized_items = list()
    for item in word_phonemes:
        if isinstance(item, str) is False:
            raise ValueError('Each item of word_phonemes must be a str')
        if len(item) == 0:
            raise ValueError('Empty pronunciation item in word_phonemes')
        phones = item.split('-')
        phones = [p for p in phones if len(p) > 0]
        if len(phones) == 0:
            raise ValueError('Empty phoneme list for a token.')
        normalized_phones = self.__rules.normalize_word_phones(phones)
        normalized_items.append('-'.join(normalized_phones))
    return tuple(normalized_items)
```

*Return normalized pronunciations for each word.*

Input example: ('w-aI-t', '@-dZ-OI-n', 'OI-l')
Output example: ('w-a-I-t', '@-dZ-O-I-n', 'O-I-l')

##### Parameters

- **word_phonemes**: (*tuple*) Pronunciation of each token, as '-' separated phones.


##### Raises

- *ValueError*: Invalid type or empty item.


##### Returns

- (*tuple*) Normalized pronunciations, same token count as input.



## Class `CueingKeysByToken`

### Description

*Segment an already cued text into per-token keys and per-token phones.*

The cueing result is a list of items: (keys_str, phones_str).
Each string can contain multiple key pairs separated with '.'.

The segmentation rule assigns each key to the token that consumes its vowel phones.


### Constructor

#### __init__

```python
def __init__(self):
    """Create a new instance."""
    pass
```

*Create a new instance.*



### Public functions

#### segment

```python
def segment(self, word_phonemes: tuple, key_items: list) -> tuple:
    """Return per-token keys and per-token phones.

        :param word_phonemes: (tuple) Pronunciation of each token ('-' separated phones).
        :param key_items: (list) Cueing result: list of (keys_str, phones_str).
        :return: (tuple) (codes_by_token, phones_by_token), each is a tuple of strings ('.' separated).

        """
    words_phones = self.__parse_words(word_phonemes)
    (flat_codes, flat_phons) = self.__flatten_key_items(key_items)
    token_codes = [[] for _ in range(len(words_phones))]
    token_phons = [[] for _ in range(len(words_phones))]
    token_consumed = [False for _ in range(len(words_phones))]
    cursor = _PhonesCursor(words_phones, token_consumed)
    for i in range(len(flat_codes)):
        code_item = flat_codes[i]
        phon_item = flat_phons[i]
        (consonants, vowels) = self.__parse_key_pair(phon_item)
        token_index = None
        if len(consonants) > 0:
            token_index = cursor.consume(consonants, 'consonants')
        cursor.advance_if_done()
        if len(vowels) > 0:
            token_index = cursor.consume(vowels, 'vowels')
        if token_index is None:
            raise ValueError('Key has neither consonant nor vowel phones: ' + phon_item)
        token_codes[token_index].append(code_item)
        token_phons[token_index].append(phon_item)
    for i in range(len(words_phones)):
        if token_consumed[i] is True and len(token_codes[i]) == 0:
            token_codes[i].append(self.__PLACEHOLDER_CODE)
            token_phons[i].append(self.__PLACEHOLDER_PHON)
    codes_by_token = tuple(['.'.join(items) for items in token_codes])
    phons_by_token = tuple(['.'.join(items) for items in token_phons])
    return (codes_by_token, phons_by_token)
```

*Return per-token keys and per-token phones.*

##### Parameters

- **word_phonemes**: (*tuple*) Pronunciation of each token ('-' separated phones).
- **key_items**: (*list*) Cueing result: list of (keys_str, phones_str).


##### Returns

- (*tuple*) (codes_by_token, phones_by_token), each is a tuple of strings ('.' separated).



### Protected functions

#### __parse_words

```python
def __parse_words(self, word_phonemes: tuple) -> list:
    """Return a list of list of phones per token."""
    if isinstance(word_phonemes, (list, tuple)) is False:
        raise ValueError('word_phonemes must be a tuple or list')
    words = list()
    for item in word_phonemes:
        if isinstance(item, str) is False:
            raise ValueError('Each item of word_phonemes must be a str')
        phones = self.__split_non_empty(item, '-')
        if len(phones) == 0:
            raise ValueError('Empty phoneme list for a token')
        words.append(phones)
    if len(words) == 0:
        raise ValueError('word_phonemes is empty')
    return words
```

*Return a list of list of phones per token.*

#### __flatten_key_items

```python
def __flatten_key_items(self, key_items: list) -> tuple:
    """Return flat lists of codes and phones."""
    if isinstance(key_items, list) is False:
        raise ValueError('key_items must be a list')
    codes_flat = list()
    phons_flat = list()
    for item in key_items:
        if isinstance(item, (list, tuple)) is False or len(item) != 2:
            raise ValueError('Each item of key_items must be a (codes_str, phon_str) pair.')
        (codes_str, phon_str) = item
        if isinstance(codes_str, str) is False:
            raise ValueError('codes_str must be a str')
        if isinstance(phon_str, str) is False:
            raise ValueError('phon_str must be a str')
        codes = self.__split_non_empty(codes_str, '.')
        phons = self.__split_non_empty(phon_str, '.')
        if len(codes) != len(phons):
            raise ValueError("codes_str '" + codes_str + "' and phon_str '" + phon_str + "' do not have the same number of keys.")
        for c in codes:
            codes_flat.append(c)
        for p in phons:
            phons_flat.append(p)
    if len(codes_flat) == 0:
        raise ValueError('No key found in key_items')
    return (codes_flat, phons_flat)
```

*Return flat lists of codes and phones.*

#### __parse_key_pair

```python
def __parse_key_pair(self, pair_str: str) -> tuple:
    """Return (consonants, vowels) lists from a 'C-V' pair string."""
    if isinstance(pair_str, str) is False:
        raise ValueError('Invalid key-phoneme pair: ' + str(pair_str))
    if pair_str.count('-') == 0:
        raise ValueError('Invalid key-phoneme pair: ' + pair_str)
    (left, right) = pair_str.split('-', 1)
    left = left.strip()
    right = right.strip()
    consonants = list()
    vowels = list()
    if left != 'cnil':
        consonants = self.__split_non_empty(left, '-')
    if right != 'vnil':
        vowels = self.__split_non_empty(right, '-')
    return (consonants, vowels)
```

*Return (consonants, vowels) lists from a 'C-V' pair string.*

#### __split_non_empty

```python
@staticmethod
def __split_non_empty(value: str, sep: str) -> list:
    """Split and remove empty items."""
    out = list()
    for part in value.split(sep):
        if len(part) > 0:
            out.append(part)
    return out
```

*Split and remove empty items.*



## Class `sppasWhatKeyPredictor`

### Description

*Cued Speech keys automatic generator from a sequence of phonemes.*




### Constructor

#### __init__

```python
def __init__(self, cue_rules: CuedSpeechKeys=CuedSpeechKeys()):
    """Instantiate a CS generator.

    :param cue_rules: (CuedSpeechKeys) Rules to convert phonemes to keys

    """
    self.__cued = None
    self.set_cue_rules(cue_rules)
```

*Instantiate a CS generator.*

##### Parameters

- **cue_rules**: (CuedSpeechKeys) Rules to convert phonemes to keys



### Public functions

#### set_cue_rules

```python
def set_cue_rules(self, cue_rules: CuedSpeechKeys) -> None:
    """Set new rules.

        :param cue_rules: (CuedSpeechKeys) Rules and codes for vowel positions and hand shapes

        """
    if isinstance(cue_rules, CuedSpeechKeys) is False:
        raise sppasTypeError('cue_rules', 'CuedSpeechKeys')
    self.__cued = cue_rules
```

*Set new rules.*

##### Parameters

- **cue_rules**: (CuedSpeechKeys) Rules and codes for vowel positions and hand shapes

#### phons_to_segments

```python
def phons_to_segments(self, phonemes: sppasTier) -> sppasTier:
    """Convert time-aligned phonemes into CS segments.

        PhonAlign:            |  b   | O~ |  Z |  u |  R   |
        CS-PhonSegments:      |  b O~     |  Z u    |  R   |

        :param phonemes: (sppasTier) time-aligned phonemes tier
        :return: (sppasTier) Phonemes grouped into key segments

        """
    if isinstance(phonemes, sppasTier) is False:
        raise sppasTypeError('phons', 'sppasTier')
    segments_tier = sppasTier('CS-PhonSegments')
    segments_tier.set_meta('cued_speech_segments_of_tier', phonemes.get_name())
    intervals = sppasWhatKeyPredictor._phon_to_intervals(phonemes)
    for interval in intervals:
        start_phon_idx = phonemes.lindex(interval.get_lowest_localization())
        if start_phon_idx == -1:
            start_phon_idx = phonemes.mindex(interval.get_lowest_localization(), bound=-1)
        end_phon_idx = phonemes.rindex(interval.get_highest_localization())
        if end_phon_idx == -1:
            end_phon_idx = phonemes.mindex(interval.get_highest_localization(), bound=1)
        if start_phon_idx != -1 and end_phon_idx != -1:
            self.__gen_key_segments(phonemes, start_phon_idx, end_phon_idx, segments_tier)
        else:
            logging.warning(info(1224, 'annotations').format(interval))
    return segments_tier
```

*Convert time-aligned phonemes into CS segments.*

PhonAlign:            |  b   | O~ |  Z |  u |  R   |
CS-PhonSegments:      |  b O~     |  Z u    |  R   |

##### Parameters

- **phonemes**: (sppasTier) time-aligned phonemes tier


##### Returns

- (sppasTier) Phonemes grouped into key segments

#### segments_to_keys

```python
def segments_to_keys(self, segments: sppasTier, start_point: sppasPoint | None=None, end_point: sppasPoint=None) -> tuple:
    """Create tiers with the CS denomination and the class of each phoneme.

        CS-PhonSegments:      |  b O~     |  Z u    |   R   |   #   |
        CS-PhonStructs:       |  C V      |  C V    |   C   |       |
        CS-Keys:              |  4 m      |  1 c    |  3 n  |  0 n  |
        CS-KeysClass:         |  C V      |  C V    |  C N  |  N N  |

        :param segments: (sppasTier) A tier in which key segments
        :param start_point: (sppasPoint)
        :param end_point: (sppasPoint)
        :returns: (sppasTier, sppasTier, sppasTier) CS-Keys CS-KeysClass CS-PhonStructs

        """
    key_tier = sppasTier('CS-Keys')
    key_tier.set_meta('cued_speech_key_of_tier', segments.get_name())
    class_tier = sppasTier('CS-KeysClass')
    class_tier.set_meta('cued_speech_phonclass_of_tier', segments.get_name())
    struct_tier = sppasTier('CS-PhonStructs')
    struct_tier.set_meta('cued_speech_struct_of_tier', segments.get_name())
    for ann in segments:
        phons = [label.copy() for label in ann.get_labels()]
        if len(phons) == 0:
            raise ValueError('A CS key should contain at least one phoneme.Got {:d} instead.'.format(len(phons)))
        if len(phons) > 2:
            raise ValueError('A CS key should contain at max two phonemes.Got {:d} instead.'.format(len(phons)))
        if len(phons) == 1:
            content = phons[0].get_best().get_content()
            if self.__cued.get_class(content) == 'V':
                phons.insert(0, sppasLabel(sppasTag('cnil')))
            elif self.__cued.get_class(content) == 'C':
                phons.append(sppasLabel(sppasTag('vnil')))
            else:
                phons.insert(0, sppasLabel(sppasTag(symbols.unk)))
        consonant = phons[0].get_best().get_content()
        consonant_class = self.__cued.get_class(consonant)
        vowel = phons[1].get_best().get_content()
        vowel_class = self.__cued.get_class(vowel)
        labels = self.__create_labels(self.__cued.get_key(consonant), self.__cued.get_key(vowel), phons[0].get_key(), phons[1].get_key())
        a1 = ann.copy()
        a1.set_labels(labels)
        key_tier.append(a1)
        labels = self.__create_labels(consonant_class, vowel_class, phons[0].get_key(), phons[1].get_key())
        a2 = ann.copy()
        a2.set_labels(labels)
        class_tier.append(a2)
        labels = self.__create_labels(consonant_class if consonant_class != 'N' else None, vowel_class if vowel_class != 'N' else None, phons[0].get_key(), phons[1].get_key())
        a3 = ann.copy()
        a3.set_labels(labels)
        struct_tier.append(a3)
    self.__fill_key_segments(key_tier, class_tier, start_point, end_point)
    return (key_tier, class_tier, struct_tier)
```

*Create tiers with the CS denomination and the class of each phoneme.*

CS-PhonSegments:      |  b O~     |  Z u    |   R   |   #   |
CS-PhonStructs:       |  C V      |  C V    |   C   |       |
CS-Keys:              |  4 m      |  1 c    |  3 n  |  0 n  |
CS-KeysClass:         |  C V      |  C V    |  C N  |  N N  |

##### Parameters

- **segments**: (sppasTier) A tier in which key segments
- **start_point**: (sppasPo*int*)
- **end_point**: (sppasPo*int*)


##### Returns

- (sppasTier, sppasTier, sppasTier) CS-Keys CS-KeysClass CS-PhonStructs



### Private functions

#### _phon_to_intervals

```python
@staticmethod
def _phon_to_intervals(phonemes: sppasTier) -> sppasTier:
    """Create a tier with only the intervals to be syllabified.

        We could use symbols.phone only, but for backward compatibility,
        the symbols used in previous versions of SPPAS are added here.

        :param phonemes: (sppasTier)
        :return: a tier with consecutive filled intervals.

        """
    stop = list(symbols.phone.keys())
    stop.append('#')
    stop.append('@@')
    stop.append('+')
    stop.append('gb')
    stop.append('lg')
    return phonemes.export_to_intervals(stop)
```

*Create a tier with only the intervals to be syllabified.*

We could use symbols.phone only, but for backward compatibility,
the symbols used in previous versions of SPPAS are added here.

##### Parameters

- **phonemes**: (sppasTier)


##### Returns

- a tier with consecutive filled intervals.



### Protected functions

#### __gen_key_segments

```python
def __gen_key_segments(self, tier_palign, from_p, to_p, tier_key_segs):
    """Perform the key generation of a sequence of phonemes.

        :param tier_palign: (sppasTier) Time-aligned phonemes
        :param from_p: (int) index of the first phoneme to be syllabified
        :param to_p: (int) index of the last phoneme to be syllabified
        :param tier_key_segs: (sppasTier)

        """
    phons = list()
    for ann in tier_palign[from_p:to_p + 1]:
        tag = ann.get_best_tag()
        phons.append(tag.get_typed_content())
    syll_keys = self.__cued.syllabify(phons)
    for (i, syll) in enumerate(syll_keys):
        (start_idx, end_idx) = syll
        a1 = tier_palign[start_idx + from_p].get_lowest_localization().copy()
        a3 = tier_palign[end_idx + from_p].get_highest_localization().copy()
        location = sppasLocation(sppasInterval(a1, a3))
        labels = list()
        for ann in tier_palign[from_p + start_idx:from_p + end_idx + 1]:
            tag = ann.get_best_tag()
            label = sppasLabel(tag.copy())
            label.set_key(key=ann.get_id())
            labels.append(label)
        tier_key_segs.create_annotation(location, labels)
    return tier_key_segs
```

*Perform the key generation of a sequence of phonemes.*

##### Parameters

- **tier_palign**: (sppasTier) Time-aligned phonemes
- **from_p**: (*int*) index of the first phoneme to be syllabified
- **to_p**: (*int*) index of the last phoneme to be syllabified
- **tier_key_segs**: (sppasTier)

#### __fill_key_segments

```python
def __fill_key_segments(self, tier_keys, tier_class, start_point, end_point):
    """Fill the gaps with the neutral shape and neutral position.

        :param tier_keys: (sppasTier)
        :param tier_class: (sppasTier)

        """
    if len(tier_keys) == 0:
        return
    cn = self.__cued.get_neutral_consonant()
    vn = self.__cued.get_neutral_vowel()
    prev = None
    prev_shape_key = None
    prev_pos_key = None
    prev_shape_class = None
    prev_pos_class = None
    current_pos_key = None
    current_shape_key = None
    if start_point is not None and tier_keys[0].get_lowest_localization() > start_point:
        interval = sppasInterval(start_point.copy(), tier_keys[0].get_lowest_localization())
        labels = [sppasLabel(sppasTag(cn)), sppasLabel(sppasTag(vn))]
        annotation = sppasAnnotation(sppasLocation(interval), labels)
        tier_keys.add(annotation)
        prev_shape_key = cn
        prev_pos_key = vn
        labels = [sppasLabel(sppasTag(self.__cued.NEUTRAL_CLASS)), sppasLabel(sppasTag(self.__cued.NEUTRAL_CLASS))]
        annotation = sppasAnnotation(sppasLocation(interval.copy()), labels)
        tier_class.add(annotation)
        prev_shape_class = self.__cued.NEUTRAL_CLASS
        prev_pos_class = self.__cued.NEUTRAL_CLASS
    for (a, ac) in zip(tier_keys, tier_class):
        fill_hole = False
        if prev is not None and prev.get_highest_localization() < a.get_lowest_localization():
            interval = sppasInterval(prev.get_highest_localization(), a.get_lowest_localization())
            duration = interval.duration().get_value()
            if prev_shape_key == 's' and duration > sppasWhatKeyPredictor.NEUTRAL_SHAPE_THRESHOLD:
                current_shape_key = cn
                current_shape_class = self.__cued.NEUTRAL_CLASS
                fill_hole = True
            else:
                current_shape_key = prev_shape_key
                current_shape_class = prev_shape_class
            if prev_pos_key is not None and duration > sppasWhatKeyPredictor.NEUTRAL_POSITION_THRESHOLD:
                current_pos_key = vn
                current_pos_class = self.__cued.NEUTRAL_CLASS
                fill_hole = True
                current_shape_key = cn
                current_shape_class = self.__cued.NEUTRAL_CLASS
            else:
                current_pos_key = prev_pos_key
                current_pos_class = prev_pos_class
            if fill_hole is True:
                labels = [sppasLabel(sppasTag(current_shape_key)), sppasLabel(sppasTag(current_pos_key))]
                annotation = sppasAnnotation(sppasLocation(interval), labels)
                tier_keys.add(annotation)
                labels = [sppasLabel(sppasTag(current_shape_class)), sppasLabel(sppasTag(current_pos_class))]
                annotation = sppasAnnotation(sppasLocation(interval), labels)
                tier_class.add(annotation)
                prev = annotation
                prev_shape_key = current_shape_key
                prev_shape_class = current_shape_class
                prev_pos_key = current_pos_key
                prev_pos_class = current_pos_class
        if fill_hole is False:
            prev = a
            prev_shape_key = a.get_labels()[0].get_best().get_content()
            prev_shape_class = ac.get_labels()[0].get_best().get_content()
            prev_pos_key = a.get_labels()[1].get_best().get_content()
            prev_pos_class = ac.get_labels()[1].get_best().get_content()
    if end_point is not None and tier_keys[-1].get_highest_localization() < end_point:
        interval = sppasInterval(tier_keys[-1].get_highest_localization(), end_point.copy())
        labels = [sppasLabel(sppasTag(cn)), sppasLabel(sppasTag(vn))]
        annotation = sppasAnnotation(sppasLocation(interval), labels)
        tier_keys.add(annotation)
        labels = [sppasLabel(sppasTag(self.__cued.NEUTRAL_CLASS)), sppasLabel(sppasTag(self.__cued.NEUTRAL_CLASS))]
        annotation = sppasAnnotation(sppasLocation(interval.copy()), labels)
        tier_class.add(annotation)
```

*Fill the gaps with the neutral shape and neutral position.*

##### Parameters

- **tier_keys**: (sppasTier)
- **tier_class**: (sppasTier)

#### __create_labels

```python
@staticmethod
def __create_labels(consonant, vowel, ann_key_c, ann_key_v):
    tag_c = None
    if consonant is not None:
        tag_c = sppasTag(consonant)
    tag_v = None
    if vowel is not None:
        tag_v = sppasTag(vowel)
    cs_c = sppasLabel(tag_c)
    cs_c.set_key(ann_key_c)
    cs_v = sppasLabel(tag_v)
    cs_v.set_key(ann_key_v)
    return [cs_c, cs_v]
```







~ Created using [Clamming](https://clamming.sf.net) version 2.1 ~
