from datetime import datetime
import os


class Exportador:

    def __init__(self):

        self.carpeta = "../salidas"

        if not os.path.exists(self.carpeta):
            os.makedirs(self.carpeta)

    def exportar_txt(self, conversacion):

        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")

        archivo = os.path.join(
            self.carpeta,
            f"Transcripcion_{fecha}.txt"
        )

        with open(archivo, "w", encoding="utf-8") as f:

            f.write("=" * 70 + "\n")
            f.write("ENTREVISTA\n")
            f.write("=" * 70 + "\n\n")

            for bloque in conversacion:

                numero = int(
                    bloque["speaker"].replace("SPEAKER_0", "")
                ) + 1

                f.write(f"Persona {numero}:\n")
                f.write(bloque["texto"] + "\n\n")

        print("\nArchivo TXT generado correctamente.")
        print(archivo)