# Uso general

## Configuracion inicial

Corpus CESS_ESP:
[Enlace Oficial de nltk](https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/cess_esp.zip)

Instale `requeriments.txt` (ya sea en un entorno con venv o local)

```python
pip install -r requeriments.txt
```

El script automaticamente descargara este corpus, sin embargo para elegir donde descargar debe configurar la variable de entorno

Configurar Variable de entorno:
(Linux)

```sh
> export NLTK='<PATH>/nltk_data
```

Ejemplo:

```sh
> tree .
.
├── nltk_data
│   ├── cess_esp.zip
└── extract.py
```

> [!NOTE]
> Si usa Windows debe buscar en linea acerca de como usar las variables de entorno

El script usa argparse que permite al usuario especificar la ruta del archivo de salida mediante el parametro -o u --output (aunque este no es obligatorio)

```sh
> python3 extract.py -o /PATH/[name].json
```

El usuario puede especificar el nombre para el diccionario de frecuencias

Sin embargo, tambien puede usarlo sin el parametro y se guardara por defecto donde esta el script.

# ¿Cómo funciona?

## 1. Importaciones y Extracción de Documentos

El código comienza importando el corpus cess_esp de NLTK y otras utilidades:

```python
from nltk.corpus import cess_esp  # type: ignore
import re, json
from collections import Counter, OrderedDict
```

Luego, extrae las palabras de cada documento del corpus:

Después, se recorre todos los documentos usando `cess_esp.fileids()` y se va acumulando cada lista de palabras en el arreglo `all_documents`

```python
all_documents = []
for file in cess_esp.fileids():
    text_split = cess_esp.words(file)
    all_documents.append(text_split)

```

## 2. Definición de la Expresión Regular

Nos interesa filtrar las palabras en español.

```python
word_regex = r"[A-Za-zÁáÉéÍíÓóÚúÜüÑñ]+"
```

Esta expresion permite letras mayusculas y minnusculas

## 3. Filtrado y Normalización de Palabras

El siguiente fragmento recorre cada documento y cada palabra dentro de él, y verifica que la palabra coincida con la expresión regular:

```python
set_words = []
for doc in all_documents:
    for w in doc:
        w = w.lower()  # Normalizamos la palabra a minúsculas
        if re.fullmatch(word_regex, w):  # O re.match tambien seria valido
            set_words.append(w)
```

## 4. Conteo y Ordenación de las Palabras

Una vez obtenida la lista set_words, se aplica Counter para contar
las apariciones de cada palabra:

```python
counts = Counter(set_words)
```

Después, se ordenan las tuplas del contador de forma descendente (de mayor a menor frecuencia) y se crea un OrderedDict:

```python
counts_list = sorted(counts.items(), key=lambda i: i[1], reverse=True)
ordered_counts = OrderedDict(counts_list)
```

## 5. Exportación a un Archivo JSON

Finalmente, se guarda el diccionario ordenado en un archivo JSON:

```python
with open("cess_esp_word_count.json", "w", encoding="utf-8") as outfile:
    json.dump(ordered_counts, outfile, indent=4, ensure_ascii=False)
```

El parámetro `ensure_ascii=False` es importante para mantener correctamente los caracteres especiales en español (por ejemplo, á, ñ, etc.).

## Resumen

- **Objetivo del Script**: Extraer todas las palabras del corpus CESS‑ESP utilizando NLTK, normalizarlas (preferentemente a minúsculas), filtrar las que cumplan con la expresión regular definida y contar su frecuencia. El resultado se genera en un archivo JSON (cess_esp_word_count.json) con la estructura:

```json
{
    "de": 10286,
    "la": 6925,
    "el": 6013,
    "que": 5570,
    ...
}
```

- **Uso en el Corrector**: Este JSON se puede usar en el corrector pasando el diccionario al parámetro nlp_data dentro de la clase Speller, lo cual **adaptará la corrección ortográfica a la frecuencia real del corpus CESS‑ESP**.
