import sys
import os


def main():
    if len(sys.argv) != 2:
        print("Usage: generate_ast <output directory>", file=sys.stderr)
        sys.exit(64)

    output_dir = sys.argv[1]

    define_ast(output_dir, "Expr", [
        "Literal  : value",
        "Variable : name",
        "List     : elements"
    ])


def define_ast(output_dir, base_name, types):
    path = os.path.join(output_dir, f"{base_name}.py")
    with open(path, "w") as f:
        f.write(f"class {base_name}:\n")
        f.write("    def accept(self, visitor):\n")
        f.write("        raise NotImplementedError()\n\n\n")

        f.write(f"class {base_name}Visitor:\n")
        for type_def in types:
            class_name = type_def.split(":")[0].strip()
            f.write(f"    def visit_{class_name}_{base_name}(self, {base_name.lower()}):\n")
            f.write("        pass\n\n")

        for type_def in types:
            class_name, fields = [part.strip() for part in type_def.split(":")]
            fields = [field.strip() for field in fields.split(",")]

            f.write("\n")
            f.write(f"class {class_name}({base_name}):\n")
            f.write(f"    def __init__(self, {', '.join(fields)}):\n")
            for field in fields:
                f.write(f"        self.{field} = {field}\n")
            f.write("\n")
            f.write(f"    def accept(self, visitor):\n")
            f.write(f"        return visitor.visit_{class_name}_{base_name}(self)\n")
            f.write("\n")


if __name__ == "__main__":
    main()
