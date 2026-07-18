"""
:filename: sppas.ui.swapp.app_textcues.models.overlays_model.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Generate overlay images for the given sequence of keys.

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
import os
import logging
from datetime import datetime

from sppas.core import paths
from sppas.core import separators
from sppas.core import sppasIOError
from sppas.src.imgdata import sppasImage
from sppas.src.imgdata import sppasCoords
from sppas.src.imgdata import sppasSights
from sppas.src.imgdata import sppasImageSightsReader
from sppas.src.anndata import sppasTrsRW
from sppas.src.anndata import sppasFuzzyPoint
from sppas.src.annotations.CuedSpeech.whatkey import CuedSpeechKeys
from sppas.src.annotations.CuedSpeech.wherecue.positions import WhereVowelPositionsPredictor
from sppas.src.annotations.CuedSpeech.wherecue.angles import WhereAnglesPredictor
from sppas.src.annotations.CuedSpeech.wherecue.faceheight import sppasFaceHeight
from sppas.src.annotations.CuedSpeech.whowtag.whowimgtag import sppasHandCoords
from sppas.src.annotations.CuedSpeech.whowtag.whowimgtag import sppasImageHandTagger
from sppas.ui.swapp.wappcore.wappsg import wapp_settings

from .images_model import PathwayCodeImagesModel

# ---------------------------------------------------------------------------

COLORS = {
    "t": (90, 75, 24),
    "s": (139, 91, 42),
    "m": (9, 68, 127),
    "c": (179, 26, 95),
    "b": (88, 21, 161)
}

# ---------------------------------------------------------------------------


class PathwayCodeOverlayModel(PathwayCodeImagesModel):
    """Generates image results for a given cued sequence.

    """

    def __init__(self, cued_rules: CuedSpeechKeys, prefix: str = "yoyo"):
        """Create a new instance.

        :param cued_rules: (CuedSpeechKeys) The rules of the cued speech.
        :param prefix: (str) Name of both the handset and the face
        :raises: sppasIOError: if prefix does not match valid face and sights files
        :raises: sppasIOError: If invalid hands set with given prefix

        """
        super().__init__(cued_rules, prefix)

        # Face image and sights file -- both must exist at construction time.
        self._face_path = PathwayCodeImagesModel.IMAGES_PATH + f"{self._prefix}.jpg"
        self._face_sight = PathwayCodeImagesModel.IMAGES_PATH + f"{self._prefix}-sights.xra"
        if os.path.exists(self._face_path) is False:
            raise sppasIOError(self._face_path)
        if os.path.exists(self._face_sight) is False:
            raise sppasIOError(self._face_sight)
        # Get the face image and its sights
        self._img = sppasImage(filename=self._face_path)
        self._sights = self.__extract_image_sights()

        # Predict the size of the hand
        self._face_dist = sppasFaceHeight.eval_height(self._sights)

        # Default predictor models
        self._model_pos = WhereVowelPositionsPredictor()
        self._model_pos.set_sights_and_predict_coords(self._sights, self._cs.get_vowels_codes())

        self._model_angle = WhereAnglesPredictor()
        self._model_angle.predict_angle_values(self._cs.get_vowels_codes())

        self.__img_tagger = sppasImageHandTagger(self._cs)
        self.__img_tagger.load_hands(prefix)
        self.__img_tagger.enable_hand_mode()

    # -----------------------------------------------------------------------
    # Getters and setters
    # -----------------------------------------------------------------------

    def get_wherepositionpredictor_version(self) -> int:
        """Return the version number of the vowel positions prediction system."""
        return self._model_pos.get_version_number()

    # -----------------------------------------------------------------------

    def get_whereanglepredictor_version(self) -> int:
        """Return the version number of the angle prediction system."""
        return self._model_angle.get_version_number()

    # -----------------------------------------------------------------------

    def set_model_angle(self, model_number: int):
        self._model_angle = WhereAnglesPredictor(model_number)
        self._model_angle.predict_angle_values(self._cs.get_vowels_codes())

    # -----------------------------------------------------------------------

    def set_model_position(self, model_number: int):
        self._model_pos = WhereVowelPositionsPredictor(model_number)
        self._model_pos.set_sights_and_predict_coords(self._sights, self._cs.get_vowels_codes())

    # -----------------------------------------------------------------------
    # Generator
    # -----------------------------------------------------------------------

    def generate(self, cuedkeys: tuple, cuedphons: tuple, *args, **kwargs) -> tuple:
        """Generate the images filepath matching the given cued keys.

        Example for the French sentence "un exemple de texte":
        - input cuedkeys: ('5-t', '4-c.7-s.2-m.1-s.6-s', '1-b', '5-c.2-s.3-s.5-s')
        - input cuedphons: ('cnil-9~', 'n-E.g-vnil.z-a~.p-vnil.l-@', 'd-2', 't-E.k-vnil.s-vnil.t-@')
        - output: 11 filenames in a tuple with 4 entries - because 11 keys, 4 tokens.

        :param cuedkeys: (tuple) Cued Speech keys of each token.
        :return: (tuple) Filepath of overlaid images

        """
        # Fix basename for files
        _dirname = self.__generate_temp_basename()
        os.mkdir(_dirname)
        logging.info(f"Temporary basename for created files: {_dirname}")

        result = list()

        # for each coded token
        # --------------------
        for coded_key_seq, coded_phon_seq in zip(cuedkeys, cuedphons):
            coded_phons = tuple(coded_phon_seq.split(separators.syllables))
            coded_keys = tuple(coded_key_seq.split(separators.syllables))
            token_result = list()

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
                
                try:
                    _filename = self._generate_coded_image(_dirname, _code_cv[0], _code_cv[1])
                    token_result.append(_filename)
                except Exception as e:
                    logging.exception(str(e))
                    token_result.append(None)
            
            result.append(token_result)

        if all(elt is None for elt in result) is True:
            raise sppasIOError("None of the images could be generated.")

        return tuple(result)

    # -----------------------------------------------------------------------
    # PRIVATE WORKERS
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

    def _generate_coded_image(self, dirname: str, shape: str, position: str) -> str:
        """Generate a plain face image.

        :return: (str|None) filename.

        """
        _filename = os.path.join(dirname, "_".join((self._prefix, shape, position)) + ".jpg")
        
        # Do not generate the same image twice
        if os.path.exists(_filename):
            return _filename

        # Predict position of the vowel 
        target = self._model_pos.get_vowel_coords(position)

        # Predict the angle of the arm
        vowel_angle = self._model_angle.get_angle(position)

        # Estimate S0, S9 and target coordinates
        _model = sppasHandCoords(self._cs, self.__img_tagger)
        _label_coords = _model.eval_hand_points(target, [shape], vowel_angle, self._face_dist)

        # Overlay the hand on the face image
        _img_tag = self.__img_tagger.slap_on(self._img, [(shape, 1.)], _label_coords) 
        _img_tag.write(_filename)

        return _filename

    # -----------------------------------------------------------------------

    def __extract_image_sights(self) -> sppasSights:
        """Read the sights file and return the labels of the single annotation.

        :raises: sppasIOError: if the file does not contain exactly one tier with one annotation.
        :return: (sppasSights) Sights

        """
        # Read the sights file
        parser = sppasTrsRW(self._face_sight)
        trs = parser.read()
        # Validate structure: exactly one tier with one annotation expected
        if len(trs) != 1:
            raise sppasIOError(f"Expected only one tier in file {self._sights_filename}. "
                               f"Got {len(trs)} instead.")
        if len(trs[0]) != 1:
            raise sppasIOError(f"Expected only one annotation in file {self._sights_filename}. "
                               f"Got {len(trs[0])} instead.")

        # Convert labels into a sppasSights() instance
        labels = trs[0][0].get_labels()
        _s = sppasSights()
        for _i, label in enumerate(labels):
            tag = label.get_best()
            _x, _y = tag.get_typed_content().get_midpoint()
            _s.set_sight(_i, _x, _y)
    
        return _s

# ---------------------------------------------------------------------------

# Launch with: python -m sppas.ui.swapp.app_textcues.models.overlays_model
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

    model = PathwayCodeOverlayModel(cued_rules, prefix="yoyo")
    output_filenames = model.generate(cuedkeys, cuedphons)

    print(output_filenames)
