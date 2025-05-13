from flask import Flask, render_template, request, send_file, redirect, url_for
from autocorrect.autocorrect import Speller
from io import BytesIO
import json
from stats import generar_estadisticas
from detectChange import highlight_correcciones

app = Flask(__name__)
spell = None

PATH_CORPUS_DEFAULT = "./corpus/word_count.json"
PATH_CREA_DICT = "./corpus/crea_frequency_dict.json"
PATH_MARKD_NGRAM = "./corpus/markdavies_bigram_model.json"
PATH_EURO_DICT = "./corpus/europarl_frequency_dict.json"
PATH_EURO_NGRAM = "./corpus/europarl_bigram_model.json"


def create_speller(threshold, context_threshold, selected_dict, selected_ngram):
    # Mapea la selección del diccionario a su camino
    if selected_dict == "CREA":
        dict_path = PATH_CREA_DICT
    elif selected_dict == "EURO":
        dict_path = PATH_EURO_DICT
    else:
        dict_path = PATH_CORPUS_DEFAULT  # Default

    # Mapea la selección de bigramas a su camino
    if selected_ngram == "MarkDavies":
        ngram_path = PATH_MARKD_NGRAM
    elif selected_ngram == "Europarl":
        ngram_path = PATH_EURO_NGRAM
    else:
        ngram_path = None  # Default (bi gram CESS_SPA)

    # Cargar el diccionario de frecuencias (nlp_data)
    with open(dict_path, 'r', encoding='utf-8') as f:
        nlp_data = json.load(f)

    # Cargar el modelo de bigramas (ngram_data)
    with open(ngram_path, 'r', encoding='utf-8') as f:
        ngram_data = json.load(f)

    # Crear la instancia de Speller pasando los parámetros personalizados
    speller = Speller(
        lang="es",
        threshold=threshold,
        context_threshold=context_threshold,
        nlp_data=nlp_data,
        ngram_data=ngram_data
    )
    return speller

def validateForm(form, files):
    result = {}
    input_type = form.get('input_type')
    if input_type not in ['text', 'file']:
        raise ValueError("Tipo de entrada desconocido.")
    result['input_type'] = input_type

    if input_type == 'text':
        texto = form.get('texto', '').strip()
        if not texto:
            raise ValueError("Debe ingresar un texto.")
        result['texto'] = texto
    elif input_type == 'file':
        archivo = files.get('archivo')
        if not archivo or archivo.filename == '':
            raise ValueError("Debe subir un archivo.")
        result['texto'] = archivo.read().decode('utf-8')

    try:
        result['context_threshold'] = int(form.get('context_threshold', 4))
        result['threshold'] = int(form.get('threshold', 10))
    except ValueError:
        raise ValueError("Error en los parámetros numéricos.")

    selected_dictionary = form.get('selected_dictionary')
    if selected_dictionary not in ['CREA', 'EURO']:
        raise ValueError("Diccionario seleccionado inválido.")
    result['selected_dictionary'] = selected_dictionary

    selected_bigram = form.get('selected_bigram')
    if selected_bigram not in ['MarkDavies', 'Europarl']:
        raise ValueError("Modelo de bigramas seleccionado inválido.")
    result['selected_bigram'] = selected_bigram

    return result


@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html', texto_original = '', texto_corregido = '', error = '')

@app.route('/procesar', methods = ['POST'])
def procesar():
    try:
        data = validateForm(request.form, request.files)
        texto_original = data['texto']

        # Crear la instancia de Speller con los parámetros elegidos por el usuario
        spell = create_speller(
            threshold=data['threshold'],
            context_threshold=data['context_threshold'],
            selected_dict=data['selected_dictionary'],
            selected_ngram=data['selected_bigram']
        )

        texto_corregido = spell.autocorrect_sentence_with_context(texto_original)
        stats_data = generar_estadisticas(texto_original, texto_corregido)
        texto_corregido_resaltado = highlight_correcciones(texto_original, texto_corregido)
    except Exception as e:
        return render_template('index.html', 
                               texto_original='', 
                               texto_corregido='', 
                               error=str(e), 
                               stats=None)

    return render_template('index.html', 
                           texto_original = texto_original, 
                           texto_corregido = texto_corregido, 
                           texto_corregido_resaltado = texto_corregido_resaltado, 
                           error = '', stats=stats_data)

@app.route('/descargar', methods = ['POST'])
def descargar():
    texto_corregido = request.form.get('texto_corregido')
    buffer = BytesIO()
    buffer.write(texto_corregido.encode('utf-8'))
    buffer.seek(0)
    return send_file(buffer, as_attachment = True, download_name = 'texto_corregido.txt', mimetype = 'text/plain')

def corregir_texto(texto):
    return spell(texto)


if __name__ == '__main__':
    app.run(debug = True)
