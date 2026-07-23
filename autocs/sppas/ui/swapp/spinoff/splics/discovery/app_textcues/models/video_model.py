"""
:filename: sppas.ui.swapp.spinoff.splics.discovery.app_textcues.models.video_model.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Generate a video for the given sequence of keys.

..
    This file is part of Auto-CS: <https://autocs.sourceforge.io>
    -------------------------------------------------------------------------

    Copyright (C) 2021-2026  Brigitte Bigi, CNRS
    Laboratoire Parole et Langage, Aix-en-Provence, France

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    This banner notice must not be removed.

    -------------------------------------------------------------------------

"""

from __future__ import annotations
from datetime import datetime
import os
import logging
import math

from sppas.core import paths
from sppas.core import separators
from sppas.core import sppasError
from sppas.core import IntervalRangeException
from sppas.core import sppasIOError
from sppas.core import sppasExecProcess
from sppas.src.anndata import sppasTrsRW
from sppas.src.anndata import sppasTranscription
from sppas.src.anndata import sppasTier
from sppas.src.anndata import sppasMedia
from sppas.src.anndata import sppasLocation
from sppas.src.anndata import sppasInterval
from sppas.src.anndata import sppasPoint
from sppas.src.anndata import sppasLabel
from sppas.src.anndata import sppasTag
from sppas.src.annotations.CuedSpeech.whatkey import CuedSpeechKeys
from sppas.src.annotations.CuedSpeech.whenhand.whenhandtrans import sppasWhenHandTransitionPredictor
from sppas.src.annotations.CuedSpeech.wherecue.wherecue import sppasWhereCuePredictor
from sppas.src.annotations.CuedSpeech.whowtag import CuedSpeechVideoTagger
from sppas.src.imgdata import sppasImage
from sppas.src.videodata import sppasVideoWriter
from sppas.ui.swapp.wappcore.wappsg import wapp_settings

from .images_model import PathwayCodeImagesModel

# ---------------------------------------------------------------------------


