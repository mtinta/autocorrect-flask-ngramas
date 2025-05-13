# Autocorrect Module

El módulo **autocorrect** es una herramienta de corrección ortográfica que ha evolucionado para incorporar el análisis del contexto en la determinación de correcciones. En esta versión se han modificado algunas partes clave de `__init__.py` para utilizar un modelo de n-gramas y un diccionario de frecuencia, combinando ambas señales en un score que permite una corrección más precisa y sensible al estilo y entorno de las palabras en el texto.

## Características Principales

- **Corrección basada en typos:**  
  Se mantienen las técnicas tradicionales de corrección que generan candidatos a partir de errores de tipo (_typos_) mediante eliminaciones, transposiciones, reemplazos e inserciones.

- **Evaluación de Contexto:**  
  Gracias a la incorporación de un modelo de n-gramas (bigramas) cargado desde un archivo JSON, el sistema analiza el contexto (la palabra previa y la siguiente) para asignar un score a cada candidato utilizando frecuencias extraídas de un corpus.

- **Cálculo de Score Combinado:**  
  Se implementan métodos que combinan:

  - La frecuencia del candidato (obtenida del diccionario de frecuencia).
  - El score de contexto (obtenido de los n-gramas).  
    Estas señales podrian combinarse de diversas formas (mediante combinación lineal, multiplicativa, media armónica, entre otras) para decidir si se aplica la corrección.

- **Soporte para Datos Externos:**  
  El módulo trabaja en conjunto con archivos JSON generados anteriormente (por ejemplo, en la carpeta `corpus`), con modelos de bigramas y diccionarios de frecuencia que pueden provenir de distintas fuentes (como MarkDavies, Europarl, CREA, etc.).

## Estructura Interna

La estructura del módulo **autocorrect** se organiza en varios ficheros:

```bash
autocorrect/
├── autocorrect/
│ ├── init.py # Núcleo de la funcionalidad. Ahora incorpora la evaluación del contexto.
│ ├── constants.py # Constantes y expresiones regulares para tokenización.
│ ├── typos.py # Genera candidatos a partir de errores tipográficos.
│ └── word_count.py # Funciones auxiliares para el manejo del diccionario de frecuencia. (default)
├── PKG-INFO
└── setup.py
```

### Cambios en `__init__.py`

- **Carga del Modelo de N-gramas:**  
  `__init__.py` se ha actualizado para cargar un archivo JSON con bigramas (por ejemplo, ubicado en `corpus/bigram_model.json`). Esto permite evaluar el contexto en que aparece cada palabra candidata.

- **Nuevas Funciones de Corrección Contextual:**  
  Se han añadido métodos como `autocorrect_word_with_context` y `autocorrect_sentence_with_context` para analizar y comparar múltiples candidatos utilizando:

  - El score obtenido del contexto.
  - La frecuencia de la palabra extraída del diccionario.
  - Una función de combinación (como la suma ponderada, o mediante combinaciones multiplicativas o armónicas, según la experimentación).

- **Normalización y Ajuste de Parámetros:**  
  Se normalizan tanto las frecuencias como el score de contexto para que ambos tengan una escala comparable (por ejemplo, valores entre 0 y 1). Los parámetros como `context_threshold`, `alpha` y `beta` se pueden ajustar para calibrar la sensibilidad del corrector.

## Uso e Integración

1. **Requisitos:**  
   Este módulo requiere que los archivos JSON con los modelos de bigramas y diccionarios de frecuencia estén disponibles (por defecto, se espera que se encuentren en la carpeta `corpus`). Estos archivos son generados mediante los scripts ubicados en el módulo `pre_process`.

2. **Corrección Básica:**  
    El método por defecto, accesible usando el objeto del módulo como función, aplica la corrección tradicional sin evaluación contextual:

   ```python
   from autocorrect import spell
   texto_corregido = spell("El rapído zorro marron salta sobre el perro perezoso.")
   Esto invoca el método autocorrect_sentence (antiguo).

   ```

3. **Corrección con Contexto:** Para aprovechar la nueva funcionalidad basada en contexto, se puede llamar específicamente al método:

```python
from autocorrect.autocorrect import Speller

speller = Speller(lang="es", context_threshold=4, <otro parametros como los .json>)
texto_corregido = speller.autocorrect_sentence_with_context("El rapído zorro marron salta sobre el perro perezoso.")
print(texto_corregido)

```

## Consideraciones Adicionales

- **Ajuste y Experimentación**: Se recomienda experimentar con distintos métodos y ajustar los umbrales (context_threshold) para optimizar la corrección según el corpus y el dominio del texto.

- **Extensibilidad**: El diseño modular permite integrar nuevos modelos (por ejemplo, trigramas o análisis más profundo del contexto) o incorporar diccionarios alternativos sin grandes cambios en la arquitectura.

- **Actualización de Datos**: Asegúrese de que los archivos de datos (**en la carpeta corpus**) estén actualizados y sean consistentes con la tokenización y normalización empleada en el módulo para obtener mejores resultados.

## Conclusión

La incorporación de análisis de contexto en autocorrect mejora la precisión de las correcciones al considerar no solo los errores tipográficos, sino también el entorno en el que se ubican las palabras. Esta integración permite que el corrector sea más sensible a estilos y registros específicos, ofreciendo correcciones adecuadas tanto en textos formales como informales.

Para mayor información, consulte la documentación en el módulo pre_process y los scripts asociados que generan los recursos de datos.

## Creditos

Spelling corrector in python. Currently supports English, Polish, Turkish, Russian, Ukrainian, Czech, Portuguese, Greek, Italian, Vietnamese, French and Spanish, but you can easily add new languages.

Based on: https://github.com/phatpiglet/autocorrect and Peter Norvig's spelling corrector.
