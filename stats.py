
import re

def contar_palabras(texto):
    """Cuenta todas las palabras en el texto usando una expresión regular."""
    # \w+ captura secuencias de caracteres alfanuméricos,
    # lo que en la práctica equivale a palabras.
    palabras = re.findall(r'\w+', texto, re.UNICODE)
    return len(palabras)

def contar_oraciones(texto):
    """Cuenta el número de oraciones en el texto.
       Separa usando signos de cierre de oración (punto, ?, !)."""
    # Dividimos por ".!?" y filtramos las cadenas vacías.
    oraciones = re.split(r'[.!?]+', texto)
    oraciones = [s for s in oraciones if s.strip() != '']
    return len(oraciones)

def contar_correcciones(original, corregido):
    """
    Compara palabra por palabra y cuenta las correcciones realizadas.
    Si los textos tienen distinta longitud, suma la diferencia.
    """
    orig_words = original.split()
    corr_words = corregido.split()
    
    # Contar diferencias en las posiciones comunes
    differences = sum(1 for o, c in zip(orig_words, corr_words) if o != c)
    # Sumar los restos si la longitud de las listas es distinta
    differences += abs(len(orig_words) - len(corr_words))
    return differences

def generar_estadisticas(original, corregido):
    """Genera un diccionario con estadísticas del proceso de corrección."""
    total_palabras = contar_palabras(original)
    total_oraciones = contar_oraciones(original)
    total_correcciones = contar_correcciones(original, corregido)
    total_no_correciones = total_palabras - total_correcciones
    porcentaje = (total_correcciones / total_palabras * 100) if total_palabras > 0 else 0


    return {
        'total_palabras': total_palabras,
        'total_oraciones': total_oraciones,
        'palabras_corregidas': total_correcciones,
        'palabras_no_corregidas': total_no_correciones,
        'porcentaje_cambiado': round(porcentaje, 2)
    }
