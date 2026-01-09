import re

class CppToPythonTranslator:
    def __init__(self):
        self.indent = 0

    def translate(self, code: str) -> str:
        self.indent = 0
        prepared = code.replace("{", "\n{\n").replace("}", "\n}\n")
        lines = prepared.splitlines()
        result = []

        for line in lines:
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            if line == "}":
                self.indent -= 1
                continue
            py_line = self.translate_line(line)
            if py_line:
                result.append("    " * self.indent + py_line)

            if line.endswith("{"):
                self.indent += 1

        return "\n".join(result)

    def translate_line(self, line: str) -> str:
        line = line.rstrip(";").replace("{", "").strip()
        match = re.match(r"(int|double|void)\s+(\w+)\s*\((.*?)\)", line)
        if match:
            _, name, args = match.groups()
            py_args = []

            if args.strip():
                for arg in args.split(","):
                    arg = arg.strip()
                    arg = re.sub(r"(vector<\w+>\s*&?)|(int|double)", "", arg)
                    arg = arg.replace("[]", "").strip()
                    py_args.append(arg)

            return f"def {name}({', '.join(py_args)}):"

        match = re.match(r"vector<\w+>\s+(\w+)$", line)
        if match:
            return f"{match.group(1)} = []"

        match = re.match(r"vector<\w+>\s+(\w+)\((.+)\)", line)
        if match:
            name, size = match.groups()
            return f"{name} = [0] * {size}"

        match = re.match(r"vector<\w+>\s+(\w+)\s*=\s*\{(.+)\}", line)
        if match:
            name, values = match.groups()
            return f"{name} = [{values}]"

        match = re.match(r"(int|double)\s+(\w+)\[(\d+)\]", line)
        if match:
            _, name, size = match.groups()
            return f"{name} = [0] * {size}"

        match = re.match(r"(int|double)\s+(\w+)\s*=\s*(.+)", line)
        if match:
            _, var, value = match.groups()
            return f"{var} = {value}"

        match = re.match(r"(int|double)\s+(\w+)$", line)
        if match:
            return f"{match.group(2)} = 0"

        match = re.match(r"cin\s*>>\s*(.+)", line)
        if match:
            return f"{match.group(1)} = int(input())"

        match = re.match(r"(\w+)\.push_back\((.+)\)", line)
        if match:
            v, value = match.groups()
            return f"{v}.append({value})"

        line = re.sub(r"(\w+)\.size\(\)", r"len(\1)", line)

        if line.startswith("cout"):
            parts = re.findall(r"<<\s*([^<]+)", line)
            parts = [p.strip() for p in parts if p.strip() != "endl"]
            return f"print({', '.join(parts)})"

        match = re.match(r"if\s*\((.+)\)", line)
        if match:
            return f"if {match.group(1)}:"

        match = re.match(r"else if\s*\((.+)\)", line)
        if match:
            return f"elif {match.group(1)}:"

        if line == "else":
            return "else:"

        match = re.match(r"for\s*\(\s*int\s+(\w+)\s*=\s*(\d+)\s*;\s*\1\s*<\s*(.+)\s*;\s*\1\+\+\s*\)", line)
        if match:
            var, start, end = match.groups()
            return f"for {var} in range({start}, {end}):"

        match = re.match(r"return\s+(.+)", line)
        if match:
            return f"return {match.group(1)}"

        return line
