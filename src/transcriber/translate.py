import dl_translate as dlt
from .constants import Constants


class DltModel:
    def __init__(self, src, dst, device="cuda"):
        self.__model = dlt.TranslationModel("nllb200", device=device)
        self.src = Constants.LANGUAGES[src]
        self.dst = Constants.LANGUAGES[dst]

    def translate(self, txt):
        return self.__model.translate(txt, self.src, self.dst)
