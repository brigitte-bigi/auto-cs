# CuedSpeech module

## List of classes

## Class `sppasAnnsOnFrames`

### Description

Move points to match with the framerate of the media




### Constructor

#### __init__

```python
def __init__(self, fps=60.0):
    self.__fps = float(fps)
```





### Public functions

#### get_fps

```python
def get_fps(self):
    """Return framerate (float)."""
    return self.__fps
```

*Return framerate (float).*

#### set_fps

```python
def set_fps(self, value: float):
    """Set a new framerate.

        :param value: (float) A framerate.

        """
    try:
        value = float(value)
    except:
        raise TypeError('Expected a float.')
    if value < 0.0:
        raise ValueError('Invalid framerate. ')
    self.__fps = value
```

*Set a new framerate.*

##### Parameters

- **value**: (*float*) A framerate.

#### adjust_boundaries

```python
def adjust_boundaries(self, tier):
    """Move boundaries to frames of a video.

        :param tier: (sppasTier) Tier to be adjusted.

        """
    for ann in tier:
        begin_point = ann.get_lowest_localization()
        end_point = ann.get_highest_localization()
        new_begin = self.adjust_point_boundary(begin_point)
        new_end = self.adjust_point_boundary(end_point)
        ann.set_best_localization(sppasInterval(new_begin, new_end))
```

*Move boundaries to frames of a video.*

##### Parameters

- **tier**: (sppasTier) Tier to be adjusted.

#### adjust_point_boundary

```python
def adjust_point_boundary(self, point):
    """Move a point to a frame of a video.

        Put the midpoint either between 2 frames or at the middle of a frame.
        Set the radius to fully cover 0, 1 or 2 frames.

        :param tier: (sppasTier) Tier to be adjusted.

        """
    frame_duration = 1.0 / self.__fps
    half_frame = frame_duration / 2.0
    quart_frame = frame_duration / 4.0
    nframes = int(point.get_midpoint() / frame_duration)
    s = nframes * frame_duration
    m = s + frame_duration / 2.0
    radius = point.get_radius()
    if s <= point.get_midpoint() < s + quart_frame:
        midpoint = s
        if radius is None or (radius is not None and radius < quart_frame):
            radius = 0.0
        else:
            radius = frame_duration
    elif s + quart_frame <= point.get_midpoint() < m + quart_frame:
        midpoint = m
        if radius is None or (radius is not None and radius < frame_duration):
            radius = half_frame
        else:
            radius = 1.5 * frame_duration
    else:
        midpoint = s + frame_duration
        if radius is None or (radius is not None and radius < quart_frame):
            radius = 0.0
        else:
            radius = frame_duration
    return sppasPoint(midpoint, radius)
```

*Move a point to a frame of a video.*

Put the midpoint either between 2 frames or at the middle of a frame.
Set the radius to fully cover 0, 1 or 2 frames.

##### Parameters

- **tier**: (sppasTier) Tier to be adjusted.



## Class `sppasCuedSpeech`

### Description

*SPPAS integration of the automatic Cued Speech key-code generation.*




### Constructor

#### __init__

```python
def __init__(self, log=None):
    """Create a new instance.

    Log is used for a better communication of the annotation process and its
    results. If None, logs are redirected to the default logging system.

    :param log: (sppasLog) Human-readable logs.

    """
    super(sppasCuedSpeech, self).__init__('cuedspeech.json', log)
    self.__lang = 'und'
    self.__cued = CuedSpeechKeys()
    self.__genkey = sppasWhatKeyPredictor()
    self.__genhand = sppasWhenHandTransitionPredictor(predictor_version=self._options['handtrans'])
    self.__gencue = sppasWhereCuePredictor()
    self.__tagger = None
    self.__ann_on_media = sppasAnnsOnFrames(fps=60.0)
```

*Create a new instance.*

Log is used for a better communication of the annotation process and its
results. If None, logs are redirected to the default logging system.

##### Parameters

- **log**: (sppasLog) Human-readable logs.



