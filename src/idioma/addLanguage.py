import chardet
import nltk
import spacy
from nltk.corpus import wordnet

from src.database import existRegistroIngles, inserirRegistroPortugues, inserirRegistroIngles, existRegistroPortugues

nltk.download('wordnet')

nlpPT = spacy.load("pt_core_news_sm")
nlpEN = spacy.load("en_core_web_sm")


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read()
        result = chardet.detect(rawdata)
    return result['encoding']


def get_synonyms_antonyms(word):
    synonyms = []
    antonyms = []

    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
            if lemma.antonyms():
                antonyms.append(lemma.antonyms()[0].name())

    return set(synonyms), set(antonyms)


def process_file(file_path, nlp, exist_function, insert_function):
    encoding = detect_encoding(file_path)
    with open(file_path, 'r', encoding=encoding) as arquivo:
        text = arquivo.read().lower()  # Convertendo tudo para minúsculo
        doc = nlp(text)

        for token in doc:
            if token.is_alpha and token.text not in nlp.Defaults.stop_words:
                morf = token.tag_
                synonyms, antonyms = get_synonyms_antonyms(token.text)

                # Você pode adicionar sinônimos e antônimos ao banco de dados aqui
                # Exemplo: inserir_syn_ant(token.text, synonyms, antonyms)

                if not exist_function(token.text):
                    insert_function(token.text, 'palavra', 1, morf)
                    print(token.text)

        # Criando 2-gramas para contexto
        bigrams = [b for b in nltk.bigrams(text.split())]
        # Você pode armazenar bigrams no banco de dados para contexto.


def main():
    process_file('E:/OneDrive/Projeto/JarvesProcessamento/resources/br.txt', nlpPT, existRegistroPortugues,
                 inserirRegistroPortugues)
    process_file('E:/OneDrive/Projeto/JarvesProcessamento/resources/en.txt', nlpEN, existRegistroIngles,
                 inserirRegistroIngles)


if __name__ == "__main__":
    main()
