import time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

base_model_name = "codellama/CodeLlama-7b-Instruct-hf"
finetuned_path = "./code_lora/checkpoint-1689"

tokenizer = AutoTokenizer.from_pretrained(base_model_name)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    llm_int8_enable_fp32_cpu_offload=True
)

def load_model(path):
    return AutoModelForCausalLM.from_pretrained(
        path,
        quantization_config=bnb_config,
        device_map="auto"
    )

base_model = load_model(base_model_name)
finetuned_model = load_model(finetuned_path)

prompt = "Write a program that prints a number 20 in my custom language"
inputs = tokenizer(prompt, return_tensors="pt").to(base_model.device)

def benchmark(model, inputs, n=5):
    with torch.no_grad():
        model.generate(**inputs, max_new_tokens=20)  # warmup
        start = time.time()
        for _ in range(n):
            model.generate(**inputs, max_new_tokens=20, do_sample=False)
        end = time.time()
    return (end - start) / n

def generate_answer(model, inputs):
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=50, do_sample=False)
    return tokenizer.decode(output[0], skip_special_tokens=True)

print("Base model avg time:", benchmark(base_model, inputs))
print("Finetuned model avg time:", benchmark(finetuned_model, inputs))
print("Base output:")
print(generate_answer(base_model, inputs))
print("Finetuned output:")
print(generate_answer(finetuned_model, inputs))
