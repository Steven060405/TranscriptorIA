import whisperx


class Formateador:

    def __init__(self):
        pass

    def unir(self, resultado_whisper, diarizacion):

        print("\nUniendo transcripción con hablantes...\n")

        resultado = whisperx.assign_word_speakers(
            diarizacion,
            resultado_whisper
        )

        return resultado

    def agrupar(self, resultado):

        conversacion = []

        speaker_actual = None
        texto_actual = ""

        for segmento in resultado["segments"]:

            speaker = segmento.get("speaker", "SPEAKER_00")
            texto = segmento["text"].strip()

            if speaker == speaker_actual:

                texto_actual += " " + texto

            else:

                if speaker_actual is not None:

                    conversacion.append({
                        "speaker": speaker_actual,
                        "texto": texto_actual.strip()
                    })

                speaker_actual = speaker
                texto_actual = texto

        if speaker_actual is not None:

            conversacion.append({
                "speaker": speaker_actual,
                "texto": texto_actual.strip()
            })

        return conversacion

    def imprimir(self, conversacion):

        print("\n" + "=" * 70)
        print("ENTREVISTA")
        print("=" * 70)

        for bloque in conversacion:

            speaker = bloque.get("speaker", "SPEAKER_00")
            numero = 1

            if isinstance(speaker, str):
                if speaker.startswith("SPEAKER_0"):
                    try:
                        numero = int(speaker.replace("SPEAKER_0", "")) + 1
                    except ValueError:
                        numero = 1
                elif speaker.startswith("SPEAKER_"):
                    try:
                        numero = int(speaker.split("_")[-1]) + 1
                    except ValueError:
                        numero = 1

            print(f"\nPersona {numero}:")
            print(bloque.get("texto", ""))

        print("\n" + "=" * 70)