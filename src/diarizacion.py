import os
from dotenv import load_dotenv
import whisperx


class Diarizador:

    def __init__(self):

        load_dotenv()

        token = os.getenv("HF_TOKEN")

        if token is None:
            raise Exception("No se encontró HF_TOKEN en el archivo .env")

        print("Cargando modelo de diarización...")

        self.pipeline = whisperx.diarize.DiarizationPipeline(
            token=token,
            device="cpu"
        )

        print("Modelo de diarización cargado.\n")

    def diarizar(self, audio):

        print("Detectando hablantes...")

        diarizacion = self.pipeline(audio)

        print("Diarización terminada.\n")

        return diarizacion