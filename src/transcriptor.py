import gc

import torch
import whisperx


class Transcriptor:

    def __init__(self, model_name="medium", device=None, batch_size=8):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model_name = model_name
        self.batch_size = batch_size

        if self.device == "cuda":
            self.compute_type = "float16"
        else:
            self.compute_type = "int8"

        print(f"Cargando modelo WhisperX '{self.model_name}' en {self.device} con {self.compute_type}...")

        self.model = whisperx.load_model(
            self.model_name,
            self.device,
            compute_type=self.compute_type,
            language="es"
        )

        print("Modelo cargado correctamente.\n")

    def transcribir(self, archivo_audio):

        print("Cargando audio...")

        audio = whisperx.load_audio(archivo_audio)

        print("Transcribiendo...")

        resultado = self.model.transcribe(
            audio,
            batch_size=self.batch_size
        )

        print("Transcripción terminada.\n")

        return resultado

    def liberar_memoria(self):
        del self.model
        gc.collect()

        if self.device == "cuda" and torch.cuda.is_available():
            torch.cuda.empty_cache()