### Public functions

#### load_resources

```python
def load_resources(self, config_filename, lang='und', **kwargs):
    """Fix the keys from a configuration file.

        :param config_filename: Name of the configuration file with the keys
        :param lang: (str) Iso639-3 of the language or "und" if unknown.

        """
    self.__lang = lang
    if lang != 'und':
        self.__cued.load(config_filename)
    self.__genkey.set_cue_rules(self.__cued)
    self.__genhand.set_cue_rules(self.__cued)
    self.__gencue.set_cue_rules(self.__cued)
    if self._options['createvideo'] is True:
        self.__set_video_tagger()
```

*Fix the keys from a configuration file.*

##### Parameters

- **config_filename**: Name of the configuration file with the keys
- **lang**: (*str*) Iso639-3 of the language or "und" if unknown.

#### fix_options

```python
def fix_options(self, options):
    """Fix all options.

        Available options are:

            - inputpattern1, inputpattern2, inputpattern3, outputpattern,
            - createvideo: boolean
            - handtrans: version of the hand transition estimator model
            - handangle: version of the hand angle estimator model
            - handsset: name of the hand pictures set, or empty string to draw badges
            - angleface: boolean (hand angle is corrected by face angle)
            - infotext: boolean
            - vowelspos: boolean

        :param options: (sppasOption)

        """
    for opt in options:
        key = opt.get_key()
        if 'createvideo' == key:
            self.set_create_video(opt.get_value())
        elif 'pattern' in key:
            self._options[key] = opt.get_value()
        elif 'handtrans' == key:
            self.set_when_handtrans_version(opt.get_value())
        elif 'handangle' == key:
            self.set_where_handangle_version(opt.get_value())
        elif 'handpos' == key:
            self.set_where_handposition_version(opt.get_value())
        elif 'angleface' == key:
            self.set_where_angleface_correction(opt.get_value())
        elif key in CuedSpeechVideoTagger.OPTIONS:
            self._options[key] = opt.get_value()
            if self.__tagger is not None:
                self.__tagger.set_option(key, opt.get_value())
                self._options[key] = opt.get_value()
        else:
            raise AnnotationOptionError(key)
```

*Fix all options.*

Available options are:

- inputpattern1, inputpattern2, inputpattern3, outputpattern,
- createvideo: boolean
- handtrans: version of the hand transition estimator model
- handangle: version of the hand angle estimator model
- handsset: name of the hand pictures set, or empty string to draw badges
- angleface: boolean (hand angle is corrected by face angle)
- infotext: boolean
- vowelspos: boolean

##### Parameters

- **options**: (sppasOption)

#### set_when_handtrans_version

```python
def set_when_handtrans_version(self, version=4):
    """Fix the version of the hand transition times generator.

        :param version: (int)

        """
    all_versions = self.__genhand.get_whenpredictor_versions()
    version = int(version)
    if version not in all_versions:
        msg = "Invalid version number '{}' for transition times. Expected one of {}".format(version, all_versions)
        self.logfile.print_message(msg, status=annots.error)
        version = 4
    self.__genhand.set_whenpredictor_version(version)
    self._options['handtrans'] = version
```

*Fix the version of the hand transition times generator.*

##### Parameters

- **version**: (*int*)

#### set_where_handposition_version

```python
def set_where_handposition_version(self, version=1):
    """Fix the version of the vowel' positions generator.

        :param version: (int)

        """
    all_versions = self.__gencue.get_wherepositionpredictor_versions()
    version = int(version)
    if version not in all_versions:
        msg = "Invalid version number '{}' for vowels positions predictor. Expected one of {}".format(version, all_versions)
        self.logfile.print_message(msg, status=annots.error)
        version = 1
    self.__gencue.set_wherepositionpredictor_version(version)
    self._options['handpos'] = version
```

*Fix the version of the vowel' positions generator.*

##### Parameters

- **version**: (*int*)

#### set_where_handangle_version

