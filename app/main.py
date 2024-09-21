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
    i = 0
    length = len(file_contents)

    while i < length:
        c = file_contents[i]

        # Check for multi-character tokens like '==', '!=', '<=', '>=' and comments
        if c == "=" and i + 1 < length and file_contents[i + 1] == "=":
            print("EQUAL_EQUAL == null")
            i += 2  # Move past the two-character token
        elif c == "=":
            print("EQUAL = null")
            i += 1
        elif c == "!" and i + 1 < length and file_contents[i + 1] == "=":
            print("BANG_EQUAL != null")
            i += 2  # Move past the two-character token
        elif c == "!":
            print("BANG ! null")
            i += 1
        elif c == "<" and i + 1 < length and file_contents[i + 1] == "=":
            print("LESS_EQUAL <= null")
            i += 2  # Move past the two-character token
        elif c == "<":
            print("LESS < null")
            i += 1
        elif c == ">" and i + 1 < length and file_contents[i + 1] == "=":
            print("GREATER_EQUAL >= null")
            i += 2  # Move past the two-character token
        elif c == ">":
            print("GREATER > null")
            i += 1
        elif c == "/" and i + 1 < length and file_contents[i + 1] == "/":
            # Comment: skip until the end of the line
            while i < length and file_contents[i] != "\n":
                i += 1
        elif c == "/":
            print("SLASH / null")
            i += 1
        elif c == "(":
            print("LEFT_PAREN ( null")
            i += 1
        elif c == ")":
            print("RIGHT_PAREN ) null")
            i += 1
        elif c == "{":
            print("LEFT_BRACE { null")
            i += 1
        elif c == "}":
            print("RIGHT_BRACE } null")
            i += 1
        elif c == "*":
            print("STAR * null")
            i += 1
        elif c == ".":
            print("DOT . null")
            i += 1
        elif c == ",":
            print("COMMA , null")
            i += 1
        elif c == "-":
            print("MINUS - null")
            i += 1
        elif c == "+":
            print("PLUS + null")
            i += 1
        elif c == ";":
            print("SEMICOLON ; null")
            i += 1
        elif c == "\n":
            # Move past newline without doing anything
            i += 1
        else:
            # Handle unexpected characters (lexical errors)
            print(f"[line 1] Error: Unexpected character: {c}", file=sys.stderr)
            has_error = True
            i += 1

    # Print EOF at the end
    print("EOF  null")  # Ensure there are exactly two spaces between 'EOF' and 'null'

    # Exit with code 65 if there were any lexical errors, otherwise 0
    if has_error:
        exit(65)
    else:
        exit(0)

if __name__ == "__main__":
    main()
