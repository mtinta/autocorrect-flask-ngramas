#!/usr/bin/env python
from collections import Counter
import json
import re
from nltk import ngrams

debug = False

def read_europarl(filepath):

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read().lower()
    # Usamos una expresión regular para extraer palabras (ajusta según necesidades)
    # Regular expresion for to extract spanish words
    word_regex = r"[A-Za-zÁáÉéÍíÓóÚúÜüÑñ]+"

    words = re.findall(word_regex, text)
    if debug:
        print(words[:20])
        return
    return words

def generate_ngram_model(tokens, n=2):
    all_ngrams = []
    all_ngrams.extend(list(ngrams(tokens, n)))
    return Counter(all_ngrams)

def main():
    filepath = "extraccion/europarl.txt"  # Ajusta la ruta
    words = read_europarl(filepath)
    if not(debug):
        ngram_counter = generate_ngram_model(words, n=2)
        model_serializable = {" ".join(k): v for k, v in ngram_counter.items()}
        output_path = "corpus/europarl_bigram_model.json"
        with open(output_path, "w", encoding="utf-8") as outfile:
            json.dump(model_serializable, outfile, indent=4, ensure_ascii=False)
        print(f"Modelo de bigramas de Europarl guardado en {output_path}")

if __name__ == '__main__':
    main()
