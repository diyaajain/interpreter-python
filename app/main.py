import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    try:
        with open(filename) as file:
            file_contents = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found", file=sys.stderr)
        exit(1)

    has_error = False

    for c in file_contents:
        if c == "(":
            print("LEFT_PAREN ( null")
        elif c == ")":
            print("RIGHT_PAREN ) null")
        elif c == "{":
            print("LEFT_BRACE { null")
        elif c == "}":
            print("RIGHT_BRACE } null")
        elif c == "*":
            print("STAR * null")
        elif c == ".":
            print("DOT . null")
        elif c == ",":
            print("COMMA , null")
        elif c == "-":
            print("MINUS - null")
        elif c == "+":
            print("PLUS + null")
        elif c == ";":
            print("SEMICOLON ; null")
        elif c == "=":
            print("EQUAL = null")
        elif c == "==":
            print("EQUAL_EQUAL == null")
        else:
            # Handle unexpected characters (lexical errors)
            print(f"[line 1] Error: Unexpected character: {c}", file=sys.stderr)
            has_error = True

    print("EOF  null")  # Ensure there are exactly two spaces between 'EOF' and 'null'


    # Exit with code 65 if there were any lexical errors, otherwise 0
    if has_error:
        exit(65)
    else:
        exit(0)

if __name__ == "__main__":
    main()
