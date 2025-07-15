# Local Setup and Fine-Tuning Base
This module sets up a local instance of the CodeLlama 7B Instruct model using Hugging Face transformers.
It is intended as a base for future fine-tuning using LoRA (Low-Rank Adaptation) of the model.

The current version loads the model and accepts interactive input from the terminal.
1. Install the required packages:
   pip install -r requirements.txt
   
2. Run the script using:
    python local_model/local_test.py
  This script loads the tokenizer and model then runs the model on your input and print the result

   Example input:
     You: Write a Python function to reverse a list.
   Output:
     def reverse_list(my_list):
        return my_list[::-1]
     This code will work for all lists, not just the ones with only numbers.
