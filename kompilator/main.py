import sys

from src.compiler import compile_pascal_to_c


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python main.py <input.pas> <output.c>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, "r", encoding="utf-8") as f:
        source = f.read()

    c_code = compile_pascal_to_c(source)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(c_code)


if __name__ == "__main__":
    main()

