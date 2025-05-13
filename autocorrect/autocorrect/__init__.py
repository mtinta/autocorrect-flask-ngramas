import json
import os
import re
import sys
import tarfile
import textwrap
from contextlib import closing
from urllib.request import urlretrieve

from .constants import word_regexes, backup_urls, ipfs_gateways, ipfs_paths
from .typos import Word

PATH = os.path.abspath(os.path.dirname(__file__))


# credit: https://stackoverflow.com/questions/43370284
class ProgressBar:
    def __init__(self):
        self.old_percent = 0
        print("_" * 50)

    def download_progress_hook(self, count, blockSize, totalSize):
        percent = int(count * blockSize * 100 / totalSize)
        if percent >= 2 + self.old_percent:
            self.old_percent = percent
            # print(percent, '%')
            print(">", end="")
            sys.stdout.flush()
        if percent == 100:
            print("\ndone!")


def load_from_tar(lang, file_name="word_count.json"):
    archive_name = os.path.join(PATH, f"data/{lang}.tar.gz")

    if lang not in word_regexes:
        supported_langs = ", ".join(word_regexes.keys())
        raise NotImplementedError(
            textwrap.dedent(
                f"""
            language '{lang}' not supported
            supported languages: {supported_langs}
            you can easily add new languages by following instructions at
            https://github.com/fsondej/autocorrect/tree/master#adding-new-languages
            """
            )
        )

    if not os.path.isfile(archive_name):
        print("dictionary for this language not found, downloading...")
        urls = [
            gateway + path for gateway in ipfs_gateways for path in ipfs_paths[lang]
        ]
        if lang in backup_urls:
            urls += backup_urls[lang]
        for url in urls:
            progress = ProgressBar()
            try:
                urlretrieve(url, archive_name, progress.download_progress_hook)
                error_message = None
                break
            except Exception as ex:
                print(f"couldn't download {url}, trying next url...")
                error_message = str(ex)
        if error_message is not None:
            raise ConnectionError(
                error_message
                + "\nFix your network connection, or manually download \n{}"
                "\nand put it in \nPATH_TO_REPO/autocorrect/data/".format(url)
            )

    with closing(tarfile.open(archive_name, "r:gz")) as tarf:
        with closing(tarf.extractfile(file_name)) as file:
            return json.load(file)


class Speller:
    def __init__(
        self, lang="en", threshold=0, nlp_data=None, fast=False, only_replacements=False, ngram_data=None, context_threshold=5
    ):
        self.lang = lang
        self.threshold = threshold
        self.nlp_data = load_from_tar(lang) if nlp_data is None else nlp_data
        self.fast = fast
        self.only_replacements = only_replacements
        #nuevo para n-grams
        self.context_threshold = context_threshold


        if threshold > 0:
            # print(f'Original number of words: {len(self.nlp_data)}')
            self.nlp_data = {k: v for k, v in self.nlp_data.items() if v >= threshold}
            # print(f'After applying threshold: {len(self.nlp_data)}')

        if ngram_data is None:
            ngram_file = os.path.join(PATH, "bigram_model.json")
            with open(ngram_file, "r", encoding="utf-8") as f:
                self.ngram_model = json.load(f)
            print("Se importo con exito\n")
        else: 
            self.ngram_model = ngram_data

    def existing(self, words):
        """{'the', 'teh'} => {'the'}"""
        return {word for word in words if word in self.nlp_data}

    def get_candidates(self, word):
        w = Word(word, self.lang, self.only_replacements)
        #print(f"Palabra a buscar: {word}")
        if self.fast:
            candidates = self.existing([word]) or self.existing(w.typos()) or [word]
        else:
            candidates = (
                self.existing([word])
                or self.existing(w.typos())
                or self.existing(w.double_typos())
                or [word]
            )
        return [(self.nlp_data.get(c, 0), c) for c in candidates]

    def autocorrect_word(self, word):
        """most likely correction for everything up to a double typo"""
        if word == "":
            return ""

        candidates = self.get_candidates(word)

        # in case the word is capitalized
        if word[0].isupper():
            decapitalized = word[0].lower() + word[1:]
            candidates += self.get_candidates(decapitalized)

        best_word = max(candidates)[1]

        if word[0].isupper():
            best_word = best_word[0].upper() + best_word[1:]
        return best_word

    def autocorrect_sentence(self, sentence):
        return re.sub(
            word_regexes[self.lang],
            lambda match: self.autocorrect_word(match.group(0)),
            sentence,
        )
    
    @staticmethod
    def score_context(candidate, left_context, right_context, ngram_model):
        score = 0
        if left_context:
            bigram_left = f"{left_context[-1].lower()} {candidate.lower()}"
            score += ngram_model.get(bigram_left, 0)
        if right_context:
            bigram_right = f"{candidate.lower()} {right_context[0].lower()}"
            score += ngram_model.get(bigram_right, 0)
        return score
    
    def autocorrect_word_with_context(self, word, left_context, right_context):
        """
        Evalúa múltiples candidatos para una palabra basándose en su puntaje de contexto.
        Si alguno supera el umbral, se selecciona el de mayor puntaje.
        De lo contrario, se devuelve la palabra original.
        """
        if word == "":
            return ""
        # Obtiene la lista de candidatos junto con su frecuencia
        candidates = self.get_candidates(word)
        #print(candidates)
        # Si la palabra está capitalizada, agregar candidatos de su versión en minúsculas
        if word[0].isupper():
            decapitalized = word[0].lower() + word[1:]
            candidates += self.get_candidates(decapitalized)

        best_candidate = word
        best_score = 0

        # Evalúa cada candidato
        for freq, candidate in candidates:
            context_score = self.score_context(candidate, left_context, right_context, self.ngram_model)
            #print(f"Palabra: {candidate}, score={context_score}")
            if context_score > best_score:
                best_score = context_score
                best_candidate = candidate

        # Solo se retorna si se supera el umbral
        if best_score >= self.context_threshold:
            if word[0].isupper():
                best_candidate = best_candidate[0].upper() + best_candidate[1:]
            return best_candidate
        else:
            return word
    
    def autocorrect_sentence_with_context(self, sentence):
        tokens = sentence.split()
        corrected_tokens = tokens.copy()
        for i, word in enumerate(tokens):
            candidate = self.autocorrect_word(word)
            if candidate != word:
                # Evaluar teniendo en cuenta los bordes
                left_context = tokens[i-1:i] if i > 0 else []
                right_context = tokens[i+1:i+2] if i < len(tokens)-1 else []

                candidate = self.autocorrect_word_with_context(word, left_context, right_context)
                corrected_tokens[i] = candidate
                ''' 
                score_val = self.score_context(candidate, left_context, right_context, self.ngram_model)
                # Solo se aplica la corrección si el puntaje es suficientemente alto
                print(f"Palabra: {candidate}, score={score_val}")
                if score_val >= self.context_threshold:
                    corrected_tokens[i] = candidate
                '''
        return " ".join(corrected_tokens)

    __call__ = autocorrect_sentence


# for backward compatibility
class LazySpeller:
    def __init__(self):
        self.speller = None

    def __call__(self, sentence):
        print(
            "autocorrect.spell is deprecated, \
            use autocorrect.Speller instead"
        )
        if self.speller is None:
            self.speller = Speller()
        return self.speller(sentence)


spell = LazySpeller()
