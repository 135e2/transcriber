import whisperx
from .constants import Constants
import torch
import gc


class WhisperxModel:
    def __init__(self, model_name="large-v2", device="cuda"):
        self.model_name = model_name
        self.device = device
        try:
            self.__model = whisperx.load_model(
                model_name, device, compute_type=Constants.COMPUTE_TYPE
            )
        except ValueError:
            self.__model = whisperx.load_model(
                model_name, device, compute_type="int8"
            )

    def load_audio(self, filename):
        self.__audio = whisperx.load_audio(filename)

    def transcribe(self):
        return self.__model.transcribe(
            self.__audio, batch_size=Constants.BATCH
        )

    def cleanup(self):
        # delete model if low on GPU resources
        gc.collect()
        torch.cuda.empty_cache()
        del self.__model
