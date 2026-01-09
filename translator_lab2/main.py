import sys
from translator import CppToPythonTranslator
from utils import read_file, write_file

def main():
    sys.argv = ["main.py", "example.cpp", "example.py"]
    if len(sys.argv) != 3:
        print("Error: enough files")
        return

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    cpp_code = read_file(input_path)

    translator = CppToPythonTranslator()
    py_code = translator.translate(cpp_code)

    write_file(output_path, py_code)

    print(f"Translation finished: from {input_path} to {output_path}")


if __name__ == "__main__":
    main()
