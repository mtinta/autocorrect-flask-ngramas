from difflib import SequenceMatcher

def highlight_correcciones(original, corregido):
    """
    Compara el texto original y el corregido palabra por palabra,
    envolviendo en un span (con clase 'corrected-word') aquellas palabras
    que fueron modificadas.
    """
    orig_words = original.split()
    corr_words = corregido.split()
    matcher = SequenceMatcher(None, orig_words, corr_words)
    resultado = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        # Si no hubo cambio, agregamos las palabras tal como están
        if tag == "equal":
            resultado.extend(corr_words[j1:j2])
        # Si se trata de reemplazo o inserción, marcamos las palabras
        elif tag in ("replace", "insert"):
            for word in corr_words[j1:j2]:
                resultado.append(f"<span class='corrected-word'>{word}</span>")
        # Las eliminaciones no se muestran en el texto corregido
        elif tag == "delete":
            pass
    return " ".join(resultado)
