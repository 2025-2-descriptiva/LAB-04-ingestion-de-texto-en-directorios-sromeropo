# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""
import os
import glob
import pandas as pd
from typing import List, Dict

def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```


    """
    # --- Definición de Rutas ---
    ROOT_DIR = "."
    
    # ⭐ CORRECCIÓN CLAVE: La carpeta de entrada es 'files/input'
    FILES_DIR = os.path.join(ROOT_DIR, "files")
    INPUT_DIR = os.path.join(FILES_DIR, "input")
    
    # La carpeta de salida es 'files/output'
    OUTPUT_DIR = os.path.join(FILES_DIR, "output") 
    
    # 1. Asegurar que la carpeta de salida exista
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    def _process_directory(data_type: str) -> pd.DataFrame:
        """
        Función auxiliar para procesar recursivamente los archivos .txt 
        dentro de 'files/input/{data_type}/'.
        """
        dataset: List[Dict[str, str]] = []
        base_path = os.path.join(INPUT_DIR, data_type) # e.g., 'files/input/train'
        
        # Patrón de búsqueda recursiva: **/*.txt busca cualquier subcarpeta y archivos .txt.
        search_pattern = os.path.join(base_path, "**", "*.txt")
        file_paths = glob.glob(search_pattern, recursive=True)

        if not file_paths:
            # Esta alerta ayuda a confirmar que la ruta sigue siendo el problema si falla de nuevo
            print(f"⚠️ Alerta: No se encontraron archivos en el patrón: {search_pattern}")

        for file_path in file_paths:
            # El target es el nombre del directorio padre ('negative', 'neutral', 'positive')
            target = os.path.basename(os.path.dirname(file_path))

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    phrase = f.read().strip()
            except IOError:
                phrase = ""
            
            # Construir el registro
            dataset.append({
                "phrase": phrase,
                "target": target, 
            })
            
        return pd.DataFrame(dataset)

    # 2. Procesar los datasets de entrenamiento y prueba
    df_train = _process_directory("train")
    df_test = _process_directory("test")

    # 3. Guardar los DataFrames en la carpeta 'files/output/'
    train_output_path = os.path.join(OUTPUT_DIR, "train_dataset.csv")
    test_output_path = os.path.join(OUTPUT_DIR, "test_dataset.csv")

    # Guardar sin el índice de Pandas
    df_train.to_csv(train_output_path, index=False)
    df_test.to_csv(test_output_path, index=False)

    return df_train, df_test

pregunta_01()