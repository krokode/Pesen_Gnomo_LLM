import os
import glob
from transformers import GPT2LMHeadModel, GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments

def load_dataset(train_path, test_path, tokenizer):
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

def train(train_file_path, model_name, 
        output_dir, overwrite_output_dir, 
        per_device_train_batch_size, 
        num_train_epochs, save_steps):
    """
    Train a GPT-2 model on a dataset of text files.
    """
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)
    
    # For simplicity, using the same file for train and test (or split if needed, but for now just train)
    # Actually TextDataset splits by block_size.
    
    train_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=train_file_path,
        block_size=128)
    
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False,
    )

    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=overwrite_output_dir,
        per_device_train_batch_size=per_device_train_batch_size,
        num_train_epochs=num_train_epochs,
        save_steps=save_steps,
        logging_steps=100,
        prediction_loss_only=True,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
    )

    trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)

def create_full_train_data(files, output_file):
    """
    Create a full train data file from a list of text files.
    """
    full_text = ""
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            full_text += f.read() + "\n"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_text)

if __name__ == "__main__":

    # Prepare data
    # We will combine all text files into one for training
    # gnomo_files = glob.glob("data/txt_gnomo/*.txt")
    pesen_files = glob.glob("data/txt_pesen/*.txt")

    create_full_train_data(pesen_files, "full_train_data.txt")
    
    train(
        train_file_path='full_train_data.txt',
        model_name='sberbank-ai/rugpt3small_based_on_gpt2',
        output_dir='output/model',
        overwrite_output_dir=True,
        per_device_train_batch_size=8,
        num_train_epochs=3,
        save_steps=500
    )
