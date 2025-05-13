#!/usr/bin/env python
import json
import re
from collections import Counter, OrderedDict

def process_europarl_frequency(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read().lower()
    # Usamos una expresión regular para extraer palabras (ajusta según necesidades)
    # Regular expresion for to extract spanish words
    word_regex = r"[A-Za-zÁáÉéÍíÓóÚúÜüÑñ]+"

    words = re.findall(word_regex, text)
    counts = Counter(words)
    ordered_counts = OrderedDict(sorted(counts.items(), key=lambda i: i[1], reverse=True))
    return ordered_counts

def main():
    filepath = "extraccion/europarl.txt"  # Utilizamos el archivo del Europarl corpus
    freq_dict = process_europarl_frequency(filepath)
    output_path = "corpus/europarl_frequency_dict.json"
    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(freq_dict, outfile, indent=4, ensure_ascii=False)
    print(f"Diccionario de frecuencias de Europarl guardado en {output_path}")

if __name__ == '__main__':
    main()
