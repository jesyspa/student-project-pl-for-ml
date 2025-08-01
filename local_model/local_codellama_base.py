# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
def generator():
    tokenizer = AutoTokenizer.from_pretrained("codellama/CodeLlama-7b-Instruct-hf")
    model = AutoModelForCausalLM.from_pretrained(
        "codellama/CodeLlama-7b-Instruct-hf",
        torch_dtype=torch.float16,
        device_map="auto"
    )
    prompt = f"{input('You: ')}\n"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            do_sample=True,
            temperature=0.7,
            top_p=0.95,
            top_k=50,
            repetition_penalty=1.1,
            eos_token_id=tokenizer.eos_token_id
        )

    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text
if __name__ == "__main__":
    print(generator())