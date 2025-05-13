#!/usr/bin/env python
import json
import math
import re

def read_crea_frequency(filepath):
    frequency_dict = {}
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # Omitir la primera línea (encabezado) y posibles líneas vacías
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        # Si es que el separador es cualquier tabulador o múltiples espacios
        # El formato es: Orden, palabra, Frec.absoluta, Frec.normalizada
        # Intentar separar por tabulador si existiera
        parts = re.split(r'\t+', line)
        if len(parts) >= 3:
            word = parts[1].strip()
            # Remover comas o puntos de la frecuencia
            freq_str = parts[3].strip()
            freq_num = math.ceil(float(freq_str))
            frequency_dict[word.lower()] = freq_num
    return frequency_dict

def main():
    filepath = "extraccion/crea_frecuencias.txt"  # Ruta al archivo CREA
    freq_dict = read_crea_frequency(filepath)
    output_path = "corpus/crea_frequency_dict.json"
    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(freq_dict, outfile, indent=4, ensure_ascii=False)
    print(f"Diccionario de frecuencias CREA guardado en {output_path}")

if __name__ == '__main__':
    main()
