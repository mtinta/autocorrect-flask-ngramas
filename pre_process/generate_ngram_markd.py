#!/usr/bin/env python
from nltk import ngrams
from collections import Counter
import json
import re

debug = False

# Función para limpiar cada línea y obtener el texto
def extract_text_from_line(line):
    # Formato es: "ID[tab]texto"
    # Dividir por tabulacion
    parts = re.split(r'\t+', line.strip())
    if len(parts) >= 2:
        return parts[1]
    # Si no hay tabulador, intenta por espacios
    parts = line.strip().split()
    if len(parts) >= 2:
        return " ".join(parts[1:])
    return ""

def read_markdavies(filepath):
    texts = []
    with open(filepath, "r", encoding="utf-8") as f:
        # Omitir la primera línea (encabezado)
        next(f)
        for line in f:
            text = extract_text_from_line(line)
            #print(text[:20])
            if text:
                texts.append(text)
    return texts

def tokenizar(text):
    arr_tokens = []
    word_regex = r"[A-Za-zÁáÉéÍíÓóÚúÜüÑñ]+"
    for token in text:
        token = token.lower()
        match = re.fullmatch(word_regex, token)
        if match is not None:
            arr_tokens.append(token)
    return arr_tokens

def generate_ngram_model(texts, n=2):
    all_ngrams = []
    for text in texts:
        # Convertir a minúsculas y tokenizar
        tokens = tokenizar(text.split())
        all_ngrams.extend(list(ngrams(tokens, n)))
        if debug:
            break
    return Counter(all_ngrams)

def main():
    filepath = "extraccion/markdavies.txt"  # Ajusta la ruta según corresponda
    texts = read_markdavies(filepath)
    ngram_counter = generate_ngram_model(texts, n=2)  # Para bigramas, si deseas trigramas, cambia n=3

    if not(debug):
        # Convertir tuplas a string para que el JSON sea serializable
        model_serializable = {" ".join(k): v for k, v in ngram_counter.items()}
        output_path = "corpus/markdavies_bigram_model.json"
        with open(output_path, "w", encoding="utf-8") as outfile:
            json.dump(model_serializable, outfile, indent=4, ensure_ascii=False)
        print(f"Modelo de bigramas guardado en {output_path}")


if __name__ == '__main__':
    main()
