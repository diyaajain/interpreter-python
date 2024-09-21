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
    line_number = 1

    while i < length:
        c = file_contents[i]

        # Ignore whitespace characters, track line numbers for newlines
        if c == ' ' or c == '\t':
            i += 1
            continue
        elif c == '\n':
            line_number += 1
            i += 1
            continue

        # Handle string literals
        if c == '"':
            string_start = i
            i += 1
            string_content = ""

            while i < length and file_contents[i] != '"':
                if file_contents[i] == '\n':  # Unterminated string at newline
                    print(f"[line {line_number}] Error: Unterminated string.", file=sys.stderr)
                    has_error = True
                    break
                string_content += file_contents[i]
                i += 1

            if i < length and file_contents[i] == '"':
                # Properly terminated string
                i += 1  # Move past the closing "
                lexeme = file_contents[string_start:i]
                print(f'STRING {lexeme} {string_content}')
            else:
                has_error = True  # Unterminated string, no closing quote

        # Check for multi-character tokens like '==', '!=', '<=', '>=' and comments
        elif c == "=" and i + 1 < length and file_contents[i + 1] == "=":
            print("EQUAL_EQUAL == null")
            i += 2
        elif c == "=":
            print("EQUAL = null")
            i += 1
        elif c == "!" and i + 1 < length and file_contents[i + 1] == "=":
            print("BANG_EQUAL != null")
            i += 2
        elif c == "!":
            print("BANG ! null")
            i += 1
        elif c == "<" and i + 1 < length and file_contents[i + 1] == "=":
            print("LESS_EQUAL <= null")
            i += 2
        elif c == "<":
            print("LESS < null")
            i += 1
        elif c == ">" and i + 1 < length and file_contents[i + 1] == "=":
            print("GREATER_EQUAL >= null")
            i += 2
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
        else:
            # Handle unexpected characters (lexical errors)
            print(f"[line {line_number}] Error: Unexpected character: {c}", file=sys.stderr)
            has_error = True
            i += 1

    # Print EOF at the end
    print("EOF  null")

    # Exit with code 65 if there were any lexical errors, otherwise 0
    if has_error:
        exit(65)
    else:
        exit(0)

if __name__ == "__main__":
    main()
