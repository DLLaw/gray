import sys

class Gray:
    had_error = False

    @staticmethod
    def main():
        args = sys.argv[1:]
        if len(args) > 1:
            print("Usage: python src/gray.py [script.gray]")
            sys.exit(64)
        elif len(args) == 1:
            Gray.run_file(args[0])
        else:
            Gray.run_prompt()

    @staticmethod
    def run_file(path: str):
        try:
            with open(path, "r", encoding="utf-8") as file:
                Gray.run(file.read())
            if Gray.had_error:
                sys.exit(65)
        except FileNotFoundError:
            print(f"Error: Could not open file '{path}'.")
            sys.exit(74)

    @staticmethod
    def run_prompt():
        while True:
            try:
                line = input("> ")
                if line is None:
                    break
                Gray.run(line)
                Gray.had_error = False
            except (KeyboardInterrupt, EOFError):
                print("\nExiting REPL...")
                break

    @staticmethod
    def run(source: str):
        # Initial stub required for Lab 1
        print("Scanner Not Implemented")

if __name__ == "__main__":
    Gray.main()