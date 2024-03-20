from transformers import GPT2Tokenizer, GPT2LMHeadModel, TextDataset, DataCollatorForLanguageModeling, Trainer, \
    TrainingArguments
import os


def load_dataset(train_path, test_path, tokenizer):
    """
    Loads the train and test datasets.

    Parameters:
    - train_path: Path to the training data file.
    - test_path: Path to the test data file.
    - tokenizer: Tokenizer to use for encoding the texts.

    Returns:
    - train_dataset, test_dataset
    """
    train_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=train_path,
        block_size=128)

    test_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=test_path,
        block_size=128)

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False,
    )

    return train_dataset, test_dataset, data_collator


def train_gpt_model(train_dataset, test_dataset, data_collator):
    """
    Trains the GPT model.

    Parameters:
    - train_dataset: Training dataset.
    - test_dataset: Test dataset.
    - data_collator: Data collator.
    """
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    training_args = TrainingArguments(
        output_dir="./results",  # output directory for model checkpoints
        overwrite_output_dir=True,  # overwrite the content of the output directory
        num_train_epochs=3,  # number of training epochs
        per_device_train_batch_size=4,  # batch size for training
        per_device_eval_batch_size=4,  # batch size for evaluation
        eval_steps=400,  # number of evaluation steps
        save_steps=800,  # after # steps model is saved
        warmup_steps=500,  # number of warmup steps for learning rate scheduler
        evaluation_strategy="steps",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
    )

    trainer.train()
    model.save_pretrained("./trained_model")
    tokenizer.save_pretrained("./trained_model")


if __name__ == "__main__":
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    train_path = 'path_to_your_train_file.txt'
    test_path = 'path_to_your_test_file.txt'
    train_dataset, test_dataset, data_collator = load_dataset(train_path, test_path, tokenizer)
    train_gpt_model(train_dataset, test_dataset, data_collator)
    print("Model training completed.")
