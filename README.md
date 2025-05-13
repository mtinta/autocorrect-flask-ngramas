# Autocorrect + Flask

Implementacion de una aplicacion Flask que permite el ingreso de texto en un archivo con el extension apropiada. Se consigue que se corrijan faltas ortograficas en Español usando el corpus _cess_esp_.

Detecta y corrige errores de escritura. Esto suele implicar identificar palabras mal escritas, **compararlas con un corpus** de palabras correctas. Usando heuristica para la distancia de edicion y ofrece estadísticas detalladas sobre el contenido, tales como:

- Total de palabras y oraciones en el texto original.

- Cantidad y porcentaje de palabras corregidas.

- Visualización interactiva: Las palabras modificadas se resaltan (por ejemplo, en negrita), y el usuario puede activar o desactivar esta visualización mediante un checkbox.

La aplicación también permite descargar el texto corregido.

---

## Caracteristicas

- **Entrada flexible**: Permite escribir texto directamente o subir un archivo de texto.

- **Corrección personalizada**: Utiliza un diccionario de frecuencias basado en el corpus CESS-ESP para mejorar la precisión en español.

- **Estadísticas de corrección**: Muestra el total de palabras, oraciones, y las palabras modificadas así como el porcentaje de correlación.

- **Visualización interactiva**: Resalta las palabras corregidas y permite alternar dicha funcionalidad mediante un checkbox.

- **Descarga del resultado**: Genera un archivo de texto corregido para descargar de manera sencilla.

---

## Requisitos

- Python > 3.X
- Flask
- autocorrect (módulo con la clase Speller)
- nltk
- Otros módulos: json, io, difflib, etc.

## Instalacion

1. Clonar el repositorio

```bash
git clone https://github.com/fabrik12/autocorrect-Flask.git
cd autocorrector-flask
```

2. Crear y activar un entorno virtual:

```bash
python3 -m venv env
source env/bin/activate       # En Windows: env\Scripts\activate
```

3. Instalar dependencias

```bash
pip install -r requirements.txt
pip install -e autocorrect
```

---

## Uso

1. Ejecutar la aplicacion:

```bash
python app.py
```

2. Accede a la aplicación:
   Abre tu navegador y dirígete a http://127.0.0.1:5000.

3. Interacción:

- **Escribir texto**: Ingresa tu texto en el área de texto y envíalo para corregir.
- **Subir archivo**: Selecciona un archivo de texto, súbelo y envía para corregir.
- **Visualización de estadísticas**: Se mostrarán el total de palabras, oraciones, y las palabras modificadas (con su porcentaje respectivo).
- **Resaltado de correcciones**: Podrás ver en el texto corregido que las palabras modificadas aparecen en negrita; además, mediante un checkbox se puede mostrar u ocultar este resaltado.
- **Descarga**: Una vez corregido, podrás descargar el texto corregido como archivo .txt.

---

## Estructura del Proyecto

```bash
flask-autocorrect/
├── app.py                 # Archivo principal de Flask
├── autocorrect/           # Modulo con funciones de Speller
├── pre_process/           # Modulo con funciones para realizar diccionario de frecuencias desde CESS_ESP
├── corpus/
│   └── word_count.json    # Diccionario de frecuencias basado en CESS-ESP
├── static/
│   ├── css/
│   │   └── styles.css     # Archivo de estilos
│   └── js/
│       └── index.js       # Lógica de JavaScript para manejo de pestañas y resaltado
├── templates/
│   └── index.html         # Template principal de la aplicación
├── stats.py          # Módulo con funciones de estadísticas
├── detectChange.py          # Módulo con funciones de resaltado de texto
├── requirements.txt       # Lista de dependencias del proyecto
└── README.md              # Este archivo
```

---

## Mejoras Futuras

- **Historial de Correcciones**: Almacenar en sesión los textos corregidos para que el usuario pueda consultarlos.
- **Comparación visual lado a lado**: Mostrar el texto original junto al corregido resaltando las diferencias.
- **Feedback del usuario**: Permitir que el usuario marque correcciones erróneas para mejorar el modelo del corrector.
- **API REST**: Exponer algunos endpoints para que otros sistemas puedan acceder a la funcionalidad de corrección.
