from formato import Formateador
from transcriptor import Transcriptor
from diarizacion import Diarizador
from exportador import Exportador

def main():

    archivo = "../audios/Voz 260711_133527 - 11.m4a"

    transcriptor = Transcriptor()

    resultado = transcriptor.transcribir(archivo)
    diarizador = Diarizador()

    diarizacion = diarizador.diarizar(archivo)
    
    formateador = Formateador()

    resultado = formateador.unir(
        resultado,
        diarizacion
    )
    conversacion = formateador.agrupar(resultado)
    transcriptor.liberar_memoria()
    
    exportador = Exportador()

    formateador.imprimir(conversacion)
    exportador.exportar_txt(conversacion)

    print("IDIOMA DETECTADO:")
    print(resultado["language"])

    print("=" * 70)

    print("\nTRANSCRIPCIÓN\n")

    for segmento in resultado["segments"]:

        print(segmento["text"])

    
    

if __name__ == "__main__":
    main()
