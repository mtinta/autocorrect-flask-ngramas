import nltk
from nltk.corpus import cess_esp # type: ignore
import re, json
from collections import Counter, OrderedDict
import argparse

# Principal function to process corpus and generate a JSON
def process_corpus(output_path):
    
    nltk.download('cess_esp')

    # Regular expresion for to extract spanish words
    word_regex = r"[A-Za-zÁáÉéÍíÓóÚúÜüÑñ]+"

    # Extract all documents from cess_esp and append to array by document
    # Each document has Strings array
    all_documents = []
    for file in cess_esp.fileids():
        text_split = cess_esp.words(file)
        all_documents.append(text_split)

    # Create array with all words, and filter with regex match
    set_words = []
    for doc in all_documents:
        for w in doc:
            w = w.lower() #Normalize word to lowercase
            #if not re.match(word_regex, w):
            match = re.fullmatch(word_regex, w)
            if match is not None: # Validate with regular expresion
                set_words.append(w)

    # Counting word frecuencies
    counts = Counter(set_words)

    counts_list = sorted(counts.items(), key=lambda i: i[1], reverse=True)
    ordered_counts = OrderedDict(counts_list)

    # Save the frenquency dictionary to a JSON file
    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(ordered_counts, outfile, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process corpus CESS-ESP and generate to a word frequency JSON file")
    parser.add_argument(
        "-o", "--output", 
        type=str, 
        required=False, 
        help="Output file path for the frequency JSON. Default: './cess_esp_word_count.json'"
    )
    args = parser.parse_args()

    output_path = args.output if args.output else "./cess_esp_word_count.json"

    # Execute principal function with path o default path
    process_corpus(output_path)