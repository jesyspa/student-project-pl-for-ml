# CodeLlama 7B Local Test 

1. Install the required packages:
  pip install torch transformers accelerate

3. Run the script using:
    python Codellama/local_test.py
  This script loads the tokenizer and model then runs the model on your input and print the result

   Example input:
     You: Write a Python function to reverse a list.
   Output:
     def reverse_list(my_list):
        return my_list[::-1]
     This code will work for all lists, not just the ones with only numbers.
