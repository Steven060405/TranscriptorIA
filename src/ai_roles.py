import torch
from transformers import pipeline


class AsignadorRoles:
    def __init__(self, model_name="google/flan-t5-small"):
        self.device = 0 if torch.cuda.is_available() and torch.cuda.device_count() > 0 else -1
        self.model_name = model_name
        print(f"Cargando modelo de clasificación de roles '{self.model_name}' en {'GPU' if self.device == 0 else 'CPU'}...")
        self.classificador = pipeline(
            "text2text-generation",
            model=self.model_name,
            device=self.device,
            max_length=64,
        )
        print("Modelo de clasificación de roles cargado correctamente.\n")

    def _normalize_output(self, generated_text: str) -> str:
        text = generated_text.strip().lower()
        if "entrevistador" in text:
            return "Entrevistador"
        if "entrevistado" in text:
            return "Entrevistado"
        return "Entrevistado"

    def _prepare_prompt(self, speaker_text: str) -> str:
        speaker_text = speaker_text.replace("\n", " ").strip()
        if len(speaker_text) > 2000:
            speaker_text = speaker_text[:2000] + "..."

        prompt = (
            "Eres un asistente que identifica si un fragmento de una entrevista fue dicho "
            "por el entrevistador o por el entrevistado. "
            "Responde solo con una de estas dos palabras: Entrevistador o Entrevistado.\n\n"
            "Texto:\n" + speaker_text
        )
        return prompt

    def clasificar_hablantes(self, hablantes_texto: dict[str, str]) -> dict[str, str]:
        roles = {}

        for speaker_id, texto in hablantes_texto.items():
            prompt = self._prepare_prompt(texto)
            try:
                salida = self.classificador(prompt, max_new_tokens=20, do_sample=False)
                if salida and isinstance(salida, list):
                    roles[speaker_id] = self._normalize_output(salida[0].get("generated_text", ""))
                else:
                    roles[speaker_id] = "Entrevistado"
            except Exception:
                roles[speaker_id] = "Entrevistado"

        return roles
