import torch
from transformers import pipeline


class AIResumidor:
    def __init__(self, model_name="mrm8488/bert2bert_shared-spanish-finetuned-summarization"):
        self.device = 0 if torch.cuda.is_available() and torch.cuda.device_count() > 0 else -1
        self.model_name = model_name
        print(f"Cargando modelo de resumen AI '{self.model_name}' en {'GPU' if self.device == 0 else 'CPU'}...")
        self.summarizer = pipeline(
            "summarization",
            model=self.model_name,
            device=self.device,
        )
        print("Modelo de resumen AI cargado correctamente.\n")

    def _chunk_text(self, text, max_chars=2800):
        sentences = [s.strip() for s in text.replace("\n", " ").split(". ") if s.strip()]
        chunks = []
        current = ""

        for sentence in sentences:
            sentence = sentence if sentence.endswith(".") else sentence + "."
            if current and len(current) + len(sentence) + 1 > max_chars:
                chunks.append(current.strip())
                current = sentence + " "
            else:
                current += sentence + " "

        if current.strip():
            chunks.append(current.strip())

        return chunks

    def resumir(self, text):
        text = text.strip()
        if not text:
            return ""

        chunks = self._chunk_text(text)
        summaries = []

        for chunk in chunks:
            result = self.summarizer(
                chunk,
                max_length=130,
                min_length=60,
                do_sample=False,
            )
            summaries.append(result[0]["summary_text"].strip())

        if len(summaries) == 1:
            return summaries[0]

        joined = " ".join(summaries)
        final = self.summarizer(
            joined,
            max_length=130,
            min_length=60,
            do_sample=False,
        )
        return final[0]["summary_text"].strip()