class PathwayCodeVideoModel(PathwayCodeImagesModel):
    """Generate a video result for a given cued speech sequence.

    """
    
    # The default duration of the silence
    SILENCE_DURATION = 0.80
    
    # The default duration of a phoneme
    DEFAULT_PHON_DURATION = 0.20

    # The default framerate -- allowing a very good output quality
    DEFAULT_FPS = 30

    # -----------------------------------------------------------------------

    def __init__(self, cued_rules: CuedSpeechKeys, prefix: str = "yoyo"):
        """Create a new instance.

        :param cued_rules: (CuedSpeechKeys) The rules of the cued speech.
        :param prefix: (str) Name of both the handset and the face
        :raises: sppasIOError: if prefix does not match valid face and sights files

        """
        super().__init__(cued_rules, prefix)

        self._process = sppasExecProcess()
        success = self._process.test_command("ffmpeg -h")
        if success is False:
            raise RuntimeError("ffmpeg not found. Video can't be generated.")
        
        if os.path.exists(PathwayCodeImagesModel.TMP_PATH) is False:
            os.mkdir(PathwayCodeImagesModel.TMP_PATH)

        # Face image and sights file -- both must exist at construction time.
        _face_path = PathwayCodeImagesModel.IMAGES_PATH + f"{self._prefix}.jpg"
        if os.path.exists(_face_path) is False:
            raise sppasIOError(_face_path)
        self._img = sppasImage(filename=_face_path)

        _face_sight = PathwayCodeImagesModel.IMAGES_PATH + f"{self._prefix}-sights.xra"
        if os.path.exists(_face_sight) is False:
            raise sppasIOError(_face_sight)
        self._sights_labels = self.__extract_image_sights(_face_sight)

        # Tiers generator of hand shapes and hand positions.
        # It answers the "When?" question.
        self.__genhand = sppasWhenHandTransitionPredictor(cue_rules=cued_rules)

        # Tiers generator of vowels & hand coordinates.
        # It answers the "Where?" question. Requires sights.
        self.__gencue = sppasWhereCuePredictor(cue_rules=cued_rules)

        # Video tagger.
        # It answers the "How?" question.
        self.__tagger = CuedSpeechVideoTagger(cued_rules)
        self.__tagger.set_option("handsset", prefix)
        self.__tagger.set_option("handsfilter", "")
        self.__tagger.set_option("infotext", False)
        self.__tagger.set_option("vowelspos", False)

        # Others
        self._fps = PathwayCodeVideoModel.DEFAULT_FPS
        self._pdur = PathwayCodeVideoModel.DEFAULT_PHON_DURATION

    # -----------------------------------------------------------------------
    # Getters/Setters
    # -----------------------------------------------------------------------

    def get_fps(self) -> int:
        """Return the video framerate in frames per second.

        :return: (int) Framerate value.

        """
        return self._fps

    # -----------------------------------------------------------------------

    def get_phon_dur(self) -> float:
        """Return the default phoneme duration in seconds.

        :return: (float) Duration value.

        """
        return self._pdur

    # -----------------------------------------------------------------------

    def set_fps(self, value: int) -> None:
        """Set the video framerate.

        The value must be between 15 and 60 frames per second.

        :param value: (int) Framerate value.
        :raises: sppasTypeError: if value cannot be converted to int.
        :raises: IntervalRangeException: if value is out of [15, 60].

        """
        # Type validation
        try:
            value = int(value)
        except:
            raise sppasTypeError(value, "int")
        # Range validation
        if 15 <= value <= 60:
            self._fps = value
        else:
            raise IntervalRangeException(value, 15, 60)

    # -----------------------------------------------------------------------

    def set_phon_dur(self, value: float) -> None:
        """Set the default phoneme duration.

        The value must be between 0.08 and 0.35 seconds.

        :param value: (float) Duration value in seconds.
        :raises: sppasTypeError: if value cannot be converted to float.
        :raises: IntervalRangeException: if value is out of [0.08, 0.35].

        """
        # Type validation
        try:
            value = float(value)
        except:
            raise sppasTypeError(value, "float")
        # Range validation
        if 0.08 <= value <= 0.35:
            self._pdur = value
        else:
            raise IntervalRangeException(value, 0.08, 0.35)

    # -----------------------------------------------------------------------

    def get_whenpredictor_version(self) -> int:
        """Return the version number of the timing generation system."""
        return self.__genhand.get_whenpredictor_version()

    # -----------------------------------------------------------------------

    def get_wherepositionpredictor_version(self) -> int:
        """Return the version number of the vowel positions prediction system."""
        return self.__gencue.get_wherepositionpredictor_version()

    # -----------------------------------------------------------------------

    def get_whereanglepredictor_version(self) -> int:
        """Return the version number of the angle prediction system."""
        return self.__gencue.get_whereanglepredictor_version()

    # -----------------------------------------------------------------------

    def set_whenpredictor_version(self, version_number: int) -> None:
        """Set the prediction system version.

        - 0: no time estimation.
        - 1: system based on P. Duchnowski et al. (1998)
        - 2: system based on P. Duchnowski et al. (2000)
        - 3: system based on V. Attina (2005) synchronization model
        - 4: empirical rules from B. Bigi & Datha
        - 5: revised rules by B. Bigi

        :param version_number: (int) One of the supported versions.
        :raises: sppasKeyError:
        :raises: TypeError:

        """
        self.__genhand.set_whenpredictor_version(version_number)

    # -----------------------------------------------------------------------

    def set_wherepositionpredictor_version(self, version_number: int) -> None:
        """Change the vowel position predictor version number.

        :param version_number: (int) One of the supported versions.
        :raises: sppasKeyError: if invalid version number

        """
        self.__gencue.set_wherepositionpredictor_version(version_number)

    # -----------------------------------------------------------------------

    def set_whereanglepredictor_version(self, version_number: int) -> None:
        """Change the angle predictor version number.

        :param version_number: (int) One of the supported versions.
        :raises: sppasKeyError: if invalid version number

        """
        self.__gencue.set_whereanglepredictor_version(version_number)

    # -----------------------------------------------------------------------
    # Generator
    # -----------------------------------------------------------------------

    def generate(self, cuedkeys: tuple, cuedphons: tuple, *args, **kwargs) -> str:
        """Return the video filename generated from the given cued keys.

        Example for the French sentence "un exemple de texte":
        - input cuedkeys: ('5-t', '4-c.7-s.2-m.1-s.6-s', '1-b', '5-c.2-s.3-s.5-s')
        - input cuedphons: ('cnil-9~', 'n-E.g-vnil.z-a~.p-vnil.l-@', 'd-2', 't-E.k-vnil.s-vnil.t-@')
        - output: One filename

        :param cuedkeys: (tuple) Cued keys of each token.
        :param cuedphos: (tuple) Phonemes of each key of each token.
        :raises: sppasError: No time aligned keys/segments created.
        :raises: sppasError: No 'prefix' found. 
        :return: (str) filename

        """
        # ------------------------------------------------------------------
        # Predict what and when cueing the given phonemes
        # -----------------------------------------------
        # What? Turn the given cued phons and keys into two time-aligned tiers: CS-PhonSegments and CS-Keys
        tier_phon, tier_segments, tier_keys = self._generate_what_tiers(cuedkeys, cuedphons)
        if len(tier_segments) != len(tier_keys) or len(tier_keys) == 0:
            raise sppasError(f"No time-aligned segments and keys generated from the given keys {cuedkeys} and phons {cuedphons}.")
        _duration = tier_phon.get_last_point().get_midpoint()
        logging.info(f"The sequence {cuedphons} will be coded in {_duration} seconds.")

        # Generate a video from the face, using the tiers duration and a fps value
        # Create a sppasMedia with the created input video
        _vid_filename, _sights_filename = self._generate_video_and_sights(_duration)
        if len(_vid_filename) * len(_sights_filename) == 0:
            raise sppasError(f"No video generated from the given keys {cuedkeys} and phons {cuedphons}, for an expected duration of {_duration} seconds.")

        # When? Predict hand shapes and hand positions
        tier_pos_transitions, tier_shapes_transitions = self.__genhand.when_hands(tier_keys, tier_segments)

        # ------------------------------------------------------------------
        # Predict where the vowels are, relatively to the given sights, where
        # to tag the hand, what is the angle of the hand and its size by
        # predicting S0 and S9 of the hand.
        # ------------------------------------------------------------------
        # Adjust positions to correspond to frames of the video
        adjusted_pos = tier_pos_transitions.copy()
        # Adjust shapes to correspond to frames of the video
        adjusted_shapes = tier_shapes_transitions.copy()
        # Eval where from the video sights and adjusted pos&shapes
        trs_coords = self.__gencue.predict_where(_sights_filename, adjusted_pos, adjusted_shapes)
        trs_coords.append(tier_phon)

        self.__tagger.load(_vid_filename)
        output = _vid_filename.replace(".mp4", "-cued")  # The tagger adds the extension
        self.__tagger.tag_with_keys(trs_coords, output)
        self.__tagger.close()
        os.remove(_vid_filename)
        os.remove(_sights_filename)

        # Convert to web video format
        self.to_webm(output + ".mp4", output + ".webm")
        
        return output + ".webm"

    # -----------------------------------------------------------------------

    def to_webm(self, video_in: str, webm_out: str, crf: int = 16) -> None:
        """Convert a video file to WebM format using libvpx-vp9 (two-pass).

        Two-pass encoding is used to achieve better quality at a given CRF.
        Pass 1 analyses the video and writes statistics to /dev/null.
        Pass 2 produces the final WebM file.

        :param video_in: (str) Path to the input video file.
        :param webm_out: (str) Path for the output WebM file.
        :param crf: (int) CRF quality value for libvpx-vp9 in [0, 63].
                    Lower is better. Defaults to 16.
        :raises: TypeError: video_in or webm_out is not a non-empty string.
        :raises: TypeError: crf is not an integer.
        :raises: ValueError: crf is not in range [0, 63].
        :raises: FileNotFoundError: video_in does not exist.

        """
        if isinstance(video_in, str) is False or len(video_in.strip()) == 0:
            raise TypeError("video_in must be a non-empty string.")
        if isinstance(webm_out, str) is False or len(webm_out.strip()) == 0:
            raise TypeError("webm_out must be a non-empty string.")
        if isinstance(crf, int) is False:
            raise TypeError("crf must be an integer.")
        if crf < 0 or crf > 63:
            raise ValueError("crf must be in range [0, 63].")
        if os.path.exists(video_in) is False:
            raise FileNotFoundError(f"Video {video_in} does not exist.")

        pass1 = (
            f"ffmpeg -i '{video_in}' "
            f"-b:v 0 -crf {crf:d} -pass 1 "
            f"-an -f webm -y /dev/null"
        )
        pass2 = (
            f"ffmpeg -i '{video_in}' "
            f"-b:v 0 -crf {crf:d} -pass 2 "
            f"-c:v libvpx-vp9 "
            f"'{webm_out}'"
        )
        
        try:
            self._process.run(pass1, timeout=90)
            self._process.run(pass2, timeout=90)
        except Exception as e:
            logging.exception(e)
            raise RuntimeError("Command failed. Can't convert mp4 to webm.")
    
    # -----------------------------------------------------------------------
    # Private
    # -----------------------------------------------------------------------

    def _set_media_to_tier(self, tier, media, adjust=False):
        """Set the media to the tier and optionally adjust annotation boundaries.

        :param tier: (sppasTier) The tier to assign the media to.
        :param media: (sppasMedia) The media to assign. Silently ignored if None.
        :param adjust: (bool) If True, move annotation points to match video frames.

        """
        if media is None:
            return
        tier.set_media(media)
        fps = media.get_meta("fps", None)
        if fps is not None and adjust is True:
            # Move all points to match the frames of the media
            self.__ann_on_media.fps = fps
            self.__ann_on_media.adjust_boundaries(tier)

    # -----------------------------------------------------------------------

    def _generate_what_tiers(self, cuedkeys: tuple, cuedphons: tuple) -> tuple:
        """Return three time-aligned tiers built from the given cued keys and phonemes.

        Data example:
         > cuedkeys = ( "5-t", "4-c.7-s.2-m.1-s.6-s" )
         > cuedphons = ( "cnil-9~", "n-E.g-vnil.z-a~.p-vnil.l-@" )
        then at 2nd loop (for each coded token):
            > coded_phons = ['n-E', 'g-vnil', 'z-a~', 'p-vnil', 'l-@']
            > coded_keys = ['4-c', '7-s', '2-m', '1-s', '6-s']
            then loop (for each coded key) 
                - _i = 0: _code_cv = ('4', 'c') ; _phon_cv = ('n', 'E')
                    * shape = 4
                    * position = c
                    * consonant = n
                    * vowel = E
                - _i = 1: _code_cv = ('7', 's') ; _phon_cv = ('g', 'vnil')
                    * shape = 7
                    * position = s
                    * consonant = g
                    * vowel = vnil
                - _i = 2: _code_cv = ('2', 'm') : _phon_cv = ('z', 'a~')
                    * shape = 2
                    * position = m
                    * consonant = z
                    * vowel = a~
                ...

        :param cuedkeys: (tuple) Cued Speech keys, one entry per token.
        :param cuedphons: (tuple) Coded phonemes, one entry per token.
        :raises: ValueError: if a coded key is empty or malformed.
        :return: (tuple) PhonAlign tier, CS-PhonSegments tier, CS-Keys tier.

        """
        _tier_phons = sppasTier("PhonAlign")
        _tier_sgmts = sppasTier("CS-PhonSegments")
        _tier_keys = sppasTier("CS-Keys")
        # Add a silence before starting to code
        _loc = sppasLocation(sppasInterval(sppasPoint(0.), sppasPoint(self.SILENCE_DURATION)))
        _tier_phons.create_annotation(_loc, sppasLabel(sppasTag("sil")))
        _cur_pos = self.SILENCE_DURATION
        
        # for each coded token
        # --------------------
        for coded_key_seq, coded_phon_seq in zip(cuedkeys, cuedphons):
            coded_phons = tuple(coded_phon_seq.split(separators.syllables))
            coded_keys = tuple(coded_key_seq.split(separators.syllables))

            # for each coded key
            # ------------------
            for _i, coded_key in enumerate(coded_keys):
                if len(coded_key) == 0:
                    raise ValueError(f"Given coded_key is an empty string, "
                                     f"at index {_i} of cued keys: {cuedkeys}.")

                _code_cv = tuple(coded_key.split(separators.phonemes))
                _phon_cv = tuple(coded_phons[_i].split(separators.phonemes))
                if len(_code_cv) != 2 or len(_phon_cv) != 2:
                    raise ValueError(f"Given coded_key is invalid at index {_i} of cued keys: {cuedkeys}. Got '{_code_cv}' and '{_phon_cv}' instead.")
                
                # Get phoneme durations and create annotations
                _c_dur, _v_dur = self.__predict_durations(_code_cv, _phon_cv)
                if _cur_pos == self.SILENCE_DURATION:
                    _c_dur = _c_dur * 2.
                    _v_dur = _v_dur * 1.5
                _next_pos = _cur_pos + _c_dur + _v_dur
                _tier_phons.create_annotation(
                    sppasLocation(sppasInterval(sppasPoint(_cur_pos), sppasPoint(_cur_pos+_c_dur))),
                    sppasLabel(sppasTag(_phon_cv[0]))
                )
                _tier_phons.create_annotation(
                    sppasLocation(sppasInterval(sppasPoint(_cur_pos + _c_dur), sppasPoint(_next_pos))),
                    sppasLabel(sppasTag(_phon_cv[1]))
                )

                _loc = sppasLocation(sppasInterval(sppasPoint(_cur_pos), sppasPoint(_next_pos)))
                _tier_sgmts.create_annotation(_loc, [sppasLabel(sppasTag(_phon_cv[0])), sppasLabel(sppasTag(_phon_cv[1]))])
                _tier_keys.create_annotation(_loc, [sppasLabel(sppasTag(_code_cv[0])), sppasLabel(sppasTag(_code_cv[1]))])

                _cur_pos = _next_pos

        # Add a silence after the code
        _loc = sppasLocation(sppasInterval(sppasPoint(_cur_pos), sppasPoint(_cur_pos + self.SILENCE_DURATION)))
        _tier_phons.create_annotation(_loc, sppasLabel(sppasTag("sil")))
        return _tier_phons, _tier_sgmts, _tier_keys

    # -----------------------------------------------------------------------

    def _generate_video_and_sights(self, duration: float) -> tuple:
        """Generate a plain face video and a matching sights file for the given duration.

        :param duration: (float) Expected duration of the video in seconds.
        :return: (tuple) video filename, sights filename.

        """
        # Fix basename for files
        _dirname = self.__generate_temp_basename()
        os.mkdir(_dirname)
        logging.info(f"Temporary basename for created files: {_dirname}")

        # Create intermediate objects: image/video
        _w, _h = self._img.size()
        _vid_filename, _vid_writer = self.__open_video(_dirname, _w, _h)

        # Create intermediate objects: tier/sights
        _tier = sppasTier("VideoCoords")

        # A partial frame must be counted as a full frame to avoid cutting 
        # the last key short.
        _nb_frames = math.ceil(duration * self._fps)
        # Radius is half frame duration (vagueness of the sights is one frame)
        _radius = (1. / self._fps) / 2.  

        for _i in range(_nb_frames):
            _vid_writer.write(self._img)
            _a = _tier.create_annotation(
                sppasLocation(sppasPoint((_i / self._fps) + _radius, _radius)),
                self._sights_labels.copy()
                )
            # <Entry key="frame_index">0</Entry>
            _a.set_meta("frame_index", str(_i))

        _vid_writer.close()
        # The media must be assigned to the tier; it is required by the SightsReader
        _vid_media = sppasMedia(os.path.abspath(_vid_filename), mime_type="video/mp4")
        _vid_media.set_meta("fps", str(self._fps))
        _vid_media.set_meta("duration", str(duration))
        _vid_media.set_meta("size", str(self._img.size()))
        _tier.set_media(_vid_media)
        _trs_filename = self.__save_sights(_dirname, _tier) 

        return _vid_filename, _trs_filename
    
    # -----------------------------------------------------------------------
    # PRIVATE
    # -----------------------------------------------------------------------

    def __generate_temp_basename(self):
        """Return a timestamped basename for output files.

        Unused and staying here for a further use, eventually.

        :return: (str) Absolute basename including prefix and timestamp.

        """
        now = datetime.now()
        date_str = now.strftime('%Y_%m_%d')
        seconds_since_midnight = now.hour * 3600 + now.minute * 60 + now.second

        return PathwayCodeImagesModel.TMP_PATH + self._prefix + date_str + "_" + str(seconds_since_midnight)
    
    # -----------------------------------------------------------------------

    def __predict_durations(self, key_code: tuple, key_phons: tuple) -> tuple:
        """Return the duration of the consonant and the vowel in seconds.

        Approximation until a decision tree, a neural network or any optimized
        model is learned from a coded corpus.

        :param key_code: (tuple) Coded shape and position (e.g. ('4', 'c')).
        :param key_phons: (tuple) Coded consonant and vowel (e.g. ('n', 'E')).
        :return: (tuple) consonant duration, vowel duration.

        """
        # Default durations
        _cd = self._pdur
        _vd = self._pdur

        # Reduce duration for null phonemes (no acoustic content to produce)
        consonant, vowel = key_phons
        if vowel == "vnil":
            _vd = _vd * 0.5
        if consonant == "cnil":
            _cd = _cd * 0.5

        return _cd, _vd

    # -----------------------------------------------------------------------

    def __open_video(self, dirname: str, w: int, h: int) -> tuple:
        """Open a new video writer and return the output filename and the writer.

        :param dirname: (str) Directory where the video file will be created.
        :param w: (int) Video frame width in pixels.
        :param h: (int) Video frame height in pixels.
        :return: (tuple) output filename, sppasVideoWriter instance.

        """
        _vid_writer = sppasVideoWriter()
        _vid_writer.set_size(w, h)
        _vid_writer.set_fps(self._fps)
        _filename = os.path.join(dirname, self._prefix + ".mp4")
        _vid_writer.open(_filename)

        return _filename, _vid_writer

    # -----------------------------------------------------------------------

    def __extract_image_sights(self, face_sights: str) -> list:
        """Read the sights file and return the labels of the single annotation.

        :return: (list) Labels of the sights annotation.
        :raises: sppasIOError: if the file does not contain exactly one tier with one annotation.

        """
        # Read the sights file
        parser = sppasTrsRW(face_sights)
        trs = parser.read()
        # Validate structure: exactly one tier with one annotation expected
        if len(trs) != 1:
            raise sppasIOError(f"Expected only one tier in file {face_sights}. "
                               f"Got {len(trs)} instead.")
        if len(trs[0]) != 1:
            raise sppasIOError(f"Expected only one annotation in file {face_sights}. "
                               f"Got {len(trs[0])} instead.")

        return trs[0][0].get_labels()

    # -----------------------------------------------------------------------

    def __save_sights(self, dirname: str, tier: sppasTier) -> str:
        """Save the given sights tier to an XRA file and return the filename.

        :param dirname: (str) Directory where the XRA file will be created.
        :param tier: (sppasTier) Tier containing the video frame sights.
        :return: (str) Absolute path of the created XRA file.

        """
        _filename = os.path.join(dirname, self._prefix + ".xra")
        _trs = sppasTranscription(self._prefix)
        _trs.append(tier)
        _parser = sppasTrsRW(_filename)
        _parser.write(_trs)
        return _filename

# ---------------------------------------------------------------------------

# Launch with: python -m sppas.ui.swapp.app_textcues.models.video_model
if __name__ == "__main__":
    cuedkeys = (
        "5-t",
        "4-c.7-s.2-m.1-s.6-s",
        "1-b",
        "5-c.2-s.3-s.5-s",
    )

    cuedphons = (
        "cnil-9~",
        "n-E.g-vnil.z-a~.p-vnil.l-@",
        "d-2",
        "t-E.k-vnil.s-vnil.t-@",
    )

    cued_rules = CuedSpeechKeys(paths.resources + "/cuedspeech/cueConfig-fra.txt")

    model = PathwayCodeVideoModel(cued_rules, prefix="yoyo")
    output_filename = model.generate(cuedkeys, cuedphons)

    print(output_filename)
