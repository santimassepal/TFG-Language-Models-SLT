# -*- coding: utf-8 -*-
"""
Created on Fri May 19 23:10:57 2023

@author: Idener
"""

from transformers import BartTokenizer, BartForConditionalGeneration

model_name = 'facebook/bart-base'
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

with open('eng-slg.txt', 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()

source_texts, target_texts = [], []
for line in lines:
    source, target = line.split('@')
    source_texts.append(source.strip())
    target_texts.append(target.strip())
    
print(source_texts[0:10])
print(target_texts[0:10])

print("-----------------------------------")

input_encodings = tokenizer(source_texts, truncation=True, padding=True)
target_encodings = tokenizer(target_texts, truncation=True, padding=True)

import torch

class TranslationDataset(torch.utils.data.Dataset):
    def __init__(self, input_encodings, target_encodings):
        self.input_encodings = input_encodings
        self.target_encodings = target_encodings

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.input_encodings.items()}
        item['labels'] = torch.tensor(self.target_encodings['input_ids'][idx])
        return item

    def __len__(self):
        return len(self.input_encodings.input_ids)

dataset = TranslationDataset(input_encodings, target_encodings)

from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir='./results',          # output directory
    num_train_epochs=3,              # total number of training epochs
    per_device_train_batch_size=32,  # batch size per device during training
    warmup_steps=500,                # number of warmup steps for learning rate scheduler
    weight_decay=0.01,               # strength of weight decay
    logging_dir='./logs',            # directory for storing logs
)

trainer = Trainer(
    model=model,                         # the instantiated 🤗 Transformers model to be trained
    args=training_args,                  # training arguments, defined above
    train_dataset=dataset,               # training dataset
)

trainer.train()

model.save_pretrained('./my_bart_model')