```python
def set_where_handangle_version(self, version: int=1):
    """Fix the version of the hand angle generator.

        :param version: (int)

        """
    all_versions = self.__gencue.get_whereanglepredictor_versions()
    version = int(version)
    if version not in all_versions:
        msg = "Invalid version number '{}' for angle predictor. Expected one of {}".format(version, all_versions)
        self.logfile.print_message(msg, status=annots.error)
        version = 1
    self.__gencue.set_whereanglepredictor_version(version)
    self._options['handangle'] = version
```

*Fix the version of the hand angle generator.*

##### Parameters

- **version**: (*int*)

#### set_where_angleface_correction

```python
def set_where_angleface_correction(self, value: bool=False):
    """Whether correct tha hand angle or not with the face one.

        :param value: (bool)

        """
    value = bool(value)
    self.__gencue.set_angle_use_face(value)
    self._options['angleface'] = value
```

*Whether correct tha hand angle or not with the face one.*

##### Parameters

- **value**: (*bool*)

#### set_create_video

```python
def set_create_video(self, create=True):
    """Fix the createvideo option.

        :param create: (bool)

        """
    create = bool(create)
    self._options['createvideo'] = create
    if create is True:
        self.__set_video_tagger()
    else:
        self.__tagger = None
```

*Fix the createvideo option.*

##### Parameters

- **create**: (*bool*)

#### convert

```python
def convert(self, phonemes, media):
    """Syllabify labels of a time-aligned phones tier.

        :param phonemes: (sppasTier) time-aligned phonemes tier
        :param media: (sppasMedia) a media representing the video file
        :returns: (sppasTier*6)

        """
    cs_segments = self.__genkey.phons_to_segments(phonemes)
    (cs_keys, cs_class, cs_struct) = self.__genkey.segments_to_keys(cs_segments, phonemes.get_first_point(), phonemes.get_last_point())
    (cs_pos, cs_shapes) = self.__genhand.when_hands(cs_keys, cs_segments)
    return (cs_segments, cs_keys, cs_class, cs_struct, cs_shapes, cs_pos)
```

*Syllabify labels of a time-aligned phones tier.*

##### Parameters

- **phonemes**: (sppasTier) time-aligned phonemes tier
- **media**: (sppasMedia) a media representing the video file


##### Returns

- (sppasTier*6)

#### make_video

```python
def make_video(self, video_file, trs, output):
    """Create a video with the tagged keys.

        :param video_file: (str) Filename of the given video
        :param trs: (sppasTranscription) All required tiers to tag the video
        :param output: (str) Output file name

        """
    if cfg.feature_installed('video') is True and self.__tagger is not None:
        self.logfile.print_message('Create the tagged video', status=annots.info)
        self.__tagger.load(video_file)
        self.__tagger.tag_with_keys(trs, output)
        self.__tagger.close()
    else:
        self.logfile.print_message(f"To tag a video, the video support feature must be enabled ({cfg.feature_installed('video')}) and a video tagger must be instantiated ({self.__tagger is not None}).", status=annots.error)
```

*Create a video with the tagged keys.*

##### Parameters

- **video_file**: (*str*) Filename of the given video
- **trs**: (sppasTranscription) All required tiers to tag the video
- **output**: (*str*) Output file name

#### get_inputs

```python
def get_inputs(self, input_files):
    """Return the media and the annotated filenames.

        :param input_files: (list)
        :raise: NoInputError
        :return: (str, str) Names of the 3 expected files

        """
    ext = self.get_input_extensions()
    media_ext = [e.lower() for e in ext[1]]
    phons_ext = [e.lower() for e in ext[0]]
    sights_ext = [e.lower() for e in ext[2]]
    media = None
    annot_phons = None
    annot_sights = None
    pphones = self._options['inputpattern1']
    psights = self._options['inputpattern3']
    for filename in input_files:
        if filename is None:
            continue
        (fn, fe) = os.path.splitext(filename)
        if media is None and fe in media_ext:
            media = filename
        elif annot_phons is None and fe.lower() in phons_ext and fn.endswith(pphones):
            annot_phons = filename
        elif annot_sights is None and fe.lower() in sights_ext and fn.endswith(psights):
            annot_sights = filename
    if annot_phons is None:
        logging.error('The annotated file with time-aligned phonemes was not found.')
        raise NoInputError
    return (media, annot_phons, annot_sights)
```

