import os
from nelox.pretty_printer import pretty_program
from Fuzzer import Fuzzer

class Saver:
    def __init__(self, output_dir="dataset"):
        self.output_dir = output_dir
        self.num_samples = 5
        os.makedirs(output_dir, exist_ok=True)

    def save(self):
        for i in range(self.num_samples):
            fuzzer = Fuzzer()
            program = fuzzer.generate_program()
            code = pretty_program(program)
            with open(os.path.join(self.output_dir, f"sample_{i + 1}.txt"), "w") as f:
                f.write(code)


if __name__ == "__main__":
    Saver().save()