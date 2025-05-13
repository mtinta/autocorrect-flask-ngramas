# Autocorrect – Módulo Principal

Este directorio contiene el núcleo del módulo **autocorrect**, el cual provee funciones para detectar y corregir errores tipográficos en textos, considerando además el contexto en el que aparecen las palabras. El sistema integra tradicionalmente los métodos basados en manipulaciones de cadenas (typos) y ahora incorpora análisis de n-gramas y diccionarios de frecuencia para evaluar el contexto.

## Estructura del Módulo

- **`__init__.py`**  
  Contiene la clase principal `Speller`

  - **Nuevas funciones:**
    - `autocorrect_word_with_context`: Evalúa múltiples candidatos para una palabra considerando tanto su frecuencia en un diccionario como el score de contexto basado en bigramas.
    - `autocorrect_sentence_with_context`: Aplica la corrección contextual palabra por palabra en un texto.
    - Funciones auxiliares para la normalización y evaluacion de candidatos: `score_context`.

- **`constants.py`**  
  Define constantes y expresiones regulares para la tokenización y procesamiento de palabras, así como rutas y parámetros predeterminados.

- **`typos.py`**  
  Implementa la generación de candidatos a corrección a partir de una palabra dada.
  - Funciones principales:
    - Métodos para obtener todas las variaciones de la palabra (eliminaciones, transposiciones, reemplazos, inserciones y sus combinaciones dobles).
- **`word_count.py`**  
  Provee utilidades para manejar y filtrar los diccionarios de frecuencia basados en datos preprocesados (por ejemplo, cargados desde los archivos .tar.gz o archivos JSON generados por el módulo `pre_process`).

## Funcionamiento Esencial

### Corrección Tradicional

- **`autocorrect_word`**  
  – Selecciona el candidato con la frecuencia máxima en el diccionario de frecuencias, utilizando los métodos de `typos()`.  
  – Conserva la lógica original para corregir palabras sin evaluar el contexto.

- **`autocorrect_sentence`**  
  – Usa expresiones regulares definidas en `constants.py` para localizar palabras en una oración y las corrige con `autocorrect_word`.

### Corrección Basada en Contexto (Nuevas Funciones)

- **Carga de Datos:**  
  – Al inicializar `Speller`, se carga un modelo de n-gramas desde un archivo JSON (por ejemplo, `corpus/bigram_model.json`), el cual contiene las frecuencias de bigramas extraídas mediante scripts del módulo **pre_process**.  
  – Se carga también el diccionario de frecuencia más amplio (por ejemplo, derivado de CREA o Europarl), que se utiliza para respaldar la corrección ortográfica.

- **Evaluación de Contexto:**  
  – **`score_context(candidate, left_context, right_context, ngram_model)`**:  
   Calcula un score sumando las frecuencias de los bigramas formados entre el candidato y las palabras adyacentes. Se asegura que tanto las palabras del contexto como el candidato sean procesados a minúsculas para mantener consistencia.

- **Corrección Contextual:**  
  – **`autocorrect_word_with_context(word, left_context, right_context)`**:  
   Recorre todos los candidatos generados (incluyendo variantes derivadas de `typos()` y `double_typos()`) y calcula el score combinado para cada uno. Retorna el candidato con el mejor score siempre que supere el umbral definido; en caso contrario, conserva la palabra original.
  – **`autocorrect_sentence_with_context(sentence)`**:  
   Divide el texto en tokens y aplica `autocorrect_word_with_context` a cada palabra, evaluando el contexto (palabra anterior y siguiente) de forma local.

## Parámetros Clave y Ajustes

- **`context_threshold`**:  
  Umbral mínimo que debe superar el score combinado para que se aplique una corrección. Este parámetro puede ajustarse según la sensibilidad deseada.

## Ejemplo de Uso

Para utilizar la corrección basada en contexto:

```python
from autocorrect.autocorrect import Speller

# Inicializar el corrector con parámetros para análisis del contexto.
speller = Speller(lang="es", context_threshold=0.5, <parametros adicionales como los archivos .json>)

texto = "El rapído zorro marron salta sobre el perro perezoso."
texto_corregido = speller.autocorrect_sentence_with_context(texto)
print(texto_corregido)
```

## Notas adicionales

- **Ajuste de Parámetros**: Los scripts y el módulo de corrección incorporan parámetros como context_threshold, u otros (dependiendo de la función que se podria implementar en el score). Se recomienda ajustar estos parámetros en función de pruebas reales y de la calidad de las correcciones obtenidas.

- **Pruebas**: Se recomienda utilizar textos de prueba para evaluar el desempeño de la corrección en diferentes escenarios (informal, formal, variado, etc.). Esto permitirá afinar tanto el preprocesamiento como la lógica de corrección.

- **Futuras Mejoras**: Se contempla la posibilidad de incorporar modelos de mayor orden (trigramas o 4-gramas) o técnicas de normalización adicionales para mejorar el score de contexto.

## Conclusión

La integración del análisis de contexto en autocorrect se realiza en el núcleo del módulo, mejorando la precisión de las correcciones al evaluar tanto la frecuencia global de las palabras como su adecuación en el entorno local. Este README detalla los puntos esenciales y debería servir de guía para desarrolladores que quieran extender o ajustar la funcionalidad (por ejemplo, probando combinaciones multiplicativas o media armónica para el score combinado).
