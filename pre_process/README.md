# Pre_process Module

Este módulo contiene los scripts y recursos necesarios para preprocesar datos de corpus y generar los archivos JSON requeridos por el corrector en el módulo **autocorrect**. En particular, se generan:

- **Modelos de n-gramas (bigramas):**  
  Archivos JSON que contienen la frecuencia de aparición de combinaciones de dos palabras extraídas de corpus de texto (por ejemplo, MarkDavies y Europarl).  
  _Importancia:_ El archivo JSON generado se utiliza en en la clase Speller de **autocorrect** para evaluar el contexto en la corrección de palabras.

- **Diccionarios de frecuencia:**  
  Archivos JSON que almacenan los recuentos (frecuencias absolutas y/o normalizadas) para cada forma ortográfica.  
  Se generaron dos diccionarios para pruebas, el primero utiliza el diccionario generado a partir de datos de _CREA (RAE)_ y, para el segundo se genera a partir del _corpus Europarl_.

## Estructura de archivos (dentro de pre_process)

```bash
pre_process/
├── extract.py # Script original de extracción de frecuencias (p.ej., para CESS-ESP).
├── generate_ngram_markdavies.py # Genera JSON de bigramas para el corpus MarkDavies (archivo .txt).
├── generate_ngram_europarl.py # Genera JSON de bigramas para el corpus Europarl (archivo .txt).
├── generate_frequency_crea.py # Procesa el diccionario de frecuencias CREA (RAE) en formato .txt y genera un JSON.
├── generate_frequency_europarl.py # Genera el diccionario de frecuencias a partir del corpus Europarl.
├── README.md # Este documento.
└── requeriments.txt # Dependencias necesarias para el preprocesamiento (incluye nltk, etc.).
```

## Archivos nuevos y su propósito

1. **`Clase Speller` (en el paquete `autocorrect/autocorrect`):**

   - Se ha modificado para incorporar la evaluación de contexto en la corrección de palabras.
   - Ahora utiliza un archivo JSON con bigramas para calcular un score de contexto que se combina con la frecuencia de la palabra.
   - _Requisito:_ Debe contar con un archivo JSON de bigramas generado (por ejemplo, `corpus/markdavies_bigram_model.json` o `corpus/europarl_bigram_model.json`).

2. **Scripts para la generación de modelos y diccionarios:**
   - **Generación de n-gramas:**
     - `generate_ngram_markdavies.py`: Procesa un archivo .txt proveniente del corpus MarkDavies, limpiando el contenido y extrayendo bigramas; exporta el resultado a JSON.
     - `generate_ngram_europarl.py`: Realiza la generación de bigramas a partir del corpus Europarl, separando el texto en párrafos y generando el modelo JSON.
   - **Generación de diccionarios de frecuencia:**
     - `generate_frequency_crea.py`: Procesa un archivo .txt (formateado con columnas para orden, palabra, frecuencia absoluta y normalizada) proveniente de CREA (RAE) y genera un JSON con las formas ortográficas y sus frecuencias.
     - `generate_frequency_europarl.py`: Extrae y cuenta las palabras del corpus Europarl, generando un diccionario de frecuencia en JSON.

## Cómo utilizar los scripts

1. **Instalar Dependencias:**  
   Asegúrate de tener instaladas las dependencias listadas en `requeriments.txt`. Por ejemplo:
   ```bash
   pip install -r requeriments.txt
   ```

Entre las dependencias se incluye nltk y otros módulos requeridos.

2. **Generar el modelo de n-gramas:** Para generar el archivo JSON de bigramas a partir del corpus MarkDavies:

```bash
python generate_ngram_markdavies.py
```

O para el corpus Europarl:

```bash
python generate_ngram_europarl.py
```

Los archivos se generarán en la carpeta **corpus/** (por ejemplo, markdavies_bigram_model.json o europarl_bigram_model.json).

3. **Generar el diccionario de frecuencia**: Para el diccionario basado en CREA:

```bash
python generate_frequency_crea.py
```

O para el corpus Europarl:

```bash
python generate_frequency_europarl.py
```

Los archivos resultantes (por ejemplo, crea_frequency_dict.json y europarl_frequency_dict.json) se ubicarán en la carpeta **corpus/**.

## Datos de entrada

- **Datos de texto plano**: Los corpus y diccionarios se obtuvieron a partir de fuentes de datos en formato .txt:

  - **MarkDavies Corpus**: Contiene entradas estructuradas con un ID y el texto correspondiente.

  - **Europarl Corpus**: Archivo de texto plano con discursos parlamentarios.

  - **CREA Diccionario de Frecuencia (RAE)**: Archivo de texto con columnas para orden, palabra y frecuencias.

Es importante asegurarse de que el formato de estos archivos sea consistente con lo que esperan los scripts de generación.

### Diferencias entre par 1 y par 2

- **Par 1:**

  - **Corpus para n-gramas:**  
    Utiliza el **MarkDavies Corpus**. Este conjunto de datos, en formato de texto plano, recopila textos que suelen tener un estilo más variado e incluso periodístico, lo que puede reflejar el uso cotidiano del idioma.
  - **Diccionario de frecuencia:**  
    Emplea el diccionario de frecuencias del **CREA (RAE)**, que contiene información detallada sobre la frecuencia de uso de formas ortográficas ampliamente aceptadas del español. Esto le brinda robustez y respaldo normativo en la corrección.

- **Par 2:**
  - **Corpus para n-gramas:**  
    Se basa en el **Europarl Corpus**, el cual contiene discursos parlamentarios y otros textos oficiales. Esto genera un modelo de n-gramas que enfatiza el uso formal del idioma y estructuras lingüísticas propias del ámbito político-institucional.
  - **Diccionario de frecuencia:**  
    Se genera un diccionario de frecuencias directamente a partir del Europarl Corpus, orientado al contexto formal de los discursos, lo que puede favorecer correcciones en textos escritos con estilo institucional.

Estos enfoques permiten comparar cómo se comporta el corrector en diferentes registros lingüísticos, siendo el Equipo 1 más representativo del uso general y cotidiano, mientras que el Equipo 2 se adapta a un estilo más formal.

Para ver mas diferencias acerca del corpus de MarkDavies con el corpus de la RAE
https://www.corpusdelespanol.org/web-dial/help/compare.asp

## Integración con el Corrector

Una vez generados los archivos JSON (bigramas y diccionarios de frecuencia), estos deben colocarse en la carpeta corpus o en la ubicación configurada en el código del módulo autocorrect. La **clase Speller** en autocorrect se encargará de cargar estos modelos y utilizarlos para evaluar y corregir palabras según su contexto.

## Referencias

- Europarl: A Parallel Corpus for Statistical Machine Translation, Philipp Koehn, MT Summit 2005, pdf.
- REAL ACADEMIA ESPAÑOLA: Banco de datos (CREA Anotado) [en línea]. Corpus de referencia del español actual (CREA). <http://www.rae.es> [10-may-2025]
