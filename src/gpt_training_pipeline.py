import fitz  # PyMuPDF
import os
import re
import unicodedata
import logging
from transformers import GPT2Tokenizer, GPT2LMHeadModel, TextDataset, DataCollatorForLanguageModeling, Trainer, \
    TrainingArguments
from accelerate import Accelerator, DataLoaderConfiguration

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GPTTrainerConfig:
    MODEL = "gpt2"
    BLOCK_SIZE = 128
    NUM_TRAIN_EPOCHS = 1
    PER_DEVICE_TRAIN_BATCH_SIZE = 4
    SAVE_STEPS = 10_000
    SAVE_TOTAL_LIMIT = 2


def extract_text_from_pdf(pdf_path):
    extracted_text = ''
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                extracted_text += page.get_text()
    except Exception as e:
        logging.error(f"Error extracting text from {pdf_path}: {str(e)}")
    return extracted_text


def normalize_text(text):
    text = text.lower()
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def preprocess_pdf_folder(folder_path, output_file):
    with open(output_file, 'w', encoding='utf-8') as f_out:
        for filename in os.listdir(folder_path):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(folder_path, filename)
                text = extract_text_from_pdf(pdf_path)
                text = normalize_text(text)
                f_out.write(text + "\n")
    logging.info(f"Preprocessed text saved to {output_file}")


def train_gpt_model(data_file, model_output_dir):
    tokenizer = GPT2Tokenizer.from_pretrained(GPTTrainerConfig.MODEL)
    tokenizer.pad_token = tokenizer.eos_token

    dataset = TextDataset(tokenizer=tokenizer, file_path=data_file, block_size=GPTTrainerConfig.BLOCK_SIZE)
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    model = GPT2LMHeadModel.from_pretrained(GPTTrainerConfig.MODEL)

    training_args = TrainingArguments(
        output_dir=model_output_dir,
        overwrite_output_dir=True,
        num_train_epochs=GPTTrainerConfig.NUM_TRAIN_EPOCHS,
        per_device_train_batch_size=GPTTrainerConfig.PER_DEVICE_TRAIN_BATCH_SIZE,
        save_steps=GPTTrainerConfig.SAVE_STEPS,
        save_total_limit=GPTTrainerConfig.SAVE_TOTAL_LIMIT,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset,
    )

    trainer.train()
    model.save_pretrained(model_output_dir)
    tokenizer.save_pretrained(model_output_dir)

    logging.info("Training complete. Model saved.")


if __name__ == "__main__":
    folder_path = r"D:\OneDrive\Projeto\PDF"
    preprocessed_file = "preprocessed_text.txt"
    model_output_dir = "D:/OneDrive/Projeto/gpt_model"

    preprocess_pdf_folder(folder_path, preprocessed_file)
    train_gpt_model(preprocessed_file, model_output_dir)