*Return the media and the annotated filenames.*

##### Parameters

- **input_files**: (*list*)


##### Raises

NoInputError


##### Returns

- (*str*, *str*) Names of the 3 expected files

#### create_media

```python
def create_media(self, video_filename):
    """Create a sppasMedia() instance from a video filename.

        """
    if video_filename is None:
        return None
    extm = os.path.splitext(video_filename.lower())[1]
    video_media = sppasMedia(os.path.abspath(video_filename), mime_type='video/' + extm)
    try:
        vid = sppasVideoReader()
        vid.open(video_filename)
        video_media.set_meta('fps', str(vid.get_framerate()))
        video_media.set_meta('duration', str(vid.get_duration()))
        video_media.set_meta('size', str(vid.get_size()))
        vid.close()
    except:
        pass
    return video_media
```

*Create a sppasMedia() instance from a video filename.*



#### run

```python
def run(self, input_files, output=None):
    """Run the automatic annotation process on an input.

        :param input_files: (list of str) time-aligned phonemes, and optionally video, csv files
        :param output: (str) the output name
        :returns: (sppasTranscription)

        """
    try:
        do_vid = False
        (file_video, file_phons, file_sights) = self.get_inputs(input_files)
        video_media = self.create_media(file_video)
        parser = sppasTrsRW(file_phons)
        trs_input = parser.read()
        tier_phon = sppasFindTier.aligned_phones(trs_input)
        trs_output = sppasTranscription(self.name)
        self._set_trs_metadata(trs_output, file_phons)
        (tier_cs, tier_key, tier_class, tier_struct, tier_shapes_transitions, tier_pos_transitions) = self.convert(tier_phon, video_media)
        trs_output.append(tier_cs)
        trs_output.append(tier_struct)
        trs_output.append(tier_key)
        trs_output.append(tier_class)
        trs_output.append(tier_shapes_transitions)
        trs_output.append(tier_pos_transitions)
        trs_coords = sppasTranscription(self.name)
        self._set_trs_metadata(trs_coords, file_phons)
        if file_sights is not None:
            if video_media is not None:
                trs_coords.add_media(video_media)
                adjusted_pos = tier_pos_transitions.copy()
                self._set_media_to_tier(adjusted_pos, video_media, adjust=True)
                trs_coords.append(adjusted_pos)
                adjusted_shapes = tier_shapes_transitions.copy()
                self._set_media_to_tier(adjusted_shapes, video_media, adjust=True)
                trs_coords.append(adjusted_shapes)
                trs_coords = self.__gencue.predict_where(file_sights, adjusted_pos, adjusted_shapes)
            else:
                trs_coords = self.__gencue.predict_where(file_sights, tier_pos_transitions, tier_shapes_transitions)
            trs_coords.append(tier_phon)
            for tier in trs_coords:
                self._set_media_to_tier(tier, video_media, adjust=False)
            if self._options['createvideo']:
                if len(input_files) > 2:
                    if file_video is not None and file_sights is not None:
                        do_vid = True
                        self.make_video(file_video, trs_coords, output)
                if do_vid is False:
                    self.logfile.print_message('The option to tag the video was enabled but no video/csv corresponding to the annotated file {:s} was found.'.format(input_files[0]), status=-1)
        else:
            logging.info('No sights available.')
        if output is None:
            return trs_output
        outputs = list()
        output_file = self.fix_out_file_ext(output)
        if len(trs_output) > 0:
            parser = sppasTrsRW(output_file)
            parser.write(trs_output)
            outputs.append(output_file)
        else:
            raise EmptyOutputError
        if output is not None:
            coords_output = output_file.replace(self.get_output_pattern(), '-coords')
            parser = sppasTrsRW(coords_output)
            parser.write(trs_coords)
            outputs.append(coords_output)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise
    return outputs
```

