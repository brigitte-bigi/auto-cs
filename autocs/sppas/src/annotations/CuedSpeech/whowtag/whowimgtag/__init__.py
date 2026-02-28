from .gencoords import sppasHandCoords

from sppas.src.imgdata import sppasImageDataError
from sppas.core.config import cfg

if cfg.feature_installed("video") is True:
    from .imgpostag import sppasImageVowelPosTagger
    from .imghandtag import sppasImageHandTagger
else:

    class sppasImageVowelPosTagger(sppasImageDataError):
        pass

    class sppasImageHandTagger(sppasImageDataError):
        pass


__all__ = (
    "sppasHandCoords",
    "sppasImageVowelPosTagger",
    "sppasImageHandTagger"
)

