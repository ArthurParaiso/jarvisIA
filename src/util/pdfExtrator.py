import asyncio
import concurrent.futures
import logging
import os
import re

import fitz
import unicodedata
from langdetect import detect_langs, LangDetectException

from src.database import criar_tabela_registros, inserir_registro, existRegistroIngles

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def remove_accents(palavra):
    return ''.join(char for char in unicodedata.normalize('NFD', palavra) if unicodedata.category(char) != 'Mn')


def remover_numeros_e_caracteres_especiais(palavra):
    return re.sub(r'[^\w\s]', '', palavra)


def processar_pagina(page):
    text = page.get_text()
    text = remover_numeros_e_caracteres_especiais(text)
    words = re.findall(r'\b[^\d\W]+\b', text.lower())

    for word in words:
        if word:
            try:
                language_probs = detect_langs(word)

                ingles, portugues, espanhol = 0, 0, 0

                for lang_prob in language_probs:
                    if lang_prob.lang == "en":
                        ingles = word
                    elif lang_prob.lang == "pt":
                        portugues = word
                    elif lang_prob.lang == "es":
                        espanhol = word

                if not (ingles or portugues or espanhol):
                    continue

                inserir_registro(word, "palavra", ingles, portugues, espanhol)

            except LangDetectException as e:
                logging.warning(f'Erro na detecção da linguagem para a palavra "{word}": {e}')


def processar_pdf_paginas(executor, pdf_path):
    pdf_document = fitz.open(pdf_path)
    num_paginas = len(pdf_document)
    pdf_filename = os.path.basename(pdf_path)

    if not existRegistroIngles(pdf_filename):
        logging.info(f'Iniciando processamento das páginas do PDF "{pdf_path}"')
        for page_num in range(num_paginas):
            page = pdf_document[page_num]
            executor.submit(processar_pagina, page)
            logging.info(f'Processamento da página "{page_num + 1}" concluído.')
        inserir_registro(pdf_filename, 'pdf', 0, 0, 0)
        logging.info(f'Processamento das páginas do PDF "{pdf_path}" concluído. Páginas processadas: {num_paginas}.')
    else:
        logging.info(f'As páginas do PDF "{pdf_path}" já foram processadas anteriormente.')


async def main():
    pasta = 'E:\OneDrive\Projeto\PDF'

    logging.info('Iniciando o programa de processamento de PDFs')
    criar_tabela_registros()
    logging.info('Tabela "registros" criada ou já existente.')

    pdf_files = [os.path.join(pasta, filename) for filename in os.listdir(pasta) if filename.endswith('.pdf')]

    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
        for pdf_file in pdf_files:
            processar_pdf_paginas(executor, pdf_file)


if __name__ == "__main__":
    asyncio.run(main())