*Run the automatic annotation process on an input.*

##### Parameters

- **input_files**: (*list* of *str*) time-aligned phonemes, and optionally video, csv files
- **output**: (*str*) the output name


##### Returns

- (sppasTranscription)

#### get_output_pattern

```python
def get_output_pattern(self):
    """Pattern this annotation uses in an output filename."""
    return self._options.get('outputpattern', '-cuedspeech')
```

*Pattern this annotation uses in an output filename.*

#### get_input_patterns

```python
def get_input_patterns(self):
    """Pattern this annotation expects for its input filename."""
    return [self._options.get('inputpattern1', '-palign'), self._options.get('inputpattern2', ''), self._options.get('inputpattern3', '-sights')]
```

*Pattern this annotation expects for its input filename.*

#### get_input_extensions

```python
@staticmethod
def get_input_extensions():
    """Extensions that the annotation expects for its input filename.

        Priority is given to video files, then image files.

        """
    media_ext = list(sppasFiles.get_informat_extensions('VIDEO'))
    for img_ext in sppasFiles.get_informat_extensions('IMAGE'):
        media_ext.append(img_ext)
    return [sppasFiles.get_informat_extensions('ANNOT_ANNOT'), media_ext, ['.xra', '.csv']]
```

*Extensions that the annotation expects for its input filename.*

Priority is given to video files, then image files.

#### get_hands_sets

```python
@staticmethod
def get_hands_sets() -> list:
    """List of all hands sets in the resources.cuedspeech folder.

        :return: (list) A list of all hands sets available.

        """
    hand_manager = sppasHandResource()
    hand_manager.automatic_loading()
    return hand_manager.get_hand_sets_identifiers()
```

*List of all hands sets in the resources.cuedspeech folder.*

##### Returns

- (*list*) A list of all hands sets available.

#### get_hands_filters

```python
@staticmethod
def get_hands_filters() -> list:
    """List of all available hands filters.

        :return: (list) A list of all hands filters.

        """
    return CuedSpeechVideoTagger.get_hands_filters()
```

*List of all available hands filters.*

##### Returns

- (*list*) A list of all hands filters.



### Private functions

#### _set_media_to_tier

```python
def _set_media_to_tier(self, tier, media, adjust=False):
    """Set the media to the tier and adjust annotation boundaries.

        """
    if media is None:
        return
    tier.set_media(media)
    fps = media.get_meta('fps', None)
    if fps is not None and adjust is True:
        self.__ann_on_media.fps = fps
        self.__ann_on_media.adjust_boundaries(tier)
```

*Set the media to the tier and adjust annotation boundaries.*



#### _set_trs_metadata

```python
def _set_trs_metadata(self, trs, filename):
    trs.set_meta('annotation_result_of', filename)
    trs.set_meta('language_iso', 'iso639-3')
    trs.set_meta('language_name_0', 'Undetermined')
    if len(self.__lang) == 3:
        trs.set_meta('language_code_0', self.__lang)
        trs.set_meta('language_url_0', 'https://iso639-3.sil.org/code/' + self.__lang)
    else:
        trs.set_meta('language_code_0', 'und')
        trs.set_meta('language_url_0', 'https://iso639-3.sil.org/code/und')
```





### Protected functions

#### __set_video_tagger

```python
def __set_video_tagger(self):
    try:
        if self.__tagger is None:
            self.__tagger = CuedSpeechVideoTagger(self.__cued)
            for key in CuedSpeechVideoTagger.OPTIONS:
                if key in self._options:
                    self.__tagger.set_option(key, self._options[key])
        else:
            self.__tagger.set_cue_rules(self.__cued)
    except sppasEnableFeatureError as e:
        self.__tagger = None
        logging.warning("Cued Speech Video Tagger can't be enabled: {:s}".format(str(e)))
```







~ Created using [Clamming](https://clamming.sf.net) version 2.1 ~
