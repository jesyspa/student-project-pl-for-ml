import os
import torch
from transformers import (
    AutoTokenizer, AutoModelForCausalLM,
    Trainer, TrainingArguments, DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, TaskType
from datasets import Dataset, DatasetDict


data_dir = os.path.join(os.path.dirname(__file__), "..", "dataset_generator", "dataset")
files = sorted([os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".txt")])

texts = []
for f in files:
    with open(f, "r", encoding="utf-8") as infile:
        content = infile.read().strip()
        if content:
            texts.append({"text": content})


# split 9 train 1 validation
split_idx = int(0.9 * len(texts))
train_texts = texts[:split_idx]
val_texts = texts[split_idx:]

dataset = DatasetDict({
    "train": Dataset.from_list(train_texts),
    "validation": Dataset.from_list(val_texts)
})

model_name = "codellama/CodeLlama-7b-Instruct-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype=torch.float16,
    load_in_8bit=True
)

lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"]
)
model = get_peft_model(model, lora_config)

def tokenize(batch):
    return tokenizer(batch["text"], truncation=True, max_length=512)

dataset = dataset.map(tokenize, batched=True)
dataset.set_format(type="torch", columns=["input_ids", "attention_mask"])

data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)

training_args = TrainingArguments(
    output_dir="./code_lora",
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    gradient_accumulation_steps=8,
    num_train_epochs=3,
    learning_rate=3e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch",
    save_total_limit=2,
    report_to="none",
    load_best_model_at_end=False
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["validation"],
    tokenizer=tokenizer,
    data_collator=data_collator
)

trainer.train()
